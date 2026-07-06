from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ForceReply,
)
from pyrogram import enums


def ikb(rows=None):
    """
    Create an InlineKeyboardMarkup from a list of lists of buttons.
    :param rows: List of lists of buttons. Defaults to empty list.
    :return: InlineKeyboardMarkup
    """
    if rows is None:
        rows = []

    lines = []
    for row in rows:
        line = []
        for button in row:
            if isinstance(button, str):
                button = btn(button, button)
            elif isinstance(button, dict):
                button = btn(**button)
            else:
                button = btn(*button)
                
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def btn(text, value, type="callback_data", style=enums.ButtonStyle.DEFAULT, icon_custom_emoji_id=None):
    """
    Create an InlineKeyboardButton.
    """
    kwargs = {
        type: value,
        "style": style,
        "icon_custom_emoji_id": icon_custom_emoji_id
    }
    return InlineKeyboardButton(text, **kwargs)


def bki(keyboard):
    lines = []
    for row in keyboard.inline_keyboard:
        line = []
        for button in row:
            button = ntb(button)
            line.append(button)
        lines.append(line)
    return lines


def ntb(button):
    for btn_type in [
        "callback_data",
        "url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
    ]:
        value = getattr(button, btn_type)
        if value:
            break
    button = [button.text, value]
    if btn_type != "callback_data":
        button.append(btn_type)
    return button


def kb(rows=None, **kwargs):
    if rows is None:
        rows = []

    lines = []
    for row in rows:
        line = []
        for button in row:
            button_type = type(button)
            if button_type == str:
                button = KeyboardButton(button)
            elif button_type == dict:
                button = KeyboardButton(**button)

            line.append(button)
        lines.append(line)
    return ReplyKeyboardMarkup(keyboard=lines, **kwargs)


kbtn = KeyboardButton

def force_reply(selective=True):
    return ForceReply(selective=selective)

def array_chunk(input_array, size):
    return [input_array[i: i + size] for i in range(0, len(input_array), size)]
