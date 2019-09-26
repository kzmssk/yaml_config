import pathlib
import dataclasses
import yaml
import inspect

yaml.add_representer(pathlib.Path, lambda dumper, instance: dumper.represent_str(str(instance)))
yaml.add_constructor(pathlib.Path, lambda loader, node: pathlib.Path(node))


@dataclasses.dataclass
class YamlConfig:
    def save(self, config_path: pathlib.Path):
        """ Export config as YAML file """
        assert config_path.parent.exists(), f'directory {config_path.parent} does not exist'
        with open(config_path, 'w') as f:
            yaml.dump(dataclasses.asdict(self), f)

    @classmethod
    def load(cls, config_path: pathlib.Path):
        """ Load config from YAML file """

        assert config_path.exists(), f'YAML config {config_path} does not exist'

        def convert_dict(parent_cls, data):
            for key, val in data.items():
                child_class = parent_cls.__dataclass_fields__[key].type
                if inspect.isclass(child_class) and issubclass(child_class, YamlConfig):
                    data[key] = child_class(**convert_dict(child_class, val))
            return data

        with open(config_path) as f:
            config_data = yaml.full_load(f)
            # recursively convert config item to YamlConfig
            config_data = convert_dict(cls, config_data)
            return cls(**config_data)