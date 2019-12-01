 

 
# Upload changes from multiple repositories  从多个存储库上传更改 

Changes in two or more separate repos will be automatically tracked for you by Gerrit if you use the same topic. 如果您使用相同的主题，则Gerrit会自动为您跟踪两个或多个单独存储库中的更改。

Multipart changes that are tracked in Gerrit using the same topic will be tested together. These changes can be landed in Gerrit at the same time with `Submit Whole Topic`. Topicscan be edited using the Gerrit UI on your browser. 使用相同主题在Gerrit中跟踪的多部分更改将一起进行测试。这些更改可以与“提交整个主题”同时进入Gerrit。使用浏览器上的Gerrit UI可以编辑Topic。

 
## Using jiri upload {#using-jiri-upload}  使用jiri上传{using-jiri-upload} 

To upload changes together, you need to create a branch with same name on all repositories.  要一起上传更改，您需要在所有存储库上创建一个具有相同名称的分支。

Do the following:  请执行下列操作：

 
1.  Make and commit the first change in a Fuchsia repository:  1.在紫红色的存储库中进行并提交第一个更改：

 
    1.  Go to the repository:  1.转到存储库：

        ```
        cd examples/fortune
        ```
 
    1.  Create a new branch; for example, *add_my_new_feature*:  1.创建一个新分支；例如* add_my_new_feature *：

        ```
        git checkout -b add_my_new_feature
        ```
 
    1.  Edit and add the files related to the feature:  1.编辑并添加与功能相关的文件：

        ```
        git add <my_feature_related_files>
        ```
 
    1.  Commit your first change:  1.提交您的第一个更改：

        ```
        git commit
        ```
 

 
1.  Make and commit the second change in another Fuchsia repository:  1.在另一个紫红色的存储库中进行并提交第二个更改：

 
    1.  Go to the second repository:  1.转到第二个存储库：

        ```
        cd fuchsia/build
        ```
 
    1.  Create a new branch with the same name, *add_my_new_feature*:  1.创建一个具有相同名称的新分支* add_my_new_feature *：

        ```
        git checkout -b add_my_new_feature
        ```
 

 
    1.  Edit and add the files related to the feature:  1.编辑并添加与功能相关的文件：

        ```
        git add <more_of_my_feature_related_files>
        ```
 
    1.  Commit your second change:  1.进行第二次更改：

        ```
        git commit
        ```
 

 
1.  Use `-multipart` to upload all changes with the same branch name across repos:  1.使用`-multipart`在仓库中上传具有相同分支名称的所有更改：

    ```
    jiri upload -multipart
    ```
 

    Or  要么

    ```
    jiri upload -multipart -topic="custom_topic"
    ```
 

After the changes are submitted, clean up the local branches:  提交更改后，请清理本地分支：

```
cd examples/fortune
git branch -d add_my_new_feature
```
And  和

```
cd fuchsia/build
git branch -d add_my_new_feature
```
 

 
## Using Git command  使用Git命令 

You can also use the `git` command to upload all changes across repositories. The steps are identical as the steps in [Using jiriupload](#using-jiri-upload); however, instead of `jiri upload -multipart` in Step 3, use thefollowing `git` command to upload your changes: 您也可以使用git命令在存储库中上传所有更改。这些步骤与[使用jiriupload]（使用jiri-upload）中的步骤相同；但是，不要在步骤3中使用“ jiri upload -multipart”，而是使用以下“ git”命令来上传您的更改：

```
git push origin HEAD:refs/for/master%topic=add_my_new_feature
```
 

