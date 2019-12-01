 
# Fuchsia Merkle Roots  紫红色的默克尔根 

[Merkle Trees][merkletree] are used in various places in the Fuchsia ecosystem, including the [FAR Archive Format][far], the Blob Storage Filesystem, and the[Package Manager][pm]. [Merkle Trees] [merkletree]在紫红色的生态系统中的各个地方使用，包括[FAR存档格式] [far]，Blob存储文件系统和[Package Manager] [pm]。

In [Zircon][zircon] `zx-verity` provides an API for application components to read data from local storage. When retrieving data the integrity of the data isverified and causing reads to fail when the data has been modified or corrupted.zx-verity is based on a [Merkle Tree][merkletree], and is derived from a similarsystem in [Chrome OS][dmverity]. 在[Zircon] [zircon]中，`zx-verity`提供了一个API，供应用程序组件从本地存储读取数据。检索数据时，将验证数据的完整性，并在数据被修改或损坏时导致读取失败。zx-verity基于[Merkle Tree] [merkletree]，并源自[Chrome OS]中的类似系统[ dmverity]。

All of these implementations share the algorithm documented herein.  所有这些实现都共享此处记录的算法。

 
## Parameters of the Merkle Tree  Merkle树的参数 

 
 * Block size: 8kb, 0 padded.  *块大小：8kb，0填充。
 * Root digest size: 32 bytes.  *根摘要大小：32个字节。
 * Hash algorithm: SHA-256.  *哈希算法：SHA-256。
 * Block digest computation: SHA-256(u64(offset | level) + u32(length) + data)  *块摘要计算：SHA-256（u64（偏移量|水平）+ u32（长度）+数据）

 
## Definitions  定义 

The merkle tree contains levels. A level is a row of the tree, starting at 0 and counting upward. Level 0 represents the level that contains hashes of chunks ofthe input stream. merkle树包含级别。级别是树的一行，从0开始并向上计数。级别0表示包含输入流的大块哈希值的级别。

Each level contains a number of hashes of the previous level. The hashes within a level are computed from 8kb blocks from the previous level (or data, if level0), prepended with a block identity. 每个级别包含多个先前级别的哈希。某个级别中的哈希值是根据前一个级别的8kb块（或数据（如果为level0））计算的，并以块标识开头。

A block identity is the binary OR of the starting byte index of the block within the current level and the current level index, followed by the length of theblock. For level 0, the length of the block is 8kb, except for the last block,which may be less than 8kb. All other levels use a length of 8kb, even when thelast block is 0 padded. 块标识是当前级别和当前级别索引内该块的起始字节索引的二进制或，后跟该块的长度。对于级别0，块的长度为8kb，最后一个块除外，该长度可能小于8kb。所有其他级别都使用8kb的长度，即使最后一个块为0填充也是如此。

 
## Computation of a level  水平计算 

 
 1. Initialize the level with an index, an offset starting at 0, and an empty list of hashes. 1.用一个索引，一个从0开始的偏移量和一个空的哈希表初始化该级别。
 2. For each 8kb (or remainder of) of input, compute the next block identity by taking the binary OR of the level index and the current offset, followedby the length of the input. 2.对于输入的每8kb（或其余部分），通过采用电平索引和当前偏移量的二进制或，再加上输入的长度，计算下一个块标识。
 3. Init a SHA-256 digest, append to it the identity, the input, and if the input is shorter than 8kb, a pad of 0 up to 8kb. 3.初始化一个SHA-256摘要，在其后附加身份，输入，如果输入少于8kb，则填充0到8kb。
 4. Append the output of the digest to the level's list of hashes. Increment the offset by the input length. 4.将摘要的输出追加到该级别的哈希列表中。将偏移量增加输入长度。
 5. Repeat 1-4 until all input is consumed.  5.重复1-4，直到消耗完所有输入。
 6. If the length of hashes is 32, finish.  6.如果散列的长度是32，则结束。
 7. If the length of hashes is not 8kb aligned, 0 fill up to an 8kb alignment and compute more levels until there is a root level containing asingle 32 byte digest. 7.如果哈希的长度不是8kb对齐的，则0填充到8kb对齐，并计算更多级别，直到根级别包含单个32字节摘要。

 
## Computation of a root digest  根摘要的计算 

Compute level 0 with the input data. Construct and compute subsequent levels using the previous level hashes as input data, until a level hashes containsexactly 32 bytes. This last level contains the root digest of the merkle tree. 使用输入数据计算级别0。使用先前的级别哈希作为输入数据来构造和计算后续级别，直到一个级别哈希包含正好32个字节为止。最后一级包含merkle树的根摘要。

 
## A note about the empty digest  关于空摘要的说明 

As a special case, when there is no input data, implementations may need to handle the calculation independently. The digest of the empty input is simplythe SHA-256 of 12 0 bytes, the block identity of a single 0 length block. 作为一种特殊情况，当没有输入数据时，实现可能需要独立处理计算。空输入的摘要就是12个0字节的SHA-256，即单个0长度块的块标识。

 
## Example values  值示例 

 
 * The empty digest: `15ec7bf0b50732b49f8228e07d24365338f9e3ab994b00af08e5a3bffe55fd8b` *空摘要：`15ec7bf0b50732b49f8228e07d24365338f9e3ab994b00af08e5a3bffe55fd8b`
 * 8192 bytes of `0xff` - "oneblock" `68d131bc271f9c192d4f6dcd8fe61bef90004856da19d0f2f514a7f4098b0737` * 8192个字节的'0xff`-“ oneblock”`68d131bc271f9c192d4f6dcd8fe61bef90004856da19d0f2f514a7f4098b0737`
 * 65536 bytes of `0xff` - "small" `f75f59a944d2433bc6830ec243bfefa457704d2aed12f30539cd4f18bf1d62cf` * 65536字节的'0xff`-“ small”`f75f59a944d2433bc6830ec243bfefa457704d2aed12f30539cd4f18bf1d62cf`
 * 2105344 bytes of `0xff` - "large" `7d75dfb18bfd48e03b5be4e8e9aeea2f89880cb81c1551df855e0d0a0cc59a67` * 2105344个字节的`0xff`-“大”`7d75dfb18bfd48e03b5be4e8e9aeea2f89880cb81c1551df855e0d0a0cc0a59`
 * 2109440 bytes of `0xff` - "unaligned" `7577266aa98ce587922fdc668c186e27f3c742fb1b732737153b70ae46973e43` * 2109440个字节的``0xff''-``未对齐''`7577266aa98ce587922fdc668c186e27f3c742fb1b732737153b70ae46973e43`
 * `0xff0080` bytes filled with repetitions of `0xff0080` - "fuchsia" `2feb488cffc976061998ac90ce7292241dfa86883c0edc279433b5c4370d0f30` *`0xff0080`字节填充了`0xff0080`-“紫红色”的重复项。2feb488cffc976061998ac90ce7292241dfa86883c0edc279433b5c4370d0f30`

 

