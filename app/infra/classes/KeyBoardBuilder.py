from schemas.TelegramModels import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyBoardBuilder:
    """Билдер inline клавиатуры
    Реализует паттерн Builder
    """

    def __init__(self, ):
        self.inline_kb = []

    def add_inline_button(self, text: str, callback_data: str):
        """Добавить inline кнопку

        Args:
            text (str):
            callback_data (str):
        """
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        self.inline_kb.append([button])

    def get_keyboard(self):
        """Получить inline клавиатуру

        Returns:
            InlineKeyboardMarkup: inline клавиатура

        """

        kb = InlineKeyboardMarkup(inline_keyboard=self.inline_kb)
        return kb
