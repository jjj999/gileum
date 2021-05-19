from importlib.machinery import ModuleSpec
import importlib.util
import inspect
import os
from pathlib import Path
import sys
import typing as t

from .gileum import BaseGileum
from .manager import _get_glm_manager


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


def _search_glm_from_mod(mod: ModuleSpec) -> t.List[BaseGileum]:
    f_predicate = lambda obj: isinstance(obj, BaseGileum)
    return [val for _, val in inspect.getmembers(mod, f_predicate)]


def _has_glmfile_name(file: str) -> bool:
    base = os.path.basename(file)
    return base.startswith("glm_") and base.endswith(".py")


def list_glmfiles(dir: str, join: bool = True) -> t.List[str]:
    files = filter(_has_glmfile_name, os.listdir(dir))
    if join:
        files = map(lambda f: os.path.join(dir, f), files)
    return list(files)


def load_glms_at(file: str) -> None:
    mod = _import_directly(file)
    glms = _search_glm_from_mod(mod)

    manager = _get_glm_manager()
    for glm in glms:
        manager._set_glm(glm)


def load_glms_in(dir: str) -> None:
    for gilfile in list_glmfiles(dir):
        load_glms_at(gilfile)
