 
# Guide to Configuring the Modular Framework  配置模块化框架指南 

 
## Requirements  要求 

To configure the modular framework, you will need to create a JSON file defining the required configurations for `basemgr` and `sessionmgr` as detailed below.The configuration file should be packaged via the build rule `modular_config`,which will validate your file against a schema. You must then include themodular_config() target in the product's base packages. 要配置模块化框架，您将需要创建一个JSON文件，定义“ basemgr”和“ sessionmgr”的必需配置，如下所述。配置文件应通过构建规则“ modular_config”打包，以验证您的文件是否符合模式。然后，您必须在产品的基本程序包中包含modular_config（）目标。

 
## Example  例 

```
{
  "basemgr": {
    "enable_cobalt": false,
    "use_session_shell_for_story_shell_factory": true,
    "base_shell": {
      "url": "fuchsia-pkg://fuchsia.com/dev_base_shell#meta/dev_base_shell.cmx",
    },
    "session_shells": [
      {
        "url": "fuchsia-pkg://fuchsia.com/ermine_session_shell#meta/ermine_session_shell.cmx",
        "display_usage": "near",
        "screen_height": 50,
        "screen_width": 100
      }
    ]
  },
  "sessionmgr": {
    "use_memfs_for_ledger": true,
    "cloud_provider": "NONE",
    "startup_agents": [
      "fuchsia-pkg://fuchsia.com/startup_agent#meta/startup_agent.cmx"
    ],
    "session_agents": [
      "fuchsia-pkg://fuchsia.com/session_agent#meta/session_agent.cmx"
    ],
    "component_args": [
      {
        "uri": "fuchsia-pkg://fuchsia.com/startup_agent#meta/startup_agent.cmx",
        "args": [ "--foo", "--bar=true" ]
      }
    ],
    "agent_service_index": [
      {
        "service_name": "fuchsia.modular.SomeServiceName",
        "agent_url": "fuchsia-pkg://fuchsia.com/some_agent#meta/some_agent.cmx"
      }
    ]
  }
}
```
 

 
## Basemgr fields  Basemgr字段 

 
- `base_shell` **boolean** _(required)_  -`base_shell` **布尔值** _（必需）_
  - `url`: **string** _(required)_  -`url`：**字符串** _（必填）_
    - The fuchsia component url for which base shell to use.  -紫红色组件的URL用于哪个基础外壳。
  - `keep_alive_after_login` **boolean** _(optional)_  -`keep_alive_after_login` **布尔值** _（可选）_
    - When set to true, the base shell is kept alive after a log in. This is used for testing because current integration tests expect base shellto always be running. -设置为true时，登录后基本外壳将保持活动状态。这用于测试，因为当前的集成测试期望基本外壳始终运行。
    - **default**: `false`  -**默认**：`false`
  - `args` **string[]** _(optional)_  -`args` ** string [] ** _（可选）_
    - A list of arguments to be passed to the base shell specified by url. Arguments must be prefixed with --. -要传递给url指定的基本shell的参数列表。参数必须以-为前缀。
- `session_shells` **array** _(required)_  -`session_shells` **数组** _（必需）_
  - Lists all the session shells with each shell containing the following fields: -列出所有会话外壳，每个外壳包含以下字段：
    - `url`: **string** _(required)_  -`url`：**字符串** _（必填）_
      - The fuchsia component url for which session shell to use.  -会话外壳程序使用的紫红色组件url。
    - `display_usage`: **string** _(optional)_  -`display_usage`：**字符串** _（可选）_
      - The display usage policy for this session shell.  -此会话外壳的显示使用策略。
      - Options:  -选项：
        - `handheld`: the display is used well within arm's reach.  -“手持”：显示器在手臂可及的范围内可以很好地使用。
        - `close`: the display is used at arm's reach.  -`close`：在手臂可及的地方使用显示器。
        - `near`: the display is used beyond arm's reach.  -`near`：显示器超出了手臂的触及范围。
        - `midrange`: the display is used beyond arm's reach.  -`midrange`：显示超出了手臂的使用范围。
        - `far`: the display is used well beyond arm's reach.  -`far`：显示器在手臂无法触及的范围内使用。
    - `screen_height`: **float** _(optional)_  -`screen_height`：**浮动** _（可选）_
      - The screen height in millimeters for the session shell's display.  -会话外壳程序显示的屏幕高度（以毫米为单位）。
    - `screen_width`: **float** _(optional)_  -`screen_width`：** float ** _（可选）_
      - The screen width in millimeters for the session shell's display.  -会话外壳程序显示的屏幕宽度（以毫米为单位）。
- `story_shell_url`: **string** _(optional)_  -`story_shell_url`：**字符串** _（可选）_
  - The fuchsia component url for which story shell to use.  -故事外壳使用的紫红色成分网址。
  - **default**: `fuchsia-pkg://fuchsia.com/mondrian#meta/mondrian.cmx`  -**默认**：`fuchsia-pkg：// fuchsia.com / mondrianmeta / mondrian.cmx`
- `enable_cobalt`: **boolean** _(optional)_  -`enable_cobalt`：布尔值_（可选）_
  - When set to false, Cobalt statistics are disabled.  -设置为false时，禁用钴统计。
  - **default**: `true`  -**默认**：`true`
- `use_minfs`: **boolean** _(optional)_  -`use_minfs`：布尔值_（可选）_
  - When set to true, wait for persistent data to initialize.  -设置为true时，等待持久性数据初始化。
  - **default**: `true`  -**默认**：`true`
- `use_session_shell_for_story_shell_factory`: **boolean** _(optional)_  -`use_session_shell_for_story_shell_factory`：布尔值_（可选）_
  - Create story shells through StoryShellFactory exposed by the session shell instead of creating separate story shell components. When set,`story_shell_url` and any story shell args are ignored. -通过会话外壳公开的StoryShellFactory创建故事外壳，而不是创建单独的故事外壳组件。设置后，`story_shell_url`和任何故事外壳参数将被忽略。
  - **default**: `false`  -**默认**：`false`

 
## Sessionmgr fields  Sessionmgr字段 

 
- `cloud_provider`: **string** _(optional)_  -`cloud_provider`：**字符串** _（可选）_
  - Options:  -选项：
    - `LET_LEDGER_DECIDE`: Use a cloud provider configured by ledger.  -`LET_LEDGER_DECIDE`：使用由账本配置的云提供商。
    - `FROM_ENVIRONMENT`: Use a cloud provider available in the incoming namespace, rather than initializing and instance within sessionmgr.This can be used to inject a custom cloud provider. -`FROM_ENVIRONMENT`：使用传入名称空间中可用的云提供程序，而不是在sessionmgr中进行初始化和实例化。这可用于注入自定义云提供程序。
    - `NONE`: Do not use a cloud provider.  -`NONE`：请勿使用云提供商。
  - **default**: `LET_LEDGER_DECIDE`  -**默认**：`LET_LEDGER_DECIDE`
- `enable_cobalt`: **boolean** _(optional)_  -`enable_cobalt`：布尔值_（可选）_
  - When set to false, Cobalt statistics are disabled. This is used for testing. -设置为false时，禁用钴统计。这用于测试。
  - **default**: `true`  -**默认**：`true`
- `enable_story_shell_preload`: **boolean** _(optional)_  -`enable_story_shell_preload`：**布尔值** _（可选）_
  - When set to false, StoryShell instances are not warmed up as a startup latency optimization. This is used for testing. -设置为false时，StoryShell实例不会作为启动延迟优化而预热。这用于测试。
  - **default**: `true`  -**默认**：`true`
- `use_memfs_for_ledger`: **boolean** _(optional)_  -`use_memfs_for_ledger`：**布尔值** _（可选）_
  - Tells the sessionmgr whether it should host+pass a memfs-backed directory to the ledger for the user's repository, or to use /data/LEDGER. -告诉sessionmgr是应该主机+将memfs支持的目录传递给用户存储库的分类帐，还是使用/ data / LEDGER。
  - **default**: `false`  -**默认**：`false`
- `startup_agents`: **string[]** _(optional)_  -`startup_agents`：** string [] ** _（可选）_
  - A list of fuchsia component urls that specify which agents to launch at startup. -紫红色组件url的列表，用于指定启动时要启动的代理。
- `session_agents`: **string[]** _(optional)_  -`session_agents`：** string [] ** _（可选）_
  - A list of fuchsia component urls that specify which agents to launch at startup with PuppetMaster and FocusProvider services. -紫红色组件url的列表，用于指定在启动时使用PuppetMaster和FocusProvider服务启动的代理。
- `component_args`: **array** _(optional)_  -`component_args`：**数组** _（可选）_
  - A list of key/value pairs to construct a map from component URI to arguments list for that component. Presence in this list results in thegiven arguments passed to the component as its argv at launch. -键/值对列表，用于构造从组件URI到该组件的参数列表的映射。此列表中的存在导致给定的参数在启动时作为其argv传递给组件。
    - `uri`: The component's uri.  -`uri`：组件的uri。
    - `args`: A list of arguments to be passed to the component specified by `uri`. Arguments must be prefixed with --. -args：要传递给uri指定的组件的参数列表。参数必须以-为前缀。
- `agent_service_index`: **array** _(optional)_  -`agent_service_index`：**数组** _（可选）_
  - A list of key/value pairs to construct a map from service name to the serving agent's URL. Service names must be unique, so only one agent canprovide a given named service. -键/值对列表，用于构建从服务名称到服务代理URL的映射。服务名称必须唯一，因此只有一个代理可以提供给定的命名服务。
    - `service_name`: The name of a service offered by a session agent.  -`service_name`：会话代理提供的服务的名称。
