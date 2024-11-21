
Running the emulator
====================


Interactive Session
^^^^^^^^^^^^^^^^^^^

If you just want to interact with the Q1 via the keyboard, you
should use the following invocation

.. code-block:: text

  > python3 emulator.py         # no instr. decode, no hexdump

Typed-in keys are passed to the Q1 system via fake interrupts.
Characters are sent to the display emulator.

The keyboard interaction is currently tailored to my MacBook Pro
keyboard. If you are using a different system you should make your own
bindings. Values for non printable characters are output during an
interactive session.

On my MacBook Pro the following Q1 keys are implemented. Here,
they are referenced by their variable names, not the names printed on
the keys (see emulator.py):


.. list-table:: Key bindings
  :header-rows: 1

  * - Key Name
    - MacBook key
  * - GO
    - Option-g
  * - STOP
    - Option-s
  * - CORR
    - Backspace
  * - RETURN
    - Return (LF -> CR)
  * - CLEAR ENTRY
    - Option-c
  * - INSERT MODE
    - Option-m
  * - CHAR ADV
    - Option-l
  * - DEL CHAR
    - Option-d



.. list-table:: Special functions
  :header-rows: 1

  * - MacBook key
    - Function
  * - Option-f
    - Function Keys (F1 - F9) by user input
  * - Option-b
    - hexdump of modified parts of memory
  * - Option-r
    - Reset button
  * - Option-t
    - Toggle instruction decode
  * - Option-a
    - misc. debug



Execution decode
^^^^^^^^^^^^^^^^

.. code-block:: text

  > python3 emulator.py -d   # instruction decode, no hexdump



Breakpoint
^^^^^^^^^^
You might want to halt the program and print out various information
when the Program Counter reaches a certain address. To do this:

.. code-block:: text

  > python3 emulator.py -b 0x1ff

This will do a hexdump of the RAM part of the memory, show the previous
10 instructions and dump information about INDEX and LFILE file descriptors.


Triggerpoint
^^^^^^^^^^^^
If you want detailed debug, but only starting from a certain Program Counter,
do This

.. code-block:: text

  > python3 emulator.py -t 0x1ff
