import yaml
import re
import os

_env_pattern = re.compile(r".*?\${(.*?)}.*?")


def _env_constructor(loader, node):
    value = loader.construct_scalar(node)
    groups = _env_pattern.findall(value)

    # Check if the string is quoted or not
    quoted = False
    buffer = None
    try:
        lines = node.start_mark.buffer.split("\n")
        temp = ""
        for i in range(node.start_mark.line, node.end_mark.line + 1):
            temp += lines[i] + "\n"
        buffer = temp

    except (AttributeError, IndexError):
        # In case it is not a ScalerNode. I believe it always is though
        pass
    if buffer:

        value_index = buffer.index(value)
        char_before = buffer[value_index-1:value_index]
        if char_before == "'" or char_before == '"':
            after_index = value_index + len(value)
            if after_index < len(buffer):
                char_after = buffer[after_index:after_index+1]
                if char_after == char_before:
                    quoted = True

    for group in groups:
        env_var = group
        default = None
        if ":" in group:
            parts = group.split(":")
            if len(parts) != 2:
                raise Exception(f"Invalid value '{group}' in '{value}'")
            env_var = parts[0]
            default = parts[1]

        env_value = os.getenv(env_var)
        if env_value == None and default != None:
            env_value = default

        if env_value == None:
            raise Exception(f"No environment variable called '{env_var}', and no default value was specified for '{value}'")

        value = value.replace(f"${{{group}}}", env_value)

    if not quoted:
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False

        try:
            return int(value)
        except:
            pass

        try:
            return float(value)
        except:
            pass

    return value

def setup_yaml_for_env_vars():
    """
    Configures the YAML Loader to do replacement of environment variables.
    It will replace YAML value strings such as '${HOST}' and '${PORT:80}' with environment
    variable lookups.
    In the first example, '${HOST}', it will replace the string with the value from doing
    `os.getenv("HOST")`. If the environment variable 'HOST" is not set, an exception will be thrown.
    In the second example, '${PORT:80}', we are doing the same but looking up `os.getenv("PORT"). In this case,
    if the 'PORT' environment variable is not set, it will use the default value shows, which in this case is '80'.
    """
    yaml.add_implicit_resolver("!env_var", _env_pattern)
    yaml.add_constructor("!env_var", _env_constructor)

