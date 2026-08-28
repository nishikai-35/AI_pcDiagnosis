import json
import urllib.request


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma4"


prompt = """
あなたはPC診断AIです。

次の診断結果を分析してください。

CPU使用率: 5%
メモリ使用率: 47%
ディスク使用率: 27%
Windowsイベントログ: 警告あり

以下のJSONだけを返してください。

{
  "summary": "PCの状態",
  "priority": "正常",
  "causes": [
    "原因"
  ],
  "recommendations": [
    "対策"
  ]
}

JSON以外の文章は出力しないでください。
"""


data = {
    "model": OLLAMA_MODEL,
    "prompt": prompt,
    "stream": False,
}


request = urllib.request.Request(
    OLLAMA_URL,
    data=json.dumps(
        data,
        ensure_ascii=False,
    ).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
    },
    method="POST",
)


print("=" * 60)
print("Ollama JSONテスト")
print("=" * 60)

print("Ollamaへ接続します...")
print(f"モデル: {OLLAMA_MODEL}")

try:

    with urllib.request.urlopen(
        request,
        timeout=300,
    ) as response:

        response_data = json.loads(
            response.read().decode("utf-8")
        )

    print("\nAIからの回答:")
    print(response_data["response"])

    print("\n" + "=" * 60)
    print("Ollama JSONテスト成功")
    print("=" * 60)

except Exception as e:

    print("\nOllamaへの接続に失敗しました。")
    print(f"エラー: {e}")

    print("\n" + "=" * 60)
    print("Ollama JSONテスト失敗")
    print("=" * 60)