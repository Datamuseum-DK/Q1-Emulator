
.. _PL1V10RGENA:

V10RGENA
^^^^^^^^

From fluxxample disk we were able to extract nearly all of the accounting
related program V10RGENA.

.. code-block:: text

    DCL     VER                      FIXED (8) INIT (84020611);
    /*      PROGRAM-ID.              V10RGENA.
            DATE-WRITTEN.            1984-02-06.
            AUTHOR.                  OLLE.
    ???????????????????????????????????????????????????????????????????????????????
                                     UPP EN TABELL I X-LED MED 10 ST VALFRIA KONTON
                                     I Y-LED L[GGER DEN SJ[LV UPP TILL 39 ST IK-
                                     SLAG SOM DEN FINNER KONTERADE F\R ANGIVNA
                                     KONTON. POSTENS BELOPP ADDERAS TILL PASSANDE
    ???????????????????????????????????????????????????????????????????????????????
                                     TABELLEN. KONTON L[GGES IN MED FORM XKTOFORM
                                     XKTOFIL. PARAMETERN F\R KONTON SKALL TILL-
                                     DELAS ETT NAMN P] TRE TECKEN.
        840206. OBg.                                                        */
    DCL     RKONTO1                  CHAR (3) INIT ('---'),
            RKONTO2                  CHAR (3) INIT ('---'),
    ???????????????????????????????????????????????????????????????????????????????
        DATUM2 CHAR(6),
        DAT1BIN BINARY,
        DAT2BIN BINARY,
        SPTYP BINARY,     /*                       1 = PERDAG 2 = BOKDAG */
        STAB(11) BINARY;

    DCL 1 TSTR,
          2 VERNRT FIXED(5),
    ???????????????????????????????????????????????????????????????????????????????
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
    ???????????????????????????????????????????????????????????????????????????????

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
                    PUT SKIP;
                    IF SPTYP = 1 THEN PUT EDIT ('PER-D ') (A);
    ???????????????????????????????????????????????????????????????????????????????
    ???????????????????????????????????????????????????????????????????????????????
    ???????????????????????????????????????????????????????????????????????????????
                    END;
                PUT SKIP EDIT (' ') (A(19));
    RUB20:
                DO I = 1 TO XANT;
                    PUT EDIT (RTEXT(J,I)) (A(14));
                    END;
                END;

    RUB99:
            RETURN;                                /*234*/
    END;

    STYRDATA:PROC;
    S1:
            PUT FILE(D) SKIP EDIT(VERSION)(A(49))('KOL/OLJA')(A(47))
            ('Fr.o.m. BEST-NR')(A(47))('Till BEST-NR')(A(47));

            J=138;
            CALL MOVEBUFF(J);
            GET SKIP LIST (SUBSTR(SOK,1,2));
            PUT FILE (D) EDIT (SUBSTR(SOK,1,2)) (A);
            J=185;
            CALL MOVEBUFF(J);
            GET SKIP LIST (RKONTO2);
    S15:
            IF (RKONTO1 > RKONTO2) | (TYP1=TYP2) THEN GO TO S1;
            PUT FILE(D) EDIT(RKONTO2)(A);
            UANT = RKONTO2 - RKONTO1;
            UIND = 0;
            J = 237;
            CALL MOVEBUFF (J);

    S17:
            PUT FILE (D) EDIT ('1 = PERDATUM')(A(47))('2 = BOKDATUM')(A(44));
    S4:     GET SKIP LIST(SPTYP);
            IF SPTYP<1 | SPTYP>2 THEN GO TO S4;
            PUT FILE(D) EDIT(SPTYP)(A(3))('Fr.o.m DATUM')(A(47))
            ('Till DATUM')(A);
            J=370;
            CALL MOVEBUFF(J);
    S3:     GET SKIP LIST(D);
            CALL DATCHECK(DATUM1);
            IF DATUM1='0     ' THEN GO TO S3;
            PUT FILE(D) EDIT(DATUM1)(A);
            J=417;
    ???????????????????????????????????????????????????????????????????????????????
    S2:     GET SKIP LIST(D);
            CALL DATCHECK(DATUM2);
            IF DATUM1>=DATUM2  THEN GO TO S2;
            D='0';
            PUT FILE(D) EDIT(DATUM2)(A);
            J = 470;
            CALL MOVEBUFF;
            PUT FILE (D) EDIT (' ') (A(2)) ('OLJA = O, KOL = K') (A(18));
            J = 515;
            CALL MOVEBUFF (J);
    /*      GET SKIP LIST (SUBSTR(SOK,2,1));
            PUT FILE (D) EDIT (SUBSTR(SOK,2,1)) (A);   */
            IF TYP1=1 THEN Y='6 ';
            IF TYP1=2 THEN Y='7 ';
            IF Y='4 ' THEN LISTTYP=1;
            ELSE LISTTYP=2;
            DAT1BIN=372*(SUBSTR(DATUM1,1,2)-78)+31*(SUBSTR(DATUM1,3,2)-1)+
               SUBSTR(DATUM1,5,2)-1;
            DAT2BIN=372*(SUBSTR(DATUM2,1,2)-78)+31*(SUBSTR(DATUM2,3,2)-1)+
               SUBSTR(DATUM2,5,2)-1;
            RETURN;                                /*293*/
    END;

    STARTPOST:PROC;
            RCODE=0;
            PK=ADDR(AREA);
            OPEN VERBELOP;
            CALL SEOF(VERBELOP);
            MAX=UNSPEC(VERBELOP);
            UNSPEC(VERBELOP)=0;
           ON ERROR GO TO ST1;
           READ KEY(KT8) FILE(VERBELOP) INTO(AREA);
            GO TO ST2;
    ST1:    IF ONCODE=4 THEN DO;
               PUT SKIP LIST('L[SFEL I TIMMAR   I POST: PROC ',RCODE);
               D=DATUM;
               CALL PLOAD('TR      ');
            END;
            RCODE=1;
            RETURN;                                /*371*/
    ST2:
            UNSPEC(VERBELOP)=UNSPEC(VERBELOP)-1;
            BLOCKANT=MAX-UNSPEC(VERBELOP);
            JJ=5;
            JK=0;
            IF (LISTTYP=1) | (SPTYP=2) THEN DO;
               OPEN VERTEXT;
               READ FILE(VERTEXT) INTO(TSTR);
               KONSTANT=VERNRT;
            END;
            RETURN;                                /*384*/
    END;

    POST:PROC;
    P1:     JJ=JJ+1;
            IF JJ>5 THEN DO;
               IF JK<1 THEN DO;
                  IF BLOCKANT>0 THEN DO;
                     JK=255;
                     IF JK>BLOCKANT THEN JK=BLOCKANT;
                     BLOCKANT=BLOCKANT-JK;
                     CALL RD(VERBELOP,AREA,JK,RCODE);
                     IF RCODE=0 THEN PUT SKIP LIST('L[SFEL I TIMMAR  ',RCODE);
                     PK=ADDR(AREA);
                  END;
                  ELSE DO;
    ???????????????????????????????????????????????????????????????????????????????
                     PDATUM=DAT1BIN;
                     DATUMT=DAT1BIN;
                     RETURN;                       /*403*/
                  END;
               END;
               ELSE DO;
                  UNSPEC(PK)=UNSPEC(PK)+BSTRL;
               END;
               JK=JK-1;
               JJ=1;
            END;
            UNSPEC(PB)=UNSPEC(PK)+JJ*10+1;
            IF PDATUM=0 THEN GO TO P1;
            RETURN;                                /*414*/
    END;

    DATTEST:PROC;
            RCODE=0;
            IF (SPTYP=2) & (PDATUM<0) THEN DO;
               IF VERNR=VERNRT THEN DO;
                  UNSPEC(VERTEXT)=VERNR-KONSTANT;
                  ON ERROR GO TO D1;
                  ON ENDFILE GO TO D1;
                  READ FILE(VERTEXT) INTO(TSTR);
               END;
               IF (DAT1BIN>DATUMT) | (DAT2BIN<=DATUMT) THEN RCODE=1;
            END;
            ELSE DO;
               IF PDATUM<0 THEN PDATUM=-PDATUM;
               IF (DAT1BIN>PDATUM) | (DAT2BIN<=PDATUM) THEN RCODE=1;
            END;
            RETURN;                                /*432*/

    ???????????????????????????????????????????????????????????????????????????????
            R=R-1;
            RCODE=1;
            RETURN;                                /*437*/
    END;


    ???????????????????????????????????????????????????????????????????????????????
    NOLLTAB: PROC;

    NP10:
            DO YL = 1 TO 39;
                DO XL = 1 TO 10;

    Track information for track 5

    ???????????????????????????????????????????????????????????????????????????????
                    END;
                END;

    NP99:
            RETURN;
            END;




    KONTORED: PROC;

    KP10:
            UIND = UIND + 1;
            LASNYCKEL = '0';
            IF UIND = UANT THEN DO;
                LASNYCKEL = '1';
                UIND = 0;
                GO TO KP20;
                END;

            IF SWFORSTA = 'J' THEN DO;
                UIND = 0;
                SWFORSTA = 'N';
                GO TO KP20;
                END;
            GO TO KP90;

    KP20:
            KIND = KIND + 1;
            XL = KIND;
            IF KIND = XANT THEN DO;
                RCODE = 3;
                GO TO KP99;
                END;

    KP90:
            KONTOG = '00000000000';
            SUBSTR (KONTOG,1,5) = XKTO (KIND);
            IF RKONTO1 + UIND > '99 ' THEN DO;
                SUBSTR (KONTOG,6,3) = RKONTO1 + UIND;
                 GO TO KP95;
                 END;
            IF RKONTO1 + UIND > '9  ' THEN DO;
                 SUBSTR (KONTOG,7,2) = RKONTO1 + UIND;
                 GO TO KP95;
                 END;
            SUBSTR (KONTOG,8,1) = RKONTO1 + UIND;
    KP95:
            KT8 = SUBSTR (KONTOG,1,8);
    KP99:
    /*      PUT SKIP LIST ('KONTO = ',KONTOG);       */
            RETURN;
            END;


    ???????????????????????????????????????????????????????????????????????????????


    SKR10:
            UNSPEC (IK) = ADDR (RYTEXT(1));
    ???????????????????????????????????????????????????????????????????????????????
            DO YL = 1 TO 39;
                OPEN KSKONTOP;
                IKSLAG = YRADKTOREDEF;
                READ KEY (IKSLAG) FILE (KSKONTOP) INTO (KSPOST);
                UNSPEC (IK) = UNSPEC (IK) + 14;
                PUT SKIP EDIT (YRADKTOREDEF) (A(4)) (IKTEXT) (A(15));
                DO XL = 1 TO XANT;
                    IF SUMMA (YL,XL) = 0 THEN DO;
                        PUT EDIT (' ') (A(14));
                        GO TO SKR20;
                        END;
    ???????????????????????????????????????????????????????????????????????????????
    ???????????????????????????????????????????????????????????????????????????????
    SKR20:
                    END;
    SKR30:
                END;

    SKR99:
            RETURN;
            END;


    YKORD: PROC;

    YP10:
            OKEY = 'N';
            UNSPEC (IK) = ADDR (RYTEXT(1));
            UNSPEC (IK) = UNSPEC (IK) - 14;
            DO I = 1 TO 39;
                UNSPEC (IK) = UNSPEC (IK) + 14;
                IF SUBSTR (KONTONR,9,3) = YRADKTOREDEF THEN DO;
                    OKEY = 'J';
                    YL = I;
                    GO TO YP99;
                    END;
                YRADKTOREDEF = SUBSTR (KONTONR,9,3);
                OKEY = 'J';
                YL = I;
                GO TO YP99;
                END;
                PUT SKIP LIST ('IK-TABELLEN [R FULL ',KONTONR);


    YP99:
            RETURN;
            END;



    /*  H [ R   B \ R J A R   H U V U D P R O G R A M M E T  */


    START:
            CALL DATCHECK(DATUM);
            IF DATUM='0     ' THEN CALL PLOAD('Q       ');
            UNSPEC(P)=16570;
    ???????????????????????????????????????????????????????????????????????????????
            UNSPEC(PP)=16616;
            RADANT = 51;
    A10:
            CALL STYRDATA;
    A20:
            OPEN XKTOFIL;
            I = 0;
    A21:
            ON ENDFILE GO TO A29;
            READ FILE (XKTOFIL) INTO (XKTOPOST);
            PUT SKIP LIST ('SOK = ',SOK);
            PUT SKIP LIST ('XOK = ',XOK);
            IF SUBSTR (XOK,1,2) = SUBSTR (SOK,1,2) THEN GO TO A21;
            IF SUBSTR (XOK,3,1) = 'R' THEN DO;
                SUBSTR (RUBTEXT,1,14) = XTEXT1;
                SUBSTR (RUBTEXT,15,14) = XTEXT2;
                SUBSTR (RUBTEXT,29,14) = XTEXT3;
                SUBSTR (RUBTEXT,43,14) = XTEXT4;
                SUBSTR (RUBTEXT,57,14) = XTEXT5;
                GO TO A21;
                END;
            I = I + 1;
            RTEXT (1,I) = XTEXT1;
            RTEXT (2,I) = XTEXT2;
            RTEXT (3,I) = XTEXT3;
            RTEXT (4,I) = XTEXT4;
            RTEXT (5,I) = XTEXT5;
            XKTO (I) = XKONTO;
            GO TO A21;
    A29:
            IF I = 0 THEN DO;
    ???????????????????????????????????????????????????????????????????????????????
                DO I = 1 TO 1000;
                END;
                GO TO A10;
                END;
            XANT = I;
            KIND = 0;

    A30:
            OPEN YKTOFIL;
            UNSPEC (IK) = ADDR (RYTEXT (1));
            UNSPEC (IK) = IK - 14;

    Track information for track 7

            DO I = 1 TO 39;
                UNSPEC (IK) = IK + 14;
                YRADKTOREDEF = 0;
                YRADTEXTREDEF = '            ';
                END;
            UNSPEC (IK) = ADDR (RYTEXT (1));
            UNSPEC (IK) = IK - 14;
            DO I = 1 TO 40;
                ON ENDFILE GO TO A39;
                READ FILE (YKTOFIL) INTO (YKTOPOST);
                UNSPEC (IK) = IK + 14;
                YRADTEXTREDEF = YTEXT;
                YRADKTOREDEF = YKTO;
                END;
    A39:
    L0:
            CALL NOLLTAB;
            CALL KONTORED;
            CALL STARTPOST;
            IF RCODE=1 THEN GO TO L3;
    L1:
            CALL POST;                  /* INL[SN. AV 255 REC. FR]N VERBELOP */
            CALL DATTEST;
            IF SUBSTR (KONTONR,1,8) > KT8 THEN GO TO L3;
            GO TO L5;
    L3:
            CALL KONTORED;
            IF RCODE = 3 THEN GO TO UT;
            CALL STARTPOST;
            IF RCODE = 1 THEN GO TO L3;
            GO TO L1;
    L5:

            IF KONTONR='SLUT9999999' THEN GO TO UT;
            CALL YKORD;
            IF OKEY = 'J' THEN GO TO L10;
            GO TO L1;
    L10:
            SUMMA (YL,XL) = SUMMA (YL,XL) + BELOPP;
            SUMMA (YL,XANT) = SUMMA (YL,XANT) + BELOPP;
            SUMMA (39,KIND) = SUMMA (39,KIND) + BELOPP;
            SUMMA (39,XANT) = SUMMA (39,XANT) + BELOPP;
            GO TO L1;

    UT:
    SLUT:
            CALL RUB;
            CALL SKRIV_SUMMA;
            DO I = 1 TO 2000;
            END;
            PUT SKIP (5);
            D=DATUM;
            CALL PLOAD('Q       ');

    END;
            CALL STARTPOST;
            IF RCODE = 1 THEN GO TO L3;
            GO TO L1;
    L5:

            IF KONTONR='SLUT9999999' THEN GO TO UT;
            CALL YKORD;
            IF OKEY = 'J' THEN GO TO L10;
            GO TO L1;
    L10:
    ???????????????????????????????????????????????????????????????????????????????
            SUMMA (YL,XANT) = SUMMA (YL,XANT) + BELOPP;
            SUMMA (39,KIND) = SUMMA (39,KIND) + BELOPP;
            SUMMA (39,XANT) = SUMMA (39,XANT) + BELOPP;
            GO TO L1;

    UT:
    SLUT:
            CALL RUB;
            CALL SKRIV_SUMMA;
            DO I = 1 TO 2000;
            END;
            PUT SKIP (5);
            D=DATUM;
            CALL PLOAD('Q       ');

    END;
