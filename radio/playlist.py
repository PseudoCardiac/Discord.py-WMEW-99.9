import os, re
from random import sample
from state import State, AUDIO_PATH
from intro_outro import INTRO, OUTRO
from random import choice


# 뒤섞인 사본을 반환
def shuffle( l ):
    return sample( l, k = len( l ) )


class Playlist:
    def __init__( self, state: State ):
        self.state = state
        self.list = shuffle( os.listdir( AUDIO_PATH[ self.state ] ) )


    def nowPlaying( self ):
        if not self.list:
            self.reshuffle()

        self.songName = self.list.pop()
        return AUDIO_PATH[ self.state ] + '/' + self.songName
    

    def getIntro( self ):
        if self.state != State.SONG: raise Exception( "오류: 음악 이외의 오디오의 인트로를 취득하려고 시도함!" )
        
        intros = []

        title = self.songName[:-4]
        for intro in INTRO:
            if intro.startswith( title ):
                intros.append( AUDIO_PATH[ State.INTRO ] + '/' + intro )

        if not intros: 
            return None
        else:           
            result = choice( intros )
            print( f"{'[INTRO]':<15}{ result[ len( AUDIO_PATH[ State.INTRO ] ) + 1 : -4 ] }" )
            return result


    def getOutro( self ):
        if self.state != State.SONG: raise Exception( "오류: 음악 이외의 오디오의 아우트로를 취득하려고 시도함!" )
        
        outros = []

        title = self.songName[:-4]
        for outro in OUTRO:
            if outro.startswith( title ):
                outros.append( AUDIO_PATH[ State.OUTRO ] + '/' + outro )

        if not outros:  
            return None
        else:           
            result = choice( outros )
            print( f"{'[OUTRO]':<15}{ result[ len( AUDIO_PATH[ State.OUTRO ] ) + 1 : -4 ] }" )
            return result


    def reshuffle( self ):
        self.list = shuffle( os.listdir( AUDIO_PATH[ self.state ] ) )