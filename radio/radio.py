from random import choice
from radio.playlist import Playlist
from radio.state import State, NEXT
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

            songSource = self.playlist[ self.state ].nowPlaying()
            song = mixer.Sound( songSource )
            
            try:
                introSource = self.playlist[ self.state ].getIntro()
                intro = mixer.Sound( introSource )
                # intro.play()
                introRunningtime = intro.get_length()
                # sleep( self.runningTime + PADDING_TIME )
            except TypeError:
                print( f"{'[INTRO]':<15}!SKIPPED DUE TO NO INTRO!" )
                introSource = None
                introRunningtime = 0.0

            self.printLog()
            # song.play()
            songRunningtime = song.get_length()
            # sleep( self.runningTime + PADDING_TIME )

            return [ ( introSource, introRunningtime ), ( songSource, songRunningtime ) ]

        # nowPlaying 호출 전, 직전 재생된 음악의 아우트로를 재생
        elif self.state == State.OUTRO:
            try:
                outroSource = self.playlist[ State.SONG ].getOutro()
                outro = mixer.Sound( outroSource )
                # outro.play()
                outroRunningtime = outro.get_length()
                # sleep( outro.get_length() + PADDING_TIME )
            except TypeError:
                print( f"{'[OUTRO]':<15}!SKIPPED DUE TO NO OUTRO!" )
                outroSource = None
                outroRunningtime = 0.0

            return [ ( outroSource, outroRunningtime ) ]


        else:
            audioSource = self.playlist[ self.state ].nowPlaying()
            audio = mixer.Sound( audioSource )
            self.printLog()
            # audio.play()
            runningtime = audio.get_length()
            # sleep( self.runningTime + PADDING_TIME )

            return [ ( audioSource, runningtime ) ]


    def nextState( self ):
        self.state = choice( NEXT[ self.state ] )


    def printLog( self ):
        print( f"{'['+self.state.name+']':<15}{ self.playlist[ self.state ].songName[ :-4 ] }" )


    def loop( self ):
        while True:
            self.nextState()
            self.play()


    def next( self ):
        self.nextState()
        return self.play()