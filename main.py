import telebot 
from config import token
from logic import Pokemon, Wizard, Fighter
from random import randint

bot = telebot.TeleBot(token) 

def get_pokemon(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        bot.reply_to(message, "Сначала создай покемона командой /go")
        return None, username
    return Pokemon.pokemons[username], username

@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        del Pokemon.pokemons[username]
    
    chance = randint(1, 10)
    if chance <= 5:
        pokemon = Pokemon(username)
    elif chance <= 8:
        pokemon = Wizard(username)
    else:
        pokemon = Fighter(username)
    
    bot.send_message(message.chat.id, pokemon.info())
    bot.send_photo(message.chat.id, pokemon.show_img())
    if pokemon.is_rare:
        bot.send_message(message.chat.id, "🌟 РЕДКИЙ ПОКЕМОН!")

@bot.message_handler(commands=['train', 'feed', 'play', 'info'])
def action(message):
    pokemon, username = get_pokemon(message)
    if not pokemon: return
    
    if message.text[1:] == 'train':
        result = pokemon.train()
    elif message.text[1:] == 'feed':
        result = pokemon.feed()
    elif message.text[1:] == 'play':
        result = pokemon.play()
    else:
        result = pokemon.info()
    
    bot.send_message(message.chat.id, result)
    if message.text[1:] != 'info':
        bot.send_message(message.chat.id, pokemon.info())

@bot.message_handler(commands=['rename'])
def rename(message):
    pokemon, username = get_pokemon(message)
    if not pokemon: return
    
    try:
        new_name = message.text.split(' ', 1)[1]
        pokemon.set_name(new_name)
        bot.send_message(message.chat.id, f"Имя изменено на {new_name}")
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    except:
        bot.reply_to(message, "Используй: /rename <новое_имя>")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if not message.reply_to_message:
        bot.send_message(message.chat.id, "Ответь на сообщение соперника")
        return
    
    attacker, _ = get_pokemon(message)
    defender = message.reply_to_message.from_user.username
    if not attacker or defender not in Pokemon.pokemons:
        bot.send_message(message.chat.id, "Нет покемонов для битвы")
        return
    
    enemy = Pokemon.pokemons[defender]
    res = attacker.attack_enemy(enemy)
    bot.send_message(message.chat.id, res)
    if enemy.hp <= 0:
        bot.send_message(message.chat.id, f"🏆 {message.from_user.username} победил!")
        del Pokemon.pokemons[defender]

@bot.message_handler(commands=['class'])
def show_class(message):
    pokemon, username = get_pokemon(message)
    if not pokemon: return
    
    if isinstance(pokemon, Wizard):
        bot.send_message(message.chat.id, "🧙‍♂️ Твой покемон - ВОЛШЕБНИК! +20 HP при кормлении, интервал 10 сек")
    elif isinstance(pokemon, Fighter):
        bot.send_message(message.chat.id, "⚔️ Твой покемон - БОЕЦ! Интервал кормления 5 секунд")
    else:
        bot.send_message(message.chat.id, "🐾 Твой покемон - ОБЫЧНЫЙ! Интервал 10 сек, +10 HP")

bot.infinity_polling(none_stop=True)