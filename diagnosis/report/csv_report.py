import csv
from datetime import datetime
from pathlib import Path


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

    # 保存したファイルのパスを返す
    return output_path