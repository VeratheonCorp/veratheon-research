# server/server.py
import os
import sys
from pathlib import Path
import importlib.util
import uvicorn

def load_app_from_api() -> object:
    """Load FastAPI app from server/api.py without importing package name 'server'.

    This avoids the module/package name collision between this launcher file
    'server.py' and the 'server/' package directory.
    """
    api_path = Path(__file__).parent / "server" / "api.py"
    spec = importlib.util.spec_from_file_location("server_api", str(api_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module spec from {api_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["server_api"] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    if not hasattr(module, "app"):
        raise AttributeError("The module 'server/api.py' does not define 'app'")
    return getattr(module, "app")

if __name__ == "__main__":
    # Runs the FastAPI app defined in server/api.py while avoiding import name collision
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8085"))
    reload = os.getenv("RELOAD", "false").lower() in {"1", "true", "yes", "on"}
    app = load_app_from_api()
    uvicorn.run(app, host=host, port=port, reload=reload)