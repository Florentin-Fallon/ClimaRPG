from character import Character


class Arena:
    def __init__(self):
        self._characters : list[Character] = []

    def get_characters(self) -> list[Character]:
        return self._characters

    def add(self, character: Character):
        self._characters += [character]
