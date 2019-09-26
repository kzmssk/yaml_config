from yaml_config.yaml_config import YamlConfig
import dataclasses
import typing
import pathlib
import tempfile


@dataclasses.dataclass
class MySubSubConfig(YamlConfig):
    val_float: float
    val_list: typing.List[int]
    val_str: str


@dataclasses.dataclass
class MySubConfig(YamlConfig):
    val_int: int
    val_path: pathlib.Path
    sub_sub_config: MySubSubConfig


@dataclasses.dataclass
class MyConfig(YamlConfig):
    sub_config: MySubConfig


def test_config():

    config = MyConfig(
        sub_config=MySubConfig(val_int=1,
                               val_path=pathlib.Path('./2'),
                               sub_sub_config=MySubSubConfig(val_float=3.0, val_list=[1, 2, 3, 4], val_str='5')))

    with tempfile.TemporaryDirectory() as d:
        config_path = pathlib.Path(str(d)) / 'tmp.yaml'

        # dump into YAML file
        config.save(config_path)

        # restore from YAML file
        config_load = MyConfig.load(config_path)

        assert config == config_load
