 
# VS Code Configuration  VS代码配置 

 
## General configurations  常规配置 

 
### Speed up automatic file reloading  加速自动文件重新加载VS Code watches external file changes. It automatically reloads the lastest stored file if it does not have a working copy that conflicts. Watching and detecting changes, however, can take long time. The larger the code base, the longer it takes to detect the file change. Excluding some directories from the search space improves the speed.  VS Code监视外部文件更改。如果没有冲突的工作副本，它将自动重新加载最新存储的文件。但是，监视和检测更改可能需要很长时间。代码库越大，检测文件更改所需的时间就越长。从搜索空间中排除某些目录可以提高速度。

Follow the menu Code -> Preferences -> Text Editor -> File -> Add Pattern Add a directory pattern you want to exclude the search from. Alternatively one can directory modify `settings.json` and add exclude pattern similar to below 遵循菜单代码->首选项->文本编辑器->文件->添加模式添加要从中排除搜索的目录模式。或者，可以在目录中修改“ settings.json”并添加类似于以下内容的排除模式

```
    "files.watcherExclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "**/topaz": true,
        "**/.cipd": true,
        "**/.idea": true,
        "**/.ssh": true,
        "**/buildtools": true,
        "**/zircon/prebuilt": true,
        "**/src/chromium": true,
        "**/garnet/third_party": true,
        "**/garnet/test_data": true,
        "**/zircon/experimental": true,
        "**/zircon/third_party": true,
        "**/out": true,
        "**/rustfmt.toml": true,
        "**/PATENTS": true,
        "**/.dir-locals.el": true,
        "**/.gitignore": true,
        "**/.jiri_manifest": true,
        "**/AUTHORS": true,
        "**/CMakeLists.txt": true,
        "**/.clang-tidy": true,
        "**/.clang-format": true,
        "**/.gitattributes": true,
        "**/.style.yapf": true,
        "**/CODE_OF_CONDUCT.md": true,
        "**/CONTRIBUTING.md": true,
        "**/LICENSE": true,
        "**/examples": true,
        "**/.jiri_root": true,
        "**/prebuilt": true,
    },
```
 

 

 
## Language specifics  语言细节Each language may require extra configuration. See more for  每种语言可能需要额外的配置。查看更多

 
* [Rust](/docs/development/languages/rust/editors.md#visual-studio-code)  * [Rust]（/ docs / development / languages / rust / editors.mdvisual-studio-code）
* [Dart](/docs/development/languages/dart/ides.md#visual-studio-code)  * [Dart]（/ docs / development / languages / dart / ide.visual-studio-code）
* [C/C++](/docs/development/languages/c-cpp/editors.md#visual-studio-code)  * [C / C ++]（/ docs / development / languages / c-cpp / editors.mdvisual-studio-code）
