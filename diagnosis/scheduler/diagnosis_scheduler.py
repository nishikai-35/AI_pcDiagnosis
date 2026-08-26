import argparse

from apscheduler.schedulers.blocking import BlockingScheduler
from app import run_diagnosis_process


def scheduled_diagnosis():
    print()
    print("=" * 60)
    print("定期診断を開始します")
    print("=" * 60)

    try:
        (
            info,
            memory_processes,
            cpu_processes,
            diagnosis,
            log_path,
        ) = run_diagnosis_process()

        print()
        print("=" * 60)
        print("定期診断完了")
        print("=" * 60)
        print(f"診断結果 : {diagnosis.status}")
        print(f"JSON     : {log_path}")
        print("=" * 60)

    except Exception as e:
        import traceback

        print()
        print("=" * 60)
        print("定期診断でエラーが発生しました")
        print("=" * 60)
        print(f"エラー: {e}")
        print()
        print("詳細:")
        traceback.print_exc()
        print("=" * 60)


def main(test_mode=False):
    scheduler = BlockingScheduler()

    if test_mode:
        # テスト用：1分ごと
        scheduler.add_job(
            scheduled_diagnosis,
            "interval",
            minutes=1,
        )

        schedule_message = "テストモード：1分ごとに定期診断します"

    else:
        # 本番用：毎日 09:00 / 21:00
        scheduler.add_job(
            scheduled_diagnosis,
            "cron",
            hour="9,21",
            minute=0,
        )

        schedule_message = "本番モード：毎日 09:00 と 21:00 に定期診断します"

    print("=" * 60)
    print("       AI PC Diagnosis Scheduler")
    print("=" * 60)
    print("スケジューラを起動しました")
    print(schedule_message)
    print("終了する場合は Ctrl + C")
    print("=" * 60)

    try:
        scheduler.start()

    except (KeyboardInterrupt, SystemExit):
        print()
        print("スケジューラを終了しました")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--test",
        action="store_true",
        help="テストモード：1分ごとに診断する",
    )

    args = parser.parse_args()

    main(test_mode=args.test)