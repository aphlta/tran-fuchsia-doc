 
# Owners  拥有者 

Each repository in the system has a set of owners. These are tracked in files all aptly named `OWNERS`. One of these willalways be present in the root of a repository. Many directories willhave their own `OWNERS` files. 系统中的每个存储库都有一组所有者。这些文件都被恰当地命名为“ OWNERS”。其中之一总是存在于存储库的根目录中。许多目录将有自己的`OWNERS`文件。

 
## Contents  内容 

Each file lists a number of individuals (via their email address) who are familiar with and can provide code review for the contents of thatdirectory. We strive to always have at least two individuals in agiven file. Anything with just one is either too fine grained todeserve its own, or is in need of someone else to learn enough aboutthe code to feel comfortable approving changes to it or answeringquestions about it. 每个文件列出了一些熟悉的人（通过他们的电子邮件地址），可以为该目录的内容提供代码审查。我们力争始终将至少两个人保留在给定的档案中。仅有一个代码的任何东西要么太细粒度而不值得拥有它，要么需要其他人学习足够的代码知识，以便于批准更改或回答有关它的问题。

 
## Responsibilities  职责范围 

Fuchsia requires changes to have an OWNERS +2 review. However, many OWNERS files contain a `*` allowing anyone to provide such a +2. 紫红色需要更改才能获得OWNERS +2审查。但是，许多OWNERS文件都包含一个“ *”，任何人都可以提供+2。

 
## Tools  工具类 

INTK-108 tracks the work to stand up more infra tooling around these, such as suggesting reviewers automatically in Gerrit. INTK-108跟踪工作以围绕这些工作建立更多的基础工具，例如在Gerrit中自动建议审阅者。

 
## Format  格式 

We use the [Gerrit find-owners plugin][find-owners] file format for our OWNERS files. 对于我们的OWNERS文件，我们使用[Gerrit查找所有者插件] [find-owners]文件格式。

