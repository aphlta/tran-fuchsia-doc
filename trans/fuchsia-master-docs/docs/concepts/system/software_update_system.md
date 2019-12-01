 
# Software Update System  软件更新系统 

Fuchsia is a project that constantly gets updates for new features, enhancements, and security fixes. Fuchsia's software update system makes use of[The Update Framework (TUF) version 1.0](https://github.com/theupdateframework/specification/blob/master/tuf-spec.md).However, Fuchsia does have some differences from TUF: 紫红色是一个不断获取新功能，增强功能和安全修复程序更新的项目。紫红色的软件更新系统使用了[The Update Framework（TUF）version 1.0]（https://github.com/theupdateframework/specification/blob/master/tuf-spec.md）。但是，紫红色确实与TUF有一些区别：

 
* [Specification version](#specification-version)  * [规格版本]（规格版本）
* [Package organization](#package-organization)  * [包装组织]（package-organization）
* [Merkle root](#merkle-root)  * [Merkle根]（merkle根）

 
## Specification version {#specification-version}  规范版本{specification-version} 

In a Fuchsia repository, the Fuchsia repository version is listed as a top-level attribute of the target role's signed data. This example showsthe format of the specification version: 在Fuchsia存储库中，Fuchsia存储库版本被列为目标角色的签名数据的顶级属性。此示例显示了规范版本的格式：

```
{
  ...

  "signed": {
    "_type": ROLE,
    "spec_version": "1",
    "custom": {
      "fuchsia_spec_version": <FUCHSIA_SPEC_VERSION>,
  }

  ...
}
```
 

Definition of values:  值的定义：

 
* `FUCHSIA_SPEC_VERSION`. `INT`. The value of the Fuchsia repository specification version. For example, `1`. *`FUCHSIA_SPEC_VERSION`。 `INT`。紫红色存储库规范版本的值。例如，“ 1”。

 
## Package organization {#package-organization}  包裹组织{package-organization} 

TUF targets in a Fuchsia repository that address Fuchsia packages contain custom meta data that points to the Package Metadata Archive. This example shows theformat for packages: 在Fuchsia存储库中的TUF目标（针对Fuchsia包）包含指向包元数据存档的自定义元数据。此示例显示了软件包的格式：

```
{
  ...

  "targets": {
    "/PACKAGE_PATH": {
      ...
    }

  ...
  }
}
```
 

Definition of values:  值的定义：

 
* `PACKAGE_PATH`. The relative path to the package from the repository's base URL. *`PACKAGE_PATH`。从存储库的基本URL到软件包的相对路径。

  Note: At the moment the only supported path is `PACKAGE/VARIANT`, where `PACKAGE` is the package name and `VARIANT` is the package version. 注意：目前唯一支持的路径是“ PACKAGE / VARIANT”，其中“ PACKAGE”是软件包名称，而“ VARIANT”是软件包版本。

 
## Merkle root {#merkle-root}  默克尔根{merkle-root} 

In the Fuchsia repository, each package target includes the [merkle root](/docs/concepts/storage/merkleroot.md) of the package's meta FAR as a custom attribute.This example shows the format for the merkle root: 在Fuchsia存储库中，每个程序包目标都将程序包meta FAR的[merkle root]（/ docs / concepts / storage / merkleroot.md）包含为自定义属性。此示例显示了merkle root的格式：

```
{
  ...

  "targets" : {
    PACKAGEPATH : {
      "length" : LENGTH,
      "hashes" : HASHES,
      "custom" : {
        "merkle" : <MERKLE_ROOT>,
        "size" : <BLOB_SIZE>,
      }
    }

    ...
  }
}
```
 

Definition of values:  值的定义：

 
* `MERKLE_ROOT`. `STRING`. The hex string of the merkle root hash of the package's meta FAR. *`MERKLE_ROOT`。 `STRING`。包的meta FAR的Merkle根哈希值的十六进制字符串。
* `BLOB_SIZE`. `INT`. The size, in bytes, of the unencrypted BLOB identified by the `MERKLE_ROOT`.  *`BLOB_SIZE`。 `INT`。 MERKLE_ROOT标识的未加密BLOB的大小（以字节为单位）。

