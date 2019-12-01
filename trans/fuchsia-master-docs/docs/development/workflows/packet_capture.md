 
# Packet Capture on Fuchsia  紫红色的数据包捕获 

Packet capture is a fundamental tool for developing, debugging, and testing networking.  数据包捕获是用于开发，调试和测试网络的基本工具。

`fx sniff` is a development host command that:  fx sniff是一个开发主机命令，它可以：

 
* Runs the packet capture on the Fuchsia **target** device.  *在紫红色的目标设备上运行数据包捕获。
* Stores the packets in PCAPNG format on the Fuchsia development **host**.  *将数据包以PCAPNG格式存储在紫红色的开发主机上。
* Streams out to a graphical user interface such as `Wireshark`.  *流到图形用户界面，例如“ Wireshark”。

`netdump` is a packet capturer with rich capture filter support. `fx sniff` internally invokes `netdump` with predefined capture filters that are necessary for Fuchsia's developer workflow. For use cases where `fx sniff` is not viable (e.g. when you have serial console access but without dev host connected), use `netdump` directly.  netdump是具有丰富捕获过滤器支持的数据包捕获器。 fx sniff在内部使用Fuchsia开发人员工作流程必需的预定义捕获过滤器调用netdump。对于无法使用“ fx sniff”的用例（例如，当您具有串行控制台访问权限但未连接开发主机时），请直接使用“ netdump”。

 
## Prepare the image {#prepare-image}  准备图像{prepare-image} 

`netdump` is part of the [universe dependency list](/docs/development/build/boards_and_products.md#universe) of the core product. If a package server is available, there is no extra step to prepare the image. Just running `netdump` will fetch the binary.  netdump是核心产品[universe依赖项列表]（/ docs / development / build / boards_and_products.mduniverse）的一部分。如果有软件包服务器可用，则无需执行其他准备映像的步骤。仅运行`netdump`即可获取二进制文件。

If the package server is not available, make sure to bundle `netdump` into your set of base packages.  如果软件包服务器不可用，请确保将“ netdump”捆绑到基础软件包中。

```shell
$ fx set core.x64 --with-base //src/connectivity/network/netdump
$ fx build
```
 

 

 
## How-to (On Host)  操作方法（在主机上） 

 
### Capture packets over WLAN interface  通过WLAN接口捕获数据包 

```shell
[host] $ fx sniff wlan
```
 

By default, this command captures packets for 30 seconds. To configure the duration, add the `--time {sec}` or `-t {sec}` option.  缺省情况下，该命令捕获数据包的时间为30秒。要配置持续时间，请添加`--time {sec}`或`-t {sec}`选项。

If you don't know the network interface name, run `fx sniff` without options. The error message shows you what interfaces are available. Alternatively, run:  如果您不知道网络接口名称，请运行不带选项的`fx sniff`。该错误消息向您显示可用的接口。或者，运行：

```shell
[host] $ fx shell net if list       # Take note of `filepath` in output
```
 

 

 
### Show the hexdump of packets over the ethernet interface  显示通过以太网接口发送的数据包的十六进制转储 

```shell
[host] $ fx sniff --view hex eth
```
 

 
### Capture WLAN packets and store them in a file  捕获WLAN数据包并将其存储在文件中 

```shell
[host] $ fx sniff --file my_packets wlan
```
 

The captured packets are first stored in the target's `/tmp/` directory. After the capture is complete, the files are moved to `//out/my_packets.pcapng` automatically.  捕获的数据包首先存储在目标的`/ tmp /`目录中。捕获完成后，文件将自动移至“ //out/my_packets.pcapng”。

 
### Stream out to Wireshark in realtime  实时流式传输到Wireshark 

**_NOTE:_** Linux only.  ** _注意：_ **仅适用于Linux。

```shell
[host] $ fx sniff --view wireshark wlan
```
 

 
### Force stop  强制停止Packet capture runs for the specified duration (`--time` or `-t` option). If a user desires to stop early, presse one of the following keys:  数据包捕获以指定的持续时间运行（“ --time”或“ -t”选项）。如果用户希望提前停止，请按以下键之一：

```
c, q, C, Q
```
This will stop both a target side process and a host side process.  这将同时停止目标方过程和主机方过程。

 
## How-to (on target device)  操作方法（在目标设备上） 

 
### Use netdump for debugging  使用netdump进行调试 

`fx sniff` requires working `ssh` connectivity from the host to the target, which means that networking must be working to some degree. In some cases, networking might not be working at all. If you have access to the serial console while networking, including `ssh`, is not working, you must run `netdump` directly on the target. `netdump` provides a richer set of features than `fx sniff`.  “ fx sniff”需要从主机到目标的有效“ ssh”连接，这意味着网络必须在某种程度上起作用。在某些情况下，联网可能根本无法正常工作。如果在网络连接（包括ssh）不起作用时可以访问串行控制台，则必须直接在目标计算机上运行netdump。与`fx sniff`相比，`netdump`提供了更丰富的功能。

 
#### Prerequisites  先决条件 

Before you use `netdump`, you must get the file path for the network interface. This is an example for WLAN interface (assuming your target device has one and only one WLAN interface - which is a typical case).  在使用“ netdump”之前，您必须获取网络接口的文件路径。这是WLAN接口的示例（假设目标设备只有一个WLAN接口，这是典型的情况）。

```shell
[target] $ iface_filepath=$(net if list wlan | grep filepath | while read c1 c2; do echo $c2; done)
```
 

 
#### Capture packets over the WLAN interface  通过WLAN接口捕获数据包 

```shell
[target] $ netdump -t 30 "$iface_filepath"
```
 

 
#### Show the hexdump of packets over the ethernet interface  显示通过以太网接口发送的数据包的十六进制转储 

```shell
[target] $ netdump --raw "$iface_filepath"
```
 

 
#### Stream out the binary dump in PCAPNG format  以PCAPNG格式输出二进制转储 

```shell
[target] $ netdump --pcapdump ${iface_filepath}
```
 

 
#### Capture packets and store them in a file  捕获数据包并将其存储在文件中 

```shell
[target] $ netdump -t 30 -w /tmp/my_packets.pcapng "$iface_filepath"
```
 

 
#### Copy the dump file to the host  将转储文件复制到主机 

```shell
[host] $ cd ${FUCHSIA_OUT_DIR} && fx scp "[$(fx get-device-addr)]:/tmp/my_precious_packets.pcapng" .
```
 

 
#### `netdump` help  `netdump`帮助 

```shell
[target] $ netdump --help
```
 

 
#### Only Watch ARP, DHCP, and DNS packets  仅观看ARP，DHCP和DNS数据包 

```shell
[target] $ netdump -t 10 -f "arp or port dns,dhcp" "$iface_filepath"
```
 

 
## Full syntax for filters  过滤器的完整语法The packet filter language syntax is as follows. Keywords are in **bold**. Optional terms are in `[square brackets]`. Placeholders for literals are in `<angle brackets>`. Binary logical operators associate to the left. All keywords and port aliases should be in lower case.  包过滤器语言语法如下。关键字以粗体显示。可选术语在“ [方括号]”中。文字的占位符在“ <尖括号>”中。二进制逻辑运算符与左侧关联。所有关键字和端口别名均应小写。

<pre><code> expr ::= <b>(</b> expr <b>)</b>| <b>not</b> expr  | expr <b>and</b> expr | expr <b>or</b> expr| eth_expr  | host_expr     | trans_exprlength_expr ::= <b>greater</b> &lt;len&gt; | <b>less</b> &lt;len&gt;type ::= <b>src</b> | <b>dst</b>eth_expr ::= length_expr| <b>ether</b> [type] <b>host</b> &lt;mac_addr&gt;| [<b>ether</b> <b>proto</b>] net_exprnet_expr ::= <b>arp</b>| <b>vlan</b>| <b>ip</b>  [length_expr | host_expr | trans_expr]| <b>ip6</b> [length_expr | host_expr | trans_expr]host_expr ::= [type] <b>host</b> &lt;ip_addr&gt;trans_expr ::= [<b>proto</b>] <b>icmp</b>| [<b>proto</b>] <b>tcp</b> [port_expr]| [<b>proto</b>] <b>udp</b> [port_expr]| port_exprport_expr ::= [type] <b>port</b> &lt;port_lst&gt;</code></pre> <pre> <code> expr :: = <b>（</ b> expr <b>）</ b> | <b>不是</ b> expr | expr <b>和</ b> expr | expr <b>或</ b> expr | eth_expr | host_expr | trans_exprlength_expr :: = <b>更大</ b> lt; lengt; | <b> less </ b> lt; lengt; type :: = <b> src </ b> | <b> dst </ b> eth_expr :: = length_expr | <b> ether </ b> [type] <b> host </ b> lt; mac_addrgt; | [<b> ether </ b> <b> proto </ b>] net_exprnet_expr :: = <b> arp </ b> | <b> vlan </ b> | <b> ip </ b> [length_expr | host_expr | trans_expr] | <b> ip6 </ b> [length_expr | host_expr | trans_expr] host_expr :: = [类型] <b>主机</ b> lt; ip_addrgt; trans_expr :: = [<b> proto </ b>] <b> icmp </ b> | [<b> proto </ b>] <b> tcp </ b> [port_expr] | [<b> proto </ b>] <b> udp </ b> [port_expr] | port_exprport_expr :: = [类型] <b>端口</ b> lt; port_lstgt; </ code> </ pre>

 
*   `<len>`: Packet length in bytes. Greater or less comparison is inclusive of `len`.  *`<len>`：数据包长度，以字节为单位。比较或多或少都包含“ len”。
*   `<mac_addr>`: MAC address, e.g. `DE:AD:BE:EF:D0:0D`. Hex digits are case-insensitive.  *`<mac_addr>`：MAC地址，例如DE：AD：BE：EF：D0：0D`十六进制数字不区分大小写。
*   `<ip_addr>`: IP address consistent with the IP version specified previously. E.g. `192.168.1.10`, `2001:4860:4860::8888`. *`<ip_addr>`：IP地址与先前指定的IP版本一致。例如。 192.168.1.10，2001：4860：4860 :: 8888。
*   `<port_lst>`: List of ports or port ranges separated by commas, e.g. `13,ssh,6000-7000,20`. The following aliases for defined ports and port ranges can be used as items in the list, butnot as part of a range (`3,dhcp,12` is allowed, `http-100` is not): *`<port_lst>`：端口或端口范围的列表，以逗号分隔，例如`13，ssh，6000-7000,20`。定义的端口和端口范围的以下别名可以用作列表中的项目，但不能用作范围的一部分（允许使用“ 3，dhcp，12”，不允许使用“ http-100”）：

  Alias    | Port(s) :--------| :-------------------------`dhcp`   | `67-68``dns`    | `53``echo`   | `7``ftpxfer`| `20``ftpctl` | `21``http`   | `80``https`  | `443``irc`    | `194``ntp`    | `123``sftp`   | `115``ssh`    | `22``telnet` | `23``tftp`   | `69``dbglog` | Netboot debug log port`dbgack` | Netboot debug log ack port 别名|端口：-------- | ：-------------------------`dhcp` | `67-68''dns` | `53''回声`7``ftpxfer` | `20``ftpctl` | `21``http` | `80``https` | `443``irc` | ``194''ntp` | `123''sftp` | 115''ssh` | `22``telnet` | `23``tftp` | `69``dbglog` | Netboot调试日志端口dbgack Netboot调试日志确认端口

 
### Synonyms  同义字The following aliases may be used instead of the keywords listed in the syntax:  可以使用以下别名代替语法中列出的关键字：

Keyword | Alias :-------| :----------`ip`    | `ip4``port`  | `portrange` 关键字|别名：------- | ：----------`ip` | ip4端口`portrange`

 

 
## Reference: `fx` workflow packet signatures  参考：`fx`工作流数据包签名There are many different kinds of services running between the Fuchsia development host and the target. Those are usually invoked by `fx` commands. Most of times, you are not interested in those packets generated by the `fx` workflows.  The following table lists noteworthy signatures.  紫红色的开发主机与目标之间运行着许多不同类型的服务。这些通常由`fx`命令调用。大多数时候，您对`fx`工作流程生成的那些数据包不感兴趣。下表列出了值得注意的签名。

|Use           |Signature                   |Reference             | |--------------|----------------------------|----------------------||Logger        |port 33337                  |DEBUGLOG_PORT         ||Logger        |port 33338                  |DEBUGLOG_ACK_PORT     ||Bootserver    |port 33330                  |NB_SERVER_PORT        ||Bootserver    |port 33331                  |NB_ADVERT_PORT        ||Bootserver    |port 33332                  |NB_CMD_PORT_START     ||Bootserver    |port 33339                  |NB_CMD_PORT_END       ||Bootserver    |port 33340                  |NB_TFTP_OUTGOING_PORT ||Bootserver    |port 33341                  |NB_TFTP_INCOMING_PORT ||Package Server|port 8083                   |docs/packages.md      ||fx shell      |port 22                     |devshell/shell        ||target addr   |fe80::xxxx:xx4d:fexx:xxxx%XX|fx netaddr            ||target addr   |fe80::xxxx:xxff:fexx:xxxx%XX|fx netaddr --local    ||target addr   |fe80::xxxx:xxff:fexx:xxxx%XX|fx netaddr --fuchsia  ||zxdb          |port 2345                   |devshell/contrib/debug||-             |port 65026                  |                      ||-             |port 65268                  |                      ||-             |1900                        |                      | |使用|签名|参考| | -------------- | ---------------------------- | ----- ----------------- ||记录器|端口33337 | DEBUGLOG_PORT ||记录器|端口33338 | DEBUGLOG_ACK_PORT ||引导服务器|端口33330 | NB_SERVER_PORT ||引导服务器|端口33331 | NB_ADVERT_PORT | |引导服务器|端口33332 | NB_CMD_PORT_START ||引导服务器|端口33339 | NB_CMD_PORT_END ||引导服务器|端口33340 | NB_TFTP_OUTGOING_PORT ||引导服务器|端口33341 | NB_TFTP_INCOMING_PORT ||打包服务器|端口8083 | docs / packages.md || fx shell 22 | devshell / shell ||目标地址| fe80 :: xxxx：xx4d：fexx：xxxx％XX | fx netaddr ||目标地址| fe80 :: xxxx：xxff：fexx：xxxx％XX | fx netaddr --local ||目标地址| fe80 :: xxxx：xxff：fexx：xxxx％XX | fx netaddr --fuchsia || zxdb |端口2345 | dev shell / contrib / debug ||-|端口65026 | ||-|端口65268 | ||-| 1900 | |

 

 
## How do I test if `netdump` is broken?  如何测试`netdump`是否损坏？You can run some sanity checks locally.  您可以在本地运行一些完整性检查。

```shell
[host] $ fx set core.x64 --with //src/connectivity:tests,//src/connectivity/network/netdump:netdump_unit_tests
# (After running your target)
[host] $ fx run-test netdump_unit_test          # unit test
[host] $ fx run-test netdump_integration_tests  # integration test
```
 

 

 
## Troubleshooting  故障排除 

**_Q_** `fx sniff` commands give me the error `env: python3: No such file or directory`  ** _ Q _ **`fx sniff`命令给我错误`env：python3：没有这样的文件或目录`

**A** Please install Python 3 in your environment. Fuchsia is in the middle of migrating from Python 2.7 to Python 3.  ** A **请在您的环境中安装Python 3。紫红色正在从Python 2.7迁移到Python 3的过程中。

**_Q_** I get the error `/boot/bin/sh: netdump not found`  ** _ Q _ **我收到错误`/ boot / bin / sh：未找到netdump`

