 
# Third-party Rust Crates  第三方防锈箱 

 
## Overview  总览 

Fuchsia uses third-party Rust crates. They are placed in [`//third-party/rust_crates/vendor`][3p-vendor].This set of crates is based on the dependencies listed in[`//third_party/rust_crates/Cargo.toml`][3p-cargo-toml].If you don't find a crate that you want to use, you may bring that into Fuchsia. 紫红色使用第三方Rust板条箱。它们放置在[`// third-party / rust_crates / vendor`] [3p-vendor]中。这组箱子是基于[`//third_party/rust_crates/Cargo.toml`][3p-如果您找不到要使用的板条箱，可以将其放入紫红色中。

Roughly, it is a 3-step process.  大致来说，这是一个三步过程。
 - Calculate dependencies.  -计算依赖关系。
 - Get OSRB approval.  -获得OSRB批准。
 - Upload the change for code review.  -上传更改以进行代码审查。

Pay attention to transitive dependencies: A third-party crate may depend on other third-party crates. List all the new crates that end up with beingbrought in, in the OSRB review. For OSRB, follow the instructions under the"Process for 3rd Party Hosted Code" section in [this document][osrb-process]. 注意传递依赖性：第三方箱可能依赖于其他第三方箱。在OSRB审查中列出所有最终带入的新板条箱。对于OSRB，请按照[本文档] [osrb-process]中“第三方托管代码的处理”部分下的说明进行操作。

Note, one needs to get OSRB approval first _before_ uploading a CL for review.  请注意，必须先获得OSRB批准_之前_上传CL进行审查。

 
## Steps to add a third-party crate  添加第三方板条箱的步骤 

 
1. Change directory to Fuchsia repo base directory. (eg. cd ~/fuchsia) 1.将目录更改为Fuchsia repo基本目录。 （例如cd〜/紫红色）
1. Add an entry in [`third_party/rust_crates/Cargo.toml`][3p-cargo-toml]for the crate you want to add. 1.在[`third_party / rust_crates / Cargo.toml`] [3p-cargo-toml]中添加要添加的板条箱的条目。
   ```
   fx update-rustc-third-party
   ```
1. Run the following command to Calculate the dependencies and download the crates.This will download all crates listed in[`rust_crates/Cargo.toml`][3p-cargo-toml] as well as their dependencies,place them in the `vendor` directory, and update `Cargo.toml' and`Cargo.lock`.Prerequisite: on Linux, `pkg-config` needs to be installed. 1.运行以下命令来计算依赖性并下载板条箱。这将下载[rust_crates / Cargo.toml`] [3p-cargo-toml]中列出的所有板条箱以及它们的依赖性，将它们放在供应商中目录，并更新Cargo.toml和Cargo.lock前提：在Linux上，需要安装pkg-config。
   ```
   fx set core.x64 && fx build
   ```
1. Do a build test. For example,  1.进行构建测试。例如，
   ```
   fx update-rustc-crate-map --output third_party/rust_crates/crate_map.json
   ```
1. Run the following command to Update crate-map. This will update `crate_map.json` with information about the Rust cratesavailable for each target (Fuchsia and host).Note that this step uses information from the build step - make sure that thebuild for the `third_party` folder has succeeded first before running thiscommand.  This would be part of the `fx build` you are expected to run in theprevious step. 1.运行以下命令更新crate-map。这将使用每个目标（紫红色和主机）可用的Rust装箱信息更新`crate_map.json`。请注意，此步骤使用构建步骤中的信息-确保在运行此命令之前首先成功完成`third_party`文件夹的构建。这将是您希望在上一步中运行的“ fx build”的一部分。
1. Identify all the crates to be brought (see the diff in `//third_party/rust_crates/vendor/`).Do not submit the CL for code review. Get OSRB approval first.If there are any files in the source repository that are not included whenvendored, make a note of that for the OSRB reviewer. For example, font filesthat are only used for testing but are excluded when the crate is vendored.If you are not a Google employee, you will need to ask a Google employee todo this part for you. 1.确定所有要携带的包装箱（请参阅`// third_party / rust_crates / vendor /`中的差异）。请勿将CL提交代码审查。首先获得OSRB批准。如果供应商提供的源存储库中没有任何文件，请为OSRB审阅者记录下来。例如，字体文件仅用于测试，而在供应板条箱时将其排除。如果您不是Google员工，则需要请Google员工为您做这部分。
1. After the OSRB approval, upload the change for review to Gerrit.  1.在OSRB批准后，将更改上传到Gerrit进行审查。
1. Get code-review+2, merge the change into [third_party/rust_crates][3p-crates].  1.获得code-review + 2，将更改合并到[third_party / rust_crates] [3p-crates]。

 
## Steps to update a third-party crate  更新第三方板条箱的步骤 

Updating is very similar to adding a crate.  更新与添加条板箱非常相似。
1. Start by bumping bumping the version number of the crate in [`third_party/rust_crates/Cargo.toml`](3p-cargo-toml] and rerunning`fx update-rustc-third-party as above. 1.首先修改[[third_party / rust_crates / Cargo.toml]]（3p-cargo-toml]中的木箱版本号，然后如上所述重新运行fx update-rustc-third-party。
1. Identify all new library dependencies brought in (see the diff in `//third_party/rust_crates/vendor/`).Again, do not submit the CL for code review until you've received OSRBapproval for any new dependencies added. 1.确定引入的所有新库依赖项（请参阅`// third_party / rust_crates / vendor /`中的差异）。同样，在收到OSRBapproval所添加的任何新依赖项之前，请不要提交CL进行代码审查。
1. After OSRB approval, upload the change for review to Gerrit and merge as above. 1.在OSRB批准后，将更改上传到Gerrit进行审核，然后如上所述进行合并。

 
## Adding a new mirror  添加新镜像 

 
1. Request the addition of a mirror on *fuchsia.googlesource.com*;  1.请求在* fuchsia.googlesource.com *上添加一个镜像；
1. Add the mirror to the [Jiri manifest][jiri-manifest] for the Rust runtime;  1.将镜像添加到Rust运行时的[Jiri清单] [jiri-manifest]中；
1. Add a patch section for the crate to the workspace;  1.将板条箱的修补程序部分添加到工作区；
1. Run the update script.  1.运行更新脚本。

[3p-crates]: /third_party/rust_crates/ [3p-cargo-toml]: /third_party/rust_crates/Cargo.toml[3p-vendor]: /third_party/rust_crates/vendor[osrb-process]: https://docs.google.com/document/d/1X3eNvc4keQxOpbkGUiyYBMtr3ueEnVQCPW61FT96o_E/edit#heading=h.7mb7m2qs89th[jiri-manifest]: https://fuchsia.googlesource.com/manifest/+/master/runtimes/rust "Jiri manifest" [3p-crates]：/ third_party / rust_crates / [3p-cargo-toml]：/third_party/rust_crates/Cargo.toml[3p-vendor]：/ third_party / rust_crates / vendor [osrb-process]：https：// docs .google.com / document / d / 1X3eNvc4keQxOpbkGUiyYBMtr3ueEnVQCPW61FT96o_E / editheading = h.7mb7m2qs89th [jiri-manifest]：https://fuchsia.googlesource.com/manifest/+/master/runtimes/rust“ Jiri清单”

 
## Unicode crates  Unicode板条箱 

If the project requires importing a new third-party crate to handle functionality related to Unicode and internationalization, prefer crates fromthe [UNIC project](https://crates.io/crates/unic) when available. 如果项目需要导入新的第三方包装箱以处理与Unicode和国际化相关的功能，则请使用[UNIC项目]（https://crates.io/crates/unic）中可用的包装箱。

 
### Grandfathered non-UNIC crates  祖父的非UNIC板条箱 

The following non-UNIC crates are already vendored and are grandfathered, but we will aim to migrate to UNIC equivalents when possible. 以下非UNIC板条箱已被出售并被继承，但我们将力争在可能的情况下迁移到UNIC等效板条箱。

 
* unicode-bidi  * unicode-bidi
* unicode-normalization  * Unicode规范化
* unicode-segmentation  * unicode分段
* unicode-width  * Unicode宽度
* unicode-xid  * unicode-xid

We should encourage upstream dependencies to migrate to UNIC as well.  我们也应鼓励上游依赖项也迁移到UNIC。

 
### Rationale for standardization  标准化依据 

UNIC crates have distinct advantages over other crates:  UNIC板条箱相对于其他板条箱具有明显的优势：

 
* UNIC crates are developed in a single repo, with shared common code and a single version scheme. * UNIC板条箱是在单个存储库中开发的，具有共享的通用代码和单个版本方案。

 
  * Independently developed crates do not share a common release schedule, versioning scheme, or adherence to any particular version of the Unicodestandard. *独立开发的板条箱不共享通用的发布时间表，版本控制方案，也不遵循Unicode标准的任何特定版本。

 
* UNIC crates are generated from a consistent set of Unicode data files.  * UNIC包装箱是从一组一致的Unicode数据文件中生成的。

 
  * Each of the independent crates uses an arbitrary version and subset of the data. For example, different crates might have different assumptionsabout whether a particular code point is assigned, what its propertiesare, etc. *每个独立的板条箱都使用任意版本和数据子集。例如，关于是否分配了特定代码点，其属性是什么等，不同的包装箱可能有不同的假设。

 
* The UNIC project is aiming for comprehensive feature coverage, to be like [ICU](http://site.icu-project.org/) for Rust. If the project succeeds, ourdependencies on unrelated Unicode crates should be reduced over time. * UNIC项目旨在全面覆盖功能，就像Rust的[ICU]（http://site.icu-project.org/）一样。如果项目成功，则随着时间的流逝，我们对不相关的Unicode板条箱的依赖性应降低。

