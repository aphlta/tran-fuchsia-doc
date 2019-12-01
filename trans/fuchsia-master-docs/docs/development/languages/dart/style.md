Dart style guide ================ 飞镖样式指南================

The Fuchsia project follows the guidelines in [Effective Dart][effective-dart], but with some additions. 紫红色项目遵循[有效飞镖] [有效飞镖]中的指南，但有一些补充。

All code must be formatted using `dartfmt` before being checked in.  所有代码必须在签入之前使用`dartfmt`进行格式化。

 
# Additional Style Rules  其他样式规则 

 
### DON'T follow the Flutter repository style guide.  不要遵循Flutter存储库样式指南。 

The Flutter project's style guide is meant to be used for code in the Flutter framework itself. It is not intended as style guidance for projects usingFlutter. All code in the Fuchsia repository should follow the standardDart style. Although we are not following the style, the Flutter's guide ondocumentation and development is still useful. Flutter项目的样式指南旨在用于Flutter框架本身中的代码。它不打算用作使用Flutter的项目的样式指南。紫红色存储库中的所有代码均应遵循standardDart样式。尽管我们没有遵循这种样式，但是Flutter的文档编制和开发指南仍然很有用。

 
### DO use trailing commas on all tree structures longer than one line.  请勿在长度超过一行的所有树结构上使用结尾逗号。 

Without trailing commas, code that builds widget trees or similar types of code tends to be hard to read. Adding the trailing commas allows `dartfmt`to do its job correctly. 如果没有尾随逗号，那么构建小部件树或类似类型代码的代码往往很难阅读。添加结尾逗号可以使dartfmt正确执行其工作。

 
#### Without trailing commas:  没有尾随逗号： 

``` dart
children.add(Expanded(
  child: Center(
      child: Container(
          width: 64.0, height: 64.0, child: FuchsiaSpinner())),
));
```
 

 
#### With trailing commas:  尾随逗号： 

``` dart
children.add(Expanded(
  child: Center(
      child: Container(
        width: 64.0,
        height: 64.0,
        child: FuchsiaSpinner(),
      ),
   ),
));
```
 

 
### DO order members using the Dart Analyzer.  使用Dart分析仪订购成员。In Visual Studio Code, this is the Dart: Organize Members command available in the Command Palette. (Control+Shift+P or View -> Command Palette) 在Visual Studio代码中，这是“命令面板”中可用的“飞镖：整理成员”命令。 （Control + Shift + P或View-> Command Palette）

This formatter doesn’t appear to be available outside of the supported IDEs.  在支持的IDE之外，该格式化程序似乎不可用。

 
### PREFER to keep lines below 80 characters unless it would be more readable.  除非可读性更好，否则请保持行数不超过80个字符。This is a slight amendment from the general Dart [rule][dartstyle-80-chars]. Unlike that rule, it is fine to have lines above 80 characters in the Fuchsiarepository, as long as it improves readability, and dartfmt won't automaticallytruncate the line. 这是对通用Dart [rule] [dartstyle-80-chars]的略微修改。与该规则不同，在Fuchsia存储库中行数超过80个字符是可以的，只要它能提高可读性，并且dartfmt不会自动截断该行。

 
# Additional Usage Rules  其他使用规则 

 
## Repositories and Files  储存库和文件 

 
### DO prefix library names in `/lib` and `/public/lib` with `lib.`  务必在`/ lib`和`/ public / lib`中用`lib'前缀库名。 
#### Example:  例： 

```
Dart_library("lib.settings") {
  package_name = "lib.settings"
  ...
}
```
 

 
### PREFER minimizing the number of public members exposed in a package.  尽量减少包装中的公共成员数量。This can be done by only making things public when needed, and keeping all implementation detail libraries in the `/src` directory. Assume anythingpublic in the `lib` directory will be re-used. 这可以通过仅在需要时将其公开，并将所有实现细节库保留在/ src目录中来完成。假设lib目录中的任何公共内容都将被重用。

 
### CONSIDER exporting publicly visible classes in a single `.dart` file.  考虑在单个.dart文件中导出公开可见的类。 

For multiple classes that are used together but are in different files, it’s more convenient for users of your library to import a single file rathermany at once. If the user wants narrower imports they can always restrictvisibility using the `show` keyword. 对于同时使用但文件不同的多个类，您的图书馆用户一次可以导入多个文件更为方便。如果用户想要缩小进口范围，则可以始终使用“ show”关键字来限制可见性。

This also helps minimize the publicly visible surface.  这也有助于最小化公众可见的表面。

Example:  例：

``` dart
/// In src/apple.dart
class Apple {}

/// In src/orange.dart
class Orange {}

/// In src/veggies.dart
class Potato {}
class Tomato {}

/// In botanical_fruits.dart
export 'src/apple.dart';
export 'src/orange.dart';
// Can also be: export 'src/veggies.dart' hide Potato;
export 'src/veggies.dart' show Tomato;

/// In squeezer.dart
import 'package:plants/botanical_fruits.dart' show Orange;

```
 

 
### DO import all files within a package using relative paths.  不要使用相对路径导入包中的所有文件。 

Mixing and matching relative and absolute paths within a single package causes Dart to act as if there were two separate imports of identical files,which will introduce errors in typechecking. Either format works as long asit is consistent. Within the Fuchsia repository, relative paths are used. 在单个程序包中混合并匹配相对路径和绝对路径会导致Dart好像有两个单独的导入相同文件的行为，这将在类型检查中引入错误。只要格式一致，任何一种格式都可以使用。在紫红色的存储库中，使用相对路径。

This does not apply to external libraries, as only the absolute path can be used. 这不适用于外部库，因为只能使用绝对路径。

 
#### Good:  好： 

``` dart
import 'access_point.dart';
```
 

 
#### Bad:  坏： 

``` dart
import 'package:wifi/access_point.dart';
```
 

 
### DO use namespacing when you import FIDL packages.  导入FIDL软件包时，请使用命名空间。 

This adds clarity and readability. FIDL namespaces (library statements) are not respected in Dart (e.g. `fuchsia.io.Node` becomes `Node`).Because of tight namespaces, people tend to use more generic names in FIDL(Error, File, Node, etc.), which result in more collisions/ambiguity in Dart. 这增加了清晰度和可读性。 Dart不尊重FIDL名称空间（库语句）（例如fuchsia.io.Node变为Node）。由于名称空间的紧凑性，人们倾向于在FIDL中使用更多通用名称（错误，文件，节点等）。 ，这会导致Dart发生更多冲突/歧义。

 
#### Good:  好： 

``` dart
import 'package:fidl_fuchsia_file/fidl.dart' as file_fidl;
...

file_fidl.File.get(...) ...
```
 

 
#### Bad:  坏： 

``` dart
import 'package:fidl_fuchsia_file/fidl.dart';
...

File.get(...) ...
```
 

 
### DO use namespacing when there is ambiguity, e.g. in class names.  如有歧义，请使用命名空间，例如在班级名称中。 

There are often functions or classes that can collide, e.g. `File` or `Image`. If you don't namespace, there will be a compile error. 通常会有一些功能或类可能会发生冲突，例如文件或图片。如果没有命名空间，则会出现编译错误。

 
#### Good:  好： 

``` dart
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
...

ui.Image(...) ...
```
 

 
#### Bad:  坏： 

``` dart
import 'dart:ui';

import 'package:flutter/material.dart';
...

Image(...) ... // Which Image is this?
```
 

 
### PREFER to use `show` if you only have a few imports from that package. Otherwise, use `as`.  如果您仅从该软件包中导入了少量内容，则最好使用“ show”。否则，使用`as`。 

Using `show` can avoid collisions without requiring you to prepend namespaces to types, leading to cleaner code. 使用`show`可以避免冲突，而无需您在名称空间之前添加类型，从而使代码更简洁。

 
#### Good:  好： 

``` dart
import 'package:fancy_style_guide/style.dart' as style;
import 'package:flutter/material.dart';
import 'package:math/simple_functions.dart' show Addition, Subtraction;
```
 

 
#### Bad:  坏： 

``` dart
import 'package:flutter/material.dart show Container, Row, Column, Padding,
  Expanded, ...;
```
 

 
## Coding practicies  编码惯例 

 
### DON'T use `new` or use `const` redundantly.  不要重复使用new或const。 

Dart 2 makes the `new` optional for constructors, with an aim at removing them in time. The `const` keyword is also optional where it can be inferred by thecompiler. Dart 2使“ new”对于构造函数是可选的，目的是及时删除它们。 const关键字在编译器可以推断的地方也是可选的。

`const` can be inferred in:  const可以推断为：

 
* A const collection literal.  * const集合常量。
* A const constructor call.  * const构造函数调用。
* A metadata annotation.  *元数据注释。
* The initializer for a const variable declaration.  * const变量声明的初始化程序。
* A switch case expression&mdash;the part right after case before the :, not the body of the case. *开关大小写表达式-在：之后紧接在case之后的部分，而不是case的主体。

This guidance will eventually be part of Effective Dart due to the changes for Dart 2. 由于Dart 2的更改，该指南最终将成为有效Dart的一部分。

 
#### Good:  好： 

``` dart
final foo = Foo();
const foo = Foo();
const foo = const <Widget>[A(), B()];
const Foo(): bar = Bar();
```
 

 
#### Bad:  坏： 

``` dart
final foo = new Foo();
const foo = const Foo();
foo = const [const A(), const B()];
const Foo(): bar = const Bar();
```
 

 
### DON'T do useful work in assert statements.  不要在assert语句中做有用的工作。 

Code inside assert statements are not executed in production code. Asserts should only check conditions and be side-effect free. assert语句中的代码不在生产代码中执行。断言应该只检查条件并且没有副作用。

 
### PREFER to use `const` over `final` over `var`.  最好在var之前使用const在final之上。 

This minimizes the mutability for each member or local variable.  这使每个成员或局部变量的可变性最小化。

 
### PREFER return `Widget` instead of a specific type of Flutter widget.  PREFER返回`Widget`，而不是特定类型的Flutter Widget。 

As your project evolves, you may change the widget type that is returned in your function. For example, you might wrap your widget with a Center. Returning`Widget` simplifies the refactoring, as the method signature wouldn't have tochange. 随着项目的发展，您可以更改函数中返回的窗口小部件类型。例如，您可以用中心包装小部件。返回Widget简化了重构，因为方法签名无需更改。

 
#### Good:  好： 

``` dart
Widget returnContainerWidget() {
  return Container();
}
```
 

 
#### Bad:  坏： 

``` dart
Container returnContainerWidget() {
  return Container();
}
```
 

 
# Additional Design Rules  其他设计规则 

 
### PREFER storing state in Models instead of state.  将状态存储在模型中而不是状态中。 

When storing state that Flutter widgets need to access, prefer to use `ScopedModel` and `ScopedModelDescendant` instead of `StatefulWidget`.A `StatefulWidget` should contain only internal widget state that can be lostwithout any consequences. 当存储Flutter窗口部件需要访问的状态时，请首选使用ScopedModel和ScopedModelDescendant而不是StatefulWidget.StatefulWidget应该仅包含内部窗口状态，该状态可以丢失而不会造成任何后果。

Examples of stuff to store in a `ScopedModel`:  存储在`ScopedModel`中的东西的例子：

 
* User selections  *用户选择
* App state  *应用状态
* Anything that needs to be shared by widgets  *小部件需要共享的任何内容

Examples of stuff to store in a `StatefulWidget`'s `State`:  存储在StatefulWidget的State中的东西的示例：

 
* Animation state that doesn't need to be controlled  *不需要控制的动画状态

 
### AVOID mixing named and positional parameters.  避免混合命名和位置参数。 

Instead, `@required` should be used in place of required positional parameters.  相反，应使用@required代替必需的位置参数。

 
### PREFER named parameters.  优选命名参数。 

In most situations, named parameters are less error prone and easier to read than positional parameters, optional or not. They give users to pass in theparameters in whatever order they please, and make Flutter trees especiallyclearer. 在大多数情况下，与位置参数（是否为可选参数）相比，命名参数不易出错且更易于阅读。它们使用户可以按自己希望的顺序传递参数，并使Flutter树更清晰。

In the Fuchsia repository, positional parameters should be reserved for simple operational functions with only a few parameters. 在紫红色的存储库中，位置参数应保留为仅具有少量参数的简单操作功能。

 
#### Good:  好： 

``` dart
int add(int a, int b);
int addNumbers(int a, [int b, int c, int d]);
Foo fromJson(String json);
void load(String file);

Widget buildButton({
  @required Widget child,
  VoidCallback onTap,
  double width,
  bool isDisabled = false,
});
```
 

 
#### Bad:  坏： 

``` dart
int add({int a, int b});
Foo fromJson({@required String json});

Widget buildButton(
  Widget child,
  VoidCallback onTap, [
  double width,
  bool isDisabled = false,
]);
```
 

 
### DO add [logging statements][dart-logging]  务必添加[记录语句] [dart-logging] 

