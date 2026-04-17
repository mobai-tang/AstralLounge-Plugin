# AstralLounge 鎻掍欢寮€鍙戞寚鍗?
鏈寚鍗楀皢甯姪浣犲紑鍙?AstralLounge 鐨?BaseSkill 鎻掍欢绯荤粺銆?
---

## 鐩綍

- [蹇€熷紑濮媇(#蹇€熷紑濮?
- [鎻掍欢缁撴瀯](#鎻掍欢缁撴瀯)
- [BaseSkill 鍩虹被](#baseskill-鍩虹被)
- [SkillMetadata 鍏冩暟鎹甝(#skillmetadata-鍏冩暟鎹?
- [鐢熷懡鍛ㄦ湡閽╁瓙](#鐢熷懡鍛ㄦ湡閽╁瓙)
- [鏍稿績鏂规硶](#鏍稿績鏂规硶)
- [瀹炴垬绀轰緥](#瀹炴垬绀轰緥)
- [鏈€浣冲疄璺礭(#鏈€浣冲疄璺?
- [璋冭瘯鎶€宸(#璋冭瘯鎶€宸?

---

## 蹇€熷紑濮?
### 1. 鍒涘缓鎻掍欢鏂囦欢

鍦?`backend/plugins/skills/` 鐩綍涓嬪垱寤?Python 鏂囦欢锛?
```python
# backend/plugins/skills/my_awesome_plugin.py
from backend.plugins.plugin_manager import BaseSkill, SkillMetadata

class MyAwesomePlugin(BaseSkill):
    metadata = SkillMetadata(
        name="my-awesome",
        version="1.0.0",
        description="鎴戠殑绗竴涓彃浠?,
        author="Your Name",
        triggers=["hello:", "/hello"]
    )

    async def process_input(self, text: str, context: dict):
        if text.startswith("hello:"):
            return f"浣犲ソ锛亄text[6:].strip()}"
        return text
```

### 2. 閲嶅惎鍚庣鏈嶅姟

鎻掍欢浼氬湪鏈嶅姟鍚姩鏃惰嚜鍔ㄥ姞杞姐€?
### 3. 娴嬭瘯鎻掍欢

鍦ㄨ亰澶╂杈撳叆瑙﹀彂璇嶏細
```
hello: 涓栫晫
```

---

## 鎻掍欢缁撴瀯

### 鍩虹缁撴瀯

```
backend/plugins/skills/
鈹溾攢鈹€ __init__.py           # 鍖呭垵濮嬪寲
鈹溾攢鈹€ plugin_manager.py     # 鎻掍欢绠＄悊鍣?鈹溾攢鈹€ echo.py              # 绀轰緥锛氬洖澹版彃浠?鈹溾攢鈹€ translate.py         # 绀轰緥锛氱炕璇戞彃浠?鈹斺攢鈹€ your_plugin.py       # 浣犵殑鎻掍欢
```

### 鏂囦欢妯℃澘

```python
"""
[鎻掍欢鍚嶇О] - [绠€鐭弿杩癩

璇︾粏璇存槑锛?- 鍔熻兘鎻忚堪
- 浣跨敤鏂规硶
- 渚濊禆椤癸紙濡傛灉鏈夛級
"""

from backend.plugins.plugin_manager import BaseSkill, SkillMetadata
from typing import Dict, Any, Optional
from loguru import logger


class YourPlugin(BaseSkill):
    """鎻掍欢璇存槑"""

    metadata = SkillMetadata(
        name="your-plugin",           # 鍞竴鏍囪瘑锛堣嫳鏂囷紝kebab-case锛?        version="1.0.0",              # 璇箟鐗堟湰鍙?        description="鎻掍欢鍔熻兘鎻忚堪",     # 涓枃鎻忚堪
        author="寮€鍙戣€呭悕绉?,           # 浣滆€?        triggers=["trigger:", "/cmd"], # 瑙﹀彂璇嶅垪琛?        category="tools",             # 鍒嗙被
        icon="馃敡",                    # 鍥炬爣
        config_schema={},             # 閰嶇疆 schema
        dependencies=[]               # 渚濊禆椤?    )

    def __init__(self):
        super().__init__()
        # 鍒濆鍖栦綘鐨勫睘鎬?
    async def on_load(self):
        """鎻掍欢鍔犺浇鏃惰皟鐢?""
        logger.info("鎻掍欢宸插姞杞?)

    async def on_unload(self):
        """鎻掍欢鍗歌浇鏃惰皟鐢?""
        pass

    async def process_input(self, text: str, context: Dict[str, Any]) -> str:
        """澶勭悊杈撳叆娑堟伅"""
        return text

    async def process_output(self, text: str, context: Dict[str, Any]) -> str:
        """澶勭悊杈撳嚭娑堟伅"""
        return text
```

---

## BaseSkill 鍩虹被

鎵€鏈夋彃浠跺繀椤荤户鎵?`BaseSkill` 绫伙細

```python
from backend.plugins.plugin_manager import BaseSkill
```

### 蹇呴渶灞炴€?
| 灞炴€?| 绫诲瀷 | 璇存槑 |
|------|------|------|
| `metadata` | `SkillMetadata` | 鎻掍欢鍏冩暟鎹?|

### 鍙€夊睘鎬?
| 灞炴€?| 绫诲瀷 | 璇存槑 |
|------|------|------|
| `config` | `Dict[str, Any]` | 鎻掍欢閰嶇疆 |

---

## SkillMetadata 鍏冩暟鎹?
```python
@dataclass
class SkillMetadata:
    name: str              # 鍞竴鏍囪瘑锛堝繀濉級
    version: str            # 鐗堟湰鍙凤紙蹇呭～锛?    description: str        # 鎻忚堪锛堝繀濉級
    author: str             # 浣滆€咃紙蹇呭～锛?    triggers: List[str]     # 瑙﹀彂璇嶏紙蹇呭～锛?    enabled: bool = True   # 榛樿鍚敤
    category: str = "tools" # 鍒嗙被
    icon: str = "馃敡"        # 鍥炬爣
    config_schema: Dict = {} # 閰嶇疆 schema
    dependencies: List = [] # 渚濊禆椤?```

### 鍒嗙被鍒楄〃

| ID | 鍚嶇О | 鍥炬爣 | 璇存槑 |
|----|------|------|------|
| `tools` | 瀹炵敤宸ュ叿 | 馃敡 | 閫氱敤宸ュ叿 |
| `ai` | AI 澧炲己 | 馃 | AI 鐩稿叧鍔熻兘 |
| `roleplay` | 瑙掕壊鎵紨 | 鉁?| 瑙掕壊鎵紨鐩稿叧 |
| `info` | 淇℃伅鏌ヨ | 馃摎 | 鏌ヨ绫诲姛鑳?|
| `dev` | 寮€鍙戝伐鍏?| 馃捇 | 寮€鍙戣€呭伐鍏?|
| `media` | 濯掍綋澶勭悊 | 馃帹 | 鍥剧墖/闊抽澶勭悊 |
| `system` | 绯荤粺鍔熻兘 | 鈿欙笍 | 绯荤粺闆嗘垚 |

### 閰嶇疆 Schema 绀轰緥

```python
config_schema={
    "type": "object",
    "properties": {
        "api_key": {
            "type": "string",
            "description": "API 瀵嗛挜"
        },
        "enabled": {
            "type": "boolean",
            "description": "鏄惁鍚敤",
            "default": True
        },
        "max_results": {
            "type": "integer",
            "description": "鏈€澶х粨鏋滄暟",
            "default": 10
        }
    }
}
```

---

## 鐢熷懡鍛ㄦ湡閽╁瓙

### on_load()

鎻掍欢鍔犺浇鏃惰皟鐢紝鐢ㄤ簬鍒濆鍖栬祫婧愩€?
```python
async def on_load(self):
    """鍒濆鍖?""
    self.api_key = self.config.get("api_key", "")
    self.client = AsyncClient()
    logger.info(f"{self.metadata.name} 宸插姞杞?)
```

### on_unload()

鎻掍欢鍗歌浇鏃惰皟鐢紝鐢ㄤ簬娓呯悊璧勬簮銆?
```python
async def on_unload(self):
    """娓呯悊"""
    if self.client:
        await self.client.aclose()
    logger.info(f"{self.metadata.name} 宸插嵏杞?)
```

### on_config_change(new_config)

閰嶇疆鏇存柊鏃惰皟鐢ㄣ€?
```python
async def on_config_change(self, new_config: Dict[str, Any]):
    """閰嶇疆鍙樻洿"""
    self.config = new_config
    self.api_key = new_config.get("api_key", "")
```

---

## 鏍稿績鏂规硶

### process_input(text, context)

澶勭悊鐢ㄦ埛杈撳叆锛岃繑鍥炲鐞嗗悗鐨勬枃鏈€?
**鍙傛暟锛?*
- `text: str` - 鐢ㄦ埛杈撳叆鐨勫師濮嬫枃鏈?- `context: Dict[str, Any]` - 涓婁笅鏂囦俊鎭?
**涓婁笅鏂囧瓧娈碉細**
```python
context = {
    "user_id": "鐢ㄦ埛ID",
    "session_id": "浼氳瘽ID",
    "character_id": "瑙掕壊ID",
    "platform": "骞冲彴",
    # ... 鍏朵粬鑷畾涔夊瓧娈?}
```

**绀轰緥锛?*

```python
async def process_input(self, text: str, context: Dict[str, Any]) -> str:
    """澶勭悊杈撳叆"""
    # 妫€鏌ヨЕ鍙戣瘝
    if text.startswith("translate:"):
        content = text[10:].strip()
        # 璋冪敤缈昏瘧 API
        translated = await self.translate(content)
        return translated
    # 涓嶆槸瑙﹀彂璇嶏紝涓嶅鐞?    return text
```

### process_output(text, context)

澶勭悊 AI 杈撳嚭锛岃繑鍥炲鐞嗗悗鐨勬枃鏈€?
```python
async def process_output(self, text: str, context: Dict[str, Any]) -> str:
    """澶勭悊杈撳嚭"""
    # 鍙互淇敼 AI 鐨勫洖澶?    return text
```

### on_message(text, context)

鎷︽埅娑堟伅锛岃繑鍥炲€煎喅瀹氬悗缁涓恒€?
**杩斿洖鍊硷細**
- `None` - 缁х画浼犻€掔粰涓嬩竴涓妧鑳?- `str` - 浣跨敤杩斿洖鐨勫瓧绗︿覆鏇夸唬鍘熸秷鎭?
```python
async def on_message(self, text: str, context: Dict[str, Any]) -> Optional[str]:
    """鎷︽埅娑堟伅"""
    if text == "stop":
        return "瀵硅瘽宸插仠姝?
    return None
```

---

## 瀹炴垬绀轰緥

### 绀轰緥 1锛氱畝鍗曡绠楀櫒

```python
"""
璁＄畻鍣ㄦ彃浠?- 鏀寔绠€鍗曟暟瀛﹁繍绠?"""
from backend.plugins.plugin_manager import BaseSkill, SkillMetadata
import re

class CalculatorSkill(BaseSkill):
    metadata = SkillMetadata(
        name="calculator",
        version="1.0.0",
        description="绠€鍗曡绠楀櫒锛屾敮鎸佸姞鍑忎箻闄?,
        author="AstralLounge",
        triggers=["calc:", "/calc", "璁＄畻:"],
        category="tools",
        icon="馃М"
    )

    async def process_input(self, text: str, context: dict):
        # 妫€鏌ヨЕ鍙戣瘝
        for trigger in self.metadata.triggers:
            if text.startswith(trigger):
                expression = text[len(trigger):].strip()
                try:
                    # 瀹夊叏璁＄畻锛堜粎鏀寔鍩烘湰杩愮畻锛?                    result = eval(expression, {"__builtins__": {}}, {})
                    return f"璁＄畻缁撴灉锛歿expression} = {result}"
                except Exception:
                    return "鏃犳硶璁＄畻杩欎釜琛ㄨ揪寮?
        return text
```

**浣跨敤锛?*
```
calc: 2 + 3 * 4
璁＄畻: 100 / 5
```

### 绀轰緥 2锛氬ぉ姘旀煡璇?
```python
"""
澶╂皵鏌ヨ鎻掍欢
闇€瑕侀厤缃ぉ姘?API锛堢ず渚嬩娇鐢?wttr.in锛?"""
import httpx
from backend.plugins.plugin_manager import BaseSkill, SkillMetadata

class WeatherSkill(BaseSkill):
    metadata = SkillMetadata(
        name="weather",
        version="1.0.0",
        description="鏌ヨ澶╂皵棰勬姤",
        author="AstralLounge",
        triggers=["澶╂皵:", "weather:", "/weather"],
        category="info",
        icon="馃尋锔?
    )

    async def on_load(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    async def on_unload(self):
        await self.client.aclose()

    async def process_input(self, text: str, context: dict):
        for trigger in self.metadata.triggers:
            if text.startswith(trigger):
                city = text[len(trigger):].strip() or "Beijing"
                try:
                    resp = await self.client.get(
                        f"https://wttr.in/{city}?format=j1"
                    )
                    data = resp.json()
                    current = data["current_condition"][0]
                    temp = current["temp_C"]
                    desc = current["weatherDesc"][0]["value"]
                    return f"馃尋锔?{city} 澶╂皵\n娓╁害: {temp}掳C\n{desc}"
                except Exception as e:
                    return f"鏌ヨ澶╂皵澶辫触: {e}"
        return text
```

### 绀轰緥 3锛氭彁閱掓彃浠讹紙瀹屾暣绀轰緥锛?
```python
"""
鎻愰啋鎻掍欢 - 璁剧疆鍜岀鐞嗗畾鏃舵彁閱?
浣跨敤绀轰緥:
- remind: 5鍒嗛挓鍚?寮€浼?- remind: 1灏忔椂鍚?鍚冭嵂
- reminders 鏌ョ湅鎵€鏈夋彁閱?"""
import asyncio
import re
from datetime import datetime, timedelta
from backend.plugins.plugin_manager import BaseSkill, SkillMetadata

class RemindSkill(BaseSkill):
    metadata = SkillMetadata(
        name="remind",
        version="1.0.0",
        description="瀹氭椂鎻愰啋鍔熻兘",
        author="AstralLounge",
        triggers=["remind:", "reminders", "cancel-remind"],
        category="tools",
        icon="鈴?
    )

    def __init__(self):
        super().__init__()
        self.reminders = []
        self._check_task = None

    async def on_load(self):
        self._start_checker()

    async def on_unload(self):
        if self._check_task:
            self._check_task.cancel()

    def _start_checker(self):
        async def check_loop():
            while True:
                await asyncio.sleep(30)
                # 妫€鏌ュ苟瑙﹀彂鍒版湡鐨勬彁閱?                for r in self.reminders:
                    if not r["triggered"] and r["time"] <= datetime.now():
                        r["triggered"] = True
                        print(f"鎻愰啋: {r['text']}")

        self._check_task = asyncio.create_task(check_loop())

    async def process_input(self, text: str, context: dict):
        if text.startswith("remind:"):
            # 瑙ｆ瀽骞惰缃彁閱?            pass
        elif text.startswith("reminders"):
            # 杩斿洖鎻愰啋鍒楄〃
            pass
        return text
```

### 绀轰緥 4锛氬甫閰嶇疆鐨勬彃浠?
```python
"""
缈昏瘧鎻掍欢 - 鏀寔澶氱璇█
"""
from backend.plugins.plugin_manager import BaseSkill, SkillMetadata
from typing import Dict, Any

class TranslateSkill(BaseSkill):
    metadata = SkillMetadata(
        name="translate",
        version="1.0.0",
        description="澶氳瑷€缈昏瘧",
        author="AstralLounge",
        triggers=["缈昏瘧:", "translate:"],
        category="tools",
        icon="馃寪",
        config_schema={
            "type": "object",
            "properties": {
                "default_target": {
                    "type": "string",
                    "description": "榛樿鐩爣璇█",
                    "default": "涓枃"
                },
                "api_key": {
                    "type": "string",
                    "description": "缈昏瘧 API 瀵嗛挜"
                }
            }
        }
    )

    def __init__(self):
        super().__init__()
        self.target_lang = "涓枃"

    async def on_load(self):
        self.target_lang = self.config.get("default_target", "涓枃")

    async def on_config_change(self, new_config: Dict[str, Any]):
        self.config = new_config
        self.target_lang = new_config.get("default_target", "涓枃")

    async def process_input(self, text: str, context: dict):
        if text.startswith("缈昏瘧:"):
            content = text[3:].strip()
            # 璋冪敤缈昏瘧閫昏緫
            return f"[缈昏瘧涓簕self.target_lang}]: {content}"
        return text
```

---

## 鏈€浣冲疄璺?
### 1. 閿欒澶勭悊

```python
async def process_input(self, text: str, context: dict):
    try:
        # 浣犵殑閫昏緫
        result = await self.do_something(text)
        return result
    except ValueError as e:
        logger.warning(f"鍙傛暟閿欒: {e}")
        return text  # 鍑洪敊鏃惰繑鍥炲師鏂囨湰
    except Exception as e:
        logger.error(f"澶勭悊澶辫触: {e}")
        return text
```

### 2. 寮傛鎿嶄綔

```python
async def process_input(self, text: str, context: dict):
    # 鉁?姝ｇ‘锛氫娇鐢?await
    result = await self.api_call(text)

    # 鉂?閿欒锛氫笉瑕佷娇鐢ㄩ樆濉炶皟鐢?    # time.sleep(1)
    # result = requests.get(url)

    return result
```

### 3. 閰嶇疆绠＄悊

```python
async def on_load(self):
    # 璇诲彇閰嶇疆锛屾彁渚涢粯璁ゅ€?    self.timeout = self.config.get("timeout", 30)
    self.max_retries = self.config.get("max_retries", 3)

    # 璇诲彇鐜鍙橀噺浣滀负澶囬€?    self.api_key = self.config.get("api_key") or os.getenv("MY_API_KEY", "")
```

### 4. 璧勬簮娓呯悊

```python
async def on_unload(self):
    # 鍏抽棴 HTTP 瀹㈡埛绔?    if hasattr(self, "client"):
        await self.client.aclose()

    # 鍙栨秷鍚庡彴浠诲姟
    if self._background_task:
        self._background_task.cancel()
        try:
            await self._background_task
        except asyncio.CancelledError:
            pass

    # 鍏抽棴鏂囦欢/鏁版嵁搴撹繛鎺?    if self.db:
        await self.db.close()
```

### 5. 鏃ュ織璁板綍

```python
from loguru import logger

async def process_input(self, text: str, context: dict):
    logger.debug(f"鏀跺埌璇锋眰: {text[:50]}")

    result = await self.process(text)
    logger.info(f"澶勭悊瀹屾垚锛岀粨鏋? {result[:50]}")

    return result
```

---

## 璋冭瘯鎶€宸?
### 1. 鏌ョ湅宸插姞杞界殑鎻掍欢

鎻掍欢鍔犺浇鏃朵細鍦ㄦ帶鍒跺彴鏄剧ず锛?
```
姝ｅ湪鍒濆鍖栨彃浠剁鐞嗗櫒...
  - 鍔犺浇鎶€鑳? echo v1.0.0
  - 鍔犺浇鎶€鑳? translate v1.0.0
  - 鍔犺浇鎶€鑳? remind v1.0.0
鎻掍欢绠＄悊鍣ㄥ垵濮嬪寲瀹屾垚锛屽凡鍔犺浇 3 涓妧鑳?```

### 2. 鏌ョ湅鎻掍欢鍒楄〃 API

璁块棶 `GET /api/plugins` 鍙煡鐪嬫墍鏈夋彃浠朵俊鎭€?
### 3. 鐑噸杞?
淇敼鎻掍欢鏂囦欢鍚庯紝璋冪敤 `POST /api/plugins/reload/{plugin_name}` 閲嶈浇鎻掍欢銆?
### 4. 鏌ョ湅鏃ュ織

```bash
# 瀹炴椂鏌ョ湅鏃ュ織
docker compose logs -f backend

# 鎼滅储鎻掍欢鐩稿叧鏃ュ織
docker compose logs backend | grep -i remind
```

---

## 甯歌闂

### Q: 鎻掍欢娌℃湁鍔犺浇锛?
1. 妫€鏌ユ枃浠舵槸鍚﹀湪 `backend/plugins/skills/` 鐩綍
2. 妫€鏌ョ被鍚嶆槸鍚︽纭户鎵?`BaseSkill`
3. 妫€鏌?`metadata` 鏄惁瀹氫箟
4. 鏌ョ湅鍚庣鏃ュ織

### Q: 瑙﹀彂璇嶄笉鐢熸晥锛?
1. 妫€鏌ヨЕ鍙戣瘝鏄惁瀹屽叏鍖归厤锛堝寘鎷啋鍙凤級
2. 纭繚鎻掍欢宸插惎鐢?3. 妫€鏌?`process_input` 鏂规硶鏄惁姝ｇ‘瀹炵幇

### Q: 濡備綍鑾峰彇鐢ㄦ埛淇℃伅锛?
閫氳繃 `context` 鍙傛暟锛?
```python
async def process_input(self, text: str, context: dict):
    user_id = context.get("user_id")
    session_id = context.get("session_id")
```

### Q: 濡備綍鍙戦€佹秷鎭埌鑱婂ぉ锛?
鍦?`process_input` 涓繑鍥炵殑鍐呭浼氭樉绀虹粰鐢ㄦ埛銆備綘涔熷彲浠ラ€氳繃 WebSocket 鎴?API 鍙戦€佹秷鎭€?
---

## 杩涢樁鍔熻兘

### 鑷畾涔夐厤缃?UI

鍦?`config_schema` 涓畾涔夐厤缃紝鍚庣浼氳嚜鍔ㄧ敓鎴愰厤缃晫闈€?
### 鎻掍欢甯傚満

灏嗘彃浠跺彂甯冨埌绀惧尯锛屽叾浠栫敤鎴峰彲浠ヤ竴閿畨瑁呫€?
### 鐙珛杩涚▼鎻掍欢

瀵逛簬闇€瑕佺嫭绔嬭繍琛岀殑鎻掍欢锛屽彲浠ュ垱寤?`BasePlugin` 绫诲瀷鎻掍欢锛岃繍琛屽湪鐙珛杩涚▼涓€?
---

## 鍙傝€冭祫鏂?
- [SillyTavern 鎻掍欢绯荤粺](https://docs.sillytavern.app/development/plugins/)
- [Loguru 鏃ュ織搴揮(https://loguru.readthedocs.io/)
- [Python 寮傛缂栫▼](https://docs.python.org/3/library/asyncio.html)

---

**绁濅綘寮€鍙戞剦蹇紒** 馃殌
