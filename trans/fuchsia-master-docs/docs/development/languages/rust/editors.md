 
# Rust Editor Configuration  Rust编辑器配置 

[TOC]  [目录]

 
## Generating Cargo.toml files for use by editors {#generating-cargo-toml}  生成供编辑使用的Cargo.toml文件{generating-cargo-toml} 

Many editors require Cargo.toml files in order to understand how your Rust project is structured. These files can be generated using the followingcommands, where `//garnet/foo/path/to/target:label` is the GN target thatyou want to work on: 为了了解Rust项目的结构，许多编辑器都需要Cargo.toml文件。可以使用以下命令生成这些文件，其中`// garnet / foo / path / to / target：label`是要处理的GN目标：

```sh
you@computer:/path/to/fuchsia $ fx build garnet/foo/path/to/target:some_label
you@computer:/path/to/fuchsia $ fx gen-cargo garnet/foo/path/to/target:some_label
```
 

Note that this label must point to a `rustc_...` GN template, not a Fuchsia package or other GN target. For example: 请注意，此标签必须指向`rustc _...`GN模板，而不是Fuchsia软件包或其他GN目标。例如：

```
rustc_binary("some_label") {
   ...
}
```
 
## Intellij  智能 

See instructions on [the Intellij Rust site](https://intellij-rust.github.io/). Finally, follow the steps above to generate a Cargo.toml file for use by Intellij. 请参阅[Intellij Rust网站]（https://intellij-rust.github.io/）上的说明。最后，按照上述步骤生成Intellij使用的Cargo.toml文件。

 
## VIM  VIM 

See instructions on [`rust-lang/rust.vim`](https://github.com/rust-lang/rust.vim).  请参阅[`rust-lang / rust.vim`]（https://github.com/rust-lang/rust.vim）上的说明。

If you use Tagbar, see [this post](https://users.rust-lang.org/t/taglist-like-vim-plugin-for-rust/21924/13) for instructions on making it work better with Rust. 如果您使用标签栏，请参见[this post]（https://users.rust-lang.org/t/taglist-like-vim-plugin-for-rust/21924/13），了解如何使其与Rust更好地配合使用。

 
## Visual Studio Code {#visual-studio-code}  Visual Studio代码{visual-studio-code} 

The VS Code plugin uses the RLS (Rust language server) so you'll need to first [install rustup](https://rustup.rs/). Next, install [this VSCode plugin].You need to configure `rustup` to use the Fuchsia Rust toolchain.Run this command from your Fuchsia source code root directory. VS Code插件使用RLS（Rust语言服务器），因此您需要首先[安装rustup]（https://rustup.rs/）。接下来，安装[此VSCode插件]。您需要配置`rustup`以使用Fuchsia Rust工具链。从Fuchsia源代码根目录运行此命令。

```sh
rustup toolchain link fuchsia $(scripts/youcompleteme/paths.py VSCODE_RUST_TOOLCHAIN)
rustup default fuchsia
```
 

Follow [the steps above](#generating-cargo-toml) to generate a `Cargo.toml` file for use by VSCode. 按照[上述步骤]（generating-cargo-toml）生成`Cargo.toml`文件供VSCode使用。

Open VS Code and ensure that the directory where the generated `Cargo.toml` file resides is added as a directory in your workspace (even though you probably haveits ancestor `fuchsia` directory already in your workspace). For example: 打开VS Code，并确保将生成的Cargo.toml文件所在的目录作为目录添加到您的工作空间中（即使您的工作空间中可能已经有其祖先的fuchsia目录）。例如：

```sh
you@computer:/path/to/fuchsia $ fx build src/rusty/component:bin
you@computer:/path/to/fuchsia $ fx gen-cargo src/rusty/component:bin
```
 

In a new VS Code workspace, in this example, add both `/path/to/fuchsia` and `/path/to/fuchsia/src/rusty/component` to the workspace. Saving theworkspace would yield something like: 在此示例中，在新的VS Code工作空间中，将/ path / to / fuchsia和/ path / to / fuchsia / src / rusty / component添加到工作空间。节省工作空间将产生如下结果：

```javascript
{
  "folders": [
    {
      "path": "/path/to/fuchsia"
    },
    {
      "path": "/path/to/fuchsia/src/rusty/component"
    }
  ]
}
```
`fuchsia_rusty_component.code-workspace`  `fuchsia_rusty_component.code-workspace`

Next, take note of the paths output by the following:  接下来，记下以下内容输出的路径：

```sh
you@computer:/path/to/fuchsia $ ./scripts/youcompleteme/paths.py FUCHSIA_ROOT
you@computer:/path/to/fuchsia $ ./scripts/youcompleteme/paths.py VSCODE_RUST_TOOLCHAIN
```
 

Open VS Code settings  打开VS Code设置

 
  * MacOS X: Code>Preferences>Settings  * MacOS X：“代码”>“首选项”>“设置”
  * Linux: File>Preferences>Settings  * Linux：文件>首选项>设置

Note there are different settings defined for each environment (for example, user vs remote development server). In the upper right corner, click an icon whose mouse-over balloon tip says "Open Settings (JSON)".Add the following settings: 请注意，为每种环境定义了不同的设置（例如，用户与远程开发服务器）。单击右上角的图标，该图标的鼠标悬停提示框上显示“打开设置（JSON）”。添加以下设置：

```javascript
{
  // General rust and RLS configuration.
  "rust.target": "x86_64-fuchsia",
  "rust.target_dir": "<FUCHSIA_ROOT>/out/cargo_target",
  "rust.unstable_features": true,
  "rust-client.rlsPath": "<VS_CODE_TOOLCHAIN>/bin/rls",
  "rust-client.disableRustup": true,
  "rust.mode": "rls",

  // Read `Cargo.toml` from innermost root workspace directory.
  "rust-client.nestedMultiRootConfigInOutermost": false,

  // Optional extras:

  // Log RLS info/warning/error messages to a VSCode Output Panel.
  "rust-client.revealOutputChannelOn": "info",

  // Create `rls[numeric-id].log` in your project directory. Errors from RLS
  // will be logged there.
  "rust-client.logToFile": true,
}
```
 

[this VSCode plugin]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust  [此VSCode插件]：https://marketplace.visualstudio.com/items?itemName=rust-lang.rust

 
## emacs  emacs 

 
### Synopsis  概要 

You will be using [flycheck](https://www.flycheck.org/en/latest/) to compile your Rust files when you save them.  flycheck will parse those outputs andhighlight errors.  You'll also use[flycheck-rust](https://github.com/flycheck/flycheck-rust) so that it willcompile with cargo and not with rustc.  Both are available from[melpa](https://melpa.org/#/). 保存文件时，您将使用[flycheck]（https://www.flycheck.org/en/latest/）编译Rust文件。 flycheck将解析这些输出并突出显示错误。您还将使用[flycheck-rust]（https://github.com/flycheck/flycheck-rust），以便将其与货物一起编译，而不与rustc一起编译。两者都可以从[melpa]（https://melpa.org//）获得。

 
### Instructions  使用说明 

If you don't yet have melpa, follow the instructions [here](https://melpa.org/#/getting-started). 如果您还没有Melpa，请按照[此处]（https://melpa.org//getting-started）中的说明进行操作。

Install `flycheck` and `flycheck-rust` in `M-x list-packages`.  Type `i` to queue for installation what you are missing and then `x` to execute. 在M-x list-packages中安装`flycheck`和`flycheck-rust`。输入“ i”以排队安装缺少的内容，然后输入“ x”执行。

Next, make sure that flycheck-rust is run at startup.  Put this in your `.emacs` files:  接下来，确保flycheck-rust在启动时运行。将其放入您的.emacs文件中：

```elisp
(with-eval-after-load 'rust-mode
  (add-hook 'flycheck-mode-hook #'flycheck-rust-setup))
```
 

You'll want cargo to run "check" and not "test" so set `flycheck-rust-check-tests` to `nil`.  You can do this by typing `C-h vflycheck-rust-check-tests<RET>` and then customizing the variable in the normalway. 您希望货物运行“检查”而不是“测试”，因此将“ flycheck-rust-check-tests”设置为“ nil”。您可以通过输入`C-h vflycheck-rust-check-tests <RET>`来执行此操作，然后按照常规方式自定义变量。

Now, you'll want to make sure that the default `cargo` and `rustc` that you are using are Fuchsia versions of those.  From your fuchsia root, type: 现在，您将要确保使用的默认`cargo`和`rustc`是它们的紫红色版本。从紫红色的根中键入：

```elisp
rustup toolchain link fuchsia $PWD/prebuilt/third_party/rust/linux-x64 && rustup default fuchsia
```
 

Finally, follow the steps at the top of this page to generate a Cargo.toml for the GN target that you want to work on. 最后，按照此页面顶部的步骤为您要处理的GN目标生成Cargo.toml。

You can [read about](http://www.flycheck.org/en/latest/user/error-reports.html) adjusting flycheck to display your errors as you like.  Type `C-h vflycheck-highlighting-mode<RET>` and customize it.  Also customize `C-h vflycheck-indiation-mode<RET>`. 您可以[了解]（http://www.flycheck.org/en/latest/user/error-reports.html）调整flycheck以根据需要显示错误。输入`C-h vflycheck-highlighting-mode <RET>`并对其进行自定义。还自定义`C-h vflycheck-indiation-mode <RET>`。

Now restart emacs and try it out.  现在重新启动emacs并尝试一下。

 
### Test and debug  测试和调试 

To test that it works, you can run `M-x flycheck-compile` and see the command-line that flycheck is using to check syntax.  It ought to look like oneof these depending on whether you are in a lib or bin: 为了测试它是否有效，您可以运行M-x flycheck-compile并查看flycheck用于检查语法的命令行。根据您是在lib还是bin中，它应该看起来像其中之一：

```sh
cargo check --lib --message-format\=json
cargo check --bin recovery_netstack --message-format\=json
```
 

If it runs `rustc` instead of `cargo`, that's because you didn't `fx gen-cargo`.  如果它运行的是Rustc而不是cargo，那是因为您没有执行fx gen-cargo。

