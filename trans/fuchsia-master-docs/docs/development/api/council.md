 
# Fuchsia API Council Charter  紫红色API委员会章程 

 
## Overview  总览 

This document describes the *Fuchsia API Council*, which is a group of people who are accountable for the quality and long-term health of the Fuchsia APISurface. The council will collaborate constructively with the people who createand modify Fuchsia’s APIs to help guide the evolution of those APIs. The councilwill communicate its decisions clearly, including the underlying rationale, andwill document best practices by contributing to Fuchsia’s API readabilityrubrics. 本文档介绍了* Fuchsia API Council *，这是一群对Fuchsia APISurface的质量和长期健康负责的人。该委员会将与创建和修改Fuchsia API的人员进行建设性合作，以帮助指导这些API的发展。该委员会将清楚地传达其决定，包括基本原理，并通过为Fuchsia的API可读性规范做出贡献来记录最佳实践。

 
## Definitions  定义 

The *Fuchsia System Interface* is the binary interface that the Fuchsia operating system presents to software running on the system. For example, theentry points into the vDSO as well as all the FIDL protocols used by the systemare part of the Fuchsia System Interface. * Fuchsia系统接口*是Fuchsia操作系统提供给系统上运行的软件的二进制接口。例如，该条目指向vDSO以及系统使用的所有FIDL协议都是Fuchsia系统接口的一部分。

A *client library* is a library that people writing software for Fuchsia might choose to use rather than interfacing directly with the Fuchsia SystemInterface. For example, FDIO is a client library that provides a POSIX-likeabstraction over the underlying fuchsia.io protocol in the Fuchsia SystemInterface. *客户端库*是人们为Fuchsia编写软件的人可能选择使用的库，而不是直接与Fuchsia SystemInterface接口。例如，FDIO是一个客户端库，它对Fuchsia SystemInterface中的底层fuchsia.io协议提供了类似于POSIX的抽象。

The *Fuchsia SDK* is a collection of libraries and tools that the Fuchsia project provides to people writing software for Fuchsia. Among other things, theFuchsia SDK contains a definition of the Fuchsia System Interface as well as anumber of client libraries. * Fuchsia SDK *是Fuchsia项目提供给人们为Fuchsia编写软件的库和工具的集合。除其他外，Fuchsia SDK包含Fuchsia系统接口的定义以及许多客户端库。

The *Fuchsia API Surface* is the combination of the Fuchsia System Interface and the client libraries included in the Fuchsia SDK. * Fuchsia API Surface *是Fuchsia系统接口和Fuchsia SDK中包含的客户端库的组合。

*Fuchsia contributors* are people who are involved in creating the Fuchsia operating system, including people who work for Google and people who do not. *紫红色的贡献者*是参与创建紫红色操作系统的人员，包括为Google工作的人和没有为Google工作的人。

*Fuchsia API* designers are people who create or modify the Fuchsia API Surface, including people who work for Google and people who do not. * Fuchsia API *设计师是创建或修改Fuchsia API Surface的人，包括为Google工作的人和不为Google工作的人。

*End-developers* are people who write software that consumes the Fuchsia API Surface. *最终开发者*是编写使用Fuchsia API Surface的软件的人。

*Users* are people who use devices that run the Fuchsia operating system.  *用户*是使用运行紫红色操作系统的设备的人。

 
## Goals  目标 

Ultimately, the end-goal of the Fuchsia API Council is to foster a healthy software ecosystem around the Fuchsia operating system. Fostering a healthyecosystem requires balancing many concerns, including growing the ecosystem andguiding the ecosystem towards particular outcomes. 最终，Fuchsia API委员会的最终目标是在Fuchsia操作系统周围建立一个健康的软件生态系统。培育健康的生态系统需要平衡许多问题，包括发展生态系统并使生态系统实现特定成果。

 
### Values  价值观 

The ecosystem has many participants who play many different roles. Ideally, we would be able to design APIs that meet the needs of everyone in the ecosystemsimultaneously, but API designers are often called upon to make decisions thatinvolve trade-offs. The council should help API designers make these decisionsin a way that respects the following *priority of constituencies*: 生态系统中有许多参与者扮演着不同的角色。理想情况下，我们将能够设计出能够同时满足生态系统中每个人需求的API，但是通常会要求API设计者做出涉及折衷的决策。理事会应该以尊重以下*优先对象*的方式，帮助API设计者做出这些决定：

 
1.  Users  1.用户
1.  End-developers  1.最终开发者
1.  Contributors  1.贡献者
1.  API designers  1. API设计人员
1.  Council members  1.理事会成员

For example, we should design APIs that protect user privacy, even at the expense of not fulfilling all the desires of end-developers. Similarly, weshould design APIs that are better for end-developers even if those designsplace a higher burden on the people implementing the APIs. 例如，我们应该设计保护用户隐私的API，即使以不满足最终开发人员的所有愿望为代价。同样，即使这些设计给实施API的人员带来更大的负担，我们也应该设计出对最终开发者更好的API。

These values help guide the ecosystem towards meeting the needs of users, which promotes the health and growth of the ecosystem in the long run because usersare more likely to join, and remain in, an ecosystem that meets their needs. 这些价值有助于指导生态系统满足用户的需求，从长远来看将促进生态系统的健康和增长，因为用户更有可能加入并留在满足其需求的生态系统中。

 
### Strategy  战略 

To achieve these goals, the council focus on the following metrics:  为了实现这些目标，理事会着重于以下指标：

 
*   *Functionality*. The council is accountable for the functionality of the Fuchsia API Surface. Specifically, functionality refers to whether the APIsmeet the needs of the ecosystem participants. For example, the council isaccountable for how well our APIs protect the privacy of users, how well ourAPIs help end-developers accomplish a given task, and how well our APIs letFuchsia contributors improve their implementations over time. * *功能*。该委员会对Fuchsia API Surface的功能负责。具体来说，功能是指API是否满足生态系统参与者的需求。例如，理事会负责解决我们的API如何保护用户的隐私，我们的API如何帮助最终开发人员完成给定的任务，以及我们的API如何使紫红色的贡献者随着时间的推移改善其实现。

 
*   *Usability*. The council is accountable for the usability of the Fuchsia API Surface. For example, the council should strive for consistency in howsimilar concepts are expressed in our APIs, which makes our APIs easier forend-developers to learn. Similarly, the council should ensure that our APIsare well-documented and that the semantics of interfaces are intuitive fromtheir declaration. * *可用性*。该委员会对紫红色API Surface的可用性负责。例如，理事会应该努力在API中表达相似概念的方式上保持一致，这使我们的API更易于最终开发人员学习。同样，理事会应确保我们的API记录良好，并且接口的语义从其声明起就很直观。

 
*   *System impact*. The council is accountable for the burden on the system as a whole incurred through the use of the Fuchsia API Surface, including bothintended and unintended usage. For example, APIs that use polling impose alarge burden on the system because they require their clients to runcontinuously to monitor changes in conditions. Assessing system impactrequires a significant amount of judgement and experience, especially topredict unintended uses of APIs. * *系统影响*。对于使用Fuchsia API Surface造成的整个系统负担，理事会负责，包括计划内和计划外使用。例如，使用轮询的API给系统带来了很大的负担，因为它们要求其客户端连续运行以监视条件的变化。评估系统影响需要大量的判断和经验，尤其是要预测API的意外使用。

 
*   *Communication clarity*. The council is responsible for clearly communicating decisions and the rationale behind those decisions to Fuchsiacontributors. This communication should provide transparency about thedecision-making process and should help educate API designers about how tocreate high-quality APIs. For example, the council should document bestpractices by contributing to Fuchsia’s API readability rubrics. * *通讯清晰度*。该委员会负责向紫红色的贡献者清楚地传达决策及其决策的依据。这种交流应使决策过程透明，并应帮助教育API设计人员如何创建高质量的API。例如，理事会应通过对Fuchsia的API可读性准则做出贡献来记录最佳实践。

 
*   *Customer satisfaction*. The council is responsible for collaborating constructively with API designers. The council should foster an environmentin which council members and API designers work in partnership to improvethe Fuchsia API Surface. API designers should see the council as providingpositive value, helping them make better APIs, rather than as bureaucraticburden. For example, council members should respond promptly andrespectfully to requests for API reviews. *   *消费者满意度*。该委员会负责与API设计人员进行建设性的合作。理事会应该营造一种环境，理事会成员和API设计师可以在这种环境下合作改善紫红色API Surface。 API设计人员应将理事会视为提供积极价值，帮助他们制定更好的API的机构，而不是官僚负担。例如，理事会成员应对API审查请求做出及时，尊重的回应。

 
## Membership  会员资格 

The council is comprised of Fuchsia contributors who have demonstrated:  该委员会由紫红色的贡献者组成，他们表现出：

 
*   Good judgement about the quality and long-term health of APIs, either within Fuchsia or in their past work with other platforms. *对API的质量和长期运行状况做出良好的判断，无论是在Fuchsia中还是在过去与其他平台一起使用中。

 
*   Strong communication and collaboration skills, as viewed by API designers (i.e., their collaborators). * API设计者（即他们的合作者）所认为的强大的沟通和协作技能。

Members are appointed by each functional area of the project:  成员由项目的每个职能领域任命：

| Area              | Appointee               | | ----------------- | ----------------------- || Auth              | jsankey@google.com      || Architecture      | silberst@google.com     || Component         | jeffbrown@google.com    || Connectivity      | tkilbourn@google.com    || DDK               | teisenbe@google.com     || Developer         | dschulyer@google.com    || Drivers           | ravoorir@google.com     || Experiences       | chaselatta@google.com   || FIDL              | ianloic@google.com      || Graphics          | adamgousetis@google.com || Kernel            | cpu@google.com          || Ledger            | qsr@google.com          || Media             | dalesat@google.com      || Metrics           | rudominer@google.com    || Modular           | lindkvist@google.com    || Security          | jsankey@google.com      || Software Delivery | raggi@google.com        || Storage           | smklein@google.com      || System            | cpu@google.com          || Toolchain         | mcgrathr@google.com     || Virtualization    | abdulla@google.com      || Web               | wez@google.com          | |面积任命| | ----------------- | ----------------------- ||验证| jsankey@google.com ||建筑| silberst@google.com ||组件| jeffbrown@google.com ||连接性| tkilbourn@google.com || DDK | teisenbe@google.com ||开发人员dschulyer@google.com ||驱动程序| ravoorir@google.com ||经验| chaselatta@google.com || FIDL | ianloic@google.com ||图形| adamgousetis@google.com ||内核| cpu@google.com ||分类帐| qsr@google.com ||媒体| dalesat@google.com ||指标| rudominer@google.com ||模块化| lindkvist@google.com ||安全性jsankey@google.com ||软件交付| raggi@google.com ||储存| smklein@google.com ||系统| cpu@google.com ||工具链| mcgrathr@google.com ||虚拟化abdulla@google.com ||网页| wez@google.com |

As the project evolves, the list of functional areas (and therefore the makeup of the council) will evolve as well. The list of functional areas is maintainedby Fuchsia leadership. 随着项目的发展，职能领域的清单（以及理事会的组成）也会随之发展。功能区列表由紫红色领导层维护。

The council also has a *chair*, whose job is to facilitate the operations of the council. For example, the chair (a) schedules meetings, (b) sets the agenda forthose meetings, and (c) assesses whether the council has reached[rough consensus](https://en.wikipedia.org/wiki/Rough_consensus). The chair isappointed by Fuchsia leadership. 理事会还有一位“主席”，其职责是促进理事会的运作。例如，主席（a）安排会议，（b）安排会议议程，（c）评估理事会是否已达成[大致共识]（https://en.wikipedia.org/wiki/Rough_consensus）。主席由樱红色领导任命。

 
## Decision process  决策过程 

If the council is called upon to make a decision, the decision process is as follows. The council member for the area in question is the *primary decisionmaker*, but the council as a whole is the *final decision maker*. The council asa whole makes decisions by *rough consensus*, as assessed by the chair. 如果要求理事会做出决定，则决定过程如下。该地区的理事会成员是“主要决策者”，但整个理事会是“最终决策者”。整个理事会通过主席评估的“大致共识”做出决策。

 
*   The primary decision maker can *defer* a decision, in which case the council will make the decision. If the council fails to reach rough consensus, thechair will make the final decision. *主要决策者可以*推迟*一项决定，在这种情况下，理事会将做出决定。如果理事会未能达成大致共识，则主席将做出最终决定。

 
*   A council member can ask the council to *overrule* the primary decision maker. If the council fails to reach rough consensus, the decision made bythe primary decision maker stands. *理事会成员可以要求理事会*推翻*主要决策者。如果理事会未能达成大致共识，则由主要决策者做出的决定有效。

 
## Operations  运作方式 

The council has two major functions: API review and API calibration.  该委员会具有两个主要职能：API审查和API校准。

 
### API review  API审查 

Every change to the Fuchsia API Surface requires approval from a council member. A change in a particular functional area should typically be approved by thecouncil member responsible for that area, but any council member can approve thechange if the responsible council member is unavailable. 紫红色API Surface的每次更改都需要获得理事会成员的批准。特定功能区域的更改通常应由负责该功能区域的理事会成员批准，但是如果负责的理事会成员不可用，则任何理事会成员都可以批准该更改。

Before being merged, every CL that modifies the Fuchsia API Surface must receive an API-Review+1 from a member of[api-council@fuchsia.com](https://groups.google.com/a/fuchsia.com/forum/#!forum/api-council)in addition to the usual Code-Review+2. The same person can provide bothAPI-Review+1 and Code-Review+2 for a given change, but someone cannot give theirown CLs API-Review+1. See[Review Labels](https://gerrit-review.googlesource.com/Documentation/config-labels.html)for documentation about this Gerrit feature. 在合并之前，每个修改Fuchsia API Surface的CL都必须从[api-council@fuchsia.com]（https://groups.google.com/a/fuchsia.com/ Forum /！forum / api-council），以及通常的Code-Review + 2。同一个人可以为给定的更改提供API-Review + 1和Code-Review + 2，但是某人无法提供自己的CL API-Review + 1。有关此Gerrit功能的文档，请参见[Review Labels]（https://gerrit-review.googlesource.com/Documentation/config-labels.html）。

For small API changes, especially incremental refinements to existing APIs, a code review is usually sufficient for an API reviewer to give the changeAPI-Review+1. However, for larger changes, especially those that expand the APIsurface significantly, the API designer should write an *API Design Document*(see [Fuchsia API Design Template](http://go.corp.google.com/fuchsia-api-design-template)),which explains the design of the API, including use cases and examples, as wellas security and privacy considerations. An API reviewer can always request theAPI designer to write an API Design Document, even for small changes if the APIreviewer does not feel comfortable approving the change purely through codereview. 对于较小的API更改，尤其是对现有API的增量改进，通常，对于API审阅者来说，进行代码审阅就足以提供changeAPI-Review + 1。但是，对于较大的更改，尤其是那些显着扩展API表面的更改，API设计者应编写* API设计文档*（请参阅[Fuchsia API设计模板]（http://go.corp.google.com/fuchsia-api-设计模板）），其中说明了API的设计，包括用例和示例，以及安全性和隐私注意事项。 API审阅者始终可以要求API设计者编写API设计文档，即使对于较小的更改，如果API审阅者不愿意纯粹通过codereview批准更改，则API审阅者也可以。

API designers are also encouraged to seek early feedback from council members. For example, API designers should consider sharing work-in-progress API DesignDocuments with council members to get input early in the design process. Councilmembers should engage in these discussions with the goal of partnering with APIdesigners to help design the best API. API designers can also seek feedbackearly in the design process from the full council by asking the chair for a slotin the agenda for an upcoming API calibration session (see the next section). 还鼓励API设计人员寻求理事会成员的早期反馈。例如，API设计人员应考虑与理事会成员共享进行中的API DesignDocuments，以便在设计过程中尽早获得意见。委员们应该参与这些讨论，以与APIdesigners合作，以帮助设计最佳的API。 API设计人员还可以在整个设计委员会的早期寻求反馈，方法是要求主席为即将到来的API校准会议安排议程中的空位（请参阅下一节）。

The API reviewer should work with the API designer to improve the API Design Document to the point where the API reviewer feels comfortable approving thedocument. An approved document serves as the plan of record for the API inquestion. However, individual CLs that modify the API surface still need toreview API-Review+1 before being merged. API designers should expect that CLsthat follow the plan laid out in an approved API Design Document should reviewAPI-Review+1 quite easily, even from other council members. API审阅者应与API设计人员合作，以将API设计文档改进到API审阅者可以轻松批准文档的程度。批准的文件将用作API询问的记录计划。但是，修改API表面的单个CL仍需要在合并之前检查API-Review + 1。 API设计人员应该期望遵循批准的API设计文档中列出的计划的CL应当很容易地对API-Review + 1进行审核，即使是来自其他理事会成员。

API designers or reviewers can refer a API Design Document to the full council by asking the chair for a slot in the agenda for an upcoming API calibrationsession (see the next section). For example, an API reviewer might refer adocument to the full council if the API reviewer does not feel sufficientlycalibrated, if the API is particularly complex or important, or if the reviewerfeels pressured by looming deadlines or other teams. API设计人员或审阅者可以通过要求主席在议程中安排即将举行的API校准会议的方式将API设计文档提交给整个理事会（请参阅下一节）。例如，如果API审阅者觉得校准不够充分，API特别复杂或重要，或者如果审阅者感到迫在眉睫的截止日期或其他团队的压力，则API审阅者可能会将文档提交给全体理事会。

 
### API calibration  API校准 

Periodically, the API council will meet for *API calibration*. The purpose of API calibration is to promote consistency of API reviews across the project andto improve the quality of API reviews by cross-pollinating best practices acrossthe council. These meetings often have a *facilitator*, who keeps the meeting ontopic and helps ensure each participant has a chance to provide their feedback. API委员会将定期召开* API校准*会议。 API校准的目的是通过跨委员会的最佳实践来提高整个项目中API评审的一致性，并提高API评审的质量。这些会议通常有一个“主持人”，负责保持会议的主题，并帮助确保每个参与者都有机会提供反馈。

Fuchsia contributors can observe API calibration meetings. Observing these meetings can be a good way to learn best practices about evolving our APIsurface. 紫红色的贡献者可以参加API校准会议。观察这些会议可能是学习有关改进APIsurface的最佳实践的好方法。

 
#### Review API Design Documents  审核API设计文档 

The first priority in API calibration is to review any API Design Documents that have been referred to the full council. If there are multiple pending documents,the chair will select the order in which the council works through thedocuments. API校准的首要任务是查看已提交给全体理事会的所有API设计文档。如果有多个待处理的文件，主席将通过文件选择理事会的工作顺序。

The API designer who wrote the document should present the document, providing the council with the necessary context to understand the issues at stake.Afterwards, the person who referred the document should lead a discussion of theareas of the API design for which they are seeking feedback. Council members areencouraged to focus their feedback on those areas but are free to providefeedback about the document as a whole. 编写文档的API设计师应提交文档，为理事会提供必要的背景信息，以了解相关问题。随后，提交文档的人员应领导对他们寻求反馈的API设计领域的讨论。 。鼓励理事会成员将反馈意见集中在这些领域，但可以自由提供有关整个文档的反馈。

 
#### Review backlog  审查积压 

The Fuchsia API Surface contains a large number of APIs that were designed before the council was formed. The council will work through that backlog of APIreviews, eventually reaching the point where every API in the Fuchsia APISurface has been reviewed. Ideally, the council will have a chance to review theentire Fuchsia API Surface before Fuchsia commits to the backwards compatibilityof its APIs. 紫红色的API Surface包含大量在理事会成立之前设计的API。该委员会将处理积压的API审查，最终达到对紫红色APISurface中的每个API进行审查的地步。理想情况下，在紫红色致力于其API的向后兼容性之前，理事会将有机会审查整个紫红色API表面。

The chair selects the order in which the council works through the backlog, attempting to balance reviewing APIs from diverse areas of the project with theurgency to review APIs that are acreeting a large number of clients. 主席选择委员会通过积压工作的顺序，试图平衡项目各个领域的审阅API与审阅吸引大量客户的API的紧迫性。

When reviewing an API, the council member who is responsible for the area that contains the API (hereafter the *responsible member*) will present the API,providing the council with the necessary context to understand the use cases andmotivation for the API. The responsible member can invite one or more subjectmatter experts to help provide additional context and technical details.Ideally, the responsible member will have pre-reviewed the API and will have alist of proposed modifications. 在审查API时，负责包含该API的区域的理事会成员（以下称“负责成员”）将介绍API，为理事会提供必要的背景信息，以了解该API的用例和动机。负责任的成员可以邀请一位或多名主题专家来帮助提供其他上下文和技术细节。理想情况下，负责任的成员将对API进行预审，并列出建议的修改内容。

 
#### Secondary review  二次审查 

The council will also cycle through the functional areas of the project, performing a secondary review of changes to the API surface for each area sincethe last cycle. This activity lets the council provide feedback to members ontheir recent API reviews. 理事会还将在项目的功能区域中进行循环，对自上一个循环以来每个区域的API表面变化进行二次审查。通过此活动，理事会可以就其最近的API审查向成员提供反馈。

The chair will select the order in which the areas are reviewed, attempting to balance reviewing APIs from diverse areas of the project with the urgency toreview APIs that have a large volume of changes. 主席将选择区域审核的顺序，尝试平衡项目各个领域的审核API与迫切需要进行大量更改的API的平衡。

During secondary review, the council member who was the primary reviewer for the API change will present the change as well as any associated API DesignDocuments, providing the council with the necessary context to understand theuse cases and motivation for the changes. The API designer who made the changein question is also encouraged (but not required) to attend. 在二次审核期间，作为API更改的主要审核者的理事会成员将提出更改以及任何相关的API设计文档，从而为理事会提供必要的背景信息，以了解更改的用例和动机。鼓励（但不是必须）进行更改问题的API设计人员参加。

Generally, the council should respect the decisions made during the primary API review, but council members are encouraged to provide feedback about how the APIcould have been improved, which benefits future reviews. Depending on thematurity of the API, the primary reviewer might decide to incorporate theseimprovements into the API. In rare cases, the council can overrule the primaryreviewer, per the council’s decision process. 通常，理事会应尊重主要API审核期间做出的决定，但鼓励理事会成员提供有关API可能如何改进的反馈，这对将来的审核很有帮助。根据API的成熟度，主要审核者可能会决定将这些改进合并到API中。在极少数情况下，理事会可以根据理事会的决策流程推翻主要审核者。

 
## Acknowledgements  致谢 

