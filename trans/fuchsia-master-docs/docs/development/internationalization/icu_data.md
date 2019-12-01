 
# ICU timezone data  ICU时区数据 

The ICU timezone data in Fuchsia is provided dynamically through the ICU data files (`icudtl.dat`).  These are loaded on demand by programs, provided thatthe program's package is configured to make the file available to the programat runtime. 紫红色中的ICU时区数据是通过ICU数据文件（icudtl.dat）动态提供的。只要程序的程序包配置为使文件在运行时可用，程序就可以按需加载这些文件。

Section below shows how to do that.  以下部分显示了如何执行此操作。

 
# Making the ICU data available to packages  使ICU数据可用于程序包 

In order for the ICU data files to be visible to a program in Fuchsia, it first needs to be made available in the package that contains the program.  This isan example use from [the wisdomserver](/garnet/examples/intl/wisdom/rust/server/BUILD.gn). 为了使ICU数据文件对紫红色的程序可见，首先需要在包含该程序的程序包中使ICU数据文件可用。这是来自[thingsserver]（/ garnet / examples / intl / wisdom / rust / server / BUILD.gn）中的示例。

```gn
{%includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/intl/wisdom/rust/server/BUILD.gn" region_tag="icudata" adjust_indentation="auto" %}
```
 

Note the section that adds a resource for `icudtl.dat`.  请注意为`icudtl.dat`添加资源的部分。

```gn
{%includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/intl/wisdom/rust/server/BUILD.gn" region_tag="icudata_resource" adjust_indentation="auto" %}
```
 

Since the library's footprint can be large, we do not simply import it as a public dependency on any rust program that uses ICU. 由于该库的占用空间可能很大，因此我们不能简单地将其作为对使用ICU的任何rust程序的公共依赖项进行导入。

 
# Using the ICU data  使用ICU数据 

You *must* load the ICU data in your program to make the locale data available. If you do not do that, no locale data will be available, and your ICU code willbehave as if the set of i18n data is empty. 您*必须*在程序中加载ICU数据，以使语言环境数据可用。如果您不这样做，那么将没有可用的语言环境数据，并且您的ICU代码将表现为好像i18n数据集为空。

The APIs to load the code made available are different per language, so please refer to the pages below for specific examples: 每种语言用于加载提供的代码的API有所不同，因此请参考以下页面以获取具体示例：

 
- [C++ library for ICU data loading](/src/lib/icu_data/cpp)  -[用于ICU数据加载的C ++库]（/ src / lib / icu_data / cpp）
- [Rust library for ICU data loading](/src/lib/icu_data/rust)  -[用于ICU数据加载的锈迹库]（/ src / lib / icu_data / rust）

 
## Rust example  锈示例 

In Rust, you should use the `icu_data::Loader`, which will automatically do the right thing. Here is an example from the ICU data tests showing this approach. 在Rust中，您应该使用`icu_data :: Loader`，它将自动执行正确的操作。这是来自ICU数据测试的示例，说明了这种方法。

Note that at least one instance of `icu_data::Loader` must be kept alive for as long as your code needs ICU data. Since it is difficult to predict when thisdata is needed, and the ICU liveness rules are a bit confusing, it is probablybest to simplify things and keep an `icu_data::Loader` handy for the lifetimeof the program. 请注意，只要您的代码需要ICU数据，就必须至少保留一个icu_data :: Loader实例。由于很难预测何时需要该数据，并且ICU活动规则有些混乱，因此最好简化程序并在程序生命周期内方便使用`icu_data :: Loader`。

```rust
{%includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="src/lib/icu_data/rust/icu_data/src/lib.rs" region_tag="loader_example" adjust_indentation="auto" %}
```
 

In code, this amounts to instantiating a `icu_data::Loader` and keeping at least one instance of it alive for the lifetime of the program.  The `Loader`can be cloned at will and copied around: the ICU data will be loaded before thefirst time it is needed, it will be unloaded when it is not needed, and will bereloaded again if needed again. 在代码中，这相当于实例化了一个“ icu_data :: Loader”，并在程序生命周期中至少使其一个实例保持活动状态。可以随意克隆和复制“ Loader”：ICU数据将在第一次需要时被加载，不需要时将被卸载，如果需要则将被重新加载。

```rust
{%includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/intl/wisdom/rust/server/src/main.rs" region_tag="loader_example" adjust_indentation="auto" %}
```
 

Perhaps a more robust approach to maintaining a live `icu_data::Loader` is to pass a possibly cloned instance of a `Loader` into whatever struct requires ICUdata.  This will ensure that even in face of code refactors, the code thatneeds live ICU data always has it available: 维护活动的“ icu_data :: Loader”的更健壮的方法可能是将“ Loader”的可能克隆的实例传递到任何需要ICUdata的结构中。这将确保即使面对代码重构，需要实时ICU数据的代码也始终具有可用的代码：

```rust
{%includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/intl/wisdom/rust/client/src/wisdom_client_impl.rs" region_tag="loader_example" adjust_indentation="auto" %}
```
 

 
# See also  也可以看看 

 
