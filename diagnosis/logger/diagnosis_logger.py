import json
from datetime import datetime
from pathlib import Path
from dataclasses import asdict


LOG_DIR = Path("logs/diagnosis")

# 保存するログの最大数
MAX_LOG_FILES = 10


def cleanup_old_logs():
    """
    診断ログが最大保存数を超えた場合、
    古いログから削除する。
    """

    log_files = sorted(
        LOG_DIR.glob("diagnosis_*.json"),
        key=lambda path: path.stat().st_mtime,
    )

    while len(log_files) > MAX_LOG_FILES:
        oldest_file = log_files.pop(0)

        try:
            oldest_file.unlink()
            print(f"古いログを削除しました: {oldest_file}")

        except OSError as e:
            print(f"ログ削除に失敗しました: {oldest_file}")
            print(f"エラー: {e}")


def save_diagnosis_log(results, ai_analysis=None):
    """
    DiagnosisResultの一覧をJSONログとして保存する。

    正常・注意・警告に関係なく保存する。
    保存数は最大10ファイル。
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now()

    filename = (
        f"diagnosis_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    )

    log_path = LOG_DIR / filename

    data = {
        "timestamp": timestamp.isoformat(),
        "results": [
            asdict(result)
            for result in results
        ],
    }
    
    if ai_analysis is not None:
        data["ai_analysis"] = {
            "summary": ai_analysis.summary,
            "priority": ai_analysis.priority,
            "causes": ai_analysis.causes,
            "recommendations": ai_analysis.recommendations,
        }

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )

    # 保存後に古いログを整理
    cleanup_old_logs()

    return log_path


def has_abnormal_result(results):
    """
    診断結果に「注意」または「警告」が含まれているか判定する。
    """

    return any(
        result.status in ("注意", "警告")
        for result in results
    )


def save_if_abnormal(results):
    """
    注意または警告がある場合のみログを保存する。
    """

    if not has_abnormal_result(results):
        return None

    return save_diagnosis_log(results)


def save_periodic_log(results):
    """
    定期診断用のJSONログを保存する。
    正常・注意・警告に関係なく保存する。
    """

    return save_diagnosis_log(results)