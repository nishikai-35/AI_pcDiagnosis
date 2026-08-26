import csv
from datetime import datetime
from pathlib import Path


# CSVの最大保存数
MAX_CSV_FILES = 10


def cleanup_old_csv_files(output_dir):
    """
    CSVレポートが最大保存数を超えた場合、
    古いファイルから削除する。
    """

    csv_files = sorted(
        output_dir.glob("diagnosis_report_*.csv"),
        key=lambda path: path.stat().st_mtime,
    )

    while len(csv_files) > MAX_CSV_FILES:
        oldest_file = csv_files.pop(0)

        try:
            oldest_file.unlink()
            print(f"古いCSVレポートを削除しました: {oldest_file}")

        except OSError as e:
            print(f"CSVレポートの削除に失敗しました: {oldest_file}")
            print(f"エラー: {e}")


def export_csv(diagnosis, output_dir="reports"):
    """
    診断結果をCSVファイルとして出力する。

    Parameters
    ----------
    diagnosis : OverallDiagnosis
        run_diagnosis() が返す総合診断結果

    output_dir : str | Path
        CSVファイルを保存するディレクトリ
    """

    # 保存先ディレクトリ
    output_dir = Path(output_dir)

    # ディレクトリが存在しない場合は作成
    output_dir.mkdir(parents=True, exist_ok=True)

    # 現在日時を取得
    now = datetime.now()

    # ファイル名を作成
    filename = (
        f"diagnosis_report_"
        f"{now.strftime('%Y%m%d_%H%M%S')}.csv"
    )

    # 最終的な保存先
    output_path = output_dir / filename

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as csvfile:

        writer = csv.writer(csvfile)

        # 総合診断
        writer.writerow(["総合評価", diagnosis.status])
        writer.writerow(["総合説明", diagnosis.message])

        # 主な原因
        writer.writerow([])
        writer.writerow(["主な原因"])

        for cause in diagnosis.causes:
            writer.writerow([cause])

        # 総合推奨対策
        writer.writerow([])
        writer.writerow(["総合推奨対策"])

        for recommendation in diagnosis.recommendations:
            writer.writerow([recommendation])

        # 個別診断
        writer.writerow([])
        writer.writerow([
            "項目",
            "判定",
            "数値",
            "説明",
            "原因",
            "推奨対策",
        ])

        for result in diagnosis.results:

            causes = " / ".join(result.causes)
            recommendations = " / ".join(result.recommendations)

            writer.writerow([
                result.item,
                result.status,
                result.value,
                result.message,
                causes,
                recommendations,
            ])

    # 古いCSVを整理
    cleanup_old_csv_files(output_dir)

    # 保存したファイルのパスを返す
    return output_path