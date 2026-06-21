import os


INTRO: list[ str ] = []

for intro in os.listdir( "./radio/intros" ):
    INTRO.append( intro )


OUTRO: list[ str ] = []

for outro in os.listdir( "./radio/outros" ):
    OUTRO.append( outro )