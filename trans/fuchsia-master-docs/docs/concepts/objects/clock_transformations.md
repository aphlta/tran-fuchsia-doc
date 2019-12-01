 
# Clock Transformations  时钟转换 

 
## Overview  总览 

[Clock objects](/docs/concepts/objects/clock.md) represent functions which map all of the points on a reference clock timeline to all of the points on the clock object'stimeline.  Over all time, this function is represented as a[piecewise linear function](https://en.wikipedia.org/wiki/Piecewise_linear_function).Each segment of this function is a one dimensional[affine transformation](https://en.wikipedia.org/wiki/Affine_transformation)which relates the reference timeline to the clock's timeline. [Clock objects]（/ docs / concepts / objects / clock.md）表示将参考时钟时间轴上的所有点映射到时钟对象的时间轴上的所有点的函数。在所有时间内，此函数均表示为[逐段线性函数]（https://en.wikipedia.org/wiki/Piecewise_linear_function）。此函数的每个段都是一维[仿射变换]（https：// en （.wikipedia.org / wiki / Affine_transformation），将参考时间线与时钟时间线相关联。

Clock objects store only the most recent segment of the transformation at any given time, not the entire history. 时钟对象在任何给定时间仅存储转换的最新片段，而不存储整个历史记录。

 
## Definition of the Affine Transformation  仿射变换的定义 

A segment of the piecewise linear function is stored using four numbers.  分段线性函数的一部分使用四个数字存储。

 
 + The offset on the reference timeline _R<sub>off_</sub> (64 bits)  +参考时间轴_R <sub> off _ </ sub>上的偏移量（64位）
 + The offset on the clock timeline _C<sub>off_</sub> (64 bits)  +时钟时间轴_C <sub> off _ </ sub>上的偏移量（64位）
 + The ratio of the reference to clock rate (_R<sub>rate_</sub>/_C<sub>rate_</sub>) (32/32 bits)  +参考与时钟速率之比（_R <sub> rate _ </ sub> / _ C <sub> rate _ </ sub>）（32/32位）

Given a reference time _r_, the function to apply the most recent segment of the transformation, _C(r)_ is given as 给定参考时间_r_，应用转换的最新片段_C（r）_的函数为

_C(r) = (((r - R<sub>off</sub>) * C<sub>rate</sub>) / R<sub>rate</sub>) + C<sub>off</sub>_  _C（r）=（（（（r-R <sub> off </ sub>）* C <sub> rate </ sub>）/ R <sub> rate </ sub>）+ C <sub> off </子> _

Given a clock time _c_, the inverse of the _C_ may be used to compute the corresponding time on the reference timeline _r_. 给定时钟时间_c_，可以将_C_的倒数用于计算参考时间轴_r_上的相应时间。

_C<sup>-1</sup>(c) = r = (((c - C<sub>off</sub>) * R<sub>rate</sub>) / C<sub>rate</sub>) + R<sub>off</sub>_  _C <sup> -1 </ sup>（c）= r =（（（（c-C <sub> off </ sub>）* R <sub> rate </ sub>）/ C <sub> rate </ sub>）+ R <sub> off </ sub> _

