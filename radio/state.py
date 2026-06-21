import os
from enum import IntEnum


class State( IntEnum ):
    BEGIN = 0
    SONG = 1
    INTRO = 2
    OUTRO = 3
    TRANSITIONAL = 4
    COMM_INTRO = 5
    COMM = 6
    SEGMENT = 7
    CALL_LETTER = 8


NEXT = {
    State.BEGIN: ( State.CALL_LETTER,
                   State.INTRO,
                   State.TRANSITIONAL,
                   State.COMM_INTRO,
                   State.SEGMENT,
                   State.CALL_LETTER,
                   State.SONG,
                   State.SONG ),

    State.SONG: ( State.INTRO,
                  State.OUTRO,
                  State.TRANSITIONAL,
                  State.COMM_INTRO,
                  State.SEGMENT,
                  State.CALL_LETTER,
                  State.SONG,
                  State.SONG ),

    State.INTRO: ( State.SONG, ),

    State.OUTRO: ( State.SONG, ),

    State.TRANSITIONAL: ( State.INTRO, State.SONG, State.SONG ),
    
    State.COMM_INTRO: ( State.COMM, ),

    State.COMM: ( State.INTRO, State.SONG, State.CALL_LETTER ),

    State.SEGMENT: ( State.INTRO, State.SONG, State.CALL_LETTER ),

    State.CALL_LETTER: ( State.INTRO, State.SONG )
}


AUDIO_PATH = {
    State.BEGIN: "./radio/gamestart_intros",

    State.SONG: "./radio/songs",

    State.INTRO: "./radio/intros",

    State.OUTRO: "./radio/outros",

    State.TRANSITIONAL: "./radio/transitionals",

    State.COMM_INTRO: "./radio/commercialbreak",

    State.COMM: "./radio/commercials",

    State.SEGMENT: "./radio/segments",

    State.CALL_LETTER: "./radio/call_letters"

}