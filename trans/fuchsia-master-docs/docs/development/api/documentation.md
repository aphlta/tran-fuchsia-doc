 
# API Documentation Readability Rubric  API文档的可读性 

 
## Overview  总览 

This section contains guidance on writing documentation for Fuchsia's APIs.  It applies both to public-facing APIs (those surfaced via an SDK) andFuchsia-internal ones.  Public facing API documentation will be reviewed by the[API Council](council.md) for adherence to this rubric. 本节包含有关编写Fuchsia API的文档的指南。它同时适用于面向公众的API（通过SDK公开的API）和紫红色的内部API。面向公众的API文档将由[API委员会]（council.md）进行审核，以确保其遵守该原则。

 
## Overall commenting rules  总体评论规则 

In most cases, documentation should follow the language's style guide for comments.  If there is a rule in this document that contradicts thelanguage-specific rules, follow this document's guidance.  In some cases, thelanguage-specific rules take precedence; these special cases are identifiedbelow. 在大多数情况下，文档应遵循该语言的样式指南进行注释。如果本文档中有一条规则与特定于语言的规则相矛盾，请遵循本文档的指导。在某些情况下，特定于语言的规则优先；这些特殊情况如下。

Here are the links to language-specific guidelines for languages likely to be used in the Fuchsia repository: [C andC++](/docs/development/languages/c-cpp/cpp-style.md),[Dart](/docs/development/languages/dart/style.md)[Rust](https://github.com/rust-lang-nursery/fmt-rfcs/blob/master/guide/guide.md),[Java](https://google.github.io/styleguide/javaguide.html),[Kotlin](https://kotlinlang.org/docs/reference/coding-conventions.html#documentation-comments).We also recommend reading [Google's guidelines on APIdocumentation](https://developers.google.com/style/api-reference-comments). 以下是指向可能在Fuchsia存储库中使用的语言的特定于语言的准则的链接：[C和C ++]（/ docs / development / languages / c-cpp / cpp-style.md），[Dart]（/ docs /开发/语言/dart/style.md）[锈]（https://github.com/rust-lang-nursery/fmt-rfcs/blob/master/guide/guide.md），[Java]（https：/ /google.github.io/styleguide/javaguide.html),[Kotlin](https://kotlinlang.org/docs/reference/coding-conventions.htmldocumentation-comments）。我们还建议您阅读[Google关于API文档的指南]（ https://developers.google.com/style/api-reference-comments）。

 
## Communicating with care  谨慎沟通 

Documentation is intended to be consumed by the general public, and should be written in a technical and neutral tone.  There are some explicit restrictionson what you can write below, but they aren't intended to be comprehensive - usegood judgment! 文件旨在供普通大众使用，并且应以技术性和中性的语调编写。您可以在下面写一些明确的限制，但它们并不旨在全面，请使用良好的判断力！

 
 * Do not include any reference to anyone's proprietary information.  Do not use sensitive information (personally identifiable information, authenticationkeys, etc). *请勿引用任何人的专有信息。请勿使用敏感信息（个人身份信息，身份验证密钥等）。
 * Do not use swear words or other potentially aggressive language (words like, e.g., "stupid") *请勿使用脏话或其他潜在的攻击性语言（例如“愚蠢”之类的词）

 
## General style  一般风格 

 
 * Spelling, punctuation, and grammar matter.  Use US English spelling.  Use the serial comma. *拼写，标点和语法问题。使用美国英语拼写。使用串行逗号。
 * Do not list authors explicitly.  Author information goes out of date quickly, as developers move to different projects.  Consider providing a maintainersfile, although be wary that this goes out of date, too. *不要明确列出作者。随着开发人员转到不同的项目，作者信息很快就会过时。考虑提供一个维护者文件，尽管请注意这也已过时。
 * Optimize your code for the intended display (e.g., use markdown or Javadoc as intended).<!-- * Do not write TODO(username), write TODO(reference-to-bug).  Bug ownershipgoes out of date quickly, as developers move to different projects.  Thisincludes documentation on unimplemented APIs and implementation notes. --> *针对预期的显示优化代码（例如，按预期使用markdown或Javadoc）。<！-*不要编写TODO（用户名），编写TODO（引用错误）。随着开发人员转移到其他项目，错误所有权很快就会过时。这包括有关未实现的API的文档和实现说明。 ->

Only apply the following rules in the absence of language-specific practices and guidance: 仅在没有特定语言的实践和指导的情况下应用以下规则：

 
 * Documentation should immediately precede the element it is documenting.  *文档应紧接在要记录的元素之前。
 * Use markdown for comments.  The style of markdown is the style understood by the tool most likely to consume the API. *使用markdown进行评论。 markdown的样式是工具最有可能使用API​​的样式。
   * Use backticks for code blocks instead of 4-space indents.  *对代码块使用反引号，而不是4空格的缩进。
 * All comments should use complete sentences.  *所有评论应使用完整的句子。

 
## API elements  API元素 

 
 * A **public facing API element** is one that is made available to developers via an SDK.  All public facing API elements (including, but not limited tomethods, classes, fields, types) must have a description.  Internal librariesshould be documented; there should be a good reason if they are not. *面向公众的API元素**是可通过SDK向开发人员提供的元素。所有面向公众的API元素（包括但不限于方法，类，字段，类型）都必须具有描述。内部图书馆应形成文件；如果没有，应该有充分的理由。

 
 * All parameters must have a description, unless that description would be redundant with the type and name. *所有参数都必须具有描述，除非该描述与类型和名称重复。
   * If it is not obvious from the type what a parameter's legal values are, consider changing the type.  For example, {-1, 0, 1} is less useful than anenum with {LESS\_THAN, EQUAL\_TO, GREATER\_THAN}. *如果从类型上看不到参数的合法值是什么，请考虑更改类型。例如，{-1，0，1}比使用{LESS \ _THAN，EQUAL \ _TO，GREATER \ _THAN}的小事例有用。
   * Otherwise, document the behavior of the API for all possible input values. We discourage undocumented values. *否则，请针对所有可能的输入值记录API的行为。我们不鼓励未记录的价值。

 
 * All return values must have a description, unless that description would be redundant with the type and name. *所有返回值都必须具有描述，除非该描述在类型和名称上多余。
   * If a method or function returns a subset of its return type, document the subset. *如果方法或函数返回其返回类型的子集，请记录该子集。
   * Document all returned errors and the circumstances under which they can be produced. *记录所有返回的错误及其可能产生的情况。
   * For example, if the method's return type is zx\_status\_t, and it only returns ZX\_OK and ZX\_ERR\_INVALID\_ARGS, your documentation must statethat explicitly. *例如，如果该方法的返回类型为zx \ _status \ _t，并且仅返回ZX \ _OK和ZX \ _ERR \ _INVALID \ _ARGS，则您的文档必须明确声明。
   * If it is not immediately obvious what a particular return value means, it must be documented.  For example, if a method returns ZX\_OK, you don'tneed to document it.  If a method returns the length of a string, itshould be documented. *如果不能立即明显看出特定返回值的含义，则必须将其记录在案。例如，如果某个方法返回ZX \ _OK，则无需对其进行记录。如果方法返回字符串的长度，则应将其记录下来。

 
 * All possible thrown exceptions must have a description, which must include the conditions under which they are thrown, unless obvious from the type andname. *所有可能引发的异常都必须有描述，其中必须包括引发异常的条件，除非从类型和名称可以明显看出。
   * Some third party code does not document exceptions consistently.  It may be hard (or impossible) to document the behavior of code that depends suchAPIs.  Best effort is acceptable; we can resolve resulting issues as theyarise. *某些第三方代码不能一致地记录例外情况。要记录依赖于此类API的代码的行为可能很困难（或不可能）。尽力而为是可以接受的；我们可以解决随之而来的问题。
   * Document whether exceptions are recoverable and, if so, how to recover from them. *记录异常是否可恢复，以及如何恢复。

 
 * For any API elements that are extensible, indicate whether they are intended to be extended, and requirements for those who might want to extend them. *对于任何可扩展的API元素，请指明它们是否打算扩展，以及对可能要扩展它们的需求。
   * If an API is extensible for internal reasons (e.g., testing), document that.  For example, you should document if you have allowed a class to beextended in order to make it easy to create test doubles. *如果API是出于内部原因（例如，测试）而可扩展的，请记录该文件。例如，您应该记录是否允许扩展一个类，以便于创建测试对偶。

 
 * Document deprecated API elements.  *文档弃用的API元素。
   * Documentation on deprecated API elements must state what a user is expected to do instead of using the API. *关于过时的API元素的文档必须说明希望用户做什么，而不是使用API​​。
   * Plans to eliminate the API should be clearly documented (if they exist).  *消除API的计划应明确记录（如果存在）。
   * If an explanation of the deprecation status of an API element would reduce the quality of the API documentation, consider providing a pointer tofurther information, including URLs and bug identifiers. *如果对API元素的弃用状态的解释会降低API文档的质量，请考虑提供指向更多信息的指针，包括URL和错误标识符。

 
## API behavior  API行为 

Document user-facing invariants, as well as pre- and post-conditions.  记录面向用户的不变式，以及前提条件和后置条件。

 
 * As a rule, ensure that there are assertions / tests to enforce these conditions. *通常，请确保有断言/测试来强制执行这些条件。
 * Preconditions and postconditions that require explicit user action should be documented.  For example, provide documentation if an `Init()` methodneeds to be called before anything else happens. *应该记录需要显式用户操作的前提条件和后置条件。例如，如果需要在其他任何事情发生之前调用Init（）方法，请提供文档。
 * Correlations between parameters or return values (e.g., one has to be less than another) should be documented. *应记录参数或返回值之间的相关性（例如，一个必须小于另一个）。

 
### Concurrency  并发 

Document the concurrency properties of APIs that have internal state.  记录具有内部状态的API的并发属性。

 
 * FIDL servers may execute requests in an unpredictable order.  Documentation should account for situations where this might affect the behavior the callerobserves. * FIDL服务器可能以不可预测的顺序执行请求。文档应说明可能影响呼叫者观察到的行为的情况。
 * Every API with internal state falls into one of the following categories. Document which one, using the following terms: *每个具有内部状态的API都属于以下类别之一。使用以下术语记录其中一个：
   * **Thread-safe**: This means invocations of individual elements of the API (e.g., methods in a class) are atomic with respect to other concurrentprocesses.  There is no need for a caller to use any externalsynchronization (e.g., a caller should not have to acquire a lock for theduration of the method invocation).  You may still describe your API asthread-safe if a caller needs to use external synchronization to makereferences to instances of the API visible to other threads (e.g., bysetting and getting a global pointer to an instance of a class with atomicoperations). * **线程安全**：这意味着API的各个元素（例如，类中的方法）的调用相对于其他并发进程是原子的。调用者无需使用任何外部同步（例如，调用者不必为方法调用的持续时间获取锁）。如果调用者需要使用外部同步来使对该API实例的引用对其他线程可见（例如，通过使用atomicoperations设置并获取指向类实例的全局指针），您仍可以将API描述为线程安全的。
   * **Thread-unsafe**: This means that all methods must use external synchronization to ensure invariants are maintained (e.g., mutualexclusion enforced by a lock). * **线程不安全**：这意味着所有方法都必须使用外部同步来确保不变性得到维护（例如，由锁强制执行的互斥）。
   * **Thread-hostile**: This means that the API element should not be accessed from multiple threads (e.g., it has implementation details that rely onunsynchronized access to static data behind the scenes, like strtok()).This should include documentation about thread affinity (e.g., it usesTLS).  It is only allowed in Fuchsia APIs by exception. * **线程不友好**：这意味着不应从多个线程访问API元素（例如，其实现细节依赖于对后台静态数据的非同步访问，例如strtok（）），其中应包括文档关于线程亲和力（例如，它使用TLS）。紫红色API仅允许例外。
   * **Special**: This means that the correct concurrent use of this API requires thought, please read the docs.  This is especially relevant whenentities need to be initialized and references to them published in aspecific way. * **特殊**：这意味着需要同时考虑正确使用此API，请阅读文档。当需要初始化实体并以特定方式发布对它们的引用时，这尤其重要。
   * **Immutable**: The other four classes assume that internal state is mutable and thread safety is guaranteed by synchronization.  Immutableclasses appear constant without any additional synchronization, but youhave to maintain strict rules about serialization / deserialization andhow references to the object are shared between threads. * **不可变**：其他四个类假定内部状态是可变的，并且通过同步保证线程安全。不可变类在没有任何其他同步的情况下显示为常量，但是您必须维护有关序列化/反序列化以及如何在线程之间共享对对象的引用的严格规则。
 * An API is **blocking** if it is not guaranteed to make progress.  Document the blocking properties of your APIs. *如果不保证一定要取得进展，则API是“阻塞”的。记录API的阻止属性。
   * If an API is blocking, the documentation must state what is required for the code to make progress, unless blocking is a low probability event thatrequires implementation understanding. *如果API被阻塞，除非阻塞是需要实现理解的低概率事件，否则文档必须说明代码取得进展所需的条件。
     * An example of when you must document a method's blocking behavior is when it blocks waiting for a response on a channel. *您何时必须记录方法的阻塞行为的一个示例是何时阻塞等待通道上的响应。
     * An example of when you do not have to document a method's blocking behavior is when it may block if lock starvation is a theoreticalpossibility under high load. *不必记录方法的阻塞行为的一个例子是，如果锁饥饿在高负载下是理论上可行的，则该方法可能会阻塞。
   * An API is not considered blocking only because it takes a long time to finish.  A slow algorithm should not be documented to be blocking. *仅因为花费很长时间才能将API视为阻塞。慢速算法不应被记录为阻塞。
   * Documentation should only state that an API is non-blocking when the non-blocking behavior is critical to its use (for example, if an APIreturns a future). *文档仅应在非阻塞行为对其使用至关重要的情况下（例如，如果API返回未来）说明API是非阻塞的。
 *  An API is **reentrant** if it may be safely interrupted in the middle of its execution and then called again.  Document the reentrance properties of yourAPIs. *如果可以在执行过程中安全地中断该API，然后再次调用该API，则该API是“可重入的” **。记录您的API的重入属性。
    * APIs may be assumed to be reentrant.  Documentation must state if an API is not reentrant. *可以认为API是可重入的。文档必须说明API是否不可重入。
 * Document whether a function relies on **thread-local storage (TLS)** to maintain its invariants, and any preconditions and postconditions related tothat TLS (e.g., if it needs to call an initializer once per thread). *记录函数是否依赖**线程本地存储（TLS）**来保持其不变性，以及与该TLS相关的任何前提条件和后置条件（例如，是否需要每个线程调用一次初始化程序）。

 
### Ownership  所有权 

Document ownership and liveness properties.  文档所有权和活动性属性。

 
 * For parameters or return values that are stored beyond the life of a function, or resources allocated by the function and passed back to thecaller, or resources with particular ownership constraints that must beobserved by a set of APIs (i.e., shared resources), ownership and livenessmust be documented. *对于超出函数寿命存储的参数或返回值，或者由函数分配并传递回调用者的资源，或具有特定所有权约束的资源（必须由一组API进行观察）（即共享资源），所有权和活泼必须记录在案。
 * Document who is responsible for releasing any associated resources.  *记录谁负责释放任何相关资源。
 * Where appropriate, documentation should state the protocol for releasing those resources.  This can be a special issue when memory allocationroutines differ between the caller of an API and the API. *在适当的地方，文档应说明释放这些资源的协议。当API的调用者和API的内存分配例程不同时，这可能是一个特殊的问题。
   * Languages should call out default ownership behavior in their style guides. *语言应在其样式指南中注明默认的所有权行为。

 
### Nullness  虚无 

All parameters and return values must have their nullness properties defined (if they are of a nullable type). 所有参数和返回值都必须定义其nullness属性（如果它们是可为null的类型）。

 
 * Even in Dart!  *即使在Dart中！
 * Where appropriate, refer to parameters and return values as **nullable** (may contain null) or **non-null** (may not contain null). *在适当的地方，将参数和返回值称为** nullable **（可能包含空值）或** non-null **（可能不包含空值）。

 
### Units  单位 

For all parameters and return types, units must be well defined (whether by documentation or by type). 对于所有参数和返回类型，必须明确定义单位（无论是按文档还是按类型）。

 
## Best Practices  最佳实践 

This section contains guidance that should be taken into consideration when writing comments.  It contains opinions, rather than the unambiguous rules givenabove. 本节包含编写注释时应考虑的指导。它包含意见，而不是上面给出的明确规则。

 
* A reader should not have to look at an API's implementation to figure out what it does.  Consider writing documentation that would allow a reader toimplement your API independently based on the documentation.  If, to do this,a comment needs to provide a level of detail that is not useful to mostprogrammers, consider putting that detail in a separate document and providinga link to that document. *读者不必查看API的实现来弄清楚它的作用。考虑编写文档，使读者可以根据文档独立地实现您的API。如果要这样做，注释需要提供对大多数程序员没有用的详细程度，请考虑将这些详细信息放在单独的文档中并提供指向该文档的链接。
* Avoid jargon that may not be obvious to the reader (think: "if I am interested in this API, will I definitely know what this word means?"). *避免使用对读者来说不明显的行话（请考虑：“如果我对此API感兴趣，我肯定会知道这个词是什么意思吗？”）。
* Avoid abbreviations and acronyms.  When you need to use them, explain them. If the abbreviation is widely used in the industry (e.g., "TransmissionControl Protocol / Internet Protocol" (TCP/IP)), you do not need to explainit, but you should consider giving a link for more context. *避免使用缩写和首字母缩写词。当您需要使用它们时，请对它们进行解释。如果该缩写在行业中被广泛使用（例如“ TransmissionControl协议/ Internet协议”（TCP / IP）），则无需进行解释，但应考虑提供链接以获取更多上下文。
* Code samples should be considered whenever they might be useful.  Providing an example can often make patterns clearer.  We recommend an example of APIfor every top level API element (e.g., class). *只要有可能，就应考虑代码示例。提供示例通常可以使模式更清晰。我们为每个顶级API元素（例如，类）推荐一个API示例。
* It should be clear how to use your API from the comments.  *从注释中应该清楚如何使用您的API。
  * Consider writing examples as separate programs and linking to them, but be careful about stale links in docs. *考虑将示例作为单独的程序编写并链接至它们，但请注意文档中的陈旧链接。
  * Examples should all compile and run.  *示例应全部编译并运行。
* When someone who has read the docs asks a question that should be answered by the docs, improve the docs. *阅读过文档的人提出应由文档回答的问题时，请改进文档。
* If the documentation is very obvious from context, then err on the side of brevity.  The Don't Repeat Yourself (DRY) principle applies.  The following isnot useful, because it repeats the same information twice: *如果从上下文的角度来看文档很明显，那么简短起见是错误的。请勿重复使用（DRY）原则。以下内容无用，因为它会重复两次相同的信息：

``` java
 /**
  * Returns an instance of Foo.
  * @return an instance of Foo.
  */
 public Foo getFoo() { ... }
```
 

 
* Similarly, if the comment is very obvious, avoid making it.  If, for example, a property is guaranteed by the type system, you do not need to document itseparately.  However, bear in mind that your API description should be enoughto enable an independent implementation. *同样，如果评论非常明显，请避免发表评论。例如，如果属性由类型系统保证，则无需单独记录其属性。但是，请记住，您的API描述应足以启用独立的实现。
* Consider documenting performance considerations and resource consumption issues, but also remember that such issues are often implementation dependentand change over time, whereas the contract for your method will probablyremain the same.  Consider including this information in implementation notes/ release notes instead. *考虑记录性能注意事项和资源消耗问题，但也请记住，此类问题通常与实现有关，并且会随时间而变化，而您的方法的合同可能会保持不变。考虑改为将此信息包含在实施说明/发行说明中。
* Similarly, consider avoiding documenting features that may change over time, unless you specifically call out that feature may change over time.  The moreyou prescribe, the less flexibility you give to future maintainers.  However,recognize that it might not matter, since your users will depend on everybehavior.  See also [Hyrum's Law](http://www.hyrumslaw.com/). *同样，请考虑避免记录可能随时间变化的功能，除非您特别指出该功能可能随时间变化。您开的越多，给未来维护者的灵活性就越差。但是，请意识到这可能无关紧要，因为您的用户将取决于每种行为。另请参见[希律定律]（http://www.hyrumslaw.com/）。

