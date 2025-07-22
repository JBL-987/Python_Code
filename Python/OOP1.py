class Character:
    def __init__(self):
        self._type = []

class Allies(Character):
    def __init__(self):
        super().__init__()
        self._type = [
            {"name": "Chris", "power": 30, "health": 100},
            {"name": "Sona", "power": 20, "health": 80},
        ]

    def attack(self, musuh):
        target_name = input(f"{self._type[0]['name']} mau serang siapa? ")
        for m in musuh._type:
            if m["name"] == target_name:
                m["health"] -= self._type[0]["power"]
                return f"{m['name']} diserang! Sisa darah: {m['health']}"
        return "Musuh tidak ditemukan!"

class Musuh(Character):
    def __init__(self):
        super().__init__()
        self._type = [
            {"name": "Goblin", "power": 15, "health": 90},
            {"name": "Orc", "power": 25, "health": 120},
        ]

    def attack(self, teman):
        target_name = input(f"{self._type[0]['name']} mau serang siapa? ")
        for a in teman._type:
            if a["name"] == target_name:
                a["health"] -= self._type[0]["power"]
                return f"{a['name']} diserang! Sisa darah: {a['health']}"
        return "Teman tidak ditemukan!"


musuh01 = Musuh()
teman01 = Allies()
print(musuh01.attack(teman01))