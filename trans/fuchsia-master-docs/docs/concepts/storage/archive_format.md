 
# Fuchsia Archive Format  紫红色档案格式 

 
## Overview  总览 

The Fuchsia Archive format is a format for storing a directory tree in a file. Like a `.tar` or `.zip` file, a Fuchsia Archive file stores a mappingfrom path names to file contents. 紫红色档案格式是一种用于在文件中存储目录树的格式。与.tar或.zip文件一样，紫红色档案文件存储从路径名到文件内容的映射。

Fuchsia Archive files are sometimes referred to as FARs or FAR archives, and are given the filename extension `.far`. 紫红色档案文件有时被称为FAR或FAR档案，并且文件扩展名为`.far`。

 
## Format  格式 

An archive is a sequence of bytes, divided into chunks:  档案是一个字节序列，分为多个块：

 
 * The first chunk is the index chunk, which describes where other chunks are located in the archive. *第一个块是索引块，它描述了其他块在归档中的位置。
 * All the chunks listed in the index must appear in the archive in the order listed in the index (which is sorted by their type). *索引中列出的所有块必须按照索引中列出的顺序（按其类型排序）出现在归档中。
 * The archive may contain additional chunks that are not referenced in the index, but these chunks must appear in the archive after all the chunkslisted in the index. For example, content chunks are not listed in theindex. Instead, the content chunks are reachable from the directory chunk. *归档文件可能包含索引中未引用的其他块，但是这些块必须在索引中列出的所有块之后出现在归档文件中。例如，内容块未在索引中列出。而是可以从目录块访问内容块。
 * The chunks must not overlap.  *块不得重叠。
 * All chunks are aligned on 64 bit boundaries.  *所有块都在64位边界上对齐。
 * All chunks must be packed as tightly as possible subject to their alignment constraints. *所有大块必须根据其对齐约束尽可能紧密地打包。
 * Any gaps between chunks must be filled with zeros.  *块之间的任何间隙都必须用零填充。

All offsets and lengths are encoded as unsigned integers in little endian.  所有偏移量和长度都以little endian编码为无符号整数。

 
## Index chunk  索引块 

The index chunk is required and must start at the beginning of the archive.  索引块是必需的，并且必须从存档的开头开始。

 
 * 8 bytes of magic.  * 8字节的魔术。
    - Must be 0xc8 0xbf 0x0b 0x48 0xad 0xab 0xc5 0x11.  -必须为0xc8 0xbf 0x0b 0x48 0xad 0xab 0xc5 0x11。
 * 64 bit length of concatenated index entries, in bytes.  *串联索引条目的64位长度，以字节为单位。
 * Concatenated index entries.  *串联索引条目。

No two index entries can have the same type and the entries must be sorted by type in increasing lexicographical octet order (e.g., as compared by memcmp).The chunks listed in the index must be stored in the archive in the order listedin the index. 不能有两个索引条目具有相同的类型，并且条目必须按字典的八位字节递增顺序按类型排序（例如，与memcmp比较）。索引中列出的块必须按照索引中列出的顺序存储在归档中。

 
### Index entry  索引输入 

 
 * 64 bit chunk type.  * 64位块类型。
 * 64 bit offset from start of the archive to the start of the referenced chunk, in bytes. *从存档的开始到引用的块的开始的64位偏移量（以字节为单位）。
 * 64 bit length of referenced chunk, in bytes.  *引用块的64位长度，以字节为单位。

 
## Directory chunk (Type "DIR-----")  目录块（类型“ DIR -----”） 

The directory chunk is required.  Entries in the directory chunk must have unique names and the entries must be sorted by name in increasinglexicographical octet order (e.g., as compared by memcmp). 目录块是必需的。目录块中的条目必须具有唯一的名称，并且条目必须按名称按字典序八位字节的递增顺序排序（例如，与memcmp进行比较）。

 
 * Concatenated directory table entries.  *串联目录表条目。

These entries represent the files contained in the archive. Directories themselves are not represented explicitly, which means archives cannot representempty directories. 这些条目代表存档中包含的文件。目录本身没有明确表示，这意味着归档文件不能表示空目录。

 
### Directory table entry  目录表条目 

 
 * Name.  * 名称。
    - 32 bit offset from the start of the directory names chunk to the path data, in bytes. -从目录名称块的开始到路径数据的32位偏移量（以字节为单位）。
    - 16 bit length of name, in bytes.  -名称的16位长度，以字节为单位。
 * 16 bits of zeros, reserved for future use.  * 16位零，保留供将来使用。
 * Data.  *数据。
    - 64 bit offset from start of archive to the start of the content chunk, in bytes. -从存档开始到内容块开始的64位偏移量（以字节为单位）。
    - 64 bit length of the data, in bytes.  -数据的64位长度，以字节为单位。
 * 64 bits of zeros, reserved for future use.  * 64位零，保留供将来使用。

 
## Directory names chunk (Type "DIRNAMES")  目录名称块（类型“ DIRNAMES”） 

The directory names chunk is required and is used by the directory chunk to name the content chunks. Path data must be sorted in increasing lexicographicaloctet order (e.g., as compared by memcmp). 目录名称块是必需的，目录块使用它来命名内容块。路径数据必须按字典顺序的八位字节顺序递增排序（例如，与memcmp进行比较）。

 
 * Concatenated path data (no encoding specified).  *串联的路径数据（未指定编码）。
 * Zero padding to next 8 byte boundary.  *零填充到下一个8字节边界。

Note: The offsets used to index into the path data are 32 bits long, which means there is no reason to create a directory name chunk that is larger than 4 GB. 注意：用于索引路径数据的偏移量为32位长，这意味着没有理由创建大于4 GB的目录名称块。

Although no encoding is specified, clients that wish to display path data using unicode may attempt to decode the data as UTF-8. The path data might or mightnot be UTF-8, which means that decoding might fail. 尽管未指定编码，但是希望使用unicode显示路径数据的客户端可能会尝试将数据解码为UTF-8。路径数据可能是UTF-8，也可能不是UTF-8，这意味着解码可能会失败。

 
### Path data  路径数据 

 
 * Octets of path.  *路径的八位字节。
    - Must not be empty.  -不能为空。
    - Must not contain a 0x00 octet.  -不得包含0x00八位位组。
    - The leading octet must not be 0x2F ('/').  -前导八位字节不得为0x2F（'/'）。
    - The trailing octet must not be 0x2F ('/').  -尾部八位位组不得为0x2F（'/'）。
    - Let *segments* be the result of splitting the path on 0x2F ('/'). Each segment must meet the following requirements: -假设* segments *是在0x2F（'/'）上分割路径的结果。每个细分市场必须满足以下要求：
       - Must not be empty.  -不能为空。
       - Must not be exactly 0x2E ('.')  -不能完全是0x2E（'。'）
       - Must not be exactly 0x2E 0x2E ('..')  -不能完全是0x2E 0x2E（'..'）

 
## Content chunk  内容块 

Content chunks must be after all the chunks listed in the index chunk. The content chunks must appear in the archive in the order they are listed in thedirectory. 内容块必须位于索引块中列出的所有块之后。内容块必须按照目录中列出的顺序出现在归档中。

 
 * data  *数据

