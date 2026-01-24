INCLUDE "const.inc"



SECTION "Play", ROM0

    play_init::
        ; Setup tile routine
        .troutine:
            ld hl, play_troutine
            ld de, play_troutinesrc
            ld b, play_troutinesrc_end - play_troutinesrc
            .troutine_loop:
                ; Copy byte
                ld a, [de]
                ld [hli], a
                inc de
                ; Next
                dec b
                jr nz, .troutine_loop

    play::
        ; Reset "previous"
        .setcurr:
            ld hl, play_area1
            ld de, testarea
            ; Rows
            ld c, AREA_H
            .setcurr_y:
                ; Columns
                ld b, AREA_W
                .setcurr_x:
                    ; Copy byte
                    ld a, [de]
                    ld [hli], a
                    inc de
                    ; Next
                    dec b
                    jr nz, .setcurr_x
                ; Next
                dec c
                jr nz, .setcurr_y
        ; Reset active
        .active:
            ld a, 0
            ld [play_area], a
            ld a, LOW(play_area0)
            ld [play_area_c_lo], a
            ld a, HIGH(play_area0)
            ld [play_area_c_hi], a
            ld a, LOW(play_area1)
            ld [play_area_p_lo], a
            ld a, HIGH(play_area1)
            ld [play_area_p_hi], a

    play_loop:
        ; Update area
        .area:
            ; Clear 1st row and column
            .area_clr:
                ld a, [play_area_c_hi]
                ld d, a
                ld a, [play_area_c_lo]
                ld e, a
                ld a, 0
                ; Clear first row
                ld h, d
                ld l, e
                ld b, AREA_W
                .area_clr_row:
                    ; Set byte
                    ld [hli], a
                    ; Next
                    dec b
                    jr nz, .area_clr_row
                ; Clear first column
                ld h, d
                ld l, e
                ld d, 0
                ld e, AREA_W
                ld b, AREA_H
                .area_clr_col:
                    ; Set byte
                    ld [hl], a
                    ; Next row
                    add hl, de
                    ; Next
                    dec b
                    jr nz, .area_clr_col
            ; Update
            .area_fix:
                ld a, [play_area_p_hi]
                ld h, a
                ld a, [play_area_p_lo]
                ld l, a
                ld a, [play_area_c_hi]
                ld d, a
                ld a, [play_area_c_lo]
                ld e, a
                ; Rows
                ld c, AREA_H - 1 ; We won't pass thru the last
                .area_fix_row:
                    ; Columns
                    ld b, AREA_W - 1 ; We won't pass thru the last
                    .area_fix_col:
                        ; Update
                        push bc
                        push hl
                            ; Examine
                            .area_fix_col_exam:
                                push de
                                    ; TL
                                    ld a, [hl]
                                    swap a
                                    ld b, a
                                    ; TR
                                    inc hl
                                    ld a, [hl]
                                    or a, b
                                    ld b, a
                                    ; BL
                                    ld de, AREA_W - 1
                                    add hl, de
                                    ld a, [hl]
                                    swap a
                                    ld c, a
                                    ; BR
                                    inc hl
                                    ld a, [hl]
                                    or a, c
                                    ld c, a
                                pop de
                            ; Set values
                            .area_fix_col_set:
                                ld h, d
                                ld l, e
                                push de
                                    MACRO play_loop_area_fix_col_set_0
                                        ld a, 0
                                        ; Check neighbor in same tile
                                        .area_fix_col_set_\@_n1:
                                            bit \2, \1
                                            jr z, .area_fix_col_set_\@_n1_end
                                            inc a
                                            .area_fix_col_set_\@_n1_end:
                                        ; Check neighbor in same tile
                                        .area_fix_col_set_\@_n2:
                                            bit \3, \1
                                            jr z, .area_fix_col_set_\@_n2_end
                                            inc a
                                            .area_fix_col_set_\@_n2_end:
                                        ; Check neighbor in same tile
                                        .area_fix_col_set_\@_n3:
                                            bit \4, \1
                                            jr z, .area_fix_col_set_\@_n3_end
                                            inc a
                                            .area_fix_col_set_\@_n3_end:
                                        ; Check neighbor in adjacent tile
                                        .area_fix_col_set_\@_a1:
                                            bit \5, \1
                                            jr z, .area_fix_col_set_\@_a1_end
                                            inc a
                                            .area_fix_col_set_\@_a1_end:
                                        ; Check neighbor in adjacent tile
                                        .area_fix_col_set_\@_a2:
                                            bit \6, \1
                                            jr z, .area_fix_col_set_\@_a2_end
                                            inc a
                                            .area_fix_col_set_\@_a2_end:
                                    ENDM
                                    MACRO play_loop_area_fix_col_set_1
                                        ; Check neighbor below tile
                                        .area_fix_col_set_\@_b1:
                                            bit \2, \1
                                            jr z, .area_fix_col_set_\@_b1_end
                                            inc a
                                            .area_fix_col_set_\@_b1_end:
                                        ; Check neighbor below tile
                                        .area_fix_col_set_\@_b2:
                                            bit \3, \1
                                            jr z, .area_fix_col_set_\@_b2_end
                                            inc a
                                            .area_fix_col_set_\@_b2_end:
                                        ; Check neighbor below adjacent tile
                                        .area_fix_col_set_\@_ba:
                                            bit \4, \1
                                            jr z, .area_fix_col_set_\@_ba_end
                                            inc a
                                            .area_fix_col_set_\@_ba_end:
                                    ENDM
                                    MACRO play_loop_area_fix_col_set_2
                                        ; Live or die?
                                        .area_fix_col_set_\@_lod:
                                            ; Is the cell currently dead or alive?
                                            bit \2, \1
                                            jr nz, .area_fix_col_set_\@_lod_alive
                                            .area_fix_col_set_\@_lod_dead:
                                                ; Can cell be revived?
                                                cp a, 3
                                                jr z, .area_fix_col_set_\@_lod_survive
                                                jr .area_fix_col_set_\@_lod_end
                                            .area_fix_col_set_\@_lod_alive:
                                                ; Will cell survive?
                                                cp a, 2
                                                jr z, .area_fix_col_set_\@_lod_survive
                                                cp a, 3
                                                jr z, .area_fix_col_set_\@_lod_survive
                                                jr .area_fix_col_set_\@_lod_end
                                            .area_fix_col_set_\@_lod_survive:
                                                ; Cell will live!
                                                ld a, [hl]
                                                or a, \3
                                                ld [hl], a
                                            .area_fix_col_set_\@_lod_end:
                                    ENDM
                                    ; TL
                                    play_loop_area_fix_col_set_0 b, 4, 5, 6, 0, 2
                                    play_loop_area_fix_col_set_1 c, 4, 5, 0
                                    play_loop_area_fix_col_set_2 b, 7, %00001000
                                    ; TR
                                    inc hl
                                    play_loop_area_fix_col_set_0 b, 0, 1, 3, 5, 7
                                    play_loop_area_fix_col_set_1 c, 0, 1, 5
                                    play_loop_area_fix_col_set_2 b, 2, %00000100
                                    ; BL
                                    ld de, AREA_W - 1
                                    add hl, de
                                    play_loop_area_fix_col_set_0 c, 4, 6, 7, 0, 2
                                    play_loop_area_fix_col_set_1 b, 6, 7, 2
                                    play_loop_area_fix_col_set_2 c, 5, %00000010
                                    ; BR
                                    inc hl
                                    ld [hl], 0
                                    play_loop_area_fix_col_set_0 c, 1, 2, 3, 5, 7
                                    play_loop_area_fix_col_set_1 b, 2, 3, 7
                                    play_loop_area_fix_col_set_2 c, 0, %00000001
                                pop de
                        pop hl
                        pop bc
                        ; Next column
                        inc hl
                        inc de
                        ; Next
                        dec b
                        jp nz, .area_fix_col
                    ; Next row
                    inc hl
                    inc de
                    ; Next
                    dec c
                    jp nz, .area_fix_row


        ; Update tiles
        .tiles:
            ld a, [play_area_c_hi]
            ld h, a
            ld a, [play_area_c_lo]
            ld l, a
            ; Rows
            ld de, VR_9800
            ld c, AREA_H
            .tiles_y:
                ld a, h
                ld b, l
                ld hl, play_troutine + 1
                ; Set VRAM address
                ld [hl], e
                inc hl
                ld [hl], d
                inc hl
                ; Columns
                push de
                    ; Loop
                    ld d, a
                    ld e, b
                    ld b, AREA_W
                    .tiles_x:
                        ; Copy byte
                        inc hl
                        ld a, [de]
                        ld [hli], a
                        inc hl
                        inc de
                        ; Next
                        dec b
                        jr nz, .tiles_x
                    ; Execute
                    .tiles_y_exe:
                        ; Wait
                        ld hl, LCD_STAT
                    .tiles_y_exe__wait:
                        bit 1, [hl] ; Mode 0 or 1
                        jr nz, .tiles_y_exe__wait
                        ; VBlank
                    .tiles_y_exe__vb:
                        ld a, [LCD_Y]
                        cp VBLANK
                        jp c, .tiles_y_exe__vb
                        ; Execute
                        call play_troutine
                    ; Next input row
                    ld h, d
                    ld l, e
                pop de
                ; Next output row
                ld a, e
                add a, 32
                ld e, a
                ld a, d
                adc a, 0
                ld d, a
                ; Next
                dec c
                jr nz, .tiles_y
        ; Next active
        .nextarea:
            ; Update previous
            ld a, [play_area_c_lo]
            ld [play_area_p_lo], a
            ld a, [play_area_c_hi]
            ld [play_area_p_hi], a
            ; Update current
            ld a, [play_area]
            xor a, $01
            ld [play_area], a
            jr nz, .nextarea_1
            .nextarea_0:
                ld a, LOW(play_area0)
                ld [play_area_c_lo], a
                ld a, HIGH(play_area0)
                ld [play_area_c_hi], a
                jr .nextarea_end
            .nextarea_1:
                ld a, LOW(play_area1)
                ld [play_area_c_lo], a
                ld a, HIGH(play_area1)
                ld [play_area_c_hi], a
            .nextarea_end:
        ; Loop
        jp play_loop



SECTION "Play WRAM", WRAM0
    play_area: db
    play_area_p_lo: db
    play_area_p_hi: db
    play_area_c_lo: db
    play_area_c_hi: db
    ; Play area 0
    play_area0:
        ds AREA_W * AREA_H
    play_area0_end:
    ; Play area 1
    play_area1:
        ds AREA_W * AREA_H
    play_area1_end:



SECTION "Play Test Area", ROM0
INCLUDE "testarea.inc"



SECTION "Play Tile Routine Source", ROM0
    play_troutinesrc:
        ld hl, $0000
        ld [hl], $00
REPT SCR_W
        inc hl
        ld [hl], $00
ENDR
        ret
    play_troutinesrc_end:



SECTION "Play Tile Routine", WRAMX
    play_troutine:
        ds play_troutinesrc_end - play_troutinesrc