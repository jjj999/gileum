from __future__ import annotations
from threading import RLock
import typing as t

from .gileum import BaseGileum


Gileum_t = t.TypeVar("Gileum_t", bound=BaseGileum)


class GileumManager:

    def __init__(self) -> None:
        self.__glms: t.Dict[t.Type[BaseGileum], t.Dict[str, BaseGileum]] = {}

    def _set_glm(self, glm: BaseGileum) -> None:
        if not isinstance(glm, BaseGileum):
            raise TypeError

        if not hasattr(glm, "glm_name"):
            raise AttributeError

        if glm.glm_name in self.__glms:
            return

        if self.__glms.get(glm.__class__) is None:
            self.__glms[glm.__class__] = {}
        self.__glms[glm.__class__][glm.glm_name] = glm

    def get_glm(self, typ: t.Type[Gileum_t], name: str = "main") -> Gileum_t:
        if typ not in self.__glms:
            raise ValueError(
                f"Any gileums typed with {typ.__name__} were not found."
            )
        if name not in self.__glms.get(typ):
            raise ValueError(
                f"{typ.__name__} named {name} was not found."
            )

        return self.__glms.get(typ).get(name)


class SyncGileumManager(GileumManager):

    def __init__(self) -> None:
        super().__init__()

        self.__lock = RLock()

    def _set_glm(self, glm: BaseGileum) -> None:
        with self.__lock:
            super()._set_glm(glm)

    def get_glm(self, typ: t.Type[Gileum_t], name: str = "main") -> Gileum_t:
        with self.__lock:
            res = super().get_glm(typ, name)
        return res


class GileumManagerAlreadySetError(Exception):
    pass


GileumManager_t = t.TypeVar("GileumManager_t", bound=GileumManager)
__glm_man__: t.Optional[GileumManager_t] = None


def init_glm_manager(manager: GileumManager_t) -> None:
    global __glm_man__

    # NOTE
    #   __glm_man__ must be a single object within runtime. There are some
    #   reasons for it:
    #
    #   1.  GileumManager object will be in the global scope regardless of
    #       implementation because, in most cases, setting information should
    #       be shared with all objects at runtime. It means the GileumManager
    #       object has its state within the global scope.
    #   2.  If __glm_man__ were resetable, then some objects referencing
    #       __glm_man__ would face the situation that sometimes __glm_man__
    #       had certain gileum, and sometimes __glm_man__ didn't have the one.

    if __glm_man__ is not None:
        raise GileumManagerAlreadySetError
    if not isinstance(manager, GileumManager):
        raise TypeError
    __glm_man__ = manager


def _get_glm_manager() -> GileumManager_t:
    global __glm_man__
    if __glm_man__ is None:
        __glm_man__ = GileumManager()
    return __glm_man__


def get_glm(typ: t.Type[Gileum_t], glm_name: str = "main") -> Gileum_t:
    glmman = _get_glm_manager()
    return glmman.get_glm(typ, glm_name)


# NOTE
#   This function is for testing. See the NOTE in `init_glm_manager` to
#   know the reasons for it.
def _reset_glm_manager() -> None:
    global __glm_man__
    __glm_man__ = None
