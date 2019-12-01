Python style guide ============================== Python样式指南==============================

The Fuchsia project follows the [Google Python style guide]( https://github.com/google/styleguide/blob/gh-pages/pyguide.md), with a few[refinements](#Refinements). 紫红色项目遵循[Google Python样式指南]（https://github.com/google/styleguide/blob/gh-pages/pyguide.md），其中包含一些[改进]（Refinements）。

The Google Python style guide allows more variation (presumably to cover a large breadth of existing source). This guide has a tighter set of choices. So aFuchsia Python file will also comply with the Google style guide, but a GooglePython file might not comply with this guide. See [refinements](#Refinements)below for details. Google Python样式指南提供了更多的变化形式（大概涵盖了现有资源的广度）。本指南有更多选择。因此，紫红色的Python文件也将符合Google样式指南，但GooglePython文件可能不符合该指南。有关详细信息，请参见下面的[改进]（改进）。

 
## Python 2 vs 3  Python 2与3 

Lean towards a Python 3 style where the languages differ, but continue to support both versions. 倾向于使用Python 3样式，其中的语言有所不同，但继续支持两种版本。

Developers working on Fuchsia modules may use various platforms. Some platforms include Python 2.x and not Python 3.x and vice versa. Until Python 3.x isincluded in the prominent development environments we support, we should supportPython 2.x. 使用Fuchsia模块的开发人员可以使用各种平台。某些平台包含Python 2.x，但不包含Python 3.x，反之亦然。在我们支持的重要开发环境中包括Python 3.x之前，我们应该支持Python2.x。

While Python 2.x is supported, test scripts on both versions. Python 2.7 will be supported by the Python team until January 1, 2020. When we drop Python 2.7support will be influenced by, but not dictated by that support pledge from thePython team. 虽然支持Python 2.x，但在两个版本上都测试脚本。 Python团队将在2020年1月1日之前为Python 2.7提供支持。当我们删除Python 2.7的支持时，Python团队的支持承诺将对其影响但不受其决定。

 
## Multiple Inheritance  多重继承 

Multiple inheritance is strongly discouraged. This is for the same reason listed in the Google C++ style guide: risk of "diamond" inheritance patterns,which are prone to confusion. If a case is found where avoiding multipleinheritance is unreasonable, all classes involved must initially inherit fromthe base class `object`, which governs which multiple inheritance scheme isused. 强烈禁止多重继承。这与Google C ++样式指南中列出的原因相同：容易产生“钻石”继承模式的风险。如果发现避免避免多重继承是不合理的，则所有涉及的类必须首先从基类“对象”继承，该基类控制使用哪种多重继承方案。

 
## Use Unicode for Text  对文本使用Unicode 

While Python 2.x is supported, explicitly declare text strings as unicode and binary data as bytes, using `u""`, `unicode()`, `unichr()` and  `b""`,`bytes()`, `byte()` respectively.Python 3.x defaults to using Unicode for strings, so this guideline will beremoved when support for Python 2 is dropped. 支持Python 2.x时，使用`u'“`，ʻunicode（）、、 unichr（）和`b”“`，`bytes（）将文本字符串显式声明为unicode，将二进制数据声明为字节。 Python 3.x默认将Unicode用于字符串，因此，在删除对Python 2的支持后，将删除该准则。

```python {.good}
Yes:

  a = u"Hello"  # Unicode constant.
  b = unicode(foo)  # Convert to Unicode.
  c = unichr(c)  # Convert to Unicode.
  d = io.open("bar.txt").read()  # Read text as Unicode.
```
 

```python {.bad}
No:

  a = "Hello"  # Ambiguous (depends on Python version).
  b = str(foo)  # Convert to ascii.
  c = chr(c)  # Convert to ascii.
  d = open("bar.txt").read()  # Read text as ascii.
```
 

 
# Refinements  细化 

The following refinements we make to the Google Python style guide are largely choices between variations. For example, if the style guide says you may do A,B, or C we may choose to favor B and avoid the other choices. 我们对Google Python样式指南所做的以下改进主要是在变体之间进行选择。例如，如果样式指南说您可以做A，B或C，我们可以选择偏爱B并避免其他选择。

 
## [Indentation](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#34-indentation)  [缩进]（https://github.com/google/styleguide/blob/gh-pages/pyguide.md34-indentation） 

Avoid aligning with opening delimiter. Prefer instead to indent using fixed (4 space) indentation. 避免与定界符对齐。最好使用固定的（4个空格）缩进来缩进。

 
## [Statements](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#314-statements)  [声明]（https://github.com/google/styleguide/blob/gh-pages/pyguide.md314-statements） 

Avoid creating single line statements, even with `if` statements.  避免创建单行语句，即使使用`if`语句也是如此。

 
## [Type Annotations](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#319-type-annotations)  [类型注释]（https://github.com/google/styleguide/blob/gh-pages/pyguide.md319-type-annotations） 

While Python 2.x is supported, type annotations will not be used.  虽然支持Python 2.x，但不会使用类型注释。

 
## [Strings](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#310-strings)  [字符串]（https://github.com/google/styleguide/blob/gh-pages/pyguide.md310-strings） 

Prefer double quotes for strings ("). Use single quotes when the declaration is more readable with single quotes. E.g. 'The cat said "Meow"' is more readablethan "The cat said \\"Meow\\"". 对于字符串（“），建议使用双引号。当声明使用单引号更易读时，请使用单引号。例如，“猫说“喵”的猫”比“猫说\\”喵的猫”更易读。

 
## [Be consistent](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#4-parting-words)  [保持一致]（https://github.com/google/styleguide/blob/gh-pages/pyguide.md4-parting-words） 

Be consistent within a large scope. Avoid making small pockets of consistency within Fuchsia. Being consistent within one file or directory is not muchconsistency. 在大范围内保持一致。避免在紫红色的内部留出少量的一致性。在一个文件或目录中保持一致不是很多一致性。

