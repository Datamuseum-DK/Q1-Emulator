.. _exeprogs:

Executable programs
^^^^^^^^^^^^^^^^^^^

**DINDEX**

Lists content of floppy disks in detail. Comes in different versions.

> DINDEX disk#


**DISK**

Used to initialise disk - for example by making a copy. See details in
LMC System Software manual.

> DISK INIT srcdisk# dstdisk#



**EDIT**

Used to edit source code and text documents. Text is displayed one line at
a time. The user can overwrite/edit the line according to the line input
functions described in the ROS User's guide. F2: add line(s), F1: done
adding lines, F7: done editing.

> EDIT filename


**FORM**

Reads structured data from disk and applies a schema to it. Typically used
for address records for employees etc. FORM seem to be using the same
functionality as EDIT (F2 to add an entry etc.).

> FORM ADRFORM KVVADR


**PRINT**

Prints (text) files such as source code and text documents.

> PRINT filename



**Q**

Not sure. Possibly accounting. the user is prompted for a date (datum) which
has to conform to yymmdd. The the user is asked for an operator id (I think).
I don't know what to input here.

> Q


**UTSKRIFT** (f1578)

Prints address labels from a specific address database. The user is promptet
for a business id (9 works) and prints the address labels side by side.

> UTSKRIFT
