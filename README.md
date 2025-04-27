# 扫地机器人控制MCP Server

[English](README_EN.md) | 中文

科沃斯核心API现已全面兼容MCP协议，是全球首家兼容MCP协议的机器人服务商。

科沃斯已经完成了4个核心API接口和MCP协议的对接，包括设备列表查询、清扫控制、回充控制和工作状态查询。

作为全球首家支持MCP协议的清洁机器人服务商，科沃斯MCP Server发布后，智能体开发者仅需简单配置，就可以在大模型中快速接入机器人服务，实现查询、清扫、回充等能力。

大幅降低了智能体应用开发过程中调用机器人控制服务相关能力的门槛，显著提升了智能体应用的开发效率。

## 工具

### 设备列表查询

获取用户绑定的所有机器人列表。

#### Input:

无参数

#### Returns:

```json
{
  "status": 0,
  "message": "success",
  "data": [
    {
      "nickname": "机器人昵称",
    }
  ]
}
```

### 启动清扫

控制扫地机器人开始、暂停、恢复或停止清扫。

#### Input:

- `nickname`: 机器人的昵称，用于查找设备，支持模糊匹配
- `act`: 清扫行为
  - `s`: 开始清扫
  - `r`: 恢复清扫
  - `p`: 暂停清扫
  - `h`: 停止清扫

#### Returns:

```json
{
  "msg": "OK",
  "code": 0,
  "data": []
}
```

### 控制回充

控制机器人开始或停止回充。

#### Input:

- `nickname`: 机器人昵称，用于查找设备
- `act`: 机器行为
  - `go-start`: 开始回充
  - `stopGo`: 结束回充

#### Returns:

```json
{
  "msg": "OK",
  "code": 0,
  "data": []
}
```

### 查询工作状态

查询机器人当前的工作状态。

#### Input:

- `nickname`: 机器人昵称，用于查找设备

#### Returns:

```json
{
	"code": 0,
	"msg": "success",
	"data": {
		"ctl": {
			"data": {
				"ret": "ok",
				"cleanSt": "h",
				"chargeSt": "charging",
				"stationSt": "i"
			}
		}
	}
}
```

**状态码说明：**

| 参数名     | 类型           | 说明                                                                                                                                                                                                                                                                      |
| ---------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cleanSt    | string         | 清扫状态，请求成功时存在。s-清扫中，p-暂停中，h-空闲中，goposition-正在前往指定位置，gopositionpause-在指定点停止，findpet-寻找宠物，findpetpause-寻找宠物暂停，cruise-巡航中，cruisepause-巡航暂停，buildmap-创建地图，buildmappause-建图暂停 |
| chargeSt   | string         | 充电状态，请求成功时存在。g-正在回充，gp-回充暂停，i-空闲，sc-底座充电，wc-线充，charging-充电中（包括SC和WC）  
| stationSt  | string         | 基站状态，i-空闲，wash-正在清洗拖布，dry-正在烘干，drypause-烘干暂停，dust-集尘中，dustpause-集尘暂停，clean-基站清洁，cleanpause-基站清洁暂停，wash-清洗拖布，washpause-清洗拖布暂停  

## 开始

## 安装

### github本地安装

```bash
git clone git@github.com:ecovacs-ai/ecovacs-mcp.git

uv add "mcp[cli]" mcp requests

uv run ecovacs_mcp/robot_mcp_stdio.py
```

### pipy

```
pip install ecovacs-robot-mcp

python3 -m ecovacs_robot_mcp

```

## 环境变量

- `ECO_API_KEY`: API访问密钥，用于验证接口调用权限
- `ECO_API_URL`: API HOST
  - 中国内地： `https://open.ecovacs.cn`
  - 非中国内地： `https://open.ecovacs.com`

## 获取AK & 删除AK

在选择两种方法（本地或者SSE）之前，你需要在[科沃斯开放平台的控制台](https://open.ecovacs.cn)中创建一个服务端AK，通过AK你才能够调用机器人的API能力。

如果你想取消授权，在[科沃斯开放平台的控制台](https://open.ecovacs.cn)中同样可以移除AK的授权。

科沃斯开放平台（中国内地）：https://open.ecovacs.cn

科沃斯开放平台（非中国内地）：https://open.ecovacs.com

<img src="images/img_v3_02lo_b450632b-9dbe-4cd9-aead-c625ad3458fg.jpg" alt="获取AK" width="600" />

## 使用示例（Claude示列）

打开Claude for Desktop的Setting，切换到Developer，点击Edit Config，用任意的IDE打开配置文件。

<img src="images/img_v3_02lm_ac10ff15-8764-4ad3-906c-5c8433a9e5eg.jpg" alt="Claude设置界面" width="600" />

<img src="images/img_v3_02lm_2ced9293-af22-4d9f-a70c-337643a93c7g.jpg" alt="Claude配置文件" width="600" />

将以下配置添加到配置文件中，ECO_API_KEY 是访问科沃斯开放平台API的AK，在[此页面](https://open.ecovacs.cn/preparationForUse)中申请获取：

```json
{
    "mcpServers": {
        "ecovacs_mcp": {
            "command": "/Users/home/.local/bin/uv",
            "args": [
                "--directory",
                "/Users/home/ecovacs-mcp-main/ecovacs_mcp",
                "run",
                "robot_mcp_stdio.py"
            ],
            "env": {
                "ECO_API_KEY": "your AK...........",
                "ECO_API_URL": "https://open.ecovacs.cn" // 如果是非中国内地，配置为 https://open.ecovacs.com
            }
        }
    }
}
```

重启Claude，此时设置面板已经成功加载了科沃斯机器人MCP Server。在软件主界面对话框处可以看到有4个可用的MCP工具，点击可以查看详情。

<img src="images/img_v3_02lm_e1b700d6-9693-4448-8acf-d622f28b3b3g.jpg" alt="Claude MCP工具" width="600" />

#### 效果

接下来就可以进行提问，验证科沃斯机器人小助手的能力了。

<img src="images/img_v3_02lm_2f3b431a-c289-4476-8a24-1ff1a231aadg.jpg" alt="Claude交互效果" width="600" />


## 使用示例（Cursor示列）
### 进入 Cursor 设置界面配置 SSE 连接

<img src="images/doc_1743660020811_d2b5c.6bec4f04.png" alt="Cursor设置界面" width="600" />

### 添加一个新的 MCP Server 配置

- 中国内地
```json
{
  "mcpServers": {
    "robot_control_server": {
      "url": "https://open.ecovacs.cn/sse?ak=your ak"
      // For regions outside Mainland China, configure as https://open.ecovacs.com/sse?ak=your ak
    }
  }
}
```
- 非中国内地
```json
{
  "mcpServers": {
    "robot_control_server": {
      "url": "https://open.ecovacs.com/sse?ak=your ak"
    }
  }
}
```
### 返回 Cursor 设置界面查看 MCP 服务工具状态

<img src="images/20250423-175131.0caa52fa.jpg" alt="Cursor MCP服务状态" width="600" />

### 选择配置 Cursor 大模型让你拥有更好的服务体验，建议选择 claude-3.7-sonnet

<img src="images/doc_1743660126834_d2b5c.fc9da8f3.png" alt="Cursor模型配置" width="600" />

### 模型交互模式 ：选择 Agent 方式

<img src="images/doc_1743660181250_d2b5c.1d9a47eb.png" alt="Cursor交互模式" width="600" />

### 效果

<img src="images/img_v3_02lm_f5094f2f-7cf3-4ee4-a5f9-ae29b746175g.jpg" alt="Cursor交互模式" width="600" />

## 许可证

[MIT](LICENSE) © ecovacs

## 反馈

在使用科沃斯机器人MCP Server时遇到的任何问题，欢迎通过`issue或者联系我们，我们也欢迎每一个积极的`PR`，非常感谢各位的支持与贡献❤️

## 联系方式

Mail： pei.zhou@ecovacs.com

Wechat：

<img src="images/img_v3_02lm_d2a67ba9-6fa2-4f96-9d37-09f8d8b8e21g.png" alt="微信二维码" width="200" />

## 更新

| 版本 | 功能说明                   | 更新日期      |      |      |      |
| ---- | -------------------------- | ------------- | ---- | ---- | ---- |
| V1.0 | Ecovacs MCP Server正式上线 | 2025年4月24日 |      |      |      |

