INCLUDE "const.inc"



SECTION "OAM DMA Routine", ROM0

    oam_copydma::
        ld hl, oam_dmaroutine
        ld b, oam_dmaroutine_end - oam_dmaroutine
        ld c, LOW(oam_dma) ; Low byte of the destination address
      .looop:
        ld a, [hli]
        ldh [c], a
        inc c
        dec b
        jr nz, .looop
        ret
    
    oam_dmaroutine:
        ldh [DMA_HADDR], a
        ; DMA transfer begins, we need to wait 160 microseconds while it transfers
        ld a, 40
      .wait:
        dec a
        jr nz, .wait
        ret
    oam_dmaroutine_end:



SECTION "OAM Buffer", WRAM0[$C100]
    oam_buffer::
        ds $A0 ; 160 bytes for 40 sprites (4 bytes per sprite)
    oam_buffer_end::



SECTION "OAM DMA", HRAM
    ; Reserve space to copy the routine to
    oam_dma::
        ds oam_dmaroutine_end - oam_dmaroutine