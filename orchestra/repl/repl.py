from dataclasses import dataclass
from typing import Any, Dict, Mapping, Tuple

from .utils import exec_non_blocking


@dataclass
class REPLState:
    is_active: bool
    globals: Dict[str, Any]
    locals: Mapping[str, object]


@dataclass(frozen=True)
class REPL:
    index: int
    depth: int
    parent: Tuple[int, int]
    state: REPLState


@dataclass(frozen=True)
class REPLRequest:
    index: int
    depth: int
    code: str


async def process_repl_request(state: REPLState, request: REPLRequest) -> str:
    # Here we have to handle errors and stdout
    await exec_non_blocking(request.code, state.globals, state.locals)
    return "PLACEHOLDER"
