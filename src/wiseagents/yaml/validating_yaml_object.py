import json
import yaml
from jsonschema import validate

class ValidatingYAMLObject(yaml.YAMLObject):

    yaml_schema = None

    def __setstate__(self, d):
        if self.__class__.yaml_schema:
            with open(self.__class__.yaml_schema) as f:
                try:
                    schema = self.yaml_schema = json.load(f)
                finally:
                    f.close()

            validate(d, schema)
            d = self._translate_dictionary(d)

        for key, value in d.items():
            setattr(self, key, value)

    @classmethod
    def _translate_dictionary(cls, d: dict) -> dict:
        """
        Translate the dictionary by adding underscores to all the keys

        Args:
            d (dict): the parsed representation of the YAML object
        """

        copy = {}
        for key, value in d.items():
            if not key.startswith('_'):
                key = f"_{key}"
                copy[key] = value
        return copy
