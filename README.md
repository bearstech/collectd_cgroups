Collectd Cgroups
================

Yet another cgroups plugin for collectd.

You can hide cgroups with patterns, and later, monitoring memory.

There is an official Cgroups C plugin for collectd, but it handles only cpuacct values, and doesn't handle patterns.

Debian
------

This plugin is tested with Debian Jessie.

One of your service has to active CPUAccounting :

    [Service]
    CPUAccounting=true

After that, you will see something in the path :

    ls /sys/fs/cgroup/cpu,cpuacct/system.slice/

Configure
---------

### hide

Path like pattern for hidding strange systemd stuff

### mode

user, system, total. Pick none or more.

### Collectd configuration file

    LoadPlugin Python

    <Plugin Python>
        ModulePath "/opt/collectd_cgroups/"
        LogTraces true
        Interactive false
        Import "cgroups"
        <Module cgroups>
                hide "systemd-*" "dev-*" "*.mount" "udev-finish.service" "kmod-static-nodes.service" "irqbalance.service" "dbus.service" "debian-fixup.service" "networking.service" "system-getty.slice"
                mode "total"
        </Module>
    </Plugin>

Licence
-------

GPLv2, © 2015 Mathieu Lecarme, just like Collectd.
