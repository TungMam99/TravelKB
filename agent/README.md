# agent/ — Sales Copilot (Spec 2)

Agent tư vấn cho đội sales Hồng Ngọc Hà. Chạy trên Travel KB (Lớp 1), tái dùng làm backend web (Spec 3).

## Chạy

```bash
# Test deterministic (KHÔNG cần API key) — pricing / lọc confidential / flight / loop+gate
.venv/bin/python -m agent.selftest

# Chạy agent live (cần ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python -m agent.cli
# Ví dụ: "Khách muốn Phú Quốc 4N3Đ, 2 người lớn, tầm trung, đi tháng 9"
```

Model mặc định `claude-sonnet-4-6` (đổi qua env `AGENT_MODEL`, vd `claude-opus-4-8` cho ca khó).

## Cấu trúc

| File | Vai trò |
|---|---|
| `pricing.py` | `quote_calc` — tính giá vốn → giá bán **deterministic** (LLM không làm toán tiền) |
| `kb.py` | Load `build/*.json` + tìm wiki; **lọc supplier confidential** khi `audience='customer'` |
| `flight.py` | `flight_search` qua fast-flights (no-API); lỗi → trả `ok=false` để agent hỏi giá tay |
| `tools.py` | 4 tool schema + dispatcher; `save_quote` có **gate** (chỉ chạy khi `approved=True`) |
| `prompts.py` | System prompt (cache prefix ổn định) |
| `conversation.py` | Manual agentic loop; **pause ở save_quote** chờ sales duyệt (human-in-the-loop) |
| `cli.py` | REPL cho sales (xử lý y/n duyệt lưu) |
| `selftest.py` | Test deterministic, chạy không cần key |

## Giao diện cho web (Spec 3)

```python
from agent.conversation import Session
s = Session()                       # cần ANTHROPIC_API_KEY
r = s.send("...")                   # {state, text, pending_save?}
if r["state"] == "awaiting_save_approval":
    r = s.approve_save(True)        # sales bấm duyệt
```
