INCLUDE "const.inc"



SECTION "Input", ROM0

    ; Waits till to no buttons are being pressed
    ; Modified: a
    input_wait::
        call input_read
        cp a, $FF
        jr nz, input_wait
        ret


    
    ; Reads joypad input
    ; Modified: a, b
    ; Return: a
    input_read::
        ; Update previous
        ld a, [input_curr]
        ld [input_prev], a
        ; Read dpad
        ld a, JP_DPAD
        call .nibble
        and a, %00001111
        ld b, a
        ; Read buttons
        ld a, JP_BTNS
        call .nibble
        and a, %00001111
        ; Combine nibbles
        swap a
        or a, b
        ; Update current
        ld [input_curr], a
        ; Success!!!
        ret
        ; Nibble reader
        .nibble:
            ld [JOYPAD], a ; switch the key nibble
            call .nibble__ret ; burn 10 cycles calling a known ret
            ldh a, [JOYPAD] ; ignore value while waiting for the key nibble to settle
            ldh a, [JOYPAD]
            ldh a, [JOYPAD] ; this read counts
            .nibble__ret:
            ret



SECTION "Input WRAM", WRAM0
    input_curr:: db
    input_prev:: db