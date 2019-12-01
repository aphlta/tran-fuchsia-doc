 
## Remote management of NUC devices  NUC设备的远程管理 

To enable remote management, including KVM, you need to configure Intel AMT (Active Management Technology).  要启用包括KVM在内的远程管理，您需要配置Intel AMT（主动管理技术）。

Note: This assumes you're using NUC connected to the EdgeRouter. If your networking setup is different, you may need a different networkconfiguration. 注意：这假定您正在使用连接到EdgeRouter的NUC。如果网络设置不同，则可能需要不同的网络配置。

 
1. Enter Intel ME settings by pressing Ctrl+P on the boot screen.  1.在启动屏幕上按Ctrl + P，输入Intel ME设置。
    + The first time you need to set a password, the default one is "admin". Password must be at least 8 characters long, contain both lowercase and uppercase characters, at least onedigit and at least one non alpha-numeric character. +首次需要设置密码时，默认密码为“ admin”。密码必须至少包含8个字符，同时包含小写和大写字母，至少一位数字和至少一位非字母数字字符。

 
1. Configure network  1.配置网络
    + Go to Network Setup > TCP/IP Settings > Wired LAN IPV4 Configuration.  +转到网络设置> TCP / IP设置>有线LAN IPV4配置。
    + Disable __DHCP Mode__ and set a static __IPV4 Address__.  +禁用__DHCP模式__并设置静态__IPV4地址__。
    + Return to AMT Configuration and enable __Activate Network Access__.  +返回AMT配置并启用__激活网络访问__。
    + Exit Intel ME settings and save your changes.  +退出Intel ME设置并保存您的更改。

 
#### Enabling Intel AMT or vPro KVM  启用Intel AMT或vPro KVM 

The Intel AMT or vPro KVM needs to be enabled before use. These are enabled using the `wsman` command-line utility. 使用前需要启用Intel AMT或vPro KVM。这些是使用“ wsman”命令行实用程序启用的。

These instructions assume you have set the `AMT_HOST` variable which contains the IPv4 address you configured in the Intel ME settings,In these instructions, `AMT_PASSWORD` is the Intel ME password and `VNC_PASSWORD`is the VNC password. 这些说明假定您已设置了“ AMT_HOST”变量，该变量包含您在Intel ME设置中配置的IPv4地址。在这些说明中，“ AMT_PASSWORD”是Intel ME密码，而“ VNC_PASSWORD”是VNC密码。

Note: Password must be _exactly_ 8 characters long, contain both lowercase and uppercase characters, at least one digit and at least one non alpha-numericcharacter. 注意：密码必须为_exactly_ 8个字符长，同时包含小写和大写字母，至少一位数字和至少一位非字母数字字符。

 
1. Set the VNC password:  1.设置VNC密码：

   ```
   wsman put http://intel.com/wbem/wscim/1/ips-schema/1/IPS_KVMRedirectionSettingData -h ${AMT_HOST} -P 16992 -u admin -p ${AMT_PASSWORD} -k RFBPassword=${VNC_PASSWORD}
   ```
 

 
2. Enable KVM redirection to port 5900:  2.启用KVM重定向到端口5900：

   ```
   wsman put http://intel.com/wbem/wscim/1/ips-schema/1/IPS_KVMRedirectionSettingData -h ${AMT_HOST} -P 16992 -u admin -p ${AMT_PASSWORD} -k Is5900PortEnabled=true
   ```
 

 
3. Disable opt-in policy (do not ask user for console access):  3.禁用选择加入策略（不要要求用户进行控制台访问）：

   ```
   wsman put http://intel.com/wbem/wscim/1/ips-schema/1/IPS_KVMRedirectionSettingData -h ${AMT_HOST} -P 16992 -u admin -p ${AMT_PASSWORD} -k OptInPolicy=false
   ```
 

 
4. Disable session timeout:  4.禁用会话超时：

   ```
   wsman put http://intel.com/wbem/wscim/1/ips-schema/1/IPS_KVMRedirectionSettingData -h ${AMT_HOST} -P 16992 -u admin -p ${AMT_PASSWORD} -k SessionTimeout=0
   ```
 

 
5. Enable KVM:  5.启用KVM：

   ```
   wsman invoke -a RequestStateChange http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_KVMRedirectionSAP -h ${AMT_HOST} -P 16992 -u admin -p ${AMT_PASSWORD} -k RequestedState=2
   ```
 

