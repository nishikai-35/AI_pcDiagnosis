import configparser

from .path_utils import CONFIG_FILE


def load_config() -> configparser.ConfigParser:
    """
    config.iniを読み込んで設定オブジェクトを返す。
    """

    config = configparser.ConfigParser()

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"設定ファイルが見つかりません: {CONFIG_FILE}"
        )

    config.read(CONFIG_FILE, encoding="utf-8")

    return config


def get_int(section: str, option: str) -> int:
    """
    config.iniから整数値を取得する。
    """

    config = load_config()

    return config.getint(section, option)
