 
# Documentation Standards  文件标准 

A document about what to document and how to document it for people who create things that need documentation. 有关创建哪些内容需要文档的人员的文档以及如何对其进行文档化的文档。

 
## Why document?  为什么要文件？ 

Fuchsia is a new operating system. Effective documentation allows new people to join and grow the project by having all necessary documentation be clear and concise. 紫红色是一个新的操作系统。有效的文档可以使新人们通过清晰简明的所有必要文档来加入并发展项目。

 
## Who is the audience?  谁是观众？ 

The documentation described here is intended to address a technical audience, i.e. those who expect to implement or exercise APIs or understand the internal dynamics of the operating system. Thesestandards are not intended for end-user product documentation. 这里描述的文档旨在面向技术受众，即那些希望实现或使用API​​或了解操作系统内部动态的人员。这些标准不适用于最终用户产品文档。

 
## What should I document?  我应该记录什么？ 

Document protocols, introduce essential concepts, explain how everything fits together.  记录协议，介绍基本概念，解释所有内容如何组合在一起。

 
- Conventions: e.g. this document about documentation, code style  -惯例：例如本文档关于文档，代码风格
- System Design: e.g. network stack, compositor, kernel, assumptions  -系统设计：例如网络堆栈，合成器，内核，假设
- APIs: e.g. FIDL protocols, library functions, syscalls  -API：例如FIDL协议，库函数，系统调用
- Protocols: e.g. schemas, encodings, wire formats, configuration files  -协议：例如模式，编码，连线格式，配置文件
- Tools: e.g. `bootserver`, `netcp`, `fx`  -工具：例如引导服务器，netcp，fx
- Workflows: e.g. environment set up, test methodologies, where to find various parts, how to get work done -工作流程：例如环境设置，测试方法，在哪里可以找到各个部分，如何完成工作

 
## Where should I put documents?  What goes where?  我应该把文件放在哪里？哪里去了？ 

Documentation that is only for developers working on creating or maintaining a specific part of the code should be kept in the same directory as the source code. 仅适用于致力于创建或维护代码特定部分的开发人员的文档应与源代码保存在同一目录中。

Documentation that should be generally available to developers must be available in one of two locations: 开发人员通常应使用的文档必须在以下两个位置之一可用：

 
* Zircon specific documentation should be created in `/docs/zircon`.  *特定于Zircon的文档应在`/ docs / zircon`中创建。
* Fuchsia documentation that is not specific to Zircon specific should be created in `/docs`.  In the `/docs/` directory, you should create yourdocumentation or images in one of these sub-directories: *不特定于Zircon的紫红色文档应在`/ docs`中创建。在`/ docs /`目录中，您应该在以下子目录之一中创建文档或图像：
    * `best-practices` General best practice guidelines on how to develop with Fuchsia source.If you create best practice documentation about about using a specificfeature of Fuchsia, you should create the documentation in the samedirectory as the other documentation for that specific feature. *`best-practices`有关如何使用Fuchsia源进行开发的通用最佳实践指南。如果创建有关使用Fuchsia特定特征的最佳实践文档，则应在与该特定功能的其他文档相同的目录中创建该文档。
    *  `development` Instructions, tutorials, and procedural documentation for developersthat are working on Fuchsia. This directory includes documentationon how to get started, build, run, and test Fuchsia and softwarerunning on devices operating Fuchsia. You should organize the contentthat you create by specific activities, such as testing, gettingstarted, or by workflow topic. *开发指南，教程和程序文档，适用于使用紫红色的开发人员。该目录包含有关如何开始，构建，运行和测试Fuchsia的文档，以及在运行Fuchsia的设备上运行的软件的文档。您应该通过特定的活动（例如测试，入门或工作流程主题）来组织创建的内容。
    * `the-book` Concept and developer guides about the features of Fuchsia. Youshould organize the content that you create by specific features. *“书本”概念和开发人员指南，关于紫红色的功能。您应按特定功能组织您创建的内容。
    * `images` Images that are used in the documentation. You should place images inthis common directory and avoid placing images in the same directoryas documentation. *`images`文档中使用的图像。您应该将映像放置在该公共目录中，并避免将映像放置在与文档相同的目录中。

 
## What documentation should I create?  我应该创建什么文档？ 

Most documentation can be divided into four categories:  大多数文档可以分为四类：

 
- [Reference](documentation_types.md#reference-documentation) - Information-oriented documentation  -[参考]（documentation_types.mdreference-documentation）-面向信息的文档
- [Conceptual](documentation_types.md#conceptual-documentation) - Understanding-oriented documentation -[概念]（documentation_types.mdconceptual-documentation）-面向理解的文档
- [Procedural](documentation_types.md#procedural-documentation)  -[程序]（documentation_types.mdprocedural-documentation）
    - How to - Goal-oriented documentation  -操作方法-面向目标的文档
    - Codelab - Learning-oriented documentation  -Codelab-学习型文档

See [Documentation Types](documentation_types.md) for more information.  有关更多信息，请参见[文档类型]（documentation_types.md）。

However, comments in your code are very important for maintainability and helping other people understand your code. See the [Code Comment Guidelines](documentation_comments.md) for style guidelinesrelated to comments for your code. 但是，代码中的注释对于可维护性和帮助其他人理解您的代码非常重要。请参阅[代码注释准则]（documentation_comments.md），以获取与代码注释相关的样式准则。

 
## What documentation style guidelines should I follow?  我应该遵循哪些文档样式指南？ 

It is important to try to follow documentation style guidelines to ensure that the documentation created by a large number of contributors can flow together. See[Documentation Style Guide](documentation_style_guide.md). 务必遵循文档样式指南，以确保由大量贡献者创建的文档可以一起流通。请参见[文档样式指南]（documentation_style_guide.md）。

 
## How can I link to source code in my documentation?  如何链接到文档中的源代码？ 

Use absolute paths starting with '/', like [`/zircon/public/sysroot/BUILD.gn`](/zircon/public/sysroot/BUILD.gn). Never use relative paths with ".." that point to content outside of `/docs`. 使用以'/'开头的绝对路径，例如[`/zircon/public/sysroot/BUILD.gn`](/zircon/public/sysroot/BUILD.gn）。切勿使用带有..的相对路径来指向`/ docs`之外的内容。

 
## How can I expose my documentation?  如何公开我的文档？ 

Documentation is only useful when users can find it. Adding links to or from existing documentation greatly improves the chances that someone can find your documentation. 文档仅在用户可以找到时才有用。添加到现有文档的链接或从现有文档添加链接可以极大地提高某人找到您的文档的机会。

Tips for leaving breadcrumbs:  留下面包屑的提示：

 
- Table of contents: Add links to documentation in the left sided navigation on fuchsia.dev. See[Change table of contents navigation](documentation_navigation_toc.md). -目录：在fuchsia.dev的左侧导航中添加指向文档的链接。请参阅[更改目录导航]（documentation_navigation_toc.md）。
- Top-down linkage: Add links from more general documents to more specific documents to help readers learn more about specific topics. The [Fuchsia book](/docs/concepts/README.md) is a goodstarting point for top-down linkage. -自上而下的链接：添加从更一般的文档到更具体的文档的链接，以帮助读者更多地了解特定主题。 [紫红色的书]（/ docs / concepts / README.md）是自上而下链接的良好起点。
- Bottom-up linkage: Add links from more specific documents to more general documents to help readers understand the full context context of the topics being discussed. Adding links frommodule, class, or protocol documentation comments to conceptual documentation overviews can beparticularly effective. -自下而上的链接：添加从更具体的文档到更一般的文档的链接，以帮助读者理解所讨论主题的完整上下文。从模块，类或协议文档注释添加链接到概念性文档概述可能特别有效。
- Sideways linkage: Add links to documents on subjects that help readers better understand the content of your document. -横向链接：添加有关主题的文档链接，以帮助读者更好地理解文档的内容。

