"""本仓独立运行单测时的导入垫片。

测试按官方插件仓约定经生产命名空间 ``app.plugins.zspacevideo`` 导入。官方仓由 MoviePilot
后端的测试引导提供这个命名空间；本仓单独跑时没有后端，这里把 ``app.plugins.zspacevideo``
登记成指向插件目录的空壳包（不执行插件入口），``core/`` 纯逻辑照常导入。
装了 MoviePilot 后端时不做任何事。
"""

import importlib.util
import sys
import types
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parents[1] / "plugins.v3" / "zspacevideo"


def _shim() -> None:
    if importlib.util.find_spec("app") is not None:
        return
    for name, path in (("app", None), ("app.plugins", None), ("app.plugins.zspacevideo", PLUGIN_DIR)):
        module = types.ModuleType(name)
        module.__path__ = [str(path)] if path else []
        sys.modules[name] = module
    sys.modules["app"].plugins = sys.modules["app.plugins"]
    sys.modules["app.plugins"].zspacevideo = sys.modules["app.plugins.zspacevideo"]


_shim()
