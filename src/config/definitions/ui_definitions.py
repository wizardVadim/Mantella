from src.config.types.config_value_selection import ConfigValueSelection
from src.localization.locales import DEFAULT_LOCALE, SUPPORTED_LOCALES


class UIDefinitions:
    @staticmethod
    def get_ui_language_config_value() -> ConfigValueSelection:
        return ConfigValueSelection(
            identifier="ui_language",
            name="Interface Language",
            description="The language used by the Mantella web interface.",
            default_value=DEFAULT_LOCALE,
            options=list(SUPPORTED_LOCALES.keys()),
        )