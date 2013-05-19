# (void)walker

(void)walker is a toolbox for GDB which provides utilities for debugging
software on an instruction level. It is heavily influenced by the
[gdbinit](https://github.com/gdbinit/Gdbinit) by  *mammon_*, *elaine*, *fG!*
et al. but opens up for a much more advanced solution by using Python instead
of GDB commands.

![(void)walker session](https://github.com/dholm/voidwalker/raw/master/screenshot.png)


## Requirements

 * [GDB](http://www.gnu.org/software/gdb/) 7.5 or later built with support for
   Python extensions.
 * [FlowUI](https://github.com/dholm/FlowUI) 0.2.1 or later.

Currently (void)walker has support for the following architectures, but adding
new ones should be fairly easy at this point.

 * X86
 * X86-64
 * MIPS


## Installation

Install the requirements using pip:

    pip install -r requirements.txt

Install (void)walker using the supplied *setup.py* by executing:

    python setup.py install

Finally add the following line to your *~/.gdbinit* to have it loaded
automatically whenever GDB is launched:

    python from voidwalker import voidwalker

The next time you start GDB you should see (void)walker being loaded.

You should also install all the (void)walker hooks in order to complete the
integration with GDB.


## Usage

Dumping the context of the current stack frame:

    voidwalker context

Dumping data by specifying address and length:

    voidwalker dump data <address> <length>

Dumping disassembly by specifying address and the number of instructions:

    voidwalker dump instructions <address> <length>

Set a breakpoint at the start of the .text section. This command can be useful
in setting a breakpoint at start if no symbols are available.

    voidwalker gdb break text

The following commands can be used to patch the loaded binary. All
modifications are applied on the loaded binary and the original file is never
touched.

    voidwalker patch snippet list
	voidwalker patch snippet apply <name> <address>


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

Modifying what is performed when hooks are executed by GDB:

    voidwalker-hook-context <on/off>


## License

(void)walker is distributed under the GPLv3 license, the same as GDB. See the
file called COPYING for the full license text.
