# Claude API 配置：
# 之前配置过 Claude Code 中转站，可能残留 ANTHROPIC_BASE_URL。
#
# Windows PowerShell：
# Remove-Item Env:ANTHROPIC_BASE_URL
# [Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", $null, "User")
#
# Linux/macOS：
# unset ANTHROPIC_BASE_URL
# 永久配置需删除 ~/.bashrc / ~/.zshrc 中的：
# export ANTHROPIC_BASE_URL=...
#
# 验证：
# Windows: echo $env:ANTHROPIC_BASE_URL
# Linux:   echo $ANTHROPIC_BASE_URL
#
# 使用官方 Anthropic API 时不要配置第三方 BASE_URL。

# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import os
from dotenv import load_dotenv

print("BASE_URL=", os.getenv("ANTHROPIC_BASE_URL"))

import anthropic

# Anthropic 公开定价（每 1M token、USD）— 运行前查看 https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-5":    {"input": 2.00, "output": 10.00},
    "claude-opus-5":      {"input": 5.00, "output": 25.00},
    "claude-fable-5-1":   {"input": 10.00, "output": 50.00},
}
# Python 读取 .env 的工具  。注意：pycharm run configuration我已经配置paths to .env files，下面load_dotenv方法不加也没问题
load_dotenv()

client = anthropic.Anthropic(
    # 如果不加这个参数，则默认读取环境变量ANTHROPIC_API_KEY
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
MODEL = "claude-haiku-4-5"

msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "你好！请自我介绍一下。"}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

# === 自我验证 ===
assert cost_one > 0, "Cloud LLM 调用应有正成本"
print("\n✅ 练习 3 通过（Anthropic）— 已按实际 token 算出 Haiku、Sonnet、Opus 与 Fable 各 1000 次的成本")