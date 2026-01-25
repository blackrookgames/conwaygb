INCLUDE "const.inc"



SECTION "Menu", ROM0

    menu_init::
        ret

    ; Input: d, e
    ; Modified: a, b, c, d, e, h, l
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
        ; Turn on LCD
        .lcdon:
            ld a, %10000011
            ld [LCD_CTRL], a
        ; Return
        ret

    ; Input: c
    ; Modified: a, b
    ; Return: a, b
    menu_input:
        call input_read
        ld b, a
        ld a, [input_prev]
        ; Prev?
        .prev:
            ; Check current input
            bit IN_DP_U, b
            jp nz, .prev__end
            ; Check previous input
            bit IN_DP_U, a
            jp z, .prev__end
            ; Clear current (to prevent input detection)
            ld b, $FF
            ; Check selected index
            ld a, [menu_sel]
            cp a, 0
            ret z
            ; Decrement selected index
            dec a
            ld [menu_sel], a
            ; Return
            ret
            ; End of prev
            .prev__end:
        ; Next?
        .next:
            ; Check current input
            bit IN_DP_D, b
            jp nz, .next__end
            ; Check previous input
            bit IN_DP_D, a
            jp z, .next__end
            ; Clear current (to prevent input detection)
            ld b, $FF
            ; Check selected index
            ld a, [menu_sel]
            cp a, c
            ret z
            ; Increment selected index
            inc a
            ld [menu_sel], a
            ; Return
            ret
            ; End of next
            .next__end:
        ; Return
        ret

    ; Input: a, b
    ; Modified a, h, l
    menu_updatecursor:
        ld hl, oam_buffer + 1
        ; X-position
        ld [hld], a
        ; Y-position
        ld a, [menu_sel]
        sla a
        sla a
        sla a
        sla a
        add a, b
        ld [hl], a
        ; Return
        ret

    MACRO menu_common
        ; Update cursor
        ld a, 8 + \1 * 8
        ld b, 16 + \2 * 8
        call menu_updatecursor
        ; VBlank
        .vblank\@:
            ld a, [LCD_Y]
            cp VBLANK
            jp c, .vblank\@
        ; OAM
        .oam\@:
            ld a, HIGH(oam_buffer)
            call oam_dma
    ENDM

    menu::
        call help_lcd_off
        ; Initialize cursor
        .cursor:
            ld a, 0
            ld [menu_sel], a
            ld [menu_0_sel], a
        ; Setup sprite
        .sprite:
            ld a, 1
            ld [oam_buffer + 2], a
        ; Set scrolling
        .scroll:
            ld a, 0
            ld [SCR_BX], a
            ld [SCR_BY], a
    
    menu_0:
        ; Load menu
        ld de, menu_0_map
        call menu_load
        ; Set cursor
        ld a, [menu_0_sel]
        ld [menu_sel], a
        ; Loop
        .rep:
            ; Read input
            .rep_input:
                ld c, 3
                call menu_input
                ; Back to drawing?
                bit IN_SELECT, b
                jp z, draw
                bit IN_B, b
                jp z, draw
                ; Select item?
                bit IN_START, b
                jp z, .select
                bit IN_A, b
                jp z, .select
                ; End of input
                .rep_input__end:
            ; Common
            menu_common MENU0_X, MENU0_Y
            jp .rep
        ; Select
        .select:
            ld a, [menu_sel]
            ld [menu_0_sel], a
            .select_create:
                cp a, 0
                jr nz, .select_create__end
                ; Goto draw screen
                jp draw
                ; End create
                .select_create__end:
            .select_clear:
                cp a, 1
                jr nz, .select_clear__end
                ; TODO: Prompt to clear
                jp menu_0
                ; End clear
                .select_clear__end:
            .select_sample:
                cp a, 2
                jr nz, .select_sample__end
                ; TODO: Goto Samples menu
                jp menu_0
                ; End sample
                .select_sample__end:
            .select_about:
                cp a, 3
                jr nz, .select_about__end
                ; TODO: Goto About screen
                jp menu_0
                ; End about
                .select_about__end:
            jp menu_0
    


SECTION "Menu Menus", ROM0
    ; Menu 0
    DEF MENU0_X EQU 5
    DEF MENU0_Y EQU 6
    menu_0_map:
        INCBIN "menu0.bin"
    menu_0_map_end:


SECTION "Menu WRAM", WRAM0
    menu_sel: db
    menu_max: db
    menu_0_sel: db