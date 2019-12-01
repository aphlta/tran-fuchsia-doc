 
# Contribute changes  贡献变化 

Fuchsia manages commits through Gerrit at [https://fuchsia-review.googlesource.com](https://fuchsia-review.googlesource.com). 紫红色通过[[https://fuchsia-review.googlesource.com]（https://fuchsia-review.googlesource.com）上的Gerrit管理提交。

To submit your contribution to the Fuchsia project, follow the instructions in the sections below.  要提交对Fuchsia项目的贡献，请遵循以下各节中的指示。

 
## Prerequisites  先决条件 

Before you submit your first contribution to the Fuchsia project, you need to [sign the Google Contributor License Agreements (CLA)](#sign-the-google-cla) and [generate a cookie to authenticate you in Gerrit](#generate-a-cookie). 在您向Fuchsia项目提交第一笔捐款之前，您需要[签署Google贡献者许可协议（CLA）]（sign-the-google-cla）和[生成Cookie以在Gerrit中对您进行身份验证]（generate-a-曲奇饼）。

 
### Sign the Google CLA {#sign-the-google-cla}  签署Google CLA {sign-the-google-cla} 

To sign the Google CLA, do the following:  要签署Google CLA，请执行以下操作：

 
1.  Go to the Google Developers' [Contributor License Agreements](https://cla.developers.google.com/) page.  1.转到Google开发者的[贡献者许可协议]（https://cla.developers.google.com/）页面。
1.  Sign the agreement on behalf of **Only Yourself** or **Your Employer**.  1.代表“仅您自己”或“您的雇主”签署协议。

 
### Generate a cookie {#generate-a-cookie}  生成Cookie {generate-a-cookie} 

To generate the cookie, do the following:  要生成cookie，请执行以下操作：

 
1.  Log into [Gerrit](https://fuchsia-review.googlesource.com).  1.登录[Gerrit]（https://fuchsia-review.googlesource.com）。
1.  At the top of [https://fuchsia.googlesource.com](https://fuchsia.googlesource.com), click **Generate Password**.  1.在[https://fuchsia.googlesource.com]（https://fuchsia.googlesource.com）的顶部，单击“生成密码” **。
1.  Copy the generated code and run it in a terminal of your workstation.  1.复制生成的代码，然后在工作站的终端中运行它。

 
## Create a Change in Gerrit {#create-a-change-in-gerrit}  在Gerrit中创建变更{create-a-change-in-gerrit} 

Follow these steps to create a Change in Gerrit:  请按照以下步骤创建Gerrit更改：

 
1.  Create a new branch:  1.创建一个新分支：

    ```
    git checkout -b <branch_name>

    ```
 
1.  Create or edit files in the new branch.  1.在新分支中创建或编辑文件。
1.  Add the changes:  1.添加更改：

    ```
    git add <files>
    ```
 
1.  Commit the changes (see [Add commit message tags](#add-commit-message-tags)):  1.提交更改（请参阅[添加提交消息标签]（add-commit-message-tags））：

    ```
    git commit
    ```
 

 
1.  Upload the changes to Gerrit:  1.将更改上传到Gerrit：

    ```
    jiri upload
    ```
 

 
    *   If you want to use the `git` command instead, run the following command: *如果要改用`git`命令，请运行以下命令：

        ```
        git push origin HEAD:refs/for/master
        ```
 

Note: If you want to upload the changes with a custom topic, see [Upload changes from multiple repositories](/docs/development/source_code/upload_changes_from_multiple_repositories.md) for details. 注意：如果要使用自定义主题上载更改，请参阅[从多个存储库上载更改]（/ docs / development / source_code / upload_changes_from_multiple_repositories.md）。

At any time, if you want to make changes to your patch, use `--amend`:  任何时候，如果您想对补丁进行更改，请使用`--amend`：

```
git commit --amend
```
 

Once the change is submitted, clean up the branch:  提交更改后，清理分支：

```
git branch -d <branch_name>
```
 

See the [Gerrit documentation](https://gerrit-documentation.storage.googleapis.com/Documentation/2.12.3/intro-user.html#upload-change) for more information.  有关更多信息，请参见[Gerrit文档]（https://gerrit-documentation.storage.googleapis.com/Documentation/2.12.3/intro-user.html上传更改）。

 
## Add commit message tags {#add-commit-message-tags}  添加提交消息标签{add-commit-message-tags} 

You must include `[tags]` in the subject of a commit message to indicate which module, library, and app are affected by your Change. 您必须在提交消息的主题中包含“ [tags]”，以指示哪个模块，库和应用受更改影响。

See the following example of a commit message, which shows the tags in the subject: 请参见以下提交消息示例，其中显示了主题中的标签：

```
[parent][component] Update component in Topaz.

<The details of the commit message here.>

Test: Added test X
```
 

For the tags, use `[docs]` for documentation, `[zircon]` for zircon, `[fidl]` for FIDL, and more. You can view the commit history of the files you've edited to check for the tags used previously.  对于标签，对文档使用`[docs]`，对锆石使用`[zircon]`，对FIDL使用`[fidl]`，等等。您可以查看已编辑文件的提交历史记录，以检查以前使用的标签。

See these examples:  请参阅以下示例：

 
*   [https://fuchsia-review.googlesource.com/c/zircon/+/112976](https://fuchsia-review.googlesource.com/c/zircon/+/112976)  * [https://fuchsia-review.googlesource.com/c/zircon/+/112976](https://fuchsia-review.googlesource.com/c/zircon/+/112976）
*   [https://fuchsia-review.googlesource.com/c/garnet/+/110795](https://fuchsia-review.googlesource.com/c/garnet/+/110795)  * [https://fuchsia-review.googlesource.com/c/garnet/+/110795](https://fuchsia-review.googlesource.com/c/garnet/+/110795）
*   [https://fuchsia-review.googlesource.com/c/peridot/+/113955](https://fuchsia-review.googlesource.com/c/peridot/+/113955)  * [https://fuchsia-review.googlesource.com/c/peridot/+/113955](https://fuchsia-review.googlesource.com/c/peridot/+/113955）
*   [https://fuchsia-review.googlesource.com/c/topaz/+/114013](https://fuchsia-review.googlesource.com/c/topaz/+/114013)  * [https://fuchsia-review.googlesource.com/c/topaz/+/114013](https://fuchsia-review.googlesource.com/c/topaz/+/114013）

Note: Gerrit flags your Change with `Needs Label: Commit-Message-has-tags` if the subject of the commit message doesn't include tags. 注意：如果提交消息的主题不包含标签，则Gerrit会使用“需要标签：Commit-Message-has-tags”标记您的更改。

 
## Add test instructions {#add-test-instructions}  添加测试说明{add-test-instructions} 

If a change requires non-obvious manual testing for validation, those testing steps should be described in a line in the change description beginning with`Test:`. 如果更改需要进行非显而易见的手动测试以进行验证，则应在更改描述的一行中以“ Test：”开头描述这些测试步骤。

If the instructions are more elaborate, they can be added to a linked bug. If the change does not intend to change behavior, the commit message shouldindicate as such. 如果说明更详尽，则可以将其添加到链接的错误中。如果更改不打算更改行为，则提交消息应这样指示。

In some cases, we are not able to test certain behavior changes because we lack some particular piece of infrastructure. In that case, we should have an issuein the tracker about creating that infrastructure and the test label shouldmention the bug number in addition to describing how the change was manuallytested: 在某些情况下，由于我们缺少某些特定的基础架构，因此我们无法测试某些行为更改。在这种情况下，除了描述如何手动测试更改之外，我们在跟踪器中还应考虑到有关创建该基础结构的问题，并且测试标签应指出错误号：

```
Test: Manually tested that [...]. Automated testing needs US-XXXX
```
 

Developers are responsible for high-quality automated testing of their code. Reviewers are responsible for pushing back on changes that do not includesufficient tests. 开发人员负责对其代码进行高质量的自动化测试。审阅者有责任推迟不包含充分测试的更改。

Note: See [Fuchsia testability rubrics](/docs/development/testing/testability_rubric.md) for more information on how to introduce testable and tested code in the Fuchsia project. 注意：有关如何在Fuchsia项目中引入可测试的代码的更多信息，请参见[Fuchsia可测试性规范]（/ docs / development / testing / testability_rubric.md）。

 
## Resolve merge conflicts {#resolve-merge-conflicts}  解决合并冲突{resolve-merge-conflicts} 

 
1.  Rebase from `origin/master`, which reveals the files that cause merge conflicts:  1.从`origin / master`重新建立基础，它揭示了导致合并冲突的文件：

    ```
    git rebase origin/master
    ```
 

 
1.  Edit those files to rsesolve the conflicts and finish the rebase:  1.编辑这些文件以解决冲突并完成变基：

    ```
    git add <files_with_resolved_conflicts>
    git rebase --continue
    ```
 

 
1.  Commit and upload your changes:  1.提交并上传您的更改：

    ```
    git commit --amend
    jiri upload
    ```
 

 
## Manage changes that span multiple repositories  管理跨多个存储库的更改 

To understand how to manage changes that span different repositories (petals), see the following pages: 要了解如何管理跨越不同存储库（花瓣）的更改，请参阅以下页面：

 
*   [Working across different petals](/docs/development/workflows/working_across_petals.md)  * [跨不同的花瓣工作]（/ docs / development / workflows / working_across_petals.md）
*   [Upload changes from multiple repositories](/docs/development/source_code/upload_changes_from_multiple_repositories.md)  * [从多个存储库上传更改]（/ docs / development / source_code / upload_changes_from_multiple_repositories.md）

