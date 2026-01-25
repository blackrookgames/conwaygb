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
        ; Read input
        .rep_input\@:
            ld c, \3
            call menu_input
            ; Back to drawing?
            bit IN_SELECT, b
            jp z, \4
            bit IN_B, b
            jp z, \4
            ; Select item?
            bit IN_START, b
            jp z, \5
            bit IN_A, b
            jp z, \5
            ; End of input
            .rep_input__end:
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

    MACRO menu_ctrl
        ; Load menu
        ld de, \1
        call menu_load
        ; "Hide" cursor
        ld a, 0
        ld b, 0
        call menu_updatecursor
        ; Loop
        .rep\@:
            ; Read input
            .rep\@_input:
                call input_read
                ; Previous?
                bit IN_SELECT, a
                jp z, \2
                bit IN_B, a
                jp z, \2
                ; Next?
                bit IN_START, a
                jp z, \3
                bit IN_A, a
                jp z, \3
            ; VBlank
            .rep\@_vblank:
                ld a, [LCD_Y]
                cp VBLANK
                jp c, .rep\@_vblank
            ; OAM
            .rep\@_oam:
                ld a, HIGH(oam_buffer)
                call oam_dma
            ; Loop
            jp .rep\@
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
            menu_common MENU_0_X, MENU_0_Y, 3, draw, .select
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
                ; Prompt to confirm clearing screen
                jp menu_1
                ; End clear
                .select_clear__end:
            .select_sample:
                cp a, 2
                jr nz, .select_sample__end
                ; TODO: Goto Samples menu
                jp menu_0
                ; End sample
                .select_sample__end:
            .select_ctrl:
                cp a, 3
                jr nz, .select_ctrl__end
                ; Goto Controls screen
                jp menu_ctrl0
                ; End about
                .select_ctrl__end:
            jp menu_0
    
    menu_1:
        ; Load menu
        ld de, menu_1_map
        call menu_load
        ; Set cursor
        ld a, 0
        ld [menu_sel], a
        ; Loop
        .rep:
            menu_common MENU_1_X, MENU_1_Y, 1, menu_0, .select
            jp .rep
        ; Select
        .select:
            ld a, [menu_sel]
            .select_y:
                cp a, 0
                jr nz, .select_y__end
                ; Clear design
                .select_y_cls:
                    ld hl, draw_area
                    ld a, 0
                    ; Row
                    ld c, AREA_H
                    .select_y_cls_y:
                        ; Columns
                        ld b, AREA_W
                        .select_y_cls_x:
                            ; Clear byte
                            ld [hli], a
                            ; Next
                            dec b
                            jr nz, .select_y_cls_x
                        ; Next
                        dec c
                        jr nz, .select_y_cls_y
                ; Goto draw screen
                jp draw
                ; End yes
                .select_y__end:
            .select_n:
                cp a, 1
                jr nz, .select_n__end
                ; Return to main menu
                jp menu_0
                ; End no
                .select_n__end:
            jp menu_1
    
    menu_ctrl0:
        menu_ctrl menu_ctrl0_map, menu_0, menu_ctrl1
    
    menu_ctrl1:
        menu_ctrl menu_ctrl1_map, menu_ctrl0, menu_0


SECTION "Menu Menus", ROM0
    ; Menu 0
    DEF MENU_0_X EQU 5
    DEF MENU_0_Y EQU 6
    menu_0_map:
        INCBIN "menu0.bin"
    menu_0_map_end:
    ; Menu 1
    DEF MENU_1_X EQU 7
    DEF MENU_1_Y EQU 6
    menu_1_map:
        INCBIN "menu1.bin"
    menu_1_map_end:
    ; Menu 2
    DEF MENU_2_X EQU 7
    DEF MENU_2_Y EQU 6
    menu_2_map:
        INCBIN "menu2.bin"
    menu_2_map_end:
    ; Menu Ctrl 0
    menu_ctrl0_map:
        INCBIN "menu_ctrl0.bin"
    menu_ctrl0_map_end:
    ; Menu Ctrl 1
    menu_ctrl1_map:
        INCBIN "menu_ctrl1.bin"
    menu_ctrl1_map_end:


SECTION "Menu WRAM", WRAM0
    menu_sel: db
    menu_max: db
    menu_0_sel: db