from enum import Enum


class ChromosomeName(str, Enum):
    chr1 = "chr1"
    chr2 = "chr2"
    chr3 = "chr3"
    chr4 = "chr4"
    chr5 = "chr5"
    chr6 = "chr6"
    chr7 = "chr7"
    chr8 = "chr8"
    chr9 = "chr9"
    chr10 = "chr10"
    chr11 = "chr11"
    chr12 = "chr12"
    chr13 = "chr13"
    chr14 = "chr14"
    chr15 = "chr15"
    chr16 = "chr16"
    chr17 = "chr17"
    chr18 = "chr18"
    chr19 = "chr19"
    chr20 = "chr20"
    chr21 = "chr21"
    chr22 = "chr22"
    chrX = "chrX"
    chrY = "chrY"


class Sorting(Enum):
    position_asc = "position,asc"
    position_desc = "position,desc"
    g4_score_asc = "score,asc"
    g4_score_desc = "score,desc"
    palindrome_spacer_asc = "spacer_length,asc"
    palindrome_spacer_desc = "spacer_length,desc"