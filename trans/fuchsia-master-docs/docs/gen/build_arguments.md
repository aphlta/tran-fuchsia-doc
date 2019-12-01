 
# GN Build Arguments  GN构建参数 

 
## All builds  所有版本 

 
### active_partition  active_partition 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:47  来自//build/images/BUILD.gn:47

 
### add_qemu_to_build_archives  add_qemu_to_build_archivesWhether to include images necessary to run Fuchsia in QEMU in build archives. 是否在构建档案中包括在QEMU中运行Fuchsia所需的图像。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/images/BUILD.gn:53  来自//build/images/BUILD.gn:53

 
### additional_bootserver_arguments  Additional_bootserver_argumentsAdditional bootserver args to add to pave.sh. New uses of this should be added with caution, and ideally discussion. The present use case is toenable throttling of netboot when specific network adapters are combinedwith specific boards, due to driver and hardware challenges. 要添加到pave.sh的其他引导服务器参数。应谨慎添加此功能的新用法，最好是进行讨论。当前的使用案例是当特定的网络适配器与特定的板卡组合在一起时，由于驱动程序和硬件的挑战，可以启用netboot的限制。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:59  来自//build/images/BUILD.gn:59

 
### always_zedboot  always_zedbootBuild boot images that prefer Zedboot over local boot (only for EFI).  构建比Zedboot优先于本地引导的引导映像（仅适用于EFI）。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/images/BUILD.gn:897  来自//build/images/BUILD.gn:897

 
### auto_login_to_guest  auto_login_to_guestWhether basemgr should automatically login as a persistent guest user.  basemgr是否应自动以永久访客用户身份登录。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //src/modular/bin/basemgr/BUILD.gn:14  来自//src/modular/bin/basemgr/BUILD.gn:14

 
### auto_update_packages  auto_update_packagesWhether the component loader should automatically update packages.  组件加载器是否应自动更新软件包。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/bin/sysmgr/BUILD.gn:10  来自//garnet/bin/sysmgr/BUILD.gn:10

 
### avb_algorithm  avb_algorithmAVB algorithm type.Supported options: SHA256_RSA2048SHA256_RSA4096SHA256_RSA8192SHA512_RSA2048SHA512_RSA4096SHA512_RSA8192 AVB算法类型。支持的选项：SHA256_RSA2048SHA256_RSA4096SHA256_RSA8192SHA512_RSA2048SHA512_RSA4096SHA512_RSA8192

**Current value (from the default):** `"SHA512_RSA4096"`  **当前值（默认值）：**`“ SHA512_RSA4096”`

From //build/images/vbmeta.gni:25  来自//build/images/vbmeta.gni:25

 
### avb_atx_metadata  avb_atx_metadataAVB metadata which will be used to validate public key  AVB元数据将用于验证公钥

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/vbmeta.gni:16  来自//build/images/vbmeta.gni:16

 
### avb_key  avb_keya key which will be used to sign VBMETA and images for AVB  一个将用于签署VBMETA和AVB图像的密钥

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/vbmeta.gni:13  来自//build/images/vbmeta.gni:13

 
### base_package_labels  base_package_labelsIf you add package labels to this variable, the packages will be included in the 'base' package set, which represents the set of packages that are partof an OTA. These pacakages are updated as an atomic unit during an OTAprocess and are immutable and are a superset of the TCB (Trusted ComputingBase) for a product. These packages are never evicted by the system. 如果将软件包标签添加到此变量，则这些软件包将包含在“基本”软件包集中，该“基本”软件包集表示属于OTA的一组软件包。这些功能在OTA流程中作为原子单位进行更新，并且是不变的，并且是产品TCB（受信任计算库）的超集。这些软件包永远不会被系统收回。

**Current value for `target_cpu = "arm64"`:** `["//build/info:build-info", "//garnet/bin/appmgr", "//garnet/bin/appmgr:appmgr_scheme_config", "//garnet/bin/device_settings:device_settings_manager", "//garnet/bin/http", "//garnet/bin/log_listener:log_listener", "//garnet/bin/log_listener:log_listener_shell", "//garnet/bin/logger", "//garnet/bin/net-cli", "//garnet/bin/netcfg", "//garnet/bin/netcfg:config", "//garnet/bin/network_time_service", "//garnet/bin/pkg_cache", "//garnet/bin/pkg_resolver", "//garnet/bin/scpi", "//garnet/bin/setui:setui_service", "//garnet/bin/sshd-host", "//garnet/bin/sshd-host:config", "//garnet/bin/stash:stash", "//garnet/bin/stash_ctl:stash_ctl", "//garnet/bin/sysmgr", "//garnet/bin/sysmgr:network_config", "//garnet/bin/sysmgr:services_config", "//garnet/bin/system-update-checker", "//garnet/bin/system-update-checker:system-update-checker-config", "//garnet/bin/thermd", "//garnet/bin/thermd:config", "//garnet/bin/timezone", "//garnet/go/src/amber", "//garnet/go/src/amber:amber_tools", "//garnet/go/src/amber:config", "//garnet/go/src/amber:pkgfs", "//garnet/lib/root_ssl_certificates", "//src/cobalt/bin/app:cobalt", "//src/cobalt/bin/system-metrics:cobalt_system_metrics", "//src/connectivity/bluetooth:core", "//src/connectivity/network/mdns/bundles:config", "//src/connectivity/network/mdns/bundles:services", "//src/connectivity/network/netdump", "//src/connectivity/network/netstack", "//src/connectivity/wlan:service", "//src/developer/exception_broker", "//src/developer/feedback/bugreport", "//src/developer/feedback/crashpad_agent", "//src/developer/feedback/feedback_agent", "//src/developer/feedback/kernel_crash_checker", "//src/developer/feedback/kernel_crash_checker:config", "//src/identity/bin:core", "//src/recovery/factory_reset", "//src/sys/timekeeper", "//third_party/openssh-portable/fuchsia/developer-keys:ssh_config", "//bundles:kitchen_sink"]`  ** target_cpu =“ arm64”的当前值：**`[“ // build / info：build-info”，“ // garnet / bin / appmgr”，“ // garnet / bin / appmgr：appmgr_scheme_config” ，“ // garnet / bin / device_settings：device_settings_manager”，“ // garnet / bin / http”，“ // garnet / bin / log_listener：log_listener”，“ // garnet / bin / log_listener：log_listener_shell”，“ // garnet / bin / logger”，“ // garnet / bin / net-cli”，“ // garnet / bin / netcfg”，“ // garnet / bin / netcfg：config”，“ // garnet / bin / network_time_service” ，“ // garnet / bin / pkg_cache”，“ // garnet / bin / pkg_resolver”，“ // garnet / bin / scpi”，“ // garnet / bin / setui：setui_service”，“ // garnet / bin / sshd-host“，” // garnet / bin / sshd-host：config“，” // garnet / bin / stash：stash“，” // garnet / bin / stash_ctl：stash_ctl“，” // garnet / bin / sysmgr“，” // garnet / bin / sysmgr：network_config“，” // garnet / bin / sysmgr：services_config“，” // garnet / bin / system-update-checker“，” // garnet / bin / system- update-checker：system-update-checker-config“，” // garnet / bin / thermd“，” // garnet / bin / thermd：config“，” // garnet / bin /时区“，” // garnet / go / src / amber“，” // garnet / g o / src / amber：amber_tools“，” // garnet / go / src / amber：config“，” // garnet / go / src / amber：pkgfs“，” // garnet / lib / root_ssl_certificates“，” // src / cobalt / bin / app：cobalt“，” // src / cobalt / bin / system-metrics：cobalt_system_metrics“，” // src / connectivity / bluetooth：core“，” // src / connectivity / network / mdns / bundles：config“，” // src / connectivity / network / mdns / bundles：services“，” // src / connectivity / network / netdump“，” // src / connectivity / network / netstack“，” // src /连接性/ WLAN：服务”，“ // src / developer / exception_broker”，“ // src / developer / feedback / bugreport”，“ // src / developer / feedback / crashpad_agent”，“ // src / developer / feedback / feedback_agent“，” // src / developer / feedback / kernel_crash_checker“，” // src / developer / feedback / kernel_crash_checker：config“，” // src / identity / bin：core“，” // src / recovery / factory_reset“ ，“ // src / sys / timekeeper”，“ // third_party / openssh-portable / fuchsia / developer-keys：ssh_config”，“ // bundles：kitchen_sink”]“

From //root_build_dir/args.gn:3  来自//root_build_dir/args.gn:3

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //BUILD.gn:18  来自//BUILD.gn:18

**Current value for `target_cpu = "x64"`:** `["//build/info:build-info", "//garnet/bin/appmgr", "//garnet/bin/appmgr:appmgr_scheme_config", "//garnet/bin/device_settings:device_settings_manager", "//garnet/bin/http", "//garnet/bin/log_listener:log_listener", "//garnet/bin/log_listener:log_listener_shell", "//garnet/bin/logger", "//garnet/bin/net-cli", "//garnet/bin/netcfg", "//garnet/bin/netcfg:config", "//garnet/bin/network_time_service", "//garnet/bin/pkg_cache", "//garnet/bin/pkg_resolver", "//garnet/bin/scpi", "//garnet/bin/setui:setui_service", "//garnet/bin/sshd-host", "//garnet/bin/sshd-host:config", "//garnet/bin/stash:stash", "//garnet/bin/stash_ctl:stash_ctl", "//garnet/bin/sysmgr", "//garnet/bin/sysmgr:network_config", "//garnet/bin/sysmgr:services_config", "//garnet/bin/system-update-checker", "//garnet/bin/system-update-checker:system-update-checker-config", "//garnet/bin/thermd", "//garnet/bin/thermd:config", "//garnet/bin/timezone", "//garnet/go/src/amber", "//garnet/go/src/amber:amber_tools", "//garnet/go/src/amber:config", "//garnet/go/src/amber:pkgfs", "//garnet/lib/root_ssl_certificates", "//src/cobalt/bin/app:cobalt", "//src/cobalt/bin/system-metrics:cobalt_system_metrics", "//src/connectivity/bluetooth:core", "//src/connectivity/network/mdns/bundles:config", "//src/connectivity/network/mdns/bundles:services", "//src/connectivity/network/netdump", "//src/connectivity/network/netstack", "//src/connectivity/wlan:service", "//src/developer/exception_broker", "//src/developer/feedback/bugreport", "//src/developer/feedback/crashpad_agent", "//src/developer/feedback/feedback_agent", "//src/developer/feedback/kernel_crash_checker", "//src/developer/feedback/kernel_crash_checker:config", "//src/identity/bin:core", "//src/recovery/factory_reset", "//src/sys/timekeeper", "//third_party/openssh-portable/fuchsia/developer-keys:ssh_config", "//bundles:kitchen_sink"]`  ** target_cpu =“ x64”`的当前值：**`[“ // build / info：build-info”，“ // garnet / bin / appmgr”，“ // garnet / bin / appmgr：appmgr_scheme_config” ，“ // garnet / bin / device_settings：device_settings_manager”，“ // garnet / bin / http”，“ // garnet / bin / log_listener：log_listener”，“ // garnet / bin / log_listener：log_listener_shell”，“ // garnet / bin / logger”，“ // garnet / bin / net-cli”，“ // garnet / bin / netcfg”，“ // garnet / bin / netcfg：config”，“ // garnet / bin / network_time_service” ，“ // garnet / bin / pkg_cache”，“ // garnet / bin / pkg_resolver”，“ // garnet / bin / scpi”，“ // garnet / bin / setui：setui_service”，“ // garnet / bin / sshd-host“，” // garnet / bin / sshd-host：config“，” // garnet / bin / stash：stash“，” // garnet / bin / stash_ctl：stash_ctl“，” // garnet / bin / sysmgr“，” // garnet / bin / sysmgr：network_config“，” // garnet / bin / sysmgr：services_config“，” // garnet / bin / system-update-checker“，” // garnet / bin / system- update-checker：system-update-checker-config“，” // garnet / bin / thermd“，” // garnet / bin / thermd：config“，” // garnet / bin /时区“，” // garnet / go / src / amber“，” // garnet / go / src / amber：amber_tools“，” // garnet / go / src / amber：config“，” // garnet / go / src / amber：pkgfs“，” // garnet / lib / root_ssl_certificates“，” // src / cobalt / bin / app：cobalt“，” // src / cobalt / bin / system-metrics：cobalt_system_metrics“，” // src / connectivity / bluetooth：core“，” // src / connectivity / network / mdns / bundles： config”，“ // src / connectivity / network / mdns / bundles：services”，“ // src / connectivity / network / netdump”，“ // src / connectivity / network / netstack”，“ // src / connectivity / wlan：service“，” // src / developer / exception_broker“，” // src / developer / feedback / bugreport“，” // src / developer / feedback / crashpad_agent“，” // src / developer / feedback / feedback_agent“ ，“ // src / developer / feedback / kernel_crash_checker”，“ // src / developer / feedback / kernel_crash_checker：config”，“ // src / identity / bin：core”，“ // src / recovery / factory_reset”，“ // src / sys / timekeeper“，” // third_party / openssh-portable / fuchsia / developer-keys：ssh_config“，” // bundles：kitchen_sink“]`

From //root_build_dir/args.gn:3  来自//root_build_dir/args.gn:3

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //BUILD.gn:18  来自//BUILD.gn:18

 
### blobfs_maximum_bytes  blobfs_maximum_bytesIn addition to reserving space for inodes and data, fs needs additional space for maintaining some internal data structures. So thespace required to reserve inodes and data may exceed sum of the spaceneeded for inodes and data.maximum_bytes puts an upper bound on the total bytes reserved for inodes,data bytes and reservation for all other internal fs metadata.An empty string does not put any upper bound. A filesystem mayreserve few blocks required for its operations. 除了为索引节点和数据保留空间外，fs还需要其他空间来维护一些内部数据结构。因此保留索引节点和数据所需的空间可能超过了索引节点和数据所需的空间之和。maximum_bytes为索引节点保留的总字节数，数据字节和所有其他内部fs元数据的保留数上限。上限。文件系统可能会保留其操作所需的几个块。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/fvm.gni:47  来自//build/images/fvm.gni:47

 
### blobfs_minimum_data_bytes  blobfs_minimum_data_bytesNumber of bytes to reserve for data in the fs. This is in addition to what is reserved, if any, for the inodes. Data bytes constitutes"usable" space of the fs.An empty string does not reserve any additional space than minimumrequired for the filesystem. 在fs中为数据保留的字节数。这是为索引节点保留的内容（如果有）的补充。数据字节构成fs的“可用”空间。空字符串不会保留任何超出文件系统所需最小空间的额外空间。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/fvm.gni:36  来自//build/images/fvm.gni:36

 
### blobfs_minimum_inodes  blobfs_minimum_inodesminimum_inodes is the number of inodes to reserve for the fs An empty string does not reserve any additional space than minimumrequired for the filesystem. minimum_inodes是为fs保留的inode数。空字符串不保留超出文件系统所需的最小值的任何其他空间。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/fvm.gni:28  来自//build/images/fvm.gni:28

 
### board_has_libvulkan_arm_mali  board_has_libvulkan_arm_maliBoard files can set this to true if they have a package with a mali libvulkan VCD.  如果棋盘文件包含带有Mali libvulkan VCD的软件包，则可以将其设置为true。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //garnet/lib/magma/gnbuild/magma.gni:51  来自//garnet/lib/magma/gnbuild/magma.gni:51

 
### board_kernel_cmdline_args  board_kernel_cmdline_argsList of kernel command line this board to bake into the boot image that are required by this board. See also kernel_cmdline_args in//build/images/BUILD.gn 此板烘烤到该板所需的启动映像中的内核命令行列表。另请参阅//build/images/BUILD.gn中的kernel_cmdline_args

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/board.gni:16  来自//build/board.gni:16

 
### board_name  board_nameBoard name used for paving and amber updates.  用于铺路和琥珀色更新的木板名称。

**Current value for `target_cpu = "arm64"`:** `"qemu-arm64"`  ** target_cpu =“ arm64”`的当前值：**`“ qemu-arm64”`

From //boards/arm64.gni:7  来自//boards/arm64.gni:7

**Overridden from the default:** `""`  **从默认值覆盖：**`“”`

From //build/board.gni:7  来自//build/board.gni:7

**Current value for `target_cpu = "x64"`:** `"pc"`  ** target_cpu =“ x64”`的当前值：**`“ pc”

From //boards/x64.gni:7  从//boards/x64.gni:7

**Overridden from the default:** `""`  **从默认值覆盖：**`“”`

From //build/board.gni:7  来自//build/board.gni:7

 
### board_package_labels  board_package_labelsA list of package labels to include in the 'base' package set. Used by the board definition rather than the product definition. 要包括在“基本”包装集中的包装标签列表。由板定义而不是产品定义使用。

**Current value for `target_cpu = "arm64"`:** `["//garnet/packages/prod:drivers" ]`  ** target_cpu =“ arm64”`的当前值：**`[“ // garnet / packages / prod：drivers”]`

From //boards/arm64.gni:9  从//boards/arm64.gni:9

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //build/board.gni:11  来自//build/board.gni:11

**Current value for `target_cpu = "x64"`:** `["//garnet/packages/prod:drivers"]`  ** target_cpu =“ x64”`的当前值：**`[“ // garnet / packages / prod：drivers”]`

From //boards/x64.gni:9  从//boards/x64.gni:9

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //build/board.gni:11  来自//build/board.gni:11

 
### bootfs_extra  bootfs_extraList of extra manifest entries for files to add to the BOOTFS. Each entry can be a "TARGET=SOURCE" string, or it can be a scopewith `sources` and `outputs` in the style of a copy() target:`outputs[0]` is used as `TARGET` (see `gn help source_expansion`). 要添加到BOOTFS的文件的其他清单条目的列表。每个条目可以是“ TARGET = SOURCE”字符串，也可以是具有copy（）target样式的`sources`和`outputs`的作用域：`outputs [0]`用作`TARGET`（参见` gn help source_expansion`）。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/images/BUILD.gn:491  来自//build/images/BUILD.gn:491

 
### bootfs_only  bootfs_onlyPut the "system image" package in the BOOTFS.  Hence what would otherwise be /system/... at runtime is /boot/... instead. 将“系统映像”包放在BOOTFS中。因此，在运行时原本是/ system / ...的是/ boot /...。

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //products/core.gni:7  来自//products/core.gni:7

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //build/images/boot.gni:15  来自//build/images/boot.gni:15

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //products/core.gni:7  来自//products/core.gni:7

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //build/images/boot.gni:15  来自//build/images/boot.gni:15

 
### bootloader_hw_revision  bootloader_hw_revisionHW revision of the bootloader to be included into OTA package and paving process. Bootloader的HW修订版将包含在OTA软件包和铺路过程中。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:505  来自//build/images/BUILD.gn:505

 
### bootloader_prebuilt  bootloader_prebuiltPrebuilt bootloader image to be included into update (OTA) package and paving process. 预建的引导加载程序映像将包含在更新（OTA）软件包和摊铺过程中。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:501  来自//build/images/BUILD.gn:501

 
### build_info_board  build_info_boardBoard configuration of the current build  当前版本的主板配置

**Current value (from the default):** `"qemu-arm64"`  **当前值（默认值）：**`“ qemu-arm64”`

From //build/info/info.gni:12  来自//build/info/info.gni:12

 
### build_info_product  build_info_productProduct configuration of the current build  当前版本的产品配置

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/info/info.gni:9  来自//build/info/info.gni:9

 
### build_info_version  build_info_versionLogical version of the current build. If not set, defaults to the timestamp of the most recent update. 当前版本的逻辑版本。如果未设置，则默认为最新更新的时间戳。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/info/info.gni:16  来自//build/info/info.gni:16

 
### build_libvulkan_arm_mali  build_libvulkan_arm_maliTargets that will be built as mali vulkan ICDS.  将以马里武尔坎ICDS建立的目标。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //garnet/lib/magma/gnbuild/magma.gni:39  来自//garnet/lib/magma/gnbuild/magma.gni:39

 
### build_libvulkan_goldfish  build_libvulkan_goldfishThis is a list of targets that will be built as goldfish vulkan ICDs.  这是将作为金鱼vulkan ICD建立的目标列表。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //garnet/lib/goldfish-vulkan/gnbuild/BUILD.gn:15  来自//garnet/lib/goldfish-vulkan/gnbuild/BUILD.gn:15

 
### build_libvulkan_img_rgx  build_libvulkan_img_rgxTargets that will be built as IMG vulkan ICDS.  将作为IMG vulkan ICDS构建的目标。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //garnet/lib/magma/gnbuild/magma.gni:48  来自//garnet/lib/magma/gnbuild/magma.gni:48

 
### build_libvulkan_qcom_adreno  build_libvulkan_qcom_adrenoTargets that will be built as qualcomm vulkan ICDS.  将作为Qualcomm Vulkan ICDS构建的目标。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //garnet/lib/magma/gnbuild/magma.gni:45  来自//garnet/lib/magma/gnbuild/magma.gni:45

 
### build_libvulkan_vsl_gc  build_libvulkan_vsl_gcTargets that will be built as verisilicon vulkan ICDS.  将以verisilicon vulkan ICDS建立的目标。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //garnet/lib/magma/gnbuild/magma.gni:42  来自//garnet/lib/magma/gnbuild/magma.gni:42

 
### build_sdk_archives  build_sdk_archivesWhether to build SDK tarballs.  是否构建SDK tarball。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/sdk/config.gni:7  来自//build/sdk/config.gni:7

 
### cache_package_labels  cache_package_labelsIf you add package labels to this variable, the packages will be included in the 'cache' package set, which represents an additional set of softwarethat is made available on disk immediately after paving and in factoryflows. These packages are not updated with an OTA, but instead are updatedephemerally. This cache of software can be evicted by the system if storagepressure arises or other policies indicate. 如果将软件包标签添加到此变量，则软件包将包含在“缓存”软件包集中，这表示在铺装后和工厂流程中立即在磁盘上可用的另一组软件。这些软件包不使用OTA进行更新，而是临时更新。如果出现存储压力或其他策略指示，则系统可以收回此软件缓存。

**Current value for `target_cpu = "arm64"`:** `[]`  ** target_cpu =“ arm64”`的当前值：**`[]`

From //products/core.gni:71  来自//products/core.gni:71

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //BUILD.gn:26  来自//BUILD.gn:26

**Current value for `target_cpu = "x64"`:** `[]`  ** target_cpu =“ x64”`的当前值：**`[]`

From //products/core.gni:71  来自//products/core.gni:71

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //BUILD.gn:26  来自//BUILD.gn:26

 
### clang_lib_dir  clang_lib_dirPath to Clang lib directory.  Clang lib目录的路径。

**Current value (from the default):** `"../build/prebuilt/third_party/clang/linux-x64/lib"`  **当前值（默认值）：**`../ build / prebuilt / third_party / clang / linux-x64 / lib“`

From //build/images/manifest.gni:19  来自//build/images/manifest.gni:19

 
### clang_prefix  clang_prefixThe default clang toolchain provided by the prebuilt. This variable is additionally consumed by the Go toolchain. 预先提供的默认clang工具链。 Go工具链另外使用了此变量。

**Current value (from the default):** `"../prebuilt/third_party/clang/linux-x64/bin"`  **当前值（默认值）：**`../ prebuilt / third_party / clang / linux-x64 / bin“`

From //build/config/clang/clang.gni:11  来自//build/config/clang/clang.gni:11

 
### cloudkms_key_dir  cloudkms_key_dir 

**Current value (from the default):** `"projects/fuchsia-infra/locations/global/keyRings/test-secrets/cryptoKeys"`  **当前值（默认值）：**`““ projects / fuchsia-infra / locations / global / keyRings / test-secrets / cryptoKeys”

From //build/testing/secret_spec.gni:8  来自//build/testing/secret_spec.gni:8

 
### concurrent_dart_jobs  concurrent_dart_jobsMaximum number of Dart processes to run in parallel.  要并行运行的Dart进程的最大数量。

Dart analyzer uses a lot of memory which may cause issues when building with many parallel jobs e.g. when using goma. To avoid out-of-memoryerrors we explicitly reduce the number of jobs. Dart分析仪使用大量内存，在进行许多并行作业时可能会导致问题，例如使用goma时。为了避免出现内存不足错误，我们明确减少了作业数量。

**Current value (from the default):** `16`  **当前值（默认值）：**`16`

From //build/dart/BUILD.gn:15  来自//build/dart/BUILD.gn:15

 
### concurrent_go_jobs  concurrent_go_jobsMaximum number of Go processes to run in parallel.  要并行运行的Go进程的最大数量。

**Current value (from the default):** `16`  **当前值（默认值）：**`16`

From //build/go/BUILD.gn:11  来自//build/go/BUILD.gn:11

 
### concurrent_link_jobs  concurrent_link_jobsMaximum number of concurrent link jobs.  并发链接作业的最大数量。

We often want to run fewer links at once than we do compiles, because linking is memory-intensive. The default to use varies by platform and bythe amount of memory available, so we call out to a script to get the rightvalue. 我们通常希望一次运行的链接少于编译的链接，因为链接会占用大量内存。使用的默认值因平台和可用内存量而异，因此我们调出脚本来获取正确的值。

**Current value (from the default):** `16`  **当前值（默认值）：**`16`

From //build/toolchain/BUILD.gn:15  来自//build/toolchain/BUILD.gn:15

 
### concurrent_rust_jobs  concurrent_rust_jobsMaximum number of Rust processes to run in parallel.  并行运行的Rust进程的最大数量。

We run multiple rustc jobs in parallel, each of which can cause significant amount of memory, especially when using LTO. To avoid out-of-memory errorswe explicitly reduce the number of jobs. 我们并行运行多个rustc作业，每个作业都会导致大量内存，尤其是在使用LTO时。为避免内存不足错误，我们显式减少了作业数量。

**Current value (from the default):** `14`  **当前值（默认值）：**`14`

From //build/rust/BUILD.gn:15  来自//build/rust/BUILD.gn:15

 
### crash_diagnostics_dir  crash_diagnostics_dirClang crash reports directory path. Use empty path to disable altogether.  Clang崩溃报告目录路径。使用空路径将其完全禁用。

**Current value (from the default):** `"//root_build_dir/clang-crashreports"`  **当前值（默认值）：**`“ // root_build_dir / clang-crashreports”`

From //build/config/BUILD.gn:10  来自//build/config/BUILD.gn:10

 
### crashpad_dependencies  crashpad_dependencies 

**Current value (from the default):** `"fuchsia"`  **当前值（默认值）：**`“紫红色”

From [//third_party/crashpad/build/crashpad_buildconfig.gni:22](https://chromium.googlesource.com/crashpad/crashpad/+/63782c8333c98850c08b4cc000dba97fe533127f/build/crashpad_buildconfig.gni#22)  来自[//third_party/crashpad/build/crashpad_buildconfig.gni:22](https://chromium.googlesource.com/crashpad/crashpad/+/63782c8333c98850c08b4cc000dba97fe533127f/build/crashpad_buildconfig.gni22）

 
### crashpad_use_boringssl_for_http_transport_socket  crashpad_use_boringssl_for_http_transport_socketTODO(scottmg): https://crbug.com/crashpad/266 fuchsia:DX-690: BoringSSL was removed from the Fuchsia SDK. Re-enable it when we have a way to acquirea BoringSSL lib again. 待办事项（scottmg）：https://crbug.com/crashpad/266 fuchsia：DX-690：BoringSSL已从Fuchsia SDK中删除。当我们有办法再次获取BoringSSL lib时，请重新启用它。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From [//third_party/crashpad/util/net/tls.gni:21](https://chromium.googlesource.com/crashpad/crashpad/+/63782c8333c98850c08b4cc000dba97fe533127f/util/net/tls.gni#21)  来自[//third_party/crashpad/util/net/tls.gni:21](https://chromium.googlesource.com/crashpad/crashpad/+/63782c8333c98850c08b4cc000dba97fe533127f/util/net/tls.gni21）

 
### create_kernel_service_snapshot  create_kernel_service_snapshot 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:101  来自//third_party/dart/runtime/runtime_args.gni:101

 
### current_cpu  current_cpu 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

 
### current_os  current_os 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

 
### custom_signing_script  custom_signing_scriptIf non-empty, the given script will be invoked to produce a signed ZBI image. The given script must accept -z for the input zbi path, and -o forthe output signed zbi path. The path must be in GN-label syntax (i.e.starts with //). 如果为非空，则将调用给定脚本以生成签名的ZBI映像。给定的脚本必须接受-z作为输入zbi路径，并且-o作为输出带符号的zbi路径。该路径必须采用GN标签语法（即以//开头）。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/custom_signing.gni:12  来自//build/images/custom_signing.gni:12

 
### dart_aot_sharing_basis  dart_aot_sharing_basismodule_suggester is not AOT compiled in debug builds  在调试版本中未对module_suggester进行AOT编译

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From [//topaz/runtime/dart/dart_component.gni:51](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni#51)  来自[//topaz/runtime/dart/dart_component.gni:51](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni51）

 
### dart_component_kind  dart_component_kindAllow for deduping the VM between standalone, flutter_runner and dart_runner.  允许在独立的flutter_runner和dart_runner之间对虚拟机进行重复数据删除。

**Current value (from the default):** `"shared_library"`  **当前值（默认值）：**`“ shared_library”`

From //third_party/dart/runtime/runtime_args.gni:78  来自//third_party/dart/runtime/runtime_args.gni:78

 
### dart_core_snapshot_kind  dart_core_snapshot_kindControls the kind of core snapshot linked into the standalone VM. Using a core-jit snapshot breaks the ability to change various flags that affectcode generation. 控制链接到独立VM的核心快照的类型。使用core-jit快照破坏了更改影响代码生成的各种标志的能力。

**Current value (from the default):** `"core"`  **当前值（默认值）：**`“ core”`

From //third_party/dart/runtime/runtime_args.gni:56  来自//third_party/dart/runtime/runtime_args.gni:56

 
### dart_custom_version_for_pub  dart_custom_version_for_pubWhen this argument is a non-empty string, the version repoted by the Dart VM will be one that is compatible with pub's interpretation ofsemantic version strings. The version string will also include the valuesof the argument. In particular the version string will read: 如果此参数是非空字符串，则Dart VM所报告的版本将与pub对语义版本字符串的解释兼容。版本字符串还将包含参数的值。特别是版本字符串将显示为：

    "M.m.p-dev.x.x-$(dart_custom_version_for_pub)-$(short_git_hash)"  “ M.m.p-dev.x.x-$（dart_custom_version_for_pub）-$（short_git_hash）”

Where 'M', 'm', and 'p' are the major, minor and patch version numbers, and 'dev.x.x' is the dev version tag most recently preceeding the currentrevision. The short git hash can be omitted by settingdart_version_git_info=false 其中“ M”，“ m”和“ p”是主要版本，次要版本和补丁版本号，而“ dev.x.x”是当前版本之前最新的dev版本标记。可以通过设置dart_version_git_info = false来省略短git哈希

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/dart/runtime/runtime_args.gni:73  来自//third_party/dart/runtime/runtime_args.gni:73

 
### dart_debug  dart_debugInstead of using is_debug, we introduce a different flag for specifying a Debug build of Dart so that clients can still use a Release build of Dartwhile themselves doing a Debug build. 代替使用is_debug，我们引入了一个不同的标志来指定Dart的Debug版本，以便客户端在自己进行Debug版本时仍可以使用Dart的Release版本。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:9  来自//third_party/dart/runtime/runtime_args.gni:9

 
### dart_debug_optimization_level  dart_debug_optimization_levelThe optimization level to use for debug builds. Defaults to 0 for builds with code coverage enabled. 用于调试版本的优化级别。对于启用了代码覆盖率的构建，默认值为0。

**Current value (from the default):** `"2"`  **当前值（默认值）：**`“ 2”`

From //third_party/dart/runtime/runtime_args.gni:36  来自//third_party/dart/runtime/runtime_args.gni:36

 
### dart_default_app  dart_default_appControls whether dart_app() targets generate JIT or AOT Dart snapshots. This defaults to JIT, use `fx set <ARCH> --args'dart_default_app="dart_aot_app"' to switch to AOT. 控制dart_app（）目标是生成JIT还是AOT Dart快照。默认为JIT，使用`fx set <ARCH> --args'dart_default_app =“ dart_aot_app”'切换到AOT。

**Current value (from the default):** `"dart_jit_app"`  **当前值（默认值）：**`“ dart_jit_app”`

From [//topaz/runtime/dart/dart_component.gni:19](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni#19)  从[//topaz/runtime/dart/dart_component.gni:19]（https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni19）

 
### dart_force_product  dart_force_productForces all Dart and Flutter apps to build in a specific configuration that we use to build products. 强制所有Dart和Flutter应用构建为用于构建产品的特定配置。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From [//topaz/runtime/dart/config.gni:10](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/config.gni#10)  来自[//topaz/runtime/dart/config.gni:10](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/config.gni10）

 
### dart_lib_export_symbols  dart_lib_export_symbolsWhether libdart should export the symbols of the Dart API.  libdart是否应导出Dart API的符号。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/dart/runtime/runtime_args.gni:91  来自//third_party/dart/runtime/runtime_args.gni:91

 
### dart_platform_bytecode  dart_platform_bytecodeWhether the VM's platform dill file contains bytecode.  VM的平台莳萝文件是否包含字节码。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:84  来自//third_party/dart/runtime/runtime_args.gni:84

 
### dart_runtime_mode  dart_runtime_modeSet the runtime mode. This affects how the runtime is built and what features it has. Valid values are:'develop' (the default) - VM is built to run as a JIT with all developmentfeatures enabled.'profile' - The VM is built to run with AOT compiled code with only theCPU profiling features enabled.'release' - The VM is built to run with AOT compiled code with no developerfeatures enabled. 设置运行时模式。这会影响运行时的构建方式及其功能。有效值为：'develop'（默认值）-VM被构建为以JIT身份运行并启用了所有开发功能。'profile'-VM被构建为以AOT编译的代码运行且仅启用了CPU分析功能。'release'-该VM可以在未启用开发人员功能的情况下以AOT编译代码运行。

These settings are only used for Flutter, at the moment. A standalone build of the Dart VM should leave this set to "develop", and should set'is_debug', 'is_release', or 'is_product'. 目前，这些设置仅用于Flutter。 Dart VM的独立构建应将此设置保留为“ develop”，并应将其设置为“ is_debug”，“ is_release”或“ is_product”。

TODO(rmacnak): dart_runtime_mode no longer selects whether libdart is build for JIT or AOT, since libdart waw split into libdart_jit andlibdart_precompiled_runtime. We should remove this flag and just setdart_debug/dart_product. TODO（rmacnak）：dart_runtime_mode不再选择是为JIT还是AOT构建libdart，因为libdart的声音分为libdart_jit和libdart_precompiled_runtime。我们应该删除此标志，而只是setdart_debug / dart_product。

**Current value (from the default):** `"develop"`  **当前值（默认值）：**`“ develop”`

From //third_party/dart/runtime/runtime_args.gni:28  来自//third_party/dart/runtime/runtime_args.gni:28

 
### dart_snapshot_kind  dart_snapshot_kind 

**Current value (from the default):** `"kernel"`  **当前值（默认值）：**`“ kernel”`

From //third_party/dart/utils/application_snapshot.gni:14  来自//third_party/dart/utils/application_snapshot.gni:14

 
### dart_space_dart  dart_space_dartWhether experimental space dart mode is enabled for Dart applications.  是否为Dart应用程序启用了实验性太空飞镖模式。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From [//topaz/runtime/dart/dart_component.gni:41](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni#41)  来自[//topaz/runtime/dart/dart_component.gni:41](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni41）

 
### dart_target_arch  dart_target_archExplicitly set the target architecture to use a simulator. Available options are: arm, arm64, x64, ia32, and dbc. 明确设置目标体系结构以使用模拟器。可用选项包括：arm，arm64，x64，ia32和dbc。

**Current value (from the default):** `"arm64"`  **当前值（默认值）：**`“ arm64”`

From //third_party/dart/runtime/runtime_args.gni:32  来自//third_party/dart/runtime/runtime_args.gni:32

 
### dart_use_crashpad  dart_use_crashpadWhether to link Crashpad library for crash handling. Only supported on Windows for now. 是否链接Crashpad库以进行崩溃处理。目前仅在Windows上受支持。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:51  来自//third_party/dart/runtime/runtime_args.gni:51

 
### dart_use_fallback_root_certificates  dart_use_fallback_root_certificatesWhether to fall back to built-in root certificates when they cannot be verified at the operating system level. 当无法在操作系统级别验证内置根证书时是否回退。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:43  来自//third_party/dart/runtime/runtime_args.gni:43

 
### dart_use_tcmalloc  dart_use_tcmallocWhether to link the standalone VM against tcmalloc. The standalone build of the VM enables this only for Linux builds. 是否将独立VM链接到tcmalloc。 VM的独立构建仅适用于Linux构建。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:47  来自//third_party/dart/runtime/runtime_args.gni:47

 
### dart_version  dart_version 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/flutter/shell/version/version.gni:10  来自//third_party/flutter/shell/version/version.gni:10

 
### dart_version_git_info  dart_version_git_infoWhether the Dart binary version string should include the git hash and git commit time. Dart二进制版本字符串是否应包含git hash和git commit time。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/dart/runtime/runtime_args.gni:60  来自//third_party/dart/runtime/runtime_args.gni:60

 
### dart_vm_code_coverage  dart_vm_code_coverageWhether to enable code coverage for the standalone VM.  是否为独立VM启用代码覆盖。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:39  来自//third_party/dart/runtime/runtime_args.gni:39

 
### data_partition_manifest  data_partition_manifestPath to manifest file containing data to place into the initial /data partition. 清单文件的路径，该文件包含要放入初始/ data分区的数据。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:30  来自//build/images/BUILD.gn:30

 
### debian_guest_earlycon  debian_guest_earlycon 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //src/virtualization/packages/debian_guest/BUILD.gn:10  来自//src/virtualization/packages/debian_guest/BUILD.gn:10

 
### debian_guest_qcow  debian_guest_qcowPackage the rootfs as a QCOW image (as opposed to a flat file).  将rootfs打包为QCOW映像（而不是平面文件）。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //src/virtualization/packages/debian_guest/BUILD.gn:9  来自//src/virtualization/packages/debian_guest/BUILD.gn:9

 
### devmgr_config  devmgr_configList of arguments to add to /boot/config/devmgr. These come after synthesized arguments to configure blobfs and pkgfs. 要添加到/ boot / config / devmgr的参数列表。这些是在配置blobfs和pkgfs的综合参数之后得出的。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/images/BUILD.gn:474  来自//build/images/BUILD.gn:474

 
### embedder_for_target  embedder_for_targetBy default, the dynamic library target exposing the embedder API is only built for the host. The reasoning is that platforms that have targetdefinitions would not need an embedder API because an embedderimplementation is already provided for said target. This flag allows tbebuilder to obtain a shared library exposing the embedder API for alternativeembedder implementations. 默认情况下，仅针对主机构建公开嵌入式API的动态库目标。原因是具有targetdefinitions的平台将不需要embedder API，因为已经为所述目标提供了embedderimplementation。该标志允许tbebuilder获得一个共享库，该库公开用于替代嵌入式实现的嵌入式API。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/flutter/shell/platform/embedder/embedder.gni:12  来自//third_party/flutter/shell/platform/embedder/embedder.gni:12

 
### enable_dart_analysis  enable_dart_analysisEnable all dart analysis  启用所有飞镖分析

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/dart/dart_library.gni:16  来自//build/dart/dart_library.gni:16

 
### enable_frame_pointers  enable_frame_pointersControls whether the compiler emits full stack frames for function calls. This reduces performance but increases the ability to generate goodstack traces, especially when we have bugs around unwind table generation.It applies only for Fuchsia targets (see below where it is unset). 控制编译器是否为函数调用发出完整的堆栈帧。这会降低性能，但会增加生成良好堆栈跟踪的能力，尤其是当我们在展开表生成方面存在错误时，仅适用于倒挂金钟目标（请参见下文未设置的地方）。

TODO(ZX-2361): Theoretically unwind tables should be good enough so we can remove this option when the issues are addressed. TODO（ZX-2361）：从理论上讲，展开表应该足够好，以便在解决问题时可以删除此选项。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/config/BUILD.gn:20  来自//build/config/BUILD.gn:20

 
### enable_gfx_subsystem  enable_gfx_subsystem 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/bin/ui/scenic/BUILD.gn:11  来自//garnet/bin/ui/scenic/BUILD.gn:11

 
### enable_input_subsystem  enable_input_subsystem 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/bin/ui/scenic/BUILD.gn:12  来自//garnet/bin/ui/scenic/BUILD.gn:12

 
### enable_mdns_trace  enable_mdns_traceEnables the tracing feature of mdns, which can be turned on using "mdns-util verbose". 启用mdns的跟踪功能，可以使用“ mdns-util verbose”打开该功能。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //src/connectivity/network/mdns/service/BUILD.gn:15  来自//src/connectivity/network/mdns/service/BUILD.gn:15

 
### enable_netboot  enable_netbootWhether to build the netboot zbi by default.  是否默认构建netboot zbi。

You can still build //build/images:netboot explicitly even if enable_netboot is false.  即使enable_netboot为false，您仍然可以显式构建// build / images：netboot。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/images/BUILD.gn:35  来自//build/images/BUILD.gn:35

 
### engine_version  engine_version 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/flutter/shell/version/version.gni:6  来自//third_party/flutter/shell/version/version.gni:6

 
### escher_use_null_vulkan_config_on_host  escher_use_null_vulkan_config_on_hostUsing Vulkan on host (i.e. Linux) is an involved affair that involves downloading the Vulkan SDK, setting environment variables, and so forth...all things that are difficult to achieve in a CQ environment.  Therefore,by default we use a stub implementation of Vulkan which fails to create aVkInstance.  This allows everything to build, and also allows running Escherunit tests which don't require Vulkan. 在主机（即Linux）上使用Vulkan是一件很麻烦的事，包括下载Vulkan SDK，设置环境变量等...在CQ环境中难以实现的所有事情。因此，默认情况下，我们使用Vulkan的存根实现，该实现无法创建aVkInstance。这样就可以构建所有内容，还可以运行不需要Vulkan的Escherunit测试。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //src/ui/lib/escher/BUILD.gn:17  来自//src/ui/lib/escher/BUILD.gn:17

 
### exclude_kernel_service  exclude_kernel_serviceWhether the VM includes the kernel service in all modes (debug, release, product). VM是否在所有模式（调试，发行，产品）中都包括内核服务。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/dart/runtime/runtime_args.gni:88  来自//third_party/dart/runtime/runtime_args.gni:88

 
### expat_build_root  expat_build_root 

**Current value (from the default):** `"//third_party/expat"`  **当前值（默认值）：**`“ // third_party / expat”`

From //garnet/lib/magma/gnbuild/magma.gni:10  来自//garnet/lib/magma/gnbuild/magma.gni:10

 
### experimental_wlan_client_mlme  experimental_wlan_client_mlmeSelects the SoftMAC client implementation to use. Choices: false (default) - C++ Client MLME implementationtrue - Rust Client MLME implementationThis argument is temporary until Rust MLME is ready to be used. 选择要使用的SoftMAC客户端实现。选项：false（默认）-C ++客户端MLME实现true-Rust客户端MLME实现该参数是临时的，直到准备使用Rust MLME为止。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //src/connectivity/wlan/lib/mlme/cpp/BUILD.gn:10  来自//src/connectivity/wlan/lib/mlme/cpp/BUILD.gn:10

 
### extra_manifest_args  extra_manifest_argsExtra args to globally apply to the manifest generation script.  全局要使用的额外参数适用于清单生成脚本。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/images/manifest.gni:22  来自//build/images/manifest.gni:22

 
### extra_package_labels  extra_package_labels 

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //third_party/cobalt/BUILD.gn:10  来自//third_party/cobalt/BUILD.gn:10

 
### extra_variants  extra_variantsAdditional variant toolchain configs to support. This is just added to [`known_variants`](#known_variants). 要支持的其他变体工具链配置。这只是添加到[`known_variants`]（known_variants）中。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/config/BUILDCONFIG.gn:409  来自//build/config/BUILDCONFIG.gn:409

 
### fastboot_product  fastboot_产品 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:49  来自//build/images/BUILD.gn:49

 
### flutter_aot_sharing_basis  flutter_aot_sharing_basisWhen AOT compiling, an app will reference objects in the sharing basis's snapshot when available instead of writing the objects in its own snapshot.The snapshot of the sharing basis app will be included in every other app'spackage and deduplicated by blobfs. 在进行AOT编译时，一个应用将在可用时引用共享基础快照中的对象，而不是在其自己的快照中写入对象。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From [//topaz/runtime/dart/dart_component.gni:27](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni#27)  从[//topaz/runtime/dart/dart_component.gni:27]（https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni27）

 
### flutter_default_app  flutter_default_app 

**Current value (from the default):** `"flutter_jit_app"`  **当前值（默认值）：**`“ flutter_jit_app”`

From [//topaz/runtime/dart/dart_component.gni:12](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni#12)  来自[//topaz/runtime/dart/dart_component.gni:12](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni12）

 
### flutter_enable_skshaper  flutter_enable_skshaperWhether to use the Skia text shaper module  是否使用Skia文字成形器模块

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/flutter/common/config.gni:22  来自//third_party/flutter/common/config.gni:22

 
### flutter_profile  flutter_profile 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From [//topaz/runtime/dart/dart_component.gni:32](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni#32)  来自[//topaz/runtime/dart/dart_component.gni:32](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni32）

 
### flutter_runtime_mode  flutter_runtime_modeThe runtime mode ("debug", "profile", or "release")  运行时模式（“调试”，“配置文件”或“发行”）

**Current value (from the default):** `"debug"`  **当前值（默认值）：**`“ debug”`

From //third_party/flutter/common/config.gni:19  来自//third_party/flutter/common/config.gni:19

 
### flutter_space_dart  flutter_space_dartWhether experimental space dart mode is enabled for Flutter applications.  Flutter应用程序是否启用了实验性太空飞镖模式。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From [//topaz/runtime/dart/dart_component.gni:38](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni#38)  来自[//topaz/runtime/dart/dart_component.gni:38](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/dart/dart_component.gni38）

 
### flutter_use_fontconfig  flutter_use_fontconfig 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/flutter/third_party/txt/BUILD.gn:18  来自//third_party/flutter/third_party/txt/BUILD.gn:18

 
### framework_packages  framework_packages 

**Current value (from the default):** `["collection", "flutter", "meta", "typed_data", "vector_math"]`  **当前值（默认值）：**`[[“ collection”，“ flutter”，“ meta”，“ typed_data”，“ vector_math”]`

From [//topaz/runtime/flutter_runner/prebuilt_framework.gni:8](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/flutter_runner/prebuilt_framework.gni#8)  来自[//topaz/runtime/flutter_runner/prebuilt_framework.gni:8](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/flutter_runner/prebuilt_framework.gni8）

 
### fuchsia_sdk_root  fuchsia_sdk_rootConsumers of the Fuchsia SDK instantiate templates for various SDK parts at a specific spot within their buildroots. The target name for the specificpart is then derived from the part name as specified in the meta.jsonmanifest. Different buildroot instantiate the SDK parts at differentlocations and then set this variable. GN rules can then prefix this variablename in SDK builds to the name of the SDK part. This flag is meaningless innon-SDK buildroots. Fuchsia SDK的使用者在其buildroot中的特定位置实例化各种SDK部件的模板。然后，从meta.jsonmanifest中指定的零件名称派生特定零件的目标名称。不同的buildroot在不同的位置实例化SDK部件，然后设置此变量。然后，GN规则可以在SDK构建中将此变量名添加到SDK部件的名称之前。该标志在非SDK构建根目录中是没有意义的。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/fuchsia/sdk.gni:17  来自//build/fuchsia/sdk.gni:17

 
### fuchsia_use_vulkan  紫红色Consolidated build toggle for use of Vulkan across Fuchsia  整合的构建切换，可在整个紫红色中使用Vulkan

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/vulkan/config.gni:7  来自//build/vulkan/config.gni:7

 
### fuchsia_vulkan_sdk  紫红色_vulkan_sdkPath to Fuchsia Vulkan SDK  紫红色Vulkan SDK的路径

**Current value (from the default):** `"//third_party/vulkan_loader_and_validation_layers"`  **当前值（默认值）：**`“ // third_party / vulkan_loader_and_validation_layers”`

From //build/vulkan/config.gni:10  来自//build/vulkan/config.gni:10

 
### full_dart_sdk  full_dart_sdk 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/flutter/BUILD.gn:14  来自//third_party/flutter/BUILD.gn:14

 
### fvm_image_size  fvm_image_sizeThe size in bytes of the FVM partition image to create. Normally this is computed to be just large enough to fit the blob and data images. Thedefault value is "", which means to size based on inputs. Specifying a sizethat is too small will result in build failure. 要创建的FVM分区映像的大小（以字节为单位）。通常，计算得出的大小正好足以适合斑点和数据图像。默认值为“”，表示根据输入进行调整。指定的尺寸太小会导致构建失败。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/fvm.gni:12  来自//build/images/fvm.gni:12

 
### fvm_slice_size  fvm_slice_sizeThe size of the FVM partition images "slice size". The FVM slice size is a minimum size of a particular chunk of a partition that is stored withinFVM. A very small slice size may lead to decreased throughput. A very largeslice size may lead to wasted space. The selected default size of 8mb isselected for conservation of space, rather than performance. FVM分区映像的大小为“切片大小”。 FVM切片大小是存储在FVM中的分区的特定块的最小大小。很小的切片大小可能导致吞吐量降低。很大的切片尺寸可能会导致空间浪费。选择所选的默认大小8mb是为了节省空间而不是性能。

**Current value (from the default):** `"8388608"`  **当前值（默认值）：**`“ 8388608”`

From //build/images/fvm.gni:19  来自//build/images/fvm.gni:19

 
### glm_build_root  glm_build_root 

**Current value (from the default):** `"//third_party/glm"`  **当前值（默认值）：**`“ // third_party / glm”`

From //garnet/lib/magma/gnbuild/magma.gni:12  来自//garnet/lib/magma/gnbuild/magma.gni:12

 
### go_vet_enabled  go_vet_enabled  go_vet_enabled [bool] if false, go vet invocations are disabled for all builds. go_vet_enabled [bool]如果为false，则对所有构建都禁用go vet调用。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/go/go_build.gni:20  来自//build/go/go_build.gni:20

 
### gocache_dir  gocache_dir  gocache_dir Directory GOCACHE environment variable will be set to. This directorywill have build and test results cached, and is safe to be written toconcurrently. If overridden, this directory must be a full path. gocache_dir目录GOCACHE环境变量将被设置为。该目录将缓存构建和测试结果，并且可以安全地并行写入。如果被覆盖，则该目录必须是完整路径。

**Current value (from the default):** `"/b/s/w/ir/k/root_build_dir/host_x64/.gocache"`  **当前值（默认值）：**`“ /b/s/w/ir/k/root_build_dir/host_x64/.gocache”`

From //build/go/go_build.gni:16  来自//build/go/go_build.gni:16

 
### goma_dir  goma_dirDirectory containing the Goma source code.  This can be a GN source-absolute path ("//...") or a system absolute path. 包含戈马源代码的目录。这可以是GN源绝对路径（“ // ...”）或系统绝对路径。

**Current value (from the default):** `"/home/swarming/goma"`  **当前值（默认值）：**`“ / home / swarming / goma”`

From //build/toolchain/goma.gni:13  来自//build/toolchain/goma.gni:13

 
### graphics_compute_generate_debug_shaders  graphics_compute_generate_debug_shadersSet to true in your args.gn file to generate pre-processed and auto-formatted shaders under the "debug" sub-directory of hotsort and spineltarget generation output directories. 在args.gn文件中设置为true，以在hotsort和spineltarget生成输出目录的“ debug”子目录下生成经过预处理和自动格式化的着色器。

These are never used, but can be reviewed manually to verify the impact of configuration parameters, or when modifying hotsort. 这些从不使用，但是可以手动检查以验证配置参数的影响，或者在修改热排序时使用。

Example results:  结果示例：

  out/default/ gen/src/graphics/lib/compute/hotsort/targets/hs_amd_gcn3_u64/comp/hs_transpose.comp   -> normal shader.debug/hs_transpose.comp   -> same, but much easier to read! out / default / gen / src / graphics / lib / compute / hotsort / targets / hs_amd_gcn3_u64 / comp / hs_transpose.comp->普通shader.debug / hs_transpose.comp->相同，但更容易阅读！

 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //src/graphics/lib/compute/gn/glsl_shader_rules.gni:27  来自//src/graphics/lib/compute/gn/glsl_shader_rules.gni:27

 
### host_byteorder  host_byteorder 

**Current value (from the default):** `"undefined"`  **当前值（默认值）：**`“ undefined”`

From //build/config/host_byteorder.gni:7  来自//build/config/host_byteorder.gni:7

 
### host_cpu  host_cpu 

**Current value (from the default):** `"x64"`  **当前值（默认值）：**`“ x64”`

 
### host_os  host_os 

**Current value (from the default):** `"linux"`  **当前值（默认值）：**`“ linux”`

 
### host_tools_dir  host_tools_dirThis is the directory where host tools intended for manual use by developers get installed.  It's something a developer might putinto their shell's $PATH.  Host tools that are just needed as partof the build do not get copied here.  This directory is only forthings that are generally useful for testing or debugging orwhatnot outside of the GN build itself.  These are only installedby an explicit install_host_tools() rule (see //build/host.gni). 这是用于开发人员手动使用的宿主工具的安装目录。这可能是开发人员可能将其$ shell放入外壳程序中的原因。在构建过程中仅需要使用的宿主工具不会在此处复制。该目录仅是通常对测试或调试有用的语言，而对于GN构建本身之外的其他语言则不可用。这些仅通过显式的install_host_tools（）规则进行安装（请参见//build/host.gni）。

**Current value (from the default):** `"//root_build_dir/tools"`  **当前值（默认值）：**`“ // root_build_dir / tools”`

From //build/host.gni:13  来自//build/host.gni:13

 
### icu_use_data_file  icu_use_data_fileTells icu to load an external data file rather than rely on the icudata being linked directly into the binary. 告诉icu加载外部数据文件，而不是依赖于直接链接到二进制文件的icudata。

This flag is a bit confusing. As of this writing, icu.gyp set the value to 0 but common.gypi sets the value to 1 for most platforms (and the 1 takesprecedence). 这个标志有点令人困惑。在撰写本文时，对于大多数平台，icu.gyp将该值设置为0，但common.gypi将该值设置为1（并且1优先）。

TODO(GYP) We'll probably need to enhance this logic to set the value to true or false in similar circumstances. TODO（GYP）我们可能需要增强此逻辑，以便在类似情况下将值设置为true或false。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From [//third_party/icu/config.gni:15](https://fuchsia.googlesource.com/third_party/icu/+/1aa5008165095c7651f500f77e04336cd2748660/config.gni#15)  来自[//third_party/icu/config.gni:15](https://fuchsia.googlesource.com/third_party/icu/+/1aa5008165095c7651f500f77e04336cd2748660/config.gni15）

 
### is_debug  is_debugDebug build.  调试版本。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/config/BUILDCONFIG.gn:15  来自//build/config/BUILDCONFIG.gn:15

 
### kernel_cmdline_args  kernel_cmdline_argsList of kernel command line arguments to bake into the boot image. See also [kernel_cmdline](/docs/reference/kernel/kernel_cmdline.md) and[`devmgr_config`](#devmgr_config). 烘烤到引导映像中的内核命令行参数列表。另请参阅[kernel_cmdline]（/ docs / reference / kernel / kernel_cmdline.md）和[`devmgr_config`]（devmgr_config）。

**Current value for `target_cpu = "arm64"`:** `["dummy=arg"]`  ** target_cpu =“ arm64”`的当前值：**`[“ dummy = arg”]`

From //products/bringup.gni:12  来自//products/bringup.gni:12

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //build/images/BUILD.gn:479  来自//build/images/BUILD.gn:479

**Current value for `target_cpu = "x64"`:** `["dummy=arg"]`  ** target_cpu =“ x64”`的当前值：**`[“ dummy = arg”]`

From //products/bringup.gni:12  来自//products/bringup.gni:12

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //build/images/BUILD.gn:479  来自//build/images/BUILD.gn:479

 
### kernel_cmdline_files  kernel_cmdline_filesFiles containing additional kernel command line arguments to bake into the boot image.  The contents of these files (in order) come after anyarguments directly in [`kernel_cmdline_args`](#kernel_cmdline_args).These can be GN `//` source pathnames or absolute system pathnames. 包含其他内核命令行参数的文件可放入引导映像中。这些文件的内容（按顺序）直接在[`kernel_cmdline_args]]（kernel_cmdline_args）中的任何参数之后。它们可以是GN`//`源路径名或绝对系统路径名。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/images/BUILD.gn:485  来自//build/images/BUILD.gn:485

 
### known_variants  已知变量List of variants that will form the basis for variant toolchains. To make use of a variant, set [`select_variant`](#select_variant). 构成变体工具链基础的变体列表。要使用变体，请设置[`select_variant`]（select_variant）。

Normally this is not set as a build argument, but it serves to document the available set of variants.See also [`universal_variants`](#universal_variants).Only set this to remove all the default variants here.To add more, set [`extra_variants`](#extra_variants) instead. 通常不将其设置为构建参数，而是用于记录可用的变体集。另请参见[`universal_variants`]（universal_variants）。仅在此处设置此项才能删除所有默认变体。要添加更多默认变体，请设置[` extra_variants`]（extra_variants）代替。

Each element of the list is one variant, which is a scope defining:  列表的每个元素都是一个变体，它是一个范围定义：

  `configs` (optional) [list of labels] Each label names a config that will beautomatically used by every target built in this variant.For each config `${label}`, there must also be a target`${label}_deps`, which each target built in this variant willautomatically depend on.  The `variant()` template is therecommended way to define a config and its `_deps` target atthe same time. configs（可选）[标签列表]每个标签都将指定一个配置，该配置将由此变体内置的每个目标自动使用。对于每个配置`$ {label}`，还必须有一个目标`$ {label} _deps `，此变体中内置的每个目标都将自动依赖。建议使用`variant（）`模板同时定义配置及其`_deps`目标。

  `remove_common_configs` (optional) `remove_shared_configs` (optional)[list of labels] This list will be removed (with `-=`) fromthe `default_common_binary_configs` list (or the`default_shared_library_configs` list, respectively) afterall other defaults (and this variant's configs) have beenadded. `remove_common_configs`（可选）`remove_shared_configs`（可选）[标签列表]此列表将在所有其他默认值（以及该默认值）之后分别从“ default_common_binary_configs”列表（或“ default_shared_library_configs”列表）中删除（带有-=`）。变体的配置）已添加。

  `deps` (optional) [list of labels] Added to the deps of every target linked inthis variant (as well as the automatic `${label}_deps` foreach label in configs). `deps`（可选）[标签列表]已添加到此变体中链接的每个目标的dep中（以及配置中的自动$ {label} _deps` foreach标签）。

  `name` (required if configs is omitted) [string] Name of the variant as used in[`select_variant`](#select_variant) elements' `variant` fields.It's a good idea to make it something concise and meaningful whenseen as e.g. part of a directory name under `$root_build_dir`.If name is omitted, configs must be nonempty and the simple names(not the full label, just the part after all `/`s and `:`s) of theseconfigs will be used in toolchain names (each prefixed by a "-"),so the list of config names forming each variant must be uniqueamong the lists in `known_variants + extra_variants`. 名称（如果省略配置则为必填项）[字符串]在[select_variant]]（select_variant）元素的variant`字段中使用的变体名称。最好使它简洁明了，例如$ root_build_dir目录下的目录名称的一部分。如果省略名称，则配置必须是非空的，并且将使用这些配置的简单名称（不是完整标签，仅是所有`/`s和`：`s之后的部分）在工具链名称中（每个名称以“-”作为前缀），因此构成每个变量的配置名称列表在“ known_variants + extra_variants”中的列表中必须唯一。

  `toolchain_args` (optional) [scope] Each variable defined in this scope overrides abuild argument in the toolchain context of this variant. `toolchain_args`（可选）[作用域]在此范围内定义的每个变量都将覆盖此变体的工具链上下文中的build参数。

  `host_only` (optional) `target_only` (optional)[scope] This scope can contain any of the fields above.These values are used only for host or target, respectively.Any fields included here should not also be in the outer scope. “ host_only”（可选）“ target_only”（可选）[scope]此范围可以包含上面的任何字段。这些值分别仅用于主机或目标。此处包含的任何字段也不应在外部范围内。

 

```
[{
  configs = ["//build/config/lto"]
}, {
  configs = ["//build/config/lto:thinlto"]
}, {
  configs = ["//build/config/profile"]
}, {
  configs = ["//build/config/scudo"]
}, {
  configs = ["//build/config/sanitizers:ubsan"]
}, {
  configs = ["//build/config/sanitizers:ubsan", "//build/config/sanitizers:sancov"]
}, {
  configs = ["//build/config/sanitizers:asan"]
  host_only = {
  remove_shared_configs = ["//build/config:symbol_no_undefined"]
}
  toolchain_args = {
  use_scudo = false
}
}, {
  configs = ["//build/config/sanitizers:asan", "//build/config/sanitizers:sancov"]
  host_only = {
  remove_shared_configs = ["//build/config:symbol_no_undefined"]
}
  toolchain_args = {
  use_scudo = false
}
}, {
  configs = ["//build/config/sanitizers:asan"]
  host_only = {
  remove_shared_configs = ["//build/config:symbol_no_undefined"]
}
  name = "asan_no_detect_leaks"
  toolchain_args = {
  asan_default_options = "detect_leaks=0"
  use_scudo = false
}
}, {
  configs = ["//build/config/sanitizers:asan", "//build/config/sanitizers:fuzzer"]
  host_only = {
  remove_shared_configs = ["//build/config:symbol_no_undefined"]
}
  remove_shared_configs = ["//build/config:symbol_no_undefined"]
  toolchain_args = {
  asan_default_options = "alloc_dealloc_mismatch=0"
  use_scudo = false
}
}, {
  configs = ["//build/config/sanitizers:ubsan", "//build/config/sanitizers:fuzzer"]
  remove_shared_configs = ["//build/config:symbol_no_undefined"]
}]
```
**Current value (from the default):**  **当前值（默认值）：**

From //build/config/BUILDCONFIG.gn:344  来自//build/config/BUILDCONFIG.gn:344

 
### linux_guest_extras_path  linux_guest_extras_path 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //src/virtualization/packages/linux_guest/BUILD.gn:12  来自//src/virtualization/packages/linux_guest/BUILD.gn:12

 
### linux_runner_extras  linux_runner_extrasIf `true`, the extras.img will be built and mounted inside the container at /mnt/chromeos. 如果为true，则extras.img将在/ mnt / chromeos的容器内构建并安装。

This is useful for including some GN-built binaries into the guest image without modifying the termina images. 这对于在不修改终端图像的情况下将一些GN构建的二进制文件包含到来宾图像中很有用。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:26  来自//src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:26

 
### linux_runner_gateway  linux_runner_gateway 

**Current value (from the default):** `"10.0.0.1"`  **当前值（默认值）：**`“ 10.0.0.1”`

From //src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:18  来自//src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:18

 
### linux_runner_ip  linux_runner_ipDefault values for the guest network configuration.  来宾网络配置的默认值。

These are currently hard-coded to match what is setup in the virtio-net device. 目前，这些文件已经过硬编码，以匹配virtio-net设备中的设置。

See //src/virtualization/bin/vmm/device/virtio_net.cc for more details.  有关更多详细信息，请参见//src/virtualization/bin/vmm/device/virtio_net.cc。

**Current value (from the default):** `"10.0.0.2"`  **当前值（默认值）：**`“ 10.0.0.2”`

From //src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:17  来自//src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:17

 
### linux_runner_netmask  linux_runner_netmask 

**Current value (from the default):** `"255.255.255.0"`  **当前值（默认值）：**`“ 255.255.255.0”`

From //src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:19  来自//src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:19

 
### linux_runner_volatile_block  linux_runner_volatile_blockIf `true`, all block devices that would normally load as READ_WRITE will be loaded as VOLATILE_WRITE. This is useful when working on changes tothe linux kernel as crashes and panics can sometimes corrupt the images. 如果为true，则所有通常以READ_WRITE加载的块设备将以VOLATILE_WRITE加载。这在处理Linux内核更改时非常有用，因为崩溃和崩溃有时会损坏映像。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:31  来自//src/virtualization/packages/biscotti_guest/linux_runner/BUILD.gn:31

 
### local_bench  local_benchUsed to enable local benchmarking/fine-tuning when running benchmarks in `fx shell`. Pass `--args=local_bench='true'` to `fx set` in order toenable it. 在`fx shell`中运行基准测试时，用于启用本地基准测试/微调。将`--args = local_bench ='true'`传递给`fx set`以启用它。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //src/developer/fuchsia-criterion/BUILD.gn:14  来自//src/developer/fuchsia-criterion/BUILD.gn:14

 
### log_startup_sleep  log_startup_sleep 

**Current value (from the default):** `"30000"`  **当前值（默认值）：**`“ 30000”`

From //garnet/bin/log_listener/BUILD.gn:15  来自//garnet/bin/log_listener/BUILD.gn:15

 
### magma_build_root  magma_build_root 

**Current value (from the default):** `"//garnet/lib/magma"`  **当前值（默认值）：**`“ // garnet / lib / magma”`

From //garnet/lib/magma/gnbuild/magma.gni:9  来自//garnet/lib/magma/gnbuild/magma.gni:9

 
### magma_enable_developer_build  magma_enable_developer_buildEnable this to have the msd include a suite of tests and invoke them automatically when the driver starts. 启用此选项可使msd包含一组测试，并在驱动程序启动时自动调用它们。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //garnet/lib/magma/gnbuild/magma.gni:22  来自//garnet/lib/magma/gnbuild/magma.gni:22

 
### magma_enable_tracing  magma_enable_tracingEnable this to include fuchsia tracing capability  使它包括紫红色追踪功能

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/lib/magma/gnbuild/magma.gni:18  来自//garnet/lib/magma/gnbuild/magma.gni:18

 
### magma_python_path  magma_python_path 

**Current value (from the default):** `"/b/s/w/ir/k/third_party/mako"`  **当前值（默认值）：**`“ / b / s / w / ir / k / third_party / mako”`

From //garnet/lib/magma/gnbuild/magma.gni:15  来自//garnet/lib/magma/gnbuild/magma.gni:15

 
### max_blob_contents_size  max_blob_contents_sizeMaximum allowable contents for the /blob in a release mode build. Zero means no limit.contents_size refers to contents stored within the filesystem (regardlessof how they are stored). 在发行模式下，/ blob的最大允许内容。零表示没有限制。contents_size指的是存储在文件系统中的内容（无论如何存储）。

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //build/images/filesystem_limits.gni:10  来自//build/images/filesystem_limits.gni:10

 
### max_blob_image_size  max_blob_image_sizeMaximum allowable image_size for /blob in a release mode build. Zero means no limit.image_size refers to the total image size, including both contents andmetadata. 在发行模式下，/ blob的最大允许image_size。零表示无限制。image_size表示总图像大小，包括内容和元数据。

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //build/images/filesystem_limits.gni:16  来自//build/images/filesystem_limits.gni:16

 
### max_data_contents_size  max_data_contents_sizeMaximum allowable contents_size for /data in a release mode build. Zero means no limit.contents_size refers to contents stored within the filesystem (regardlessof how they are stored). 发行模式下/ data的最大允许contents_size。零表示没有限制。contents_size指的是存储在文件系统中的内容（无论如何存储）。

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //build/images/filesystem_limits.gni:22  来自//build/images/filesystem_limits.gni:22

 
### max_data_image_size  max_data_image_sizeMaximum allowable image_size for /data in a release mode build. Zero means no limit.image_size refers to the total image size, including both contents andmetadata. 发行模式下/ data的最大允许image_size。零表示无限制。image_size表示总图像大小，包括内容和元数据。

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //build/images/filesystem_limits.gni:28  来自//build/images/filesystem_limits.gni:28

 
### max_fuchsia_zbi_size  max_fuchsia_zbi_sizeMaximum allowable size for fuchsia.zbi  紫红色的最大允许大小

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //build/images/filesystem_limits.gni:31  来自//build/images/filesystem_limits.gni:31

 
### max_fvm_size  max_fvm_sizeMaximum allowable size for the FVM in a release mode build Zero means no limit 在发布模式下，FVM的最大允许大小为零表示无限制

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //build/images/max_fvm_size.gni:8  来自//build/images/max_fvm_size.gni:8

 
### max_log_disk_usage  max_log_disk_usageControls how many bytes of space on disk are used to persist device logs. Should be a string value that only contains digits. 控制磁盘上多少字节的空间用于保留设备日志。应该是仅包含数字的字符串值。

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //garnet/bin/log_listener/BUILD.gn:14  来自//garnet/bin/log_listener/BUILD.gn:14

 
### max_zedboot_zbi_size  max_zedboot_zbi_sizeMaximum allowable size for zedboot.zbi  zedboot.zbi的最大允许大小

**Current value (from the default):** `"0"`  **当前值（默认值）：**`“ 0”`

From //build/images/filesystem_limits.gni:34  来自//build/images/filesystem_limits.gni:34

 
### meta_package_labels  meta_package_labelsA list of labels for meta packages to be included in the monolith.  整体中将包含的元软件包的标签列表。

**Current value for `target_cpu = "arm64"`:** `["//build/images:config-data", "//build/images:shell-commands", "//src/sys/component_index:component_index"]`  ** target_cpu =“ arm64”`的当前值：**`[“ // build / images：config-data”，“ // build / images：shell-commands”，“ // src / sys / component_index： component_index“]`

From //products/core.gni:12  来自//products/core.gni:12

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //build/images/BUILD.gn:38  来自//build/images/BUILD.gn:38

**Current value for `target_cpu = "x64"`:** `["//build/images:config-data", "//build/images:shell-commands", "//src/sys/component_index:component_index"]`  ** target_cpu =“ x64”`的当前值：**`[“ // build / images：config-data”，“ // build / images：shell-commands”，“ // src / sys / component_index： component_index“]`

From //products/core.gni:12  来自//products/core.gni:12

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //build/images/BUILD.gn:38  来自//build/images/BUILD.gn:38

 
### minfs_maximum_bytes  minfs_maximum_bytes 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/fvm.gni:48  来自//build/images/fvm.gni:48

 
### minfs_minimum_data_bytes  minfs_minimum_data_bytes 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/fvm.gni:37  来自//build/images/fvm.gni:37

 
### minfs_minimum_inodes  minfs_minimum_inodes 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/fvm.gni:29  来自//build/images/fvm.gni:29

 
### msd_arm_enable_all_cores  msd_arm_enable_all_coresEnable all 8 cores, which is faster but emits more heat.  启用所有8个核心，速度更快，但会散发更多热量。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/drivers/gpu/msd-arm-mali/src/BUILD.gn:9  来自//garnet/drivers/gpu/msd-arm-mali/src/BUILD.gn:9

 
### msd_arm_enable_cache_coherency  msd_arm_enable_cache_coherencyWith this flag set the system tries to use cache coherent memory if the GPU supports it. 设置此标志后，如果GPU支持，系统将尝试使用高速缓存一致性内存。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/drivers/gpu/msd-arm-mali/src/BUILD.gn:13  来自//garnet/drivers/gpu/msd-arm-mali/src/BUILD.gn:13

 
### msd_arm_enable_protected_debug_swap_mode  msd_arm_enable_protected_debug_swap_modeIn protected mode, faults don't return as much information so they're much harder to debug. To work around that, add a mode where protected atoms are executed in non-protected mode andvice-versa. 在保护模式下，错误不会返回太多信息，因此很难进行调试。要解决此问题，请添加一种模式，在该模式下，受保护原子以非保护模式执行，反之亦然。

NOTE: The memory security ranges should also be set (in TrustZone) to the opposite of normal, so that non-protected mode accesses can only access protected memory and vice versa.  Also,growable memory faults won't work in this mode, so larger portions of growable memory shouldprecommitted (which is not done by default). 注意：内存安全范围也应该设置为（在TrustZone中）与正常值相反，以便非保护模式访问只能访问受保护的内存，反之亦然。此外，可增长内存故障在此模式下将不起作用，因此应预先承诺可增长内存的较大部分（默认情况下不执行此操作）。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //garnet/drivers/gpu/msd-arm-mali/src/BUILD.gn:23  来自//garnet/drivers/gpu/msd-arm-mali/src/BUILD.gn:23

 
### msd_intel_gen_build_root  msd_intel_gen_build_root 

**Current value (from the default):** `"//garnet/drivers/gpu/msd-intel-gen"`  **当前值（默认值）：**`“ // garnet / drivers / gpu / msd-intel-gen”`

From //garnet/lib/magma/gnbuild/magma.gni:11  来自//garnet/lib/magma/gnbuild/magma.gni:11

 
### persist_logs  persist_logs 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/persist_logs.gni:13  来自//build/persist_logs.gni:13

 
### prebuilt_dart_sdk  prebuilt_dart_sdkDirectory containing prebuilt Dart SDK. This must have in its `bin/` subdirectory `gen_snapshot.OS-CPU` binaries.Set to empty for a local build. 包含预建Dart SDK的目录。它必须在其bin /子目录gen_snapshot.OS-CPU二进制文件中。对于本地版本，设置为空。

**Current value (from the default):** `"//prebuilt/third_party/dart/linux-x64"`  **当前值（默认值）：**`“ // prebuilt / third_party / dart / linux-x64”`

From //build/dart/dart.gni:9  来自//build/dart/dart.gni:9

 
### prebuilt_framework_name  prebuilt_framework_name 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From [//topaz/runtime/flutter_runner/prebuilt_framework.gni:7](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/flutter_runner/prebuilt_framework.gni#7)  来自[//topaz/runtime/flutter_runner/prebuilt_framework.gni:7]（https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/flutter_runner/prebuilt_framework.gni7）

 
### prebuilt_framework_path  prebuilt_framework_path 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From [//topaz/runtime/flutter_runner/prebuilt_framework.gni:6](https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/flutter_runner/prebuilt_framework.gni#6)  来自[//topaz/runtime/flutter_runner/prebuilt_framework.gni:6]（https://fuchsia.googlesource.com/topaz/+/ee9a02a4e006aceda4482bc9ceb016d2d6e0f909/runtime/flutter_runner/prebuilt_framework.gni6）

 
### prebuilt_libvulkan_arm_path  prebuilt_libvulkan_arm_path 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //garnet/lib/magma/gnbuild/magma.gni:24  来自//garnet/lib/magma/gnbuild/magma.gni:24

 
### prebuilt_libvulkan_goldfish_path  prebuilt_libvulkan_goldfish_path 

**Current value (from the default):** `"//prebuilt/third_party/libvulkan_goldfish/arm64"`  **当前值（默认值）：**`“ // prebuilt / third_party / libvulkan_goldfish / arm64”`

From //garnet/lib/goldfish-vulkan/gnbuild/BUILD.gn:10  来自//garnet/lib/goldfish-vulkan/gnbuild/BUILD.gn:10

 
### rust_lto  rust_ltoSets the default LTO type for rustc bulids.  设置仿古构建的默认LTO类型。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/rust/config.gni:20  来自//build/rust/config.gni:20

 
### rust_override_lto  rust_override_ltoOverrides the LTO setting for all Rust builds, regardless of debug/release flags or the `with_lto` arg to the rustc_ templates.Valid values are "none", "thin", and "fat". 覆盖所有Rust构建的LTO设置，而不管调试/释放标志或rustc_模板的`with_lto` arg如何。有效值为“ none”，“ thin”和“ fat”。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/rust/config.gni:37  来自//build/rust/config.gni:37

 
### rust_override_opt  rust_override_optOverrides the optimization level for all Rust builds, regardless of debug/release flags or the `force_opt` arg to the rustc_ templates.Valid values are 0-3, o, and z. 无论调试/发布标志或rustc_模板的``force_opt''arg如何，都将覆盖所有Rust构建的优化级别。有效值为0-3，o和z。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/rust/config.gni:32  来自//build/rust/config.gni:32

 
### rust_toolchain_triple_suffix  rust_toolchain_triple_suffixSets the fuchsia toolchain target triple suffix (after arch)  设置倒挂金钟工具链目标的三重后缀（拱后）

**Current value (from the default):** `"fuchsia"`  **当前值（默认值）：**`“紫红色”

From //build/rust/config.gni:23  来自//build/rust/config.gni:23

 
### rust_cap_lints  rust_cap_lintsSets the maximum lint level. "deny" will make all warnings into errors, "warn" preserves them as warnings, and "allow" willignore warnings. 设置最大皮棉级别。 “拒绝”将使所有警告变为错误，“警告”将其保留为警告，而“允许”将忽略警告。

**Current value (from the default):** `"deny"`  **当前值（默认值）：**`“ deny”`

From //build/rust/config.gni:27  来自//build/rust/config.gni:27

 
### rustc_prefix  rustc_prefixSets a custom base directory for `rustc` and `cargo`. This can be used to test custom Rust toolchains. 为“ rustc”和“ cargo”设置自定义基本目录。这可以用来测试自定义的Rust工具链。

**Current value (from the default):** `"//prebuilt/third_party/rust/linux-x64/bin"`  **当前值（默认值）：**`“ // prebuilt / third_party / rust / linux-x64 / bin”`

From //build/rust/config.gni:17  来自//build/rust/config.gni:17

 
### scenic_display_frame_number  Scenic_display_frame_numberDraws the current frame number in the top-left corner.  在左上角绘制当前帧号。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //garnet/lib/ui/gfx/BUILD.gn:11  来自//garnet/lib/ui/gfx/BUILD.gn:11

 
### scenic_enable_vulkan_validation  Scenic_enable_vulkan_validationInclude the vulkan validation layers in scenic.  在风景区中包括vulkan验证层。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/bin/ui/BUILD.gn:38  来自//garnet/bin/ui/BUILD.gn:38

 
### scenic_ignore_vsync  Scenic_ignore_vsync 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //garnet/lib/ui/gfx/BUILD.gn:8  来自//garnet/lib/ui/gfx/BUILD.gn:8

 
### scudo_default_options  scudo_default_optionsDefault [Scudo](https://llvm.org/docs/ScudoHardenedAllocator.html) options (before the `SCUDO_OPTIONS` environment variable is read atruntime).  *NOTE:* This affects only components using the `scudo`variant (see GN build argument `select_variant`), and does not affectanything when the `use_scudo` build flag is set instead. 默认[Scudo]（https://llvm.org/docs/ScudoHardenedAllocator.html）选项（在运行时读取“ SCUDO_OPTIONS”环境变量之前）。 *注意：*这仅影响使用`scudo`变量的组件（请参见GN生成参数`select_variant`），而在设置`use_scudo`生成标志时不影响任何内容。

**Current value (from the default):** `["abort_on_error=1", "QuarantineSizeKb=0", "ThreadLocalQuarantineSizeKb=0", "DeallocationTypeMismatch=false", "DeleteSizeMismatch=false", "allocator_may_return_null=true"]`  **当前值（默认值）：**`[“” abort_on_error = 1“，” QuarantineSizeKb = 0“，” ThreadLocalQuarantineSizeKb = 0“，” DeallocationTypeMismatch = false“，” DeleteSizeMismatch = false“，” allocator_may_return_null = true“] `

From //build/config/scudo/scudo.gni:17  来自//build/config/scudo/scudo.gni:17

 
### sdk_dirs  sdk_dirsThe directories to search for parts of the SDK.  用于搜索SDK部分的目录。

By default, we search the public directories for the various layers. In the future, we'll search a pre-built SDK as well. 默认情况下，我们在公共目录中搜索各个层。将来，我们还将搜索预构建的SDK。

**Current value (from the default):** `["//garnet/public", "//peridot/public", "//topaz/public"]`  **当前值（默认值）：**`[“ //石榴石/公共”，“ //橄榄石/公共”，“ //黄玉/公共”]`

From //build/config/fuchsia/sdk.gni:10  来自//build/config/fuchsia/sdk.gni:10

 
### sdk_id  sdk_idIdentifier for the Core SDK.  核心SDK的标识符。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //sdk/config.gni:7  来自//sdk/config.gni:7

 
### select_variant  select_variantList of "selectors" to request variant builds of certain targets. Each selector specifies matching criteria and a chosen variant.The first selector in the list to match a given target determineswhich variant is used for that target. “选择器”列表，用于请求某些目标的变体版本。每个选择器都指定匹配条件和一个选择的变体。列表中与给定目标匹配的第一个选择器确定哪个变体用于该目标。

Each selector is either a string or a scope.  A shortcut selector is a string; it gets expanded to a full selector.  A full selector is ascope, described below. 每个选择器都是字符串或范围。快捷方式选择器是一个字符串。它会扩展为完整的选择器。完整的选择器是一个范围，如下所述。

A string selector can match a name in [`select_variant_shortcuts`](#select_variant_shortcuts).  If it's not aspecific shortcut listed there, then it can be the name of any variantdescribed in [`known_variants`](#known_variants) and[`universal_variants`](#universal_variants) (and combinations thereof).A `selector` that's a simple variant name selects for every binarybuilt in the target toolchain: `{ host=false variant=selector }`. 字符串选择器可以匹配[`select_variant_shortcuts`]（select_variant_shortcuts）中的名称。如果这里没有列出特定的快捷方式，那么它可以是[`known_variants`]（known_variants）和[`universal_variants`]（universal_variants）（及其组合）中描述的任何变量的名称。为目标工具链中构建的每个二进制文件选择：{{host = false variant = selector}`。

If a string selector contains a slash, then it's `"shortcut/filename"` and selects only the binary in the target toolchain whose `output_name`matches `"filename"`, i.e. it adds `output_name=["filename"]` to eachselector scope that the shortcut's name alone would yield. 如果字符串选择器包含斜杠，则为“快捷方式/文件名”，并仅在目标工具链中选择其“输出名”与“文件名”匹配的二进制文件，即，将“输出名= [“文件名”]]添加到仅快捷方式名称会产生的eachselector范围。

The scope that forms a full selector defines some of these:  构成完整选择器的范围定义了其中一些：

    variant (required) [string or `false`] The variant that applies if this selectormatches.  This can be `false` to choose no variant, or a stringthat names the variant.  See[`known_variants`](#known_variants) and[`universal_variants`](#universal_variants). 变体（必需）[字符串或'false']如果此选择器匹配，则适用的变体。这可以是“ false”（不选择任何变体），也可以是用于命名变体的字符串。参见[`known_variants`]（known_variants）和[`universal_variants`]（universal_variants）。

The rest below are matching criteria.  All are optional. The selector matches if and only if all of its criteria match.If none of these is defined, then the selector always matches. 下面的其余部分是符合条件的。所有都是可选的。当且仅当其所有条件都匹配时，选择器才匹配。如果未定义所有条件，则选择器将始终匹配。

The first selector in the list to match wins and then the rest of the list is ignored.  To construct more complex rules, use a blocklistselector with `variant=false` before a catch-all default variant, ora list of specific variants before a catch-all false variant. 列表中第一个与之匹配的选择器获胜，然后其余列表被忽略。要构建更复杂的规则，请在全部使用默认变体之前使用带有“ variant = false”的blocklistselector，或者在全部使用错误变体之前使用特定变体的列表。

Each "[strings]" criterion is a list of strings, and the criterion is satisfied if any of the strings matches against the candidate string. 每个“ [strings]”条件是一个字符串列表，如果任何字符串与候选字符串匹配，则满足该条件。

    host [boolean] If true, the selector matches in the host toolchain.If false, the selector matches in the target toolchain. host [boolean]如果为true，则选择器在主机工具链中匹配。如果为false，则选择器在目标工具链中匹配。

    testonly [boolean] If true, the selector matches targets with testonly=true.If false, the selector matches in targets without testonly=true. testonly [boolean]如果为true，则选择器将匹配testonly = true的目标。如果为false，则选择器将匹配没有testonly = true的目标。

    target_type [strings]: `"executable"`, `"loadable_module"`, or `"driver_module"` target_type [strings]：“可执行文件”，“可加载模块”或“驱动程序模块”

    output_name [strings]: target's `output_name` (default: its `target name`) output_name [strings]：目标的“ output_name”（默认值：其目标名称）

    label [strings]: target's full label with `:` (without toolchain suffix) label [strings]：目标的完整标签，带有`：`（不带工具链后缀）

    name [strings]: target's simple name (label after last `/` or `:`) name [字符串]：目标的简单名称（最后一个`/`或`：`之后的标签）

    dir [strings]: target's label directory (`//dir` for `//dir:name`). dir [strings]：目标的标签目录（“ // dir：name”中的“ // dir”）。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/config/BUILDCONFIG.gn:614  来自//build/config/BUILDCONFIG.gn:614

 
### select_variant_canonical  select_variant_canonical*This should never be set as a build argument.* It exists only to be set in `toolchain_args`.See //build/toolchain/clang_toolchain.gni for details. *永远不要将其设置为build参数。*仅存在于`toolchain_args`中。有关详细信息，请参见//build/toolchain/clang_toolchain.gni。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/config/BUILDCONFIG.gn:619  来自//build/config/BUILDCONFIG.gn:619

 
### select_variant_shortcuts  select_variant_shortcutsList of short names for commonly-used variant selectors.  Normally this is not set as a build argument, but it serves to document the availableset of short-cut names for variant selectors.  Each element of this listis a scope where `.name` is the short name and `.select_variant` is aa list that can be spliced into [`select_variant`](#select_variant). 常用变量选择器的简称列表。通常，不将其设置为构建参数，而是用于记录变量选择器的快捷名称的可用集。该列表的每个元素都是一个范围，其中`.name'是简称，`.select_variant`是一个可以拼接为[`select_variant]]（select_variant）的列表。

```
[{
  name = "host_asan"
  select_variant = [{
  dir = ["//third_party/yasm", "//third_party/vboot_reference", "//garnet/tools/vboot_reference", "//third_party/shaderc/third_party/spirv-tools"]
  host = true
  variant = "asan_no_detect_leaks"
}, {
  host = true
  variant = "asan"
}]
}]
```
**Current value (from the default):**  **当前值（默认值）：**

From //build/config/BUILDCONFIG.gn:455  来自//build/config/BUILDCONFIG.gn:455

 
### shell_enable_metal  shell_enable_metal 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/flutter/shell/config.gni:7  来自//third_party/flutter/shell/config.gni:7

 
### shell_enable_vulkan  shell_enable_vulkan 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/flutter/shell/config.gni:6  来自//third_party/flutter/shell/config.gni:6

 
### signed_image  Signed_image 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/images/BUILD.gn:48  来自//build/images/BUILD.gn:48

 
### skia_android_serial  skia_android_serial 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/skia/BUILD.gn:46  来自//third_party/skia/BUILD.gn:46

 
### skia_compile_processors  skia_compile_processors 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:59  来自//third_party/skia/BUILD.gn:59

 
### skia_enable_atlas_text  skia_enable_atlas_text 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:79  来自//third_party/skia/BUILD.gn:79

 
### skia_enable_ccpr  skia_enable_ccpr 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:47  来自//third_party/skia/BUILD.gn:47

 
### skia_enable_discrete_gpu  skia_enable_discrete_gpu 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:49  来自//third_party/skia/BUILD.gn:49

 
### skia_enable_flutter_defines  skia_enable_flutter_defines 

**Current value for `target_cpu = "arm64"`:** `true`  ** target_cpu =“ arm64”的当前值：** true

From //.gn:24  来自//.gn:24

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //third_party/skia/BUILD.gn:17  来自//third_party/skia/BUILD.gn:17

**Current value for `target_cpu = "x64"`:** `true`  ** target_cpu =“ x64”的当前值：** true

From //.gn:24  来自//.gn:24

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //third_party/skia/BUILD.gn:17  来自//third_party/skia/BUILD.gn:17

 
### skia_enable_fontmgr_android  skia_enable_fontmgr_android 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:84  来自//third_party/skia/BUILD.gn:84

 
### skia_enable_fontmgr_custom  skia_enable_fontmgr_custom 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:82  来自//third_party/skia/BUILD.gn:82

 
### skia_enable_fontmgr_custom_empty  skia_enable_fontmgr_custom_empty 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:83  来自//third_party/skia/BUILD.gn:83

 
### skia_enable_fontmgr_empty  skia_enable_fontmgr_empty 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:80  来自//third_party/skia/BUILD.gn:80

 
### skia_enable_fontmgr_fuchsia  skia_enable_fontmgr_fuchsia 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:85  来自//third_party/skia/BUILD.gn:85

 
### skia_enable_fontmgr_win  skia_enable_fontmgr_win 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:86  来自//third_party/skia/BUILD.gn:86

 
### skia_enable_fontmgr_win_gdi  skia_enable_fontmgr_win_gdi 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:87  来自//third_party/skia/BUILD.gn:87

 
### skia_enable_gpu  skia_enable_gpu 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/gn/skia.gni:11  来自//third_party/skia/gn/skia.gni:11

 
### skia_enable_nvpr  skia_enable_nvpr 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:48  来自//third_party/skia/BUILD.gn:48

 
### skia_enable_particles  skia_enable_particles 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/modules/particles/BUILD.gn:7  来自//third_party/skia/modules/particles/BUILD.gn:7

 
### skia_enable_pdf  skia_enable_pdf 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //.gn:25  来自//.gn:25

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:50  来自//third_party/skia/BUILD.gn:50

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //.gn:25  来自//.gn:25

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:50  来自//third_party/skia/BUILD.gn:50

 
### skia_enable_skottie  skia_enable_skottie 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/modules/skottie/BUILD.gn:9  来自//third_party/skia/modules/skottie/BUILD.gn:9

 
### skia_enable_skpicture  skia_enable_skpicture 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:52  来自//third_party/skia/BUILD.gn:52

 
### skia_enable_skshaper  skia_enable_skshaper 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/modules/skshaper/BUILD.gn:9  来自//third_party/skia/modules/skshaper/BUILD.gn:9

 
### skia_enable_sksl_interpreter  skia_enable_sksl_interpreter 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:53  来自//third_party/skia/BUILD.gn:53

 
### skia_enable_skvm_jit  skia_enable_skvm_jit 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:55  来自//third_party/skia/BUILD.gn:55

 
### skia_enable_spirv_validation  skia_enable_spirv_validation 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:51  来自//third_party/skia/BUILD.gn:51

 
### skia_enable_tools  skia_enable_tools 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/gn/skia.gni:12  来自//third_party/skia/gn/skia.gni:12

 
### skia_enable_vulkan_debug_layers  skia_enable_vulkan_debug_layers 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:57  来自//third_party/skia/BUILD.gn:57

 
### skia_generate_workarounds  skia_generate_workarounds 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:60  来自//third_party/skia/BUILD.gn:60

 
### skia_gl_standard  skia_gl_standard 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/skia/BUILD.gn:94  来自//third_party/skia/BUILD.gn:94

 
### skia_include_multiframe_procs  skia_include_multiframe_procs 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:69  来自//third_party/skia/BUILD.gn:69

 
### skia_lex  skia_lex 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:61  来自//third_party/skia/BUILD.gn:61

 
### skia_llvm_lib  skia_llvm_lib 

**Current value (from the default):** `"LLVM"`  **当前值（默认值）：**`“ LLVM”`

From //third_party/skia/BUILD.gn:66  来自//third_party/skia/BUILD.gn:66

 
### skia_llvm_path  skia_llvm_path 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/skia/BUILD.gn:65  来自//third_party/skia/BUILD.gn:65

 
### skia_pdf_subset_harfbuzz  skia_pdf_subset_harfbuzzTODO: set skia_pdf_subset_harfbuzz to skia_use_harfbuzz.  待办事项：将skia_pdf_subset_harfbuzz设置为skia_use_harfbuzz。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/gn/skia.gni:18  来自//third_party/skia/gn/skia.gni:18

 
### skia_qt_path  skia_qt_path 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/skia/BUILD.gn:58  来自//third_party/skia/BUILD.gn:58

 
### skia_skqp_global_error_tolerance  skia_skqp_global_error_tolerance 

**Current value (from the default):** `0`  **当前值（默认值）：**`0`

From //third_party/skia/BUILD.gn:63  来自//third_party/skia/BUILD.gn:63

 
### skia_tools_require_resources  skia_tools_require_resources 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:68  来自//third_party/skia/BUILD.gn:68

 
### skia_use_angle  skia_use_angle 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:21  来自//third_party/skia/BUILD.gn:21

 
### skia_use_dawn  skia_use_dawn 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:39  来自//third_party/skia/BUILD.gn:39

 
### skia_use_dng_sdk  skia_use_dng_sdk 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //.gn:26  来自//.gn:26

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:77  来自//third_party/skia/BUILD.gn:77

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //.gn:26  来自//.gn:26

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:77  来自//third_party/skia/BUILD.gn:77

 
### skia_use_egl  skia_use_egl 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:22  来自//third_party/skia/BUILD.gn:22

 
### skia_use_expat  skia_use_expat 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //.gn:27  来自//.gn:27

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:23  来自//third_party/skia/BUILD.gn:23

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //.gn:27  来自//.gn:27

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:23  来自//third_party/skia/BUILD.gn:23

 
### skia_use_experimental_xform  skia_use_experimental_xform 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:24  来自//third_party/skia/BUILD.gn:24

 
### skia_use_ffmpeg  skia_use_ffmpeg 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:25  来自//third_party/skia/BUILD.gn:25

 
### skia_use_fixed_gamma_text  skia_use_fixed_gamma_text 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:29  来自//third_party/skia/BUILD.gn:29

 
### skia_use_fontconfig  skia_use_fontconfig 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //.gn:28  来自//.gn:28

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:26  来自//third_party/skia/BUILD.gn:26

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //.gn:28  来自//.gn:28

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:26  来自//third_party/skia/BUILD.gn:26

 
### skia_use_fonthost_mac  skia_use_fonthost_mac 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:27  来自//third_party/skia/BUILD.gn:27

 
### skia_use_freetype  skia_use_freetype 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:28  来自//third_party/skia/BUILD.gn:28

 
### skia_use_harfbuzz  skia_use_harfbuzz 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/gn/skia.gni:14  来自//third_party/skia/gn/skia.gni:14

 
### skia_use_icu  skia_use_icu 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/gn/skia.gni:13  来自//third_party/skia/gn/skia.gni:13

 
### skia_use_libheif  skia_use_libheif 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:40  来自//third_party/skia/BUILD.gn:40

 
### skia_use_libjpeg_turbo  skia_use_libjpeg_turbo 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:30  来自//third_party/skia/BUILD.gn:30

 
### skia_use_libpng  skia_use_libpng 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:31  来自//third_party/skia/BUILD.gn:31

 
### skia_use_libwebp  skia_use_libwebp 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //.gn:29  来自//.gn:29

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:32  来自//third_party/skia/BUILD.gn:32

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //.gn:29  来自//.gn:29

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:32  来自//third_party/skia/BUILD.gn:32

 
### skia_use_lua  skia_use_lua 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:33  来自//third_party/skia/BUILD.gn:33

 
### skia_use_metal  skia_use_metal 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:38  来自//third_party/skia/BUILD.gn:38

 
### skia_use_opencl  skia_use_opencl 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:34  来自//third_party/skia/BUILD.gn:34

 
### skia_use_piex  skia_use_piex 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:35  来自//third_party/skia/BUILD.gn:35

 
### skia_use_sfntly  skia_use_sfntly 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //.gn:30  来自//.gn:30

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:78  来自//third_party/skia/BUILD.gn:78

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //.gn:30  来自//.gn:30

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:78  来自//third_party/skia/BUILD.gn:78

 
### skia_use_vulkan  skia_use_vulkan 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:102  来自//third_party/skia/BUILD.gn:102

 
### skia_use_wuffs  skia_use_wuffs 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/skia/BUILD.gn:36  来自//third_party/skia/BUILD.gn:36

 
### skia_use_x11  skia_use_x11 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //.gn:31  来自//.gn:31

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:41  来自//third_party/skia/BUILD.gn:41

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //.gn:31  来自//.gn:31

**Overridden from the default:** `true`  **被默认值覆盖**** true

From //third_party/skia/BUILD.gn:41  来自//third_party/skia/BUILD.gn:41

 
### skia_use_xps  skia_use_xps 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:42  来自//third_party/skia/BUILD.gn:42

 
### skia_use_zlib  skia_use_zlib 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //third_party/skia/BUILD.gn:37  来自//third_party/skia/BUILD.gn:37

 
### skia_version  skia_version 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //third_party/flutter/shell/version/version.gni:8  来自//third_party/flutter/shell/version/version.gni:8

 
### symbol_level  symbol_levelHow many symbols to include in the build. This affects the performance of the build since the symbols are large and dealing with them is slow.2 means regular build with symbols.1 means minimal symbols, usually enough for backtraces only. Symbols withinternal linkage (static functions or those in anonymous namespaces) may notappear when using this level.0 means no symbols. 构建中要包含多少个符号。这会影响构建的性能，因为符号很大并且处理它们的速度很慢。2表示使用符号进行常规构建。1表示符号最少，通常仅用于回溯。使用此级别时，可能不会出现内部链接内的符号（静态函数或匿名名称空间中的符号）.0表示没有符号。

**Current value (from the default):** `2`  **当前值（默认值）：** 2

From //build/config/compiler.gni:13  来自//build/config/compiler.gni:13

 
### target_cpu  target_cpu 

**Current value for `target_cpu = "arm64"`:** `"arm64"`  ** target_cpu =“ arm64”`的当前值：**`“ arm64”`

From //boards/arm64.gni:5  来自//boards/arm64.gni:5

**Overridden from the default:** `""`  **从默认值覆盖：**`“”`

**Current value for `target_cpu = "x64"`:** `"x64"`  ** target_cpu =“ x64”`的当前值：**`“ x64”`

From //boards/x64.gni:5  从//boards/x64.gni:5

**Overridden from the default:** `""`  **从默认值覆盖：**`“”`

 
### target_os  target_os 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

 
### target_sysroot  target_sysrootThe absolute path of the sysroot that is used with the target toolchain.  与目标工具链一起使用的sysroot的绝对路径。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/config/sysroot.gni:7  来自//build/config/sysroot.gni:7

 
### termina_disk  termina_diskThe termina disk image.  终端磁盘映像。

Defaults to the disk image from CIPD, but can be overridden to use a custom disk for development purposes. 默认为CIPD的磁盘映像，但是可以重写以使用自定义磁盘进行开发。

**Current value (from the default):** `"//prebuilt/virtualization/packages/termina_guest/images/arm64/vm_rootfs.img"`  **当前值（从默认值开始）：**`“ //prebuilt/virtualization/packages/termina_guest/images/arm64/vm_rootfs.img”`

From //src/virtualization/packages/termina_guest/BUILD.gn:18  来自//src/virtualization/packages/termina_guest/BUILD.gn:18

 
### termina_kernel  termina_kernelThe termina kernel image.  termina内核映像。

Defaults to the common linux kernel image from CIPD, but can be overridden to use a custom kernel for development purposes. 默认为CIPD的通用Linux内核映像，但可以重写以使用自定义内核进行开发。

**Current value (from the default):** `"//prebuilt/virtualization/packages/linux_guest/images/arm64/Image"`  **当前值（默认值）：**`“ // prebuilt / virtualization / packages / linux_guest / images / arm64 / Image”`

From //src/virtualization/packages/termina_guest/BUILD.gn:12  来自//src/virtualization/packages/termina_guest/BUILD.gn:12

 
### thinlto_cache_dir  Thinlto cache_dirThinLTO cache directory path.  ThinLTO缓存目录路径。

**Current value (from the default):** `"dartlang/thinlto-cache"`  **当前值（默认值）：**`“ dartlang / thinlto-cache”`

From //build/config/lto/config.gni:16  来自//build/config/lto/config.gni:16

 
### thinlto_jobs  thinlto_jobsNumber of parallel ThinLTO jobs.  并行ThinLTO作业的数量。

**Current value (from the default):** `8`  **当前值（默认值）：** 8

From //build/config/lto/config.gni:13  来自//build/config/lto/config.gni:13

 
### toolchain_manifests  工具链_清单Manifest files describing target libraries from toolchains. Can be either // source paths or absolute system paths. 清单文件描述了工具链中的目标库。可以是// //源路径或绝对系统路径。

**Current value (from the default):** `["/b/s/w/ir/k/prebuilt/third_party/clang/linux-x64/lib/aarch64-fuchsia.manifest"]`  **当前值（默认值）：**`[“ /b/s/w/ir/k/prebuilt/third_party/clang/linux-x64/lib/aarch64-fuchsia.manifest”]

From //build/images/manifest.gni:11  来自//build/images/manifest.gni:11

 
### toolchain_variant  工具链_变量*This should never be set as a build argument.* It exists only to be set in `toolchain_args`.See //build/toolchain/clang_toolchain.gni for details.This variable is a scope giving details about the current toolchain:`toolchain_variant.base`[label] The "base" toolchain for this variant, *often theright thing to use in comparisons, not `current_toolchain`.*This is the toolchain actually referenced directly in GNsource code.  If the current toolchain is not`shlib_toolchain` or a variant toolchain, this is the sameas `current_toolchain`.  In one of those derivativetoolchains, this is the toolchain the GN code probablythought it was in.  This is the right thing to use in a testlike `toolchain_variant.base == target_toolchain`, ratherrather than comparing against `current_toolchain`.`toolchain_variant.name`[string] The name of this variant, as used in `variant` fieldsin [`select_variant`](#select_variant) clauses.  In the basetoolchain and its `shlib_toolchain`, this is `""`.`toolchain_variant.suffix`[string] This is "-${toolchain_variant.name}", "" if name is empty.`toolchain_variant.is_pic_default`[bool] This is true in `shlib_toolchain`.The other fields are the variant's effects as defined in[`known_variants`](#known_variants). *永远不要将其设置为构建参数。*仅存在于`toolchain_args`中。详细信息请参见//build/toolchain/clang_toolchain.gni。此变量是一个范围，提供了有关当前工具链的详细信息：`toolchain_variant .base` [label]此变量的“基础”工具链，*通常是比较中使用的正确的东西，而不是`current_toolchain`。*这是在GNsource代码中直接引用的工具链。如果当前工具链不是“ shlib_toolchain”或变体工具链，则与“ current_toolchain”相同。在这些衍生工具链中的一个中，这就是GN代码可能所在的工具链。这是在类似testtool_toolchain_variant.base == target_toolchain的测试中使用的正确方法，而不是与current_toolchain..toolchain_variant.name进行比较。 [string]此变量的名称，在[select_variant]]（select_variant）子句的`variant`字段中使用。在basetoolchain及其shlib_toolchain中，这是`“”。 ]这在`shlib_toolchain`中是正确的。其他字段是[`known_variants`]（known_variants）中定义的变体效果。

```
{
  base = "//build/toolchain/fuchsia:arm64"
}
```
**Current value (from the default):**  **当前值（默认值）：**

From //build/config/BUILDCONFIG.gn:78  来自//build/config/BUILDCONFIG.gn:78

 
### universal_variants  通用变量 

```
[{
  configs = []
  name = "release"
  toolchain_args = {
  is_debug = false
}
}]
```
**Current value (from the default):**  **当前值（默认值）：**

From //build/config/BUILDCONFIG.gn:429  来自//build/config/BUILDCONFIG.gn:429

 
### universe_package_labels  Universe_package_labelsIf you add package labels to this variable, the packages will be included in the 'universe' package set, which represents all software that isproduced that is to be published to a package repository or to the SDK bythe build. The build system ensures that the universe package set includesthe base and cache package sets, which means you do not need to redundantlyinclude those labels in this variable. 如果将程序包标签添加到此变量，则程序包将包含在“ Universe”程序包集中，该程序包集表示要生成的所有要由构建版本发布到程序包存储库或SDK的软件。构建系统确保Universe软件包集包括基本软件包集和缓存软件包集，这意味着您无需在这些变量中多余地包含这些标签。

**Current value for `target_cpu = "arm64"`:** `["//garnet/tools/vboot_reference:cgpt_host", "//garnet/tools/vboot_reference:futility_host", "//bundles:tools"]`  ** target_cpu =“ arm64”的当前值：**`[“ // garnet / tools / vboot_reference：cgpt_host”，“ // garnet / tools / vboot_reference：futility_host”，“ // bundles：tools”]“

From //products/core.gni:73  来自//products/core.gni:73

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //BUILD.gn:34  来自//BUILD.gn:34

**Current value for `target_cpu = "x64"`:** `["//garnet/tools/vboot_reference:cgpt_host", "//garnet/tools/vboot_reference:futility_host", "//bundles:tools"]`  ** target_cpu =“ x64”`的当前值：**`[“ // garnet / tools / vboot_reference：cgpt_host”，“ // garnet / tools / vboot_reference：futility_host”，“ // bundles：tools”]“

From //products/core.gni:73  来自//products/core.gni:73

**Overridden from the default:** `[]`  **从默认值覆盖：**`[]`

From //BUILD.gn:34  来自//BUILD.gn:34

 
### update_kernels  update_kernels(deprecated) List of kernel images to include in the update (OTA) package. If no list is provided, all built kernels are included. The names in thelist are strings that must match the filename to be included in the updatepackage. （不建议使用）要包含在更新（OTA）软件包中的内核映像列表。如果未提供列表，则包括所有构建的内核。列表中的名称是字符串，必须与要包含在updatepackage中的文件名匹配。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/images/BUILD.gn:497  来自//build/images/BUILD.gn:497

 
### use_ccache  use_ccacheSet to true to enable compiling with ccache  设置为true以启用ccache编译

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/toolchain/ccache.gni:9  来自//build/toolchain/ccache.gni:9

 
### use_goma  use_gomaSet to true to enable distributed compilation using Goma.  设置为true以启用使用Goma的分布式编译。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/toolchain/goma.gni:9  来自//build/toolchain/goma.gni:9

 
### use_lto  use_ltoUse link time optimization (LTO).  使用链接时间优化（LTO）。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/config/lto/config.gni:7  来自//build/config/lto/config.gni:7

 
### use_mock_magma  use_mock_magma 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From [//third_party/mesa/src/intel/vulkan/BUILD.gn:25](https://fuchsia.googlesource.com/third_party/mesa/+/a3d377578a974ece0ec9935046eae2e397ae41cc/src/intel/vulkan/BUILD.gn#25)  来自[//third_party/mesa/src/intel/vulkan/BUILD.gn:25](https://fuchsia.googlesource.com/third_party/mesa/+/a3d377578a974ece0ec9935046eae2e397ae41cc/src/intel/vulkan/BUILD.gn25）

 
### use_prebuilt_dart_sdk  use_prebuilt_dart_sdkWhether to use the prebuilt Dart SDK for everything. When setting this to false, the preubilt Dart SDK will not be used insituations where the version of the SDK matters, but may still be used as anoptimization where the version does not matter. 是否对所有内容都使用预构建的Dart SDK。如果将其设置为false，则在该版本的SDK不重要的情况下，不会使用preubilt Dart SDK，但是在该版本的无关紧要的情况下，仍可以将其用作优化。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/dart/dart.gni:15  来自//build/dart/dart.gni:15

 
### use_prebuilt_ffmpeg  use_prebuilt_ffmpegUse a prebuilt ffmpeg binary rather than building it locally.  See //src/media/lib/ffmpeg/README.md for details.  This is ignored whenbuilding in variant builds for which there is no prebuilt.  In thatcase, ffmpeg is always built from source so as to be built with theselected variant's config.  When this is false (either explicitly or ina variant build) then //third_party/ffmpeg must be in the source tree,which requires:`jiri import -name integration third_party/ffmpeg https://fuchsia.googlesource.com/integration` 使用预构建的ffmpeg二进制文件，而不是在本地构建。有关详细信息，请参见//src/media/lib/ffmpeg/README.md。在没有预构建的变体构建中构建时，将忽略此操作。在这种情况下，ffmpeg始终是从源代码构建的，因此可以使用所选变体的配置来构建。如果这是错误的（无论是显式构建还是变体构建），则// third_party / ffmpeg必须位于源代码树中，这要求：jiri import -name integration third_party / ffmpeg https://fuchsia.googlesource.com/integration

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //src/media/lib/ffmpeg/BUILD.gn:14  来自//src/media/lib/ffmpeg/BUILD.gn:14

 
### use_scudo  use_scudoTODO(davemoore): Remove this entire mechanism once standalone scudo is the default (DNO-442)Enable the [Scudo](https://llvm.org/docs/ScudoHardenedAllocator.html)memory allocator. 待办事项（davemoore）：一旦默认的独立scudo（DNO-442）启用[Scudo]（https://llvm.org/docs/ScudoHardenedAllocator.html）内存分配器，就删除整个机制。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/config/scudo/scudo.gni:10  来自//build/config/scudo/scudo.gni:10

 
### use_thinlto  use_thinltoUse ThinLTO variant of LTO if use_lto = true.  如果use_lto = true，请使用LTO的ThinLTO变体。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/config/lto/config.gni:10  来自//build/config/lto/config.gni:10

 
### use_vbmeta  use_vbmetaIf true, then a vbmeta image will be generated for provided ZBI and the paving script will pave vbmeta images to the target device. 如果为true，则将为提供的ZBI生成vbmeta图像，并且铺装脚本会将vbmeta图像铺装到目标设备。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/images/vbmeta.gni:10  来自//build/images/vbmeta.gni:10

 
### use_vboot  use_vbootUse vboot images  使用vboot映像

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/images/boot.gni:11  来自//build/images/boot.gni:11

 
### use_vulkan_loader_for_tests  use_vulkan_loader_for_testsMesa doesn't properly handle loader-less operation; their GetInstanceProcAddr implementation returns 0 for some interfaces.On ARM there may be multiple libvulkan_arms, so they can't all be linkedto. Mesa无法正确处理无装载程序的操作；它们的GetInstanceProcAddr实现对某些接口返回0.在ARM上可能有多个libvulkan_arms，因此不能全部链接到它们。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //garnet/lib/magma/gnbuild/magma.gni:32  来自//garnet/lib/magma/gnbuild/magma.gni:32

 
### using_fuchsia_sdk  using_fuchsia_sdkOnly set in buildroots where targets configure themselves for use with the Fuchsia SDK 仅在目标自行配置以与Fuchsia SDK一起使用的buildroot中设置

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/fuchsia/sdk.gni:8  来自//build/fuchsia/sdk.gni:8

 
### vbmeta_a_partition  vbmeta_a_partition 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:44  来自//build/images/BUILD.gn:44

 
### vbmeta_b_partition  vbmeta_b_partition 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:45  来自//build/images/BUILD.gn:45

 
### vbmeta_r_partition  vbmeta_r_partition 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:46  来自//build/images/BUILD.gn:46

 
### virtmagma_debug  virtmagma_debugEnable verbose logging in virtmagma-related code  在virtmagma相关代码中启用详细日志记录

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //garnet/lib/magma/include/virtio/virtmagma_debug.gni:7  来自//garnet/lib/magma/include/virtio/virtmagma_debug.gni:7

 
### vk_loader_debug  vk_loader_debug 

**Current value (from the default):** `"warn,error"`  **当前值（默认值）：**`“ warn，error”`

From [//third_party/vulkan_loader_and_validation_layers/loader/BUILD.gn:26](https://fuchsia.googlesource.com/third_party/vulkan_loader_and_validation_layers/+/66e293b577c45aac9478e2341d37147ec4863151/loader/BUILD.gn#26)  来自[//third_party/vulkan_loader_and_validation_layers/loader/BUILD.gn:26](https://fuchsia.googlesource.com/third_party/vulkan_loader_and_validation_layers/+/66e293b577c45aac9478e2341d37147ec4863151/loader/BUILD.gn26）

 
### vulkan_sdk  vulkan_sdk 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //garnet/lib/vulkan/tests/vkprimer/BUILD.gn:8  来自//garnet/lib/vulkan/tests/vkprimer/BUILD.gn:8

 
### warn_on_sdk_changes  warn_on_sdk_changesWhether to only warn when an SDK has been modified. If false, any unacknowledged SDK change will cause a build failure. 是否仅在修改SDK时发出警告。如果为false，则任何未经确认的SDK更改都会导致构建失败。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/sdk/config.gni:11  来自//build/sdk/config.gni:11

 
### wlancfg_config_type  wlancfg_config_typeSelects the wlan configuration type to use. Choices: "client" - client mode"ap" - access point mode"" (empty string) - no configuration 选择要使用的无线配置类型。选项：“客户端”-客户端模式“ ap”-接入点模式“”（空字符串）-无配置

**Current value (from the default):** `"client"`  **当前值（默认值）：**`“ client”`

From //src/connectivity/wlan/wlancfg/BUILD.gn:16  来自//src/connectivity/wlan/wlancfg/BUILD.gn:16

 
### zbi_compression  zbi_compressionCompression setting for ZBI "storage" items. This can be either "lz4f" or "zstd", optionally followed by ".LEVEL"where `LEVEL` can be an integer or "max". ZBI“存储”项目的压缩设置。它可以是“ lz4f”或“ zstd”，并可选地后面跟“ .LEVEL”，其中“ LEVEL”可以是整数或“ max”。

**Current value (from the default):** `"lz4f"`  **当前值（默认值）：**`“ lz4f”`

From //build/config/fuchsia/zbi.gni:11  来自//build/config/fuchsia/zbi.gni:11

 
### zedboot_cmdline_args  zedboot_cmdline_argsList of kernel command line arguments to bake into the Zedboot image. See //docs/reference/kernel/kernel_cmdline.md and[`zedboot_devmgr_config`](#zedboot_devmgr_config). 烘烤到Zedboot映像中的内核命令行参数列表。参见//docs/reference/kernel/kernel_cmdline.md和[`zedboot_devmgr_config`]（zedboot_devmgr_config）。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/images/zedboot/BUILD.gn:18  来自//build/images/zedboot/BUILD.gn:18

 
### zedboot_cmdline_files  zedboot_cmdline_filesFiles containing additional kernel command line arguments to bake into the Zedboot image.  The contents of these files (in order) come after anyarguments directly in [`zedboot_cmdline_args`](#zedboot_cmdline_args).These can be GN `//` source pathnames or absolute system pathnames. 包含其他内核命令行参数的文件可放入Zedboot映像中。这些文件的内容（按顺序）直接在[`zedboot_cmdline_args]（zedboot_cmdline_args）中的任何参数之后。它们可以是GN`//`源路径名或绝对系统路径名。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //build/images/zedboot/BUILD.gn:24  来自//build/images/zedboot/BUILD.gn:24

 
### zedboot_devmgr_config  zedboot_devmgr_configList of arguments to populate /boot/config/devmgr in the Zedboot image.  在Zedboot映像中填充/ boot / config / devmgr的参数列表。

**Current value (from the default):** `["netsvc.netboot=true"]`  **当前值（默认值）：**`[“ netsvc.netboot = true”]`

From //build/images/zedboot/BUILD.gn:27  来自//build/images/zedboot/BUILD.gn:27

 
### zircon_a_partition  zircon_a_partitionarguments to fx flash script  FX Flash脚本的参数

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:41  来自//build/images/BUILD.gn:41

 
### zircon_args  zircon_args[Zircon GN build arguments](/docs/gen/zircon_build_arguments.md). The default passes through GOMA/ccache settings and[`select_variant`](#select_variant) shorthand selectors.**Only set this if you want to wipe out all the defaults thatpropagate from Fuchsia GN to Zircon GN.**  The default valuefolds in [`zircon_extra_args`](#zircon_extra_args), so usuallyit's better to just set `zircon_extra_args` and leave `zircon_args` alone.Any individual Zircon build argument set in `zircon_extra_args` willsilently clobber the default value shown here. [Zircon GN构建参数]（/ docs / gen / zircon_build_arguments.md）。默认值通过GOMA / ccache设置和[`select_variant`]（select_variant）速记选择器传递。**仅当要清除从Fuchsia GN到Zircon GN的所有默认值时，才设置此值。**默认值折叠在[`中。 zircon_extra_args`]（zircon_extra_args），因此通常最好只设置`zircon_extra_args`而不管`zircon_args`。``zircon_extra_args`中设置的任何单独的Zircon构建参数都会悄无声息地破坏此处显示的默认值。

```
{
  default_deps = ["//:legacy-arm64"]
  enable_netsvc_debugging_features = false
  goma_dir = "/home/swarming/goma"
  use_ccache = false
  use_goma = false
  variants = []
  zbi_compression = "lz4f"
}
```
**Current value (from the default):**  **当前值（默认值）：**

From //BUILD.gn:85  来自//BUILD.gn:85

 
### zircon_asserts  zircon_asserts 

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/config/fuchsia/BUILD.gn:206  来自//build/config/fuchsia/BUILD.gn:206

 
### zircon_b_partition  zircon_b_partition 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:42  来自//build/images/BUILD.gn:42

 
### zircon_build_root  zircon_build_root 

**Current value (from the default):** `"//zircon"`  **当前值（默认值）：**`“ // zircon”`

From //garnet/lib/magma/gnbuild/magma.gni:13  来自//garnet/lib/magma/gnbuild/magma.gni:13

 
### zircon_compdb_filter  zircon_compdb_filterCompliation database filter. Gets passed to --export_compile_commands=<filter>. Default is $target_cpu. 编译数据库过滤器。获取传递给--export_compile_commands = <过滤器>。默认值为$ target_cpu。

**Current value (from the default):** `"arm64"`  **当前值（默认值）：**`“ arm64”`

From //BUILD.gn:64  来自//BUILD.gn:64

 
### zircon_enable_netsvc_debugging_features  zircon_enable_netsvc_debugging_featuresWhether to include various features (non-shipping, insecure, etc.) in the netsvc build. 是否在netsvc构建中包括各种功能（非运输，不安全等）。

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //products/core.gni:9  来自//products/core.gni:9

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //BUILD.gn:55  来自//BUILD.gn:55

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //products/core.gni:9  来自//products/core.gni:9

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //BUILD.gn:55  来自//BUILD.gn:55

 
### zircon_enable_netsvc_debugging_features  zircon_enable_netsvc_debugging_features 

**Current value for `target_cpu = "arm64"`:** `false`  ** target_cpu =“ arm64”`的当前值：**`false`

From //products/core.gni:10  来自//products/core.gni:10

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //BUILD.gn:56  来自//BUILD.gn:56

**Current value for `target_cpu = "x64"`:** `false`  ** target_cpu =“ x64”的当前值：** false

From //products/core.gni:10  来自//products/core.gni:10

**Overridden from the default:** `false`  **从默认值覆盖：**`false`

From //BUILD.gn:56  来自//BUILD.gn:56

 
### zircon_extra_args  锆石extra_args[Zircon GN build arguments](/docs/gen/zircon_build_arguments.md). This is included in the default value of [`zircon_args`](#zircon_args) soyou can set this to add things there without wiping out the defaults.When you set `zircon_args` directly, then this has no effect at all.Arguments you set here override any arguments in the default`zircon_args`.  There is no way to append to a value from the defaults.Note that for just setting simple (string-only) values in Zircon GN's[`variants`](/docs/gen/zircon_build_arguments.md#variants), thedefault [`zircon_args`](#zircon_args) uses a `variants` value derived from[`select_variant`](#select_variant) so for simple cases there is no needto explicitly set Zircon's `variants` here. [Zircon GN构建参数]（/ docs / gen / zircon_build_arguments.md）。它包含在[`zircon_args`]（zircon_args）的默认值中，因此您可以将其设置为在其中添加内容而无需清除默认值。当直接设置`zircon_args`时，则根本没有效果。在这里设置的参数覆盖默认的zircon_args中的所有参数。无法从默认值中追加值。请注意，仅在Zircon GN的[`variants`]（/​​ docs / gen / zircon_build_arguments.mdvariants）中设置简单（仅字符串）值时，默认的[`zircon_args]] （zircon_args）使用从[`select_variant`]（select_variant）派生的'variants'值，因此对于简单情况，无需在此处显式设置Zircon的'variants'。

**Current value (from the default):** `{ }`  **当前值（默认值）：**`{}`

From //BUILD.gn:47  来自//BUILD.gn:47

 
### zircon_extra_deps  zircon_extra_depsAdditional Zircon GN labels to include in the Zircon build.  Zircon版本中将包含其他Zircon GN标签。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //BUILD.gn:51  来自//BUILD.gn:51

 
### zircon_r_partition  zircon_r_partition 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/images/BUILD.gn:43  来自//build/images/BUILD.gn:43

 
### zircon_tracelog  zircon_tracelogWhere to emit a tracelog from Zircon's GN run. No trace will be produced if given the empty string. Path can be source-absolute or system-absolute. 从Zircon的GN运行中向哪里发出跟踪日志。如果给出空字符串，将不会产生跟踪。路径可以是绝对源或系统绝对路径。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //BUILD.gn:60  来自//BUILD.gn:60

 
### zvb_partition_name  zvb_partition_namePartition name from where image will be verified  将从中验证图像的分区名称

**Current value (from the default):** `"zircon"`  **当前值（默认值）：**`“ zircon”`

From //build/images/vbmeta.gni:28  来自//build/images/vbmeta.gni:28

 
### zxcrypt_key_source  zxcrypt_key_sourceThis argument specifies from where the system should obtain the zxcrypt master key to the system data partition. 此参数指定系统应从何处获取系统数据分区的zxcrypt主密钥。

This value be reified as /boot/config/zxcrypt in both the zircon boot image and the zedboot boot image, for consumption by fshost and the paver,respectively. 在zircon引导映像和zedboot引导映像中，此值均被统一化为/ boot / config / zxcrypt，以分别供fshost和paver使用。

Acceptable values are:  可接受的值为：
* "null": the device should use an all-0's master key, as we lack support for any secure on-device storage. *“ null”：设备应该使用全0的主密钥，因为我们不支持任何安全的设备上存储。
* "tee": the device is required to have a Trusted Execution Environment (TEE) which includes the "keysafe" Trusted Application (associated with theKMS service).  The zxcrypt master key should be derived from a per-devicekey accessible only to trusted apps running in the TEE. *“ tee”：要求设备具有可信执行环境（TEE），其中包括“密钥安全”可信应用程序（与KMS服务关联）。 zxcrypt主密钥应从每个设备密钥派生而来，只有在TEE中运行的受信任应用程序才能访问该设备密钥。
* "tee-opportunistic": the device will attempt to use keys from the TEE if available, but will fall back to using the null key if the key from the TEEdoes not work, or if the TEE is not functional on this device. *“开球机会”：设备将尝试使用TEE中的密钥（如果可用），但是如果TEE中的密钥不起作用或者TEE在该设备上不起作用，则将退回到使用空密钥。
* "tee-transitional": the device will require the use of a key from the TEE for new volume creation, but will continue to try both a TEE-sourced key andthe null key when unsealing volumes. *“ tee-transitional”：设备将需要使用TEE中的密钥来创建新的卷，但在启封卷时将继续尝试使用TEE来源的密钥和空密钥。

In the future, we may consider adding support for TPMs, or additional logic to explicitly support other fallback behavior. 将来，我们可能会考虑添加对TPM的支持，或增加其他逻辑以显式支持其他后备行为。

**Current value (from the default):** `"null"`  **当前值（默认值）：**`“ null”`

From //build/images/zxcrypt.gni:29  来自//build/images/zxcrypt.gni:29

 
## `target_cpu = "arm64"`  `target_cpu =“ arm64”` 

 
### amlogic_decoder_tests  amlogic_decoder_tests 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //garnet/drivers/video/amlogic-decoder/BUILD.gn:11  来自//garnet/drivers/video/amlogic-decoder/BUILD.gn:11

 
### arm_float_abi  arm_float_abiThe ARM floating point mode. This is either the string "hard", "soft", or "softfp". An empty string means to use the default one for thearm_version. ARM浮点模式。这是字符串“ hard”，“ soft”或“ softfp”。空字符串表示将默认值用于arm_version。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/config/arm.gni:20  来自//build/config/arm.gni:20

 
### arm_optionally_use_neon  arm_optionally_use_neonWhether to enable optional NEON code paths.  是否启用可选的NEON代码路径。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //build/config/arm.gni:31  来自//build/config/arm.gni:31

 
### arm_tune  arm_tuneThe ARM variant-specific tuning mode. This will be a string like "armv6" or "cortex-a15". An empty string means to use the default for thearm_version. ARM特定于变量的调整模式。这将是一个字符串，例如“ armv6”或“ cortex-a15”。空字符串表示将默认值用于arm_version。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //build/config/arm.gni:25  来自//build/config/arm.gni:25

 
### arm_use_neon  arm_use_neonWhether to use the neon FPU instruction set or not.  是否使用霓虹灯FPU指令集。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //build/config/arm.gni:28  来自//build/config/arm.gni:28

 
### arm_version  arm_version 

**Current value (from the default):** `8`  **当前值（默认值）：** 8

