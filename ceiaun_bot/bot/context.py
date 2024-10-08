from typing import Optional

from telegram.ext import CallbackContext, ExtBot

from bot import consts
from bot.types import FlagDict


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @property
    def bot_user_ids(self) -> set[int]:
        return self.bot_data.setdefault("user_ids", set())

    @property
    def request_list(self) -> list[list]:
        return self.bot_data.setdefault("request_list", [])

    @request_list.setter
    def request_list(self, value: list) -> None:
        self.bot_data["request_list"] = value

    @property
    def file_last_index(self) -> int:
        return self.bot_data.setdefault("file_last_index", 0)

    @file_last_index.setter
    def file_last_index(self, value: int) -> None:
        self.bot_data["file_last_index"] = value

    @property
    def summer_request_list(self) -> list[list]:
        return self.bot_data.setdefault("summer_request_list", [])

    @summer_request_list.setter
    def summer_request_list(self, value: list) -> None:
        self.bot_data["summer_request_list"] = value

    @property
    def flags(self) -> FlagDict:
        if "flags" not in self.bot_data or not self.bot_data["flags"]:
            self.bot_data["flags"] = FlagDict(
                REQUEST_OPEN=False,
                REQUEST_SUMMER_OPEN=False,
            )

        return self.bot_data["flags"]

    def set_flag(self, flag_key: str, value: bool) -> None:
        self.bot_data["flags"][flag_key] = value

    @property
    def user_state(self) -> int:
        return self.user_data.setdefault("state", consts.STATE_HOME)

    @user_state.setter
    def user_state(self, value: int) -> None:
        if value is not None:
            self.user_data["state"] = value

    @property
    def user_summer_course_status(self) -> dict[int, bool]:
        return self.user_data.setdefault("summer_course_status", {})

    @user_summer_course_status.setter
    def user_summer_course_status(self, value: dict[int, bool]) -> None:
        self.user_data["summer_course_status"] = value

    @property
    def user_last_inline_message(self) -> Optional[int]:
        return self.user_data.setdefault("last_inline_message", None)

    @user_last_inline_message.setter
    def user_last_inline_message(self, value: Optional[int]) -> None:
        self.user_data["last_inline_message"] = value
