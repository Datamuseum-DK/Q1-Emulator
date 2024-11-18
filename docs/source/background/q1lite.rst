
Q1-Lite
=======

To work with the Q1 it is important to understand that the system
has no operating system as we know it today.

Instead the user types in a command which is interpreted as the name
of a program located on the disk. This program is then loaded and executed.
Ekstra arguments after the filename are arguments to the program.

Programs can fail and decide to halt. Typically when this happens, user
interaction is required. The normal approach is to press the 'GO' key.

If the system is completely frozen there is a 'RESET' button to restart
the system.

Here are some examples of commands that are known to work

**DINDEX**

Reads the INDEX file and provides details of the files on the disk: Name,
record size, number of records, start and end track, whether it is protected.

Q1 drives are enumerated starting with 1.

    > DINDEX

Starts the DINDEX program. The user will be queried for which drive to investigate.

   > DINDEX 3

Starts DINDEX looking at drive 3


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

    > ALTER Protect 2 SCR
    > ALTER Free 2 SCR


**PRINT**

Prints the contents of a file.

    > PRINT Q1

**COPY**

Copies a file. Both file must already exist and record size and number of records
must be identical.

Syntax: COPY src dst src_disk dst_disk

    > COPY
    > COPY T1R10 T2R10 4 4
