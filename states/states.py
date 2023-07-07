from aiogram.filters.state import State, StatesGroup


class AskingStates(StatesGroup):
    fill_id = State()
    fill_text = State()
    confirming = State()

    @classmethod
    def get_states(cls) -> tuple[State, ...]:
        return cls.fill_id, cls.fill_text, cls.confirming
