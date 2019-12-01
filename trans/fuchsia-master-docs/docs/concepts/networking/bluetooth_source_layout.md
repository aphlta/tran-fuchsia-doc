 
# Bluetooth Source Layout  蓝牙源布局 

The [Bluetooth System](/docs/concepts/networking/bluetooth_architecture.md) comprises many components, such as drivers, profiles, and clientapplications. This document provides an overview of where the various componentslive in the source tree. [蓝牙系统]（/ docs / concepts / networking / bluetooth_architecture.md）包含许多组件，例如驱动程序，配置文件和客户端应用程序。本文档概述了各种组件在源代码树中的位置。

<!-- This was generated by running <！-这是通过运行生成的

$ (find . -name BUILD.gn -o -name rules.mk | egrep 'bt|bluetooth'; find . -name BUILD.gn | xargs grep -l 'fidl:bluetooth') \| sort | uniq $（查找。-name BUILD.gn -o -name rules.mk | egrep'bt | blue';找到。-name BUILD.gn | xargs grep -l'fidl：bluetooth'）\ |排序优衣库

And then culling and annotating by hand. --> 然后手动剔除和注释。 ->

```
src/connectivity/bluetooth/
    core/
        bt-gap/              # GAP daemon
        bt-host/             # bt-host driver and host subsystem
        bt-init/             # Bluetooth subsystem launcher
    examples/                # various LE API examples
    hci/                     # bt-hci drivers
    lib/                     # protocol and rust utility libraries
    profiles/                # profile components (A2DP, AVRCP, HID over GATT, etc)
    tests/                   # integration tests
    tools/                   # command-line tools and debug components

sdk/fidl/fuchsia.bluetooth.*                    # public API
topaz/bin/bluetooth_settings/                   # Bluetooth Settings UI
topaz/examples/eddystone_agent/                 # [Eddystone](https://github.com/google/eddystone)-based trigger
zircon/system/dev/bluetooth/                    # bt-transport drivers
```
 

See the [HCI section of the Bluetooth System document](/docs/concepts/networking/bluetooth_architecture.md#hci) for an explanation of how the drivers, such as `bt-transport`, `bt-hci`, and `bt-host`, relate to each other.  请参阅[Bluetooth系统文档的[HCI]部分]（/ docs / concepts / networking / bluetooth_architecture.mdhci），以获取有关如何驱动程序（例如bt-transport，bt-hci和bt-host）的说明。 `，彼此相关。
