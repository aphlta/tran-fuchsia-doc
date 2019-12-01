 
# Working across different petals  跨不同的花瓣工作 

 
## Hard and Soft Transitions  硬过渡和软过渡 

Because it is not possible to atomically commit a change to multiple Git repositories at once, coordinating changes that affect multiple petals - forexample, an API or ABI change in the Fuchsia tree that affects callers in Topazor Experiences - requires either a soft or hard transition. 因为不可能一次原子地将更改提交给多个Git存储库，所以要协调影响多个花瓣的更改（例如，紫红色树中的API或ABI更改会影响Topazor Experiences中的调用方）需要软或硬过渡。

 
### Terminology:  术语： 

 
* *D* - A project used in the Fuchsia tree.  * * D *-紫红色树中使用的项目。
* *P* - Another project used in the Fuchsia tree with a direct dependency on `D`. For example, `D` might be Fuchsia, and `P` might be Topaz or Experiences. * * P *-在紫红色的树中使用的另一个项目，直接依赖于`D`。例如，“ D”可能是紫红色，而“ P”可能是黄玉或Experiences。
* *integration* - The internal integration repository.  * * integration *-内部集成存储库。

 
### Soft transitions (preferred)  软过渡（首选） 

The preferred way to make changes that span multiple projects is to use a *soft transition*. In a soft transition, you make a change to `D` in such away that the interface supports both old and new clients. For example, if youare replacing a function, you might add the new version and turn the oldfunction into a wrapper for the new function. 进行跨多个项目的更改的首选方法是使用“软过渡”。在一个软过渡中，您对D进行了更改，以使该界面同时支持新旧客户端。例如，如果要替换功能，则可以添加新版本并将旧功能转换为新功能的包装。

Use the following steps to land a soft transition:  使用以下步骤进行软过渡：

 
1. Land the change in `D` that introduces the new interface without breaking the old interface used by `P`. 1.在“ D”中找到引入新接口的更改，而不会破坏“ P”所使用的旧接口。
1. Wait for the new revision of `D` to roll into the integration repository.  1.等待新的`D`版本进入集成库。
1. Migrate `P` to use the new interface.  1.迁移“ P”以使用新界面。
1. Wait for the new revision of `P` to roll into the integration repository.  1.等待新的`P`版本进入集成库。
1. Land a cleanup change in `D` to remove the old interface.  1.在“ D”中进行清理更改以删除旧界面。

 
### Hard transitions  艰难的过渡 

For some changes, creating a soft transition can be difficult or impossible. For those changes, you can make a *hard transition*. In a hard transition, you makea breaking change to `D` and update `P` manually. 对于某些更改，创建软过渡可能很困难或不可能。对于这些更改，您可以进行“硬过渡”。在艰难的过渡中，您要对D做出重大更改并手动更新P。

Note that to prevent accidental clobbering of the manifest contents, Gerrit is configured to not automatically rebase changes that edit a manifest file. Youmust manually rebase before merging so that your submit is a pure fast-forward. 请注意，为防止清单内容的意外破坏，Gerrit配置为不自动对编辑清单文件的更改进行基准调整。在合并之前，您必须手动进行基准调整，以便您提交的文件是纯快进的。

Making a hard transition is more stressful than making a soft transition because your change will be preventing other changes in 'D' from becoming available independent projects between steps 1 and 2. 进行硬过渡要比进行软过渡更为压力，因为您的更改将阻止在步骤1和2之间将'D'中的其他更改变为可用的独立项目。

Only Google developers can make hard transitions.  See internal documentation for instructions. 只有Google开发人员可以进行艰难的过渡。有关说明，请参阅内部文档。

