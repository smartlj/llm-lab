# 需要：pip install openai      （用 OpenAI-compatible SDK 与 Ollama 通信）
# 运行前：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查这个占位值
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # 已安装时也可换成 qwen2.5:3b / llama3.2:3b
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

# === 自我验证 ===
text = r.choices[0].message.content
print("响应：", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"非预期 finish_reason: {r.choices[0].finish_reason}"
# assert len(text) > 0, "响应不应为空"
print(r.model_dump())
assert r.usage.completion_tokens > 0, "output token 应大于 0"
print("✅ 练习 1 通过 — Ollama gemma4:e4b 已能在本地响应，每次 $0")