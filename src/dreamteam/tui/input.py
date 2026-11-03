"""Input helpers of the terminal UI (docs/TUI.md §4.1-4.2): suggestions for `/` commands, `@` members and
`#` tasks, parsing of what the user typed, the addressee rules, and the per-home preference and history
files. Nothing here touches the terminal or the hub."""

from __future__ import annotations

import difflib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from ..console import match_addressee, number

ALL = "all"
ALL_ALIASES = (ALL, "все", "everyone")
MAX_ROWS = 8                   # suggestion rows shown under the status line
MAX_SUGGESTIONS = 50
PREFS_FILE = "tui.json"         # <home>/.dreamteam/tui.json: {"lang": "ru"}
HISTORY_FILE = "tui_history"    # <home>/.dreamteam/tui_history (prompt_toolkit FileHistory)
EXPLICIT_ADDRESSEE_SECONDS = 60.0

_MENTION = re.compile(r"(?:^|(?<=\s))@([^@\n]{0,60})$")
_TASK_REF = re.compile(r"(?:^|(?<=\s))#(\w{0,40})$")
