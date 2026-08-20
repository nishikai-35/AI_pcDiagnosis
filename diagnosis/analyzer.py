from dataclasses import dataclass


@dataclass
class DiagnosisResult:
    item: str
    status: str
    value: float
    message: str
    causes: list[str]
    recommendations: list[str]


def get_memory_process_causes(processes, limit=3):
    causes = []

    application_processes = [
        process
        for process in processes
        if process.get("category") == "アプリケーション"
    ]

    for process in application_processes[:limit]:
        name = process["name"]
        memory_mb = process["memory_mb"]

        if memory_mb >= 500:
            causes.append(
                f"{name} が約{memory_mb:.0f}MBのメモリを使用しています"
            )

    return causes


def analyze_cpu(usage: float) -> DiagnosisResult:
    if usage >= 95:
        return DiagnosisResult(
            item="CPU",
            status="警告",
            value=usage,
            message="CPU使用率が非常に高い状態です。",
            causes=[
                "CPU負荷の高いアプリケーションが実行されている可能性があります",
                "バックグラウンド処理がCPUを大量に使用している可能性があります",
                "複数のアプリケーションが同時にCPUを使用している可能性があります",
            ],
            recommendations=[
                "タスクマネージャーでCPU使用率の高いプロセスを確認してください",
                "使用していないアプリケーションを終了してください",
                "CPU使用率が長時間高い場合は、原因となっているアプリケーションを調査してください",
            ],
        )

    if usage >= 80:
        return DiagnosisResult(
            item="CPU",
            status="注意",
            value=usage,
            message="CPU使用率が高めです。",
            causes=[
                "アプリケーションによる一時的なCPU負荷の可能性があります",
                "バックグラウンドで処理が実行されている可能性があります",
            ],
            recommendations=[
                "使用していないアプリケーションを終了してください",
                "タスクマネージャーでCPU使用率を確認してください",
            ],
        )

    return DiagnosisResult(
        item="CPU",
        status="正常",
        value=usage,
        message="CPU使用率に問題は見られません。",
        causes=[],
        recommendations=[],
    )


def analyze_memory(usage: float, processes=None) -> DiagnosisResult:
    
    if processes is None:
        processes = []
        
    process_causes = get_memory_process_causes(processes)
    
    if usage >= 90:
        causes = [
            "多数のアプリケーションが同時に実行されている可能性があります",
            "ブラウザや常駐アプリケーションが大量のメモリを使用している可能性があります",
            "搭載メモリ容量が現在の利用状況に対して不足している可能性があります",
        ]

        causes.extend(process_causes)

        return DiagnosisResult(
            item="メモリ",
            status="警告",
            value=usage,
            message="メモリ使用率が非常に高い状態です。",
            causes=causes,
            
            recommendations=[
                "使用していないアプリケーションを終了してください",
                "不要なブラウザタブを閉じてください",
                "タスクマネージャーでメモリ使用量の多いアプリケーションを確認してください",
                "頻繁に発生する場合はメモリ増設を検討してください",
            ],
        )

    if usage >= 80:
        causes = [
            "複数のアプリケーションが同時にメモリを使用している可能性があります",
            "ブラウザのタブや常駐アプリケーションがメモリを消費している可能性があります",
        ]
    
        causes.extend(process_causes)
    
        return DiagnosisResult(
            item="メモリ",
            status="注意",
            value=usage,
            message="メモリ使用率が高めです。",
            causes=causes,
        
            recommendations=[
                "使用していないアプリケーションを終了してください",
                "不要なブラウザタブを閉じてください",
                "タスクマネージャーでメモリ使用量を確認してください",
            ],
        )

    return DiagnosisResult(
        item="メモリ",
        status="正常",
        value=usage,
        message="メモリ使用率に大きな問題は見られません。",
        causes=[],
        recommendations=[],
    )


def analyze_disk(usage: float) -> DiagnosisResult:
    if usage >= 90:
        return DiagnosisResult(
            item="ディスク",
            status="警告",
            value=usage,
            message="ディスクの空き容量が非常に少なくなっています。",
            causes=[
                "大量のファイルやアプリケーションが保存されている可能性があります",
                "一時ファイルや不要なファイルが蓄積している可能性があります",
                "ディスク容量そのものが不足している可能性があります",
            ],
            recommendations=[
                "不要なファイルを削除してください",
                "ごみ箱を空にしてください",
                "不要なアプリケーションをアンインストールしてください",
                "必要に応じて大容量ファイルを別のストレージへ移動してください",
            ],
        )

    if usage >= 80:
        return DiagnosisResult(
            item="ディスク",
            status="注意",
            value=usage,
            message="ディスク使用率が高くなっています。",
            causes=[
                "不要なファイルが蓄積している可能性があります",
                "アプリケーションや動画などの大容量ファイルが増えている可能性があります",
            ],
            recommendations=[
                "不要なファイルを整理してください",
                "ごみ箱を確認してください",
                "不要なアプリケーションをアンインストールしてください",
            ],
        )

    return DiagnosisResult(
        item="ディスク",
        status="正常",
        value=usage,
        message="ディスク容量に問題は見られません。",
        causes=[],
        recommendations=[],
    )


def analyze_system(
    cpu_usage,
    memory_usage,
    disk_usage,
    memory_processes=None,
):  
    results = [
        analyze_cpu(cpu_usage),
        analyze_memory(memory_usage, memory_processes),
        analyze_disk(disk_usage),
    ]

    if any(result.status == "警告" for result in results):
        overall_status = "警告"
    elif any(result.status == "注意" for result in results):
        overall_status = "注意"
    else:
        overall_status = "正常"

    return overall_status, results