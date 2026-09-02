from pathlib import Path
import sys


def get_app_dir() -> Path:
    """
    アプリケーションの基準ディレクトリを取得する。

    開発環境:
        AI_pcDiagnosis/

    PyInstaller:
        AI_PC_Diagnosis.exe が存在するフォルダ
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent


APP_DIR = get_app_dir()

TOOLS_DIR = APP_DIR / "tools"

REPORTS_DIR = APP_DIR / "reports"

LOGS_DIR = APP_DIR / "logs"

CONFIG_FILE = APP_DIR / "config.ini"

LHM_DIR = TOOLS_DIR / "LibreHardwareMonitor"

LHM_EXE = LHM_DIR / "LibreHardwareMonitor.exe"

SMARTCTL_DIR = TOOLS_DIR / "smartctl"

SMARTCTL_EXE = SMARTCTL_DIR / "smartctl.exe"
