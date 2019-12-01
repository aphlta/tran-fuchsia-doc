 
# Workflow: Tips  工作流程：提示 

This is a list of tips that should help you be more productive when working on fuchsia.  这是一些提示，它们可以帮助您在进行紫红色时提高工作效率。

 
## Gerrit Monitor  Gerrit Monitor 

Install the [Gerrit Monitor](https://chrome.google.com/webstore/detail/gerrit-monitor/leakcdjcdifiihdgalplgkghidmfafoh) Chrome extension to have in the Chrome toolbar the list of CLs requiring yourattention. 安装[Gerrit Monitor]（https://chrome.google.com/webstore/detail/gerrit-monitor/leakcdjcdifiihdgalplgkghidmfafoh）Chrome扩展程序，以便在Chrome浏览器工具栏中具有需要注意的CL列表。

 
## Enabling three-way diffs in Git  在Git中启用三向差异 

By default Git uses two-way diffs when presenting conflicts. It does not display what the original text was before the conflict, which makes it [hard tosolves some conflicts](https://stackoverflow.com/questions/4129049/why-is-a-3-way-merge-advantageous-over-a-2-way-merge). 默认情况下，Git在出现冲突时使用双向差异。它不会显示冲突前的原始文本，这使其[难以解决某些冲突]（https://stackoverflow.com/questions/4129049/why-is-a-3-way-merge-advantageous-over -a-2-way-merge）。

You can configure Git to show the original text by enabling three-way diffs:  您可以通过启用三向差异来将Git配置为显示原始文本：

```git config --global merge.conflictstyle diff3```

## Enabling fuchsia-specific git commands

Add `$FUCHSIA_DIR/scripts/git` to your PATH to be able to use fuchsia-specific git
commands such as `git fuchsia-review [<commit ref>]`, which opens the current
or given commit in gerrit.


# Workflow: Questions and Answers

You are encouraged to add your own questions (and answers) here!

[TOC]

## Q: Is there a standard Git workflow for Fuchsia?

There are a wide variety of workflows used by the Fuchsia team. A daily
workflow to get you started is as follows:

```shell
$ jiri update -gc  $ jiri更新-gc
# Start a new feature "myfeature" from the current stable commit  从当前的稳定提交启动新功能“ myfeature”$ git checkout -b myfeature JIRI_HEAD  $ git checkout -b myfeature JIRI_HEAD
# Do work, making changes, etc.  做工作，进行更改等。$ git commit  $ git commit
# Upload your work to Gerrit for review  将您的工作上传到Gerrit进行审核$ jiri upload  $ jiri上传
# OR  要么```

Congratulations, you made your first Gerrit change!

Suppose you want to start new work while you wait for review of "myfeature":

```shell
$ git push origin HEAD:refs/for/master  $ git push origin HEAD：refs / for / master
# Start a new independent line of work while waiting for review:  在等待审核的同时开始新的独立工作：$ git checkout -b otherfeature JIRI_HEAD  $ git checkout -b otherfeature JIRI_HEAD
# OR  要么 
# Start a derivative line of work while waiting for review:  在等待审查的同时开始衍生工作：```

When you want to update "myfeature" and you've been working on an
"independent" line of work:

```shell
$ git checkout -b otherfeature  $ git checkout -b其他功能
# Commit any present dirty work, then, switch to "myfeature":  进行任何当前的脏工作，然后切换到“ myfeature”：$ git checkout myfeature  $ git checkout myfeature
# Make any relevant edits to the code, then:  对代码进行任何相关的编辑，然后：$ git commit --amend  $ git commit-修改
# Now upload the new patchset to Gerrit:  现在将新补丁集上传到Gerrit：$ jiri upload  $ jiri上传
# OR  要么```

When you want to update "myfeature" because you got some review comments, and
you are using a "derivative" line of work:

```shell
$ git push origin HEAD:refs/for/master  $ git push origin HEAD：refs / for / master
# Now you get a review comment that needs a change in "myfeature"  现在，您会收到需要更改“ myfeature”的评论评论 
# Commit your present work, if you aren't finished, maybe use a work-in-progress change:  提交您当前的工作，如果还没有完成，则可以使用进行中的更改：$ git commit -a -m "work in progress"  $ git commit -a -m“正在进行中”
# Start a rebase operation, so you can edit your first change:  开始变基操作，因此您可以编辑第一个更改：$ git rebase -i JIRI_HEAD  $ git rebase -i JIRI_HEAD
# Replace "pick" with "edit" on the change you need to update and save and close the file  在您需要更新并保存并关闭文件的更改上，将“ pick”替换为“ edit” 
# Make the relevant code changes, then:  进行相关代码更改，然后：$ git add . && git rebase --continue  $ git添加。 git rebase-继续
# You may need to make additional "rebase" steps if your edits need integration  如果您的编辑需要集成，则可能需要执行其他“变基”步骤 
# with later commits For each case, look at "git status" to see what files are  在以后的提交中对于每种情况，请查看“ git status”以查看哪些文件是 
# in conflict, and make the relevant adjustments. The rebase is complete when  发生冲突，并进行相关调整。基准完成于 
# git reports "Successfully rebased and updated ...." If you made a "work in  git报告“成功地重新建立基础并更新了...。”如果您进行了“ 
# progress" change and want to unwind that commit:  进度”更改，并希望取消该提交：$ git reset HEAD  $ git reset HEAD
# Now you can upload your modified changes to Gerrit:  现在，您可以将修改后的更改上传到Gerrit：$ jiri upload  $ jiri上传
# OR  要么```

When you see "merge conflict" in Gerrit because your change can't cleanly be
integrated with "master":

```shell
$ git push origin HEAD:refs/for/master  $ git push origin HEAD：refs / for / master
# Checkout the branch for the change you need to update (e.g. "myfeature"):  检出分支以获取您需要更新的更改（例如“ myfeature”）：$ git checkout myfeature  $ git checkout myfeature
# Update your git repository:  更新您的git仓库：$ git fetch  $ git获取
# Update your branch:  更新您的分支：$ git rebase origin/master  $ git rebase原始/主服务器
# Fixup and continue the rebase as necessary, until you see "Successfully rebased ..."  修正并根据需要继续进行变基，直到看到“成功变基...”。 
# Then upload your newly updated code:  然后上传您新更新的代码：$ jiri upload  $ jiri上传
# OR  要么```

When you've been working for more than a day, and you need to "sync your
code" with upstream (you generally want to do this at least once per day):

```
$ git push origin HEAD:refs/for/master  $ git push origin HEAD：refs / for / master
# Commit any in-progress work, then  进行任何正在进行的工作，然后 
# Checkout the stable upstream you last sync'd  检出您上次同步的稳定上游$ git checkout JIRI_HEAD  $ git checkout JIRI_HEAD
# Update your local repository (this will include updates for prebuilts, third  更新您的本地存储库（这将包括预建的更新，第三个 
# party repositories, and so on):  派对存储库，等等）：$ jiri update -gc  $ jiri更新-gc
# Now to switch back to, and update your working branch (e.g. "myfeature"):  现在切换回并更新您的工作分支（例如“ myfeature”）：$ git checkout myfeature  $ git checkout myfeature
# Updating "myfeature" with the latest stable code:  使用最新的稳定代码更新“ myfeature”：$ git rebase JIRI_HEAD  $ git rebase JIRI_HEAD
# Perform fixups and "git rebase --continue" until you get to "Successfully rebased ..."  执行修复程序和“ git rebase --continue”，直到获得“ Successful rebase ...”。```

You can find more information on parts of workflows below.
You can find more information on general git workflows in [gitworkflows(7)](https://github.com/git/git/blob/master/Documentation/gitworkflows.txt).
You can find more information on git in general at [git-scm.com/doc](https://git-scm.com/doc).

### Rebasing

Update all projects simultaneously, and rebase your work branch on `JIRI_HEAD`:

```shell
```

The `git rebase` to `JIRI_HEAD` should be done in *each* repo where you have
ongoing work. It's not needed for repos you haven't touched.

### Uploading a new patch set (snapshot) of a change

You'll need to *upload* a patch set to
[Gerrit](https://fuchsia-review.googlesource.com/) to have it reviewed by
others. We do this with `jiri upload`.

Gerrit uses an auto-generated metadata marker in the CL description to figure
out which Gerrit review thread to upload a patch to, such as: `Change-Id:
I681125d950205fa7654e4a8ac0b3fee7985f5a4f`

This is different from a git commit's SHA hash, and can be considered stable
during review, as you make edits to your changes and commits. Use the same
Change-Id for a given review (in case you are
[squashing](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) multiple
commits).

If you've made changes and want to upload a new patch set, then (assuming that
this is the latest change in your branch; use `git log` to find out) you can do
something like:

```shell
$ jiri update -gc -rebase-untracked $ git checkout <my_branch>$ git rebase JIRI_HEAD$ git commit -a --amend $ jiri update -gc -rebase-untracked $ git checkout <my_branch> $ git rebase JIRI_HEAD $ git commit -a --amend
# -a for all uncommitted files, --amend to amend latest commit  -a用于所有未提交的文件，--amend修改最新的提交```

### Resolving merge conflicts

Attempt a rebase:

```shell
$ jiri upload $ git fetch origin && git rebase origin/master $ jiri上传$ git获取来源git rebase来源/主
# Resolve conflicts as needed...  根据需要解决冲突...```

But read below about how a `git rebase` can negatively interact with `jiri
update`.

### Stashing

You can save all uncommitted changes aside, and re-apply them at a later time.
This is often useful when you're starting out with Git.

```shell
$ jiri upload $ git stash # uncommitted changes will go away $ jiri上传$ git隐藏未提交的更改将消失
# do stuff  做东西```

## Q: I use **fx** and **jiri** a lot. How are they related?

A: They are not related.
[`jiri`](https://fuchsia.googlesource.com/jiri/+/master/) is a wrapper around
git that provides support for managing more than one git repository in sync
(the Fuchsia code base is composed of many git repositories), as well as
synchronizing a set of prebuilt artifacts, such as those found in
`//prebuilt`.
[`fx`](/scripts/fx) is a
convenience wrapper around many tools built in the Fuchsia tree, and helps
with many daily workflow tasks, such as building, running tests, consuming
logs, connecting to shells on devices, and many other operations.

## Q: Will a git rebase to origin/master mess up my jiri-updated (i.e. synchronized) view of the repository?

A: Yes, unless jiri is configured to sync the rebased repository/petal to HEAD
instead of the globally integrated version. This is not the case if you use the
current/new default bootstrap setup, which tracks global integration for all
repos, but may be the case if you set up your checkout in the past or used `fx
set-petal X`.

When working at petal X (accomplished with `fx set-petal X`), `jiri update` will
rebase the local branches in repo X onto HEAD of origin/master. But other
petals' repos will be synced to specific revisions that may be behind HEAD of
their origin/master.

Our continuous integration system (specifically rollers) makes a new revision of
a petal available to other petals only after testing that the new revision
doesn't break other petals. `jiri update` will always leave other petals synced
to these successfully-tested revisions. But a git rebase to origin/master for a
petal may advance that repo beyond the tested revision, which has the potential
to introduce breaking changes. The result may be that you can build for a
certain petal, but not for other petals (e.g., correctly build garnet, but not
be able to build topaz).

If you have a particular commit that you want jiri to honor, download its
`jiri.update` file and feed it to `jiri update`.

## Q: What if I need an atomic commit across git repositories?

A: Can't, sorry. Try to arrange your CLs to not break each petal during a
transition (i.e., do a [soft
transition](working_across_petals.md#soft-transitions-preferred)). But sometimes
you will necessarily break things; aim to minimize the duration of breakage
(i.e., a [hard transition](working_across_petals.md#hard-transitions)).

Example scenario: I have an interface defined in stem, and it is implemented in
another petal. If I change the interface, am I doomed to break other petals?

Yes. But you can "babysit" the rollers so that the breakage range is minimized.
The gotcha with babysitting is that others may *also* be babysitting a breakage,
and you may end up babysitting for longer than you had intended.

Alternatively, you *could* do something as follows:

1.  Introduce a new interface in `lower` that is a copy of the original
    interface.
1.  Wait for `lower-roller` to roll into `upper`, or roll yourself by updating
    the file `upper/manifest`.
1.  Change `upper` to use the new clone interface that maintains the old
    contract.
1.  Change `lower` such that the original interface’s contract is modified to
    the new, desired form.
1.  Wait for `lower-roller`, or roll yourself.
1.  Change `upper` to use the original interface name, now with its new
    contract. Make any changes required.
1.  Delete the clone interface in `lower`.

## Q: How do I do parallel builds from a single set of sources?

Note: this answer is subject to change/breakage shortly after authorship.

Lets assume you want to produce four builds:

 * a "bringup" product for x64
 * a "workstation" product for x64
 * a "core" product for vim2
 * a "workstation" product for vim2

First, one must build Zircon, as the Zircon build directory is shared across
Fuchsia build targets. It doesn't matter at this stage which product/board
combination you pick, we just need to start building Zircon.

```shell
$ git stash pop # uncommitted changes will come back  $ git stash pop尚未提交的更改将返回
# We start with bringup, because it's small, but it doesn't matter which you start with:  我们从启动开始，因为它很小，但是无论从哪个开始都没关系：```

Now you have Zircon built, you can start building several other builds concurrently:

```shell
$ fx set bringup.x64 out/bringup.x64 $ fx --dir=out/bringup.x64 build$ fx set workstation.x64 out/workstation.x64$ fx --dir out/workstation.x64 build > workstation.x64.build.log & $ fx设置bringup.x64 out / bringup.x64 $ fx --dir = out / bringup.x64 build $ fx设置worker.x64 out / workstation.x64 $ fx --dir out / workstation.x64 build> worker.x64。 build.log

$ fx set core.arm64 out/core.vim2 $ fx --dir out/core.vim2 build > core.vim2.build.log & $ fx设置core.arm64 out / core.vim2 $ fx --dir out / core.vim2 build> core.vim2.build.log

```

You can reference each of these builds while running `fx` tools by passing
`--dir` to your fx command, e.g. to run `fx serve` using the vim2 workstation
product, you would use:

```shell
```

You can also change which build directory is your current default by using `fx use`:

```shell
```

## Q: What if I want to build at a previous snapshot across the repos?

A: You'll need to `jiri update` against a *jiri snapshot file*, an XML file that
captures the state of each repo tracked by jiri.

## Q: I'm building on Mac, how to do I stop getting spammed with 'incoming network connection' notifications?

A: You'll want to run `fx setup-macos`, which registers all the relevant Fuchsia
tools with the MacOS Application Firewall.

## Q: When/how do I make a soft vs hard transition when changing APIs?

See [this section](working_across_petals.md#hard-and-soft-transitions) about hard
and soft transitions.

## Q: How do I update a FIDL protocol?

A: The preferred method for updating a FIDL protocol is to use a *soft
transition*. In order for a soft transition to work, you need to create an
intermediate state that supports both the old and new versions of the protocol.

Use the following steps to execute a soft transition:

1.  Modify the FIDL definition in the Stem repository to support both the old
    and new protocol elements. Before landing the change, trigger the *global
    integration* tryjobs to validate that step 2 will succeed.

1.  Publish the Stem repository, either by waiting for the daily automatic
    publication or by manually publishing the repository.

1.  Update all the clients to use the new protocol elements.

1.  Publish all the clients.

1.  Remove the old protocol elements from the FIDL definition in the Stem
    repository.

1.  Publish the Stem repository, typically by waiting for the daily automatic
    publication.

## Q: How do I coordinate changes across multiple Petals?

A: Coordinating an atomic change across multiple Petals (or between the Stem
repository and one or more Petals) requires performing a *hard transition*.

Use the following steps to execute a hard transition:

1.  Prepare changes to all affected repositories. If all of these repositories
    are part of the Platform Source Tree:

    1.  Upload CLs containing the changes to fuchsia-review.googlesource.com.
    1.  Upload another CL that modifies the *global integration* repository to
        reference the git revisions from your CLs. Perform a "dry run" of the
        commit queue for this CL.

1.  Notify the team stating your intention to execute a hard transition.

1.  Land all the changes in the affected repositories. This step will break
    local integration in these repositories but will not break global
    integration because the changes have not been published yet.

1.  Land a change in the *global integration* repository that references the new
    versions of the affected repositories. This change will publish the new
    version of all the affected repositories and should not break global
    integration. This change should unbreak local integration in the affected
    repositories.

## Q: How do I bisect history to track down when something changed?

A: To bisect history, perform the following steps:

1.  Bisect the history in the configuration repository, which contains the
    revision history of global integration, before and after the observable
    change. The result of this bisect will be a single change to configuration
    repository, presumably that includes the publication of one or more
    repositories or prebuilt packages.

1.  If the change to the configuration repository is a publication of a single
    repository, bisect the history of that repository before and after the
    publication of global integration. The result of this bisect should be the
    revision at which the behavior changed.

1.  If the change to the configuration repository is a publication of prebuilt
    packages, switch to the source tree from which the prebuilt packages were
    created. Consult the documentation for that repository regarding how to
    bisect changes in that repository.

1.  If the change to the configuration repository is a publication of multiple
    repositories, bisecting history becomes complicated because the two
    repositories have likely been changed in concert and you will need to
    traverse their history in concert. Consider studying the history of the
    repositories to understand why they were published together.
