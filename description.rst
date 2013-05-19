.. -*- restructuredtext -*-

(void)walker
============

`(void)walker` is a toolbox for `GDB` which provides utilities for debugging
software on an instruction level.


Requirements
------------

 * `GDB <http://www.gnu.org/software/gdb/>`_ 7.5 or later built with support
   for Python extensions.
 * `FlowUI <https://github.com/dholm/FlowUI>`_ 0.2.1 or later.

Currently (void)walker has support for the following architectures::

 * X86
 * X86-64
 * MIPS


Usage
-----

(void)walker can be loaded manually from within ``GDB`` by running::

    python from voidwalker import voidwalker

By adding the previous line to ``~/.gdbinit`` (void)walker will be loaded
automatically whenever ``GDB`` is launched.

Also register the following hooks in ``~/.gdbinit``::

    define hook-stop
        voidwalker hook-stop
    end


Commands
--------

Here follows a list of a few commands, see the ``README`` for a complete list.

Dumping the context of the current stack frame::

    voidwalker context

Dumping data by specifying address and length::

    voidwalker dump data <address> <length>

Dumping disassembly by specifying address and the number of instructions::

    voidwalker dump instructions <address> <length>
