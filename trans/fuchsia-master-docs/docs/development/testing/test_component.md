 
# Test Component  测试组件 

 
## Create a test component  创建一个测试组件 

 
### BUILD.gn  BUILD.gn 

```gn
import("//build/test/test_package.gni")

executable("my_test_bin") {
  testonly = true
  output_name = "my_test"

  sources = [
    "my_test.cc",
  ]
}

test_package("my_test_pkg") {
  deps = [
    ":my_test_bin",
  ]

  tests = [
    {
      name = "my_test"
    },
  ]
}
```
 

`test_package` will expect that there is a corresponding cmx file in the `meta` folder. So for above example there should be a `my_test.cmx` file in `meta/`. “ test_package”将期望在“ meta”文件夹中存在一个对应的cmx文件。因此，对于上面的示例，在`meta /`中应该有一个`my_test.cmx`文件。

 
### meta/my\_test.cmx  meta / my \ _test.cmx 

```json
{
    "program": {
        "binary": "test/my_test"
    },
    "sandbox": {
        "services": [...]
    }
}
```
 

 
## Run test  运行测试 

```bash
run-test-component fuchsia-pkg://fuchsia.com/my_test_pkg#meta/my_test.cmx
```
 

The URL passed to `run-test-component` represents a unique component url.  传递给`run-test-component`的URL代表唯一的组件URL。

A short form can be used if it is unambiguous:  如果明确，则可以使用简短形式：

```bash
run-test-component my_test.cmx
```
 

 
## Ambient Services  环境服务 

All test components are started in a new hermetic environment. By default, this environment only contains a few basic services (ambient): 所有测试组件均在新的密封环境中启动。默认情况下，此环境仅包含一些基本服务（环境）：

```text
"fuchsia.sys.Environment"
"fuchsia.sys.Launcher"
"fuchsia.process.Launcher"
"fuchsia.process.Resolver"
```
 

Tests can use these services by mentioning them in their `sandbox > services`.  测试可以通过在其“沙盒>服务”中提及它们来使用这些服务。

 
## Logger Service  记录仪服务 

Tests and the components launched in a hermetic environment will have access to system's `fuchsia.logger.LogSink` service if it is included in their sandbox. For tests to inject Logger, the tests must use `injected-services` (see below). Then, the injected Logger service takes precedence.  如果测试和在密闭环境中启动的组件包含在其沙箱中，则可以访问系统的“ fuchsia.logger.LogSink”服务。为了注入Logger的测试，测试必须使用`injected-services`（见下文）。然后，注入的Logger服务优先。

 
## Run external services  运行外部服务 

If your test needs to use (i.e. its sandbox includes) any services other than the ambient and logger services above, you must perform either, both or none:  如果您的测试需要使用（即沙盒包括）上述环境和记录器服务以外的任何服务，则您必须执行以下一项或两项：

 
- Inject the services by starting other components that provide those services in the hermetic test environment  -通过在密封测试环境中启动提供这些服务的其他组件来注入服务
- Request non-hermetic system services be included in the test environment, when a service cannot be faked or mocked, see [Other system services](#Other-system-services).  -当无法伪造或嘲笑服务时，要求将非密封系统服务包含在测试环境中，请参阅[其他系统服务]（Other-system-services）。

To inject additional services, you can add a `injected-services` clause to the manifest file's facets:  要注入其他服务，可以在清单文件的各个方面添加一个`injected-services`子句：

```json
"facets": {
  "fuchsia.test": {
    "injected-services": {
        "service_name1": "component_url1",
        "service_name2": "component_url2"
    }
  }
}
```
 

`run-test-component` will start `component_url1` and `component_url2` and the test will have access to `service_name1` and `service_name2`. Note that this makes the injected services available in the test environment, but the test component still needs to "use" them by including the service in its `sandbox > services`. “运行测试组件”将启动“ component_url1”和“ component_url2”，并且测试将有权访问“ service_name1”和“ service_name2”。请注意，这使注入的服务在测试环境中可用，但是测试组件仍需要通过将服务包含在其“沙箱>服务”中来“使用”它们。

 

 
### Network access  网络访问 

Currently we cannot run an instance of netstack inside a hermetic environment, because it conflicts with the real netstack.  If your test needs to talk tonetstack, it may only talk to the real netstack outside the test environment. Toenable this workaround you need to allow some system services: 当前，我们无法在封闭环境中运行netstack实例，因为它与实际的netstack冲突。如果您的测试需要与netstack通信，则它可能仅与测试环境外部的真实netstack通信。要启用此替代方法，您需要允许一些系统服务：

```json
"facets": {
  "fuchsia.test": {
    "system-services": [
      "fuchsia.device.NameProvider",
      "fuchsia.net.Connectivity",
      "fuchsia.net.stack.Stack",
      "fuchsia.netstack.Netstack",
      "fuchsia.net.NameLookup",
      "fuchsia.posix.socket.Provider",
    ]
  }
}
```
 

 
### Other system services  其他系统服务 

There are some services, such as network, that cannot be faked or mocked. However, you can connect to real system versions of these services by mentioning these services in `system-services`. Services that cannot be faked:  有些服务（例如网络）不能被伪造或嘲笑。但是，您可以通过在“系统服务”中提及这些服务来连接到这些服务的实际系统版本。不能伪造的服务：

```text
"fuchsia.boot.FactoryItems"
"fuchsia.boot.ReadOnlyLog"
"fuchsia.boot.RootJob"
"fuchsia.boot.RootResource"
"fuchsia.boot.WriteOnlyLog"
"fuchsia.device.NameProvider"
"fuchsia.kernel.Counter"
"fuchsia.scheduler.ProfileProvider"
"fuchsia.sys.test.CacheControl"
"fuchsia.sysmem.Allocator"
"fuchsia.ui.policy.Presenter"
"fuchsia.ui.scenic.Scenic"
"fuchsia.vulkan.loader.Loader"
```
 

Depending on your use case you can include one or more of the services above. However, services that are not listed here are not supported. 根据您的用例，您可以包括上面的一项或多项服务。但是，不支持此处未列出的服务。

This option would be replaced once we fix CP-144 (in component manager v2).  修复CP-144（在组件管理器v2中）后，将替换此选项。

