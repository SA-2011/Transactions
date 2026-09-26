# Transactions

import asyncio
from dotenv import load_dotenv
from aiogram import Dispatcher, Router, Bot , F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from connection import create_table
from service import *
import os
from aiogram.types import ReplyKeyboardMarkup , KeyboardButton

load_dotenv()

token = os.getenv("token")
bot = Bot(token)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Show history"),
            KeyboardButton(text="Show profile"),
        ],
        [
            KeyboardButton(text="Deposit"),
            KeyboardButton(text="Withdraw"),
        ],
        [
            KeyboardButton(text="Add debt"),
            KeyboardButton(text="Add goal"),
        ],
        [
            KeyboardButton(text="See all debts"),
            KeyboardButton(text="See all goals"),
        ],
        [
            KeyboardButton(text="Update debt"),
            KeyboardButton(text="Update goal"),
        ],
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def startbot(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(f"Hello {message.from_user.full_name} dear! This is your accoutn where you van see your money tranzactions! 💸💵" , reply_markup=main_kb)
    else:
        await save_user(message.from_user.id , message.from_user.username , message.from_user.full_name)
        await message.answer(f"Hello {message.from_user.full_name} dear! This is your accoutn where you van see your money tranzactions! 💸💵" , reply_markup=main_kb)

@dp.message(F.text == "Show history")
@dp.message(Command("show_history"))
async def history(message: Message):
    sh = await show_history(message.from_user.id)
    if sh == None:
        await message.answer("No transactions found.")
        return
    text = "== History ==\n"

    for trans in sh:
        text += f"""
Transaction ID: {trans['tranzactions_id']}
Full name: {trans['full_name']}
Balance: {trans['balance']}
Type: {trans['type']}
Telegram ID: {trans['tg_id']}
Amount: {trans['amount']}"""

    await message.answer(text)

@dp.message(F.text == "Show profile")
@dp.message(Command("show_profile"))
async def profile(message: Message):
    sp = await show_profile(message.from_user.id)
    await message.answer(f"""
    ==Profile==
user id {sp['user_id']}
Username {sp['user_name']}
Fullname {sp['full_name']}
Balance {sp['balance']}
Telegram id {sp['tg_id']}
""")

@dp.message(F.text == "Deposit")
async def d_a(message: Message):
    await message.answer("Enter /deposit command to try this function and acomand name enter amount like ts:\n/deposit 500")

@dp.message(Command("deposit"))
async def depos(message: Message , command: CommandObject):
    u_answer = command.args
    if u_answer is None:
        await message.answer("enter like this /deposit 500")
        return
    await deposit(message.from_user.id , u_answer)

@dp.message(F.text == "Withdraw")
async def d_a(message: Message):
    await message.answer("Enter /withdraw command to try this function and acomand name enter amount like this:\n/withdraw 100")

@dp.message(Command("withdraw"))
async def depos(message: Message , command: CommandObject):
    u_answer = command.args
    if u_answer is None:
        await message.answer("enter like this /withdraw 500")
        return
    await withdraw(message.from_user.id , u_answer)

@dp.message(F.text == "Add debt")
async def debt_button(message: Message):
    await message.answer("For this function enter /add_debt info/amount")

@dp.message(Command("add_debt"))
async def add_debt(message: Message , command: CommandObject):
    u_answer = command.args
    if u_answer is None:
        await message.answer("You don't added all information or you enter nothing plese add")
    else:
        u_answer = u_answer.split("/")
        await add_dolg(u_answer[0] , int(u_answer[1]) , message.from_user.id)
        await message.answer("Debt added sucsessfully!")

@dp.message(F.text == "Add goal")
async def debt_button(message: Message):
    await message.answer("For this function enter /add_goal info/amount")

@dp.message(Command("add_goal"))
async def add_debt(message: Message , command: CommandObject):
    u_answer = command.args
    if u_answer is None:
        await message.answer("You don't added all information or you enter nothing plese add all information lie you need 📜📝")
    else:
        u_answer = u_answer.split("/")
        await add_dolg(u_answer[0] , int(u_answer[1]) , message.from_user.id)
        await message.answer("Goal added sucsessfully!")

@dp.message(F.text == "See all debts")
@dp.message(Command("see_debts"))
async def see_debt(message: Message):
    show = await show_your_dolg(message.from_user.id)
    if show == None:
        await message.answer("You don't have debts")
    else:
        text = "Your debts:\n"
        for i in show:
            text += (f"""
Debt_id: {i[0]}
Information: {i[2]}
Money amount: {i[3]}
    """)
        await message.answer(text)

@dp.message(F.text == "See all goals")
@dp.message(Command("see_goals"))
async def see_debt(message: Message):
    show = await show_your_goals(message.from_user.id)
    if show is None:
        await message.answer("You don't have goals")
    else:
        text = "Your Goals:\n"
        for i in show:
            text += (f"""
Debt_id: {i[0]}
Information: {i[2]}
Money amount: {i[3]}
    """)
        await message.answer(text)

@dp.message(F.text == "Update debt")
async def message_for_debts(message: Message):
    await message.answer("For thise func enter /update_debt dept_id/amount to add to dolg from your balance")

@dp.message(Command("update_debt"))
async def update_debts(message: Message , command: CommandObject):
    update_d = command.args
    if update_d is not None:
        update_d = update_d.split("/")
        await update_dolg(message.from_user.id , update_d[0] , update_d[1])
        await message.answer("Update finished")
    else:
        await message.answer("You don't enter information or you enter not properly enter like this: /update_debt dept_id/amount")

@dp.message(F.text == "Update goal")
async def message_for_goal(message: Message):
    await message.answer("For thise func enter /update_goal goal_id/amount to add to goal from your balance")

@dp.message(Command("update_goal"))
async def update_goal(message: Message , command: CommandObject):
    update_d = command.args
    if update_d is not None:
        update_d = update_d.split("/")
        await update_goal(message.from_user.id , update_d[0] , update_d[1])
        await message.answer("Update finished")
    else:
        await message.answer("You don't enter information or you enter not properly enter like this: /update_goal goal_id/amount")


async def main():
    print("Bot started")
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())