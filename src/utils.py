import yaml

def load_settings() -> dict:
    with open("settings.yaml", "r") as settings_file:
        settings = yaml.safe_load(settings_file)
    return settings
