import multiprocessing
import time


def load():
    while True:
        pass


if __name__ == "__main__":
    processes = []

    for _ in range(12):
        process = multiprocessing.Process(target=load)
        process.start()
        processes.append(process)

    print("CPU負荷テスト開始")
    print("停止する場合は Ctrl + C を押してください")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nCPU負荷テストを停止します")

        for process in processes:
            process.terminate()

        for process in processes:
            process.join()

        print("CPU負荷テスト終了")