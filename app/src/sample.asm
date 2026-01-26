INCLUDE "const.inc"



SECTION "Sample", ROM0

    sample::
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
    ; Sample 6
    sample_6::
        INCBIN "sample6.bin"
    sample_6_end::
    ; Sample 7
    sample_7::
        INCBIN "sample7.bin"
    sample_7_end::
    ; Sample 8
    sample_8::
        INCBIN "sample8.bin"
    sample_8_end::
    ; Sample 9
    sample_9::
        INCBIN "sample9.bin"
    sample_9_end::



SECTION "Sample WRAM", WRAM0
    sample_lo:: db
    sample_hi:: db