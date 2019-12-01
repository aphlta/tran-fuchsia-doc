 
# Bootsvc  Bootsvc 

`bootsvc` is (typically) the first program loaded by usermode (contrast with [userboot](userboot.md), which is loaded by the kernel).  `bootsvc` providesseveral system services: “ bootsvc”（通常）是usermode加载的第一个程序（与[userboot]（userboot.md）相比，后者是由内核加载的）。 bootsvc提供了几种系统服务：

 
- A filesystem service with the contents of the bootfs (/boot)  -具有bootfs（/ boot）内容的文件系统服务
- A loader service that loads from that bootfs  -从该bootfs加载的加载程序服务

