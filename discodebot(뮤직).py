import discord
from discord.ext import commands

# 봇의 프리픽스를 설정
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용을 읽을 수 있도록 허용
bot = commands.Bot(command_prefix="!", intents=intents)

# 봇이 준비되었을 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# !실행 명령어: 봇이 음성 채널에 들어갑니다.
@bot.command()
async def 실행(ctx):
    # 메시지를 보낸 사용자가 음성 채널에 있는지 확인
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"{channel.name}에 입장했습니다!")
    else:
        await ctx.send("음성 채널에 먼저 들어가야 합니다.")

# !멈춰 명령어: 봇이 음성 채널에서 퇴장합니다.
@bot.command()
async def 멈춰(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("음성 채널에서 퇴장했습니다!")
    else:
        await ctx.send("현재 음성 채널에 없습니다.")

# 봇 실행
bot.run('bot token')

#pip install discord.py[voice]
