# QYAI · AutoDL 镜像代码仓库

用于 AutoDL「发布镜像」的算法代码载体。镜像内置 ComfyUI H3 视频生成环境与轻语AI 面板。

## 镜像内容

- ComfyUI H3：`/root/ComfyUI-h3`，监听 `0.0.0.0:6006`
- 轻语AI 面板：`/root/panel`，监听 `0.0.0.0:6008`，健康检查 `GET /api/health`
- 工作流以 `.wfj` 密文形式存放于 `ComfyUI/user/default/workflows/`，面板运行期在内存解密

## 开机与访问

自启已做进镜像：`/etc/autodl.sh` 是 AutoDL 平台的开机钩子（容器 pid1 `bash /init/boot/boot.sh` → `/init/bin/customer.cmd.sh` 会执行它），其内容只有一行调用 `/root/boot.sh`。因此从本镜像开出的实例，开机后自动拉起面板，再由面板启动并监管 ComfyUI。

| 平台 | 开机时 | 你需要做什么 |
|---|---|---|
| `https://www.autodl.com/` | 平台钩子执行镜像内 `/etc/autodl.sh`，进而执行 `boot.sh` | 一般无需操作；若端口访问不到，手动执行一次 `bash /root/boot.sh` |
| `https://www.autodl.art/` | 平台自带开机运行脚本，环境自动拉起 | 无需执行，直接访问端口 |

`bash /root/boot.sh` 会拉起面板，之后由面板启动并监管 ComfyUI。实测：面板约 2 秒 ready，ComfyUI 约 10 秒到 `ready`。

- 面板：`http://<实例地址>:6008`，健康检查 `GET /api/health`
- ComfyUI：`http://<实例地址>:6006`，首次启动约需 10~60 秒，`/api/comfy/status` 变为 `ready` 后可用

## 环境自检

```bash
cd /root
/root/ComfyUI-h3/.venv/bin/python QYAI-autodl/check_env.py
```

仓库已随镜像预置在 `/root/QYAI-autodl`，`git remote` 指向 `https://github.com/GetRichPills/QYAI-autodl.git`，满足 autodl.art 审核标准：`/root` 下有对应 Git 代码仓库，且仓库内代码可直接执行。若该目录缺失，执行 `git clone https://github.com/GetRichPills/QYAI-autodl.git /root/QYAI-autodl` 重新拉取。

实例内没有系统级 `python3`，请使用 ComfyUI 虚拟环境解释器 `/root/ComfyUI-h3/.venv/bin/python`。
`check_env.py` 会打印 Python / PyTorch / CUDA 版本，校验 ComfyUI 目录与工作流密文；面板健康状态为提示项。
核心项全部通过时退出码为 0，因此刚开机、面板尚未启动时执行同样返回 0。

## 目录约定（镜像内）

| 路径 | 说明 |
|---|---|
| `/root/ComfyUI-h3` | ComfyUI 主程序与 H3 插件 |
| `/root/panel` | 轻语AI 面板（已编译为 `.pyc` / `.so`） |
| `/root/autodl-tmp/panel-data` | 面板数据目录 |
| `/root/start-comfyui.sh` | 手动启动 ComfyUI 的脚本 |
| `/root/QYAI-autodl` | 本仓库（镜像内预置，供审核与自检） |
| `/etc/autodl.sh` | AutoDL 平台开机钩子，调用 `/root/boot.sh` |

## 说明

本仓库仅用于镜像发布校验，不含工作流明文、密钥、模型权重或用户数据。
