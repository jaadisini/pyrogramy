#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class ReplyKeyboardMarkup(Object):
    """A custom keyboard with reply options."""

    def __init__(
        self,
        keyboard: List[List[Union["types.KeyboardButton", str, tuple]]],
        is_persistent: bool = None,
        resize_keyboard: bool = None,
        one_time_keyboard: bool = None,
        selective: bool = None,
        placeholder: str = None
    ):
        super().__init__()

        self.keyboard = keyboard
        self.is_persistent = is_persistent
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        self.placeholder = placeholder

    @staticmethod
    def read(kb: "raw.base.ReplyMarkup"):
        keyboard = []

        for i in kb.rows:
            row = []
            for j in i.buttons:
                row.append(types.KeyboardButton.read(j))
            keyboard.append(row)

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            is_persistent=kb.persistent,
            resize_keyboard=kb.resize,
            one_time_keyboard=kb.single_use,
            selective=kb.selective,
            placeholder=kb.placeholder
        )

    async def write(self, _: "pyrogram.Client"):
        processed_rows = []
        
        for row in self.keyboard:
            processed_buttons = []
            for btn in row:
                # Jika formatnya tuple (text, style)
                if isinstance(btn, tuple):
                    text, style = btn[0], btn[1]
                    # Membuat objek KeyboardButton dengan parameter style custom
                    button_obj = types.KeyboardButton(text=text, style=style)
                    processed_buttons.append(button_obj.write())
                # Jika hanya string biasa
                elif isinstance(btn, str):
                    processed_buttons.append(types.KeyboardButton(btn).write())
                # Jika sudah merupakan objek KeyboardButton
                else:
                    processed_buttons.append(btn.write())
                    
            processed_rows.append(raw.types.KeyboardButtonRow(buttons=processed_buttons))

        return raw.types.ReplyKeyboardMarkup(
            rows=processed_rows,
            resize=self.resize_keyboard or None,
            single_use=self.one_time_keyboard or None,
            selective=self.selective or None,
            persistent=self.is_persistent or None,
            placeholder=self.placeholder or None
        )
