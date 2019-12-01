 
# Errors  失误 

This describes the set of userspace-exposed errors used in Zircon. The first section provides the canonical names and description of each error code. The second section provides the concrete values. 这描述了Zircon中使用的用户空间暴露的错误集。第一部分提供每个错误代码的规范名称和描述。第二部分提供了具体的值。

Within the kernel, errors are typically resulted as variables of type `status_t` and errors are defined by macros of the form `ZX_ERR_CANONICAL_NAME` e.g. `ZX_ERR_INTERNAL`. All error cases are negativevalues and success is represented by a non-negative value. 在内核中，错误通常是由于类型为status_t的变量导致的，并且错误由格式为ZX_ERR_CANONICAL_NAME的宏定义，例如ZX_ERR_INTERNAL。所有错误情况均为负值，而成功则由非负值表示。

In userspace the syscall dispatch layer (libzircon) exposes the result values as variables of type `zx_status_t` that currently use the same spelling and values as the kernel for errors, but whichwill transition to using 0 for success and positive values for errors. 在用户空间中，系统调用调度层（libzircon）将结果值显示为类型为zx_status_t的变量，该变量当前使用与内核相同的拼写和值来表示错误，但是将转换为使用0表示成功，使用正值表示错误。

See [Kernel internal errors](kernel_internal_errors.md) for a list of kernel-internal values.  有关内核内部值的列表，请参见[内核内部错误]（kernel_internal_errors.md）。

 
## Descriptions  内容描述 

Each category represents a class of errors. The first error code in each category is the generic code for that category and is used when no more specific code applies. Further error codes (if any)within a category represent particular types of errors within the class. In general, more specificerror codes are preferred where possible. 每个类别代表一类错误。每个类别中的第一个错误代码是该类别的通用代码，并且在没有其他特定代码适用时使用。类别中的其他错误代码（如果有）表示该类中的特定类型的错误。通常，在可能的情况下，首选更具体的错误代码。

Errors are described in terms of an operation, arguments, a subject, and identifiers. An operation is typically a function or system call. Arguments are typically the parameters to the call. Thesubject of an operation is the primary object the operation acts on, typically a handle andtypically passed as the first argument. Identifiers are typically numbers or strings intended tounambiguously identify a resource used in the operation. 错误是根据操作，参数，主题和标识符来描述的。操作通常是函数或系统调用。参数通常是调用的参数。操作的对象是操作操作的主要对象，通常是通常通常作为第一个参数传递的句柄。标识符通常是旨在明确标识操作中使用的资源的数字或字符串。

 
## Categories  分类目录 

 
### Success  成功**ZX\_OK** Operation succeeded. ** ZX \ _OK **操作成功。

 
### General errors  一般错误 

These indicate that the system hit a general error while attempting the operation.  这些指示系统在尝试操作时遇到一般错误。

**INTERNAL** The system encountered an otherwise unspecified error while performing the operation. **内部**在执行操作时，系统遇到了其他未指定的错误。

**NOT\_SUPPORTED** The operation is not supported, implemented, or enabled. **否\ _SUPPORTED **不支持，未实现或未启用该操作。

**NO\_RESOURCES** The system was not able to allocate some resource needed for the operation. **否\ _RESOURCES **系统无法分配该操作所需的某些资源。

**NO\_MEMORY** The system was not able to allocate memory needed for the operation. **否\ _MEMORY **系统无法分配该操作所需的内存。

 
### Parameter errors  参数错误 

These indicate that the caller specified a parameter that does not specify a valid operation or that is invalid for the specified operation. 这些指示调用者指定了一个参数，该参数未指定有效操作或对该指定操作无效。

**INVALID\_ARGUMENT** An argument is invalid. ** INVALID \ _ARGUMENT **参数无效。

**WRONG\_TYPE** The subject of the operation is the wrong type to perform the operation.Example: Attempting a message\_read on a thread handle. ** WRONG \ _TYPE **操作的主题是执行该操作的类型错误。例如：尝试在线程句柄上读取一条消息\ _read。

**BAD\_SYSCALL** The specified syscall number is invalid. ** BAD \ _SYSCALL **指定的系统调用号无效。

**BAD\_HANDLE** A specified handle value does not refer to a handle. ** BAD \ _HANDLE **指定的句柄值未引用句柄。

**OUT\_OF\_RANGE** An argument is outside the valid range for this operation.Note: This is used when the argument may be valid if the system changes state, unlikeINVALID\_ARGUMENT which is used when the argument will never be valid. ** OUT \ _OF \ _RANGE **参数超出此操作的有效范围。注意：如果系统更改状态时该参数可能有效，则使用此参数，这与INVALID \ _ARGUMENT不同，INVALID \ _ARGUMENT在参数永远无效时使用。

**BUFFER\_TOO\_SMALL** A caller provided buffer is too small for this operation. ** BUFFER \ _TOO \ _SMALL **调用者提供的缓冲区对于此操作而言太小。

 
### Precondition or state errors  前提条件或状态错误 

These indicate that the operation could not succeed because the preconditions for the operation are not satisfied or the system is unable to complete the operation in its current state. 这些表明操作无法成功，因为操作的前提条件不满足或系统无法在其当前状态下完成操作。

**BAD\_STATE** The system is unable to perform the operation in its current state.Note: FAILED\_PRECONDITION is a reserved alias for this error ** BAD \ _STATE **系统无法在当前状态下执行操作。注意：FAILED \ _PRECONDITION是此错误的保留别名。

**NOT\_FOUND** The requested entity was not found. ** NOT \ _FOUND **找不到请求的实体。

**TIMED\_OUT** The time limit for the operation elapsed before the operation completed. ** TIMED \ _OUT **操作完成之前经过的时间限制。

**ALREADY\_EXISTS** An object with the specified identifier already exists.Example: Attempting to create a file when a file already exists with that name. ** ALREADY \ _EXISTS **具有指定标识符的对象已存在。例如：尝试使用该名称存在文件时尝试创建文件。

**ALREADY\_BOUND** The operation failed because the named entity is already owned or controlled by another entity.The operation could succeed later if the current owner releases the entity. ** ALREADY \ _BOUND **操作失败，因为命名实体已经由另一个实体拥有或控制。如果当前所有者释放该实体，则该操作可能会在以后成功。

**HANDLE\_CLOSED** A handle being waited on was closed. ** HANDLE \ _CLOSED **等待中的句柄已关闭。

**REMOTE\_CLOSED** The operation failed because the remote end of the subject of the operation was closed. ** REMOTE \ _CLOSED **操作失败，因为操作对象的远端已关闭。

**UNAVAILABLE** The subject of the operation is currently unable to perform the operation.Note: This is used when there's no direct way for the caller to observe when the subject will beable to perform the operation and should thus retry. **无法使用**该操作的对象当前无法执行该操作。注意：当调用者无法直接观察该对象何时可以执行该操作并应重试时，将使用此方法。

**SHOULD\_WAIT** The operation cannot be performed currently but potentially could succeed if the caller waits fora prerequisite to be satisfied, for example waiting for a handle to be readable or writable.Example: Attempting to read from a channel that has no messages waiting but has an openremote will return **SHOULD\_WAIT**. Attempting to read from a channel that has no messageswaiting and has a closed remote end will return **REMOTE\_CLOSED**. ** SHOULD \ _WAIT **该操作当前无法执行，但如果调用方等待满足先决条件（例如，等待句柄可读取或可写），则可能会成功执行。示例：尝试从没有任何内容的通道读取等待但有openremote的消息将返回** SHOULD \ _WAIT **。尝试从没有消息等待且具有封闭的远端的通道中读取将返回** REMOTE \ _CLOSED **。

 
### Permission errors  权限错误 

**ACCESS\_DENIED** The caller did not have permission to perform the specified operation. ** ACCESS \ _DENIED **呼叫者没有执行指定操作的权限。

 
### Input/output errors  输入/输出错误 

**IO** Otherwise unspecified error occurred during I/O. ** IO **否则在I / O期间发生未指定的错误。

**IO\_REFUSED** The entity the I/O operation is being performed on rejected the operation.Example: an I2C device NAK'ing a transaction or a disk controller rejecting an invalid command. ** IO \ _REFUSED **正在执行I / O操作的实体拒绝了该操作。例如：I2C设备NAK正在事务处理或磁盘控制器拒绝了无效命令。

**IO\_DATA\_INTEGRITY** The data in the operation failed an integrity check and is possibly corrupted.Example: CRC or Parity error. ** IO \ _DATA \ _INTEGRITY **操作中的数据未通过完整性检查，并且可能已损坏。例如：CRC或奇偶校验错误。

