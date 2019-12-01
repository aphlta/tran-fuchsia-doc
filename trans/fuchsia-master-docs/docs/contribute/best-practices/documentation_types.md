 
# Documentation Types  文件类型 

Documentation is an important part of any product or feature because it lets users know how to properly use a feature that has been implemented. These guidelines are meant to be a quick and easyreference for types of documentation. For information on documentation style guidelines, see[Documentation Style Guide](documentation_style_guide.md). 文档是任何产品或功能的重要组成部分，因为它使用户知道如何正确使用已实现的功能。这些准则旨在快速方便地参考文档类型。有关文档样式指南的信息，请参见[文档样式指南]（documentation_style_guide.md）。

 
## Conceptual, procedural, or reference documentation  概念，程序或参考文档 

Most documentation can be divided into these categories:  大多数文档可以分为以下几类：

 
- [Reference](#reference-documentation) - Documentation that provides a source of information about parts of a system such as API parameters. -[参考]（参考文档）-提供有关系统部分信息的资源的文档，例如API参数。
- [Conceptual](#conceptual-documentation) - Documentation that helps you understand a concept such as mods in Fuchsia. -[Conceptual]（conceptual-documentation）-帮助您理解诸如紫红色中的mods之类的概念的文档。
- [Procedural](#procedural-documentation)  -[程序]（程序文档）
    - How-to - Documentation that provides steps on how to accomplish a goal such as create a user.  -操作方法-提供有关如何实现目标（例如创建用户）的步骤的文档。
    - Codelab - Documentation that provides steps of a learning path (this tends to be a much bigger procedure than a how-to) such as create a component. -Codelab-提供学习路径步骤的文档（这通常比how-to方法大得多），例如创建组件。

**You should write a reference document** if you need to provide information about parts of a system including, but not limited to APIs and CLIs. Reference documentation should allow the user tounderstand how to use a specific feature quickly and easily. **如果您需要提供有关系统各部分的信息，包括但不限于API和CLI，则应编写参考文档**。参考文档应使用户理解如何快速，轻松地使用特定功能。

**You should write a conceptual document** if you plan on explaining a concept about a product. Conceptual documents explain a specific concept, but for the most part they do not include actualexamples. They provide essential facts, background, and diagrams to help your readers build afoundational understanding of a product or topic. You should not explain industry standards thatyour audience should be familiar with, for example, TCP/IP. You might explain how this concept tiesin with your feature, but you should not explain the basics behind that industry standard concept. **如果打算说明有关产品的概念，则应编写概念文件**。概念性文件解释了一个特定的概念，但是在大多数情况下，它们不包括实际示例。它们提供必要的事实，背景和图表，以帮助您的读者建立对产品或主题的基础性理解。您不应解释您的听众应该熟悉的行业标准，例如TCP / IP。您可能会解释此概念如何与您的功能联系在一起，但您不应解释该行业标准概念背后的基础知识。

**You should write a procedural document** if you plan on explaining to a user how to use a specific feature and are able to guide a user through simple numbered steps. Procedural documents tend toreinforce the concepts that were explained in a conceptual document by giving one or moreexamples that might be useful for users. **如果您打算向用户解释如何使用特定功能，并能够通过简单的编号步骤来指导用户，则应编写程序文档**。过程文档往往会通过提供一个或多个对用户有用的示例来增强概念文档中解释的概念。

Procedural documents are divided into two categories:  程序文件分为两类：

 
- **How-to** - Consider writing a how to when you want to help the user accomplish a very specific goal. -**操作方法**-考虑何时要帮助用户实现非常具体的目标。
- **Codelab** - Consider writing a codelab when you want to help the user learn about a bigger goal that might involve working with multiple parts of a product or feature. The codelab should notgo over 60 minutes and should provide the user with a specific result. -**代码实验室**-当您想帮助用户了解可能涉及使用产品或功能的多个部分的更大目标时，请考虑编写代码实验室。该代码实验室不应超过60分钟，并且应为用户提供特定的结果。

How can you decide what type of document is appropriate for your use case? Consider these examples:  您如何确定适合您的用例的文档类型？考虑以下示例：

 
- What is a car? This is a conceptual document.  -什么是汽车？这是一个概念文件。
- How does an internal combustion engine work? This is a conceptual document that would be geared towards more advanced users. -内燃机如何工作？这是一个概念文件，将针对更高级的用户。
- How to use the alarm manager in Android. That is a procedural document. The main set of procedures can be a codelab since a hand-held example is ideal to understand the function of thealarm manager. -如何在Android中使用警报管理器。那是程序文件。程序的主要集合可以是一个代码实验室，因为手持示例非常适合理解报警管理器的功能。
- How to operate the radio. This is a procedural document. This can be a how to guide since the use of a radio tends to be quite intuitive and in most cases wouldn't require a hand-held example. -如何操作收音机。这是一个程序文件。这可能是一种指导方法，因为无线电的使用往往非常直观，并且在大多数情况下不需要手持示例。
- How does a transistor work? This is a conceptual document that would be geared towards a more advanced user. -晶体管如何工作？这是一个概念文件，将针对更高级的用户。
- Functions of the car radio. This is a reference document.  -汽车收音机的功能。这是参考文件。
- How a new technology improved the car radio. This is a conceptual document.  -新技术如何改善车载收音机。这是一个概念文件。

Note: A feature may require more than one type of document. You may decide that your feature requires just reference documentation or that you need reference, conceptual, and how todocumentation. 注意：功能可能需要不止一种类型的文档。您可能会决定您的功能仅需要参考文档，或者您需要参考，概念以及如何记录文档。

 
## Reference documentation {#reference-documentation}  参考文档{reference-documentation} 

Reference documentation should provide information about parts of a system including, but not limited to APIs and CLIs. The style of reference documentation should be the same for all referencedocumentation of that type. For example, API documentation should define all of the API's parameters,indicate if a parameter is required or optional, and show examples of the use of the API. Theseexamples should be very generic and simple. If you feel like you need a more elaborate example,consider creating a procedural document to reinforce your reference documentation. 参考文档应提供有关系统各部分的信息，包括但不限于API和CLI。对于该类型的所有参考文档，参考文档的样式应相同。例如，API文档应定义API的所有参数，指示参数是必需参数还是可选参数，并显示API使用示例。这些示例应该非常通用和简单。如果您需要一个更详细的示例，请考虑创建一个程序文档以增强您的参考文档。

For the style guide for API documentation, see [API style guide](/docs/development/api/documentation.md). 有关API文档的样式指南，请参见[API样式指南]（/ docs / development / api / documentation.md）。

 
## Conceptual documentation {#conceptual-documentation}  概念文档{conceptual-documentation} 

Conceptual documentation should try to be brief and for the most part should not go above 1 page. If you need to write more than one page to describe a concept, consider breaking that concept intosub-concepts by using headings. By keeping your document brief you achieve the following: 概念性文档应尽量简短，并且大部分不应超过一页。如果您需要写多个页面来描述一个概念，请考虑使用标题将该概念分解为多个子概念。通过使文档简短，可以实现以下目的：

 
- You do not overwhelm your reader with a wall of text.  -您不会因一堵墙而使读者不知所措。
- Avoid losing the reader while they read your document.  -避免在阅读者阅读文档时迷失读者。

The first paragraph should try to be a brief summary of your document, this should allow the user to quickly read through it, determine what the document covers, and if this is relevant to what theywant to learn. If your document has multiple headings, you should include a bulleted list with thehigh-level headings after this first paragraph. 第一段应该是您文档的简短摘要，这应该使用户可以快速通读它，确定文档涵盖的内容以及与您想学习的内容有关的内容。如果您的文档有多个标题，则应在此第一段之后包括一个带有高级标题的项目符号列表。

You should use graphics, images, or diagrams to reinforce certain concepts. The text that comes before and after the graphic should explain what the graphic shows. Images should be saved ina feature specific 'images/' directory or a common 'images/' directory. You should also savethe source file of your images in a 'images/src/' directory. 您应该使用图形，图像或图表来增强某些概念。图形前后的文字应解释图形显示的内容。图像应保存在功能特定的“ images /”目录或公共“ images /”目录中。您还应该将图像的源文件保存在“ images / src /”目录中。

Good conceptual documentation usually includes:  好的概念文档通常包括：

 
- **Description** rather than instruction  -**说明**，而不是说明
- **Background** concepts  -**背景**概念
- **Diagrams** or other visual aids (preferably in .png format)  -图表或其他视觉辅助工具（最好是.png格式）
- **Links** to how-to and/or reference docs  -**链接**操作方法和/或参考文档

After writing your document, it is good practice to proofread the document, put yourself in the user's shoes (no longer being the expert that developed the feature), and try to answer thesequestions: 编写文档后，优良作法是校对文档，将自己放在用户的鞋子上（不再是开发此功能的专家），然后尝试回答以下问题：

 
- Does the information in the document explain the concept completely?  -文件中的信息是否完全说明了概念？
- Is there information that is not needed for this concept? If so, remove it.  -是否存在此概念不需要的信息？如果是这样，请将其删除。
- Is there unnecessary detail about how things might work in the background?  -是否有不必要的细节说明背景如何运作？
- If I am the user, is there additional I would have liked to know?  -如果我是用户，还有其他我想知道的吗？

Then, add your feedback into your document.  然后，将您的反馈添加到您的文档中。

 
## Procedural documentation {#procedural-documentation}  程序文档{procedural-documentation} 

Procedural documents are divided into two categories:  程序文件分为两类：

 
- **How-to** - Consider writing a how to when you want to help the user accomplish a very specific goal. -**操作方法**-考虑何时要帮助用户实现非常具体的目标。
- **Codelab** - Consider writing a codelab when you want to help the user learn about a bigger goal that might involve working with multiple parts of a product or feature. -**代码实验室**-当您想帮助用户了解可能涉及使用产品或功能的多个部分的更大目标时，请考虑编写代码实验室。

Procedural documentation should try to be brief and each task within your documentation should try to avoid going above 10 steps (codelabs can be much longer, but should not exceed 45-60 minutes fora user to complete). You should divide long procedures into multiple sub-tasks to try to keep tasksmanageable for a user. For example, if you wanted to write a procedural document for taking care ofa dog, you might have a table of content that looks like this: 过程性文档应该尽量简短，文档中的每个任务都应尽量避免超过10个步骤（代码实验室可以更长，但对于用户而言，则不应超过45-60分钟）。您应该将长过程分为多个子任务，以尝试使用户可管理任务。例如，如果您想编写一个程序文件来照顾狗，则可能会有一个如下所示的目录：

How to take care of a dog:  如何照顾狗：

 
- Feeding a dog  -喂狗
- Washing a dog  -洗狗
- Trimming a dog's nails  -修剪狗的指甲
- Brushing a dog  -刷狗
- Playing with a dog  -和狗一起玩

 
### Difference between a codelab and a how to  Codelab和方法之间的区别 

At a very high-level, a codelab is essentially a large how to, composed of various smaller how tos. Codelabs are great when you want to give the user a hand-held experience of working through a task,especially if this task is considered a little more complicated and might involve working withvarious areas of a product. On the other hand, a how to should describe the steps on how to workthrough a minor task that should only involve a single area of a product. 从很高的层次上讲，代码实验室本质上是一个大型的方法，由各种较小的方法组成。当您想为用户提供完成任务的手持式体验时，Codelabs非常有用，特别是如果认为该任务稍微复杂一点并且可能涉及产品的各个领域。另一方面，一种方法应该描述如何完成仅涉及产品单个区域的次要任务的步骤。

Consider the following when you think that you might need to create a codelab:  当您认为可能需要创建代码实验室时，请考虑以下内容：

 
- How many codelabs are planned for this general feature? Keep in mind that you do not want a whole documentation set to just be codelabs, use them in moderation. -为此通用功能计划了多少个代码实验室？请记住，您不希望整个文档集都只是代码实验室，而应适度使用它们。
- Codelabs should be self-contained, avoid creating links to other codelabs, other how-tos or other information that might have a user leave the actual codelab. It is ok to provide links toconceptual documents that can enhance a user's knowledge for a given topic. -代码实验室应该是独立的，避免创建指向其他代码实验室的链接，其他操作方法或其他可能使用户离开实际代码实验室的信息。可以提供指向概念性文档的链接，这些链接可以增强用户对给定主题的知识。
- Would this procedural documentation benefit from having a very specific example through a codelab? -通过代码实验室提供一个非常具体的示例，该程序文档会受益吗？
- Do you want to expose an exciting feature from the product through the codelab? This helps you highlight a neat feature that a user might not know about without doing a codelab. -您想通过Codelab公开产品中令人兴奋的功能吗？这可以帮助您突出显示一项精巧的功能，如果不执行代码实验室，用户可能会不知道。

 
### General procedural documentation guidelines  一般程序文件指南 

 
- Each task or subtask should have a paragraph that lets a user know what the task is about and what a user should be able to do after performing the steps. -每个任务或子任务都应有一个段落，让用户知道任务的含义以及执行步骤后用户应该能够执行的操作。
- Use screenshots or graphics to assist a user in navigating a user interface (UI).  -使用屏幕截图或图形来帮助用户浏览用户界面（UI）。
- A procedural document should not have to explain any concepts to a user, but should reference conceptual documents in case a user does not know about a certain concept. For example, aprocedure with a reference to a conceptual document might look like this: -程序文档不必向用户解释任何概念，而应在用户不知道某个概念的情况下引用概念文档。例如，参考概念文件的过程可能看起来像这样：

   Configure the server with the appropriate configuration. For more information about server configurations, see "server configuration". 使用适当的配置配置服务器。有关服务器配置的更多信息，请参阅“服务器配置”。

 
- Avoid giving the users multiple paths to select when working through procedures. When you avoid giving the user choices, your documentation should lead all users to the same end result (forexample, starting the server). -避免在执行过程时为用户提供多个选择路径。当您避免给用户选择时，您的文档应将所有用户引向相同的最终结果（例如，启动服务器）。
- If a procedural document is meant for beginner users, avoid adding procedures that you might consider better suited for advanced users. If your document is intended for advanced users, stateit up front and give them a list of prerequisites before they go through your how to or codelab. -如果程序文档是为初学者准备的，请避免添加您认为更适合高级用户的程序。如果您的文档供高级用户使用，请先声明并为他们提供先决条件列表，然后他们才能进行操作或使用代码实验室。
  
