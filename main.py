import discord
from discord.ext import commands
import random
import easydata2 as ed
from pathlib import Path
from localcd import cooldown_check, cooldown_set

DB_NAME = 'philin_data'
db_path = Path(f'{DB_NAME}.json')
if not db_path.exists():
    print('Файл базы данных не обнаружен!')
    ed.create_database(DB_NAME)

CONFIG_NAME = 'config'
db_path = Path(f'{CONFIG_NAME}.json')
if not db_path.exists():
    print('Файл конфига не обнаружен!')
    ed.create_database(CONFIG_NAME)
    ed.give_id_data(CONFIG_NAME, 'config', {'prefix': '>', 'balance': 0, 'inc_balance': 500, 'currency': '$', 'bank_balance': 0, 'bank_limit': 200, 'inc_ad': 1, 'inc_building': 1, 'skill_hack': 1, 'skill_protect': 1, 'business_price': 1000, 'ad_price': 250, 'building_price': 1000, 'inc_stocks': 0, 'inc_workers': '0', 'inc_max_stocks': 20, 'inc_stock_percent': 2})

config = ed.get_id_data(CONFIG_NAME, 'config')

messages = 0

client = commands.Bot(command_prefix=config['prefix'])

@client.event
async def on_ready():
    print('Выполнен вход в {0.user}'.format(client))
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(name=f'>help', type= discord.ActivityType.playing))

@client.command()
async def bal(message):
    user_id = str(message.author.id)
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_balance'):
        bank_balance = ed.give_item_data(DB_NAME, user_id, 'bank_balance', config['bank_balance'])
    bank_balance = ed.get_item_data(DB_NAME, user_id, 'bank_balance')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_limit'):
        bank_limit = ed.give_item_data(DB_NAME, user_id, 'bank_limit', config['bank_limit'])
    bank_limit = ed.get_item_data(DB_NAME, user_id, 'bank_limit')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'work'):
        work = ed.give_item_data(DB_NAME, user_id, 'work', 'Отсутствует')
    work = ed.get_item_data(DB_NAME, user_id, 'work')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')
    
    if business != 'Отсутствует':
        work = '**Бизнес**'
    
    embed1 = discord.Embed(
    title = 'Ваш баланс',
    description = f'💸 Наличка: {currency}**{balance}**\n💳 Банк: {currency}**{bank_balance}**\n💰 Лимит: {currency}**{bank_limit}**\n🔧 Работа: {work}',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def bonus(message):
    
    user_id = str(message.author.id)

    if cooldown_check(user_id, 'bonus', 43200) != True:
        wait = cooldown_check(user_id, 'bonus', 43200)
        embed2 = discord.Embed(
        title = '<a:no:998468646533869658> Пожалуйста, подождите',
        description = f'Осталось ждать: {wait} секунд',
        color = 0xffff00)
        await message.channel.send(embed = embed2)
        
        return

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    payment = random.randint(1, 400)
    new_balance = int(balance) + payment
    
    ed.give_item_data(DB_NAME, user_id, 'balance', new_balance)
    
    cooldown_set(user_id, 'bonus')

    embed1 = discord.Embed(
    title = 'Ежедневная выплата',
    description = f'📬 Оплата: {currency}**{payment}**\n💸 Итоговый баланс: {currency}**{new_balance}**',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def pay(message, *, content):
    user_id = str(message.author.id)

    content_split = content.split()
    another_id = content_split[0].replace('<', '').replace('@', '').replace('>', '')
    count = content_split[1]

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, another_id, 'balance'):
        another_balance = ed.give_item_data(DB_NAME, another_id, 'balance', config['balance'])
    another_balance = ed.get_item_data(DB_NAME, another_id, 'balance')

    count = str(int(count) / 100 * 95).split('.')[0]

    sub = int(balance) - int(count)
    sum = int(another_balance) + int(count)
    sum = int(str(sum).split('.')[0])

    if sub and sum and int(balance) >= int(count) and int(count) >= 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        ed.give_item_data(DB_NAME, another_id, 'balance', sum)
        text = f'<a:yes:998468643627212860> **Успешная транзакция!**\n📤 Отправитель: <@{user_id}>\n📥 Получатель: <@{another_id}>\n💸 Сумма: {currency}**{count}**\n📄 Комиссия: **5**%'
    elif int(balance) < int(count):
        text = f'<a:no:998468646533869658> Нехватка средств!\nУ вас на балансе: {currency}*{balance}*'
    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\n**Возможные причины:**\n- Отсутствуют данные\n- Данное число не доступно'

    embed1 = discord.Embed(
    title = 'Перевод средств',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def deposit(message, *, content):
    user_id = str(message.author.id)
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_balance'):
        bank_balance = ed.give_item_data(DB_NAME, user_id, 'bank_balance', config['bank_balance'])
    bank_balance = ed.get_item_data(DB_NAME, user_id, 'bank_balance')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_limit'):
        bank_limit = ed.give_item_data(DB_NAME, user_id, 'bank_limit', config['bank_limit'])
    bank_limit = ed.get_item_data(DB_NAME, user_id, 'bank_limit')

    if content == 'all':
        content = balance
        
    payment = str(int(content) / 100 * 90).split('.')[0]

    sub = int(balance) - int(content)
    sum = int(bank_balance) + int(payment)
    sum = int(str(sum).split('.')[0])


    if int(balance) >= int(content) and int(bank_balance) + int(content) <= int(bank_limit) and int(content) > 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        ed.give_item_data(DB_NAME, user_id, 'bank_balance', sum)
        text = f'<a:yes:998468643627212860> **Успешное пополнение!**\n📤 Отправитель: <@{user_id}>\n📥 Получатель: **Philin Bank**\n💸 Сумма: {currency}**{payment}**\n📄 Комиссия: **10**%'
    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\n**Возможные причины:**\n- Не хватка средств (Доступно: {currency}**{balance}**)\n- Данная сумма превысит лимит ({currency}**{bank_limit}**)\n- Данное число не доступно'

    embed1 = discord.Embed(
    title = 'Перевод средств',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def withdraw(message, *, content):
    user_id = str(message.author.id)
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_balance'):
        bank_balance = ed.give_item_data(DB_NAME, user_id, 'bank_balance', config['bank_balance'])
    bank_balance = ed.get_item_data(DB_NAME, user_id, 'bank_balance')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_limit'):
        bank_limit = ed.give_item_data(DB_NAME, user_id, 'bank_limit', config['bank_limit'])
    bank_limit = ed.get_item_data(DB_NAME, user_id, 'bank_limit')

    if content == 'all':
        content = balance

    sub = int(bank_balance) - int(content)
    sum = int(balance) + int(content)
    sum = int(str(sum).split('.')[0])


    if int(bank_balance) >= int(content) and int(content) >= 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sum)
        ed.give_item_data(DB_NAME, user_id, 'bank_balance', sub)
        text = f'<a:yes:998468643627212860> **Успешное снятие!**\n📤 Отправитель: **Philin Bank**\n📥 Получатель: <@{user_id}>\n💸 Сумма: {currency}**{content}**\n📄 Комиссия: **0**%'
    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\n**Возможные причины:**\n- Не хватка средств (Доступно: {currency}**{bank_balance}**)\n- Данное число не доступно'

    embed1 = discord.Embed(
    title = 'Перевод средств',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def hack(message, *, content):
    user_id = str(message.author.id)

    content_split = content.split()
    another_id = content_split[0].replace('<', '').replace('@', '').replace('>', '')


    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, another_id, 'balance'):
        another_balance = ed.give_item_data(DB_NAME, another_id, 'balance', config['balance'])
    another_balance = ed.get_item_data(DB_NAME, another_id, 'balance')

    if not ed.is_item_exist(DB_NAME, another_id, 'skill_protect'):
        skill_protect = ed.give_item_data(DB_NAME, another_id, 'skill_protect', config['skill_protect'])
    skill_protect = ed.get_item_data(DB_NAME, another_id, 'skill_protect')

    if not ed.is_item_exist(DB_NAME, user_id, 'skill_hack'):
        skill_hack = ed.give_item_data(DB_NAME, user_id, 'skill_hack', config['skill_hack'])
    skill_hack = ed.get_item_data(DB_NAME, user_id, 'skill_hack')

    chance = random.randint(1, 100)

    if int(skill_protect) >= int(skill_hack):
        procent = 100 / (int(skill_protect) / int(skill_hack) + 1)
        procent = int(str(procent).split('.')[0])
    elif int(skill_protect) < int(skill_hack):
        procent = 100 - (100 / (int(skill_hack) / int(skill_protect) + 1))
        procent = int(str(procent).split('.')[0])
    
    
    if chance <= procent:
        count = int(another_balance) // 2
        
        sum = int(balance) + count
        sub = int(another_balance) - count
        
        ed.give_item_data(DB_NAME, another_id, 'balance', sub)
        ed.give_item_data(DB_NAME, user_id, 'balance', sum)
        text = f'<a:yes:998468643627212860> **Успешное ограбление!**\n📤 Жертва: <@{another_id}>\n📥 Грабитель: <@{user_id}>\n💸  Сумма: {currency}**{count}**\n📄 Шанс: **{procent}**%'
    else:
        count = int(balance) // 2
        sub = int(balance) - count
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        text = f'<a:no:998468646533869658> Ограбление не удалось!\n⚖️ Штраф: {currency}**{count}**\n📄 Шанс: **{procent}**%'

    embed1 = discord.Embed(
    title = 'Ограбление',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def set_work(message, *, content): #обновить
    id_user = str(message.author.id)

    work = getData(WORK_FILE, id_user) or 'None'
    business = getData(BUSINESS_NAME_FILE, id_user) or 'None'
    workers = getData(BUSINESS_WORKERS_FILE, content.replace(' ', '_'))
    print(f'-------------------------------------------------------------------------------------------{workers}')
    businesses = readData(BUSINESS_NAME_FILE)

    if work == 'None' and content.replace(' ', '_') + ' Inc.' in businesses and content != '_leave_' and business == 'None': #если нет в базе данных
        addData(WORK_FILE, id_user, content.replace(' ', '_')) #добавляем
        text = 'Вы успешно устроились на работу в компанию **' + content + ' Inc.**'
        if workers:
            updateData(BUSINESS_WORKERS_FILE, content.replace(' ', '_'), int(workers) + 1)

    elif work == 'Free' and content.replace(' ', '_') + ' Inc.' in businesses and content != '_leave_' and business == 'None': #если есть в базе данных, но без работы
        updateData(WORK_FILE, id_user, content.replace(' ', '_')) #обновляем
        text = 'Вы успешно устроились на работу в компанию **' + content + ' Inc.**'
        if workers:
            updateData(BUSINESS_WORKERS_FILE, content.replace(' ', '_'), int(workers) + 1) #добавляем единицу
        
    elif work != 'None' and work != 'Free' and content == '_leave_' and business == 'None':
        work = getData(WORK_FILE, id_user)
        workers = getData(BUSINESS_WORKERS_FILE, work)
        updateData(WORK_FILE, id_user, 'Free') #обновляем
        text = 'Вы успешно уволились из компании **' + work.replace('_', ' ') + ' Inc.**'
        updateData(BUSINESS_WORKERS_FILE, work, int(workers) - 1) #добавляем единицу

    else:
        text = f'<:error:1001754203565326346> Ошибка взаимодействия\nВозможные причины:\n- Данного бизнеса/параметра не существует\n- Вы уже где то работаете\n- У вас есть свой бизнес'

    embed1 = discord.Embed(
    title = 'Работа',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def skill_up(message, *, content):

    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if not ed.is_item_exist(DB_NAME, user_id, 'skill_hack'):
        skill_hack = ed.give_item_data(DB_NAME, user_id, 'skill_hack', config['skill_hack'])
    skill_hack = ed.get_item_data(DB_NAME, user_id, 'skill_hack')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'skill_protect'):
        skill_protect = ed.give_item_data(DB_NAME, user_id, 'skill_protect', config['skill_protect'])
    skill_protect = ed.get_item_data(DB_NAME, user_id, 'skill_protect')
    text = '<:error:1001754203565326346> Проверьте написание команды!'

    if content == 'hack':
        hack_price = int(skill_hack) * 50
        if int(balance) >= hack_price:

            skill_hack = int(skill_hack) + 1
            sub = int(balance) - hack_price

            ed.give_item_data(DB_NAME, user_id, 'balance', sub)
            
            ed.give_item_data(DB_NAME, user_id, 'balance', skill_hack)
                
            text = f'🗡Вы успешно повысили навык взлома за {currency}**{hack_price}**\nВаш новый уровень: **{skill_hack}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸Нужная сумма: {currency}**{hack_price}**'

    if content == 'protect':
        protect_price = int(skill_protect) * 100
        if int(balance) >= protect_price:

            skill_protect = int(skill_protect) + 1
            sub = int(balance) - protect_price

            ed.give_item_data(DB_NAME, user_id, 'balance', sub)
            
            ed.give_item_data(DB_NAME, user_id, 'balance', skill_hack)
            
            text = f'🔒Вы успешно повысили защиту от взлома за {currency}**{protect_price}**\nВаш новый уровень: **{skill_protect}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸Нужная сумма: {currency}**{protect_price}**'

    embed1 = discord.Embed(
    title = 'Улучшение',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_create(message, *, content):

    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    business_price = int(config['business_price'])

    if int(balance) >= business_price and not ed.is_id_exist(DB_NAME, content) and content != None and business == 'Отсутствует':
        sub = int(balance) - business_price

        inc_name = ed.give_item_data(DB_NAME, user_id, 'business', content)
        inc_ad = ed.give_item_data(DB_NAME, content, 'ad', config['inc_ad'])
        inc_building = ed.give_item_data(DB_NAME, content, 'building', config['inc_building'])
        inc_grafic = ed.give_item_data(DB_NAME, content, 'grafic', '🔺')
        inc_balance = ed.give_item_data(DB_NAME, content, 'balance', config['inc_balance'])
        inc_workers = ed.give_item_data(DB_NAME, content, 'workers', config['inc_workers'])
        inc_stocks = ed.give_item_data(DB_NAME, content, 'stocks', config['inc_stocks'])
        inc_max_stocks = ed.give_item_data(DB_NAME, content, 'max_stocks', config['inc_max_stocks'])
        inc_stock_percent = ed.give_item_data(DB_NAME, content, 'stock_percent', config['inc_stock_percent'])

        stock_price = ed.give_item_data(DB_NAME, content, 'stock_price', int(str(int(inc_balance) / 100 * 2).split('.')[0]))

        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        text = f'<a:yes:998468643627212860> **Успешно создан бизнес**: **{content} Inc.**\n💸 С вашего баланса списано {currency}**{business_price}**'

    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Нехватка средств ({currency}**{business_price}**)\n- Отсутствует название\n- У вас уже есть бизнес\n- Бизнес с таким названием уже существует\n- Данное наименование запрещено'
        
    embed1 = discord.Embed(
    title = 'Предприятие',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_up(message, *, content):

    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    text = text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Непредусмотренный параметр\n- Отсутствие бизнеса'

    if content == 'ad' and business != 'Отсутствует':
        ad_price = int(ed.get_item_data(DB_NAME, business, 'ad')) * 150
        if int(balance) >= ad_price:
            
            sub = int(balance) - ad_price
            
            ed.give_item_data(DB_NAME, user_id, 'balance', sub)
            ed.give_item_data(DB_NAME, business, 'ad', int(ed.get_item_data(DB_NAME, business, 'ad')) + 1)
                
            text = f'📈 Вы успешно повысили уровень распространенности своей компании за {currency}**{ad_price}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸Нужная сумма: {currency}**{ad_price}**'

    if content == 'building' and business != 'Отсутствует':
        building_price = int(ed.get_item_data(DB_NAME, business, 'building')) * 1000
        if int(balance) >= building_price:

            sub = int(balance) - building_price
            
            ed.give_item_data(DB_NAME, user_id, 'balance', sub)

            ed.give_item_data(DB_NAME, business, 'building', int(ed.get_item_data(DB_NAME, business, 'building')) + 1)
                
            text = f'📈 Вы успешно повысили уровень распространенности своей компании за {currency}**{building_price}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸 Нужная сумма: {currency}**{building_price}**'

    embed1 = discord.Embed(
    title = 'Улучшение',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_info(message): 
    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    text = '<a:no:998468646533869658> У вас отсутствует бизнес!'

    if business != 'Отсутствует':
        inc_ad = ed.get_item_data(DB_NAME, business, 'ad')
        inc_building = ed.get_item_data(DB_NAME, business, 'building')
        inc_grafic = ed.get_item_data(DB_NAME, business, 'grafic')
        inc_balance = ed.get_item_data(DB_NAME, business, 'balance')
        inc_workers = ed.get_item_data(DB_NAME, business, 'workers')
        inc_stocks = ed.get_item_data(DB_NAME, business, 'stocks')
        inc_max_stocks = ed.get_item_data(DB_NAME, business, 'max_stocks')
        inc_stock_percent = ed.get_item_data(DB_NAME, business, 'stock_percent')

        stock_price = int(str(int(inc_balance) / 100 * 2).split('.')[0])

        text = f'📌Название: **{business}**\n📨Уровень рекламы: **{inc_ad}**\n🏢Количество зданий: **{inc_building}**\n💸Бюджет: {currency}**{inc_balance}**\n📊Цена акции: {currency}**{stock_price}**{inc_grafic}\n🧷Процент акции: **{inc_stock_percent}%**\n📈Продано акций: **{inc_stocks}/{inc_max_stocks}**\n👤Сотрудников: {inc_workers}'
    
    embed1 = discord.Embed(
    title = 'Предприятие',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def badge(message):
    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'badges'):
        badges = ed.give_item_data(DB_NAME, user_id, 'badges', 'Отсутствуют')
    badges = ed.get_item_data(DB_NAME, user_id, 'badges')
    
    embed1 = discord.Embed(
    title = 'Инвентарь',
    description = f'🗃 Ваши значки: {badges}',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def set_currency(message, *, content):
    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'badges'):
        badges = ed.give_item_data(DB_NAME, user_id, 'badges', 'Отсутствуют')
    badges = ed.get_item_data(DB_NAME, user_id, 'badges')

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if badges != 'Отсутствуют':
        badges_split = badges.split()
        badges_count = len(badges_split)

    num = int(content) - 1

    if badges != '**Отсутствуют**' and num <= badges_count:
        ed.give_item_data(DB_NAME, user_id, 'currency', badges_split[num])
        
        text = f'<a:yes:998468643627212860> **Успешно изменена иконка!**\nНовая иконка: {badges_split[num]}'
    else:
        text = f'<a:no:998468646533869658> У вас нет значка с таким номером'

    embed1 = discord.Embed(
    title = 'Кастомизация',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def id(message, *, content):
    embed1 = discord.Embed(
    title = 'Поиск айди',
    description = f'Эмодзи: {content}\nАйди: ```{content}```',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_withdraw(message, *, content):
    user_id = str(message.author.id)

    count = int(content)

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')

    if not ed.is_item_exist(DB_NAME, business, 'inc_balance'):
        inc_balance = ed.give_item_data(DB_NAME, business, 'business', config['inc_balance'])
    inc_balance = ed.get_item_data(DB_NAME, business, 'business')

    sum = int(balance) + count
    sub = int(inc_balance) - count

    text = '<a:no:998468646533869658> У вас отсутствует бизнес!'
    if business != 'Отсутствует' and count > 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sum)
        ed.give_item_data(DB_NAME, business, 'balance', sub)
        ed.give_item_data(DB_NAME, business, 'grafic','🔻')
        text = f'<a:yes:998468643627212860> **Успешная транзакция!**\n📤Отправитель: {business}\n📥Получатель: <@{user_id}>\n💸Сумма: {currency}**{count}**\n📄Комиссия: **0**%'
    elif int(content) > 0:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- У вас нет бизнеса\n- Снятие данной суммы невозможно'
    
    embed1 = discord.Embed(
    title = 'Предприятие',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_store(message, *, content = 'None'): #обновить
    user_id = str(message.author.id)

    content_split = content.split()
    text = ''

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'inventory'):
        inventory = ed.give_item_data(DB_NAME, user_id, 'inventory', {})
    inventory = ed.get_item_data(DB_NAME, user_id, 'inventory')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Данного параметра не существует\n- Данного бизнеса не существует\n- Данное число не доступно\n- Нехватка средств'
    
    if content_split == ['None']:
        
        text = ''
    
        ids = ed.ids(DB_NAME)
        
        for id in ids:
            if ed.is_item_exist(DB_NAME, id, 'grafic'):
                inc_balance = ed.get_item_data(DB_NAME, id, 'balance')
                inc_grafic = ed.get_item_data(DB_NAME, id, 'grafic')
                stock_price = ed.give_item_data(DB_NAME, id, 'stock_price', int(str(int(inc_balance) / 100 * 2).split('.')[0]))

                text = text + f'{id}: {currency}**{stock_price}** {inc_grafic}'
                
    elif content_split[0] == 'buy':

        if ed.is_item_exist(DB_NAME, content_split[1], 'grafic'):

            price = int(ed.get_item_data(DB_NAME, content_split[1], 'stock_price')) * int(content_split[2].split('.')[0])
            
            if int(content_split[2]) <= int(ed.get_item_data(DB_NAME, content_split[1], 'max_stocks')) - int(ed.get_item_data(DB_NAME, content_split[1], 'stocks')) and int(content_split[2]) > 0 and balance >= price:
                
                if cooldown_check(user_id, f'inc_store buy {content_split[1]}', 172800) != True:
                    wait = cooldown_check(user_id, f'inc_store buy {content_split[1]}', 172800)
                    embed2 = discord.Embed(
                    title = '<a:no:998468646533869658> Пожалуйста, подождите',
                    description = f'Осталось ждать: {wait} секунд',
                    color = 0xffff00)
                    await message.channel.send(embed = embed2)
        
                    return
                price = int(ed.get_item_data(DB_NAME, content_split[1], 'stock_price')) * int(content_split[2].split('.')[0])
            
                inc_balance = ed.get_item_data(DB_NAME, content_split[1], 'balance')
                inc_stocks =  ed.get_item_data(DB_NAME, content_split[1], 'stocks')
                
                sum = int(inc_balance) + price
                sub = int(balance) - price
                
                ed.give_item_data(DB_NAME, content_split[1], 'balance', sum)
                ed.give_item_data(DB_NAME, user_id, 'balance', sub)
                
                inventory[content_split[1]] = inventory.get(content_split[1], 0) + int(content_split[2])
                
                ed.give_item_data(DB_NAME, user_id, 'inventory', inventory)
                
                sum = int(content_split[2]) + int(ed.get_item_data(DB_NAME, content_split[1], 'stocks'))
                
                ed.give_item_data(DB_NAME, content_split[1], 'stocks', sum)
                ed.give_item_data(DB_NAME, content_split[1], 'grafic', '🔺')
                
                cooldown_set(user_id, f'inc_store sell {content_split[1]}')
                
                text = f'<a:yes:998468643627212860> **Успешная покупка** {content_split[2]} акций компании {content_split[1]} за {currency}**{price}**'
                
    elif content_split[0] == 'sell':
        
        if ed.is_item_exist(DB_NAME, content_split[1], 'grafic'):

            if int(content_split[2]) <= int(ed.get_item_data(DB_NAME, user_id, 'inventory')[content_split[1]]) and int(content_split[2]) > 0:
                
                if cooldown_check(user_id, f'inc_store sell {content_split[1]}', 172800) != True:
                    wait = cooldown_check(user_id, f'inc_store sell {content_split[1]}', 172800)
                    embed2 = discord.Embed(
                    title = '<a:no:998468646533869658> Пожалуйста, подождите',
                    description = f'Осталось ждать: {wait} секунд',
                    color = 0xffff00)
                    await message.channel.send(embed = embed2)
        
                    return
                
                price = int(ed.get_item_data(DB_NAME, content_split[1], 'stock_price')) * int(content_split[2].split('.')[0])
            
                inc_balance = ed.get_item_data(DB_NAME, content_split[1], 'balance')
                inc_stocks =  ed.get_item_data(DB_NAME, content_split[1], 'stocks')
                
                sum = int(balance) + price
                sub = int(inc_balance) - price
                
                ed.give_item_data(DB_NAME, content_split[1], 'balance', sub)
                ed.give_item_data(DB_NAME, user_id, 'balance', sum)
                
                inventory[content_split[1]] = inventory.get(content_split[1], 0) - int(content_split[2])
                
                ed.give_item_data(DB_NAME, user_id, 'inventory', inventory)
                
                sub = int(ed.get_item_data(DB_NAME, content_split[1], 'stocks')) - int(content_split[2])
                
                ed.give_item_data(DB_NAME, content_split[1], 'stocks', sub)
                ed.give_item_data(DB_NAME, content_split[1], 'grafic', '🔻')
                
                cooldown_set(user_id, f'inc_store buy {content_split[1]}')
                
                text = f'<a:yes:998468643627212860> **Успешная продажа** {content_split[2]} акций компании {content_split[1]} за {currency}**{price}**'
        
    
    embed1 = discord.Embed(
    title = 'Рынок акций',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_stocks(message, *, content): #обновить
    id_user = str(message.author.id)

    print(f'------------------------{id_user}: >inc_stocks {content}')

    cur = getData(CURRENCY_FILE, id_user) or '$'
    if not cur: #проверяем наличие в базе данных, если нет - добавляем (сервер)
        addData(CURRENCY_FILE, id_user, STARTING_CURRENCY)

    balance = getData(BALANCE_FILE, id_user) or 0
    if not balance: #проверяем наличие в базе данных, если нет - добавляем
        addData(BALANCE_FILE, id_user, STARTING_BALANCE)

    name = content + ' Inc.'

    money = int(getData(BUSINESS_MONEY_FILE, name))

    stocksData = findDataMulti(INV_FILE, id_user, content) or '0 0'
    stocksCount = int(stocksData.split()[0])

    price = money / 200
    price = int(str(price).split('.')[0])
    price = price * stocksCount

    sum = int(balance) + price
    sub = money - price

    updateData(BALANCE_FILE, id_user, sum ) #обновляем значение в базе
    updateData(BUSINESS_MONEY_FILE, name, sub ) #обновляем значение в базе
    updateData(BUSINESS_GRAF_FILE, name.replace(' Inc.', ''), '🔻')
    text = f'**Успешная транзакция!**\n📤Отправитель: {name}\n📥Получатель: <@{id_user}>\n💸Сумма: {cur}**{price}**\n📄Комиссия: **0**%'
    
    embed1 = discord.Embed(
    title = 'Предприятие',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_inv(message): #обновить
    id_user = str(message.author.id)

    print(f'------------------------{id_user}: >inc_inv')
    inv = getData(INV_FILE, id_user).replace(';', '\n')
    inv_split = inv.split('\n')
    newText = ''
    for x in inv_split:
        if x != '':
            x_split = x.split()
            newData = x_split[0] + ' - ' + x_split[1].replace('_', ' ') + ' Inc.'
            if newText == '':
                newText = newData
            else:
                newText = newText + '\n' + newData
    embed1 = discord.Embed(
    title = 'Инвентарь',
    description = newText,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def cmd(message, *, content): #обновить
    id_user = message.author.id
    if id_user == 986313671661727744:
        content_s = content.split('  ')
        file = content_s[1] + '.json'
        if content_s[0] == 'add':
            addData(file, content_s[2], content_s[3])
            await message.channel.send(f'Файл: {content_s[1]}\nАйди: {content_s[2]}\nЗначение: {content_s[3]}')
        elif content_s[0] == 'get':
            get = getData(file, content_s[2])
            await message.channel.send(f'Файл: {content_s[1]}\nАйди: {content_s[2]}\nЗначение: {get}')
        elif content_s[0] == 'read':
            read = readData(file)
            await message.channel.send(f'Файл: {content_s[1]}\nКонтент: {read}')
        elif content_s[0] == 'update':
            updateData(file, content_s[2], content_s[3])
            await message.channel.send(f'Файл: {content_s[1]}\nАйди: {content_s[2]}\nЗначение: {content_s[3]}')
        elif content_s[0] == 'reset':
            resetData(file, content_s[2])
            await message.channel.send(f'Файл: {content_s[1]}\nАйди: {content_s[2]}')

@client.command()
async def bank_up(message): #обновить

    id_user = str(message.author.id)

    print(f'------------------------{id_user}: >bank_up')

    cur = getData(CURRENCY_FILE, id_user) or '$'
    if not cur: #проверяем наличие в базе данных, если нет - добавляем
        addData(CURRENCY_FILE, id_user, STARTING_CURRENCY)

    balance = getData(BALANCE_FILE, id_user) or 0
    if not balance: #проверяем наличие в базе данных, если нет - добавляем
        addData(BALANCE_FILE, id_user, STARTING_BALANCE)


    price = getData(LIMIT_FILE, id_user) or 200
    if int(balance) >= int(price) * 2:

        sub = int(balance) - int(price) * 2
        
        if getData(LIMIT_FILE, id_user):
            updateData(BALANCE_FILE, id_user, sub) #забираем деньги
            updateData(LIMIT_FILE, id_user, int(price) * 2) #обновляем значение
            text = f'📈Вы успешно повысили свой лимит в банке в 2 раза за {cur}**{price}**'
        elif not getData(LIMIT_FILE, id_user):
            updateData(BALANCE_FILE, id_user, sub) #забираем деньги
            addData(LIMIT_FILE, id_user, int(price) * 2) #обновляем значение
            text = f'📈Вы успешно повысили свой лимит в банке в 2 раза за {cur}**{price}**'
    
    else:
        text = f'<:error:1001754203565326346> Нехватка средств!\n💸Нужная сумма: {cur}**{price}**'
    
    embed1 = discord.Embed(
    title = 'Банк',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def casino_start(message): #обновить

    id_user = str(message.author.id)

    cur = getData(CURRENCY_FILE, id_user) or '$'
    if not cur: #проверяем наличие в базе данных, если нет - добавляем
        addData(CURRENCY_FILE, id_user, STARTING_CURRENCY)

    list_full = ['🍀', '🐉', '🐍', '🐍', '🍎', '🍏', '🥝', '🥝', '🍙', '🍙', '🎩', '🎲', '🧠', '😈', '🎲', '🐙', '🧠', '🍄', '🌵', '🍨', '🧧', '🏮', '🧧', '🎁', '🎉', '🍄', '🔥', '👊', '👊', '🦀', '👊']
    list = list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)]
    
    if not getData(CASINO_FILE, 'casino'):
        addData(CASINO_FILE, 'casino', list)
    else:
        updateData(CASINO_FILE, 'casino', list)

    embed1 = discord.Embed(
    title = 'Лотерея',
    description = f'🔒Создана комбинация: {list}\n💰Цена билета: **{cur}500**',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def casino(message, *, content): #обновить

    id_user = str(message.author.id)

    cur = getData(CURRENCY_FILE, id_user) or '$'
    if not cur: #проверяем наличие в базе данных, если нет - добавляем
        addData(CURRENCY_FILE, id_user, STARTING_CURRENCY)

    balance = getData(BALANCE_FILE, id_user) or 0
    if not balance: #проверяем наличие в базе данных, если нет - добавляем
        addData(BALANCE_FILE, id_user, STARTING_BALANCE)

    if content == 'view':
        text = '🔒Общая комбинация: ' + getData(CASINO_FILE, 'casino')
    elif content == 'buy':
        price = 500
        if int(balance) >= int(price):
            unit = 0
            list_full = ['🍀', '🐉', '🐍', '🐍', '🍎', '🍏', '🥝', '🥝', '🍙', '🍙', '🎩', '🎲', '🧠', '😈', '🎲', '🐙', '🧠', '🍄', '🌵', '🍨', '🧧', '🏮', '🧧', '🎁', '🎉', '🍄', '🔥', '👊', '👊', '🦀', '👊']
            list_user = list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)] + ' ' + list_full[random.randint(0, 30)]
            list_user_split = list_user.split(' ')
            list = getData(CASINO_FILE, 'casino')
            list_split = list.split(' ')
            for x in list_user_split:
                if x in list_split:
                    unit += 1
            win = str(int(price) * int(unit) / 2)
            win = int(win.replace('.0', ''))
            win = int(win) - int(price)
            sum = int(balance) + int(win)
            updateData(BALANCE_FILE, id_user, sum) #добавляем деньги
            win = int(win) + int(price)
            text = f'📄Ваш билет: {list_user} \n🔒Общее: {list}\n📥С данного билета вы получили: **{cur}{win}**\n💰Цена билета: **{cur}500**'
        else:
            text = f'Нехватка средств! Стоимость билета: **{cur}{price}**'

    embed1 = discord.Embed(
    title = 'Лотерея',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def shop(message, *, content): #обновить

    id_user = str(message.author.id)

    print(f'------------------------{id_user}: >shop {content}')

    content_split = content.split()

    cur = getData(CURRENCY_FILE, id_user) or '$'
    if not cur: #проверяем наличие в базе данных, если нет - добавляем
        addData(CURRENCY_FILE, id_user, STARTING_CURRENCY)

    balance = getData(BALANCE_FILE, id_user) or 0
    if not balance: #проверяем наличие в базе данных, если нет - добавляем
        addData(BALANCE_FILE, id_user, STARTING_BALANCE)

    if content_split[0] == 'buy' and len(content_split) == 2:
        if content_split[1] == 'badge' and int(balance) >= 1000:
            sub = int(balance) - 1000
            updateData(BALANCE_FILE, id_user, sub) #забираем деньги

            badge = getData(BADGE_FILE, id_user)
            if badge and not '<:medal:1001048705350250516>' in badge:
                updateData(BADGE_FILE, id_user, badge + ' <:medal:1001048705350250516>')
            elif not badge:
                addData(BADGE_FILE, id_user, '<:medal:1001048705350250516>')
            
            text = f'Вы успешно купили значок <:medal:1001048705350250516> за {cur}**1000**'
        else:
            price = getData(SHOP_FILE, content_split[1].replace('<@&', '').replace('>', '')) or 'None'
            if price != 'None' and int(balance) >= int(price):

                sub = int(balance) - int(price)
                id_role = content_split[1].replace('<@&', '').replace('>', '')

                updateData(BALANCE_FILE, id_user, sub) #забираем деньги

                author = message.message.author
                guild = client.get_guild(int(message.guild.id))
                role = guild.get_role(int(id_role))
                await author.add_roles(role) # выдаем автору роль
                text = f'Вы успешно купили роль **{content_split[1]}** за {cur}**{price}**'
            else:
                text = '<:error:1001754203565326346> Нехватка средств или такой роли нет в магазине'

    elif content_split[0] == 'add' and len(content_split) == 3 and message.author.guild_permissions.administrator and int(content_split[2]) >= 0:
        id_role = content_split[1].replace('<@&', '').replace('>', '')
        shop = getData(SHOP_FILE, id_role) or 'None'
        if shop != 'None':
            updateData(SHOP_FILE, id_role, content_split[2]) #убираем из инвентаря
            text = f'Вы успешно заменили цену в магазине на роль {content_split[1]} на {cur}**{content_split[2]}**'
        elif shop == 'None':
            addData(SHOP_FILE, id_role, content_split[2])
            text = f'Вы успешно добавили в магазин роль {content_split[1]} за {cur}**{content_split[2]}**'

    elif content_split[0] == 'reset' and message.author.guild_permissions.administrator:
        with open(SHOP_FILE, 'w') as f:
            json.dump('', f)
            text = 'Магазин был сброшен!'

    elif content_split[0] == 'view':
        shop = readData(SHOP_FILE) or 'Пусто'
        if shop != 'Пусто':
            text = ''
            shop_s = shop.split('\n')
            for x in shop_s:
                if x != '':
                    x_s = x.split('|')

                    guild = client.get_guild(int(message.guild.id))
                    role_c = guild.get_role(int(x_s[0]))

                    if role_c:
                        role = '<@&' + x_s[0] + '>'
                        price = cur + '**' + x_s[1] + '**'
                        text = text + '\n' + role + ' - ' + price
            text = text + f'\n\n-----**Коллекция**-----\n***Монарх*** - <:medal:1001048705350250516>\nСтоимость: {cur}**1000**\n Для покупки введите вместо роли - `badge`'

    else:
        text = '<:error:1001754203565326346> Проверьте написание команды!'

    embed1 = discord.Embed(
    title = 'Офицальный магазин',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def top(message, *, content): #обновить
    id_user = message.author.id
    print('+')

    text = readData(BALANCE_FILE)  

    embed1 = discord.Embed(
    title = 'Обновления',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)


    id_user = str(message.author.id)

    print(f'------------------------{id_user}: >shop {content}')

    content_split = content.split()

    cur = getData(CURRENCY_FILE, id_user) or '$'
    if not cur: #проверяем наличие в базе данных, если нет - добавляем
        addData(CURRENCY_FILE, id_user, STARTING_CURRENCY)

    balance = getData(BALANCE_FILE, id_user) or 0
    if not balance: #проверяем наличие в базе данных, если нет - добавляем
        addData(BALANCE_FILE, id_user, STARTING_BALANCE)

    if content_split[0] == 'buy' and len(content_split) == 2:
        if content_split[1] == 'badge' and int(balance) >= 1000:
            sub = int(balance) - 1000
            updateData(BALANCE_FILE, id_user, sub) #забираем деньги

            badge = getData(BADGE_FILE, id_user)
            if badge and not '<:medal:1001048705350250516>' in badge:
                updateData(BADGE_FILE, id_user, badge + ' <:medal:1001048705350250516>')
            elif not badge:
                addData(BADGE_FILE, id_user, '<:medal:1001048705350250516>')
            
            text = f'Вы успешно купили значок <:medal:1001048705350250516> за {cur}**1000**'
        else:
            price = getData(SHOP_FILE, content_split[1].replace('<@&', '').replace('>', '')) or 'None'
            if price != 'None' and int(balance) >= int(price):

                sub = int(balance) - int(price)
                id_role = content_split[1].replace('<@&', '').replace('>', '')

                updateData(BALANCE_FILE, id_user, sub) #забираем деньги

                author = message.message.author
                guild = client.get_guild(int(message.guild.id))
                role = guild.get_role(int(id_role))
                await author.add_roles(role) # выдаем автору роль
                text = f'Вы успешно купили роль **{content_split[1]}** за {cur}**{price}**'
            else:
                text = '<:error:1001754203565326346> Нехватка средств или такой роли нет в магазине'

    elif content_split[0] == 'add' and len(content_split) == 3 and message.author.guild_permissions.administrator and int(content_split[2]) >= 0:
        id_role = content_split[1].replace('<@&', '').replace('>', '')
        shop = getData(SHOP_FILE, id_role) or 'None'
        if shop != 'None':
            updateData(SHOP_FILE, id_role, content_split[2]) #убираем из инвентаря
            text = f'Вы успешно заменили цену в магазине на роль {content_split[1]} на {cur}**{content_split[2]}**'
        elif shop == 'None':
            addData(SHOP_FILE, id_role, content_split[2])
            text = f'Вы успешно добавили в магазин роль {content_split[1]} за {cur}**{content_split[2]}**'

    elif content_split[0] == 'reset' and message.author.guild_permissions.administrator:
        with open(SHOP_FILE, 'w') as f:
            json.dump('', f)
            text = 'Магазин был сброшен!'

    elif content_split[0] == 'view':
        shop = readData(SHOP_FILE) or 'Пусто'
        if shop != 'Пусто':
            text = ''
            shop_s = shop.split('\n')
            for x in shop_s:
                if x != '':
                    x_s = x.split('|')

                    guild = client.get_guild(int(message.guild.id))
                    role_c = guild.get_role(int(x_s[0]))

                    if role_c:
                        role = '<@&' + x_s[0] + '>'
                        price = cur + '**' + x_s[1] + '**'
                        text = text + '\n' + role + ' - ' + price
            text = text + f'\n\n-----**Коллекция**-----\n***Монарх*** - <:medal:1001048705350250516>\nСтоимость: {cur}**1000**\n Для покупки введите вместо роли - `badge`'

    else:
        text = '<:error:1001754203565326346> Проверьте написание команды!'

    embed1 = discord.Embed(
    title = 'Офицальный магазин',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def news(message):
    version = '2.0.0'
    when = '09.01.2024'
    text = f'**Версия**: *v.{version}*\n**Дата обновления**: {when}\n**ВАЖНО:**\n- Начат перенос проекта под новые системы хранения данных и синхронизации'
    embed1 = discord.Embed(
    title = 'Обновления',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

client.remove_command('help')
@client.command()
async def help(message):
    text = '**💰 Базовая экономика**\n`>bal`, `>bonus`, `>deposit <count>`, `>withdraw <count>`, `>pay <@user> <count>`, `>bank_up`, `>hack <@user>`, `>hack_up <hacks/protects>`, `>shop <buy/add/reset/view> (price)`\n**🏢 Корпорация**\n`>inc_create <name>`, `>inc_info`, `>inc_up <ad/build>`, `>inc_inv`, `>set_work <name/_leave_>`, `>inc_market <buy/sell> <count> <name>`, `>inc_stocks <name>`, `>inc_store`, `>inc_take <count>`\n**💾 Кастомизация**\n`>badge`, `>set_currency <number>`'

    embed1 = discord.Embed(
    title = 'Помощь',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def info(message): #обновить
    embed1 = discord.Embed(
    title = 'Помощь',
    description = 'Документация: [Click](https://docs.google.com/document/d/1QI_4Ye-nl4sGJo4N6G45699uZ6UwIhgSeuf_cWwejFw/edit?usp=sharing)',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

#@client.event
#async def on_command_error(message, error):  

    #if isinstance(error, commands.MissingRequiredArgument):
    #    embed1 = discord.Embed(
    #    title = 'Ошибка',
    #    description = f'<:error:1001754203565326346> Проверьте написание команды или запрошенные ею аргументы! (в команде `>help`, то что `<`в скобочках`>`)',
    #    color = 0xffff00)
    #    await message.channel.send(embed = embed1)

    #    user = await client.fetch_user(user_id=986313671661727744)
    #    await user.send(error)


    #elif isinstance(error, commands.errors.CommandInvokeError):    
    #    embed1 = discord.Embed(
    #    title = 'Ошибка',
    #    description = f'<:error:1001754203565326346> Отсутствие данных',
    #    color = 0xffff00)
    #    await message.channel.send(embed = embed1)

    #    user = await client.fetch_user(user_id=986313671661727744)
    #    await user.send(error)

    #elif isinstance(error, commands.CommandNotFound):
    #    embed1 = discord.Embed(
    #    title = 'Ошибка',
    #    description = f'<:error:1001754203565326346> Такой команды **не существует**, проверьте в `>help`!',
    #    color = 0xffff00)
    #    await message.channel.send(embed = embed1)

    #    user = await client.fetch_user(user_id=986313671661727744)
    #    await user.send(error)


    #else:
    #    embed1 = discord.Embed(
    #    title = 'Неизвестная ошибка',
    #    description = f'<:error:1001754203565326346> {error}',
    #    color = 0xffff00)
    #    await message.channel.send(embed = embed1)

    #    user = await client.fetch_user(user_id=986313671661727744)
    #    await user.send(error)

@client.event
async def on_message(message): #обновить
    await client.process_commands(message)
    user_id = str(message.author.id)

    global messages
    messages += 1

client.run("OTk4MjU2NTAyOTQwOTA1NTQy.GzpghI.K0CKOr8m2YOpPqI8IlA4gJP8ZT0J2UAVLsW2hY", bot=True) #запускаем бота
