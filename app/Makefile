MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MKFILE_DIR := $(dir $(MKFILE_PATH))

BINDIR := $(MKFILE_DIR)bin
OBJDIR := $(MKFILE_DIR)obj
INCDIR := $(MKFILE_DIR)inc
SRCDIR := $(MKFILE_DIR)src

EXENAME := conway
EXEPATH := $(BINDIR)/$(EXENAME).gb
SYMPATH := $(BINDIR)/$(EXENAME).sym
MAPPATH := $(BINDIR)/$(EXENAME).map

SRCPATHS := main.asm oam.asm input.asm help.asm menu.asm draw.asm play.asm

OBJPATHS := $(foreach path,$(notdir $(SRCPATHS)),$(OBJDIR)/$(path:.asm=.o))

all : $(EXEPATH)

$(EXEPATH) : $(OBJPATHS)
	@mkdir -p "$$(dirname $@)"
	@rgblink -m $(MAPPATH) -n $(SYMPATH) -o $(EXEPATH) $(OBJPATHS)
	@rgbfix -v -p 0xFF $(EXEPATH)

$(OBJDIR)/%.o : $(SRCDIR)/%.asm
	@mkdir -p "$$(dirname $@)"
	@rgbasm -o $@ $< -I$(INCDIR) -I$(SRCDIR)

clean:
	@if [ -d $(BINDIR) ]; then rm -r $(BINDIR); fi
	@if [ -d $(OBJDIR) ]; then rm -r $(OBJDIR); fi