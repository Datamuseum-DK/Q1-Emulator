


The (partial) Q1 disk images available to us seem to be related to accounting.



.. code-block:: text

    DCL     VER                      FIXED (8) INIT (84020611);
    /*      PROGRAM-ID.              V10RGENA.
            DATE-WRITTEN.            1984-02-06.
            AUTHOR.                  OLLE.
                                     UPP EN TABELL I X-LED MED 10 ST VALFRIA KONTON
                                     I Y-LED L[GGER DEN SJ[LV UPP TILL 39 ST IK-
                                     SLAG SOM DEN FINNER KONTERADE F\R ANGIVNA
                                     KONTON. POSTENS BELOPP ADDERAS TILL PASSANDE
                                     TABELLEN. KONTON L[GGES IN MED FORM XKTOFORM
                                     XKTOFIL. PARAMETERN F\R KONTON SKALL TILL-
                                     DELAS ETT NAMN P] TRE TECKEN.
        840206. OBg.                                                        */
    DCL     RKONTO1                  CHAR (3) INIT ('---'),
            RKONTO2                  CHAR (3) INIT ('---'),
        DATUM2 CHAR(6),
        DAT1BIN BINARY,
        DAT2BIN BINARY,
        SPTYP BINARY,     /*                       1 = PERDAG 2 = BOKDAG */
        STAB(11) BINARY;

    DCL 1 TSTR,
          2 VERNRT FIXED(5),
          2 TEXT CHAR(13),
          2 ANTVERP BINARY;
    DCL PK POINTER,
        1 BSTR BASED(PK),
          2 KONTONR CHAR(11);

    DCL PB POINTER,
        1 BELSTR BASED(PB),
          2 VERNR BINARY,
          2 PDATUM BINARY,
          2 BELOPP FIXED(11);
    DCL 1 AREA,
          2 CH(255) CHAR(61);
          /* 15 555 BYTES */



    DCL 1   IKPOST,
    DCL 1   IKPOST,
            2   SDATUM3              FIXED (6),
            2   IKTEXT               CHAR (32),
            2   UHMARK               CHAR (1);

    DCL 1   XKTOPOST,
            2   XOK                  CHAR (3),
            2   XKONTO               FIXED (5),
            2   XTEXT1               CHAR (14),
            2   XTEXT2               CHAR (14),
            2   XTEXT3               CHAR (14),
            2   XTEXT4               CHAR (14),
            2   XTEXT5               CHAR (14);

    DCL 1   YKTOPOST,
            2   YKTO                 FIXED (3),
            2   YTEXT                CHAR (12);

    DCL 1   RYTEXT (40),
            2   YRADTEXT             CHAR (12),
            2   YRADKTO              FIXED (3);

    DCL     IK  POINTER,
            1   RYTEXTREDEF BASED (IK),
                2   YRADTEXTREDEF    CHAR (12),
                2   YRADKTOREDEF     FIXED (3);
    DCL     XKTO (10)                CHAR (5),
            IKSLAG                   CHAR (3),
            SOK                      CHAR (3);


    DCL VERTEXT FILE,
        VERBELOP FILE,
        KSKONTOP FILE,
        XKTOFIL FILE,
        YKTOFIL FILE;


And the first (of seven tracks) of the file **V10RGENA** from the 'fluxsample' disk.

.. code-block:: text

    DCL BSTRL BINARY INIT(61),
        MAX BINARY,
        BLOCKANT BINARY,
        JK BINARY,
        JJ BINARY,
        LISTTYP BINARY,            /* 1 = KONTOUTDRAG,   2 = SALDOBESKED */
        RCODE BINARY,
        KONTOG CHAR(11),
        SIDA BINARY INIT(1),
        R BINARY INIT(0),
        NAMN(2) CHAR(10) INIT('KVV/KWAROS','AROSKRAFT'),
        T15BELRED                      CHAR (15),
        KONSTANT BINARY,
        BUFF CHAR(20),
        T1 CHAR(1),
        T61 CHAR(6),
        T62 CHAR(6),
        T11 CHAR(11),
        T13 CHAR(13),
        T14 CHAR(14),
        T15                          CHAR (15),
        RUBTEXT                      CHAR (70),
        LASNYCKEL                    CHAR (1) INIT ('0'),
        SWFORSTA                     CHAR (1) INIT ('J'),
        KT8 CHAR(8),
        FX6                FIXED(6),
        TYP1               BINARY  INIT(0),
        TYP2               BINARY INIT(0),
        OFFSET             BINARY INIT(1),
        LENGD              BINARY INIT(0),
        SUMMA (39,10)       FIXED (11) INIT ((39)0),
        SSUMMA                       FIXED (11,2),
        XL                 BINARY,                 /* KOORDINAT I X-LED SUMMATAB */
        YL                 BINARY,                 /* KOORDINAT I Y-LED SUMMATAB */
        XANT               BINARY,
        UANT               BINARY,
    ???????????????????????????????????????????????????????????????????????????????
        KIND               BINARY,
        OKEY               CHAR (1),
        P                  POINTER,
        D                  CHAR(6) BASED(P),
        DATUM              CHAR(6),
        PP                 POINTER,
        1 STR              BASED(PP),
          2 X              CHAR(2),
          2 Y              CHAR(2),      /* 6 = UKTO,  7 = IKSLAG        */
          2 FIRMA          CHAR (1),
          2   OP_KOD                   BINARY,
          2   RADANT                   BINARY,
        T4                 CHAR(4),
        ANTAL_KONT         BINARY INIT(0),
        TOT_ANTAL_KONT     BINARY INIT(0),
        VERSION CHAR(47) INIT(' TR10KOLJA  Version 1.1                  830603');



    RUB:PROC;
    RUB10:
            IF FIRMA = '8' THEN DO;
    ???????????????????????????????????????????????????????????????????????????????
                END;
            IF FIRMA = '9' THEN DO;
                PUT SKIP (2) EDIT ('AROS') (A(40));
                END;
    ???????????????????????????????????????????????????????????????????????????????
                (A(8)) (DATUM) (A(6));
            DO J = 1 TO 5;
                IF J = 2 THEN DO;
                    PUT SKIP EDIT ('PARA:') (A) (SUBSTR(SOK,1,2)) (A(4));
    ???????????????????????????????????????????????????????????????????????????????
                    IF SUBSTR (SOK,1,1) = 'O' THEN PUT EDIT ('OLJA') (A(4));
                    PUT EDIT (' ') (A(6));
                    GO TO RUB20;
                    END;
                IF J = 3 THEN DO;
                    PUT SKIP EDIT ('BEST-NR: ') (A) (RKONTO1) (A(3)) ('-') (A)
                        (RKONTO2 - '001') (P'999') (' ') (A(3));
                    GO TO RUB20;
                    END;
                IF J = 4 THEN DO;
