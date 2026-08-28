from ollama import chat


def main():
    print("=" * 60)
    print("Ollama ローカルAI 接続テスト")
    print("=" * 60)

    print("\nOllamaへ接続します...")

    try:
        response = chat(
            model="gemma4:latest",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "あなたはPC診断AIです。"
                        "PCのメモリ使用率が85%の場合、"
                        "考えられる原因を簡潔に説明してください。"
                    ),
                }
            ],
        )

        print("\nAIからの回答:")
        print(response.message.content)

        print("\n" + "=" * 60)
        print("Ollama 接続成功")
        print("=" * 60)

    except Exception as e:
        print("\nOllamaへの接続に失敗しました。")
        print(f"エラー: {e}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()