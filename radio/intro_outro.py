import os


INTRO: list[ str ] = []

for intro in os.listdir( "./radio/radio/intros" ):
    INTRO.append( intro )


OUTRO: list[ str ] = []

for outro in os.listdir( "./radio/radio/outros" ):
    OUTRO.append( outro )