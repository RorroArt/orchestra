from typing import Any, Dict, Mapping

import trio


async def exec_non_blocking(
    code: str, globals: Dict[str, Any], locals: Mapping[str, object]
):
    await trio.to_thread.run_sync(exec, globals, locals)
