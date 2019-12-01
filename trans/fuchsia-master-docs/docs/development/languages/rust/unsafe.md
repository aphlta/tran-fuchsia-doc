 
# Unsafe code in Rust  Rust中的不安全代码 

 

`unsafe` is a dangerous but sometimes necessary escape hatch in Rust. When writing or reviewing `unsafe` code, it's essential that you: “不安全”是Rust中的危险但有时是必要的逃生舱口。在编写或查看“不安全”代码时，请务必：

 
- clearly identify all of the assumptions and invariants required by every `unsafe` block; -明确指出每个“不安全”区块所需的所有假设和不变量；
- ensure that those assumptions are met;  -确保符合这些假设；
- ensure that those assumptions will *continue* to be met.  -确保这些假设将*继续*得到满足。

In order to ensure that `unsafe` invariants are not broken by future editors, each usage of `unsafe` must be accompanied by a clear, concise commentexplaining what assumptions are being made. 为了确保将来的编辑者不会破坏“不安全”的不变量，每次使用“不安全”时都必须附有清晰简明的注释，解释正在做的假设。

Where possible, package up unsafety into a single function or module which provides a safe abstraction to the outside world. FFI calls should usuallybe exposed through a safe function whose only purpose is to provide a safewrapper around the function in question. These functions should containa comment with the following information (if applicable): 在可能的情况下，将不安全性打包到单个函数或模块中，以向外界提供安全的抽象。 FFI调用通常应通过安全功能公开，该安全功能的唯一目的是为有关功能提供安全的包装。这些功能应包含带有以下信息的注释（如果适用）：

 
- Preconditions (e.g. what are the valid states of the arguments?)  -前提条件（例如，参数的有效状态是什么？）
- Failure handling (e.g. what values should be free'd? forgotten? invalidated?)  -失败处理（例如，应该释放哪些值，忘记了哪些值或使它们无效？）
- Success handling (e.g. what values are created or consumed?)  -成功处理（例如，创建或使用了哪些值？）

Example:  例：

```rust
impl Channel {
    /// Write a message to a channel. Wraps the
    /// [zx_channel_write](//docs/zircon/syscalls/channel_write.md)
    /// syscall.
    pub fn write(&self, bytes: &[u8], handles: &mut Vec<Handle>)
            -> Result<(), Status>
    {
        let opts = 0;
        let n_bytes = try!(usize_into_u32(bytes.len()).map_err(|_| Status::OUT_OF_RANGE));
        let n_handles = try!(usize_into_u32(handles.len()).map_err(|_| Status::OUT_OF_RANGE));

        // Requires that `self` contains a currently valid handle or ZX_HANDLE_INVALID.
        // On success, all of the handles in the handles array have been moved.
        // They must be forgotten and not dropped.
        // On error, all handles are still owned by the current process and can be dropped.
        unsafe {
            let status = sys::zx_channel_write(self.raw_handle(), opts, bytes.as_ptr(), n_bytes,
                handles.as_ptr() as *const sys::zx_handle_t, n_handles);
            ok(status)?;
            // Handles were successfully transferred, forget them on sender side
            handles.set_len(0);
            Ok(())
        }
    }
}
```
 

If `unsafe` code relies on other safe code for correctness, a comment must be left alongside the corresponding safe code indicating what invariantsit must uphold and why. Invariants that rely upon the behavior of multiplefunctions will draw extra scrutiny, and cross-module or cross-crate unsafetyrequires even more attention. `unsafe` code that depends on correct behavior ofa third-party crate will likely be rejected, and `unsafe` code that dependsupon the internal representation details of third-party types will _never_ beaccepted. 如果`unsafe`代码依赖于其他安全代码来确保正确性，则必须在相应的安全代码旁边留下一个注释，指示其必须坚持哪些不变性以及原因。依赖多功能行为的不变量将引起更多的审查，并且跨模块或跨板条箱的不安全性需要更多的关注。依赖于第三方包装箱正确行为的“不安全”代码可能会被拒绝，而依赖于第三方类型的内部表示详细信息的“不安全”代码将被拒绝。

Finally, `struct` definitions containing `unsafe` types such as `*const`, `*mut`, or `UnsafeCell` must include a comment explaining the internalrepresentation invariants of the type. If the `unsafe` type is used to performa mutation OR if it aliases with memory inside another type, there should bean explanation of how it upholds Rust's "aliasing XOR mutation" requirements.If any `derive`able traits are purposefully omitted for safety reasons, acomment must be left to prevent future editors from adding the unsafe impls. 最后，包含“ * const”，“ * mut”或“ UnsafeCell”等“ unsafe”类型的“ struct”定义必须包含注释，以解释该类型的内部表示不变量。如果使用`unsafe`类型来执行突变，或者如果它使用另一种类型内的内存作为别名，则应使用bean解释其如何支持Rust的“别名XOR突变”要求。 ，必须留下注释，以防止以后的编辑者添加不安全的提示。

The rules above are applied to any additions of `unsafe` code or any modifications of existing `unsafe` code. 以上规则适用于“不安全”代码的任何添加或对现有“不安全”代码的任何修改。

For more discussion on encapsulating `unsafe` invariants, see [Ralf Jung's "The Scope of Unsafe"][scope-of-unsafe] and[Niko Matsakis's "Tootsie Pop" model][tootsie-pop]. 有关封装“不安全”不变量的更多讨论，请参见[Ralf Jung的“不安全范围”] [不安全范围]和[Niko Matsakis的“ Tootsie Pop”模型] [tootsie-pop]。

 

