#!/usr/bin/env python3
"""QYAI AutoDL 镜像环境自检。核心项全部通过时退出码为 0。"""
import glob
import json
import os
import sys
import urllib.request

COMFY = "/root/ComfyUI-h3/ComfyUI"
PANEL_HEALTH = "http://127.0.0.1:6008/api/health"
WF_DIR = os.path.join(COMFY, "user", "default", "workflows")


def ok(name, passed, detail=""):
    print(f"[{'PASS' if passed else 'FAIL'}] {name}" + (f" -> {detail}" if detail else ""))
    return passed


def main():
    results = []

    v = sys.version_info
    results.append(ok("python", v >= (3, 8), f"{v.major}.{v.minor}.{v.micro}"))

    try:
        import torch
        detail = f"torch {torch.__version__}, cuda {torch.version.cuda}, available {torch.cuda.is_available()}"
        if torch.cuda.is_available():
            detail += f", device {torch.cuda.get_device_name(0)}"
        results.append(ok("torch", True, detail))
    except Exception as exc:
        results.append(ok("torch", False, repr(exc)))

    results.append(ok("comfyui_dir", os.path.isdir(COMFY), COMFY))

    vaults = sorted(glob.glob(os.path.join(WF_DIR, "*.wfj")))
    if vaults:
        head = open(vaults[0], "rb").read(5)
        results.append(ok("workflows", head == b"WFJ1\n", f"{len(vaults)} 个 .wfj，{os.path.basename(vaults[0])} magic={head!r}"))
    else:
        results.append(ok("workflows", False, f"{WF_DIR} 下没有 .wfj"))

    try:
        with urllib.request.urlopen(PANEL_HEALTH, timeout=5) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        results.append(ok("panel", resp.status == 200, f"HTTP {resp.status} {body}"))
    except Exception as exc:
        results.append(ok("panel", False, repr(exc)))

    passed = sum(1 for r in results if r)
    print(f"\n{passed}/{len(results)} 项通过")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
