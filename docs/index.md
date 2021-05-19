# [gileum](https://jjj999.github.io/gileum/)

[![PyPI version](https://badge.fury.io/py/gileum.svg)](http://badge.fury.io/py/gileum)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/gileum/)

## Installing

- Python: >= 3.7

```
python -m pip install gileum
```

## Basic Usage

*gileum* is a loader of configuration scripts written in Python. On *gileum*, a configuration can be implemented as a subclass of **gileum.BaseGileum**. `gileum.BaseGileum` is a light-weight wrapper of **pydantic.BaseModel**, so you can easily implemented the subclass in almost same way as *pydantic*.

### Developer-side

In source code of something like web application, a developer can implement a gileum class as below, which will be the interface to launch the app:

```python
from typing import Literal
from gileum import BaseGileum

class SampleGileum(BaseGileum):
    app_name: str
    hostname: str
    port: int
    glm_name: Literal["main", "test"]
```

Note that all subclasses of `gileum.BaseGileum` must have the field `glm_name` whose type must be Literal of some strings. The field may be used as a flag and the developer may judge the flag to determine how the app should work.

After the implementaion is done, the developer can invoke `gileum.load_glms_at()` specifying path of a configuration file for users to create:

```python
from gileum import load_glms_at

load_glms_at(path_to_config)
```

Note that configuration files have the naming rule like `glm_xxxxxx.py`, e.g. `glm_config.py`. There is also another function named `gileum.load_glms_in()`, which loads all the configuration files in specified directory.

Fianlly, the developer can access to the `SampleGileum` objects loaded by calling the `gileum.get_glm()` method:

```python
from gileum import get_glm

config_main = get_glm(SampleGileum, "main")
config_test = get_glm(SampleGileum, "test")

# Now you can access to the fields of the SampleGileum objects.
assert config_main.glm_name == "main"
assert config_test.glm_name == "test"
```

### User-side

A user of the app above needs to create a configuration file and generate two `SimpleGileum` objects. The location of the configuration file depends on apps the user uses. Now, let's assume that the name of the app package is *sample_app*, and in the app, the location is user's working directory. For example, the user can create a configuration file named `glm_config.py`, whose prefix is the naming rule of gileum, and generate the `SimpleGileum` objects:

```python
# glm_config.py
from sample_app import SimpleGileum

gileum_main = SimpleGileum(
    app_name="sample_app",
    hostname="example.com",
    port=443,
    glm_name="main"
)

gileum_main = SimpleGileum(
    app_name="sample_app@test",
    hostname="localhost",
    port=8000,
    glm_name="test"
)
```

That's it!! Now what you have to do the next is just to execute the app. The way of it depends on the app.
