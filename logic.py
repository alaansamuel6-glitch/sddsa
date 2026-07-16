import requests
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = random.randint(1, 1000)
        self.hunger = 100
        self.happiness = 50
        self.level = 1
        self.exp = 0
        self.hp = random.randint(1,15)
        self.power = random.randint(1,15)
        self.is_rare = False
        self.last_feed_time = None
        self.get_data()
        self.check_rare()
        Pokemon.pokemons[pokemon_trainer] = self

    def get_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.img = data['sprites']['other']['official-artwork']['front_default']
            self.name = data['forms'][0]['name']
            self.height = data['height']
            self.weight = data['weight']
            self.types = [type_info['type']['name'] for type_info in data['types']]
            self.hp = data['stats'][0]['base_stat']
            self.attack_stat = data['stats'][1]['base_stat']
            self.defense = data['stats'][2]['base_stat']
            self.speed = data['stats'][5]['base_stat']
        else:
            self.img = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
            self.name = "Pikachu"
            self.height = 6
            self.weight = 60
            self.types = ["electric"]
            self.hp = 35
            self.attack_stat = 55
            self.defense = 40
            self.speed = 90

    def check_rare(self):
        if random.randint(1, 100) == 1:
            self.is_rare = True
            self.attack_stat *= 2

    def info(self):
        rare = " ⭐РЕДКИЙ!" if self.is_rare else ""
        class_name = {
            'Wizard': '🧙‍♂️ Волшебник',
            'Fighter': '⚔️ Боец'
        }.get(self.__class__.__name__, '🐾 Обычный')
        return f"Имя: {self.name}{rare}\nКласс: {class_name}\nУровень: {self.level}\nHP: {self.hp} | Атака: {self.attack_stat}\nСытость: {self.hunger}% | Счастье: {self.happiness}%"

    def show_img(self):
        return self.img
    
    def set_name(self, new_name):
        self.name = new_name
    
    def train(self):
        if self.hunger >= 20:
            self.attack_stat += 5
            self.hp += 3
            self.exp += 20
            self.hunger -= 20
            if self.exp >= 100:
                self.level += 1
                self.exp = 0
                self.hp += 10
                self.attack_stat += 5
            return "Тренировка прошла успешно!"
        return "Покемон слишком голоден для тренировки! Покорми его!"
    
    def feed(self):
        current_time = datetime.now()
        
        if isinstance(self, Fighter):
            interval = 5
            name = "Боец"
            hp_boost = 10
        elif isinstance(self, Wizard):
            interval = 10
            name = "Волшебник"
            hp_boost = 20
        else:
            interval = 10
            name = "Покемон"
            hp_boost = 10
        
        if self.last_feed_time:
            time_diff = (current_time - self.last_feed_time).total_seconds()
            if time_diff < interval:
                wait_time = int(interval - time_diff)
                return f"{name} сыт! Следующее кормление через {wait_time} секунд"
        
        self.last_feed_time = current_time
        self.hp += hp_boost
        self.hunger = min(100, self.hunger + 30)
        self.happiness += 10
        return f"{name} покормлен! HP +{hp_boost}"

    def play(self):
        self.happiness = min(100, self.happiness + 20)
        self.hunger -= 5
        return "Поиграли! Счастье +20, сытость -5"

    def attack_enemy(self, enemy):
        if isinstance(enemy, Wizard) and random.randint(1,5) == 1:
            return "Покемон-волшебник применил щит в сражении"
        
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        enemy.hp = 0
        return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
    def attack_enemy(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = super().attack_enemy(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой: {super_power}"