# echo-translate-lite
One-way text translator agent (en→ko). JSON I/O only. Minimal junior demo.

## Quickstart
pip install -r requirements.txt
echo '{"task":"translate","text":"Hello Sonic"}' | python main.py

## Input / Output
Input: {"task":"translate","text":"<english>"}
Output: {"ok":true,"result":{"translated":"...","engine":"papago","latency_ms":123},"observations":{"src":"en","tgt":"ko"}}
See schema.json for details.

## Keys
Use env vars: PAPAGO_CLIENT_ID / PAPAGO_CLIENT_SECRET

---

## 한국어 안내
en→ko 단일 방향 텍스트 번역 에이전트 / JSON 입출력만 지원 / 주니어 제출용 최소 데모

### 빠른 실행
```bash
pip install -r requirements.txt
echo '{"task":"translate","text":"Hello Sonic"}' | python main.py
