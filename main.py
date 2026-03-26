import os
import discord
from discord.ext import commands

# intents設定（これ超重要）
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ARIGATOU_PATTERNS = [
    "ありがとう",
    "ありがとございます",
    "ありがとうございます",
    "ありがとね",
    "ありがとな",
    "thx",
    "thanks",
    "thank you",
    "サンクス",
]

@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

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

# トークン取得
token = os.getenv("DISCORD_TOKEN")

if not token:
    print("DISCORD_TOKENが設定されてねぇぞ！")
else:
    bot.run(token)
