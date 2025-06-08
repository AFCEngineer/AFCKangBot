# pingpong_game.py
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict

# Store active games: {chat_id: {"player1": user_id, "player2": user_id, "turn": 1/2, "score": (0, 0)}}
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
            "turn": 1,  # Player1 starts
            "score": (0, 0),
        }

        await message.reply(
            f"🏓 **PingPong Challenge!** 🏓\n"
            f"👤 Player 1: {message.from_user.mention}\n"
            f"👤 Player 2: {message.reply_to_message.from_user.mention}\n\n"
            f"📊 **Score:** 0-0\n"
            f"🔄 It's **Player 1**'s turn!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Hit the Ball!", callback_data="pingpong_hit")]
            ])
        )

    @client.on_callback_query(filters.regex(r"^pingpong_hit$"))
    async def handle_hit(client, callback_query):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        game = pingpong_games.get(chat_id)

        if not game:
            await callback_query.answer("Game over or not started!", show_alert=True)
            return

        current_turn = game["turn"]
        expected_player = game[f"player{current_turn}"]

        if user_id != expected_player:
            await callback_query.answer("⏳ Not your turn!", show_alert=True)
            return

        # Switch turns
        game["turn"] = 2 if current_turn == 1 else 1

        # 10% chance to miss
        import random
        if random.random() < 0.1:
            winner = "Player 2" if current_turn == 1 else "Player 1"
            await callback_query.edit_message_text(
                f"🎉 **{winner} WINS!** 🎯\n"
                f"📊 Final Score: {game['score'][0]} - {game['score'][1]}\n\n"
                "🔄 Type /pingpong to play again!"
            )
            del pingpong_games[chat_id]
            return

        # Update score
        if current_turn == 1:
            game["score"] = (game["score"][0] + 1, game["score"][1])
        else:
            game["score"] = (game["score"][0], game["score"][1] + 1)

        # Update message
        await callback_query.edit_message_text(
            f"🏓 **PingPong!** 🏓\n"
            f"📊 Score: {game['score'][0]} - {game['score'][1]}\n\n"
            f"🔄 It's **Player {game['turn']}**'s turn!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔥 Hit the Ball!", callback_data="pingpong_hit")]
            ])
        )
