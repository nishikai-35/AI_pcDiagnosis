from diagnosis.analyzer import analyze_system
from diagnosis.process_monitor import get_top_memory_processes
from diagnosis.system_info import get_system_info


def print_system_info(info):
    print("=" * 60)
    print("                 AI PC Diagnosis")
    print("=" * 60)

    print("\n[OS]")
    print(f"OS              : {info['os']}")
    print(f"OS Version      : {info['os_version']}")
    print(f"Machine         : {info['machine']}")

    print("\n[CPU]")
    print(f"CPU             : {info['cpu']}")
    print(f"Physical Cores  : {info['physical_cores']}")
    print(f"Logical Cores   : {info['logical_cores']}")
    print(f"CPU Usage       : {info['cpu_usage']:.1f} %")

    if info["cpu_temperature"] is not None:
        print(f"CPU Temperature : {info['cpu_temperature']:.1f} °C")
    else:
        print("CPU Temperature : 取得できません")

    print("\n[Memory]")
    print(f"Total           : {info['memory_total']:.2f} GB")
    print(f"Used            : {info['memory_used']:.2f} GB")
    print(f"Available       : {info['memory_available']:.2f} GB")
    print(f"Usage           : {info['memory_usage']:.1f} %")

    print("\n[Disk C:]")
    print(f"Total           : {info['disk_total']:.2f} GB")
    print(f"Used            : {info['disk_used']:.2f} GB")
    print(f"Free            : {info['disk_free']:.2f} GB")
    print(f"Usage           : {info['disk_usage']:.1f} %")

    print("\n[GPU]")
    if info["gpu_usage"] is not None:
        print(f"GPU Usage       : {info['gpu_usage']:.1f} %")
    else:
        print("GPU Usage       : 取得できません")

    if info["gpu_temperature"] is not None:
        print(f"GPU Temperature : {info['gpu_temperature']:.1f} °C")
    else:
        print("GPU Temperature : 取得できません")

    print("\n[System]")
    print(f"Boot Time       : {info['boot_time']}")

    print("\n" + "=" * 60)


def print_diagnosis(overall_status, results):
    print("\n" + "=" * 60)
    print("                 診断結果")
    print("=" * 60)

    print(f"\n総合評価：{overall_status}")

    for result in results:
        print(f"\n[{result.item}]")
        print(f"判定    : {result.status}")
        print(f"数値    : {result.value:.1f}")
        print(f"説明    : {result.message}")

        if result.causes:
            print("\n原因候補:")
            for cause in result.causes:
                print(f"  - {cause}")

        if result.recommendations:
            print("\n推奨対策:")
            for index, recommendation in enumerate(
                result.recommendations,
                start=1,
            ):
                print(f"  {index}. {recommendation}")

    print("\n" + "=" * 60)


def print_top_memory_processes(processes):
    print("\n" + "=" * 60)
    print("          メモリ使用量の多いプロセス")
    print("=" * 60)

    for index, process in enumerate(processes, start=1):
        print(
            f"{index}. "
            f"{process['name']} "
            f"(PID: {process['pid']}) "
            f"{process['memory_mb']:.1f} MB "
            f"[{process['category']}]"
        )


def main():
    # PC情報を取得
    info = get_system_info()

    # PC基本情報を表示
    print_system_info(info)

    # メモリ使用量の多いプロセスを取得
    processes = get_top_memory_processes(limit=10)

    # プロセス情報を表示
    print_top_memory_processes(processes)

    # PCを診断
    overall_status, results = analyze_system(
        cpu_usage=info["cpu_usage"],
        memory_usage=info["memory_usage"],
        disk_usage=info["disk_usage"],
        cpu_temperature=info["cpu_temperature"],
        gpu_usage=info["gpu_usage"],
        gpu_temperature=info["gpu_temperature"],
        memory_processes=processes,
    )

    # 診断結果を表示
    print_diagnosis(overall_status, results)


if __name__ == "__main__":
    main()