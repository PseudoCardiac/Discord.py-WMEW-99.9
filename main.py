import discord, os, asyncio
from dotenv import load_dotenv
from radio.radio import Radio


INTENTS = discord.Intents.default()
INTENTS.message_content = True
CLIENT = discord.Client( intents=INTENTS )
TREE = discord.app_commands.CommandTree( CLIENT )

VC = None
RADIO_CHANNEL: discord.VoiceChannel = None      # type: ignore 
# RADIO_TEXT_CHANNEL: discord.TextChannel = None  # type: ignore
# FFMPEG_PATH = "C:/Users/nooye/Downloads/ffmpeg-8.1.1-essentials_build/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FFMPEG_PATH = "/usr/bin/ffmpeg"
RADIO = Radio()


@CLIENT.event
async def on_ready():
    global RADIO_CHANNEL
    # global RADIO_TEXT_CHANNEL
    # RADIO_CHANNEL = CLIENT.get_channel( 1022402805153153065 )      # type: ignore   # 테스트 서버 보이스
    # RADIO_TEXT_CHANNEL = CLIENT.get_channel( 1022402783485370398 ) # type: ignore   # 테스트 서버 텍스트
    RADIO_CHANNEL = CLIENT.get_channel( 1517897765659873290 )      # type: ignore   # 뮤제닉스 서버 보이스
    print( "WMEW 99.9 Currently Running On:" )
    print()
    for guild in CLIENT.guilds:
        print( f"{ guild.name } ({ str( guild.id ) })" )


@CLIENT.event
async def on_voice_state_update( member: discord.Member, before: discord.VoiceState, after: discord.VoiceState ):
    global VC

    isBotConnected = CLIENT.user in RADIO_CHANNEL.members
    onlyRadio = len( RADIO_CHANNEL.members ) == 1 and isBotConnected
    onlyPeople = len( RADIO_CHANNEL.members ) > 0 and not isBotConnected
    zeroPeople = len( RADIO_CHANNEL.members ) == 0
    radioAndPeople = len( RADIO_CHANNEL.members ) > 0 and isBotConnected

    if onlyRadio:
        if not isinstance( VC, discord.VoiceClient ):
            return  # something's wrong

        VC.stop()
        await VC.disconnect()   # type: ignore

    elif onlyPeople:
        VC = await RADIO_CHANNEL.connect()
        await playBeforeReady()
        await playAudio()

    elif zeroPeople:
        pass # do nothing (maybe a warning)

    elif radioAndPeople:
        pass # do nothing (maybe a welcome message)


async def playAudio():
    if VC is None:
        print( "오디오를 재생할 음성 채널을 찾을 수 없습니다." )
        return

    while VC.is_connected():
        radio: list[ str ] = RADIO.next()    # type: ignore

        for curr in radio:
            src = curr
            VC.play( discord.FFmpegOpusAudio( executable = FFMPEG_PATH , source = src,
                                              options = "-vn -c:a libopus -b:a 64k" ) )
            # await asyncio.sleep( time + 1.0 )
            while VC.is_playing():
                await asyncio.sleep( 1 )
    
    # await VC.disconnect()


async def playBeforeReady():
    if VC is None:
        print( "오디오를 재생할 음성 채널을 찾을 수 없습니다." )
        return

    print( "대기 메시지 송출" )
    VC.play( discord.FFmpegOpusAudio( executable = FFMPEG_PATH , source = "./radio/radio/before_ready.wav",
                                      options = "-vn -c:a libopus -b:a 64k" ) )

    while VC.is_playing():
        await asyncio.sleep( 1 )


load_dotenv( "../.env" )
TOKEN = os.environ.get( "WMEW_TOKEN" )

if TOKEN is None:
    raise Exception( "Token Unavailable!" )
else:
    CLIENT.run( TOKEN )