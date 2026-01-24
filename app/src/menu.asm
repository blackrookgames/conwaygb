INCLUDE "const.inc"



SECTION "Menu", ROM0

    menu_init::
        ret

    ; Input: d, e
    ; Modified a, b, c, d, e, h, l
    menu_load:
        call input_wait
        ; Turn off LCD
        call help_lcd_off
        ; Set tiles
        tiles:
            ld hl, VR_9800
            ; Rows
            ld c, SCR_H
            .tiles_y:
                ; Columns
                ld b, SCR_W
                .tiles_x:
                    ; Copy byte
                    ld a, [de]
                    ld [hli], a
                    inc de
                    ; Next
                    dec b
                    jr nz, .tiles_x
                ; Next row
                ld a, l
                add a, TMAP_DIM - SCR_W
                ld l, a
                ld a, h
                adc a, 0
                ld h, a
                ; Next
                dec c
                jr nz, .tiles_y
        ; Initialize cursor
        .cursor:
            ld a, 0
            ld [menu_y], a
        ; Turn on LCD
        .lcdon:
            ld a, %10000011
            ld [LCD_CTRL], a
        ; Return
        ret

    menu::
        ; Setup sprite
        .sprite:
            ld a, 1
            ld [oam_buffer + 2], a
        ; Load menu
        .load:
            ld de, menu_0
            call menu_load
        ; Set scrolling
        .scroll:
            ld a, 0
            ld [SCR_BX], a
            ld [SCR_BY], a
        

    menu_loop:
        ; Read input
        .input:
            .input_read:
                call input_read
                ld b, a
                ld a, [input_prev]
                ; Back to drawing?
                bit IN_SELECT, b
                jp z, draw
                bit IN_B, b
                jp z, draw
                ; Select item?
                bit IN_START, b
                jp z, .input_select
                bit IN_A, b
                jp z, .input_select
                ; No input
                jp .input__end
            .input_select:
                ; pass
            .input__end:
        ; Update cursor
        .cursor:
            ld hl, oam_buffer
            ; Y-position
            ld a, [menu_y]
            add a, 4
            sla a
            sla a
            sla a
            ld [hli], a
            ; X-position
            ld a, 3
            sla a
            sla a
            sla a
            ld [hl], a
        ; VBlank
        .vblank:
            ld a, [LCD_Y]
            cp VBLANK
            jp c, .vblank
        ; OAM
        .oam:
            ld a, HIGH(oam_buffer)
            call oam_dma
        ; Loop
        jp menu_loop



SECTION "Menu Menus", ROM0
    menu_0:
        db $00, $01, $02, $03, $04, $05, $06, $07, $08, $09, $0A, $0B, $0C, $0D, $0E, $0F, $10, $11, $12, $13
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
    menu_0_end:


SECTION "Menu WRAM", WRAM0
    menu_y: db