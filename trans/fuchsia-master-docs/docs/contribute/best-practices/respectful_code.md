 
# Respectful Code  尊敬的代码 

Inclusivity is central to Fuchsia's culture, and our values include treating each other with dignity. As such, it’s important that everyone can contributewithout facing the harmful effects of bias and discrimination.  However, termsin our codebase, UIs, and documentation can perpetuate that discrimination.This document sets forth guidance which aims to address disrespectfulterminology in code and documentation. 包容性是紫红色文化的核心，我们的价值观包括尊严地对待彼此。因此，重要的是每个人都应在面对偏见和歧视的有害影响的情况下做出贡献。但是，我们的代码库，UI和文档中的术语可以使这种歧视永久化。本文档提出了旨在解决代码和文档中不尊重的术语的指南。

 
## Policy  政策 

Terminology that is derogatory, hurtful, or perpetuates discrimination, either directly or indirectly, should be avoided. 应避免直接或间接地贬损，伤害或永久性歧视的术语。

 
## What is in scope for this policy?  此政策的范围是什么？ 

Anything that a contributor would read while working on Fuchsia, including:  投稿者在研究紫红色时会读到的所有内容，包括：

 
- Names of variables, types, functions, files, build rules, binaries, exported variables, ... -变量名称，类型，函数，文件，构建规则，二进制文件，导出的变量，...
- Test data  - 测试数据
- System output and displays  -系统输出和显示
- Documentation (both inside and outside of source files)  -文档（在源文件的内部和外部）
- Commit messages  -提交消息

 
## Principles  原则 

 
- Be respectful: Derogatory language shouldn’t be necessary to describe how things work. -尊重他人：描述事物的运作方式时，不必使用贬义的语言。
- Respect culturally sensitive language:  Some words may carry significant historical or political meanings.  Please be mindful of this and usealternatives. -尊重文化敏感的语言：某些单词可能带有重大的历史或政治含义。请注意这一点和替代方法。

 
## How do I know if particular terminology is OK or not?  我怎么知道特定术语是否正确？ 

Apply the principles above.  If you have any questions, you can reach out to fuchsia-community-managers@google.com. 应用上述原理。如有任何疑问，请联系fuchsia-community-managers@google.com。

 
## What are examples of terminology to be avoided?  应避免哪些术语示例？ 

This list is NOT meant to be comprehensive.  It contains a few examples that people have run into frequently. 此列表并不意味着全面。它包含了一些人们经常遇到的例子。

| Term      | Suggested alternatives                                        | | --------- | ------------------------------------------------------------- || master    | primary, controller, leader, host                             || slave     | replica, subordinate, secondary, follower, device, peripheral || whitelist | allowlist, exception list, inclusion list                     || blacklist | denylist, blocklist, exclusion list                           || insane    | unexpected, catastrophic, incoherent                          || sane      | expected, appropriate, sensible, valid                        || crazy     | unexpected, catastrophic, incoherent                          || redline   | priority line, limit, soft limit                              | |条款|建议的替代品| --------- | -------------------------------------------------- ----------- ||大师主，控制器，领导者，主机||奴隶复制品，下属，次要，关注者，设备，外围设备||白名单|允许列表，例外列表，包含列表||黑名单|拒绝列表，阻止列表，排除列表||疯了意外的，灾难性的，不连贯的理智|预期，适当，明智，有效||疯狂意外的，灾难性的，不连贯的红线|优先线，限制，软限制|

 
## What if I am interfacing with something that violates this policy?  如果我遇到违反此政策的行为该怎么办？ 

This circumstance has come up a few times, particularly for code implementing specifications.  In these circumstances, differing from the language in thespecification may interfere with the ability to understand the implementation.For these circumstances, we suggest one of the following, in order of decreasingpreference: 这种情况已经出现了好几次，特别是对于实现规范的代码。在这种情况下，与规范中使用的语言不同可能会干扰理解实现的能力。对于这些情况，我们建议按以下降序排列以下之一：

 
1. If using alternate terminology doesn't interfere with understanding, use alternate terminology. 1.如果使用替代术语不会干扰理解，请使用替代术语。
