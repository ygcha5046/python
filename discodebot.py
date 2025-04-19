import discord

INTENTS = discord.Intents.all()
client = discord.Client(intents=INTENTS)

# Discord 클라이언트 객체 생성

# 봇이 준비되었을 때 실행되는 이벤트 핸들러
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# 봇이 메시지를 받았을 때 실행되는 이벤트 핸들러
@client.event
async def on_message(message):
    # 메시지를 보낸 사람이 봇 자신이면 무시
    if message.author == client.user:
        return

    # !안녕 명령어에 대한 응답
    if message.content.startswith('!안녕'):
        await message.channel.send('안녕하세요!')

    # /help 명령어에 대한 응답
    elif message.content.startswith('/rule'):
        await message.channel.send('안녕하세요, 어떻게 도와드릴까요?')

# 봇 실행
client.run('')
