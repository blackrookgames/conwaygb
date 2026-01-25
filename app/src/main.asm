INCLUDE "const.inc"



SECTION "Program", ROM0[$100]
    jp init
    ds $150 - @, 0 ; Make room for header

    init:
        ; Shut down audio
        .audio:
            ld a, 0
            ld [SND_NR52], a
        ; Turn off LCD
        call help_lcd_off
        ; Initialize tileset
        .inittset:
            ld de, tset_end
            ld hl, VR_9000 + tset_end - tset
          .inittset__loop:
            ; Copy byte
            ld a, [de]
            ld [hld], a
            dec de
            ; Next
            ld a, l
            cp a, LOW(VR_9000 - 1)
            jr nz, .inittset__loop
            ld a, h
            cp a, HIGH(VR_9000 - 1)
            jr nz, .inittset__loop
        ; Initialize window tileset
        .initwset:
            ld de, tset_end
            ld hl, VR_9000 + tset_end - tset
          .initwset__loop:
            ; Copy byte
            ld a, [de]
            ld [hld], a
            dec de
            ; Next
            ld a, l
            cp a, LOW(VR_9000 - 1)
            jr nz, .initwset__loop
            ld a, h
            cp a, HIGH(VR_9000 - 1)
            jr nz, .initwset__loop
        ; Initialize sprite set
        .initsset:
            ld de, sset_end
            ld hl, VR_8000 + sset_end - sset
          .initsset__loop:
            ; Copy byte
            ld a, [de]
            ld [hld], a
            dec de
            ; Next
            ld a, l
            cp a, LOW(VR_8000 - 1)
            jr nz, .initsset__loop
            ld a, h
            cp a, HIGH(VR_8000 - 1)
            jr nz, .initsset__loop
        ; Initialize tilemap
        .inittmap:
            ld hl, VR_9800
            ld de, TMAP_DIM - SCR_W
            ; Loop thru rows
            ld b, SCR_H
            .inittmap_y:
                ; Loop thru columns
                ld c, SCR_W
                .inittmap_x:
                    ; Set byte to zero
                    ld a, 0
                    ld [hli], a
                    ; Next
                    dec c
                    jr nz, .inittmap_x
                ; Go to next row
                add hl, de
                ; Next
                dec b
                jr nz, .inittmap_y
        ; Initialize OAM
        .initoam:
            ; Clear
            .initoam_clr:
                ld a, 0
                ld b, oam_buffer_end - oam_buffer ; test
                ld hl, OAMRAM
                ld de, oam_buffer
              .initoam_clr__loop:
                ld [hli], a
                ld [de], a
                inc de
                dec b
                jp nz, .initoam_clr__loop
            ; Setup
            .initoam_set:
                ld hl, OAMRAM
                ld de, oam_buffer
                ; Y-position
                ld a, 14
                ld [hli], a
                ld [de], a
                inc de
                ; X-position
                ld a, 6
                ld [hli], a
                ld [de], a
                inc de
                ; Index
                ld a, $00
                ld [hli], a
                ld [de], a
                inc de
                ; Index
                ld a, %00000000
                ld [hl], a
                ld [de], a
            ; Copy DMA routine
            call oam_copydma
        ; Initialize palettes
        .initpalette:
            ld a, %11100100
            ld [PAL_BG], a
            ld [PAL_O0], a
        ; Initialize input
        .initinput:
            ld a, 0
            ld [input_curr], a
            ld [input_prev], a
        ; Initialize menu
        call menu_init
        ; Initialize draw
        call draw_init
        ; Initialize play
        call play_init
        ; Finish
        jp menu



SECTION "Data", ROM0
    ; Sprite set
    sset:
        INCBIN "sset.bin"
    sset_end:
    ; Tile set
    tset:
        INCBIN "tset.bin"
    tset_end: