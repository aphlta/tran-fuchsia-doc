 
# zxcrypt  zxcrypt 

 
## Overview  总览zxcrypt is a block device filter driver that transparently encrypts data being written to and decrypts being read from data a block device.  The underlying block device that a zxcrypt deviceuses may be almost any block device, including raw disks, ramdisks, GPT partitions, FVM partitionsor even other zxcrypt devices.  The only restriction is that the block size be page-aligned.  Oncebound, the zxcrypt device will publish another block device in the device tree that consumers caninteract with normally. zxcrypt是一种块设备筛选器驱动程序，它透明地加密正在写入的数据和解密从块设备中读取的数据。 zxcrypt设备使用的基础块设备几乎可以是任何块设备，包括原始磁盘，虚拟磁盘，GPT分区，FVM分区甚至其他zxcrypt设备。唯一的限制是块大小必须页面对齐。一旦绑定，zxcrypt设备将在设备树中发布另一个块设备，供消费者正常交互。

 
## Usage  用法zxcrypt contains both a [driver](/zircon/system/dev/block/zxcrypt) and [library](/zircon/system/ulib/zxcrypt) Provided by libzxcrypt.so are four functions for managing zxcrypt devices.  Each takes one or more`zxcrypt_key_t` keys, which associates the key data, length, and slot in the case of multiple keys. zxcrypt包含[驱动程序]（/ zircon / system / dev / block / zxcrypt）和[库]（/ zircon / system / ulib / zxcrypt）。libzxcrypt.so提供了四个用于管理zxcrypt设备的功能。每个密钥都带有一个或多个“ zxcrypt_key_t”密钥，在有多个密钥的情况下，它们将密钥数据，长度和插槽关联起来。
* The __zxcrypt_format__ function takes an open block device, and writes the necessary encrypted metadata to make it a zxcrypt device.  The zxcrypt key provided does not protect the data on thedevice directly, but is used to protect the data key material. * __zxcrypt_format__函数采用一个开放块设备，并写入必要的加密元数据以使其成为zxcrypt设备。提供的zxcrypt密钥并不直接保护设备上的数据，而是用于保护数据密钥材料。

```c++
zx_status_t zxcrypt_format(int fd, const zxcrypt_key_t* key);
```
 

 
* The __zxcrypt_bind__ function instructs the driver to read the encrypted metadata and extract the data key material to use in transparently transforming I/O data. * __zxcrypt_bind__函数指示驱动程序读取加密的元数据并提取数据密钥材料，以用于透明地转换I / O数据。

```c++
zx_status_t zxcrypt_bind(int fd, const zxcrypt_key_t *key);
```
 

 
* The __zxcrypt_rekey__ function uses the old key to first read the encrypted metadata, and the new key to write it back. * __zxcrypt_rekey__函数使用旧密钥首先读取加密的元数据，并使用新密钥将其写回。

```c++
zx_status_t zxcrypt_rekey(int fd, const zxcrypt_key_t* old_key, const zxcrypt_key_t* new_key);
```
 

 
* The __zxcrypt_shred__ function first verifies that the caller can access the data by using the key provided to read the encrypted metadata.  If this succeeded, it then destroys the encryptedmetadata containing the data key material.  This prevents any future access to the data. * __zxcrypt_shred__函数首先验证调用者是否可以使用提供的密钥读取加密的元数据来访问数据。如果成功，它将破坏包含数据密钥材料的加密元数据。这样可以防止将来访问数据。

```c++
zx_status_t zxcrypt_shred(int fd, const zxcrypt_key_t* key);
```
 

 
## Technical Details  技术细节 
### DDKTL Driver  DDKTL驱动程序zxcrypt is written as a DDKTL device driver.  [ulib/ddktl](/zircon/system/ulib/ddktl) is a C++ framework for writing drivers in Fuchsia.  It allows authors to automatically supply the[ulib/ddk](/zircon/system/ulib/ddk) function pointers and callbacks by using templatized mix-ins.  In thecase of zxcrypt, the [device](/zircon/system/dev/block/zxcrypt/device.h) is "Messageable","IotxnQueueable", "GetSizable", "UnbindableDeprecated", and implements the methods listed in DDKTL's[BlockProtocol](/zircon/system/banjo/ddk.protocol.block/block.banjo). zxcrypt被编写为DDKTL设备驱动程序。 [ulib / ddktl]（/ zircon / system / ulib / ddktl）是用于在紫红色中编写驱动程序的C ++框架。它允许作者使用模板化的混入自动提供[ulib / ddk]（/ zircon / system / ulib / ddk）函数指针和回调。对于zxcrypt，[device]（/ zircon / system / dev / block / zxcrypt / device.h）是“ Messageable”，“ IotxnQueueable”，“ GetSizable”，“ UnbindableDeprecated”，并实现DDKTL的[ BlockProtocol]（/ zircon / system / banjo / ddk.protocol.block / block.banjo）。

There are two small pieces of functionality which cannot be written in DDKTL and C++:  有两个小功能无法用DDKTL和C ++编写：
* The driver binding logic, written using the C preprocessor macros of DDK's [binding.h](/zircon/system/public/zircon/driver/binding.h). *驱动程序绑定逻辑，使用DDK的[binding.h]（/ zircon / system / public / zircon / driver / binding.h）的C预处理程序宏编写。
* The completion routines of [ulib/sync](/zircon/system/ulib/sync), which are used for synchronous I/O and are incompatible with C++ atomics. * [ulib / sync]（/ zircon / system / ulib / sync）的完成例程，用于同步I / O，并且与C ++原子不兼容。

 
### Worker Threads  工作线程The device starts [worker threads](/zircon/system/dev/block/zxcrypt/worker.h) that run for the duration of the device and create a pipeline for all I/O requests.  Each has a type of I/O it operates on, aqueue of incoming requests I/O that it will wait on, and a data cipher.  When a request is received,if the opcode matches the one it is looking for, it will use its cipher to transform the data in therequest before passing it along. 设备启动在工作期间运行的[工作线程]（/ zircon / system / dev / block / zxcrypt / worker.h），并为所有I / O请求创建管道。每个都有其要操作的I / O类型，等待的传入请求I / O队列以及数据密码。收到请求后，如果操作码与它正在寻找的操作码匹配，它将在传递请求之前使用其密码对请求中的数据进行转换。

The overall pipeline is as shown:  总体管道如下所示：

```
DdkIotxnQueue -+
                \       Worker 1:        Underlying      Worker 2:        Original
    BlockRead ---+--->  Encrypter   --->   Block   --->  Decrypter  ---> Completion
                /     Acts on writes       Device      Acts on reads      Callback
   BlockWrite -+
```
 

The "encrypter" worker encrypts the data in every I/O write request before sending it to the underlying block device, and the "decrypter" worker decrypts the data in every I/O read responsecoming from the underlying block device.  The[cipher](/zircon/system/ulib/crypto/include/crypto/cipher.h) must have a key length of at least 16 bytes,be semantically secure ([IND-CCA2][ind-cca2]) and incorporate the block offset as a"[tweak][tweak]".  Currently, [AES256-XTS][aes-xts] is in use. “加密程序”工作程序在将每个I / O写入请求中的数据发送到基础块设备之前对其进行加密，而“解密程序”工作程序则对来自基础块设备的每个I / O读取响应中的数据进行解密。 [cipher]（/ zircon / system / ulib / crypto / include / crypto / cipher.h）的密钥长度必须至少为16个字节，并且在语义上是安全的（[IND-CCA2] [ind-cca2]）并包含块偏移量为“ [tweak] [tweak]”。当前，正在使用[AES256-XTS] [aes-xts]。

 
### Rings and Txns  铃声和TXNIn order to keep the encryption and decryption of data transparent to original I/O requester, the workers must copy the data when transforming it.  The I/O request sent through the pipeline is notactually the original request, but instead a "shadow" request that encapsulates the originalrequest. 为了使数据的加密和解密对原始I / O请求者透明，工作人员在转换数据时必须复制数据。通过管道发送的I / O请求实际上不是原始请求，而是封装原始请求的“影子”请求。

As shadow requests are needed, they are allocated backed sequentially by pages in the [VMO](/docs/concepts/kernel/concepts.md#shared-memory-virtual-memory-objects-vmos-).  When theworker needs to transform the data it either encrypts data from the original, encapsulated writerequest into the shadow request, or decrypts data from the shadow request into the original,encapsulated read request.  As soon as the original request can be handed back to the originalrequester, the shadow request is deallocated and its page [decommitted](/docs/reference/syscalls/vmo_op_range.md).This ensures no more memory is used than is needed for outstanding I/O requests. 当需要影子请求时，它们由[VMO]（/ docs / concepts / kernel / concepts.mdshared-memory-virtual-memory-objects-vmos-）中的页面按顺序分配。当工作人员需要转换数据时，它要么将来自原始封装的writerequest的数据加密为影子请求，要么将来自影子请求的数据解密为原始的封装读请求。一旦原始请求可以交还给原始请求者，影子请求就会被释放，并且其页面[已提交]（/ docs / reference / syscalls / vmo_op_range.md）。这确保未使用的内存不超过未完成的内存。 I / O请求。

 
### Superblock Format  超级块格式The key material for encrypting and decrypting the data is referred to as the data key, and is stored in a reserved portion of the device called the `superblock`. The presence of this superblockis critical; without it, it is impossible to recreate the data key and recover the data on thedevice.  As a result, the superblock is copied to multiple locations on the device for redundancy.These locations are not visible to zxcrypt block device consumers.  Whenever the zxcrypt driversuccessfully reads and validates a superblock from one location, it will copy this to all othersuperblock locations to help "self-heal" any corrupted superblock locations. 用于加密和解密数据的密钥材料称为数据密钥，并存储在设备的“超级块”的保留部分中。这个超级区块的存在至关重要。没有它，就无法重新创建数据密钥并恢复设备上的数据。结果，超级块被复制到设备上的多个位置以实现冗余.zxcrypt块设备使用方看不到这些位置。每当zxcrypt驱动程序成功从一个位置读取并验证超级块时，它将把它复制到所有其他超级块位置，以帮助“自我修复”任何损坏的超级块位置。

The superblock format is as follows, with each field described in turn:  超块格式如下，每个字段依次描述：

```
+----------------+----------------+----+-----...-----+----...----+------...------+
| Type GUID      | Instance GUID  |Vers| Sealed Key  | Reserved  | HMAC          |
| 16 bytes       | 16 bytes       | 4B | Key size    |    ...    | Digest length |
+----------------+----------------+----+-----...-----+----...----+------...------+
```
 

 
* _Type [GUID][guid]_: Identifies this as a zxcrypt device. Compatible with [GPT](/zircon/system/ulib/gpt/include/gpt/gpt.h). * _Type [GUID] [guid] _：将其标识为zxcrypt设备。与[GPT]（/ zircon / system / ulib / gpt / include / gpt / gpt.h）兼容。
* _Instance GUID_: Per-device identifier, used as the KDF salt as explained below.  * _Instance GUID_：每个设备的标识符，用作KDF盐，如下所述。
* _Version_: Used to indicate which cryptographic algorithms to use.  * _Version_：用于指示要使用的加密算法。
* _Sealed Key_: The data key, encrypted by the wrap key as describer below.  * _Sealed Key_：数据密钥，由包装密钥加密，如下所述。
* _Reserved_: Unused data to align the superblock with the block boundary.  * _Reserved_：未使用的数据，以使超级块与块边界对齐。
* [_HMAC_][hmac]: A keyed digest of the superblock up to this point (including the Reserved field).  * [_HMAC _] [hmac]：至此的超级块的带键摘要（包括Reserved字段）。

The wrap key, wrap [IV][iv], and HMAC key are all derived from a [KDF](/zircon/system/ulib/crypto/include/crypto/hkdf.h).  This KDF is an [RFC 5869 HKDF][hkdf], whichcombines the key provided, the "salt" of the instance GUID and a per-use label such as "wrap" or"hmac".  The KDF does __NOT__ try to do any rate-limiting.  The KDF mitigates the risk of key reuse,as a new random instance salt will lead to new derived keys.  The[HMAC](/zircon/system/ulib/crypto/include/crypto/hmac.h) prevents accidental or malicious modification togo undetected, without leaking any useful information about the zxcrypt key. 包装密钥，包装[IV] [iv]和HMAC密钥均从[KDF]（/ zircon / system / ulib / crypto / include / crypto / hkdf.h）派生。此KDF是[RFC 5869 HKDF] [hkdf]，它将提供的密钥，实例GUID的“盐”和按使用的标签（例如“ wrap”或“ hmac”）组合在一起。 KDF __NOT__尝试进行任何速率限制。 KDF降低了密钥重用的风险，因为新的随机实例盐将导致新的派生密钥。 [HMAC]（/ zircon / system / ulib / crypto / include / crypto / hmac.h）可防止意外或恶意修改未被发现，而不会泄漏有关zxcrypt密钥的任何有用信息。

_NOTE: The KDF does __NOT__ do any [key stretching][stretch].  It is assumed that an attacker can remove a device and attempt the key derivations on their own, bypassing the HMAC check and anypossible rate limits.  To prevent this, zxcrypt consumers should include properly rate-limiteddevice keys, e.g. those from a [TPM][tpm], in deriving their zxcrypt key._ _注意：KDF __NOT__不做任何[键拉伸] [拉伸]。假定攻击者可以绕过HMAC检查和任何可能的速率限制，自行删除设备并尝试密钥派生。为避免这种情况，zxcrypt使用者应包括正确的速率限制设备密钥，例如来自[TPM] [tpm]的用户，以获取其zxcrypt密钥。

 
## Future Work  未来的工作There are a number of areas where further work could, should, or must be done:  在许多领域可以，应该或必须做进一步的工作：
* __Surface hidden bind failures__  * __表面隐藏绑定失败__

  Currently, `zxcrypt_bind` may indicate success even though the device fails to initialize. zxcrypt is __NOT__ synchronously adding the device to the device tree when the binding logic isrun.  It must do I/O and cannot block the call to `device_bind` from returning, so it spawn aninitializer thread and adds the device when complete. 当前，即使设备未能初始化，“ zxcrypt_bind”也可能指示成功。绑定逻辑运行时，zxcrypt __NOT__将设备同步添加到设备树中。它必须执行I / O操作，并且不能阻止对device_bind的调用返回，因此它会生成一个初始化程序线程，并在完成时添加设备。

  As of 10/2017, this is an active area of DDK development and the policy is changing to requiring the device to be added before return, with an additional call to publish that may come later.With this it may be desirable to have the call to `zxcrypt_bind` block synchronously for callersuntil the device is ready or has unambiguously failed to bind. 从10/2017开始，这是DDK开发的活跃领域，并且策略正在更改为要求在返回之前添加设备，并可能在稍后发布额外的发布请求。在设备准备就绪或明确绑定失败之前，将“ zxcrypt_bind”同步阻止给调用方。

 
* __Use AEAD instead of AES-XTS__  * __使用AEAD代替AES-XTS__

  It is widely recognized that [AEADs][aead] provide superior cryptographic protection by validating the integrity of their data before decrypting it.  This is desirable, but requires additionalper-block overhead.  This means either that consumers will need to consume non-page-aligned blocks(once the in-line overhead is removed), or zxcrypt will need to store the overhead out-of-line andhandle [non-atomic write failures][atomic]. 众所周知，[AEADs] [aead]通过在解密之前验证其数据的完整性来提供出色的密码保护。这是理想的，但需要额外的每块开销。这意味着要么消费者将需要消耗非页面对齐的块（一旦消除了内联开销），要么zxcrypt将需要脱机存储开销并处理[非原子写入失败] [原子] 。

 
* __Support multiple keys__  * __支持多个键__

  To facilitate [key escrow and/or recovery][escrow], it is straightforward to modify the superblock format to have a series of cryptographic envelopes.  In anticipation of this, the libzxcrypt APItakes a variable number of keys, although the only length currently supported is 1, and the onlyvalid slot is 0. 为了促进[密钥托管和/或恢复] [托管]，直接修改超级块格式以具有一系列密码信封是很简单的。以此为依据，尽管当前支持的唯一长度是1，唯一有效的插槽是0，但libzxcrypt API会采用可变数量的密钥。

 
* __Adjust number of workers__  * __调整工人数__

  Currently there is one encrypter and one decrypter.  These are designed to work with an arbitrary number of threads, so performance tuning may be need to find the optimal number of workers thatbalances I/O bandwidth with [scheduler churn][thrash]. 当前有一个加密器和一个解密器。它们被设计为与任意数量的线程一起使用，因此可能需要进行性能调整，以找到可与[scheduler churn] [thrash]平衡I / O带宽的最佳工作线程数。

 
* __Remove internal checks__  * __删除内部检查__

  Currently, the zxcrypt code checks for many errors conditions at internal boundaries and returns informative errors if those conditions aren't met.  For performance, those that arise fromprogrammer error only and not data from either the requester or underlying device could beconverted to "debug" assertions that are skipped in release mode. 当前，zxcrypt代码在内部边界检查许多错误情况，如果不满足这些条件，则返回信息错误。为了提高性能，那些仅由程序员错误引起的错误而不是来自请求者或基础设备的数据的错误可以转换为在发布模式下跳过的“调试”声明。

