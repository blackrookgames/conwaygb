INCLUDE "const.inc"



SECTION "Sample", ROM0

    sample::
        ; Clear current design
        call draw_clear
        ; Get input address
        ld a, [sample_hi]
        ld d, a
        ld a, [sample_lo]
        ld e, a
        ; Load
        .load:
            ld hl, draw_area
            ; Columns
            ld c, AREA_H - 1
            .load_y:
                ; Rows
                ld b, (AREA_W - 1) / 2
                .load_x:
                    ; Input bytes represent 4x2 cells:
                    ; ABEF
                    ; CDGH
                    MACRO sample_load_cell 
                        .load_x_\@:
                            ld a, [de]
                            bit \1, a
                            jr z, .load_x_\@__end
                            ld a, [hl]
                            or a, \2
                            ld [hl], a
                            .load_x_\@__end:
                    ENDM
                    ; 0, 0
                    sample_load_cell 0, %00001000
                    inc hl
                    ; 1, 0
                    sample_load_cell 1, %00000100
                    ; 2, 0
                    sample_load_cell 4, %00001000
                    inc hl
                    ; 3, 0
                    sample_load_cell 5, %00000100
                    ; Cells in other row
                    push hl
                        ld a, l
                        add a, AREA_W - 2
                        ld l, a
                        ld a, h
                        adc a, 0
                        ld h, a
                        ; 0, 1
                        sample_load_cell 2, %00000010
                        inc hl
                        ; 1, 1
                        sample_load_cell 3, %00000001
                        ; 2, 1
                        sample_load_cell 6, %00000010
                        inc hl
                        ; 3, 1
                        sample_load_cell 7, %00000001
                    pop hl
                    ; Next byte
                    inc de
                    ; Next
                    dec b
                    jr nz, .load_x
                ; Next row
                inc hl
                ; Next
                dec c
                jr nz, .load_y
        ; Goto draw
        jp draw



SECTION "Samples", ROM0
    ; Sample 0
    sample_0::
        INCBIN "sample0.bin"
    sample_0_end::
    ; Sample 1
    sample_1::
        INCBIN "sample1.bin"
    sample_1_end::
    ; Sample 2
    sample_2::
        INCBIN "sample2.bin"
    sample_2_end::
    ; Sample 3
    sample_3::
        INCBIN "sample3.bin"
    sample_3_end::
    ; Sample 4
    sample_4::
        INCBIN "sample4.bin"
    sample_4_end::
    ; Sample 5
    sample_5::
        INCBIN "sample5.bin"
    sample_5_end::



SECTION "Sample WRAM", WRAM0
    sample_lo:: db
    sample_hi:: db