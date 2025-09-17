#!/usr/bin/env python3
# echo-translate lite (en -> ko, JSON I/O only)
import sys, json, time, os
import requests

PAPAGO_URL = "https://papago.apigw.ntruss.com/nmt/v1/translation"
ENGINE = "papago"
SRC = "en"
TGT = "ko"

# 사용자 제공 키(기본값). 환경변수로 덮어쓸 수 있음.
CLIENT_ID = os.getenv("PAPAGO_CLIENT_ID")  # 기본값 제거
CLIENT_SECRET = os.getenv("PAPAGO_CLIENT_SECRET")


def translate_en2ko(text: str) -> str:
    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("missing_papago_keys")
    headers = {
        "X-NCP-APIGW-API-KEY-ID": CLIENT_ID,
        "X-NCP-APIGW-API-KEY": CLIENT_SECRET,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    data = {"source": SRC, "target": TGT, "text": text}
    r = requests.post(PAPAGO_URL, headers=headers, data=data, timeout=15)
    r.raise_for_status()
    j = r.json()
    # Papago NCP 응답: message.result.translatedText
    return j["message"]["result"]["translatedText"]

def main():
    try:
        raw = sys.stdin.read().strip()
        payload = json.loads(raw) if raw else {}
        if payload.get("task", "translate") != "translate":
            raise ValueError("invalid_task")
        text = payload.get("text", "")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("empty_text")

        t0 = time.perf_counter()
        translated = translate_en2ko(text.strip())
        dt = int((time.perf_counter() - t0) * 1000)

        out = {
            "ok": True,
            "result": {"translated": translated, "engine": ENGINE, "latency_ms": dt},
            "observations": {"src": SRC, "tgt": TGT},
        }
        print(json.dumps(out, ensure_ascii=False))
    except requests.HTTPError as e:
        print(json.dumps({"ok": False, "error": "http_error", "detail": str(e)}, ensure_ascii=False))
        sys.exit(1)
    except KeyError:
        print(json.dumps({"ok": False, "error": "unexpected_response"}, ensure_ascii=False))
        sys.exit(1)
    except ValueError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"ok": False, "error": "exception", "detail": repr(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
