INCLUDE "const.inc"



DEF DRAW_DIR_MIN EQU 15
DEF DRAW_DIR_MAX EQU 20



SECTION "Draw", ROM0

    draw_init::
        ; Initialize cursor
        .cursor:
            ld a, 2
            ld [draw_x], a
            ld [draw_y], a
        ; Initialize tile
        .tile:
            ld a, $10 ; >= $10 will indicate no tile needs to be updated
            ld [draw_tile], a
        ; Reset area
        .area:
            ld hl, draw_area
            ld a, 0
            ; Rows
            ld c, AREA_H
            .area_y:
                ; Columns
                ld b, AREA_W
                .area_x:
                    ; Clear byte
                    ld [hli], a
                    ; Next
                    dec b
                    jr nz, .area_x
                ; Next
                dec c
                jr nz, .area_y
        ; Return
        ret

    ; Modified: a, b, c, h, l
    draw_clear::
        ld hl, draw_area
        ld a, 0
        ; Row
        ld c, AREA_H
        .clr_y:
            ; Columns
            ld b, AREA_W
            .clr_x:
                ; Clear byte
                ld [hli], a
                ; Next
                dec b
                jr nz, .clr_x
            ; Next
            dec c
            jr nz, .clr_y
        ; Return
        ret

    ; Modified: a, d, e, h, l
    ; Return: a, h, l
    draw_gettile:
        ld hl, draw_area
        ld d, 0
        ; Y
        .y:
            ; + ((draw_y + 1) >> 1)
            ld a, [draw_y]
            inc a
            ld e, a
            sra e
            add hl, de
            ; + ((draw_y + 1) >> 1) * 20
            sla e
            sla e
            add hl, de
            add hl, de
            add hl, de
            add hl, de
            add hl, de
        ; X
        .x:
            ; + ((draw_x + 1) >> 1)
            ld a, [draw_x]
            inc a
            ld e, a
            sra e
            add hl, de
        ; Return
        ld a, [hl]
        ret

    ; Modified: a, b
    ; Return: a
    draw_getbit:
        ld b, %00000001
        ; Y
        .y:
            ld a, [draw_y]
            and a, %00000001
            jr nz, .x
            sla b
            sla b
        ; Draw X
        .x:
            ld a, [draw_x]
            and a, %00000001
            jr nz, .return
            sla b
        ; Return
        .return:
            ld a, b
            ret
    
    ; Modified: a, d, e, h, l, draw_tile_hi, draw_tile_lo
    draw_vrampos:
        ld hl, VR_9800
        ld d, 0
        ; Y
        .y:
            ; + ((draw_y + 1) >> 1) * 32
            ld a, [draw_y]
            inc a
            and a, %11111110
            ld e, a
            sla e
            sla e
            add hl, de
            add hl, de
            add hl, de
            add hl, de
        ; X
        .x:
            ; + ((draw_x + 1) >> 1)
            ld a, [draw_x]
            inc a
            ld e, a
            sra e
            add hl, de
        ; Set address
        ld a, h
        ld [draw_tile_hi], a
        ld a, l
        ld [draw_tile_lo], a
        ; Return
        ret

    draw::
        call input_wait
        ; Turn off LCD
        call help_lcd_off
        ; Set tiles
        .tiles:
        ; Clear area
        .area:
            ld hl, VR_9800
            ld de, draw_area
            ld a, 0
            ; Rows
            ld c, AREA_H
            .area_y:
                ; Columns
                ld b, AREA_W
                .area_x:
                    ; Clear byte
                    ld a, [de]
                    ld [hli], a
                    inc de
                    ; Next
                    dec b
                    jr nz, .area_x
                ; Next row
                ld a, l
                add a, TMAP_DIM - AREA_W
                ld l, a
                ld a, h
                adc a, 0
                ld h, a
                ; Next
                dec c
                jr nz, .area_y
        ; Setup sprite
        .sprite:
            ld a, 0
            ld [oam_buffer + 2], a
        ; Set scrolling
        .scroll:
            ld a, 4
            ld [SCR_BX], a
            ld [SCR_BY], a
        ; Turn on LCD
        .lcdon:
            ld a, %10000011
            ld [LCD_CTRL], a
        ; Reset directional input
        .dir:
            ld a, 0
            ld [draw_dir], a
            ld [draw_dir_t], a

    draw_loop:
        ; Read input
        .input:
            call input_read
            ; Directional?
            .input_dir:
                ; Get directional input
                .input_dir_chk:
                    MACRO draw_loop_input_dir_chk
                        .input_dir_chk_\@:
                            ; Check input
                            bit \1, a
                            jr nz, .input_dir_chk_\@__end
                            ; Set direction
                            ld a, \2
                            ; End
                            jr .input_dir_chk__end
                            .input_dir_chk_\@__end:
                    ENDM
                    ; Right?
                    draw_loop_input_dir_chk IN_DP_R, $00
                    ; Up?
                    draw_loop_input_dir_chk IN_DP_U, $01
                    ; Left?
                    draw_loop_input_dir_chk IN_DP_L, $02
                    ; Down?
                    draw_loop_input_dir_chk IN_DP_D, $03
                    ; None
                    ld a, $FF
                    ld [draw_dir], a
                    ld [draw_dir_t], a
                    jp .input_dir__end
                    ; End of directional input
                    .input_dir_chk__end:
                ; Check repeat
                .input_dir_rpt:
                    ld b, a
                    ld a, [draw_dir]
                    ; New direction?
                    .input_dir_rpt_new:
                        cp a, b
                        jr z, .input_dir_rpt_new__end
                        ; Set repeat
                        ld a, 0
                        ld [draw_dir_t], a
                        ; Set direction
                        ld a, b
                        ld [draw_dir], a
                        ; End of new direction
                        jr .input_dir_rpt__end
                        .input_dir_rpt_new__end:
                    ; Repeating direction?
                    .input_dir_rpt_rpt:
                        ; Inc repeat
                        ld a, [draw_dir_t]
                        inc a
                        ; Min repeat?
                        .input_dir_rpt_rpt_min:
                            cp a, DRAW_DIR_MIN
                            jr nz, .input_dir_rpt_rpt_min__end
                            ; Update repeat
                            ld [draw_dir_t], a
                            ; Set direction
                            jr .input_dir_rpt_rpt_set
                            ; End of min repeat
                            .input_dir_rpt_rpt_min__end:
                        ; Max repeat?
                        .input_dir_rpt_rpt_max:
                            cp a, DRAW_DIR_MAX
                            jr nz, .input_dir_rpt_rpt_max__end
                            ; Update repeat
                            ld a, DRAW_DIR_MIN
                            ld [draw_dir_t], a
                            ; Set direction
                            jr .input_dir_rpt_rpt_set
                            ; End of min repeat
                            .input_dir_rpt_rpt_max__end:
                        ; No direction
                        ld [draw_dir_t], a
                        jr .input_dir_rpt_rpt__end
                        ; Set direction
                        .input_dir_rpt_rpt_set:
                            ld a, b
                        ; End of repeating direction
                        jr .input_dir_rpt__end
                        .input_dir_rpt_rpt__end:
                    ; Cancel
                    ld a, $FF
                    ; End of check repeat
                    .input_dir_rpt__end:
                ; Move cursor
                .input_dir_move:
                    MACRO draw_loop_input_dir_move
                        .input_dir_move_\@:
                            ; Check direction
                            cp a, \1
                            jp nz, .input_dir_move_\@__end
                            ; Check bound
                            ld a, [\2]
                            cp a, \3
                            jp z, .input_dir_move__end
                            ; Inc/dec
                            \4 a
                            ld [\2], a
                            ; End
                            jr .input_dir_move__end
                            .input_dir_move_\@__end:
                    ENDM
                    ; Right
                    draw_loop_input_dir_move $00, draw_x, SCR_W * 2 - 1, inc
                    ; Up
                    draw_loop_input_dir_move $01, draw_y, 0, dec
                    ; Left
                    draw_loop_input_dir_move $02, draw_x, 0, dec
                    ; Down
                    draw_loop_input_dir_move $03, draw_y, SCR_H * 2 - 1, inc
                    ; End of move
                    .input_dir_move__end:
                ; End of directional
                .input_dir__end:
            .input_action:
                ld a, [input_curr]
                ; Set cell?
                .input_action_setcell:
                    ; Check input
                    bit IN_A, a
                    jr nz, .input_action_setcell__end
                    ; Get tile
                    call draw_gettile
                    ; Set bit
                    ld c, a
                    call draw_getbit
                    or a, c
                    ld [draw_tile], a
                    ld [hl], a
                    ; Get output address
                    call draw_vrampos
                    ; End of set cell
                    jp .input_action__end
                    .input_action_setcell__end:
                ; Clear cell?
                .input_action_clrcell:
                    ; Check input
                    bit IN_B, a
                    jr nz, .input_action_clrcell__end
                    ; Get tile
                    call draw_gettile
                    ; Clear bit
                    ld c, a
                    call draw_getbit
                    xor a, %11111111
                    and a, c
                    ld [draw_tile], a
                    ld [hl], a
                    ; Get output address
                    call draw_vrampos
                    ; End of clear cell
                    jp .input_action__end
                    .input_action_clrcell__end:
                ; Start simulation?
                .input_action_sim:
                    ; Check input
                    bit IN_START, a
                    jr nz, .input_action_sim__end
                    ; Start simulation
                    jp play
                    ; End of start simulation
                    .input_action_sim__end:
                ; Display menu?
                .input_action_menu:
                    ; Check input
                    bit IN_SELECT, a
                    jr nz, .input_action_menu__end
                    ; Display menu
                    jp menu
                    ; End of display menu
                    .input_action_menu__end:
                ; End of action
                .input_action__end:
            ; End of input
            .input__end:
        ; Update cursor
        .cursor:
            ld hl, oam_buffer
            ; Y-position
            ld a, [draw_y]
            sla a
            sla a
            add a, 14
            ld [hli], a
            ; X-position
            ld a, [draw_x]
            sla a
            sla a
            add a, 6
            ld [hl], a
        ; Draw tile
        .drawtile:
            ; Wait
            ld hl, LCD_STAT
            .drawtile__wait:
            bit 1, [hl] ; Mode 0 or 1
            jr nz, .drawtile__wait
            ; VBlank
            .drawtile__vb:
            ld a, [LCD_Y]
            cp VBLANK
            jp c, .drawtile__vb
            ; Draw
            .drawtile_draw:
                ; Does a tile need to be drawn?
                ld a, [draw_tile]
                cp a, $10
                jr nc, .drawtile_draw__end
                ; Yes! Now draw.
                ld b, a
                ld a, [draw_tile_hi]
                ld h, a
                ld a, [draw_tile_lo]
                ld l, a
                ld [hl], b
                ; Reset tile
                ld a, $10
                ld [draw_tile], a
                ; End of draw
                .drawtile_draw__end:
        ; OAM
        .oam:
            ld a, HIGH(oam_buffer)
            call oam_dma
        ; Loop
        jp draw_loop



SECTION "Draw WRAM", WRAM0
    draw_x: db
    draw_y: db
    draw_tile: db
    draw_tile_lo: db
    draw_tile_hi: db
    draw_dir: db
    draw_dir_t: db
    ; Draw area
    draw_area::
        ds AREA_W * AREA_H
    draw_area_end::