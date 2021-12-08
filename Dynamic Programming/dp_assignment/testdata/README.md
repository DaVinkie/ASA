## Global 1

python align.py global1.fasta -m pam250 -g 2 -v

    Wrong TRACEBACK for global alignment using pam250 (gap penalty = 2)
      Sequence 1: MCHFLBFDNFCCCATGCQWLHKYDEY
      Sequence 2: NEVEVECWKRGNQQDFCCCMARGWKEZ
    Correct (high road) alignment is:
      ----M-C--H-FLBFDNFCCC-ATGCQWLHKYDEY
      NEVEVECWKRG-NQ-QDFCCCMARG--W--K-EZ-
    Score: 63
    Submitted code produced:
      M-C--H-FLBFDNFCCC-ATGCQWLHKYDEY
      VECWKRG-NQ-QDFCCCMARG--W--K-EZ-
    Score: 63
    Points: 0.444444


## Global 2
python align.py test3.fasta -s global -g 8 -m pam250

    Correct (high road) alignment is:
      ZMTBIIVQKTKWIEMWTBATVDPRGS
      --TNL--QDV--I-FRC-S---P--T
    Score: -80

## Global 3
python align.py global3.fasta -m pam250 -g 8 -v

    Correct (high road) alignment is:
        -A-D-T---T-DB--SBVRMNBSAFEQZD
        LPVHCVWFFIFBEFRGBBCIDEPPBTPQV
    Score: -64

## Global 4
python align.py global4.fasta -m pam250 -g 3 -v

    Correct (high road) alignment is:
        AEEQWDWVDZMWCVLH--
        -DI-RT-IGSK-DGSHEV
    Score: -13

# Semiglobal

## Semiglobal 1
python align.py sglobal1.fasta -m pam250 -g 2 -s semiglobal

    Correct (high road) alignment is:
        WAICF---YE-Y-FWF-PBP-N--
        ----YRQHYQHFCFWFLQKRITCG
    Score: 48

## Semiglobal 2
python align.py sglobal2.fasta -m pam250 -g 2 -s semiglobal -v

    Correct (high road) alignment is:
        ------GIZDBGLFH---N--RFN-LFBRHLAAMGKV
        AVISMW-L-NKG-FHABDBGGHINC-F----------
    Score: 21

## Semiglobal 3
python align.py sglobal3.fasta -m pam250 -g 3 -s semiglobal -v

    Correct (high road) alignment is:
        ZZQIPQHCBZ-EI------------------
        ---IFKH-LZLAVARNFSAWSKTAVWBMWBA
    Score: 5

## Semiglobal 4
python align.py sglobal4.fasta -m blosum62 -g 5 -s semiglobal -v

    Correct (high road) alignment is:
        ---------SFFBYCGQHAEYNB
        EDEKSIDCRDMFA----------
    Score: 4

## Semiglobal 5
python align.py sglobal5.fasta -m pam250 -g 2 -s semiglobal -v

    Correct (high road) alignment is:
        -ZKLAPTFHSNICFTPTM------------
        BNK---KFH-KICFIGEZASHHNFSKCWMS
    Score: 37

## Semiglobal 6
python align.py sglobal6.fasta -m pam250 -g 3 -s semiglobal -v

    Correct (high road) alignment is:
        --DZ-ME--YBANVSDAMEIYYY-WHNQYLRGTMT
        SRBHSMZBWYBIDYBEYBHVIWLRWS---------
    Score: 30
    
## Semiglobal 7
python align.py sglobal7.fasta -m blosum62 -g 5 -s semiglobal -v

    Correct (high road) alignment is:
        -------------------------IWLDGPLICRSLWDCYIV
        ARTTGZKFRWFFQVGKATRNGYNLA------------------
    Score: 0
## Semiglobal 8

    Correct (high road) alignment is:
        ----------------------ATGAACCGGTGTCAAAAATATTAACTTG
        AGGAAAACCGGATGCTTTAGAC----------------------------
    Score: 0

## local2
python align.py local2.fasta -m pam250 -g 8 -s local -v

    Correct (high road) alignment is:
        SGDMKVZZLR
        ZABZKATPLS
    Score: 12

## local3
python align.py local3.fasta -s local -m pam250 -g 3 -v

    Correct (high road) alignment is:
        EBQRDIEPCTF-PNCM--BVGG-HFL
        QZHANFTG-KYWQSALTANKBGYHLV
    Score: 17

# local5
python align.py local5.fasta -s local -m pam250 -g 3 -v

    Correct (high road) alignment is:
        KZCWZFEP--M-RZLE
        RK-WQAZPAYMPSBTE
    Score: 26

# local6
python align.py local6.fasta -s local -m identity -g 7 -v

    Correct (high road) alignment is:
        TGT
        TGT
    Score: 3
    Submitted code produced:
        GTTGT
        GATGT
    Score: 3
    Points: 0.888889

# local7
python align.py local7.fasta -s local -m pam250 -g 9 -v

    Correct (high road) alignment is:
      IIW
      FAW
    Score: 17
    Submitted code produced:
      QW
      AW
    Score: 17
    Points: 0.888889

