"""
The intent of this module is to be a collection of miscellaneous
utility functions used by the app.
"""
import sys
import yaml


def _load_yaml_file(cfgfilename: str) -> object:
    """Read in YAML data and return dictionary"""
    with open(cfgfilename, "r", encoding="utf8") as infile:
        params = yaml.safe_load(infile)
    return params


def get_device_config(devicefile: str, devicename: str) -> dict:
    """Return device configuration dictionary"""
    try:
        devices = _load_yaml_file(devicefile)
    except Exception as error:
        print(f"Error loading {devicefile}.  error={error}")
        sys.exit(1)

    if devicename not in devices:
        print(f"Device {devicename} not in {devicefile}")
        sys.exit(1)
    return devices[devicename]


def load_test_params(paramsfile: str) -> dict:
    """Return test configuration parameters"""
    try:
        params = _load_yaml_file(paramsfile)
    except Exception as error:
        print(f"Error loading {paramsfile}.  error={error}")
        sys.exit(1)
    return params
