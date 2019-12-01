 
# Unstable Rust Features  不稳定的防锈功能 

 
## Background  背景 

 
### What is Rust's `#![feature(...)]`?  Rust的`！[feature（...）]`是什么？ 

When using the `nightly` channel of Rust or when compiling `Rust` manually with the appropriate flags, it's possible to use unstable features. These features includelanguage additions, library additions, compiler features, and other capabilitiesnot subject to Rust's usual stability guarantees. Most of these features aretemporarily-unstable additions that will become stable after a period of time haspassed during which testing, discussion, and further design has completed. Somefeatures, however, are intentionally permanently-unstable features intended forinternal compiler use. Other features may be removed completely when a better solutionhas been found or when it was determined that the downsides of the feature outweighed theadvantages. Each feature has an [associated tracking issue on the`rust-lang/rust` Github repository][tracking issues]. 当使用Rust的“每晚”频道或使用适当的标记手动编译“ Rust”时，可能会使用不稳定的功能。这些功能包括语言添加，库添加，编译器功能以及不受Rust通常的稳定性保证约束的其他功能。这些功能大多数都是暂时不稳定的，经过一段时间的测试，讨论和进一步的设计完成后，这些功能将变得稳定。但是，某些功能是故意永久不稳定的功能，供内部编译器使用。当找到更好的解决方案或确定该功能的缺点超过了优点时，可以完全删除其他功能。每个功能都有一个[rust-lang / rust` Github存储库上的相关跟踪问题] [跟踪问题]。

 
### Our Rust Versioning Process  我们的Rust版本控制流程 

Fuchsia currently builds using a pinned revision of upstream Rust's master branch. We mirror Rust into [this repository][third_party/rust]. The version used to compileFuchsia is set [in the `prebuilts` manifest][prebuilts]. The latest revision ofRust which can be set in `prebuilts` is the most recently completed build [here][rust builder].We currently update the Rust version fairly often to pick up new changes we upstream,such as changes to syscalls used by the standard library. 紫红色目前使用上游Rust主分支的固定版本进行构建。我们将Rust镜像到[此存储库] [third_party / rust]。用来编译紫红色的版本是在[prebuilts清单] [prebuilts]中设置的。可以在“ prebuilts”中设置的Rust的最新版本是最近完成的构建[此处] [rust builder]。我们目前相当频繁地更新Rust版本，以获取上游的新更改，例如对使用的syscall的更改。标准库。

 
## The Goal  目标 

We want to be able to roll forward or backward to other versions of Rust to pick up bugfixes or roll back problem-inducing changes. Depending on too many unstable nightlyfeatures could make this process extremely painful. 我们希望能够向前或向后滚动到Rust的其他版本以获取错误修正或回退引起问题的更改。依赖太多不稳定的夜间功能可能会使此过程非常痛苦。

We also want to have code that is clear and easy to use, and use of unstable or rapidly changing features can make code harder to understand or modify. Unstable features areoften poorly documented, and what documentation exists is often out of date. 我们还希望拥有清晰易用的代码，而不稳定或快速变化的功能的使用会使代码更难以理解或修改。不稳定的功能通常记录很少，并且存在的文档经常过时。

That said, there are also a number of features that are designed explicitly for Fuchsia's use cases. These features provide great readability or performance benefits, and our useof them helps to prove them out and move them further along the path to stabilization. 也就是说，还有一些功能是针对Fuchsia的使用案例而明确设计的。这些功能提供了极大的可读性或性能优势，我们对它们的使用有助于证明它们并使其进一步稳定。

 
## The Process  流程 

Unstable feature requests should be sent to the rust-fuchsia@fuchsia.com mailing list. They should be hosted on docs.google.com to allow for comments and suggestion on thedocument itself. Proposals should include the following information: 不稳定的功能请求应发送至rust-fuchsia@fuchsia.com邮件列表。它们应托管在docs.google.com上，以允许对文档本身进行评论和建议。提案应包含以下信息：

 
- A quick summary of the feature  -功能简介
- What the feature is used for in Fuchsia  -紫红色功能有什么用
- A summary of what is left before the feature can be stabilized  -可以稳定功能之前所剩内容的摘要
- A person in charge of owning a particular feature who will follow the tracking issue, participate in discussion on how to modify or stabilize the feature, and manage anynecessary updates to Fuchsia code that result from breaking changes to the featureor removal of the feature. -拥有特定功能的人员将关注跟踪问题，参与有关如何修改或稳定功能的讨论，并管理因破坏功能或更改功能而造成的对紫红色代码的必要更新。

Following this email is a week-long comment period during which any arguments for or against a feature should be laid out on the doc. Once this period is over, a groupof reviewers will meet and come to a consensus decision on whether or not to allowuse of the feature. This decision will be based on arguments previously discussed onthe doc, and will not include new arguments brought by the review board members. Ifnew arguments surface, they will be added to the doc and more time will be given forothers to respond. 在此电子邮件之后是一个为期一周的评论期，在此期间，应在文档上列出支持或反对某项功能的任何论据。此期间结束后，一组审阅者将开会并就是否允许使用该功能达成共识。该决定将基于先前在文档中讨论过的论点，并且不包括审核委员会成员提出的新论点。如果出现新的论点，则会将其添加到文档中，并给其他人更多的响应时间。

If the feature is approved, the feature summary, usage, stabilization report, and owner listed in the doc are added to the "Currently Used Features" section listedbelow. This documentation must be checked in before the feature can be used. 如果功能获得批准，则文档中列出的功能摘要，使用情况，稳定性报告和所有者将添加到下面列出的“当前使用的功能”部分。必须先检入本文档，然后才能使用该功能。

The current list of reviewers is as follows:  当前的审阅者名单如下：

 
- cramertj@google.com  -cramertj@google.com
- etryzelaar@google.com  -etryzelaar@google.com
- raggi@google.com  -raggi@google.com
- tkilbourn@google.com  -tkilbourn@google.com

 
## Currently Used Features  当前使用的功能 

There are no longer any unstable features used in Fuchsia! The last one was `async_await`, which was stabilized in 2019 Q3. 紫红色不再使用任何不稳定的功能！最后一个是`async_await`，它在2019年第三季度稳定下来。

[the edition guide]: https://rust-lang-nursery.github.io/edition-guide/editions/index.html [Rust 2018: an early preview]: https://internals.rust-lang.org/t/rust-2018-an-early-preview/7776[Rust 2018: the home stretch]: https://internals.rust-lang.org/t/rust-2018-the-home-stretch/7810 [版本指南]：https://rust-lang-nursery.github.io/edition-guide/editions/index.html [Rust 2018：早期预览]：https://internals.rust-lang.org/ t / rust-2018-an-early-preview / 7776 [Rust 2018：the home Stretch]：https://internals.rust-lang.org/t/rust-2018-the-home-stretch/7810

