from importlib.machinery import ModuleSpec
import importlib.util
import inspect
import os
from pathlib import Path
import sys
from typing import List, Optional

from .gileum import BaseGileum
from .manager import _get_glm_manager


GILEUM_FILE_SUFFIX = ".glm.py"


def _convert2relative_path(path: str) -> str:
    return str(Path(path).relative_to(os.getcwd()))


def _import_directly(file: str) -> ModuleSpec:
    if os.path.isabs(file):
        file = _convert2relative_path(file)
    mod_name = file.replace(os.sep, ".")
    spec = importlib.util.spec_from_file_location(mod_name, file)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _search_glm_from_mod(mod: ModuleSpec) -> List[BaseGileum]:
    f_predicate = lambda obj: isinstance(obj, BaseGileum)
    return [val for _, val in inspect.getmembers(mod, f_predicate)]


def _has_glmfile_name(file: str) -> bool:
    base = os.path.basename(file)
    return base.startswith("glm_") and base.endswith(".py")


def list_glmfiles(
    dir: str,
    join: bool = True,
) -> List[str]:
    files = filter(_has_glmfile_name, os.listdir(dir))
    if join:
        files = map(lambda f: os.path.join(dir, f), files)
    return list(files)


def load_glms_at(
    file: str,
    name: Optional[str] = None,
) -> None:
    mod = _import_directly(file)
    glms = _search_glm_from_mod(mod)

    manager = _get_glm_manager()
    for glm in glms:
        if name is None:
            manager._set_glm(glm)
        elif glm.__glm_name__ == name:
            manager._set_glm(glm)


def load_glms_in(
    dir: str,
    name: Optional[str] = None,
) -> None:
    for gilfile in list_glmfiles(dir):
        load_glms_at(gilfile, name=name)
