# (void)walker

(void)walker is a toolbox for GDB which provides utilities for debugging
software on an instruction level. It is heavily influenced by the
[gdbinit](https://github.com/gdbinit/Gdbinit) by  *mammon_*, *elaine*, *fG!*
et al. but opens up for a much more advanced solution by using Python instead
of GDB commands.


## Requirements

GDB 7.5 or later built with support for Python extensions.

Currently (void)walker has support for the following architectures, but adding
new ones should be fairly easy at this point.

 * X86
 * X86-64
 * MIPS


## Installation

Put (void)walker somewhere on your system and simply add the following line to
your *~/.gdbinit*:

    python execfile('<path to voidwalker.py>')

The next time you start GDB you should see (void)walker being loaded.

You should also install all the (void)walker hooks in order to complete the
integration with GDB.


## Usage

Dumping the context of the current stack frame:

    voidwalker context

Dumping data by specifying address and length:

    voidwalker dump <address> <length>


### Hooks

(void)walker commands that are prefixed with *hook-* are intended to be put
into hooks of the same name in *~/.gdbinit*, for example:

    define hook-stop
        voidwalker hook-stop
    end


## Parameters

Changing themes:

    voidwalker-theme

For instance, to set Zenburn as the default theme instead of Solarized add the
following line to *~/.gdbinit*:

    set voidwalker-theme zenburn

Controlling what is shown as part of a context:

    voidwalker-context-stackdw <number of doublewords>
    voidwalker-context-instructions <number of instructions>

For instance, to suppress the stack from being dumped when calling *voidwalker
context* add the following line to ~/.gdbinit:

    set voidwalker-context-stackdw 0


## Themes

There is a theming system built in and the default theme is based on
Ethan Schoonover's color palette known as
[solarized](http://ethanschoonover.com/solarized).

The [Zenburn](http://slinky.imukuppi.org/zenburnpage/) theme is included as
well.


## License

(void)walker is distributed under the GPLv3 license, the same as GDB. See the
file called COPYING for the full license text.
