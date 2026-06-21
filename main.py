import discord, os, asyncio
from dotenv import load_dotenv
from radio.radio import Radio


INTENTS = discord.Intents.default()
INTENTS.message_content = True
CLIENT = discord.Client( intents=INTENTS )
TREE = discord.app_commands.CommandTree( CLIENT )

VC = None
FFMPEG_PATH = "C:/Users/nooye/Downloads/ffmpeg-8.1.1-essentials_build/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
TEST_AUDIO_PATH = "C:/Users/nooye/Downloads/WMEW 99.9/radio/songs/9th_life.ogg"
RADIO = Radio()


@CLIENT.event
async def on_ready():
    print( "WMEW 99.9 Currently Running On:" )
    print()
    for guild in CLIENT.guilds:
        print( f"{ guild.name } ({ str( guild.id ) })" )


@CLIENT.event
async def on_message( msg: discord.Message ):
    global VC
    
    if msg.author.bot:
        return

    print( f"'{ msg.content }'" )

    if msg.content == '1':
        voiceState = msg.author.voice   # type: ignore

        if voiceState is None:
            await msg.reply( "사용자가 음성 채널에 속해 있지 않습니다." )
            return

        voiceChannel = voiceState.channel

        if voiceChannel is None:
            await msg.reply( "연결할 음성 채널을 찾을 수 없습니다." )
            return

        VC = await voiceChannel.connect()
        await msg.reply( "connect" )
        await playAudio( TEST_AUDIO_PATH )

    elif msg.content == '2':
        voiceState = msg.author.voice   # type: ignore

        if voiceState is None:
            await msg.reply( "사용자가 음성 채널에 속해 있지 않습니다." )
            return

        voiceChannel = voiceState.channel

        if voiceChannel is None:
            await msg.reply( "사용자가 연결된 음성 채널을 찾을 수 없습니다." )
            return

        if VC is None:
            await msg.reply( "연결 해제할 음성 채널을 찾을 수 없습니다." )
            return

        if CLIENT.user not in voiceChannel.members:
            await msg.reply( "봇이 음성 채널에 연결되어 있지 않습니다." )
            return
        
        await VC.disconnect()
        await msg.reply( "disconnect" )


async def playAudio( audio ):
    if VC is None:
        print( "오디오를 재생할 음성 채널을 찾을 수 없습니다." )
        return

    while VC.is_connected():
        radio: list[ tuple[ str, float ] ] = RADIO.next()    # type: ignore

        for curr in radio:
            src, time = curr
            VC.play( discord.FFmpegPCMAudio( executable = FFMPEG_PATH , source = src ) )
            await asyncio.sleep( time + 2.0 )
    
    VC.stop()
    
    # await VC.disconnect()


load_dotenv( "../.env" )
TOKEN = os.environ.get( "WMEW_TOKEN" )

if TOKEN is None:
    raise Exception( "Token Unavailable!" )
else:
    CLIENT.run( TOKEN )