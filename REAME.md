Collectd Cgroups
================

Yet another cgroups plugin for collectd.

You can hide cgroups with patterns, and later, monitoring memory.


    LoadPlugin Python

    <Plugin Python>
        ModulePath "/opt/collectd_cgroups/"
        LogTraces true
        Interactive false
        Import "cgroups"
        <Module cgroups>
                hide "systemd-*" "dev-*" "*.mount" "udev-finish.service" "kmod-static-nodes.service" "irqbalance.service" "dbus.service" "debian-fixup.service" "networking.service" "system-getty.slice"
        </Module>
    </Plugin>

Licence
-------

GPLv2, © 2015 Mathieu Lecarme, just like Collectd.
