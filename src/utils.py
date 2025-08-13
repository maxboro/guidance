import yaml

def load_settings() -> dict:
    with open("settings.yaml", "r") as settings_file:
        settings = yaml.safe_load(settings_file)
    return settings


def wrap_deg(angle: float) -> float:
    """Wrap to (-180, 180]"""
    angle = (angle + 180.0) % 360.0 - 180.0
    return 180.0 if angle == -180.0 else angle
