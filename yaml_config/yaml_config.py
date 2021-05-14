import pathlib
import dataclasses
import typing
import yaml
import inspect


@dataclasses.dataclass
class YamlConfig:
    def save(self, config_path: pathlib.Path):
        """ Export config as YAML file """
        assert config_path.parent.exists(), f'directory {config_path.parent} does not exist'

        def convert_dict(data):
            for key, val in data.items():
                if isinstance(val, pathlib.Path):
                    data[key] = str(val)
                if isinstance(val, dict):
                    data[key] = convert_dict(val)
            return data

        with open(config_path, 'w') as f:
            yaml.dump(convert_dict(dataclasses.asdict(self)), f)

    @classmethod
    def load(cls, config_path: pathlib.Path):
        """ Load config from YAML file """

        assert config_path.exists(), f'YAML config {config_path} does not exist'

        def _convert(child_class, val):
            if child_class == pathlib.Path:
                val = pathlib.Path(val)
            elif inspect.isclass(child_class) and issubclass(child_class, YamlConfig):
                val = child_class(**convert_from_dict(child_class, val))
            elif isinstance(child_class, typing._GenericAlias):
                if child_class.__origin__ == list:
                    val = _convert_to_list(child_class, val)
                elif child_class.__origin__ == dict:
                    val = _convert_to_dict(child_class, val)

            return val

        def _convert_to_list(parent_cls, data):
            child_class = parent_cls.__args__[0]

            return [_convert(child_class, _) for _ in data]

        def _convert_to_dict(parent_cls, data):
            child_class = parent_cls.__args__[1]

            return {k: _convert(child_class, v) for k, v in data.items()}

        def convert_from_dict(parent_cls, data):
            for key, val in data.items():
                child_class = parent_cls.__dataclass_fields__[key].type

                data[key] = _convert(child_class, val)

            return data

        with open(config_path) as f:
            config_data = yaml.full_load(f)
            # recursively convert config item to YamlConfig
            config_data = convert_from_dict(cls, config_data)
            return cls(**config_data)
