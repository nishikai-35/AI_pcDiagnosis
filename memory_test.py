import time

blocks = []

print("メモリ負荷テスト開始")
print("停止する場合は Ctrl + C を押してください")

try:
    while True:
        blocks.append(bytearray(100 * 1024 * 1024))
        print(f"確保済み: 約{len(blocks) * 100} MB")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nメモリ負荷テスト終了")
