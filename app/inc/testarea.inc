IF !DEF(_TESTAREA_INC)
DEF _TESTAREA_INC EQU 1

testarea:
INCBIN "testarea.bin"
testarea_end:

ENDC
