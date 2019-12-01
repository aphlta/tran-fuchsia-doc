 
# Runtime Lock Validation in Zircon and Fuchsia  锆石和紫红色中的运行时锁定验证 

 
## Introduction  介绍 

Lock validation is a technique for checking the consistency of locking behavior in a program to find potential deadlock hazards. This document discussesrelevant aspects of the static and dynamic approaches to lock validation andpresents the foundation for the runtime lock validation library available inZircon and Fuchsia. 锁定验证是一种用于检查程序中锁定行为的一致性以发现潜在死锁危险的技术。本文档讨论了锁定验证的静态和动态方法的相关方面，并提供了Zircon和Fuchsia中可用的运行时锁定验证库的基础。

 
## Background  背景 

Lock validation may be performed either statically or dynamically. The following summarizes the important differences between static and dynamic approaches tolock validation: 锁验证可以静态或动态执行。以下总结了静态和动态锁验证方法之间的重要区别：

 
* When the validation is performed: compile time vs. run time.  *执行验证时：编译时间与运行时间。
* How effective the validator is at finding potential problems.  *验证者发现潜在问题的效率如何。
* What level of involvement is required by the programmer.  *程序员需要什么程度的参与。
* The overhead cost of the validation itself.  *验证本身的间接费用。

 
### Static Validation  静态验证 

Static validation is typically performed at compile time by analyzing the call graphs produced by the compiler or other source-level processor. With thisapproach it is necessary to instrument the code and locking primitives withannotations to inform the validator about which types represent locks and whichrules to apply (or not) to the code that uses the lock types. 静态验证通常是在编译时通过分析由编译器或其他源级处理器生成的调用图来执行的。使用这种方法，必须对代码和锁定原语进行批注，以通知验证程序哪些类型代表锁定，哪些规则适用于（或不适用）使用锁定类型的代码。

The benefits of static validation include early detection of issues at build time, deterministic validation results, and zero runtime overhead. Thiscombination of properties make it attractive to always enable static validation,ensuring that locking issues are often caught before code makes it into thebuild, without impacting the performance of the build artifacts. 静态验证的好处包括在构建时及早发现问题，确定性的验证结果以及零运行时间开销。属性的这种组合使得始终启用静态验证变得很有吸引力，从而确保了在代码进入构建之前通常会捕获锁定问题，而不会影响构建工件的性能。

Static validation also has some down sides. One problem is that static validation requires correct, consistent application of a variety of annotationsto both locks and code to provide useful results. This can cause maintenanceissues unless diligent code review standards are implemented. Another issue isthat static validation has limited visibility and can be fooled by conditionalpaths, dynamic dispatch, move semantics, and lock dependencies that spancompilation units. 静态验证也有一些缺点。一个问题是静态验证需要正确，一致地应用锁和代码的各种注释，以提供有用的结果。除非实施了严格的代码审查标准，否则这可能导致维护问题。另一个问题是静态验证的可见性有限，并且可以被跨越编译单元的条件路径，动态调度，移动语义和锁定依赖项所欺骗。

 
### Dynamic Validation  动态验证 

Dynamic validation is performed online at runtime by observing the relationships between locks as the code executes. With this approach it is generallysufficient to instrument just the locking primitives and acquire/releaseoperations to provide the information required for validation. 通过在代码执行时观察锁之间的关系，在运行时在线执行动态验证。使用这种方法，通常仅检测锁定原语和获取/释放操作以提供验证所需的信息就足够了。

The benefits of dynamic validation include simpler instrumentation (from the user's perspective) and potentially greater visibility into the actual runtimebehavior of the program. This makes dynamic validation useful in large codebases, where it may not be possible for static validation to see the fullset of possible lock interactions. 动态验证的好处包括更简单的检测（从用户的角度来看）以及潜在地更大程度地了解程序的实际运行时行为。这使得动态验证在大型代码库中非常有用，在大型代码库中，静态验证可能无法看到可能的锁交互的完整集合。

The main downsides of dynamic validation are runtime overhead and execution coverage requirements. Because dynamic validation must track lock interactionsat runtime, each acquire and release incurs a non-zero execution cost to updatetracking data, in addition to the memory overhead of the tracking data itself.Runtime tracking also has the consequence that code paths that are not executedcannot be analyzed by the validator. This may increase the burden on thedeveloper and QA to ensure sufficient execution coverage if that is not alreadya project requirement. 动态验证的主要缺点是运行时开销和执行覆盖范围要求。由于动态验证必须在运行时跟踪锁交互，因此除跟踪数据本身的内存开销外，每次获取和释放都会导致更新跟踪数据的执行成本为非零。运行时跟踪还导致无法执行未执行的代码路径由验证者分析。如果这还不是项目要求，则这可能会增加开发人员和质量保证人员的负担，以确保足够的执行覆盖范围。

 

 
### Locking Ordering Invariant  锁定顺序不变式 

The job of the lock validator is to determine whether or not the lock invariants of the program hold. The primary invariant is the order between two or morelocks: all paths in a program that acquire two or more locks must do so in anorder consistent with every other path involving two or more of the same locks toavoid the potential for deadlock. Environments that deal with hardwareinterrupts, such as embedded systems and kernels, have an additional orderinginvariant to avoid interrupt-induced deadlocks. These invariants are illustratedin the following subsections. 锁验证器的工作是确定程序的锁不变式是否成立。主要不变性是两个或多个锁之间的顺序：程序中获取两个或两个以上锁的所有路径的顺序必须与包含两个或多个相同锁的其他路径一致，以避免潜在的死锁。处理硬件中断的环境（例如嵌入式系统和内核）具有附加的排序不变性，以避免中断引起的死锁。在以下小节中将说明这些不变量。

 
##### Basic Inversion  基本反转 

The simplest form of inversion occurs when a program has two locks that are both acquired sequentially with inconsistent orders in different paths. 当程序具有两个锁，两个锁都在不同路径中以不一致的顺序顺序获取时，就会发生最简单的反转形式。

For example, a program with the locks **A** and **B** and code paths **P<sub>1</sub>** and **P<sub>2</sub>** and the following behavior has thepotential for deadlock: 例如，一个程序具有锁** A **和** B **以及代码路径** P <sub> 1 </ sub> **和** P <sub> 2 </ sub> **和以下行为可能会导致死锁：

Path **P<sub>1</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 1 </ sub> **获取并释放序列中的锁：

 
1. Acquire(**A**)  1.获取（** A **）
2. Acquire(**B**)  2.取得（** B **）
3. Release(**B**)  3.释放（** B **）
4. Release(**A**)  4.发布（** A **）

Path **P<sub>2</sub>** acquires and releases the locks in the inverted sequence:  路径** P <sub> 2 </ sub> **以相反的顺序获取并释放锁：

 
1. Acquire(**B**)  1.取得（** B **）
2. Acquire(**A**)  2.获取（** A **）
3. Release(**A**)  3.发布（** A **）
4. Release(**B**)  4.释放（** B **）

With the right interleaving, perhaps due to both paths executing concurrently on different threads, a deadlock occurs when path **P<sub>1</sub>** holds lock**A** and blocks waiting for lock **B**, while path **P<sub>2</sub>** holds lock**B** and blocks waiting for lock **A**. 如果进行正确的交织，可能是由于两条路径同时在不同的线程上执行，因此当路径** P <sub> 1 </ sub> **持有锁** A **并阻塞等待锁** B *时会发生死锁*，而路径** P <sub> 2 </ sub> **持有锁** B **并阻止等待锁** A **。

 
##### Circular Dependency  循环依赖 

Inversion may also occur between more than two locks and paths. This kind of inversion is much harder to recognize through manual inspection because eachpair of locks involved may appear to be correctly ordered in every path involvingjust the pairs, and yet a potential deadlock may still exist given overallordering of the locks. 在两个以上的锁和路径之间也可能发生反转。通过人工检查很难识别这种类型的反转，因为所涉及的每对锁似乎在涉及该对的每个路径中似乎都正确排序，但是考虑到锁的整体排序，可能仍然存在潜在的死锁。

For example, a program with the locks **A**, **B**, and **C**; paths **P<sub>1</sub>**, **P<sub>2</sub>**, and **P<sub>3</sub>**; with the followingbehavior has the potential for deadlock: 例如，一个带有锁** A **，** B **和** C **的程序；路径** P <sub> 1 </ sub> **，** P <sub> 2 </ sub> **和** P <sub> 3 </ sub> **;具有以下行为的行为可能会导致死锁：

Path **P<sub>1</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 1 </ sub> **获取并释放序列中的锁：

 
1. Acquire(**A**)  1.获取（** A **）
2. Acquire(**B**)  2.取得（** B **）
3. Release(**B**)  3.释放（** B **）
4. Release(**A**)  4.发布（** A **）

Path **P<sub>2</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 2 </ sub> **获取并释放序列中的锁：

 
1. Acquire(**B**)  1.取得（** B **）
2. Acquire(**C**)  2.取得（** C **）
3. Release(**C**)  3.发布（** C **）
4. Release(**B**)  4.释放（** B **）

Path **P<sub>3</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 3 </ sub> **按顺序获取并释放锁：

 
1. Acquire(**C**)  1.取得（** C **）
2. Acquire(**A**)  2.获取（** A **）
3. Release(**A**)  3.发布（** A **）
4. Release(**C**)  4.发布（** C **）

With the right interleaving of paths **P<sub>1</sub>**, **P<sub>2</sub>**, and **P<sub>3</sub>** a deadlock occurs as each path acquires the lock at thefirst step and waits for the lock at the second step. In practice this situationmay be compounded by the existence of many different paths that produce the samepairwise lock sequences. 如果路径** P <sub> 1 </ sub> **，** P <sub> 2 </ sub> **和** P <sub> 3 </ sub> **正确交错，则死锁当每个路径在第一步获取锁并在第二步等待锁时，会发生这种情况。实际上，这种情况可能会因存在许多产生相同的成对锁定序列的不同路径而变得更加复杂。

 
##### IRQ-Safe Ordering  IRQ安全订购 

In systems that deal with hardware interrupts the ordering between irq-safe and non-irq-safe locks is critical: a non-irq-safe lock must never be acquired whileholding an irq-safe lock to prevent indirect lock inversions. Irq-safe lockspreserve ordering between irq and non-irq context; a consistent order of two ormore irq-safe locks is guaranteed to be safe for paths running in both irq andnon-irq context. The same is not true for non-irq-safe locks. The reason for thisis that non-irq-safe locks permit irq handlers to effectively insert the locksacquired by the handler at arbitrary points in the interrupted task's locksequences. 在处理硬件中断的系统中，irq-安全锁和非irq-安全锁之间的顺序很重要：在持有irq-安全锁的同时，绝不能获取非irq-安全锁，以防止间接锁倒置。 Irq安全锁保留irq和非irq上下文之间的顺序；对于在irq和non-irq上下文中运行的路径，保证两个或多个irq安全锁的一致顺序是安全的。对于非irq安全锁，情况并非如此。这样做的原因是非irq安全锁允许irq处理程序有效地将处理程序获取的锁插入到中断任务的锁序列中的任意点。

For example, a system with non-irq-safe lock **A** and irq-safe lock **B<sub>irq</sub>**; paths **P<sub>1</sub>**, **P<sub>2</sub>**, and irq path**P<sub>irq</sub>**; with the following behavior has the potential for deadlock: 例如，具有非irq安全锁** A **和irq安全锁** B <sub> irq </ sub> **的系统；路径** P <sub> 1 </ sub> **，** P <sub> 2 </ sub> **和irq路径** P <sub> irq </ sub> **;具有以下行为的潜在死锁：

Path **P<sub>1</sub>** on **CPU1** acquires and releases the lock in sequence:  ** CPU1 **上的路径** P <sub> 1 </ sub> **依次获取并释放锁：

 
1. Acquire(**A**)  1.获取（** A **）
2. _**P<sub>irq</sub>** interrupts here on **CPU1**_  2. _ ** P <sub> irq </ sub> **在** CPU1 ** _处中断
3. Release(**A**)  3.发布（** A **）

Path **P<sub>irq</sub>** on **CPU1** acquires and releases the lock in sequence:  ** CPU1 **上的路径** P <sub> irq </ sub> **依次获取并释放锁：

 
1. Acquire(**B<sub>irq</sub>**)  1.获取（** B <sub> irq </ sub> **）
2. Release(**B<sub>irq</sub>**)  2.发布（** B <sub> irq </ sub> **）

Path **P<sub>2</sub>** on **CPU2** acquires and releases the locks in sequence:  ** CPU2 **上的路径** P <sub> 2 </ sub> **依次获取并释放锁：

 
1. Acquire(**B<sub>irq</sub>**)  1.获取（** B <sub> irq </ sub> **）
2. Acquire(**A**)  2.获取（** A **）
3. Release(**A**)  3.发布（** A **）
4. Release(**B<sub>irq</sub>**)  4.发布（** B <sub> irq </ sub> **）

With the right interleaving of paths **P<sub>1</sub>**, **P<sub>2</sub>**, and **P<sub>irq</sub>** a deadlock occurs as **P<sub>irq</sub>** attempts to acquire**B<sub>irq</sub>** while **P<sub>2</sub>** holds **B<sub>irq</sub>** and blockswaiting for **A**. This is an indirect lock inversion: **P<sub>irq</sub>**effectively inserts an acquire/release sequence of **B<sub>irq</sub>** in themiddle of the acquire/release sequence of **A** in path **P<sub>1</sub>**, whichis inconsistent with the lock sequence for the same locks in path**P<sub>2</sub>**. 如果路径** P <sub> 1 </ sub> **，** P <sub> 2 </ sub> **和** P <sub> irq </ sub> **正确交错，则死锁发生在** P <sub> irq </ sub> **试图获取** B <sub> irq </ sub> **而** P <sub> 2 </ sub> **持有** B < sub> irq </ sub> **并等待** A **。这是一种间接锁定反转：** P <sub> irq </ sub> **有效地在** B <sub> irq </ sub> **的获取/释放序列中间插入一个获取/释放序列。 ** P <sub> 1 </ sub> **路径中的** A **，与路径** P <sub> 2 </ sub> **中相同锁的锁序列不一致。

 
### Performing Validation  执行验证 

The invariants discussed in the previous section can be validated using a finite directed graph. The directed graph tracks the identity and order of locks as theanalysis traverses the code paths. Such a graph can be built either by traversingthe call graphs generated by a compiler or source-level processor (staticanalysis) or by observing the ordering of locks during program execution (dynamicanalysis). This section introduce the process in abstract terms that apply toeither approach, in preparation for developing a concrete dynamic analysisstrategy later on. 上一节中讨论的不变量可以使用有限有向图进行验证。当分析遍历代码路径时，有向图将跟踪锁的身份和顺序。可以通过遍历由编译器或源级处理器生成的调用图（静态分析）或通过观察程序执行期间的锁顺序（动态分析）来构建这样的图。本节以抽象的方式介绍适用于这两种方法的过程，为以后开发具体的动态分析策略做准备。

In the most general terms, building a directed graph from a code path requires maintaining a list of actively held locks as the path is traversed: a noderepresenting a lock is added to the list whenever the lock is acquired andremoved from the list whenever the lock is released. In addition to maintainingthe active list, a directed edge is added to the graph from a vertex representingthe newly acquired lock to each vertex representing a lock already in the list. 用最一般的术语来说，从代码路径构建有向图需要在遍历路径时维护一个有效持有的锁的列表：只要获取了锁，代表锁的节点就会添加到列表中，并且每当锁被获取时就从列表中删除该锁。已发布。除了维护活动列表之外，从表示新获取的锁的顶点到表示列表中已经存在的锁的每个顶点将有向边添加到图形。

 
#### Basic Inversion Example  基本反演示例 

This section illustrates a directed graph approach to detect a basic two-lock inversion. 本节说明了一种有向图方法，用于检测基本的两锁反转。

Recall from the earlier example a program with the locks **A** and **B**; code paths **P<sub>1</sub>** and **P<sub>2</sub>**; and the following behavior: 从前面的示例中调用一个带有** A **和** B **锁的程序；代码路径** P <sub> 1 </ sub> **和** P <sub> 2 </ sub> **;和以下行为：

Path **P<sub>1</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 1 </ sub> **获取并释放序列中的锁：

 
1. Acquire(**A**)  1.获取（** A **）
2. Acquire(**B**)  2.取得（** B **）
3. Release(**B**)  3.释放（** B **）
4. Release(**A**)  4.发布（** A **）

Path **P<sub>2</sub>** acquires and releases the locks in the inverted sequence:  路径** P <sub> 2 </ sub> **以相反的顺序获取并释放锁：

 
1. Acquire(**B**)  1.取得（** B **）
2. Acquire(**A**)  2.获取（** A **）
3. Release(**A**)  3.发布（** A **）
4. Release(**B**)  4.释放（** B **）

 
##### Analysis of Path **P<sub>1</sub>**  路径** P <sub> 1 </ sub> **的分析 

Starting with path **P<sub>1</sub>** we define and update the directed graph.  从路径** P <sub> 1 </ sub> **开始，我们定义并更新了有向图。

Let **L<sub>1</sub>** be the ordered _active_ list of locks held by path **P<sub>1</sub>**. 令** L <sub> 1 </ sub> **为路径** P <sub> 1 </ sub> **拥有的锁的有序_active_列表。

Let **G** = (**V**, **E**) be the directed graph, having the set of vertices **V** representing observed locks and the set of directed edges between vertices**E**. 假设** G ** =（** V **，** E **）是有向图，其顶点集** V **代表观察到的锁定，顶点之间的有向边集** E * *。

Initial state:  初始状态：

| **L<sub>1</sub>** | **V** | **E** | |-------------------|-------|-------|| ()                | {}    | {}    | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ------- | ------- || （）| {} | {} |

After **P<sub>1</sub>** step 1:  在** P <sub> 1 </ sub> **步骤1之后：

| **L<sub>1</sub>** | **V**   | **E** | |-------------------|---------|-------|| (**A**)           | {**A**} | {}    | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | --------- | ------- || （** A **）| {** A **} | {} |

This step adds lock **A** to the active list and introduces a vertex for the same lock to the directed graph. Since there are no other locks in the activelist no edges are added. 此步骤将锁** A **添加到活动列表，并为有向图引入相同锁的顶点。由于活动列表中没有其他锁，因此不会添加任何边。

After **P<sub>1</sub>** step 2:  在** P <sub> 1 </ sub> **步骤2之后：

| **L<sub>1</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| (**A**, **B**)    | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （** A **，** B **）| {** A **，** B **} | {（** B **，** A **）} |

This step adds lock **B** to the active list and also introduces a corresponding vertex to the graph. This time the active list does contain a lock, so an edgefrom the new lock to the existing lock is added to the graph. This edgerepresents that lock **B** now _depends_ on lock **A** preceding it in anyother path that involves both locks. 此步骤将锁定** B **添加到活动列表，并且还将相应的顶点引入图形。这次活动列表确实包含一个锁，因此从新锁到现有锁的边添加到了图形中。这条边表示现在锁** B **依赖于锁** A **在其他涉及这两个锁的其他路径之前。

After **P<sub>1</sub>** step 3:  在** P <sub> 1 </ sub> **步骤3之后：

| **L<sub>1</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| (**A**)           | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （** A **）| {** A **，** B **} | {（** B **，** A **）} |

Lock **B** is removed from the active list. No updates to the graph.  锁** B **从活动列表中删除。没有更新图表。

After **P<sub>1</sub>** step 4:  在** P <sub> 1 </ sub> **步骤4之后：

| **L<sub>1</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| ()                | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （）| {** A **，** B **} | {（** B **，** A **）} |

Lock **A** is removed from the active list. No updates to the graph.  锁定** A **从活动列表中删除。没有更新图表。

 
##### Analysis of Path **P<sub>2</sub>**  路径** P <sub> 2 </ sub> **的分析 

Let **L<sub>2</sub>** be the active list of locks held by **P<sub>2</sub>**.  令** L <sub> 2 </ sub> **为** P <sub> 2 </ sub> **持有的活动锁的列表。

Initial state:  初始状态：

| **L<sub>2</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| ()                | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （）| {** A **，** B **} | {（** B **，** A **）} |

In this case the initial state is the final state from path **P<sub>1</sub>**.  在这种情况下，初始状态是路径** P <sub> 1 </ sub> **中的最终状态。

After **P<sub>2</sub>** step 1:  在** P <sub> 2 </ sub> **步骤1之后：

| **L<sub>2</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| (**B**)           | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （** B **）| {** A **，** B **} | {（** B **，** A **）} |

This step adds lock **B** to the active list. As there are no other locks in the active list no edges are added to the graph. Since **B** already has a vertex inthe graph there is also no change to **V**. 此步骤将锁** B **添加到活动列表。由于活动列表中没有其他锁，因此不会将任何边添加到图中。由于** B **在图中已经有一个顶点，因此** V **也没有变化。

After **P<sub>2</sub>** step 2:  在** P <sub> 2 </ sub> **步骤2之后：

| **L<sub>2</sub>** | **V**          | **E**                            | |-------------------|----------------|----------------------------------|| (**B**, **A**)    | {**A**, **B**} | {(**B**, **A**), (**A**, **B**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ---------------------- || （** B **，** A **）| {** A **，** B **} | {（** B **，** A **），（** A **，** B **）} |

This step adds lock **A** to the active list. Since this lock already has a vertex there is no change to **V**. However, because there is a lock in theactive list an edge from the new lock to the existing lock is added to thegraph. With this new edge the graph now forms a cycle between vertices **A** and**B**, indicating that ordering between these locks is not consistent betweenthe two paths considered thus far and that a potential deadlock exists. 此步骤将锁定** A **添加到活动列表。由于此锁已具有一个顶点，因此** V **不变。但是，由于活动列表中有一个锁，因此将从新锁到现有锁的边添加到图形中。有了这个新的优势，该图现在在顶点** A **和** B **之间形成一个循环，表明到目前为止，在所考虑的两条路径之间这些锁之间的顺序不一致，并且存在潜在的死锁。

 
#### Circular Dependency Example  循环依赖示例 

This section illustrates a directed graph approach to detect a circular dependency inversion using previously discussed example from the invariantssection. This illustration is somewhat abbreviated due to the similarity to theprevious illustration. 本节使用不变式部分中先前讨论的示例说明了有向图方法来检测循环依赖项反转。由于与先前的图示相似，因此该图示略为简化。

Consider a program with the locks **A**, **B**, and **C** and paths **P<sub>1</sub>**, **P<sub>2</sub>**, and **P<sub>3</sub>** and the followingbehavior: 考虑一个程序，其锁为** A **，** B **和** C **，路径为** P <sub> 1 </ sub> **，** P <sub> 2 </ sub > **和** P <sub> 3 </ sub> **以及以下行为：

Path **P<sub>1</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 1 </ sub> **获取并释放序列中的锁：

 
1. Acquire(**A**)  1.获取（** A **）
2. Acquire(**B**)  2.取得（** B **）
3. Release(**B**)  3.释放（** B **）
4. Release(**A**)  4.发布（** A **）

Path **P<sub>2</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 2 </ sub> **获取并释放序列中的锁：

 
1. Acquire(**B**)  1.取得（** B **）
2. Acquire(**C**)  2.取得（** C **）
3. Release(**C**)  3.发布（** C **）
4. Release(**B**)  4.释放（** B **）

Path **P<sub>3</sub>** acquires and releases the locks in the sequence:  路径** P <sub> 3 </ sub> **按顺序获取并释放锁：

 
1. Acquire(**C**)  1.取得（** C **）
2. Acquire(**A**)  2.获取（** A **）
3. Release(**A**)  3.发布（** A **）
4. Release(**C**)  4.发布（** C **）

 
##### Analysis of Path **P<sub>1</sub>**  路径** P <sub> 1 </ sub> **的分析 

Let **L<sub>1</sub>** be the ordered _active_ list of locks held by path **P<sub>1</sub>**. 令** L <sub> 1 </ sub> **为路径** P <sub> 1 </ sub> **拥有的锁的有序_active_列表。

Let **G** = (**V**, **E**) be the directed graph, having the set of vertices **V** representing observed locks and the set of directed edges between vertices**E**. 假设** G ** =（** V **，** E **）是有向图，其顶点集** V **代表观察到的锁定，顶点之间的有向边集** E * *。

Initial state:  初始状态：

| **L<sub>1</sub>** | **V** | **E** | |-------------------|-------|-------|| ()                | {}    | {}    | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ------- | ------- || （）| {} | {} |

After **P<sub>1</sub>** step 1:  在** P <sub> 1 </ sub> **步骤1之后：

| **L<sub>1</sub>** | **V**   | **E** | |-------------------|---------|-------|| (**A**)           | {**A**} | {}    | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | --------- | ------- || （** A **）| {** A **} | {} |

 

After **P<sub>1</sub>** step 2:  在** P <sub> 1 </ sub> **步骤2之后：

| **L<sub>1</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| (**A**, **B**)    | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （** A **，** B **）| {** A **，** B **} | {（** B **，** A **）} |

 

After **P<sub>1</sub>** step 3:  在** P <sub> 1 </ sub> **步骤3之后：

| **L<sub>1</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| (**A**)           | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （** A **）| {** A **，** B **} | {（** B **，** A **）} |

 

After **P<sub>1</sub>** step 4:  在** P <sub> 1 </ sub> **步骤4之后：

| **L<sub>1</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| ()                | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （）| {** A **，** B **} | {（** B **，** A **）} |

 
##### Analysis of Path **P<sub>2</sub>**  路径** P <sub> 2 </ sub> **的分析 

Let **L<sub>2</sub>** be the ordered _active_ list of locks held by path **P<sub>2</sub>**. 令** L <sub> 2 </ sub> **为路径** P <sub> 2 </ sub> **持有的锁的有序_active_列表。

Initial state:  初始状态：

| **L<sub>2</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| ()                | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （）| {** A **，** B **} | {（** B **，** A **）} |

 

After **P<sub>2</sub>** step 1:  在** P <sub> 2 </ sub> **步骤1之后：

| **L<sub>2</sub>** | **V**          | **E**            | |-------------------|----------------|------------------|| (**B**)           | {**A**, **B**} | {(**B**, **A**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ---------------- | ------------ ------ || （** B **）| {** A **，** B **} | {（** B **，** A **）} |

After **P<sub>2</sub>** step 2:  在** P <sub> 2 </ sub> **步骤2之后：

| **L<sub>2</sub>** | **V**                 | **E**                            | |-------------------|-----------------------|----------------------------------|| (**B**, **C**)    | {**A**, **B**, **C**} | {(**B**, **A**), (**C**, **B**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ----------------------- || ----- ----------------------------- || （** B **，** C **）| {** A **，** B **，** C **} | {（** B **，** A **），（** C **，** B **）} |

This step adds lock **C** to the active list and also introduces a corresponding vertex to the graph. The active list contains the lock **B**, so an edge is addedfrom **C** to **B**. 此步骤将锁定** C **添加到活动列表，并且还将相应的顶点引入图形。活动列表包含锁** B **，因此会将一条边从** C **添加到** B **。

After **P<sub>2</sub>** step 3:  在** P <sub> 2 </ sub> **步骤3之后：

| **L<sub>2</sub>** | **V**                 | **E**                            | |-------------------|-----------------------|----------------------------------|| (**B**)           | {**A**, **B**, **C**} | {(**B**, **A**), (**C**, **B**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ----------------------- || ----- ----------------------------- || （** B **）| {** A **，** B **，** C **} | {（** B **，** A **），（** C **，** B **）} |

 

After **P<sub>2</sub>** step 4:  在** P <sub> 2 </ sub> **步骤4之后：

| **L<sub>2</sub>** | **V**                 | **E**                            | |-------------------|-----------------------|----------------------------------|| ()                | {**A**, **B**, **C**} | {(**B**, **A**), (**C**, **B**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | ----------------------- || ----- ----------------------------- || （）| {** A **，** B **，** C **} | {（** B **，** A **），（** C **，** B **）} |

 
##### Analysis of Path **P<sub>3</sub>**  路径** P <sub> 3 </ sub> **的分析 

Let **L<sub>3</sub>** be the ordered _active_ list of locks held by path **P<sub>3</sub>**. 令** L <sub> 3 </ sub> **为路径** P <sub> 3 </ sub> **持有的锁的有序_active_列表。

Initial state:  初始状态：

| **L<sub>3</sub>** | **V**                 | **E**                            | |-------------------|-----------------------|----------------------------------|| ()                | {**A**, **B**, **C**} | {(**B**, **A**), (**C**, **B**)} | | ** L <sub> 3 </ sub> ** | ** V ** | ** E ** | | ------------------- | ----------------------- || ----- ----------------------------- || （）| {** A **，** B **，** C **} | {（** B **，** A **），（** C **，** B **）} |

 

After **P<sub>3</sub>** step 1:  在** P <sub> 3 </ sub> **步骤1之后：

| **L<sub>3</sub>** | **V**                 | **E**                            | |-------------------|-----------------------|----------------------------------|| (**C**)           | {**A**, **B**, **C**} | {(**B**, **A**), (**C**, **B**)} | | ** L <sub> 3 </ sub> ** | ** V ** | ** E ** | | ------------------- | ----------------------- || ----- ----------------------------- || （** C **）| {** A **，** B **，** C **} | {（** B **，** A **），（** C **，** B **）} |

After **P<sub>3</sub>** step 2:  在** P <sub> 3 </ sub> **步骤2之后：

| **L<sub>3</sub>** | **V**                 | **E**                                            | |-------------------|-----------------------|--------------------------------------------------|| (**C**, **A**)    | {**A**, **B**, **C**} | {(**B**, **A**), (**C**, **B**), (**A**, **C**)} | | ** L <sub> 3 </ sub> ** | ** V ** | ** E ** | | ------------------- | ----------------------- || ----- --------------------------------------------- || （** C **，** A **）| {** A **，** B **，** C **} | {（** B **，** A **），（** C **，** B **），（** A **，** C **）} |

This step adds lock **A** to the active list. The active list contains the lock **C**, so an edge is added from **A** to **C**. With this new edge the graph nowforms a cycle in the vertices (**A**, **B**, **C**), indicating a circulardependency and the potential for deadlock if paths **P<sub>1</sub>**,**P<sub>2</sub>**, and **P<sub>3</sub>** are interleaved in the right way. 此步骤将锁定** A **添加到活动列表。活动列表包含锁** C **，因此会将一条边从** A **添加到** C **。有了这个新的优势，该图现在在顶点（** A **，** B **，** C **）中形成一个循环，表示循环相关性，并且如果路径** P <sub> 1 < / sub> **，** P <sub> 2 </ sub> **和** P <sub> 3 </ sub> **以正确的方式交错。

 
#### IRQ-Safe Ordering Example  IRQ-Safe订购示例 

This section illustrates a directed graph approach to detect irq-safe order violations using the previously discussed example from the invariants section. 本节说明了使用不变式部分中先前讨论的示例来检测irq-安全订单违规的有向图方法。

Recall the example system with non-irq-safe lock **A** and irq-safe lock **B<sub>irq</sub>**; paths **P<sub>1</sub>**, **P<sub>2</sub>**, and irq path**P<sub>irq</sub>**; with the following behavior: 回顾具有非irq安全锁** A **和irq安全锁** B <sub> irq </ sub> **的示例系统；路径** P <sub> 1 </ sub> **，** P <sub> 2 </ sub> **和irq路径** P <sub> irq </ sub> **;具有以下行为：

Path **P<sub>1</sub>** acquires and releases the lock in sequence:  路径** P <sub> 1 </ sub> **依次获取并释放锁：

 
1. Acquire(**A**)  1.获取（** A **）
2. Release(**A**)  2.发布（** A **）

Path **P<sub>irq</sub>** acquires and releases the lock in sequence:  路径** P <sub> irq </ sub> **依次获取并释放锁：

 
1. Acquire(**B<sub>irq</sub>**)  1.获取（** B <sub> irq </ sub> **）
2. Release(**B<sub>irq</sub>**)  2.发布（** B <sub> irq </ sub> **）

Path **P<sub>2</sub>** acquires and releases the locks in sequence:  路径** P <sub> 2 </ sub> **依次获取并释放锁：

 
1. Acquire(**B<sub>irq</sub>**)  1.获取（** B <sub> irq </ sub> **）
2. Acquire(**A**)  2.获取（** A **）
3. Release(**A**)  3.发布（** A **）
4. Release(**B<sub>irq</sub>**)  4.发布（** B <sub> irq </ sub> **）

 
##### Analysis of Path **P<sub>1</sub>**  路径** P <sub> 1 </ sub> **的分析 

Let **L<sub>1</sub>** be the ordered _active_ list of locks held by path **P<sub>1</sub>**. 令** L <sub> 1 </ sub> **为路径** P <sub> 1 </ sub> **拥有的锁的有序_active_列表。

Let **G** = (**V**, **E**) be the directed graph, having the set of vertices **V** representing observed locks and the set of directed edges between vertices**E**. 假设** G ** =（** V **，** E **）是有向图，其顶点集** V **代表观察到的锁定，顶点之间的有向边集** E * *。

Initial state:  初始状态：

| **L<sub>1</sub>** | **V** | **E** | |-------------------|-------|-------|| ()                | {}    | {}    | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | ------- | ------- || （）| {} | {} |

After **P<sub>1</sub>** step 1:  在** P <sub> 1 </ sub> **步骤1之后：

| **L<sub>1</sub>** | **V**   | **E** | |-------------------|---------|-------|| (**A**)           | {**A**} | {}    | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | --------- | ------- || （** A **）| {** A **} | {} |

After **P<sub>1</sub>** step 2:  在** P <sub> 1 </ sub> **步骤2之后：

| **L<sub>1</sub>** | **V**   | **E** | |-------------------|---------|-------|| ()                | {**A**} | {}    | | ** L <sub> 1 </ sub> ** | ** V ** | ** E ** | | ------------------- | --------- | ------- || （）| {** A **} | {} |

 
##### Analysis of Path **P<sub>irq</sub>**  路径** P <sub> irq </ sub> **的分析 

Let **L<sub>irq</sub>** be the ordered _active_ list of locks held by path **P<sub>irq</sub>**. 令** L <sub> irq </ sub> **为路径** P <sub> irq </ sub> **持有的锁的有序_active_列表。

Initial state:  初始状态：

| **L<sub>irq</sub>** | **V**   | **E** | |---------------------|---------|-------|| ()                  | {**A**} | {}    | | ** L <sub> irq </ sub> ** | ** V ** | ** E ** | | --------------------- | --------- | ------- || （）| {** A **} | {} |

After **P<sub>irq</sub>** step 1:  在** P <sub> irq </ sub> **步骤1之后：

| **L<sub>irq</sub>**   | **V**                        | **E** | |-----------------------|------------------------------|-------|| (**B<sub>irq</sub>**) | {**A**, **B<sub>irq</sub>**} | {}    | | ** L <sub> irq </ sub> ** | ** V ** | ** E ** | | ----------------------- | ------------------------- ----- | ------- || （** B <sub> irq </ sub> **）| {** A **，** B <sub> irq </ sub> **} | {} |

After **P<sub>irq</sub>** step 2:  在** P <sub> irq </ sub> **步骤2之后：

| **L<sub>irq</sub>** | **V**                        | **E** | |---------------------|------------------------------|-------|| ()                  | {**A**, **B<sub>irq</sub>**} | {}    | | ** L <sub> irq </ sub> ** | ** V ** | ** E ** | | --------------------- | --------------------------- --- | ------- || （）| {** A **，** B <sub> irq </ sub> **} | {} |

 
##### Analysis of Path **P<sub>irq</sub>**  路径** P <sub> irq </ sub> **的分析 

Let **L<sub>2</sub>** be the ordered _active_ list of locks held by path **P<sub>2</sub>**. 令** L <sub> 2 </ sub> **为路径** P <sub> 2 </ sub> **持有的锁的有序_active_列表。

Initial state:  初始状态：

| **L<sub>2</sub>** | **V**   | **E** | |-------------------|---------|-------|| ()                | {**A**} | {}    | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------- | --------- | ------- || （）| {** A **} | {} |

After **P<sub>2</sub>** step 1:  在** P <sub> 2 </ sub> **步骤1之后：

| **L<sub>2</sub>**     | **V**                        | **E** | |-----------------------|------------------------------|-------|| (**B<sub>irq</sub>**) | {**A**, **B<sub>irq</sub>**} | {}    | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ----------------------- | ------------------------- ----- | ------- || （** B <sub> irq </ sub> **）| {** A **，** B <sub> irq </ sub> **} | {} |

After **P<sub>2</sub>** step 2:  在** P <sub> 2 </ sub> **步骤2之后：

| **L<sub>2</sub>**            | **V**                        | **E**                          | |------------------------------|------------------------------|--------------------------------|| (**B<sub>irq</sub>**, **A**) | {**A**, **B<sub>irq</sub>**} | {(**A**, **B<sub>irq</sub>**)} | | ** L <sub> 2 </ sub> ** | ** V ** | ** E ** | | ------------------------------ | ------------------ ------------ | -------------------------------- || （** B <sub> irq </ sub> **，** A **）| {** A **，** B <sub> irq </ sub> **} | {（** A **，** B <sub> irq </ sub> **）} |

This step adds lock **A** to the active list. The active list contains lock **B<sub>irq</sub>**, so an edge is added from **A** to **B<sub>irq</sub>**.Because this is an edge from a non-irq-safe lock to an irq-safe lock the irq-safeordering invariant is violated and a potential deadlock exists. 此步骤将锁定** A **添加到活动列表。活动列表包含锁** B <sub> irq </ sub> **，因此从** A **到** B <sub> irq </ sub> **添加了一条边，因为这是一条边从非irq安全锁到irq安全锁，违反了irq安全排序不变式，并且存在潜在的死锁。

 
## From Theory to Implementation  从理论到实施 

This section develops a concrete strategy to implement a directed graph validator, based on the analysis techniques of the previous section. 本节根据上一节的分析技术，开发一种具体的策略来实现有向图验证器。

The implementation strategy has the following goals:  实施策略的目标如下：

 
1. Avoid dynamic allocation if possible.  1.尽可能避免动态分配。
2. Minimize the overhead of validation.  2.最小化验证的开销。
3. Support environments that manage hardware interrupts.  3.支持管理硬件中断的环境。

 
### Removing Redundancy with Lock Classes  使用锁类删除冗余 

In the analysis earlier in this document, locks are considered abstractly with the implication that the tracked objects are individual instances of locks.While tracking individual instances produces correct results, it has severalconsequences that might be avoided: 在本文档前面的分析中，锁被抽象地认为是被跟踪对象是锁的单个实例，尽管跟踪单个实例产生正确的结果，但有一些后果可以避免：

 
1. Tracking structures must be dynamically adjusted as lock instances come into and out of existence, possibly requiring dynamic allocation or otherper-instance data storage. 1.随着锁实例的出现和消失，必须动态调整跟踪结构，这可能需要动态分配或其他每个实例的数据存储。
2. The graph contains redundant information when multiple instances of locks are used identically by the same code paths. 2.当同一代码路径相同地使用多个锁实例时，该图包含冗余信息。
3. Relatedly, it may take longer to identify violations by locks that serve identical functions, but have not yet individually propagated through all ofthe necessary code paths. 3.相关地，通过具有相同功能但尚未通过所有必需的代码路径单独传播的锁来识别冲突可能需要更长的时间。

A key observation is that locks that serve identical functions should follow the same ordering rules, regardless of the number of instances. 一个关键的观察结果是，服务于相同功能的锁应遵循相同的排序规则，而不管实例的数量如何。

Consider the following types with lock members and an operation that mutates both types: 请考虑以下具有锁定成员的类型以及使这两种类型发生突变的操作：

```C++
struct Foo {
    Mutex lock;
    int data; GUARDED_BY(lock);
};

struct Bar {
    Mutex lock;
    int data; GUARDED_BY(lock);
};

void Swap(Foo* foo, Bar* bar) {
    foo->lock.Acquire();
    bar->lock.Acquire();

    int temp = foo->data;
    foo->data = bar->data;
    bar->data = temp;

    bar->Release();
    foo->Release();
}
```
 

Since operation `Swap` may operate on any instance of `Foo` and any instance of `Bar` it follows that `Swap` establishes an order between the locks of allinstances of `Foo` and `Bar`; failure to apply this order consistently in otherparts of a program could result in a deadlock when the same instances of `Foo`and `Bar` are locked concurrently in different orders. 由于操作“交换”可以在“ Foo”的任何实例和“ Bar”的任何实例上进行，因此，“交换”在“ Foo”和“ Bar”的所有实例的锁之间建立了顺序；如果相同的Foo和Bar实例同时以不同的顺序锁定，则未能在程序的其他部分中一致地应用此顺序可能会导致死锁。

Note that it is possible to intentionally or unintentionally segregate different collections of `Foo` and `Bar` such that instances locked in different ordersnever overlap. This is still dangerous however, because seemingly innocuouschanges to the inputs, structure, or timing of the program could defeat thesegregation and introduce a potential deadlock. This problem can be avoidedentirely by treating all instances of `Foo` and `Bar` equivalently and applyingthe same ordering rules throughout the program. 请注意，可以有意或无意地分隔“ Foo”和“ Bar”的不同集合，以使以不同顺序锁定的实例永远不会重叠。但是，这仍然很危险，因为对程序的输入，结构或时间安排看似无害的更改可能会破坏这些聚集并引入潜在的死锁。通过等效地处理“ Foo”和“ Bar”的所有实例并在整个程序中应用相同的排序规则，可以完全避免此问题。

Ensuring universal ordering throughout the program can be achieved by tracking classes of locks instead of lock instances: each lock member in each typerepresents a unique lock class. The relationships between each lock class canbe tracked and analyzed using the same directed graph techniques as withindividual locks. 通过跟踪锁的类而不是锁实例，可以确保整个程序的通用排序：每种类型的每个锁成员代表一个唯一的锁类。可以使用与单个锁内相同的有向图技术来跟踪和分析每个锁类之间的关系。

Tracking lock classes has the following benefits:  跟踪锁类具有以下优点：

 
1. Statically allocated memory: because all lock classes are known at compile time, tracking structures can be allocated up front as static global data. 1.静态分配的内存：由于所有锁类在编译时都是已知的，因此可以预先将跟踪结构分配为静态全局数据。
2. Elimination of redundant graph nodes: locks in the same class use the same tracking structures. 2.消除冗余图节点：同一类中的锁使用相同的跟踪结构。
3. Faster detection of invariant violations: violations are detected when lock class orders are inconsistent, even if the individual instances involvedhave never been used together. 3.更快地检测不变性违规：当锁类顺序不一致时，即使从未一起使用过涉及的各个实例，也会检测到违规。

 
#### Additional Ordering Rules  其他订购规则 

Tracking lock classes introduces additional ordering considerations when locking multiple locks of the same class. Because individual instances are not trackedit is necessary to take additional steps to ensure consistency when multiplelocks of the same class must be acquired at the same time. 当锁定同一类的多个锁时，跟踪锁类引入了其他排序注意事项。因为不需要单独的实例，所以在必须同时获取同一类的多个锁时，有必要采取额外的步骤来确保一致性。

 
##### Externally Ordered Locks  外部订购的锁 

Nesting locks of the same class is necessary when a hierarchical or other ordered data structure has locks in each node and more than one per-node lockmust be held at a time. In this situation the data structure or access patternmust provide a stable ordering that is used to guarantee ordering of the locks. 当层次结构或其他有序数据结构在每个节点中具有锁并且一次必须保留一个以上的每个节点锁时，必须使用同一类的嵌套锁。在这种情况下，数据结构或访问模式必须提供稳定的顺序，以保证锁的顺序。

Validation of nestable lock classes requires only that the external order is recorded in the active locks list for each nestable lock and compared when newlocks of the same class are added to the list. A consequence of this design isthat other lock classes may not be interspersed between nested locks of thesame class, only wholly before or after a collection of nested locks. 可嵌套锁类的验证仅要求将外部顺序记录在每个可嵌套锁的活动锁列表中，并在将相同类的新锁添加到列表时进行比较。这种设计的结果是，其他锁类不能仅散布在一组嵌套锁之前或之后，才散布在同一类的嵌套锁之间。

For example, non-nestable lock classes **A** and **B**, and nestable lock class **N** may be interspersed like this: 例如，非嵌套的锁类** A **和** B **和可嵌套的锁类** N **可以像这样散布：

**A**, **N<sub>0</sub>**, **N<sub>1</sub>**, ... **N<sub>n</sub>**, **B**  ** A **，** N <sub> 0 </ sub> **，** N <sub> 1 </ sub> **，... ** N <sub> n </ sub> ** ，** B **

But not like this:  但不是这样的：

**A**, **N<sub>0</sub>**, **B**, **N<sub>1</sub>**, ... **N<sub>n</sub>** or **A**, **N<sub>0</sub>**, **N<sub>1</sub>**, **B**, ... **N<sub>n</sub>** or... etc ** A **，** N <sub> 0 </ sub> **，** B **，** N <sub> 1 </ sub> **，... ** N <sub> n </ sub> **或** A **，** N <sub> 0 </ sub> **，** N <sub> 1 </ sub> **，** B **，... ** N <sub> n </ sub> **或...等

In most situations this is a reasonable constraint, as interspersing other locks within a nested structure with arbitrary depth is likely to result in inversionsas the structure is updated at runtime. On the other hand, in situations wherenesting is bounded to a few levels it may be more effective to define separatelock classes for each level instead of using a nested class -- in this caseother locks may be allowed at a specific level following normal lock orderingrules. 在大多数情况下，这是一个合理的约束，因为在运行时更新结构时，将其他锁散布在具有任意深度的嵌套结构中可能会导致反转。另一方面，在将嵌套限制在几个级别的情况下，为每个级别定义单独的锁类而不是使用嵌套类可能更有效-在这种情况下，可以按照常规锁排序规则在特定级别上允许其他锁。

 
##### Address Ordering  地址订购 

It is difficult to generalize lock ordering between locks of the same class without an externally provided order when the locks are acquired at differenttimes. It is possible however, to provide an ordering guarantee when acquiringmultiple locks at the same time, without temporal separation. In this situationthe locks may be ordered by address, guaranteeing that any path that acquiresthe same set locks produces a consistent locking order. 当在不同时间获取锁时，如果没有外部提供的顺序，很难归纳出同一类锁之间的锁顺序。但是，有可能在同时获取多个锁时提供排序保证，而不会造成时间间隔。在这种情况下，可以按地址对锁进行排序，从而确保获取同一组锁的任何路径都可以生成一致的锁顺序。

For example, consider an operation **F**(**S<sub>a</sub>**, **S<sub>b</sub>**) that operates on two instances of structure **S**, each with a lock of class**L** and, as part of the operation **F** must lock both locks. 例如，考虑对两个结构** S实例进行操作的操作** F **（** S <sub> a </ sub> **，** S <sub> b </ sub> **） **，每个都具有** L **类的锁，并且作为操作** F **的一部分，必须锁定两个锁。

If instance **S<usb>0</sub>** is ordered in memory before instance **S<sub>1</sub>** then the locks have the same relative ordering as theircontaining instances. We can consider the locks to have the subclasses**L<sub>0</sub>** and **L<sub>1</sub>** respectively. 如果在实例** S <sub> 1 </ sub> **之前在内存中对实例** S <usb> 0 </ sub> **进行了排序，则锁与包含实例的相对顺序相同。我们可以认为锁分别具有子类** L <sub> 0 </ sub> **和** L <sub> 1 </ sub> **。

A lock ordering problem arises if we perform the operation with different orders: 如果我们以不同的顺序执行操作，则会出现锁定顺序问题：

**F**(**S<sub>0</sub>**, **S<sub>1</sub>**) and **F**(**S<sub>1</sub>**, **S<sub>0</sub>**) ** F **（** S <sub> 0 </ sub> **，** S <sub> 1 </ sub> **）和** F **（** S <sub> 1 </ sub> **，** S <sub> 0 </ sub> **）

Without intervention these produce the inverted lock sequences:  在没有干预的情况下，它们会产生反向锁定序列：

**L<sub>0</sub>**, **L<sub>1</sub>** and **L<sub>1</sub>**, **L<sub>0</sub>**  ** L <sub> 0 </ sub> **，** L <sub> 1 </ sub> **和** L <sub> 1 </ sub> **，** L <sub> 0 < / sub> **

Since **F** has simultaneous access to both locks at the same time, it is possible to order the locks by address, resulting in a consistent locksequence regardless of the original order of the arguments. 由于** F **可以同时同时访问两个锁，因此可以按地址对锁进行排序，无论参数的原始顺序如何，都可以得到一致的锁序列。

Now suppose we add two more lock classes to the sequence: class **A** acquired before operation **F** and class **B** acquired after operation **F**. Theresulting lock sequence is: 现在，假设我们在序列中又添加了两个锁类：在操作** F **之前获得的** A **类和在操作** F **之后获得的** B **类。结果锁定顺序为：

**A**, **L<sub>0</sub>**, **L<sub>1</sub>**, **B**  ** A **，** L <sub> 0 </ sub> **，** L <sub> 1 </ sub> **，** B **

Note that this looks similar to the nested lock class sequence diagram in the previous section. It is in fact the same situation, only the ordering of locksis provided by address rather than an external order. This means that the samebookkeeping in the active threads list can be used for both situations. 请注意，这看起来与上一节中的嵌套锁类序列图相似。实际上是相同的情况，只是地址提供锁锁的顺序，而不是外部顺序。这意味着活动线程列表中的相同簿记可用于两种情况。

 
#### Lock Class Tracking Data Structure  锁类跟踪数据结构 

This section discusses implementation details for tracking lock classes and concrete processing techniques to detect potential deadlocks. 本节讨论用于跟踪锁类的实现细节以及用于检测潜在死锁的具体处理技术。

Each lock class has a statically allocated node in the directed graph representing all locks belonging to that class. Each node has the following datastructures: 每个锁类在有向图中有一个静态分配的节点，表示属于该类的所有锁。每个节点具有以下数据结构：

 
##### Lock-Free, Wait-Free Hash Set  无锁，无等待的哈希集 

Each lock class node has a hash set that tracks the edges from the lock class to the lock classes ordered before it. 每个锁类节点都有一个哈希集，该哈希集跟踪从锁类到在其之前排序的锁类的边缘。

**TODO**: Add implementation details of the hash set.  ** TODO **：添加哈希集的实现细节。

 
##### Lock-Free, Wait-Free Disjoint Set Structures  无锁，免等待的不交集集结构 

Each lock class node has a parent pointer used to track nodes that are connected in cycles in the directed graph. This permits reporting cycles that have beenpreviously by the loop detection algorithm without fully re-traversing the graph. 每个锁类节点都有一个父指针，该父指针用于跟踪有向图中循环连接的节点。这允许报告循环之前已由循环检测算法执行的循环，而无需完全重新遍历图形。

**TODO**: Add implementation details of the disjoint set structure.  ** TODO **：添加不相交集结构的实现细节。

 
##### Thread-Local Lock List  线程本地锁定列表 

Each thread maintains a thread-local list of the locks it currently holds.  每个线程维护其当前持有的锁的线程本地列表。

**TODO**: Add implementation details of the thread-local lock list.  ** TODO **：添加线程本地锁定列表的实现细节。

 
##### Loop Detection Thread  循环检测线程 

Whenever a new edge is added to the directed graph, the loop detection thread is triggered to traverse the graph to find circular dependencies involving more thantwo locks. Tarjan's strongly connected sets algorithm is an efficient choice,with worst case complexity of **O**(|**E**| + |**V**|). This algorithm is stableeven when traversing a graph that is updated concurrently by other threads. 每当将新边添加到有向图时，都会触发循环检测线程以遍历图以查找涉及两个以上锁的循环依赖关系。 Tarjan的强连接集算法是一种有效的选择，最坏情况下的复杂度为** O **（| ** E ** | + | ** V ** |）。即使遍历由其他线程同时更新的图形，该算法也是稳定的。

**TODO**: Add implementation details of the loop detection thread.  ** TODO **：添加循环检测线程的实现细节。

 
## References  参考文献 

 
1. Clang static [thread safety analysis](https://clang.llvm.org/docs/ThreadSafetyAnalysis.html).  1.静态Clang [线程安全分析]（https://clang.llvm.org/docs/ThreadSafetyAnalysis.html）。
2. LLVM runtime [thread sanitizer](https://github.com/google/sanitizers/wiki/ThreadSanitizerDeadlockDetector).  2. LLVM运行时[线程清理程序]（https://github.com/google/sanitizers/wiki/ThreadSanitizerDeadlockDetector）。
3. Linux Kernel [lockdep subsystem](https://www.kernel.org/doc/Documentation/locking/lockdep-design.txt).  3. Linux内核[lockdep子系统]（https://www.kernel.org/doc/Documentation/locking/lockdep-design.txt）。

