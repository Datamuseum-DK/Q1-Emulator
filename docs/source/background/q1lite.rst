
Q1-Lite
=======

To work with the Q1 it is important to understand that the Q1 operating system
has no built-in commands. As far as I can tell, not a single one.

All there is is keyboard input with some line editing support such as backspace,
tab and delete.

The user types in a command, which is interpreted as the name
of a program located on one of the disks. This program is then loaded and
executed. Extra text after the filename is (sometimes) interpreted as
arguments to the program.

Programs can fail and decide to halt. Typically when this happens, user
interaction is required. The normal approach is to press the 'GO' key. Some
programs can be halted by pressing the 'STOP' key.

There is a also a 'RESET' button to restart the system if the program is running
in an infinite loop.

Here are some examples of commands that are known to work

**DINDEX**

Reads the INDEX file and provides details of the files on the disk: Name,
record size, number of records, start and end track, whether it is protected.

Q1 drives are enumerated starting with 1.

    > DINDEX

Starts the DINDEX program. The user will be queried for which drive to investigate.

    > DINDEX 3

Starts DINDEX looking at drive 3

From here the program is function-key driven for the nine functions. Use F1 - F9.


**ALTER**

Rename, Protect or Free (unprotect) a file. ALTER takes zero or more
arguments

    > ALTER

Starts the ALTER program. The user is queried for which action to take.

    > ALTER Rename

Starts ALTER and goes straight to the rename user input. User must supply the
remaining information

    > ALTER Rename 2

Rename file on disk 2. User must supply the src and dst filename

    > ALTER Rename 2 SCR

Rename SCR on disk 2, user must provide destination filename.

    > ALTER Rename 2 SCR SCR2

Performs renaming without user interaction.

Commands for protecting and freeing/unprotecting a file without user interaction:

.. code-block:: text

    > ALTER Protect 2 SCR
    > ALTER Free 2 SCR


**PRINT**

Prints the contents of a file.

    > PRINT Q1

**COPY**

Copies a file. Both file must already exist and record size and number of records
must be identical.

Syntax: COPY src dst src_disk dst_disk

.. code-block:: text

    > COPY
    > COPY T1R10 T2R10 4 4


**SORT**

    > SORT TT1R10 TT2R10

This command sorts TT1R10, whereas the second file seems untouched.
