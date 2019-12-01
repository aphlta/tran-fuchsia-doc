 
# Mod integration testing with Topaz  与Topaz进行Mod集成测试 

[TOC]  [目录]

 
## Introduction  介绍 

This step-by-step guide is for running integration tests using [Flutter Driver](https://docs.flutter.io/flutter/flutter_driver/flutter_driver-library.html)in Topaz. If you are not looking to run integration testing on your mods, or ifyour mod is not written using Flutter, then you don’t need this guide. 本分步指南用于使用Topaz中的[Flutter驱动程序]（https://docs.flutter.io/flutter/flutter_driver/flutter_driver-library.html）运行集成测试。如果您不想在您的模组上进行集成测试，或者您不是使用Flutter编写ifyour模组，那么就不需要本指南。

This is different from unit testing with widgets because the expectation is that you will be testing simulated user interaction with your mod (tapping buttons,scrolling, etc, for example), which requires Scenic and cannot be run in QEMU. 这与使用widget进行单元测试不同，因为期望您将使用mod测试模拟的用户交互（例如，点击按钮，滚动等），这需要Scenic，并且不能在QEMU中运行。

The examples in this doc will be focused around a testing mod under [`//topaz/examples/test/driver_example_mod`](https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod).The name is derived from how it is an example mod relating to the use of[Flutter Driver](https://docs.flutter.io/flutter/flutter_driver/flutter_driver-library.html).In addition, you'll see how to set up a hermetic test with Fuchsia[component testing](/docs/development/testing/test_component.md). 本文档中的示例将重点关注[`//topaz/examples/test/driver_example_mod`](https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod）下的测试模块。该名称是从与[Flutter Driver]（https://docs.flutter.io/flutter/flutter_driver/flutter_driver-library.html）的使用有关的示例mod派生而来的。此外，您还将看到如何用Fuchsia [component testing]（/ docs / development / testing / test_component.md）进行密封测试。

The ultimate goal of this document is to make it possible for you to add integration tests into[`//topaz/tests`](https://fuchsia.googlesource.com/topaz/+/HEAD/tests) so thatyour mod can be tested in CQ and CI. 本文档的最终目标是使您可以将集成测试添加到[`//topaz/tests`](https://fuchsia.googlesource.com/topaz/+/HEAD/tests）中，以便您的mod可以在CQ和CI中进行测试。

 
## Setup  设定 

To start, this doc assumes you’ve already got a mod that you can run on Topaz (see[here](/docs/getting_started.md)if you haven't). For simplicity, we’ll assume it is a standalone mod thatdoesn’t depend on other mods (in the future this will have been tested andverified). 首先，本文档假定您已经拥有可以在Topaz上运行的mod（如果没有，请参见[here]（/ docs / getting_started.md））。为简单起见，我们假设它是一个独立的mod，它不依赖于其他mod（将来会经过测试和验证）。

Per the introduction section, we’ll be focusing on `driver_example_mod` as the mod under test. 在介绍部分，我们将重点介绍“ driver_example_mod”作为受测试的mod。

 
### Enabling Flutter Driver extensions  启用Flutter驱动程序扩展 

If you want to simulate user interaction with your mod, or capture a screenshot of a certain state you are interested in, you will need to enable the flutterdriver extensions before you can start using the flutter driver. This is done byadding `flutter_driver_extendable = true` to your `flutter_app` target in the[`BUILD.gn`](https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/BUILD.gn)for your mod: 如果要模拟用户与Mod的交互，或捕获感兴趣的特定状态的屏幕截图，则需要先启用flutterdriver扩展，然后才能开始使用flutter驱动程序。这是通过在[`BUILD.gn`]（https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/BUILD.gn）中将`flutter_driver_extendable = true`添加到您的`flutter_app`目标中来完成的）为您的国防部：

```gn
flutter_app("driver_example_mod") {
  // ...
  flutter_driver_extendable = true
  // ...
}
```
 

In a debug JIT setting, this will generate a wrapper for your [`main`](https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/lib/main.dart)that calls[`enableFlutterDriverExtension()`](https://docs.flutter.io/flutter/flutter_driver_extension/enableFlutterDriverExtension.html)from[`package:flutter_driver/driver_extension.dart`](https://docs.flutter.io/flutter/flutter_driver_extension/flutter_driver_extension-library.html).(See also:[`gen_debug_wrapper_main.py`](https://fuchsia.googlesource.com/topaz/+/HEAD/runtime/flutter_runner/build/gen_debug_wrapper_main.py)) 在调试JIT设置中，这会为您的[`main`]（https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/lib/main.dart）生成包装器。 `enableFlutterDriverExtension（）`]（https://docs.flutter.io/flutter/flutter_driver_extension/enableFlutterDriverExtension.html）来自[`package：flutter_driver / driver_extension.dart`]（https://docs.flutter.io/flutter/ flutter_driver_extension / flutter_driver_extension-library.html）。（另请参见：[`gen_debug_wrapper_main.py`]（https://fuchsia.googlesource.com/topaz/+/HEAD/runtime/flutter_runner/build/gen_debug_wrapper_main.py））

 
## Writing your tests  编写测试 

Next you’ll get to the exciting part: writing the tests for your mod! These will require use of the aforementioned[Flutter Driver](https://docs.flutter.io/flutter/flutter_driver/flutter_driver-library.html)library. 接下来，您将进入令人兴奋的部分：为您的mod编写测试！这些将需要使用前述的[Flutter驱动程序]（https://docs.flutter.io/flutter/flutter_driver/flutter_driver-library.html）库。

Tests live in a `test` subfolder of your mod and end in `_test.dart`. These requirements are stipulated by[`dart_fuchsia_test`](https://fuchsia.googlesource.com/topaz/+/master/runtime/dart/dart_fuchsia_test.gni),described [later](#build-gn-target). The tests for `driver_example_mod` are in[`driver_example_mod_test.dart`](https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/test/driver_example_mod_test.dart). 测试位于mod的“ test”子文件夹中，并以“ _test.dart”结尾。这些要求由[`dart_fuchsia_test`]（https://fuchsia.googlesource.com/topaz/+/master/runtime/dart/dart_fuchsia_test.gni）规定，并在[稍后]（build-gn-target）中进行了描述。 “ driver_example_mod”的测试位于[`driver_example_mod_test.dart`]（https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/test/driver_example_mod_test.dart）中。

 
### Boilerplate  样板 

You’ll need some boilerplate to set up and tear down your code. The following helper function starts Modular with test shells and launches the mod under testin a new story. 您需要一些样板来设置和删除代码。以下帮助程序功能使用测试外壳启动Modular，并在新情况下在test下启动mod。

```dart
import 'package:fidl_fuchsia_modular/fidl_async.dart' as modular;
import 'package:fidl_fuchsia_modular_testing/fidl_async.dart';
import 'package:fuchsia_modular_testing/test.dart';

const Pattern _isolatePattern = 'driver_example_mod.cmx';
const _testAppUrl =
    'fuchsia-pkg://fuchsia.com/driver_example_mod#meta/driver_example_mod.cmx';

final _addModCommand = modular.AddMod(
    modName: [_isolatePattern],
    modNameTransitional: 'root',
    intent: modular.Intent(action: 'action', handler: _testAppUrl),
    surfaceRelation: modular.SurfaceRelation());

// Starts Modular with test shells. This should be called from within a
// try/finally or similar construct that closes the component controller.
Future<void> _launchModUnderTest(TestHarnessProxy testHarness) async {
  final puppetMaster = modular.PuppetMasterProxy();
  await testHarness.connectToModularService(
      ModularService.withPuppetMaster(puppetMaster.ctrl.request()));

  // Use PuppetMaster to start a fake story and launch the mod under test
  final storyPuppetMaster = modular.StoryPuppetMasterProxy();
  await puppetMaster.controlStory(
      'driver_example_mod_test', storyPuppetMaster.ctrl.request());
  await storyPuppetMaster
      .enqueue([modular.StoryCommand.withAddMod(_addModCommand)]);
  await storyPuppetMaster.execute();
}
```
 

The `Intent.handler` defines the mod that will be launched via `_addModCommand`. After starting the Modular TestHarness, you can usePuppetMaster to create a new story and execute this command. Intent.handler定义将通过_addModCommand启动的mod。启动模块化TestHarness之后，可以使用PuppetMaster创建新故事并执行此命令。

In your test setup, you'll need to launch and run the Modular TestHarness. You can specify any extra Modular configurations in the `TestHarnessSpec`.Once completed, you can launch your mod and connect to Flutter Driver. 在测试设置中，您需要启动并运行模块化TestHarness。您可以在TestHarnessSpec中指定任何其他模块化配置。完成后，您可以启动您的mod并连接到Flutter Driver。

```dart
// ...
import 'package:flutter_driver/flutter_driver.dart';
import 'package:test/test.dart';

// ... _launchModUnderTest ...

void main() {
  group('driver example tests', () {
    TestHarnessProxy testHarness;
    FlutterDriver driver;

    setUpAll(() async {
      testHarness = await launchTestHarness();
      await testHarness.run(TestHarnessSpec(
          envServices:
              EnvironmentServicesSpec(serviceDir: Channel.fromFile('/svc'))));
      await _launchModUnderTest(testHarness);

      driver = await FlutterDriver.connect(
          fuchsiaModuleTarget: _isolatePattern,
          printCommunication: true,
          logCommunicationToFile: false);
    });

    tearDownAll(() async {
      await driver?.close();
      testHarness.ctrl.close();
    });

    // ...
  });
}
```
 

When a Dart app starts in debug mode, it exposes the Dart Observatory (VM Service) on an HTTP port.[`FlutterDriver.connect`](https://docs.flutter.io/flutter/flutter_driver/FlutterDriver/connect.html)connects to the Dart Observatory and finds the isolate for the mod named in`fuchsiaModuleTarget`. Behind the scenes, Flutter Driver uses[`FuchsiaCompat`](https://github.com/flutter/flutter/blob/master/packages/flutter_driver/lib/src/common/fuchsia_compat.dart)and[`FuchsiaRemoteConnection`](https://github.com/flutter/flutter/blob/master/packages/fuchsia_remote_debug_protocol/lib/src/fuchsia_remote_connection.dart)to search over all the Dart VMs running on the device to find the isolate thatmatches your `fuchsiaModuleTarget`. Once this is found, Flutter Driver opens awebsocket over which to send RPCs which were registered by your mod under testin[`enableFlutterDriverExtension()`](https://docs.flutter.io/flutter/flutter_driver_extension/enableFlutterDriverExtension.html). 当Dart应用以调试模式启动时，它将在HTTP端口上公开Dart天文台（VM服务）。[`FlutterDriver.connect`]（https://docs.flutter.io/flutter/flutter_driver/FlutterDriver/connect.html ）连接到Dart天文台，并找到名为“ fuchsiaModuleTarget”的mod的隔离株。在幕后，Flutter驱动程序使用[`FuchsiaCompat`]（https://github.com/flutter/flutter/blob/master/packages/flutter_driver/lib/src/common/fuchsia_compat.dart）和[`FuchsiaRemoteConnection`]（ https://github.com/flutter/flutter/blob/master/packages/fuchsia_remote_debug_protocol/lib/src/fuchsia_remote_connection.dart）搜索设备上运行的所有Dart VM，以查找与您的`fuchsiaModuleTarget`相匹配的隔离物。找到此文件后，Flutter驱动程序将打开一个websocket，通过该websocket发送由您的mod在testin [`enableFlutterDriverExtension（）`]（https://docs.flutter.io/flutter/flutter_driver_extension/enableFlutterDriverExtension.html）下注册的RPC。

If you’d like to see an example test that pushes a few buttons, you can check [here](https://fuchsia.googlesource.com/topaz/+/master/examples/test/driver_example_mod/test/driver_example_mod_test.dart). 如果您想查看按下几个按钮的示例测试，可以在[here]（https://fuchsia.googlesource.com/topaz/+/master/examples/test/driver_example_mod/test/driver_example_mod_test.dart ）。

 
### Component manifest  组件清单 

A [component manifest](/docs/concepts/storage/component_manifest.md)allows the test to run as a hermetic[test component](/docs/development/testing/test_component.md)under its own dedicated environment that will sandbox its services and teareverything down on completion or failure. This is particularly important forFlutter Driver tests and other graphical tests as only one Scenic instance mayown the display controller at a time, so any such test that does not properlyclean up can cause subsequent tests to fail. [component manifest]（/ docs / concepts / storage / component_manifest.md）允许测试在其自己的专用环境下作为密封的[test component]（/ docs / development / testing / test_component.md）运行服务和完成或失败的一切。这对于Flutter Driver测试和其他图形测试尤为重要，因为一次只能有一个Scenic实例可以拥有显示控制器，因此任何此类测试如果未正确清理，都可能导致后续测试失败。

The component manifest for our tests is [driver_example_mod_tests.cmx](https://fuchsia.googlesource.com/topaz/+/master/examples/test/driver_example_mod/meta/driver_example_mod_tests.cmx). 我们测试的组件清单是[driver_example_mod_tests.cmx]（https://fuchsia.googlesource.com/topaz/+/master/examples/test/driver_example_mod/meta/driver_example_mod_tests.cmx）。

```json
{
    "facets": {
        "fuchsia.test": {
            "injected-services": {
                "fuchsia.identity.account.AccountManager": "fuchsia-pkg://fuchsia.com/account_manager#meta/account_manager.cmx",
                "fuchsia.devicesettings.DeviceSettingsManager": "fuchsia-pkg://fuchsia.com/device_settings_manager#meta/device_settings_manager.cmx",
                "fuchsia.fonts.Provider": "fuchsia-pkg://fuchsia.com/fonts#meta/fonts.cmx",
                "fuchsia.tracing.provider.Registry": "fuchsia-pkg://fuchsia.com/trace_manager#meta/trace_manager.cmx",
                "fuchsia.ui.input.ImeService": "fuchsia-pkg://fuchsia.com/ime_service#meta/ime_service.cmx",
                "fuchsia.ui.policy.Presenter": "fuchsia-pkg://fuchsia.com/root_presenter#meta/root_presenter.cmx",
                "fuchsia.ui.scenic.Scenic": "fuchsia-pkg://fuchsia.com/scenic#meta/scenic.cmx"
            },
            "system-services": [
                "fuchsia.net.NameLookup",
                "fuchsia.posix.socket.Provider",
                "fuchsia.sysmem.Allocator",
                "fuchsia.vulkan.loader.Loader"
            ]
        }
    },
    "program": {
        "data": "data/driver_example_mod_tests"
    },
    "sandbox": {
        "features": [
            "deprecated-shell",
            "deprecated-ambient-replace-as-executable"
        ],
        "services": [
            "fuchsia.identity.account.AccountManager",
            "fuchsia.devicesettings.DeviceSettingsManager",
            "fuchsia.fonts.Provider",
            "fuchsia.net.NameLookup",
            "fuchsia.posix.socket.Provider",
            "fuchsia.sys.Environment",
            "fuchsia.sys.Launcher",
            "fuchsia.sysmem.Allocator",
            "fuchsia.ui.policy.Presenter",
            "fuchsia.ui.scenic.Scenic",
            "fuchsia.vulkan.loader.Loader"
        ]
    }
}
```
 

The [injected-services](/docs/development/testing/test_component.md#run-external-services)entry starts the hermetic services our mod will need, mostly related tographics. In addition, the `fuchsia.posix.socket.Provider` system service and`deprecated-shell` feature are needed to allow Flutter Driver to interact withthe Dart Observatory. [injected-services]（/ docs / development / testing / test_component.mdrun-external-services）条目启动了我们的mod所需的密封服务，主要涉及图形。另外，还需要`fuchsia.posix.socket.Provider`系统服务和`deprecated-shell`功能，以允许Flutter Driver与Dart天文台进行交互。

 
### BUILD.gn target {#build-gn-target}  BUILD.gn目标{build-gn-target} 

The test itself also needs a target in the [`BUILD.gn`](https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/BUILD.gn). 测试本身还需要[`BUILD.gn`]（https://fuchsia.googlesource.com/topaz/+/HEAD/examples/test/driver_example_mod/BUILD.gn）中的目标。

```gn
dart_fuchsia_test("driver_example_mod_tests") {
  deps = [
    "//sdk/fidl/fuchsia.sys",
    "//third_party/dart-pkg/git/flutter/packages/flutter_driver",
    "//third_party/dart-pkg/pub/test",
    "//topaz/public/dart/fuchsia_modular_testing",
    "//topaz/public/dart/fuchsia_services",
  ]

  meta = [
    {
      path = rebase_path("meta/driver_example_mod_tests.cmx")
      dest = "driver_example_mod_tests.cmx"
    },
  ]

  environments = []

  # Flutter driver is only available in debug builds.
  if (is_debug) {
    environments += [
      nuc_env,
      vim2_env,
    ]
  }
}
```
 

[`dart_fuchsia_test`](https://fuchsia.googlesource.com/topaz/+/master/runtime/dart/dart_fuchsia_test.gni) defines a Dart test that runs on a Fuchsia device. It uses each file in the`test` subfolder that ends in `_test.dart` as an entrypoint for tests. Inaddition, it links the component manifest for the tests and specifies the[environments](/docs/development/testing/environments.md)in which to run the test in automated testing (CI/CQ). (See also the predefinedenvironments in[//build/testing/environments.gni](/build/testing/environments.gni).) [`dart_fuchsia_test`]（https://fuchsia.googlesource.com/topaz/+/master/runtime/dart/dart_fuchsia_test.gni）定义了在Fuchsia设备上运行的Dart测试。它使用`test`子文件夹中每个以'_test.dart'结尾的文件作为测试的入口。另外，它链接测试的组件清单并指定要在自动测试（CI / CQ）中运行测试的[environments]（/ docs / development / testing / environments.md）。 （另请参见[//build/testing/environments.gni]（/build/testing/environments.gni）中的预定义环境。）

 
### Topaz Package  黄玉包装 

Once you have this target available, you can add it to the build tree. In the case of `driver_example_mod`, this can be done in[`//topaz:tests`](https://fuchsia.googlesource.com/topaz/+/HEAD/BUILD.gn)to be available in `//topaz/bundles:buildbot` and other configurations, like so: 一旦有了该目标，就可以将其添加到构建树中。对于`driver_example_mod`，可以在[`//topaz:tests`](https://fuchsia.googlesource.com/topaz/+/HEAD/BUILD.gn）中完成，以便在`//中可用topaz / bundles：buildbot`和其他配置，例如：

```gn
group("tests") {
  testonly = true
  public_deps = [
    # ...
    "//topaz/examples/test/driver_example_mod",
    "//topaz/examples/test/driver_example_mod:driver_example_mod_tests",
    # ...
  ]
}
```
 

With that you’re ready to run your test on your device.  这样，您就可以在设备上运行测试了。

 
## Running Your Tests  运行测试 

To run your tests, you first need to make sure you're building a configuration that includes your test packages. One typical way is to use the `core` productand `//topaz/bundles:buildbot` bundle, as that is what the CI/CQ bots use. 要运行测试，首先需要确保所构建的配置包含测试包。一种典型的方法是使用“核心”产品和“ // topaz / bundles：buildbot”捆绑包，因为CI / CQ僵尸程序使用的是捆绑包。

```bash
$ fx set core.arm64 --with //topaz/bundles:buildbot
```
 

(If you are on an Acer or Nuc, use `x64` rather than `arm64` as the board.)  （如果您使用的是Acer或Nuc，请使用“ x64”而不是“ arm64”作为开发板。）

Then, build and pave or OTA as necessary.  然后，根据需要进行构建和铺装或OTA。

```bash
$ fx build
$ fx serve / ota / reboot
```
 

The tests can then be run using  然后可以使用以下命令运行测试

```bash
$ fx run-test driver_example_mod_tests
```
 

