# handlers/pingpong.py
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict

pingpong_games = defaultdict(dict)

def register_pingpong_handlers(client):
    @client.on_message(filters.command("pingpong") & filters.group)
    async def start_pingpong(client, message):
        chat_id = message.chat.id
        if chat_id in pingpong_games:
            await message.reply("🚫 A game is already running here!")
            return

        if not message.reply_to_message:
            await message.reply("❌ Reply to a user to challenge them!")
            return

        player1 = message.from_user.id
        player2 = message.reply_to_message.from_user.id

        pingpong_games[chat_id] = {
            "player1": player1,
            "player2": player2,
            "turn": 1,
            "score": (0, 0),
        }

        await message.reply(
            f"🏓 **PingPong Challenge!** 🏓\n"
            f"👤 Player 1: {message.from_user.mention}\n"
            f"👤 Player 2: {message.reply_to_message.from_user.mention}\n\n"
            f"📊 Score: 0-0\n"
            f"🔄 It's Player 1's turn!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Hit the Ball!", callback_data="pingpong_hit")]
            ])
        )

    @client.on_callback_query(filters.regex(r"^pingpong_hit$"))
    async def handle_hit(client, callback_query):
        # ... (keep the rest of the callback code unchanged)
        # Full code: https://github.com/AFCEngineer/AFCKangBot/blob/main/handlers/pingpong.py
