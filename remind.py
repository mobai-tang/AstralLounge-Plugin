"""
鎻愰啋浜嬮」鎻掍欢
璁剧疆鍜岀鐞嗗畾鏃舵彁閱掞紝鏀寔鍒版湡閫氱煡

瑙﹀彂璇?
- remind: 璁剧疆鎻愰啋
- reminders: 鏌ョ湅鎵€鏈夋彁閱?- cancel-remind: 鍙栨秷鎻愰啋

浣跨敤绀轰緥:
- remind: 5鍒嗛挓 鍚庡紑浼?- remind: 1灏忔椂鍚?鍚冭嵂
- remind: 鏄庡ぉ涓婂崍9鐐?鎻愪氦鎶ュ憡
- reminders 鏌ョ湅鎵€鏈夋彁閱?- cancel-remind 1 鍙栨秷绗?涓彁閱?"""

import asyncio
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from loguru import logger

from backend.plugins.plugin_manager import BaseSkill, SkillMetadata


@dataclass
class Reminder:
    """鎻愰啋鏁版嵁"""
    id: int
    text: str
    remind_at: datetime
    created_at: datetime
    triggered: bool = False


class RemindSkill(BaseSkill):
    """鎻愰啋浜嬮」鎶€鑳?""

    metadata = SkillMetadata(
        name="remind",
        version="1.0.0",
        description="璁剧疆鍜岀鐞嗗畾鏃舵彁閱掞紝鏀寔鍒版湡閫氱煡",
        author="AstralLounge",
        triggers=["remind:", "reminders", "cancel-remind"],
        category="tools",
        icon="鈴?,
        config_schema={
            "type": "object",
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "description": "鏄惁鍚敤鎻愰啋鍔熻兘",
                    "default": True
                },
                "max_reminders": {
                    "type": "integer",
                    "description": "鏈€澶у悓鏃跺瓨鍦ㄧ殑鎻愰啋鏁伴噺",
                    "default": 20
                },
                "notify_before_minutes": {
                    "type": "integer",
                    "description": "鎻愬墠澶氬皯鍒嗛挓鎻愰啋",
                    "default": 0
                }
            }
        }
    )

    def __init__(self):
        super().__init__()
        self.reminders: List[Reminder] = []
        self.next_id = 1
        self._check_task: Optional[asyncio.Task] = None
        self._data_file: Optional[Path] = None
        self.max_reminders = 20

    async def on_load(self):
        """鍔犺浇鏃跺垵濮嬪寲"""
        self.max_reminders = self.config.get("max_reminders", 20)
        self._data_file = Path("data/reminders.json")
        await self._load_reminders()
        self._start_checker()
        logger.info("鎻愰啋鎶€鑳藉凡鍔犺浇")

    async def on_unload(self):
        """鍗歌浇鏃朵繚瀛樺苟鍋滄"""
        if self._check_task:
            self._check_task.cancel()
        await self._save_reminders()
        logger.info("鎻愰啋鎶€鑳藉凡鍗歌浇")

    async def on_config_change(self, new_config: Dict[str, Any]):
        """閰嶇疆鍙樻洿"""
        self.config = new_config
        self.max_reminders = new_config.get("max_reminders", 20)

    def _start_checker(self):
        """鍚姩瀹氭椂妫€鏌ヤ换鍔?""
        async def check_loop():
            while True:
                try:
                    await asyncio.sleep(30)  # 姣?0绉掓鏌ヤ竴娆?                    await self._check_reminders()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"妫€鏌ユ彁閱掑け璐? {e}")

        self._check_task = asyncio.create_task(check_loop())

    async def _check_reminders(self):
        """妫€鏌ュ苟瑙﹀彂鍒版湡鐨勬彁閱?""
        now = datetime.now()
        triggered_ids = []

        for reminder in self.reminders:
            if not reminder.triggered and reminder.remind_at <= now:
                reminder.triggered = True
                triggered_ids.append(reminder.id)
                logger.info(f"鎻愰啋瑙﹀彂: {reminder.text}")

        # 淇濆瓨鏇存柊鍚庣殑鐘舵€?        if triggered_ids:
            await self._save_reminders()

    async def _load_reminders(self):
        """浠庢枃浠跺姞杞芥彁閱?""
        if self._data_file and self._data_file.exists():
            try:
                data = json.loads(self._data_file.read_text(encoding="utf-8"))
                self.reminders = [
                    Reminder(
                        id=r["id"],
                        text=r["text"],
                        remind_at=datetime.fromisoformat(r["remind_at"]),
                        created_at=datetime.fromisoformat(r["created_at"]),
                        triggered=r.get("triggered", False)
                    )
                    for r in data.get("reminders", [])
                    if datetime.fromisoformat(r["remind_at"]) > datetime.now() or not r.get("triggered")
                ]
                self.next_id = data.get("next_id", 1)
                logger.info(f"宸插姞杞?{len(self.reminders)} 涓彁閱?)
            except Exception as e:
                logger.error(f"鍔犺浇鎻愰啋澶辫触: {e}")

    async def _save_reminders(self):
        """淇濆瓨鎻愰啋鍒版枃浠?""
        if self._data_file:
            self._data_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "reminders": [
                    {
                        "id": r.id,
                        "text": r.text,
                        "remind_at": r.remind_at.isoformat(),
                        "created_at": r.created_at.isoformat(),
                        "triggered": r.triggered
                    }
                    for r in self.reminders
                ],
                "next_id": self.next_id
            }
            self._data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _parse_time(self, time_str: str) -> Optional[datetime]:
        """瑙ｆ瀽鏃堕棿瀛楃涓?""
        now = datetime.now()
        time_str = time_str.strip()

        # 鍖归厤 "X鍒嗛挓/鍒嗗悗" 鎴?"X鍒嗛挓鍚?
        match = re.match(r"(\d+)\s*(鍒嗛挓|鍒?\s*(?:鍚??", time_str)
        if match:
            minutes = int(match.group(1))
            return now + timedelta(minutes=minutes)

        # 鍖归厤 "X灏忔椂鍚? 鎴?"X灏忔椂"
        match = re.match(r"(\d+)\s*(灏忔椂|鏃?\s*(?:鍚??", time_str)
        if match:
            hours = int(match.group(1))
            return now + timedelta(hours=hours)

        # 鍖归厤 "X澶╁悗" 鎴?"X澶?
        match = re.match(r"(\d+)\s*澶?, time_str)
        if match:
            days = int(match.group(1))
            return now + timedelta(days=days)

        # 鍖归厤 "鏄庡ぉ涓婂崍9鐐? 绛?        if "鏄庡ぉ" in time_str:
            tomorrow = now + timedelta(days=1)
            time_str = time_str.replace("鏄庡ぉ", "").strip()

            hour_match = re.search(r"(\d+)\s*鐐?, time_str)
            if hour_match:
                hour = int(hour_match.group(1))
                return tomorrow.replace(hour=hour, minute=0, second=0, microsecond=0)

        # 鍖归厤 "浠婂ぉ涓嬪崍3鐐?
        if "浠婂ぉ" in time_str:
            time_str = time_str.replace("浠婂ぉ", "").strip()
            hour_match = re.search(r"涓嬪崍(\d+)\s*鐐?, time_str)
            if hour_match:
                hour = int(hour_match.group(1)) + 12
                return now.replace(hour=hour, minute=0, second=0, microsecond=0)
            hour_match = re.search(r"涓婂崍(\d+)\s*鐐?, time_str)
            if hour_match:
                hour = int(hour_match.group(1))
                return now.replace(hour=hour, minute=0, second=0, microsecond=0)

        return None

    async def process_input(self, text: str, context: Dict[str, Any]) -> str:
        """澶勭悊杈撳叆"""
        text = text.strip()

        # 璁剧疆鎻愰啋
        if text.startswith("remind:"):
            return await self._handle_set_reminder(text, context)

        # 鏌ョ湅鎻愰啋鍒楄〃
        if text.startswith("reminders"):
            return self._handle_list_reminders()

        # 鍙栨秷鎻愰啋
        if text.startswith("cancel-remind"):
            return await self._handle_cancel_reminder(text)

        # 甯姪
        if "鎻愰啋" in text and ("鎬庝箞鐢? in text or "help" in text.lower()):
            return self._get_help()

        return text

    async def _handle_set_reminder(self, text: str, context: Dict[str, Any]) -> str:
        """澶勭悊璁剧疆鎻愰啋"""
        content = text[7:].strip()  # 鍘绘帀 "remind:"

        if not content:
            return "璇疯緭鍏ユ彁閱掑唴瀹癸紝渚嬪: remind: 5鍒嗛挓鍚?寮€浼?

        # 灏濊瘯鍒嗙鏃堕棿鍜屽唴瀹?        # 鏍煎紡: "5鍒嗛挓鍚?寮€浼? 鎴?"1灏忔椂鍚?鍚冭嵂"
        time_match = re.match(r"^(.+?)\s+(.+)$", content)

        if time_match:
            time_str, reminder_text = time_match.groups()
        else:
            # 灏濊瘯鎻愬彇鏃堕棿閮ㄥ垎
            time_match = re.search(r"(\d+\s*(?:鍒嗛挓|鍒唡灏忔椂|鏃秥澶?)(?:\s*鍚??", content)
            if time_match:
                time_str = time_match.group(1)
                reminder_text = content.replace(time_match.group(0), "").strip()
            else:
                return "鏃犳硶瑙ｆ瀽鏃堕棿锛岃浣跨敤浠ヤ笅鏍煎紡:\n鈥?remind: 5鍒嗛挓鍚?寮€浼歕n鈥?remind: 1灏忔椂鍚?鍚冭嵂\n鈥?remind: 鏄庡ぉ涓婂崍9鐐?鎻愪氦鎶ュ憡"

        remind_at = self._parse_time(time_str)
        if not remind_at:
            return f"鏃犳硶鐞嗚В鏃堕棿 '{time_str}'锛岃浣跨敤:\n鈥?5鍒嗛挓鍚嶾n鈥?1灏忔椂鍚嶾n鈥?鏄庡ぉ涓婂崍9鐐?

        # 妫€鏌ユ暟閲忛檺鍒?        active_reminders = [r for r in self.reminders if not r.triggered]
        if len(active_reminders) >= self.max_reminders:
            return f"鎻愰啋鏁伴噺宸茶揪涓婇檺 ({self.max_reminders}涓?锛岃鍏堝彇娑堜竴浜涙彁閱?

        # 鍒涘缓鎻愰啋
        reminder = Reminder(
            id=self.next_id,
            text=reminder_text,
            remind_at=remind_at,
            created_at=datetime.now()
        )
        self.reminders.append(reminder)
        self.next_id += 1
        await self._save_reminders()

        # 鏍煎紡鍖栨椂闂存樉绀?        time_diff = remind_at - datetime.now()
        if time_diff.total_seconds() < 60:
            time_display = "鍗冲皢鍒版湡"
        elif time_diff.total_seconds() < 3600:
            time_display = f"{int(time_diff.total_seconds() / 60)}鍒嗛挓鍚?
        elif time_diff.total_seconds() < 86400:
            time_display = f"{int(time_diff.total_seconds() / 3600)}灏忔椂鍚?
        else:
            time_display = f"{int(time_diff.total_seconds() / 86400)}澶╁悗"

        return f"鉁?鎻愰啋宸茶缃紒\n\n馃摑 {reminder_text}\n鈴?{remind_at.strftime('%Y-%m-%d %H:%M')} ({time_display})\n馃啍 缂栧彿 #{reminder.id}\n\n浣跨敤 'cancel-remind {reminder.id}' 鍙彇娑堟鎻愰啋"

    def _handle_list_reminders(self) -> str:
        """澶勭悊鍒楀嚭鎻愰啋"""
        active = [r for r in self.reminders if not r.triggered]
        completed = [r for r in self.reminders if r.triggered]

        if not active and not completed:
            return "馃搵 鏆傛棤鎻愰啋\n\n浣跨敤 'remind: 5鍒嗛挓鍚?寮€浼? 鏉ヨ缃彁閱?

        lines = ["馃搵 **鎻愰啋鍒楄〃**\n"]

        if active:
            lines.append(f"鈴?寰呮彁閱?({len(active)}涓?:\n")
            for i, r in enumerate(active, 1):
                time_diff = r.remind_at - datetime.now()
                if time_diff.total_seconds() < 60:
                    time_display = "鍗冲皢鍒版湡"
                elif time_diff.total_seconds() < 3600:
                    time_display = f"{int(time_diff.total_seconds() / 60)}鍒嗛挓鍚?
                elif time_diff.total_seconds() < 86400:
                    time_display = f"{int(time_diff.total_seconds() / 3600)}灏忔椂鍚?
                else:
                    time_display = f"{int(time_diff.total_seconds() / 86400)}澶╁悗"

                lines.append(f"  {i}. #{r.id} {r.text}")
                lines.append(f"     鈴?{r.remind_at.strftime('%H:%M')} ({time_display})\n")

        if completed:
            lines.append(f"\n鉁?鏈€杩戝畬鎴?({len(completed)}涓?:")
            for r in completed[-3:]:
                lines.append(f"  鉁?#{r.id} {r.text}")

        return "".join(lines)

    async def _handle_cancel_reminder(self, text: str) -> str:
        """澶勭悊鍙栨秷鎻愰啋"""
        parts = text.split()
        if len(parts) < 2:
            return "璇锋寚瀹氳鍙栨秷鐨勬彁閱掔紪鍙凤紝渚嬪: cancel-remind 1"

        try:
            reminder_id = int(parts[1])
        except ValueError:
            return "鏃犳晥鐨勭紪鍙凤紝璇疯緭鍏ユ暟瀛?

        for i, r in enumerate(self.reminders):
            if r.id == reminder_id:
                self.reminders.pop(i)
                await self._save_reminders()
                return f"鉁?宸插彇娑堟彁閱? {r.text}"

        return f"鏈壘鍒扮紪鍙?#{reminder_id} 鐨勬彁閱?

    def _get_help(self) -> str:
        """鑾峰彇甯姪"""
        return """鈴?**鎻愰啋鎶€鑳戒娇鐢ㄥ府鍔?*

**璁剧疆鎻愰啋:**
鈥?`remind: 5鍒嗛挓鍚?寮€浼歚
鈥?`remind: 1灏忔椂鍚?鍚冭嵂`
鈥?`remind: 鏄庡ぉ涓婂崍9鐐?鎻愪氦鎶ュ憡`
鈥?`remind: 3澶╁悗 缁垂`

**鏌ョ湅鎻愰啋:**
鈥?`reminders` - 鏌ョ湅鎵€鏈夋彁閱?
**鍙栨秷鎻愰啋:**
鈥?`cancel-remind 1` - 鍙栨秷缂栧彿涓?鐨勬彁閱?
**蹇嵎鎸囦护:**
鈥?`remind: status` - 鏌ョ湅鎻愰啋鐘舵€?""
