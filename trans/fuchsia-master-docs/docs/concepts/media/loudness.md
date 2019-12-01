 
# Loudness  响度 

The loudness of a given audio stream on Fuchsia is a product of five factors:  紫红色上给定音频流的响度是五个因素的乘积：

 
* [Usage of the stream](#usage-of-stream)  * [流的使用]（流的使用）
* [System-global volume setting for that Usage](#usage-volume)  * [该用途的系统全局音量设置]（使用量）
* [System-global gain adjustment for that Usage](#usage-gain-adjustment)  * [针对该用法的系统全局增益调整]（使用增益调整）
* [Stream-local gain adjustment for the stream](#stream-gain-adjustment)  * [流的本地流增益调整]（流增益调整）
* [Mute state](#mute-state)  * [静音状态]（静音状态）

 
## Usages {#usage-of-stream}  用法{流的使用} 

[Usages](https://fuchsia.dev/reference/fidl/fuchsia.media#Usage) are a hint to the system about the meaning of the audio to a user. Two supported Usages are `MEDIA`, for media content such asmusic and videos, and `INTERRUPTION` for things like alarms that interrupt the user's task. EachUsage has a separate volume control. [用法]（https://fuchsia.dev/reference/fidl/fuchsia.mediaUsage）是系统对用户的音频含义的提示。受支持的两种用法是：“ MEDIA”（用于音乐和视频等媒体内容）和“ INTERRUPTION”（用于中断用户任务的警报）。每个用法都有单独的音量控制。

Audio streams such as `AudioRenderers` and `AudioCapturers` must be tagged with a Usage.  诸如AudioRenderers和AudioCapturers之类的音频流必须带有用法标记。

 
## Usage Volume {#usage-volume}  使用量{usage-volume} 

Volume is a floating point value between 0 and 1, where 0 is muted and 1 is the maximum volume for the stream. 音量是介于0和1之间的浮点值，其中0被静音，而1是流的最大音量。

Some examples:  一些例子：

 
* If `MEDIA` is set to 0.5 volume and `INTERRUPTION` to 1.0, a stream tagged as `INTERRUPTION` would play back at half its loudness if played back instead as a `MEDIA` stream. *如果将“ MEDIA”设置为0.5音量，而将“ INTERRUPTION”设置为1.0，则标记为“ INTERRUPTION”的流如果以“ MEDIA”流播放，则将以其响度的一半播放。
* If `INTERRUPTION` is set to 0 volume, all streams tagged as `INTERRUPTION` are inaudible to the user. *如果将“ INTERRUPTION”设置为0音量，则所有标记为“ INTERRUPTION”的流都不会被用户听到。

 
## Usage Gain Adjustment {#usage-gain-adjustment}  使用增益调整{使用增益调整} 

To realize the stream, the Fuchsia audio subsystem must translate volume settings to gain in dbfs for each output device. Since devices have different ranges of gain and different mappings fromvolume to gain, this translation may result in a different value for each output device. 为了实现流，紫红色的音频子系统必须转换音量设置，以便为每个输出设备获取dbfs。由于设备具有不同的增益范围以及从体积到增益的不同映射，因此此转换可能会为每个输出设备产生不同的值。

After this translation, the usage's gain adjustment is applied. The gain adjustment is a persistent setting in units of gain dbfs. 转换后，将应用用法的增益调整。增益调整是以增益dbfs为单位的持续设置。

This is useful to enforce deltas between two usages when they are at the same volume.  当两个使用量相同时，在两个使用之间强制执行增量很有用。

For example, if `MEDIA` and `INTERRUPTION` are both set to 0.7 volume, but `MEDIA` has a gain adjustment of -10db, a stream tagged as `INTERRUPTION` would not be as loud as if it is played backtagged as `MEDIA`. 例如，如果将“ MEDIA”和“ INTERRUPTION”都设置为0.7音量，但“ MEDIA”的增益调整为-10db，则标记为“ INTERRUPTION”的视频流不会像被重标记为“`”时那样响亮。媒体`。

 
## Stream Gain Adjustment {#stream-gain-adjustment}  流增益调整{stream-gain-adjustment} 

Another gain adjustment can be applied, directly to the stream. This gain adjustment value is local.  可以将另一个增益调整直接应用于流。该增益调整值是本地的。

For example, if two `AudioRenderer`s exist on the system and one has a gain adjustment of -5db, the other, if unmodified, still has a no-op gain adjustment of 0db. 例如，如果系统上有两个`AudioRenderer`，一个的增益调整为-5db，另一个如果未修改，则无操作增益调整为0db。

 
## Mute State {#mute-state}  静音状态{mute-state} 

A stream, or usage, may be muted. When a stream is muted, it is not output to the user. When a usage is muted, no stream tagged with that usage is output to the user. 流或用法可能会被静音。流静音时，不会将其输出给用户。禁用用法后，不会将标记有该用法的流输出给用户。

During mute, other settings such as volume and gain are retained; muted is not the same as 0 volume because the volume may be changed while muted but the stream remains inaudible. 静音期间，其他设置（例如音量和增益）将保留；静音与0音量不同，因为静音时音量可能会更改，但流仍听不到。

When unmuted, streams will resume output at their previous loudness settings if those were not modified during mute. 取消静音时，如果在静音期间未对其进行修改，则流将以其先前的响度设置恢复输出。

 
## Gain Adjustment Considerations  增益调整注意事项 

Volume is not a precisely linear mapping to loudness but it is relatively close for the human ear.  音量并不是到响度的精确线性映射，但是对于人耳来说，音量相对较近。

