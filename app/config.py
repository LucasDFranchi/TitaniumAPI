import configparser
import os

class ConfigManager:
    def __init__(self, config_file_path: str):
        self._config = configparser.ConfigParser()
        self._config_file_path = config_file_path
        self._need_to_read = True

    def read_config(self):
        """Read the configuration from the file, if necessary."""
        if self._need_to_read:
            if os.path.exists(self._config_file_path):
                self._config.read(self._config_file_path)
                self._need_to_read = False
            else:
                raise FileNotFoundError("Configuration file not found!")

        return {
            "client_url": self._config.get("Settings", "client_url", fallback=""),
            "client_port": self._config.getint("Settings", "client_port", fallback=0)
        }
        
    def write_config(self, new_config: dict):
        """Write new configuration values to the file."""
        if "Settings" not in self._config:
            self._config["Settings"] = {}

        self._config["Settings"]["client_url"] = new_config.get("client_url", "")
        self._config["Settings"]["client_port"] = str(new_config.get("client_port", 0))
        
        with open(self._config_file_path, 'w') as config_file:
            self._config.write(config_file)
            
        self._need_to_read = True  # Mark that the config has been written and needs to be read again
