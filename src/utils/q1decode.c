
#include <stdio.h>
#include <inttypes.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

#define FM 1
#define Q1 4
#define q1thresh1 39
#define q1thresh2 57
#define q1thresh3 75
#define fmthresh 0
#define mfmthresh1 0
#define mfmthresh2 0
#define postcomp 0.5
#define cwclock 2
#define mfmshort 18.0
#define garbage 0x62
int uencoding = Q1;
int recordSize;
int cnt = 0;

int ofd = 0;
char pbuffer[100];
int splen;


void process_bit (char bit) {
  static int  data_word = 0;
  static int state = 0;
  static char lastbit;
  static char mfmword;
  static unsigned char outword;
  static int bitcnt;
  static int sum;
  static unsigned int crc;
  static int byteCnt;
  static int currentRecordSize;
  static unsigned char buffer[256];
  data_word = data_word << 1;
  data_word |= bit;


  //printf("CNT: %05X PROCESS BIT: %08X\n", cnt, data_word);
  if (data_word  == 0x55424954) { // Mark
    printf("\nCNT: %05X ADDRESS MARK: %08X ", cnt, data_word);
    state = 1; lastbit = 0; mfmword = 0; bitcnt=0; sum=0;
    crc = 0;
    byteCnt = 0;
    currentRecordSize = 2;

    sprintf(pbuffer, "\n[ 0x9e, ");
    write(ofd, pbuffer, 9);
    return;
  }
  if (data_word == 0x55424945) { // Mark
    printf("\nCNT: %05X DATA    MARK: %08X ", cnt, data_word);
    state = 1; lastbit = 1; mfmword = 0; bitcnt=0; sum=0;
    crc = 0x9B;
    byteCnt = 0;
    currentRecordSize = recordSize;

    sprintf(pbuffer, "\n[ 0x9b, ");
    write(ofd, pbuffer, 9);
    return;
  }
  //printf ("state = %d bit = %d mfmword=%1X lastbit=%d outword = %02X \n", state, bit, mfmword & 0b11, lastbit, outword);
  if (state == 1) {
    // shift in one bit into mfm word
    mfmword |= bit;
    state = 2;
  } else if (state == 2) {
    mfmword = mfmword << 1;
    mfmword |= bit;
    //printf ("mfmword=%d\n", mfmword & 0x03);
    if ((lastbit == 1) && ((mfmword & 0x3)  == 0b00)) {
      outword = outword << 1;
      outword |= 0;
      lastbit = 0;
      state = 1;
    } else if ((lastbit == 0) && ((mfmword & 0x03) == 0b10)) {
      outword = outword << 1;
      outword |= 0;
      lastbit = 0;
      state = 1;
    }  else if ((mfmword & 0x03) == 0b01) {
      outword = outword << 1;
      outword |= 1;
      lastbit = 1;
      state = 1;
    } else {
      state= 0;
      //printf ("V");
    }
    //printf ("%d", lastbit);
    //if (bitcnt == bitOffset) {
    //  printf ("%c", 0x7f & EBCDICtoASCII( outword ));
    //}
    bitcnt++;
    if (bitcnt == 8) {
      bitcnt = 0;
      if (byteCnt == currentRecordSize) {
        if ((outword & 0xff) == (crc & 0xff)) {
          //printf("CRC OK\n");
        } else {
          printf("CRC ERROR\n");
        }
      }
      buffer[byteCnt] = outword & 0xff;
      byteCnt++;
      printf (" ");
      outword = outword & 0xff;
      crc += outword & 0xff;
      if (byteCnt <= currentRecordSize) {
        printf ("%02X", outword);
      }
      if (byteCnt==currentRecordSize) {
        printf("\n");


        for (int i=0; i<currentRecordSize;i++) {

          splen = sprintf(pbuffer, "0x%02x, ", buffer[i]);
          write(ofd, pbuffer, splen);

          if ( (buffer[i] >= 32) && (buffer[i] < 127)) {
            printf ("%c", buffer[i]);
          } else {
            printf (" ");
          }
        }

        splen = sprintf(pbuffer, "],");
        write(ofd, pbuffer, splen);

        printf("\n");
      }
    }
    mfmword = 0;

  }
}


/*
* Convert Catweasel samples to strings of alternating clock/data bits
* and pass them to process_bit for further decoding.
* Ad hoc method using two fixed thresholds modified by a postcomp
* factor.
*/
void
process_sample(int sample)
{
  static float adj = 0.0;
  int len;

  if (uencoding == FM) {
    if (sample + adj <= fmthresh) {
      /* Short */
      len = 2;
    } else {
      /* Long */
      len = 4;
    }
  } else if (uencoding == Q1) {
    if (sample + adj <= q1thresh1) {
      /* Short */
      len = 2;
    } else if (sample + adj <= q1thresh2) {
      /* Medium */
      len = 3;
    } else if (sample + adj <= q1thresh3) {
      /* Long */
      len = 4;
    } else if (sample + adj <= garbage) {
      len = 5;
    } else {
      len = 6;
    }

  } else  {
    if (sample + adj <= mfmthresh1) {
      /* Short */
      len = 2;
    } else if (sample + adj <= mfmthresh2) {
      /* Medium */
      len = 3;
    } else {
      /* Long */
      len = 4;
    }

  }
  adj = (sample - (len/2.0 * mfmshort * cwclock)) * postcomp;
  if (len == 6) { cnt++; return; }
  process_bit(1);
  while (--len) process_bit(0);
  cnt ++;
}





int main (int argc, char ** argv) {
  ofd = open("output.py", O_RDWR | O_CREAT| O_TRUNC);
  if (ofd == -1) {
    printf("open() error");
    exit(0);
  }
  int c;
  if (argc==2) {
    printf ("ARG %s\n", argv[1]);
    sscanf(argv[1], "%d", &recordSize);
    printf ("recordSize=%d\n", recordSize);
  }  else {
    printf("Need one argument. Please specify the record size for the track. Wrong record size will cause the CRC calculation to fail.\n");
    return -1;
  }
  while ((c = getchar()) != -1) {
    process_sample(c & 0x7f);
  }
  close(ofd);
  return 0;
}
