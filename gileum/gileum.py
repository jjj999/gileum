import sys

if sys.version_info.minor >= 8:
    from typing import Literal
else:
    from typing_extensions import Literal

from pydantic import BaseModel


class BaseGileum(BaseModel):

    # NOTE
    #   This field is used as a part in order to identify cerntain gileum
    #   object in a glm file. The value may be used as a flag to determine
    #   application's behavior.
    glm_name: Literal["main"] = "main"
