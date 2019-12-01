 
# Bootserver  引导服务器 

The `bootserver` host tool can be used to pave, netboot or boot Fuchsia on a target device. This tool is very likely to go away in the short future witha replacement being currently implemented. bootserver主机工具可用于在目标设备上进行铺装，netboot或引导Fuchsia。该工具很可能在不久的将来消失，目前正在实施替换。

 
## x64  x64 

 
### Generic  泛型 

To pave and boot on a generic `x64` target, run:  要在通用的“ x64”目标上铺装并引导，请运行：

```
bootserver \
    --boot "$IMAGES_PATH/fuchsia.zbi" \
    --bootloader "$IMAGES_PATH/fuchsia.esp.blk" \
    --fvm "$IMAGES_PATH/obj/build/images/fvm.sparse.blk" \
    --zircona "$IMAGES_PATH/fuchsia.zbi" \
    --zirconr "$IMAGES_PATH/zedboot.zbi"
```
 

 
### Chromebook  Chromebook 

To pave and boot on a `chromebook` target, run:  要铺平并启动`chromebook`目标，请运行：

 

```
bootserver \
    --boot "$IMAGES_PATH/fuchsia.zbi" \
    --fvm "$IMAGES_PATH/obj/build/images/fvm.sparse.blk" \
    --zircona "$IMAGES_PATH/fuchsia.zbi.vboot" \
    --zirconr "$IMAGES_PATH/zedboot.vboot"
```
 

 

 
## arm64  臂64 

To pave and boot on an `arm64` target, run:  要铺装并引导至“ arm64”目标，请运行：

```
bootserver \
    --boot "$IMAGES_PATH/fuchsia.zbi" \
    --fvm "$IMAGES_PATH/obj/build/images/fvm.sparse.blk" \
    --zircona "$IMAGES_PATH/fuchsia.zbi" \
    --zirconr "$IMAGES_PATH/zedboot.zbi"
```
