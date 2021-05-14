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


@dataclasses.dataclass
class MyConfigList(YamlConfig):
    sub_sub_configs: typing.List[MySubSubConfig]


@dataclasses.dataclass
class MyConfigDict(YamlConfig):
    sub_sub_configs: typing.Dict[str, MySubSubConfig]


@dataclasses.dataclass
class MyConfigListInDict(YamlConfig):
    sub_sub_configs: typing.Dict[str, typing.List[MySubSubConfig]]


@dataclasses.dataclass
class MyConfigDictInList(YamlConfig):
    sub_sub_configs: typing.List[typing.Dict[str, MySubSubConfig]]


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


def test_config_list():

    config = MyConfigList(
        sub_sub_configs=[
            MySubSubConfig(val_float=3.0, val_list=[1, 2, 3, 4], val_str='5'),
            MySubSubConfig(val_float=13.0, val_list=[5, 6, 7, 8], val_str='9')])

    with tempfile.TemporaryDirectory() as d:
        config_path = pathlib.Path(str(d)) / 'tmp.yaml'

        # dump into YAML file
        config.save(config_path)

        # restore from YAML file
        config_load = MyConfigList.load(config_path)

        assert config == config_load


def test_config_dict():

    config = MyConfigDict(
        sub_sub_configs={
            "abc": MySubSubConfig(val_float=3.0, val_list=[1, 2, 3, 4], val_str='5'),
            "def": MySubSubConfig(val_float=13.0, val_list=[5, 6, 7, 8], val_str='9')})

    with tempfile.TemporaryDirectory() as d:
        config_path = pathlib.Path(str(d)) / 'tmp.yaml'

        # dump into YAML file
        config.save(config_path)

        # restore from YAML file
        config_load = MyConfigDict.load(config_path)

        assert config == config_load


def test_config_list_in_dict():

    config = MyConfigListInDict(
        sub_sub_configs={
            "abc": [MySubSubConfig(val_float=3.0, val_list=[1, 2, 3, 4], val_str='5'),
                    MySubSubConfig(val_float=13.0, val_list=[5, 6, 7, 8], val_str='9')]})

    with tempfile.TemporaryDirectory() as d:
        config_path = pathlib.Path(str(d)) / 'tmp.yaml'

        # dump into YAML file
        config.save(config_path)

        # restore from YAML file
        config_load = MyConfigListInDict.load(config_path)

        assert config == config_load


def test_config_dict_in_list():

    config = MyConfigDictInList(
        sub_sub_configs=[
            {"abc": MySubSubConfig(val_float=3.0, val_list=[1, 2, 3, 4], val_str='5')},
            {"def": MySubSubConfig(val_float=13.0, val_list=[5, 6, 7, 8], val_str='9')}])

    with tempfile.TemporaryDirectory() as d:
        config_path = pathlib.Path(str(d)) / 'tmp.yaml'

        # dump into YAML file
        config.save(config_path)

        # restore from YAML file
        config_load = MyConfigDictInList.load(config_path)

        assert config == config_load
