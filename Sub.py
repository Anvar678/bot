
from aiogram import Bot, Dispatcher, executor, types
import pandas as pd
import fileinput

API_TOKEN = ''
open_weather_token = ""
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

sales1 = pd.read_excel('', sheet_name = 'Лист1')
sales2 = pd.read_excel('', sheet_name = 'Лист1')
sales3 = pd.read_excel('', sheet_name = 'Лист1')

name=''

St_or_prep = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_text = ('Я студент', 'Я преподаватель')
St_or_prep.row(*(types.KeyboardButton(text) for text in buttons_text))

par_ot_k= types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_text = ('Создать пароль для комнаты', 'Назад↩')
buttons_text1 = ('Создать расписание', '')
par_ot_k.row(*(types.KeyboardButton(text) for text in buttons_text))
par_ot_k.row(*(types.KeyboardButton(text) for text in buttons_text1))

vvedite_par= types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_text = ('Ввести код комнаты', 'Назад↩')
buttons_text1 = ('Посмотреть расписание', '')
vvedite_par.row(*(types.KeyboardButton(text) for text in buttons_text))
vvedite_par.row(*(types.KeyboardButton(text) for text in buttons_text1))

st_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_text = ('Выйти из комнаты', '')
buttons_text1 =('Ответить', 'Посмотреть вопросы')
st_menu.row(*(types.KeyboardButton(text) for text in buttons_text))
st_menu.row(*(types.KeyboardButton(text) for text in buttons_text1))

t_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_text = ('Задать вопрос', 'Посмотреть ответы')
buttons_text1 =('Bыйти из сессии', 'Посмотреть список учеников')#B нглийская
t_menu.row(*(types.KeyboardButton(text) for text in buttons_text))
t_menu.row(*(types.KeyboardButton(text) for text in buttons_text1))


trig1=0
trig2=0
trig3=0
trig4=0
trig5=0
trig6=0

kol_cit = sales3["Число"][0]

def city():#главное меню
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton("Мой город", request_location=True, resize_keyboard=True)
    keyboard.add(button1)
    return keyboard

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    global latitude#широта и долгота
    global longitude#делаю все эти переменные глобальными т.к. они нужны будут потом
    global city#город вкоторомнаходитьтся пользователь
    global chat_id#айди чата, нужен для разграничения пользователей
    chat_id = message.chat.id
    latitude = message.location.latitude  # получаю эти переменные
    longitude = message.location.longitude
    await message.reply("Ваш город:", reply_markup=St_or_prep)  # определение города по координатам
    i = 0
    a = 0
    while i < kol_cit:
        if latitude >= sales3['МинШирота'][i] and latitude <= sales3['МаксШирота'][i] and longitude >= sales3['МинДолгота'][i] and longitude <= sales3['МаксДолгота'][i]:
            a = 1
            city = sales3['Город'][i]
            sil = str(sales3['Ссылка'][i])
            if sil == 'nan':
                await message.reply(city, reply_markup=St_or_prep)
                await message.reply("А тут могла быть ваша реклама)", reply_markup=St_or_prep)
            if sil != 'nan':
                with open(sil, 'rb') as photo:
                    await message.reply_photo(photo, caption=city)
                await message.reply("А тут могла быть ваша реклама в городе "+city, reply_markup=St_or_prep)
            break
        i += 1

    if a == 0:
        await message.reply("Не был обнаружен 🌏", reply_markup=St_or_prep)

    else:
        await message.reply('Кем вы являетесь?')

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.reply("Здравствуйте!", reply_markup=city())  # отвечает на старт
    await message.reply("Нажмите на кнопку, чтобы бот определил ваш город", reply_markup=city())

@dp.message_handler()
async def button_text(message: types.message):
    button_text = message.text  # текст который написал пользователь превращается в это
    if button_text == 'Я студент':
        global trig1
        await message.reply('Укажите фамилию, имя, курс и группу. С большой буквы, через пробел. \n'
                            'пример:\n'
                            'Иванов Иван 1 курс 1 группа')
        trig1=1

    elif trig1 ==1 and button_text!='Я студент':
        global name
        trig1=0
        i=0
        button_text = button_text.replace(" ", "_")
        while i < 5:
                a = 0
                if sales1['ФИ'][i]==button_text:
                    a=1
                    name = button_text
                    break
                i += 1
        if a == 0:
            await message.reply("Вы не были найдены в базе данных", reply_markup=St_or_prep)
        else:
            await message.reply('Мы Вас нашли, введите пароль от комнаты', reply_markup=vvedite_par)


    elif button_text == 'Я преподаватель':
        global trig2
        await message.reply('Введите ваш пароль')
        trig2=1

    elif trig2==1 and button_text!='Я преподаватель':
        try:
            trig2=0
            i=0
            while i < 3:
                a = 0
                if int(sales2['Код'][i]) == int(button_text):
                    a = 1
                    break
                i += 1
            if a == 0:
                await message.reply("Вы не были найдены в базе данных", reply_markup=St_or_prep)
            else:
                await message.reply('Здравствуйте, '+sales2['ФИ'][i], reply_markup=par_ot_k)
        except ValueError:
            await message.reply("Вы не были найдены в базе данных", reply_markup=St_or_prep)

    elif button_text == 'Создать пароль для комнаты':
        global trig3
        await message.reply('Введите любой набор цифр:')
        trig3=1

    elif trig3==1 and button_text!='Создать пароль для комнаты':
        trig3=0
        global par
        global file_buf
        par = button_text
        file = open(button_text+'.txt', 'a')
        file_buf = button_text+'.txt'
        file.close()
        await message.reply('Файл создан', reply_markup=t_menu)

    elif button_text == 'Ввести код комнаты':
        global trig4
        trig4=1
        await message.reply('Введите код комнаты:')

    elif trig4==1 and button_text !='Ввести код комнаты':
        trig4=0
        try:
            file = open(button_text+'.txt', 'x+')
            file.close()
        except FileExistsError:
            await message.reply('Вас добавили в комнату', reply_markup=st_menu)
            file = open(button_text + '.txt', 'w')
            file.write(name + '\n')
            file.close()

    elif button_text =='Посмотреть список учеников':
        await message.reply('Вывожу список:')
        file = open(file_buf, 'r')
        for string in file:
            await message.reply(string)
        file.close()

    elif button_text == 'Задать вопрос':
        await message.reply('Напишите вопрос, не забудьте указать знак "?"')

    elif button_text.find('?')>-1:
        print(message.chat.id)
        file = open('q.txt', 'a')
        file.write('Вопрос от учителя:'+button_text)
        file.close()
        await message.reply('Ваш вопрос задан')

    elif button_text == 'Посмотреть вопросы':
        file=open('q.txt', 'r+')
        for string in file:
            await message.reply(string)
        file.truncate(0)
        file.close()

    elif button_text == 'Ответить':
        global trig5
        await message.reply('Напишите ответ:')
        trig5=1

    elif trig5==1 and button_text!='Ответить':
        trig5=0
        file = open('otv.txt', 'r+')
        file.write('Ответ ученика '+name+': '+button_text)
        file.close()
        await message.reply('Ваш ответ отправлен')

    elif button_text == 'Посмотреть ответы':
        file = open('otv.txt', 'r+')
        for string in file:
            await message.reply(string)
        file.truncate(0)
        file.close()

    elif button_text == 'Выйти из сессии':
        await message.reply('Возвращаюсь в меню', reply_markup=St_or_prep)
        for line in fileinput.input(file_buf, inplace=True):
            if name in line:
                continue

    elif button_text == 'Создать расписание':
        global trig6
        file = open('rasp.txt', 'r')
        spis=[]
        sep = "\n"
        i=0
        for string in file:
            spis.insert(i, string)
            i+=1
        file.close()
        await message.reply('Текущее расписание:')
        await message.reply((sep.join(map(str, spis))))
        await message.reply('Напишите новое расписание желаетльно НЕ в одну строчку):')
        trig6=1

    elif button_text != 'Создать расписание' and trig6==1:
        trig6=0
        file = open('rasp.txt', 'w')
        file.write(button_text)
        file.close()
        await message.reply('Расписание создано')


    elif button_text =='Посмотреть расписание':
        file = open('rasp.txt', 'r')
        sep = "\n"
        spis = []
        i = 0
        for string in file:
            spis.insert(i, string)
            i += 1
        file.close()
        await message.reply('Текущее расписание:')
        await message.reply((sep.join(map(str, spis))))
        file.close()

    elif button_text == 'Bыйти из сессии':
        await message.reply('Возвращаюсь в меню', reply_markup=St_or_prep)

    elif button_text == 'Назад':
        await message.reply('Возвращаюсь в меню', reply_markup=St_or_prep)

    else:
        await message.reply('Вы ввели не то', reply_markup= St_or_prep)


if __name__ == '__main__':
    executor.start_polling(dp)
