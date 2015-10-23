#!/usr/bin/env python
from os import walk
from os.path import join
from fnmatch import fnmatch

bad_boys = set()


def find_cpuacct(hides=[]):
    global bad_boys
    ROOT = '/sys/fs/cgroup/cpu,cpuacct/system.slice/'
    for root, dirs, files in walk(ROOT):
        if root == ROOT:
            continue
        if 'cpuacct.stat' in files:
            top = root.split('/')[-1]
            if top in bad_boys:
                continue
            h = False
            for hide in hides:
                h = h or fnmatch(top, hide)
            if h:
                bad_boys.add(top)
                continue
            kv = dict()
            for line in open(join(root, 'cpuacct.stat'), 'r').readlines():
                k, v = line[:-1].split(' ')
                v = int(v)
                kv[k] = v
            yield top, kv


def cpuacct(group):
    kv = dict()
    for line in open('/sys/fs/cgroup/cpu,cpuacct/system.slice/%s/cpuacct.stat'
                     % group, 'r'):
        k, v = line[:-1].split(' ')
        v = int(v)
        kv[k] = v
    return kv

try:
    import collectd
except ImportError:
    # we're not running inside collectd
    # it's ok
    pass
else:

    def logger(t, msg):
        if t == 'err':
            collectd.error('%s: %s' % (NAME, msg))
        elif t == 'warn':
            collectd.warning('%s: %s' % (NAME, msg))
        elif t == 'info':
            collectd.info('%s: %s' % (NAME, msg))
        else:
            collectd.notice('%s: %s' % (NAME, msg))

    NAME = "cgroups"
    hides = set()
    modes = set()

    def config_callback(conf):
        global hides
        global modes
        MODES = set(['user', 'system', 'total'])
        for node in conf.children:
            if node.key.lower() == "hide":
                hides.update(node.values)
                logger('info', "Hidding cgroups %s" % ", ".join(node.values))
            elif node.key.lower() == "mode":
                aliens = set(node.values).difference(MODES)
                if aliens:
                    logger('warn', "Strange mode options : %s" %
                           ", ".join(aliens))
                modes = MODES.intersection(node.values)
            else:
                logger('info', "unknown config key in cgroups module: %s"
                       % node.key)
        if not(modes):
            modes = set(['user', 'system'])

    def read_callback():
        global hides
        global modes
        for group, values in find_cpuacct(hides):
            for us in modes:
                val = collectd.Values(plugin=NAME, type="absolute")
                if us == 'total':
                    val.values = [values['user'] + values['system']]
                else:
                    val.values = [values[us]]
                val.type = "absolute"
                val.type_instance = ".".join(group.replace('.', '_').split('/')
                                             + [us])
                val.dispatch()

    collectd.register_config(config_callback)
    collectd.register_read(read_callback)


if __name__ == '__main__':
    import sys
    for g, v in find_cpuacct(sys.argv[1:]):
        print(g)
