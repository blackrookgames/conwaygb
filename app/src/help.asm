INCLUDE "const.inc"



SECTION "Help", ROM0

    ; Safely turns off the LCD
    ; modified: a
    help_lcd_off::
        ; Check if LCD is already off
        ld a, [LCD_CTRL]
        bit 7, a
        jr z, .return
        ; VBlank
        .vblank:
        ld a, [LCD_Y]
        cp VBLANK
        jr c, .vblank
        ; Turn off LCD
        ld a, %00000000
        ld [LCD_CTRL], a
        ; Return
        .return:
        ret
    
    ; Clears all tiles
    ; modified a, b, c, h, l
    help_cls::
        ld hl, VR_9800
        ld a, 0
        ; Rows
        ld c, TMAP_DIM
        .y:
            ; Columns
            ld b, TMAP_DIM
            .x:
                ; Clear byte
                ld [hli], a
                ; Next
                dec b
                jr nz, .x
            ; Next
            dec c
            jr nz, .y
        ; Return
        ret