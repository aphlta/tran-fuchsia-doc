 
# Device Firmware  设备固件 

Device firmware are binary blobs containing code that are executed by device hardware. The binary blob is available in the driver's namespace for loading. 设备固件是二进制blob，其中包含由设备硬件执行的代码。二进制blob在驱动程序的名称空间中可用于加载。

Device firmware are stored in CIPD (Chrome Infrastructure Package Deployment) and mirrored in Google Storage. 设备固件存储在CIPD（Chrome基础结构软件包部署）中，并在Google Storage中进行镜像。

 
## Create a Firmware Package  创建固件包 

To create a firmware package, create a directory containing the following files: 要创建固件包，请创建一个包含以下文件的目录：

 
* One or more firmware files  *一个或多个固件文件
* A license file  *许可证文件
* [README.fuchsia](/docs/development/source_code/third-party-metadata.md)  * [README.fuchsia]（/ docs / development / source_code / third-party-metadata.md）

README.fuchsia must contain at least the following directives:  README.fuchsia必须至少包含以下指令：

 
* `Name`  *名称
* `Version`  *`版本`
* `Upstream Git`  *`上游Git`
* `License`  *`许可证`
* `License File`  *许可证文件

If this is the first time you uploaded to CIPD from the host system, authenticate with CIPD: 如果这是您首次从主机系统上传到CIPD，请使用CIPD进行身份验证：

```
fx cipd auth-login
```
 

Upload and tag the package in CIPD using the following command:  使用以下命令在CIPD中上载并标记软件包：

```
fx cipd create -in <package-directory> -install-mode copy \
    -name <package-name> \
    -tag git_repository:<source-git-repositry> \
    -tag git_revision:<source-git-revision>
```
 

`package-name` has the format `fuchsia/firmware/<name>`.  “ package-name”的格式为“ fuchsia / firmware / <name>”。

`<name>` should be a string that identifies the firmware. It may contain any non-whitespace character. It is helpful to identify the driver that willuse the firmware in the name. “ <名称>”应该是标识固件的字符串。它可以包含任何非空格字符。确定名称中将使用固件的驱动程序会很有帮助。

After this step, the package is uploaded to CIPD. Check the [CIPD browser here](https://chrome-infra-packages.appspot.com/#/?path=fuchsia/firmware)for packages under `fuchsia/firmware`. 完成此步骤后，程序包将上传到CIPD。在[fuchsia / firmware]下检查[CIPD浏览器]（https://chrome-infra-packages.appspot.com//?path=fuchsia/firmware）中的软件包。

 
## Adding the Firmware Package to the Build  将固件包添加到内部版本 

Add the following entry in `prebuilt/zircon.ensure`:  在`prebuilt / zircon.ensure`中添加以下条目：

```
@Subdir firmware/<name>
<package-name> git_revision:<source-git-revision>
```
 

Where `<name>`, `<package-name>` and `<source-git-revision>` matches the values passed to `cipd create` above. The package will be downloaded tothe path specified by `@Subdir` under `prebuilt`, i.e.`prebuilt/firmware/<name>`. 其中<name> 、、 <package-name>和<source-git-revision>与上面传递给cipd create的值匹配。软件包将被下载到prebuild下的@Subdir指定的路径，即prebuilt / firmware / <name>。

Next, update `prebuilt/zircon.versions` with the following command:  接下来，使用以下命令更新`prebuilt / zircon.versions`：

```
scripts/download-prebuilt --resolve
```
 

Upload this change to Gerrit and send it to the CQ.  The firmware package will be downloaded by `scripts/download-prebuilt` along with the toolchain and QEMU. 将此更改上传到Gerrit并将其发送到CQ。固件软件包将通过`scripts / download-prebuilt`以及工具链和QEMU下载。

 
## Using the Firmware Package in the Driver  在驱动程序中使用固件包 

Add the following line to the driver's `rules.mk`:  将以下行添加到驱动程序的“ rules.mk”中：

```
MODULE_FIRMWARE := <name>/<path-to-binary-blob>
```
 

This will install the firmware to bootfs under `/boot/lib/firmware/$(basename $(MODULE_FIRMWARE))`. 这会将固件安装到`/ boot / lib / firmware / $（basename $（MODULE_FIRMWARE））'下的bootfs中。

