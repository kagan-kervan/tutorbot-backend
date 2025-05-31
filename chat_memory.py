import json, uuid, time
from typing import Optional

from dependencies import redis

HISTORY_LIMIT = 5  # son 5 mesaj çifti


async def get_session_id(session_cookie: Optional[str]) -> str:
    if session_cookie:  # varsa kullan
        return session_cookie
    sid = str(uuid.uuid4())  # yoksa üret
    await redis.hset(f"session:{sid}", mapping={"ts": time.time()})
    return sid


async def push_history(sid: str, role: str, content: str):
    await redis.lpush(f"history:{sid}", json.dumps({"role": role, "content": content}))
    await redis.ltrim(f"history:{sid}", 0, 2 * HISTORY_LIMIT - 1)  # 5 Q,5 A = 10 eleman


async def get_last_messages(sid: str):
    raw = await redis.lrange(f"history:{sid}", 0, 2 * HISTORY_LIMIT - 1)
    # En yeni başta döner, ters çevir
    return [json.loads(m) for m in reversed(raw)]
