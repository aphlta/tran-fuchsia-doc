 
# Supplying Build-time Configuration Data to Components  向组件提供构建时配置数据 

 
## Terminology  术语 

**Base** - collection of software that constitutes the core of the system and is updated atomically as part of a system update. **基础**-构成系统核心并在系统更新中自动更新的软件集合。

**component** - a unit of execution started by the component framework which constructs its sandbox environment. ** component **-由构成其沙盒环境的组件框架开始的执行单元。

**[package](/garnet/go/src/pm/README.md#structure-of-a-fuchsia-package)** - a unit of distribution in Fuchsia which is a collection of files  ** [package]（/ garnet / go / src / pm / README.mdstructure-of-a-fuchsia-package）**-紫红色的发行单位，是文件的集合

 
## Scope  范围 

This document describes how to provide product-specific configuration data to components on a Fuchsia system. The mechanism described here is designed foruse with components that are part of Base. This mechanism **is** **not**suitable for things which are not components. 本文档介绍了如何向Fuchsia系统上的组件提供特定于产品的配置数据。此处描述的机制旨在与Base组成部分的组件一起使用。这种机制不适用于不是组成部分的事物。

 
## Overview  总览 

The goal of the mechanism documented here is to provide a way for configuration for Base components to be decentralized in the source. This means thatconfiguration data for a Base component can come from anywhere in the source treeas Base is being built. This mechanism also makes it easier for componentconfiguration to vary by product. 此处记录的机制的目标是为在源中分散基础组件的配置提供一种方法。这意味着在构建Base时，Base组件的配置数据可以来自源树中的任何位置。这种机制还使组件配置更容易随产品而变化。

The config-data mechanism could be used to provide configuration for components that are not part of Base, but using it for this is not recommended.Among other things, the configuration itself is updated as part of Base.Configuration implies an API and the different update timings create thepotential for mismatches between the implied API of the configuration data andthe component consuming the configuration. 可以使用config-data机制为不属于Base的组件提供配置，但不建议将其用于此配置中，此外，配置本身也作为Base的一部分进行更新。更新时间可能会导致配置数据的隐含API与使用配置的组件之间不匹配的可能性。

During the build of Base a package is constructed called `config-data`. This package contains a set of directories whose names are matched against the namesof the packages of running components. When the component manager starts acomponent that has requested the `config-data` feature, component manager willexamine the `config-data` package for a directory matching the name of thepackage whose component is being started. If a match is found, the configurationfiles appear in the component's namespace at `/config/data/`. 在构建Base的过程中，会构造一个名为“ config-data”的包。该软件包包含一组目录，这些目录的名称与正在运行的组件的软件包的名称匹配。当组件管理器启动请求了“ config-data”功能的组件时，组件管理器将检查“ config-data”包中与该组件正在启动的包名称相匹配的目录。如果找到匹配项，则配置文件将出现在组件的名称空间中的“ / config / data /”处。

The `config-data` package is a package included in Base itself and is therefore updated exactly when Base is updated. This fact reduces the security concerns ofaccess based only on string matching since we should have a fair amount of trustthat the software in Base is designed to work properly together. `config-data`软件包是Base本身包含的一个软件包，因此在更新Base时会完全进行更新。这个事实减少了仅基于字符串匹配进行访问的安全隐患，因为我们应该充分相信Base中的软件可以正常工作。

 
## Using config-data  使用配置数据 

Files supplied via config-data are made available to all components within a package to which the configuration is targeted if those components requestaccess to configuration data. It is not possible to restrict access of theconfiguration data to anything finer than a package. 如果这些组件请求访问配置数据，则通过config-data提供的文件可用于该配置所针对的包中的所有组件。不可能将配置数据的访问限制为比软件包还细的任何内容。

 
### Supplying Configuration  供应配置 

For things wishing to add configuration into another package the should create a `config_data` rule. The rule has a `for_pkg` attribute which should be thepackage for which this configuration is intended. The outputs and sources are anorder-matched set of inputs and outputs. If no outputs set is specified thefile(s) will be given the same name as appears in sources. If the outputs list issupplied it must contain exactly one item. Multiple build rules may not supplythe same output file for the same package, doing so will result in a buildfailure. For this reason it makes sense to consider namespacing the output eitherby file name or directory conventions for each component. 对于希望将配置添加到另一个包中的事物，应创建一个“ config_data”规则。该规则具有一个“ for_pkg”属性，该属性应该是用于此配置的软件包。输出和源是一组顺序匹配的输入和输出。如果未指定任何输出集，则将为文件指定与源文件中相同的名称。如果提供了输出列表，则它必须仅包含一项。多个构建规则可能不会为同一软件包提供相同的输出文件，否则将导致构建失败。因此，考虑通过每个组件的文件名或目录约定对输出进行命名间隔是有意义的。

```
config_data("tennis_sysmgr_config") {
  for_pkg = "sysmgr"
  outputs = [
    "tennis.config",
  ]
  sources = [
    "tennis_sysmgr.config",
  ]
}
```
 

 
### Consuming  消费中 

The component that wants to consume configuration data must request this feature in its component manifest, which might look something like the below. 想要使用配置数据的组件必须在其组件清单中请求此功能，该清单可能类似于以下内容。

```
{
    "program": {
        "binary": "bin/myapp"
        },
        "sandbox": {
            "features": [
                "config-data"
            ]
        }
    }
}
```
 

