# импорт необходимых библиотек и методов
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
# блок из aiogram для работы с клавиатурой и объект кнопки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# api ключ, который мы получили в «BotFather». Переменная бота,
# хранящая объект бота, «token» будет равен вписанному ключу
api = ""  # введите Ваш api полученный в @BotFather
bot = Bot(token=api)
# переменная dp объекта «Dispatcher», у него наш бот в
# качестве аргументов. В качестве «Storage» будет «MemoryStorage»
dp = Dispatcher(bot, storage=MemoryStorage())
# объявление переменной kb (клавиатуры) экземпляр ReplyKeyboardMarkup с параметрами
kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
kb1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
# объявление переменной "кнопка с текстом"
button = KeyboardButton(text='Информация')
button1 = KeyboardButton(text='Расчитать')
button2 = KeyboardButton(text='м')
button3 = KeyboardButton(text='ж')
# добавление созданной кнопки в клавиатуру по одной в ряд
# kb.add(button)
# kb.add(button2)
# добавление созданных кнопoк в ряд в клавиатуру разом
kb.row(button, button1)
kb1.row(button2, button3)


# добавление созданной кнопки в конец последнего ряда
# kb.insert(button)

# объявление класса состояния UserState наследованный от StatesGroup
class UserState(StatesGroup):
    # объявление объектов класса age, growth, weight, man (возраст, рост, вес, пол)
    age = State()
    growth = State()
    weight = State()
    man = State()
   
# обработчик начала общения с ботом
@dp.message_handler(commands=['start'])
# функция старта
async def start(message):
    # дополнение методом reply_markup для отображения клавиатуры kb
    await message.reply('Привет! Я бот помогающий вашему здоровью.\n'
                        'Нажмите одну из кнопок для продолжения', reply_markup=kb)


# обработчик ожидания нажатия кнопки «Расчитать»
@dp.message_handler(text=['Расчитать'], state=None)
# функция получения возраста пользователя
async def set_age(message: types.Message, state: FSMContext):
    # ожидание сообщения Calories и вывод текста
    await message.reply('Ваш возраст (полных лет):')
    # ожидание ввода возраста
    await UserState.age.set()


# обработчик ожидания окончания статуса UserState.age
@dp.message_handler(state=UserState.age)
# функция получения роста пользователя
async def set_growth(message: types.Message, state: FSMContext):
    # ожидание сохранение сообщения возраста от пользователя в базе данных состояния
    await state.update_data(age_=message.text)
    # ожидание вывода текста
    await message.reply('Введите свой рост (см):')
    # ожидание ввода роста
    await UserState.growth.set()


# обработчик ожидания окончания статуса UserState.growth
@dp.message_handler(state=UserState.growth)
# функция получения веса пользователя
async def set_weight(message: types.Message, state: FSMContext):
    # ожидание сохранение сообщения роста от пользователя в базе данных состояния
    await state.update_data(growth_=message.text)
    # ожидание вывода текста
    await message.reply('Введите свой вес (кг):')
    # ожидание ввода веса
    await UserState.weight.set()


# обработчик ожидания окончания статуса UserState.weight
@dp.message_handler(state=UserState.weight)
# функция получения пола пользователя
async def set_weight(message: types.Message, state: FSMContext):
    # ожидание сохранение сообщения веса от пользователя в базе данных состояния
    await state.update_data(weight_=message.text)
    # ожидание вывода текста
    await message.reply('Введите свой пол (м / ж):', reply_markup=kb1)
    # ожидание ввода пола
    await UserState.man.set()


# обработчик ожидания окончания статуса UserState.weight
@dp.message_handler(state=UserState.man)
# функция расчета суточного рациона пользователя в калориях
async def set_calories(message: types.Message, state: FSMContext):
    # ожидание сохранение сообщения веса от пользователя в базе данных состояния
    await state.update_data(man_=message.text)
    # сохранение полученных данных в переменной data
    data = await state.get_data()
    # условие анализа пола пользователя
    if str(data['man_']) == 'м':
        # Расчет по формуле Миффлина-Сан Жеора для мужчин
        calories = int(data['weight_']) * 10 + int(data['growth_']) * 6.25 - int(data['age_']) * 5 + 5
        # ожидание вывода текста результатов расчета
        await message.reply(f'Ваша норма калорий {calories} день')
    elif str(data['man_']) == 'ж':
        # Расчет по формуле Миффлина-Сан Жеора для женщин
        calories = int(data['weight_']) * 10 + int(data['growth_']) * 6.25 - int(data['age_']) * 5 - 161
        # ожидание вывода текста результатов расчета
        await message.reply(f'Ваша норма калорий {calories} день')
    # завершение работы машины состояния
    await state.finish()


# обработчик кнопок Информация
@dp.message_handler(text=['Информация'])
# функция кнопок
async def inform(message):
    await message.answer("Бот поможет расчитать суточный рацион в калориях\n"
                         "для вашего возраста, роста, веса и пола")


# обработчик перехвата любых сообщений
@dp.message_handler()
# функция перехвата сообщений
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    # запуск бота (dp - аргумент через что стартовать)
    executor.start_polling(dp, skip_updates=True)
