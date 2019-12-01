 
# Testing Isolated Cache Storage  测试隔离的缓存存储 

A component may request that persistent storage be present in its incoming namespace under `/cache` by using [the `isolated-cache-storage`feature][cache-feature]. This directory, unlike the storage provided by`isolated-persistent-storage`, will be cleaned up by the system when diskpressure is high. This cache cleaning event will walk _every_ component's cachestorage and unlink everything it finds. 组件可以通过使用[isolated-cache-storage`feature] [cache-feature]请求在/ cache下的传入名称空间中存在持久性存储。与“ isolated-persistent-storage”提供的存储不同，该目录将在磁盘压力较高时由系统清理。此缓存清理事件将遍历_every_组件的缓存并取消链接其找到的所有内容。

Because this cache cleaning event only happens under very specific situations, a service interface named [`fuchsia.sys.test.CacheControl`][cache-control] isprovided to allow tests to cause cache clearing events. To exercise thisinterface tests should cause components under test to populate items in their`/cache` storage, the test should call the `Clear()` function in`fuchsia.sys.test.CacheControl`, and then the test should ensure that thecomponent continues to behave correctly when faced with this unexpected removalof a file it needs. 因为此缓存清除事件仅在非常特定的情况下发生，所以提供了名为[`fuchsia.sys.test.CacheControl`] [cache-control]的服务接口，以允许测试引起缓存清除事件。要使用此接口，测试应导致被测组件填充其“ / cache”存储中的项目，测试应调用fuchsia.sys.test.CacheControl中的“ Clear（）”函数，然后测试应确保该组件遇到此所需的文件的意外删除时，继续运行正常。

Note that components not related to the test will also have their caches cleared when the `Clear()` function is called. The function clears the cache of everycomponent on the system. 请注意，与“测试”无关的组件也将在调用“ Clear（）”函数时清除其缓存。该功能清除系统上每个组件的缓存。

An example demonstrating test coverage of a user of `isolated-cache-storage` is available at [`//examples/isolated_cache`][cache-example]. 可以在[`// examples / isolated_cache]] [cache-example]中找到一个示例，说明用户对“ isolated-cache-storage”的测试覆盖率。

