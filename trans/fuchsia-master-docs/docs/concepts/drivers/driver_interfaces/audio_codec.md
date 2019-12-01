 
# Audio Codec Interface  音频编解码器接口 

This document describes the codec interface between controllers and codecs in Zircon. It is meant to serve as a reference for driver-authors, and to definethe interface contract which codec drivers must implement and that controllerscan use. The codec interface is a Banjo protocol exposed by codec drivers. 本文档介绍Zircon中控制器和编解码器之间的编解码器接口。它旨在为驱动程序作者提供参考，并定义编解码器驱动程序必须实现以及控制器可以使用的接口协定。编解码器接口是编解码器驱动程序公开的Banjo协议。

 
## Notation and Terminology  符号和术语 

In this document:  在本文件中：

 
-   All indices start from 0.  -所有索引均从0开始。
-   Vectors of n elements are represented as `<x0,x1,...,xn-1>`, for example a vector with two elements 5 and 6 as `<5,6>`. -n个元素的向量表示为`<x0，x1，...，xn-1>`，例如，具有两个元素5和6的向量表示为<< 5,6>。
-   Vectors can be nested, i.e. `<<5,6>,<7,8>>` represents a vector with 2 vectors in it. -可以嵌套向量，即`<< 5,6>，<7,8 >>`代表其中有2个向量的向量。

| Term       | Definition                                                     | | ---------- | -------------------------------------------------------------- || Codec      | A real or virtual device that encodes/decodes a signal from    |:            : digital/analog to/from analog/digital including all            ::            : combinations, e.g. digital to digital. Example codecs include  ::            : DAC-Amplifiers combos and ADC converters.                      :| Controller | The part of a system that manages the audio signals, for       |:            : example an SOC's audio subsystem or an independent sound card. :| DAI        | Digital Audio Interface. Interface between controllers and     |:            : Codecs. For example an I2S or HDA link.                        : |条款|定义| | ---------- | -------------------------------------------------- ------------ ||编解码器|真正的或虚拟的设备，将信号从|：：数字/模拟到模拟/数字，包括所有::：组合，进行编码/解码。数字到数字。示例编解码器包括:: :: DAC放大器组合和ADC转换器。 ：|控制器|管理音频信号的系统部分，例如|：：例如SOC的音频子系统或独立的声卡。 ：| DAI |数字音频接口。控制器和|：：编解码器之间的接口。例如，I2S或HDA链接。 ：

 
## Basic Operation  基本操作 

The functionality provided by the codecs is divided into:  编解码器提供的功能分为：

 
-   [Main controls](#main-controls)  -[主要控制项]（主要控制项）
-   [DAI format](#dai-format)  -[DAI格式]（每日格式）
-   [Gain control](#gain-control)  -[增益控制]（增益控制）
-   [Plug detect](#plug-detect)  -[插入检测]（插入检测）
-   [Power control](#power-control)  -[电源控制]（电源控制）
-   [Peripheral control](#peripheral-control)  -[外围设备控制]（peripheral-control）
-   [Signal processing control](#signal-processing-control)  -[信号处理控制]（信号处理控制）
-   [Content protection](#content-protection)  -[内容保护]（内容保护）

The controller is responsible for configuring and controlling the codecs. Codecs advertize capabilities and a controller determines how they are used asdescribed below. Note that the codec drivers are expected to perform their owninitialization and shutdown, just like any other driver. The controller cancontrol the codec's state, such as through the reset function, but is notrequired to get codecs to an initialized state. 控制器负责配置和控制编解码器。编解码器广告功能，然后由控制器确定如何使用它们，如下所述。请注意，编解码器驱动程序应像其他任何驱动程序一样执行自己的初始化和关闭操作。控制器可以控制编解码器的状态，例如通过重置功能，但不需要使编解码器进入初始化状态。

Codecs are composite devices that provide the codec protocol to controllers. It is expected that only one controller uses a codec's protocol, and one controllermay use multiple codecs at once. 编解码器是向控制器提供编解码器协议的复合设备。期望只有一个控制器使用编解码器的协议，并且一个控制器可以一次使用多个编解码器。

 
## Protocol definition  协议定义 

The codec protocol is defined in [Banjo](/docs/development/tools/banjo-tutorial.md) at [ddk.protocol.codec](/zircon/system/banjo/ddk.protocol.codec/codec.banjo). 编解码器协议在[Banjo]（/ docs / development / tools / banjo-tutorial.md）中的[ddk.protocol.codec]（/ zircon / system / banjo / ddk.protocol.codec / codec.banjo）中定义。

Many codec protocol operations are "fire-and-forget", i.e. they do not expect a reply. Codec protocol operations with a reply are not considered completed untilthe reply of the function is received, and not considered completed successfullyunless the reply contains a status `ZX_OK`. 许多编解码器协议操作都是“一劳永逸”的，即它们不希望得到答复。除非收到该功能的回复，否则带有回复的编解码器协议操作不会被视为已完成，并且除非回复包含状态“ ZX_OK”，否则不会认为已成功完成。

 
### Main Controls {#main-controls}  主控件{main-controls} 

A codec can be reset by a controller at any time by issuing the `Reset` function. 编解码器可以在任何时候通过发出“复位”功能由控制器复位。

The `GetInfo` function retrieves information from the codec including:  GetInfo函数从编解码器检索信息，包括：

 
1.  A unique and persistent identifier for the codec unit, e.g. a serial number or connection path. 1.编解码器单元的唯一且持久的标识符，例如序列号或连接路径。
1.  The manufacturer name.  1.制造商名称。
1.  The product name.  1.产品名称。

 
### Bridged Mode  桥接模式 

Before specifying the DAI format the controller must query the codec for its bridging capabilites. If the codec is bridgeable, then the controller mustenable or disable bridging based on its knowledge of the system configuration.Note that this is a singular property of a codec, i.e. a codec either supportsbridging or not, and it can be set in bridged mode or not. This protocol allowsconfiguring as bridged only 2 channel stereo codecs, with the 2 outputs of thecodec electrically bridged. 在指定DAI格式之前，控制器必须向编解码器查询其桥接功能。如果编解码器是可桥接的，则控制器必须基于其对系统配置的了解来强制启用或禁用桥接。请注意，这是编解码器的奇异属性，即编解码器是否支持桥接，可以将其设置为桥接模式或不。该协议仅允许将2声道立体声编解码器配置为桥接，而将编解码器的2个输出电桥接。

 
### DAI Format {#dai-format}  DAI格式{dai-format} 

The DAI Format related protocol functions allow the codec to list its supported formats for the DAI. The supported formats may include multiple sample formats,rates, etc. Each codec advertises what it can support and the controllermandates what DAI Format is to be used for each codec. 与DAI格式相关的协议功能允许编解码器列出DAI支持的格式。支持的格式可以包括多种样本格式，速率等。每个编解码器都宣传其可以支持的内容，而控制器则规定要为每个编解码器使用哪种DAI格式。

To find out what formats are supported by a given codec, the controller uses the `GetDaiFormats` function. The codec replies with a vector of`DaiSupportedFormats`, where each `DaiSupportedFormats` includes: 为了找出给定编解码器支持什么格式，控制器使用GetDaiFormats函数。编解码器以向量“ DaiSupportedFormats”答复，其中每个“ DaiSupportedFormats”包括：

 
1.  A vector of number of channels. This lists the number of channels supported by the codec, for example `<2,4,6,8>`. A stereo codec reports a vector withone element `<2>`. Note that a codec that takes one channel and outputs itscontents in all its outputs (e.g. 2 for a stereo amplifier) would report avector with one element `<1>`, if it supports either one or two inputchannels, it would report a vector with two elements `<1,2>`. 1.通道数的向量。这列出了编解码器支持的通道数，例如“ <2,4,6,8>”。立体声编解码器报告一个元素为<2>的向量。请注意，占用一个通道并在其所有输出中输出其内容的编解码器（例如，立体声放大器为2）将报告带有一个元素“ <1>”的向量，如果它支持一个或两个输入通道，则它将报告带有一个元素的向量。两个元素“ <1,2>”。
2.  A vector of sample formats. DAI sample formats, e.g. `PCM_SIGNED`.  2.样本格式的向量。 DAI样本格式，例如PCM_SIGNED。
3.  A vector of justify formats. Justification options, for example `JUSTIFY_LEFT` and `JUSTIFY_RIGHT`. 3.证明格式的向量。对齐选项，例如`JUSTIFY_LEFT`和`JUSTIFY_RIGHT`。
4.  A vector of rates. Frame rates, for example 44100, 48000, and 96000.  4.比率向量。帧速率，例如44100、48000和96000。
5.  A number of bits per channel. Number of bits in each channel in the DAI, e.g. 32 bits per channel. 5.每个通道的位数。 DAI中每个通道的位数，例如每个通道32位。
6.  A vector of bits per sample. Sample widths, e.g. 24 bits per sample.  6.每个样本的位向量。样本宽度每个样本24位。

When not all combinations supported by the codec can be described with one `DaiSupportedFormats`, the codec returns more than one `DaiSupportedFormats` inthe returned vector. 如果无法使用一个`DaiSupportedFormats`描述编解码器支持的所有组合，则该编解码器在返回的向量中返回不止一个`DaiSupportedFormats`。

For example, if one `DaiSupportedFormats` allows for 32 bits samples at 48KHz, and 16 bits samples at 96KHz, but not 32 bits samples at 96KHz, then the codecwill reply with 2 `DaiSupportedFormats`: `<<32bits>,<48KHz>>` and`<<16bits>,<96KHz>>`. For simplicity, this example ignores parameters other thanrate and bits per sample. In the case where the codec supports either 16 or 32bits samples at either 48 or 96KHz, the codec would reply with 1`DaiSupportedFormats`: `<<16bits,32bits>,<48KHz,96KHz>>`. 例如，如果一个“ DaiSupportedFormats”允许以48KHz的频率进行32位采样，而以96KHz允许16位的采样，但不允许以96KHz进行32位采样，则编解码器将以2个“ DaiSupportedFormats”进行回复：`<< 32bits>，<48KHz> >和<< 16bits>，<96KHz >>`。为简单起见，此示例忽略每个采样率和比特率以外的参数。如果编解码器支持48或96KHz的16或32bit采样，则编解码器将以1`DaiSupportedFormats`答复：<< 16bits，32bits>，<48KHz，96KHz >>。

Additionally, it is assumed that bits per sample is always smaller or equal to bits per channel. Hence, a codec can report`<<16bits_per_channel,32bits_per_channel>,<16bits_per_sample,32bits_per_sample>>`and this does not imply that it is reporting that 32 bits per sample on 16 bitssamples is valid, it specifies only the 3 valid combinations: 另外，假设每个样本的位总是小于或等于每个通道的位。因此，编解码器可以报告<< 16bits_per_channel，32bits_per_channel>，<16bits_per_sample，32bits_per_sample >>>>，这并不意味着它报告16位样本中每个样本32位有效，它仅指定3个有效组合：

 
1.  16 bits channels with 16 bits samples  1. 16位通道和16位样本
2.  32 bits channels with 32 bits samples  2.具有32位样本的32位通道
3.  32 bits channels with 16 bits samples  3. 32位通道和16位样本

Using the information provided by the codec in `IsBridgeable` and `GetDaiFormat`, what is supported by the controller, and any other requirements,the controller specifies the format to use in the DAI with the `SetDaiFormat`function. This functions takes a parameter that specifies: 控制器使用“ IsBridgeable”和“ GetDaiFormat”中编解码器提供的信息，控制器支持的功能以及任何其他要求，通过“ SetDaiFormat”功能指定DAI中使用的格式。此函数采用一个参数，该参数指定：

 
1.  A number of channels. This is the number of channels to be used in the DAI (for instance number of channels on a TDM bus, i.e. "on the wire"). For I2Sthis must be 2. 1.多个渠道。这是DAI中要使用的通道数（例如TDM总线（即“在线”）上的通道数）。对于I2S，此值必须为2。
2.  A vector of channels to use. These are the channels in the DAI to be used by the codec. For I2S this must be a vector with 2 indexes `<0,1>`, i.e. bothleft and right channels are used. In bridged mode this will list only theone channel to be used by the codec, for example a codec’s stereo amplifieroutput bridged into one electrical mono output from the right channel of anI2S DAI would list only channel `<1>`. If not bridged, a codec with multipleelectrical outputs that is configured with one channel in `SetDaiFormat` isexpected to replicate the samples in this mono input on all its outputs. 2.要使用的渠道向量。这些是编解码器要使用的DAI中的通道。对于I2S，它必须是一个具有2个索引``<0,1>''的向量，即使用左声道和右声道。在桥接模式下，它将仅列出编解码器要使用的一个通道，例如，从I2S DAI的右通道桥接到一个电单声道输出的编解码器的立体声放大器输出将仅列出通道“ <1>”。如果未桥接，则预期具有多个电气输出的编解码器（在SetDaiFormat中配置有一个通道）将在此单声道输入的所有输出上复制样本。
3.  A sample format.  3.示例格式。
4.  A justify format.  4.调整格式。
5.  A frame rate.  5.帧速率。
6.  A number of bits per channel.  6.每个通道的位数。
7.  A number of bits per sample.  7.每个样本的位数。

Once `SetDaiFormat` is successful, the DAI format configuration is considered completed and samples can be sent across the DAI. 一旦“ SetDaiFormat”成功，就认为DAI格式配置已完成，并且可以通过DAI发送样本。

TODO(andresoportus): Add DAI format loss notification support once asynchronous notifications are added to Banjo. TODO（andresoportus）：将异步通知添加到Banjo后，添加DAI格式丢失通知支持。

 
### Gain Control {#gain-control}  增益控制{gain-control} 

Gain related support by any given codec is returned by the codec in response to a `GetGainFormat` function in the `GainFormat` structure. The controller cancontrol gain, mute and AGC states in a codec using the `SetGainState` functionand the corresponding `GetGainState` function allows retrieving the currentstate for the same. 响应于GainFormat结构中的GetGainFormat函数，编解码器将返回任何给定编解码器与增益相关的支持。控制器可以使用“ SetGainState”功能控制编解码器中的增益，静音和AGC状态，而相应的“ GetGainState”功能允许检索相同的当前状态。

 
### Plug Detect {#plug-detect}  插头检测{plug-detect} 

The controller can query the plug detect state with the `GetPlugState` function. The plug state includes hardwired and plugged states. 控制器可以使用“ GetPlugState”功能查询插头检测状态。插入状态包括硬接线和插入状态。

TODO(andresoportus): Add `can_notify` bool to `PlugState` once asynchronous notifications are added to Banjo. TODO（andresoportus）：将异步通知添加到Banjo后，将`can_notify` bool添加到`PlugState`中。

 
### Power Control {#power-control}  功率控制{power-control} 

TODO(andresoportus).  TODO（andresoportus）。

 
### Peripheral Control {#peripheral-control}  外围设备控制{peripheral-control} 

TODO(andresoportus).  TODO（andresoportus）。

 
### Signal Processing Control {#signal-processing-control}  信号处理控制{signal-processing-control} 

TODO(andresoportus).  TODO（andresoportus）。

 
### Content Protection {#content-protection}  内容保护{content-protection} 

