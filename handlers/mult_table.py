import random
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from tinydb import TinyDB, Query
db = TinyDB('players.json')
Player = Query()

def create_table():    #таблица рожается функцией для возможности дальнейшего редактирования (сложность, выбор чисел и т.д)
    table = {k: "" for k in range(1, 101)}
    k = 0
    for i in range(1, 11):
        for j in range(1, 11):
            k += 1
            table[k] = [i, j]
    return table


table = create_table()


class PlayPhase(StatesGroup):       #текущая фаза игрока
    waiting_for_answer = State()
    made_error = State()


async def mult_table_start(message: types.Message, state: FSMContext):
    if not db.search(Player.id == message.from_user.id):        #впервые в игре
        db.insert({'id': message.from_user.id, 'score': 0, 'record': 0, 'lives': 3, 'ans': ""})
        await message.answer("написать приветственное сообщение с правилами")
    else:       #уже бывал в игре
        await message.answer("поприветствовать и вывести рекорд")
    ex = table[random.choice(range(1, 101))]
    await message.answer(f"А вот и первый пример: {ex[0]} * {ex[1]}")
    db.update({'ans': str(ex[0]*ex[1])}, Player.id == message.from_user.id)
    await state.set_state(PlayPhase.waiting_for_answer.state)


async def in_game(message: types.Message, state: FSMContext):
    curlives = db.search(Player.id == message.from_user.id)[0]['lives']
    curscore = db.search(Player.id == message.from_user.id)[0]['score']
    currecord = db.search(Player.id == message.from_user.id)[0]['record']
    if message.text == db.search(Player.id == message.from_user.id)[0]['ans']: #ответ верный
        db.update({'score': curscore}, Player.id == message.from_user.id)
        await message.answer("Отлично! Давай решим следующий пример!")
    else:       #произошла ошибка  ПЕРЕДЕЛАТЬ ТАК, ЧТОБЫ ПЕРЕРЕШИВАЛИ ТОТ ЖЕ ПРИМЕР
        if curlives > 1:  #не смерть
            db.update({'lives': curlives - 1}, Player.id == message.from_user.id)
            await message.answer("К сожалению, ты ошибся(( Давай попробуем ещё раз!")
        else: #смерть
            await message.answer("К сожалению, ты потерял все жизни( ")
            if currecord > curscore:
                await message.answer(f"Ты установил новый личный рекорд: {curscore}!!!")
                db.update({'record': curscore}, Player.id == message.from_user.id)
            else:
                await message.answer(f"В этой попытке ты решил верно {curscore} примеров подряд!!!")
                db.update({'record': curscore}, Player.id == message.from_user.id)
    ex = table[random.choice(range(1, 101))]
    await message.answer(f"Сколько будет: {ex[0]} * {ex[1]}?")
    db.update({'ans': str(ex[0] * ex[1])}, Player.id == message.from_user.id)
    return


def register_handlers_mult_table(dp: Dispatcher):
    dp.register_message_handler(mult_table_start, commands="start", state="*")
    dp.register_message_handler(in_game, state=PlayPhase.waiting_for_answer.state)



