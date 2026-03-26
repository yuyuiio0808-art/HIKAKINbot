import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ==========================================
# 1. Render用：Flaskでダミーサーバーを立てる
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Renderが指定するポート番号を取得（デフォルトは8080）
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """Flaskを別スレッドで実行してBotと並行動作させる"""
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. Discord Botの設定
# ==========================================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ARIGATOU_PATTERNS = [
    "ありがとう", "ありがとございます", "ありがとうございます",
    "ありがとね", "ありがとな", "thx", "thanks", "thank you", "サンクス",
]

@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # 各種マッチング処理
    arigatou_matched = any(p in content for p in ARIGATOU_PATTERNS)
    niga_matched = "ニガ" in content or "にが" in content
    game_matched = any(x in content for x in [
        "ゲームしよう", "げーむしよう", "ゲームしましょう", "ゲームしない"
    ])
    hikakin_matched = "hikakin" in content or "ひかきん" in content
    mejicon_matched = "メジコン" in content or "めじこん" in content
    resta_min_matched = "レスタミン" in content or "れすたみん" in content
    lettuce_matched = "レタス" in content or "れたす" in content
    seafood_matched = "魚介" in content or "ぎょかい" in content
    seikin_matched = "seikin" in content or "せいきん" in content

    # 応答ロジック
    if arigatou_matched:
        await message.reply("ブンブン！当たり前のことをしただけですよ〜 😊")
    elif niga_matched:
        await message.reply("ニガ？僕は普通の肌の色しか知りません")
    elif game_matched:
        await message.reply("クカッ！HIKAKINゲームズで動画をとりませんか？")
    elif seikin_matched:
        await message.reply("長らく会ってないですね")
    elif hikakin_matched:
        await message.reply("どうも！HIKAKINです！")
    elif mejicon_matched:
        await message.reply("次の企画はそれにしよう！")
    elif resta_min_matched:
        await message.reply("SEIKINが好きです！")
    elif lettuce_matched:
        await message.reply("いきなり野菜の話ですか？")
    elif seafood_matched:
        await message.reply(
            "マスクで汚染花粉からの被害を回避できます。また、魚介類は産地がわからないものは食べません。日本産の魚介類は終わってます。特に大型魚類と貝類は放射性物質が濃縮されますんでお気をつけて。"
        )

    await bot.process_commands(message)

# ==========================================
# 3. 実行
# ==========================================
token = os.getenv("DISCORD_TOKEN")

if not token:
    print("エラー: DISCORD_TOKENが設定されていません。")
else:
    # 1. まずFlaskサーバーをバックグラウンドで起動
    keep_alive()
    # 2. 次にDiscord Botを起動
    try:
    
        bot.run(token)
    except Exception as e:
        print(f"起動エラーが発生しました: {e}")
