Collectd Cgroups
================

Yet another cgroups plugin for collectd.

You can hide cgroups with patterns, and later, monitoring memory.

There is an official C plugin for collectd, but it handles only cpuacct values, and doesn't handle patterns.

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
