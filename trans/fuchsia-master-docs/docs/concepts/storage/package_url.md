 
# Fuchsia Package URLs  紫红色包装网址 

Fuchsia software, including system components and third-party components, is distributed in the form of packages.  These packages are signed in such a wayas to produce a cryptographic chain of trust between the repository root andthe package itself.  Fuchsia relies on this chain of trust to ensure theauthenticity of packages as required to implement features such as verifiedboot. 紫红色的软件，包括系统组件和第三方组件，以软件包的形式分发。这些软件包以这样一种方式进行签名，以便在存储库根目录和软件包本身之间产生加密的信任链。紫红色依赖于此信任链来确保软件包的真实性，以实现所需功能，例如经过验证的启动。

This document addresses the problem of how to identify individual packages using **fuchsia-pkg** URLs. 本文档解决了如何使用** fuchsia-pkg ** URL识别单个包装的问题。

 
## Goals  目标 

 
 * Encode stable identifiers for packages in the form of a URL under the assumption that many system components will effectively "bookmark" URLs forthe long term.  (Example: to persist the URLs of all modules in a story.) *假设许多系统组件可以长期有效地“标记” URL，则以URL形式对软件包的稳定标识符进行编码。 （示例：在故事中保留所有模块的URL。）
 * Establish an association between a package URL and the hostname of an Internet server from which the package could perhaps be downloaded. *在程序包URL和可以从中下载程序包的Internet服务器的主机名之间建立关联。
 * Be robust in the face of repository mirrors: a package's authenticity can be proven even if the contents were actually downloaded from a different hostthan the one specified in the package URL.  (Example: edge cache,peer-to-peer, USB stick...) *面对存储库镜像时应具有鲁棒性：即使实际上从与软件包URL中指定的主机不同的主机下载了内容，也可以证明软件包的真实性。 （例如：边缘缓存，点对点，U盘...）
 * Be relatively human-readable.  *相对易读。
 * Be strict about representation, including structure, allowed characters, and maximal length. *请严格遵守表示形式，包括结构，允许的字符和最大长度。
 * No requirement for TLS at point of distribution: the package and repository metadata and auxiliary information about known sources is enough to verifyauthenticity independently of how the contents were actually obtained given apackage URL (even offline). *分发时不需要TLS：程序包和存储库元数据以及有关已知来源的辅助信息足以验证真实性，而与在给定程序包URL的情况下实际获取内容的方式无关（甚至是脱机）。

 
## Non-Goals  非目标 

 
 * Establish a cryptographically strong association between a package URL itself and its repository's chain of trust, enabling proof of authenticity givennothing but the URL. *在程序包URL本身与其存储库的信任链之间建立一种加密上很强的关联，从而仅凭URL即可提供真实性证明。

 
## Identifying Repositories, Packages, and Resources  识别存储库，程序包和资源 

This section describes the various characteristics used to identity repositories, packages and resources. 本节描述用于标识存储库，程序包和资源的各种特征。

These definitions have been chosen to align with the [TUF Specification] where possible. 选择这些定义以尽可能与[TUF规范]保持一致。

These identifying characteristics are not intended to be shown to end-users during normal operation (exception: developers and system administrators).Consequently, we may eschew concerns related to localization of names. 这些标识特征不打算在正常运行期间向最终用户显示（例外：开发人员和系统管理员）。因此，我们可以避免与名称本地化有关的问题。

[TUF Specification]: https://github.com/theupdateframework/specification/blob/master/tuf-spec.md#4-document-formats  [TUF规范]：https://github.com/theupdateframework/specification/blob/master/tuf-spec.md4-document-formats

 
## Repository Identity  仓库身份 

 
### Repository Root Verification (Known Sources)  存储库根验证（已知来源） 

The repository's root role (a quorum of one or more public/private key pairs) establishes a chain of trust such that package authenticity, integrity, andfreshness can be verified cryptographically.  The root role signs keys for morelimited roles which are then used to sign package metadata and the targetsthemselves.  See [here][TUF Security] and [here][TUF METADATA] for more details. 存储库的根角色（一个或多个公共/专用密钥对的仲裁）建立了信任链，以便可以通过密码验证包的真实性，完整性和新鲜度。根角色对更多有限角色的密钥进行签名，然后将其用于对程序包元数据和目标自身进行签名。有关更多详细信息，请参见[here] [TUF安全性]和[here] [TUF METADATA]。

To verify that a package is authentic, we must also verify that the repository from which it is being downloaded is authentic.  This will be implemented bymaintaining a list of known source repositories with their public keys on thedevice.  Packages from unknown sources will be rejected. 为了验证软件包是真实的，我们还必须验证从中下载软件包的存储库是真实的。这将通过在设备上保留带有公钥的已知源存储库列表来实现。来自未知来源的包裹将被拒绝。

[TUF Security]: https://theupdateframework.github.io/security.html [TUF Metadata]: https://theupdateframework.github.io/metadata.html [TUF安全性]：https://theupdateframework.github.io/security.html [TUF元数据]：https://theupdateframework.github.io/metadata.html

 
### Repository Hostname  储存库主机名 

The package URL contains a repository [hostname] to identify the package's source.  Per [RFC 1123] and [RFC 5890], a hostname is a sequence of dot(`.`)-delimited [IDNA A-labels], each of which consists of 1 to 63 of thefollowing latin-1 characters in any order: digits (`0` to `9`), lower-caseletters (`a` to `z`), or hyphen (`-`).  No other characters are permitted.  Thetotal maximum length of a hostname is 253 characters including the dots. 程序包URL包含一个存储库[主机名]，用于标识程序包的来源。根据[RFC 1123]和[RFC 5890]，主机名是由点（`.`）分隔的[IDNA A-labels]序列，每个序列由1至63个以下拉丁1字符组成，其顺序为：数字（“ 0”至“ 9”），小写字母（“ a”至“ z”）或连字符（“-”）。不允许使用其他字符。主机名的总最大长度为253个字符（包括点）。

[hostname]: https://en.wikipedia.org/wiki/Hostname [RFC 1123]: https://tools.ietf.org/html/rfc1123[RFC 5890]: https://tools.ietf.org/html/rfc5890[IDNA A-labels]: https://tools.ietf.org/html/rfc5890#section-2.3.2.1 [主机名]：https://en.wikipedia.org/wiki/主机名[RFC 1123]：https://tools.ietf.org/html/rfc1123[RFC 5890]：https://tools.ietf.org/ html / rfc5890 [IDNA A-labels]：https：//tools.ietf.org/html/rfc5890section-2.3.2.1

**Example repository hostnames:**  **示例存储库主机名：**

 
 * `fuchsia.com`  *`fuchsia.com`
 * `mycorp.com`  *`mycorp.com`

 
## Package Identity  包裹身份 

 
### Package Name  包裹名字 

A package name is a symbolic label which identifies a logical collection of software artifacts (files), independent of any particular variant or revisionof those artifacts.  The package name is used to locate package metadata withina repository.  Package metadata must be signed by a role which is trusted bythe repository root. 软件包名称是一个符号标签，用于标识软件工件（文件）的逻辑集合，而与这些工件的任何特定变体或修订版本无关。软件包名称用于通过存储库定位软件包元数据。软件包元数据必须由存储库根目录信任的角色签名。

A package name consists of a sequence of up to 100 of the following latin-1 characters in any order: digits (`0` to `9`), lower-case letters (`a` to `z`),hyphen (`-`), and period (`.`).  No other characters are permitted. 包名称由任意顺序的最多100个以下拉丁1字符组成：数字（0到9），小写字母（a到z），连字符（ -`）和句点（`.`）。不允许使用其他字符。

A package's name must be unique among all packages in a repository. Conversely, packages within different repositories are considered distinct evenif they have the same name. 软件包名称在存储库中的所有软件包中必须唯一。相反，即使不同存储库中的软件包具有相同的名称，也被认为是不同的。

**Examples of package names:**  **包名示例：**

 
 * `fuchsia-shell-utils`  *`紫红色的壳-utils`
 * `fuchsia-scenic`  *`紫红色风景`
 * `fuchsia-fonts`  *紫红色字体
 * `mycorp-product`  *`mycorp-product`

 
### Package Variant  包装变体 

A package variant is a symbolic label for a sequence of package updates. Different variants of the same package may receive different updates, atdifferent rates, and/or with different content.  The package variant is used tolocate metadata for a sequence of package updates within a repository.  Variantmetadata must be signed by a role which is trusted by the role which signed thepackage's metadata. 软件包变体是一系列软件包更新的符号标签。同一程序包的不同变体可以接收不同的更新，不同的速率和/或具有不同的内容。程序包变体用于为存储库中的程序包更新序列定位元数据。 Variantmetadata必须由一个角色签名，该角色由对该程序包的元数据进行签名的角色所信任。

A package variant consists of a sequence of up to 100 of the following latin-1 characters in any order: digits (`0` to `9`), lower-case letters (`a` to `z`),hyphen (`-`), and period (`.`).  No other characters are permitted. 一个package变体由最多100个以下的latin-1字符组成，该序列可以按任意顺序排列：数字（“ 0”至“ 9”），小写字母（“ a”至“ z”），连字符（“ -`）和句点（`.`）。不允许使用其他字符。

What a package variant actually represents is at the discretion of the software developer and/or distributor responsible for the package since they control thesequence of updates. 软件包变体实际代表的内容由负责软件包的软件开发人员和/或发行者决定，因为他们控制更新的频率。

**Example package variant conventions:**  **示例包装变体约定：**

 
 * **update channels**: `stable`, `beta`, `bleeding-edge`, ...  * **更新频道**：“稳定”，“测试版”，“出血边缘”，...
 * **major product upgrades**: `antelope`, `bear`, `caterpillar`, `deer`, …  * **主要产品升级**：“羚羊”，“熊”，“毛毛虫”，“鹿”，…
 * **a combination of the above**: `antelope-stable`, `deer-beta`, …  * **以上各项的组合**：“羚羊稳定”，“鹿贝塔”，…
 * **breaking API revisions**: `1.0`, `1.1`, `2.0`, …  * **最新的API修订版**：`1.0`，`1.1`，`2.0`，...
 * **variant-free**: `default`  * **无变体**：`default`

This two-level scheme of package name and variant increases the overall flexibility of the package identification system. 包裹名称和变体的这种两级方案增加了包裹识别系统的整体灵活性。

 
### Package Hash  包裹杂凑 

A package hash is the [merkleroot] of the package's meta.far.  Because the package's metadata encodes the content addresses of the package's files, anychanges to the package's metadata or content will produce a different packagehash, thereby making it possible to distinguish each unique revision of thepackage. 程序包哈希是程序包meta.far的[merkleroot]。由于软件包的元数据对软件包文件的内容地址进行编码，因此，对软件包的元数据或内容进行的任何更改都会产生不同的packagehash，从而可以区分出每个唯一的版本。

A package hash is represented as a hex-encoded string consisting of exactly 64 of the following latin-1 characters: digits (`0` to `9`) and lower-case letters(`a` to `f`).  No other characters are permitted. 包散列表示为十六进制编码的字符串，该字符串完全由以下拉丁1个字符中的64个组成：数字（“ 0”至“ 9”）和小写字母（“ a”至“ f”）。不允许使用其他字符。

**Example package hashes:**  **示例包装散列：**

 
 * `15ec7bf0b50732b49f8228e07d24365338f9e3ab994b00af08e5a3bffe55fd8b`  *`15ec7bf0b50732b49f8228e07d24365338f9e3ab994b00af08e5a3bffe55fd8b`

[merkleroot]: /docs/concepts/storage/merkleroot.md  [merkleroot]：/docs/concepts/storage/merkleroot.md

 
## Resource Identity  资源身份 

 
### Resource Paths  资源路径 

A resource path is a UTF-8 string which identifies a resource within a package. This is a file path, consisting of a sequence of single `/` delimitedpath segments, each of which is a non-empty sequence of non-zero UTF-8characters not equal to `.`, `..`, or `/`. 资源路径是UTF-8字符串，用于标识包中的资源。这是一个文件路径，由一系列单个`/`分隔路径段组成，每个段都是一个非空的非零UTF-8字符序列，不等于`.`，`..`或`/`。 。

This definition is compatible with the definition of [Fuchsia filesystem paths] but it imposes a UTF-8 encoding rather than admitting arbitrary binary stringssince such strings cannot always be encoded as valid URLs. 此定义与[Fuchsia文件系统路径]的定义兼容，但是它采用UTF-8编码，而不是允许使用任意二进制字符串，因为此类字符串不能始终被编码为有效URL。

Per [RFC 3986], resource paths are percent-encoded when they appear in URLs.  根据[RFC 3986]，资源路径出现在URL中时会进行百分比编码。

**Example resource paths:**  **示例资源路径：**

 
 * `meta/my.component`  *`meta / my.component`
 * `bin/myprogram`  *`bin / myprogram`
 * `lib/mylibrary.so`  *`lib / mylibrary.so`
 * `assets/en/strings`  *`资产/ zh /字符串'
 
 

[Fuchsia filesystem paths]: /docs/concepts/framework/namespaces.md#object-relative-path-expressions [RFC 3986]: https://tools.ietf.org/html/rfc3986#page-11 [紫红色文件系统路径]：/docs/concepts/framework/namespaces.mdobject-relative-path-expressions [RFC 3986]：https://tools.ietf.org/html/rfc3986page-11

 
## The fuchsia-pkg URL Scheme  紫红色-pkg URL方案 

The **fuchsia-pkg** URL scheme combines the preceding identifying characteristics to establish a means for referring to a repository, a package,or a resource, depending on which parts are included. fuchsia-pkg ** URL方案结合了前面的标识特征，以根据所包含的部分来建立引用存储库，程序包或资源的手段。

 
## Syntax  句法 

```
fuchsia-pkg://<repo-hostname>[/<pkg-name>[/<pkg-variant>][?hash=<pkg-hash>][#<resource-path>]]
```
 

**Scheme: (required)**  **方案：（必填）**

 
 * The following case-insensitive characters: `fuchsia-pkg://`.  *以下不区分大小写的字符：`fuchsia-pkg：//`。
  * Although the canonical form is lower-case, URL scheme encoding is case-insensitive therefore the system must handle all cases. *尽管规范形式为小写，但URL方案编码不区分大小写，因此系统必须处理所有情况。

**Repository: (required)**  **存储库：（必填）**

 
 * The repository hostname encoded as dot-delimited IDNA A-Labels.  *存储库主机名编码为以点分隔的IDNA A标签。

**Package: (optional)**  **包装：（可选）**

 
 * A single `/` character.  *单个`/`字符。
 * The [package name](#package-name).  * [程序包名称]（程序包名称）。
 * Optionally followed by...  *（可选）后跟...
   * A single `/` character.  *单个`/`字符。
   * The package variant.  *包的变体。

**Package Hash: (optional, only valid if a package was specified)**  **包裹哈希：（可选，仅在指定包裹时有效）**

 
 * The string `?hash=`.  *字符串`？hash =`。
 * The [package hash](#package-hash).  * [程序包哈希]（package-hash）。

**Resource Path: (optional, only valid if a package was specified)**  **资源路径：（可选，仅在指定软件包的情况下有效）**

 
 * A single `#` character.  *单个``字符。
 * The UTF-8 [resource path](#resource-paths), relative to the root of the package, percent-encoded as required, per [RFC 3986]. *根据[RFC 3986]，相对于包根的UTF-8 [资源路径]（resource-paths）按要求进行百分比编码。

URL components containing reserved characters are percent-encoded according to [RFC 3986].  Note that the scheme, [repository hostname](#repository-hostname),[package name](#package-name), [package variant](#package-variant), and [packagehash](#package-hash) components are all defined to use a restricted subset ofcharacters, none of which require encoding, unlike the resource path. 包含保留字符的URL组件根据[RFC 3986]进行了百分比编码。请注意，已将方案，[存储库主机名]（repository-hostname），[软件包名称]（package-name），[软件包变体]（package-variant）和[packagehash]（package-hash）组件定义为使用受限的字符子集，与资源路径不同，它们都不要求编码。

 
## Interpretation  解释 

A **fuchsia-pkg** URL has different interpretations depending on which parts are present. **紫红色-pkg ** URL具有不同的解释，具体取决于存在的部分。

 
 * If the repository, package, and resource parts are present, then the URL identifies the indicated resource within the package. *如果存在存储库，软件包和资源部分，则URL标识软件包中指示的资源。
 * If only the repository and package parts are present, then the URL identifies the indicated package itself. *如果仅存在存储库和程序包部分，则URL标识指示的程序包本身。
 * If only the repository parts are present, then the URL identifies the indicated repository itself. *如果仅存在存储库部分，则URL标识指示的存储库本身。

The package parts can express varying degrees of specificity.  At minimum the package name must be present, optionally followed by the package variant andpackage hash. 包装部分可以表达不同程度的特异性。至少必须存在程序包名称，并可选地后面是程序包变体和程序包哈希。

When the **package resolver** fetches resources given a **fuchsia-pkg** URL, it is required that the package variant be specified. If the package hash ismissing, the **package resolver** fetches the resources from the newest revisionof the package variant available to the client. 当“包解析器”获取给定“ fuchsia-pkg” URL的资源时，要求指定包变体。如果缺少包散列，则“包解析器”将从客户端可用的包变体的最新版本中获取资源。

Although a repository hostname is included in the URL, it is safe to fetch resources from any replica of the repository which satisfies the samecryptographic chain of trust.  The problem of locating an appropriate mirror isbeyond the scope of this document. 尽管URL中包含存储库主机名，但是从满足相同加密信任链的存储库的任何副本中获取资源都是安全的。定位适当的镜像的问题超出了本文档的范围。

**Examples**  **例子**

 
 * a repository:  *储存库：
   * `fuchsia-pkg://fuchsia.com`  *`fuchsia-pkg：// fuchsia.com`
 * a package:  * 一袋：
   * `fuchsia-pkg://fuchsia.com/fuchsia-shell-utils`  *`fuchsia-pkg：// fuchsia.com / fuchsia-shell-utils`
   * `fuchsia-pkg://fuchsia.com/fuchsia-shell-utils/stable`  *`fuchsia-pkg：// fuchsia.com / fuchsia-shell-utils / stable`
 * a resource:  *资源：
   * `fuchsia-pkg://fuchsia.com/fuchsia-shell-utils/stable#bin/ls`  *`fuchsia-pkg：// fuchsia.com / fuchsia-shell-utils / stablebin / ls`
   * `fuchsia-pkg://google.com/chrome/stable#meta/webview.component`  *`fuchsia-pkg：// google.com / chrome / stablemeta / webview.component`
 * a resource from a specific hashed revision of a package:  *来自程序包的特定哈希修订版的资源：
