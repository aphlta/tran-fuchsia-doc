 
# Architecture Support  架构支持 

Fuchsia supports two ISAs: arm64 and x86-64.  紫红色支持两种ISA：arm64和x86-64。

 
## arm64  臂64 

Fuchsia supports arm64 (also called AArch64) with no restrictions on supported microarchitectures. 紫红色支持arm64（也称为AArch64），而不受支持的微体系结构的限制。

 
## x86-64  x86-64 

Fuchsia supports x86-64 (also called IA32e or AMD64), but with some restrictions on supported microarchitectures. 紫红色支持x86-64（也称为IA32e或AMD64），但对受支持的微体系结构有一些限制。

 
### Intel  英特尔 

For Intel CPUs, only Broadwell and later are actively supported and will have new features added for them.  Additionally, we will accept patches to keep Nehalem and later booting.  对于Intel CPU，仅积极支持Broadwell和更高版本，并将为其添加新功能。此外，我们将接受修补程序以保留Nehalem并在以后引导。

 
### AMD  AMD公司 

