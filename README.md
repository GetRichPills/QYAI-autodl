# QYAI · AutoDL 镜像代码仓库

用于 AutoDL「发布镜像」的算法代码载体。镜像内置 ComfyUI H3 视频生成环境与轻语AI 面板。

## 镜像内容

- ComfyUI H3：`/root/ComfyUI-h3`，监听 `0.0.0.0:6006`
- 轻语AI 面板：`/root/panel`，监听 `0.0.0.0:6008`，健康检查 `GET /api/health`
- 工作流以 `.wfj` 密文形式存放于 `ComfyUI/user/default/workflows/`，面板运行期在内存解密

## 开机与访问

实例开机后需执行一次启动脚本（面板会自行拉起并监管 ComfyUI）：

```bash
bash /root/boot.sh
```

建议在 AutoDL 控制台把「开机执行命令」设为 `bash /root/boot.sh`，否则新实例开机后面板与 ComfyUI 不会自动启动。

- 面板：`http://<实例地址>:6008`，健康检查 `GET /api/health`
- ComfyUI：`http://<实例地址>:6006`，首次启动约需 10~60 秒，`/api/comfy/status` 变为 `ready` 后可用

## 环境自检

```bash
cd /root
git clone https://github.com/GetRichPills/QYAI-autodl.git
/root/ComfyUI-h3/.venv/bin/python QYAI-autodl/check_env.py
```

实例内没有系统级 `python3`，请使用 ComfyUI 虚拟环境解释器 `/root/ComfyUI-h3/.venv/bin/python`。
`check_env.py` 会打印 Python / PyTorch / CUDA 版本，校验 ComfyUI 目录、工作流密文以及面板健康状态。
核心项全部通过时退出码为 0。

## 目录约定（镜像内）

| 路径 | 说明 |
|---|---|
| `/root/ComfyUI-h3` | ComfyUI 主程序与 H3 插件 |
| `/root/panel` | 轻语AI 面板（已编译为 `.pyc` / `.so`） |
| `/root/autodl-tmp/panel-data` | 面板数据目录 |
| `/root/start-comfyui.sh` | 手动启动 ComfyUI 的脚本 |

## 说明

本仓库仅用于镜像发布校验，不含工作流明文、密钥、模型权重或用户数据。
