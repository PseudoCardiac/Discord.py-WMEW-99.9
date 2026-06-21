from random import choice
from playlist import Playlist
from state import State, NEXT
from pygame import mixer
from time import sleep


mixer.init()
PADDING_TIME = 0


class Radio:
    def __init__( self ):
        self.state = State.BEGIN

        self.playlist = {
            State.SONG: Playlist( State.SONG ),
            State.TRANSITIONAL: Playlist( State.TRANSITIONAL ),
            State.COMM_INTRO: Playlist( State.COMM_INTRO ),
            State.COMM: Playlist( State.COMM ),
            State.SEGMENT: Playlist( State.SEGMENT ),
            State.CALL_LETTER: Playlist( State.CALL_LETTER ) 
        }


    def play( self ):
        # 인트로 다음 음악을 연달아 재생
        if self.state == State.INTRO:
            self.nextState()     # 반드시 song
            song = mixer.Sound( self.playlist[ self.state ].nowPlaying() )
            
            try:
                intro = mixer.Sound( self.playlist[ self.state ].getIntro() )
                intro.play()
                sleep( intro.get_length() + PADDING_TIME )
            except TypeError:
                print( f"{'[INTRO]':<15}!SKIPPED DUE TO NO INTRO!" )


            self.printLog()
            song.play()
            sleep( song.get_length() + PADDING_TIME )

        # nowPlaying 호출 전, 직전 재생된 음악의 아우트로를 재생
        elif self.state == State.OUTRO:
            try:
                outro = mixer.Sound( self.playlist[ State.SONG ].getOutro() )
                outro.play()
                sleep( outro.get_length() + PADDING_TIME )
            except TypeError:
                print( f"{'[OUTRO]':<15}!SKIPPED DUE TO NO OUTRO!" )

        else:
            audio = mixer.Sound( self.playlist[ self.state ].nowPlaying() )
            self.printLog()
            audio.play()
            sleep( audio.get_length() + PADDING_TIME )


    def nextState( self ):
        self.state = choice( NEXT[ self.state ] )


    def printLog( self ):
        print( f"{'['+self.state.name+']':<15}{ self.playlist[ self.state ].songName[ :-4 ] }" )


    def loop( self ):
        while True:
            self.nextState()
            self.play()