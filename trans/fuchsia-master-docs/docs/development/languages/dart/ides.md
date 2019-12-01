 
# IDEs  集成开发环境 

 
### Dart SDK  Dart SDK 

A prebuilt Dart SDK is available for IDE consumption at: `third_party/dart/tools/sdks/dart-sdk/`. 预构建的Dart SDK可在以下位置使用以供IDE使用：“ third_party / dart / tools / sdks / dart-sdk /”。

 
## Visual Studio Code {#visual-studio-code}  Visual Studio代码{visual-studio-code} 

 
1.  Download and install [Visual Studio Code](https://code.visualstudio.com/)  1.下载并安装[Visual Studio代码]（https://code.visualstudio.com/）
1.  [optional] Setup VS Code to launch from the command line  1. [可选]设置VS Code以从命令行启动

 
    *   For Macs: To allow running VS Code from the terminal using the `code` command, follow the instructions[here](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line) *对于Mac：要允许使用`code`命令从终端运行VS Code，请按照说明[此处]（https://code.visualstudio.com/docs/setup/mac_launching-from-the-command-line）

 
    *   For Linux and Windows: This should already be done as part of the installation *对于Linux和Windows：这应该已经在安装过程中完成

 
1.  Install the following extensions:  1.安装以下扩展：

 
    *   [Dart Code](https://marketplace.visualstudio.com/items?itemName=Dart-Code.dart-code): Support for programming in Dart. It should automatically find the dart-sdk in the Fuchsia tree. * [Dart代码]（https://marketplace.visualstudio.com/items?itemName=Dart-Code.dart-code）：支持Dart编程。它应该在紫红色的树中自动找到dart-sdk。
    *   [FIDL language support](https://marketplace.visualstudio.com/items?itemName=fuchsia-authors.language-fidl): Syntax highlighting support for Fuchsia's FIDL files * [FIDL语言支持]（https://marketplace.visualstudio.com/items?itemName=fuchsia-authors.language-fidl）：语法突出显示了对Fuchsia FIDL文件的支持
    *   [GN](https://marketplace.visualstudio.com/items?itemName=npclaudiu.vscode-gn): Syntax highlighting for GN build files * [GN]（https://marketplace.visualstudio.com/items?itemName=npclaudiu.vscode-gn）：GN构建文件的语法突出显示
    *   Optional but helpful git extensions:  *可选但有用的git扩展：
        *   [Git Blame](https://marketplace.visualstudio.com/items?itemName=waderyan.gitblame): See git blam information in the status bar * [Git Blame]（https://marketplace.visualstudio.com/items?itemName=waderyan.gitblame）：在状态栏中查看git blam信息
        *   [Git History](https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory): View git log, file history, etc. * [Git历史记录]（https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory）：查看git日志，文件历史记录等。

 
1.  Here are some helpful user settings for Dart. Open your user settings (Ctrl+,), click the '{}' icon in the top left corner and add: 1.以下是Dart的一些有用的用户设置。打开用户设置（Ctrl，），单击左上角的“ {}”图标并添加：

```json
{
  // Auto-formats your files when you save
  "editor.formatOnSave": true,

  // Don't run pub with fuchsia.
  "dart.runPubGetOnPubspecChanges": false,

  // Settings only when working in Dart
  "[dart]": {
    // Adds a ruler at 80 characters
    "editor.rulers": [
      80
    ],

    // Makes the tab size 2 spaces
    "editor.tabSize": 2,
  },
}

```
 

 
## CLion/IntelliJ  CLion / IntelliJ 

 
* Add the Dart plugin by going to `Settings > Plugins` then searching for Dart language support. *通过进入“设置>插件”，然后搜索Dart语言支持来添加Dart插件。
* Set the Dart path in `Settings > Languages & Frameworks > Dart` by  *在“设置>语言框架> Dart”中设置Dart路径，方法是
  * Check __Enable Dart support for the project <project name>.__  *选中__为项目<项目名称>启用Dart支持。__
  * Enter the Dart SDK path "${FUCHSIA_SRC}/third_party/dart/tools/sdks/dart-sdk"  *输入Dart SDK路径“ $ {FUCHSIA_SRC} / third_party / dart / tools / sdks / dart-sdk”

 

 
## Troubleshooting  故障排除 

If you find that the IDE is unable to find imports (red squigglies) that are already correctly in your BUILD.gn dependencies, this is usually a sign thatDart analysis is not working properly in your IDE. 如果发现IDE无法在BUILD.gn依赖项中找到已经正确导入的导入（红色弯曲），则通常表明Dart分析在IDE中无法正常工作。

When this happens, try the following:  发生这种情况时，请尝试以下操作：

 
### Open only the project directory you are working on  仅打开您正在处理的项目目录 

E.g. only open `/topaz/shell/ermine` instead of `/topaz`. The analyzer can have issues with really large source trees. 例如。仅打开`/ topaz / shell / ermine`而不是`/ topaz`。分析器可能会遇到很大的源代码树的问题。

 
### Remove pub output  删除发布输出 

 
1.  Delete the `.packages` and `pubspec.lock` files in your project (if present). 1.删​​除项目中的.packages和pubspec.lock文件（如果存在）。
1.  Ensure that `"dart.runPubGetOnPubspecChanges": false,` is present in your VSCode preferences to prevent the files from reappearing whenever a`pubspec.yaml` file is edited. 1.确保VSCode首选项中存在“ dart.runPubGetOnPubspecChanges”：false，以防止在编辑pubspec.yaml文件时文件再次出现。
1.  Reload VSCode to restart the Dart analyzer.  1.重新加载VSCode以重新启动Dart分析器。
    1.  Press Ctrl+Shift+P to open the VSCode Command Palette  1.按Ctrl + Shift + P打开VSCode命令面板
    1.  Select "Reload Window"  1.选择“重新加载窗口”

 
### Rebuild  重建 

Delete `/out` from your Fuchsia directory and rebuild. Dart FIDL bindings are build-generated and may be absent. 从您的紫红色目录中删除`/ out`并重建。 Dart FIDL绑定是生成生成的，可能不存在。

 
### Ensure you have a complete build  确保您具有完整的构建 

Any Dart code from packages not included in your build will not be available to the analyzer, so ensure your build configuration (`fx set`) includes allthe packages you need (the `--with` flag can be helpful.) 分析器将无法使用构建中未包含的任何Dart代码进行分析，因此请确保您的构建配置（“ fx set”）包含了所需的所有软件包（“ --with”标志可能会有所帮助）。

 
### Reload the Dart Analyzer  重新加载Dart分析仪 

Manually reloading the analyzer is often needed after modifying FIDLs.  修改FIDL后，通常需要手动重新加载分析仪。

 
#### VS Code  VS代码 

 
1.  Open the Command Palette (Ctrl+Shift+P)  1.打开命令面板（Ctrl + Shift + P）
1.  Enter and select "Reload Window"  1.输入并选择“重新加载窗口”

This also restarts the Dart analyzer.  这还会重新启动Dart分析仪。

 
#### IntelliJ  IntelliJ 

 
1.  Open Find Action (Ctrl+Shift+A)  1.打开查找动作（Ctrl + Shift + A）
1.  Enter and select "Restart Dart Analysis Server"  1.输入并选择“重新启动Dart Analysis Server”

 
### Check that the correct language has been detected for the current file type  检查是否已为当前文件类型检测到正确的语言 
1.  On VS Code use Ctrl+Shift+P then type "Change Language Mode" and ensure it is set to "Auto Detect".  1.在VS Code上，使用Ctrl + Shift + P，然后键入“更改语言模式”，并确保将其设置为“自动检测”。
1.  If this doesn't fix the issue you can try to manually fix via Ctrl+Shift+P and "Configure file association for .dart"  1.如果这不能解决问题，您可以尝试通过Ctrl + Shift + P和“为.dart配置文件关联”手动修复

 
### Manually specifying the Dart sdk path  手动指定Dart SDK路径 

 
#### VS Code  VS代码Add the line  添加行

```json
  "dart.sdkPath": "[YOUR FUCHSIA DIR LOCATION]/third_party/dart/tools/sdks/dart-sdk",
```
 

and (Ctrl+Shift+P) "Reload Window".  和（Ctrl + Shift + P）“重新加载窗口”。

 
#### IntelliJ  IntelliJ 

 
1.  Open Settings  1.打开设置
