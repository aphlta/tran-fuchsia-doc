 
# Fuchsia Update Channel Usage Policy  紫红色更新频道使用政策 

This document codifies the policy for using *Update Channel* information in Fuchsia. 本文档整理了在紫红色中使用* Update Channel *信息的策略。

 
## Background  背景 

Fuchsia exposes Get/Set channel information through the _fuchsia.update.channelcontrol_ FIDL APIs. In order to expose these APIs to awider set of clients as part of the Fuchsia SDK, it is important to ensureclient behavior is not modulated based on channel strings. Below is ourpolicy which applies to internal clients as well as any other Fuchsiasupported components. 紫红色通过_fuchsia.update.channelcontrol_ FIDL API公开获取/设置频道信息。为了将这些API作为Fuchsia SDK的一部分向更多的客户端公开，重要的是确保不基于通道字符串来调制客户端行为。以下是适用于内部客户以及Fuchsia支持的任何其他组件的我们的政策。

 
## Policy  政策 

Clients looking to obtain approvals for use of Update Channel APIs must conform to the following requirements: 希望获得使用更新通道API的批准的客户必须符合以下要求：

 
*   The channel information cannot be used in conditional logic  *通道信息不能在条件逻辑中使用
*   The client software must execute exactly the same code path regardless of channel.  *无论通道如何，客户端软件必须执行完全相同的代码路径。
*   The channel information cannot be cached or shared in a way that allows unapproved consumption. *频道信息不能以不允许未经许可的使用方式进行缓存或共享。
    *   This implies that additional clients should not by-pass the policy by reading cached channel information. *这意味着其他客户端不应通过读取缓存的通道信息来绕过策略。

 
## Update Channel Use within Fuchsia Platform  在Fuchsia平台中更新频道使用情况 

Within the Fuchsia “stem,” the use of channels MUST conform to the defined policy. Also, the following properties MUST apply: 在紫红色的“词干”中，渠道的使用必须符合所定义的政策。另外，必须应用以下属性：

 
*   There should be a single component responsible for the writing of channel information. The component should export this capability via a FIDL service toother clients. Both read/write capabilities should be exported. *应该只有一个组件负责编写频道信息。组件应通过FIDL服务将此功能导出到其他客户端。两种读/写功能都应导出。
*   Readers of channel information should use the canonical APIs of the authoritative component and should not use this information to alter runtimebehavior. *频道信息的读者应使用权威组件的规范API，并且不应使用此信息来更改运行时行为。

 
## Update Channel Use within the SDK  在SDK中更新频道使用情况 

Users of channel information in the SDK for Fuchsia components MUST follow the defined policy. The following properties MUST apply: Fuchsia组件的SDK中的频道信息用户必须遵循所定义的策略。以下属性必须适用：

 
*   Clients MUST only read the channel for the purposes of reporting (via a metrics agent), information collecting,  or displaying to a front-endinterface. *客户端必须仅出于报告（通过度量指标代理），信息收集或向前端界面显示的目的读取通道。
