

IO Addresses
============

The two main sources of information for IO are the two versions of the
"The Q1 Assembler" document I am aware of.

Karl's version (KIO) (only pages 64 to 80), dated 8/78.

`Karls ASM <https://www.peel.dk/Q1/pdf/Q1%20ASM%20IO%20addresses%20usage%20Q1%20Lite.pdf>`_

From TheByteAttic (TBA): Whole document, marked preliminary, not dated.
Pages 47 to 62 describes the IO addresses

`TheByteAttic <https://github.com/TheByteAttic/Q1/blob/main/Original%20Documentation/Q1%20Assembler.pdf>`_



The two documents have some differences. For example the known IO addresses are

.. list-table:: IO Addresses
   :header-rows: 1

   * - Address
     - KIO
     - TBA
   * - 0x00 (IO)
     - RTC
     - Timer
   * - 0x01 (IO)
     - Keyb.
     - Keyb.
   * - 0x03
     - Disp. data (O)
     - Disp. data + status (IO)
   * - 0x04
     - Disp. ctrl (IO)
     - Disp. ctrl (O)
   * - 0x05 (IO)
     - Prt. data + status
     - Prt. data + status
   * - 0x06 (O)
     - Prt. ctrl 1
     - Prt. ctrl 1
   * - 0x07 (O)
     - Prt. ctrl 2
     - Prt. ctrl 2
   * - 0x08 (IO)
     - Dotm. Print
     -
   * - 0x09 (IO)
     - Disk R+W
     -
   * - 0x0a (IO)
     - Disk ctrl 1 + status
     -
   * - 0x0b (O)
     - Disk ctrl 2
     -
   * - 0x10 (IO)
     - serial comms: select control register (O)
     - Data R+W
   * - 0x11 (IO)
     - serial comms: r/w to comntrol register
     - ctrl 1, status 1
   * - 0x12 (IO)
     -
     - ctrl 2, status 2
   * - 0x13 (O)
     -
     - ctrl 3
   * - 0x19 (IO)
     -
     - Disk R+W
   * - 0x1a (IO)
     -
     - Disk ctrl 1 + status
   * - 0x1b (O)
     -
     - Disk ctrl 2
   * - 0x1c (O)
     -
     - Disk ctrl 3


Neither seem fully compatible with the JDC roms :ref:`ROMS` as
**out** commands to both addresses 0xa and 0x1a are in use (see below).

.. code-block:: text

  ...
  0B0B 6C           ; ld l, h         |
  0B0C 67           ; ld h, a         |
  0B0D D3 1A        ; out (0x1a), a   |
  0B0F 97           ; sub a           |
  0B10 D3 0A        ; out (0xa), a    |
  0B12 DB 1A        ; in a, (0x1a)    |
  0B14 0F           ; rrca            |
  ...


Also I've seen **in()** commands to address 0xc which isn't documented in
either.

Update 2024 10 10

0xc seems to be a printer address - see log entry for 2024 10 10.



Display
=======

When reading the Display status, TBA reports **Bit 7** as busy.
However KIO has the following:

**Bit 6** = 0 for 12 line = 1 for 6 line
**Bit 5** = 1 for LITE; = 0 for LMC

Neither seem to be complete, as the code for the JDC roms
at 0x2A0 seems to be testing **Bit 3** to select a 80 character width and
**Bit 4** to select 40 bytes:


.. code-block:: text

  <<<<< Display width? >>>>>
  02A0 DB 04        ; in a, (0x4)     |
  02A2 CB 5F        ; bit 0x3, a      |
  02A4 3E 50        ; ld a, 0x50      |
  02A6 C0           ; ret nz          |
  02A7 DB 04        ; in a, (0x4)     |
  02A9 CB 67        ; bit 0x4, a      |
  02AB 3E 28        ; ld a, 0x28      |
  02AD C0           ; ret nz          |
  02AE C6 07        ; add a, 0x7      |
  02B0 C9           ; ret             |


.. list-table:: Display status (speculative)
   :header-rows: 1

   * - Bit
     - Description
   * - 7
     - busy
   * - 6
     - 1: 6 line, 0: 12 line
   * - 5
     - 1: Lite. 0: LMC
   * - 4
     - 40 bytes
   * - 3
     - 80 bytes
   * - 2
     - unknown
   * - 1
     - unknown
   * - 0
     - unknown
