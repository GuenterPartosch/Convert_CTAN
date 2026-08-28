#!/usr/bin/python3
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# 2.11   2026-07-22 __doc__ text for module
# 2.13    2026-07-25 Break the function 'make_calls' into some functions.
# 2.13.1  2026-07-25 Definition of the new functionsn make_call_load(),
#                    make_call_check(), make_call_output(),
#                    make_call_compile(), make_call_regeneration()
# 2.13.4  2026-07-26 Take into account changes to the module’s __doc__
#                    text.

"""
CTANLoadOut.py
(C) Günter Partosch, 2021-2026

CTANLoadOut.py is part of the CTAN bundle (CTANLoad.py, CTANOut.py,
CTANLoadOut.py, menu_CTANLoadOut.py).

CTANLoadOut.py combines the tasks of CTANLoayd.py and CTANOut.py:

CTANLoad.py: Loads XLM and PDF documentation files from CTAN a/o
             generates some special lists, and prepares data for
             CTANOut.
CTANOut.py:  Converts CTAN XLM package files to LaTeX, RIS, plain,
             BibLaTeX, Excel [tab separated].

CTANLoadOut.py must be located in the same OS directory as CTANLoad.py
and CTANOut.py.

Start of CTANLoadOut.py:
-----------------------
1. python -u CTANLoadOut.py <option(s)>
   -- always works
2. CTANLoadOut.py <option(s)>
    -- if the OS knows how to handle Python files (files with the name
       extension .py)
3. there is probably no executable
4. menu_CTANLoadOut.py

Requirements:
------------
+ operating system windows 10/11 or Linux (like Linux Mint or Ubuntu or
  Debian)
+ CVTANLoad.py and CTANOut.py are in the same directory.
+ wget a/o wget2 is installed (and accessible via the path)
+ Python installation 3.10 or newer
+ a series of Python modules (see the import instructions below)

Class:
-----
dataclass_variable          data class 

with method:
-----------
report                      Outputs the current values of the variables
                            defined in 'dataclass_variable'.

Functions:
---------
argparse_postprocessing(dc=dc_var)  Postprocesses some parameters for
                                    the program CTANOutLoad.
argparse_process(dc=dc_var)	    Defines the arguments for the program
                                    CTANLoadOut and starts it.                                        
fold(s:str, dc=dc_var) ->str	    auxiliary function: Shortens/foldens
                                    long option values for output.                                       
func_call_check(dc=dc_var)	    CTANLoad (Check) is processed.                                         
func_call_compile(dc=dc_var)	    Compiles the generated LaTeX source
                                    file with LuaLaTeX.                                         
func_call_load(dc=dc_var) 	    CTANLoad (for loading) is processed.                                         
func_call_output(dc=dc_var)	    CTANOut is processed.                                        
func_call_regeneration(dc=dc_var)   CTANLoad (Regeneration) is processed.                                   
head(dc=dc_var)	                    Shows the given options.                                                    
main(dc=dc_var)	                    Main Function	                                                   
make_call_load(dc=dc_var)	    Constructs the call for loading (
                                    call_load).
make_call_check(dc=dc_var)	    constructs the call for checking
                                    (call_check).
make_call_output(dc=dc_var)	    Constructs the call for output
                                    generating (call_output).
make_call_compile(dc=dc_var)	    Constructs the calls for compiling and
                                    index.
make_call_regeneration(dc=dc_var)   Constructs the call for regeneration
                                    (call_regneration).
pre_make_calls(dc=dc_var)	    Prepares dc.callx and a few other
                                    variables for processing by
                                    'make_calls'.                                          
remove_LaTeX_file(t:str, dc=dc_var) auxiliary function: Removes named
                                    LaTeX file.                                
remove_other_file(t:str, dc=dc_var) auxiliary function: Removes named
                                    other file.                                

See also:
--------
+ installation.txt
+ firststeps.txt
+ call.txt
+ wget.txt
+ CTAN-files.txt
+ CTAN-corrected-files.txt
+ CTAN-elements.txt

+ CTANLoadOut-changes.txt
+ CTANLoadOut-messages.txt
+ CTANLoadOut.man
+ CTANLoadOut-examples.txt
+ CTANLoadOut-examples.bat
+ CTANLoadOut-modules.txt
"""


#===================================================================
# Modules needed

# 2.5    2026-07-17 backtracing
# 2.5.1  2026-07-17 new module traceback
# 2.6    2026-07-18 data class used
# 2.6.0  2026-07-18 new module dataclasses imported

import argparse                                                         # argument parsing
import sys                                                              # system calls
import platform                                                         # getting OS informations
import subprocess                                                       # handling of sub-processes
import re                                                               # regular expression
import os                                                               # deleting a file on disk, for instance
from os import path                                                     # path informations
##import codecs                                                           # needed for full UTF-8 output# on stdout
import time                                                             # gets time|date of a file
from tempfile import TemporaryFile                                      # temporary file for subprocess.run
import traceback                                                        # error backtracing
from dataclasses import dataclass, field                                # Python data classes are used


#===================================================================
# Settings: Defaults and constants

# 2.3     2026-07-16 actTime -> ACT_TIME; actDate -> ACT_DATE (and is
#                    therefore recognisable as a constant)
# 2.14    2026-08-19 Avoid compiling LaTeX files with no real content
# 2.14.1  2026-08-19 new constant MIN_TEX_SIZE

PROGRAMNAME_EXT   = "CTANLoadOut.py"                                    # program name (with extension)
PROGRAMNAME       = "CTANLoadOut"
PROGRAM_VERSION   = "2.17"
PROGRAM_DATE      = "2026-08-22"
PROGRAM_AUTHOR    = "Günter Partosch"
AUTHOIR_EMAIL     = "Guenter.Partosch@web.de\n(formerly " +\
                     "Guenter.Partosch@hrz.uni-giessen.de)"
AUTHOR_INST       = "formerly " + \
                    "Justus-Liebig-Universität, Hochschulrechenzentrum"

OPERATING_SYS:str = platform.system()                                   # Operating system on which the program runs
ACT_DATE:str      = time.strftime("%Y-%m-%d")                           # actual date of program execution
ACT_TIME:str      = time.strftime("%X")                                 # actual time of program execution
EMPTY_SET         = set()                                               # set without any element

LATEX_PROCESSOR   = "lualatex"                                          # default LaTeX processor
INDEX_PROCESSOR   = "makeindex"                                         # default index processor

EMPTY             = ""
SPACE             = " "
ELLIPSIS          = " ..."

LEFT              = 35                                                  # width of labels in verbose output
SEPLINE_LENGTH    = 80                                                  # length of separation line in output
MIN_TEX_SIZE      = 2960                                                # minimal size of LaTeX files

ERR_MODE          = "[CTANLoadOut] Warning: '{0} {1}' changed to " +\
                    "'{2}' " + "(due to {3})"
LATEX_FILES       = [".aux", ".bib", ".ilg", ".log", ".idx", ".ilg",
                     ".ind", ".out", ".tex", ".pdf", ".stat", ".tap",
                     ".top", ".xref"]
OTHER_FILES       = [".ris", ".bib", ".txt", ".tsv"]

# ------------------------------------------------------------------
# Texts for argument parsing (argparse) and help

# 1.50.2 2024.04-23 new global variables: TIMEOUT_DEFAULT and
#                   TIMEOUT_TEXT
# 1.50.3 2024.04-23 new section in arparse processing: new options
#                   -tout and--timeout + corr. assigmnent to timeout
# 1.54   2024-06-12 some texts for -h and arparse changed
# 1.60   2025-11-03 argparse texts revised (x)
# 1.61   2025-11-17 texts changed: MAKE_OUTPUT_TEXT, PDF_OUTPUT_TEXT

AUTHOR_LOAD_TEMPLATE_TEXT = "[CTANLoad} Name template for authors"      # option -Al
AUTHOR_OUT_TEMPLATE_TEXT  = "[CTANOut} Name template for authors"       # option -Ao
AUTHOR_TEMPLATE_TEXT      = "[CTANLoad and CTANOut] General name " +\
                            "template for authors"                      # option -A

LICENSE_LOAD_TEMPLATE_TEXT= "[CTANLoad] Name template for licenses"     # option -Ll
LICENSE_OUT_TEMPLATE_TEXT = "[CTANOut] Name template for licenses"      # option -Lo
LICENSE_TEMPLATE_TEXT     = "[CTANLoad and CTANOut] General name " +\
                            "template for licenses"                     # option -L

KEY_LOAD_TEMPLATE_TEXT    = "[CTANLoad] Template for keys"              # option -kl
KEY_OUT_TEMPLATE_TEXT     = "[CTANOut] Template for keys"               # option -ko
KEY_TEMPLATE_TEXT         = "[CTANLoad and CTANOut] General " +\
                            "template for keys"                         # option -k

NAME_LOAD_TEMPLATE_TEXT   = "[CTANLoad] Template for package names"     # option -tl
NAME_OUT_TEMPLATE_TEXT    = "[CTANOut] Template for package names"      # option -to
NAME_TEMPLATE_TEXT        = "[CTANLoad and CTANOut] General " +\
                            "template for package names"                # option -t

YEAR_TEMPLATE_TEXT        = "[CTANLoad and CTANOut] General " +\
                            "template for years"                        # option -y
YEAR_LOAD_TEMPLATE_TEXT   = "[CTANLoad] Template for years"             # option -yl
YEAR_OUT_TEMPLATE_TEXT    = "[CTANOut] Template for years"              # option -yo

AUTHOR_TEXT               = "[CTANLoadOut] Flag: Show author of " +\
                            "the program and exit."                     # option -a
DOWNLOAD_TEXT             = "[CTANLoad] Flag: Download associated " +\
                            "documentation files [PDF]."                # option -f

INTEGRITY_TEXT            = "[CTANLoad, check] Flag: Check the " +\
                            "integrity of the 2nd .pkl file."           # option -c


LISTS_TEXT                = "[CTANLoad, Check] Flag: Generate some s" +\
                            "pecial lists and prepare files " +\
                            "for CTANOut."                              # option -l
MAKE_OUTPUT_TEXT          = "[CTANLoadOut] Flag: Do not activate " +\
                            "CTANLoad."                                 # option -mo
NO_FILES_TEXT             = "[CTANOut] Flag: Do not generate " +\
                            "output files."                             # option -nf
PDF_OUTPUT_TEXT           = "[CTANOut] Flag: Generate PDF output " +\
                            "using LuaLaTeX."                           # option -p

REGENERATE_TEXT           = "[CTANLoad, check] Flag: Regenerate " +\
                            "the two pickle files."                     # option -r
STATISTICS_TEXT           = "[CTANLoadOut] Flag: Statistics on " +\
                            "terminal"                                  # option -stat
TOPICS_TEXT               = "[CTANOut] Flag: Generate topic " + \
                            "lists [meaning of topics + " +\
                            "cross-reference (topics/packages, " +\
                            "authors/packages); only for -m LaTeX]."    # option -mt
VERBOSE_TEXT              = "[CTANLoadOut] Flag: Output is verbose."    # option -v
VERSION_TEXT              = "[CTANLoadOut] Flag: Show version of " +\
                            "the program and exit."                     # option -V

BTYPE_TEXT                = "[CTANOut] Type of BibLaTex entries " +\
                            "to be generated [valid only for " +\
                            "'-m BibLaTeX'/'--mode BibLaTeX']"          # option -b
DIREC_TEXT                = "[CTANLoad and CTANOut] OS folder " +\
                            "(directory) for input and output files"    # option -d
MODE_TEXT                 = "[CTANOut] Target format"                   # option -m
NUMBER_TEXT               = "[CTANLoad] Maximum number of XML " +\
                            "and PDF file downloads"                    # option -n
OUTPUT_TEXT               = "[CTANLoad and CTANOut] Generic name " +\
                            "for output files [without extensions]"     # option -o
SKIP_TEXT                 = "[CTANOut] Skip specified CTAN fields."     # option -s
SKIP_BIBLATEX_TEXT        = "[CTANOut] Skip specified BibLaTeX fields." # option -sb
TIMEOUT_TEXT              = "[CTANLoad and CTANOut] default " +\
                            "timeout (sec) for subprocesses"            # option -tout

PROGRAM_TEXT              = "Combines the tasks of CTANLoad  and " +\
                            "CTANOut:\nCTANLoad: Loads XLM and PDF " +\
                            "documentation files from CTAN a/o " +\
                            "generates some special lists, and " + \
                            "prepares data for CTANOut.\n CTANOut: " +\
                            "Converts CTAN XLM package files to " +\
                            "some formats."

# ------------------------------------------------------------------
# Defaults/variables for argparse

# 1.50.2 2024.04-23 new global variables: TIMEOUT_DEFAULT and
#                   TIMEOUT_TEXT
# 1.50.3 2024.04-23 new section in arparse processing: new options
#                   -tout and --timeout + corr. assigmnent to timeout

AUTHOR_TEMPLATE_DEFAULT      = """^.+$"""                               # default for author name template (-A)
AUTHOR_LOAD_TEMPLATE_DEFAULT = EMPTY                                    # default for author load name template (-Al)
AUTHOR_OUT_TEMPLATE_DEFAULT  = AUTHOR_TEMPLATE_DEFAULT                  # default for author out name template (-Ao)

LICENSE_TEMPLATE_DEFAULT     = """^.+$"""                               # default for license name template (-L)
LICENSE_LOAD_TEMPLATE_DEFAULT= EMPTY                                    # default for license load name template (-Ll)
LICENSE_OUT_TEMPLATE_DEFAULT = LICENSE_TEMPLATE_DEFAULT                 # default for license out name template (-Lo)

KEY_TEMPLATE_DEFAULT         = """^.+$"""                               # default for option -k
KEY_LOAD_TEMPLATE_DEFAULT    = EMPTY                                    # default for option -kl
KEY_OUT_TEMPLATE_DEFAULT     = KEY_TEMPLATE_DEFAULT                     # default for option -ko

NAME_TEMPLATE_DEFAULT        = """^.+$"""                               # default for option -t
NAME_LOAD_TEMPLATE_DEFAULT   = EMPTY                                    # default for option -tl
NAME_OUT_TEMPLATE_DEFAULT    = NAME_TEMPLATE_DEFAULT                    # default for option -to

YEAR_TEMPLATE_DEFAULT        = """^19[89][0-9]|20[012][0-9]$"""         # default for year template (-y) [four digits]
YEAR_LOAD_TEMPLATE_DEFAULT   = EMPTY                                    # default for year_load_template (-yl) [four digits]
YEAR_OUT_TEMPLATE_DEFAULT    = YEAR_TEMPLATE_DEFAULT                    # default for year_out_template (-yo) [four digits]

BTYPE_DEFAULT                = "@online"                                # default for option -b (BibLaTeX entry type)
MODE_DEFAULT                 = "RIS"                                    # default for option -m
NUMBER_DEFAULT               = 250                                      # default for option -n (maximum number of files to be loaded)
OUTPUT_NAME_DEFAULT          = "all"                                    # default for option -o (generic file name)
SKIP_DEFAULT                 = "[]"                                     # default for option -s
SKIP_BIBLATEX_DEFAULT        = "[]"                                     # default for option -sb
TIMEOUT_DEFAULT              = 60                                       # default for option -tout

DOWNLOAD_DEFAULT             = False                                    # flag: download PDF files (option -f)
INTEGRITY_DEFAULT            = False                                    # flag: integrity check (option -c)
LISTS_DEFAULT                = False                                    # flag: generate special lists (option -l)
MAKE_OUTPUT_DEFAULT          = False                                    # Flag: generate only output (RIS, LaTeX, BibLaTeX, Excel, plain)
MAKE_TOPICS_DEFAULT          = False                                    # flag: make topics output (option -mt)
NO_FILES_DEFAULT             = False                                    # flag: no output files (option -nf)
PDF_OUTPUT_DEFAULT           = False                                    # flag: produce PDF output (option -p)
REGENERATE_DEFAULT           = False                                    # flag: regenerate pickle files (option -r)
STATISTICS_DEFAULT           = False                                    # flag: output statistics (option -stat)
VERBOSE_DEFAULT              = False                                    # flag: output is verbose (option -v)
DEBUGGING_DEFAULT            = False                                    # flag: debugging (option -dbg)

ACT_DIREC                    = "."                                      # actual folder (directory) on OS (Windows|Linux)

# ------------------------------------------------------------------
# used in menu_CTANLoadOut.py

ALL_DEF1 = (AUTHOR_TEMPLATE_DEFAULT, AUTHOR_LOAD_TEMPLATE_DEFAULT,
            AUTHOR_OUT_TEMPLATE_DEFAULT, LICENSE_TEMPLATE_DEFAULT,
            LICENSE_LOAD_TEMPLATE_DEFAULT, LICENSE_OUT_TEMPLATE_DEFAULT,
            KEY_TEMPLATE_DEFAULT, KEY_LOAD_TEMPLATE_DEFAULT,
            KEY_OUT_TEMPLATE_DEFAULT, NAME_TEMPLATE_DEFAULT,
            NAME_LOAD_TEMPLATE_DEFAULT, NAME_OUT_TEMPLATE_DEFAULT,
            YEAR_TEMPLATE_DEFAULT, YEAR_LOAD_TEMPLATE_DEFAULT,
            YEAR_OUT_TEMPLATE_DEFAULT)
ALL_DEF2 = (BTYPE_DEFAULT, MODE_DEFAULT, NUMBER_DEFAULT,
            OUTPUT_NAME_DEFAULT, SKIP_DEFAULT, SKIP_BIBLATEX_DEFAULT,
            TIMEOUT_DEFAULT)
ALL_DEF3 = (DOWNLOAD_DEFAULT, INTEGRITY_DEFAULT, LISTS_DEFAULT,
            MAKE_OUTPUT_DEFAULT, MAKE_TOPICS_DEFAULT, NO_FILES_DEFAULT,
            PDF_OUTPUT_DEFAULT, REGENERATE_DEFAULT, STATISTICS_DEFAULT,
            VERBOSE_DEFAULT, DEBUGGING_DEFAULT)

# ------------------------------------------------------------------
SET_LOAD         = {'-A', '--author_template', '-Al',
                    '--author_load_template', '-L',
                    '--license_template',  '-Ll',
                    '--license_load_template', '-f',
                    '--download_files', '-k', '--key_template',
                    '-kl', '--key_load_template', '-n', '--number',
                    '-t', '--template', '-tl', '--template_load',
                    '-dbg', '--debugging', '-y', '--year_template',
                    '-yl', '--year_load_template'}                      # possible Arguments for load
SET_CHECK        = {'-c','--check_integrity', '-l','--lists'}           # possible arguments for check
SET_OUTPUT       = { '-A', '--author_template', '-Ao',
                     '--author_out_template', '-b', '--btype', '-k',
                     '--key_template', '-ko', '--key_out_template',
                     '-L', '--license_template', '-Lo',
                     '--license_out_template', '-m', '--mode', '-mo',
                     '--make_output', '-mt', '--make_topics', '-s',
                     '--skip', '-sb', '--skip_biblatex' '-t',
                     '--template', '-to', '--template_out', '-dbg',
                     '--debugging', '-nf', 'no_files', '-y',
                     '--year_template', '-yo', '--year_out_template'}   # possible arguments for output
SET_COMPILE      = {'-p', '--pdf_output'}                               # possible arguments for compile
SET_REGENERATION = {'-r', '--regenerate_pickle_files' }                 # possible arguments for regeneration

# ------------------------------------------------------------------
# 2.4    2026-07-16 encoding for subprocesses depends on operating
#                   system now

if OPERATING_SYS == "Windows":
    DIREC_SEP      = "\\"
    ENC            = "cp1252"                                           # Standard encoding in Windows
else:
    DIREC_SEP      = "/"
    ENC            = "utf-8"                                            # Standard encoding in Linux

DIREC_DEFAULT      = ACT_DIREC + DIREC_SEP                              # default for -d (OS output folder)


#===================================================================
# data class

# 2.6    2026-07-18 data class used
# 2.6.1  2026-07-18 new class dataclass-variable (including all globally
#                   used variables) defined
# 2.8    2026-07-19 data class dataclass_variable: converted to the
#                   existing global constants
# 2.9    2026-07-19 timout is float now

@dataclass
class dataclass_variable():                                             # class dataclass_variable
    """
    The ‘@dataclass’ decorator marks this class as a data class. In our
    case, ‘dataclass_variable’ is used to store the overall state of the
    system (including all globally used variables). The relevant
    variables are defined in the class; qualified access is achieved via
    an instance of the class.

    Methods:
    -------
    a) In 'dataclass_variable', a number of methods are automatically
       implemented, such as .__init__(), .__repr__() and .__eq__().
    b) user-defined method .report(): outputs the current values of the
       variables defined in 'dataclass_variable'.

    Example:
    -------
    a) Definition and initialisation: name_template:str = EMPTY
    b) later: dc_var = dataclass_variable()
    c) access: dc_var.name_template ...
    """

    # options for argparse
    # ------------------------------------------------------------------
    author_load_template:str    = AUTHOR_LOAD_TEMPLATE_DEFAULT          # option -Al    (author template for load)
    author_out_template:str     = AUTHOR_TEMPLATE_DEFAULT               # option -Ao    (author template for output)
    author_template:str         = AUTHOR_TEMPLATE_DEFAULT               # option -A     (author template)

    btype:str                   = BTYPE_DEFAULT                         # option -b     (Type of BibLaTex entries to be generated)
    debugging:bool              = DEBUGGING_DEFAULT                     # option -dbg   (Flag: debugging)
    direc:str                   = DIREC_DEFAULT                         # option -d     (name of the OS directory)
    download:bool               = DOWNLOAD_DEFAULT                      # option -f     (Flag: PDF download)
    integrity:bool              = INTEGRITY_DEFAULT                     # option -c     (Flag: integrity check)

    key_load_template:str       = KEY_LOAD_TEMPLATE_DEFAULT             # option -kl    (key template) for load
    key_out_template:str        = KEY_TEMPLATE_DEFAULT                  # option -ko    (key template for output)
    key_template:str            = KEY_TEMPLATE_DEFAULT                  # option -k     (key template)

    license_load_template:str   = LICENSE_LOAD_TEMPLATE_DEFAULT         # option -Ll    (license name template for load)
    license_out_template:str    = LICENSE_TEMPLATE_DEFAULT              # option -Lo    (license name template for output)
    license_template:str        = LICENSE_TEMPLATE_DEFAULT              # option -L     (license name template)

    lists:bool                  = LISTS_DEFAULT                         # option -n     (Flag: special lists are generated)
    make_output:bool            = MAKE_OUTPUT_DEFAULT                   # option -mo    (Flag: generate only output (RIS, LaTeX, BibLaTeX, Excel, plain))
    make_topics:bool            = MAKE_TOPICS_DEFAULT                   # option -mt    (Flag: make topics output)
    mode:str                    = MODE_DEFAULT                          # option -m     (target format)

    name_load_template:str      = NAME_LOAD_TEMPLATE_DEFAULT            # option -tl    (name template for output files for load)
    name_out_template:str       = NAME_TEMPLATE_DEFAULT                 # option -to    (name template for output files for output)
    name_template:str           = NAME_TEMPLATE_DEFAULT                 # option -t     (name template for output files)

    no_files:bool               = NO_FILES_DEFAULT                      # option -nf    (Flag: no output files)
    number:int                  = NUMBER_DEFAULT                        # option -n     (maximum number of files for loading)
    output_name:str             = OUTPUT_NAME_DEFAULT                   # option -o     (generic file name)
    pdf_output:bool             = PDF_OUTPUT_DEFAULT                    # option -p     (Flag: produce PDF output)
    regenerate:bool             = REGENERATE_DEFAULT                    # option -r     (pickle files are to be regenerated)
    skip:list                   = field(default_factory=list)           # option -s     (Skip specified CTAN fields)
    skip_biblatex:list          = field(default_factory=list)           # option -sb    (Skip specified BibLaTeX fields)
    statistics:bool             = STATISTICS_DEFAULT                    # option -stat  (statistics output)
    timeout:float               = TIMEOUT_DEFAULT                       # option -tout
    verbose:bool                = VERBOSE_DEFAULT                       # option -v     (Flag: output is verbose)

    year_load_template:str      = YEAR_LOAD_TEMPLATE_DEFAULT            # option -yl    (year template for load)
    year_out_template:str       = YEAR_TEMPLATE_DEFAULT                 # option -yo    (year template for output)
    year_template:str           = YEAR_TEMPLATE_DEFAULT                 # option -y     (year template)

    timeout10:float             = timeout * 10                          # timeout * 10
    timeout5:float              = timeout * 5                           # timeout * 5

    # ------------------------------------------------------------------
    # program call
    call:list                   = field(default_factory=list)           # list with program arguments
    callx:set                   = field(default_factory=set)            # set with original a/o computed arguments

    # ------------------------------------------------------------------
    # collection with options for different states
    call_check:list             = field(default_factory=list)           # collection with options for check
    call_compile:list           = field(default_factory=list)           # collection with options for compile
    call_index:list             = field(default_factory=list)           # collection with options for index
    call_load:list              = field(default_factory=list)           # collection with options for load
    call_output:list            = field(default_factory=list)           # collection with options for output
    call_regeneration:list      = field(default_factory=list)           # collection with options for regeneration

    # ------------------------------------------------------------------
    # program states
    check:bool                  = False                                 # flag: CTANLOad, check
    compile:bool                = False                                 # flag: compilation
    load:bool                   = False                                 # flag: CTANLOad, load
    regeneration:bool           = False                                 # flag: CTANLOad, regeneration
    output:bool                 = False                                 # flag: CTANOut

    delete_temporary_file:bool  = False                                 # flag: temporary files are removed

    # ------------------------------------------------------------------
    def report(self, full:bool=False):                                  # method dataclass_variable.report
        """
        Outputs the current values of the variables defined in the class
        'dataclass_variable'.

        Parameter:
        ---------
        full : bool:
               if True, all menbers of sets, lists, tuples, and
               dictionaries, else only the lengths.
               default: False

        Messages:
        --------
        There are no specific messages.
        """

        tmp = dir(self)
        for f in tmp:
            tmp2 = eval("self." + f)
            if isinstance(tmp2, (set, dict, list, tuple)) and not full:
                tmp3 = len (tmp2)
            else:
                tmp3 = tmp2
            if (not "__" in f) and (f != 'report'):
                print(f"{f:<22} {tmp3}")

# ------------------------------------------------------------------
# 2.6    2026-07-18 data class used
# 2.6.1  2026-07-18 new class dataclass-variable (including all globally
#                   used variables) defined
# 2.6.2  2026-07-18 instance "dc_var" of this class created

dc_var = dataclass_variable()                                           #  new instance of the data class dataclass_variabl


#===================================================================
# Auxiliary functions

# ------------------------------------------------------------------
def fold(s:str, dc=dc_var) ->str:                                       # function fold
    """
    auxiliary function: Shortens/foldens long option values for output.

    Parameters:
    ----------
    s:  string
        string to be folded
        no default
    dc  instance of the data class 'dataclass_variable'
        default: dc_var

    Returns:
    -------
    Returns the folded/shortened string.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    + dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

# 2.6    2026-07-18 data class used
# 2.6.3  2026-07-18 if necessary: Function definitions supplemented by
#                   the parameter "dc=dc_var"
# 2.6.4  2026-07-18 relevant local variables prefixed with "dc." and/or
#                   non-local with "dc_var"   
# 2.6.6  2026-07-18 "global" statements removed
# 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the data class

    if dc.debugging:
        print("+++ +CTANLoadOut:fold")                                  # -dbg

    OFFSET   = 79 * SPACE
    MAXLEN   = 70
    SEP      = "|"
    parts    = s.split(SEP)
    line:str = EMPTY
    out:str  = EMPTY
    
    for f in range(0, len(parts) ):
        if f != len(parts) - 1:
            line = line + parts[f] + SEP
        else:
            line = line + parts[f]
        if len(line) >= MAXLEN:
            out = out +line+ "\n" + OFFSET
            line = EMPTY
    out = out + line
    return out

# ------------------------------------------------------------------
def remove_LaTeX_file(t:str, dc=dc_var):                                # function remove_LaTeX_file
    """
    auxiliary function: Removes named LaTeX file.

    Parameters:
    ----------
    t:  str
        name of the file to be removed (str)
        no default
    dc  instance of the data class 'dataclass_variable'
        default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    + dc.debugging	         option -dbg (Flag: debugging)
    + dc.delete_temporary_file	 flag: temporary files are removed
    + dc.output_name	         option -o (generic file name)

    Message:
    -------
    + Warning: LaTeX file '{dc.output_name + t}' removed
    """

# 2.6    2026-07-18 data class used
# 2.6.3  2026-07-18 if necessary: Function definitions supplemented by
#                   the parameter "dc=dc_var"
# 2.6.4  2026-07-18 relevant local variables prefixed with "dc." and/or
#                   non-local with "dc_var"   
# 2.6.6  2026-07-18 "global" statements removed
# 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the data class

    if dc.debugging:
        print("+++ >CTANLoadOut:remove_LaTeX_file")                     # -dbg

    if dc.delete_temporary_file:
        if t in LATEX_FILES:
            if path.exists(dc.output_name + t):
                os.remove(dc.output_name + t)
                if dc.delete_temporary_file:
                    print("[CTANLoadOut] Warning: LaTeX file",
                          f" '{dc.output_name + t}' removed")
            else:
                pass

    if dc.debugging:
        print("+++ <CTANLoadOut:remove_LaTeX_file")                     # -dbg

# ------------------------------------------------------------------
def remove_other_file(t:str, dc=dc_var):                                # function remove_other_file
    """
    auxiliary function: Removes named other file.

    Parameters:
    ----------
    t:  str
        name of the file to be removed (str)
        no default
    dc  instance of the data class 'dataclass_variable'
        default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    + dc.debugging	         option -dbg (Flag: debugging)
    + dc.delete_temporary_file	 flag: temporary files are removed
    + dc.output_name	         option -o (generic file name)
    + dc.verbose	         option -v (Flag: output is verbose)

    Message:
    -------
    + Warning: file '{dc.output_name + t}' removed.
    """

# 2.6    2026-07-18 data class used
# 2.6.3  2026-07-18 if necessary: Function definitions supplemented by
#                   the parameter "dc=dc_var"
# 2.6.4  2026-07-18 relevant local variables prefixed with "dc." and/or
#                   non-local with "dc_var"   
# 2.6.6  2026-07-18 "global" statements removed
# 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the data class

    if dc.debugging:
        print("+++ >CTANLoadOut:remove_other_file")                     # -dbg

    if dc.delete_temporary_file:
        if t in OTHER_FILES:
            if path.exists(dc.output_name + t):
                os.remove(dc.output_name + t)
                if dc.verbose:
                    print("[CTANLoadOut] Warning: file",
                          f" '{dc.output_name + t}' removed")
            else:
                pass

    if dc.debugging:
        print("+++ <CTANLoadOut:remove_other_file")                     # -dbg


#===================================================================
# Parsing the arguments
# + Defines the arguments for the program CTANLoadOut
# + Gets parsed options

# 1.50   2024-04-23 timeout management revised
# 1.50.3 2024.04-23 new section in arparse processing: new options
#                   -tout and --timeout + corr. assigmnent to timeout
# 1.53   2024-06-11 additional values for -m: tsv, csv
# 1.55   2024-07-20 argparse revised
# 1.55.1 2024-07-20 additional parameter in .ArgumentParser: prog,
#                   epilog, formatter_class
# 1.55.2 2024-07-20 subdivision into groups by .add_argument_group
# 1.55.3 2024-07-20 additional arguments in .add_argument (if it
#                   makes sense): type, metavar, action, dest
# 1.59   2025-11-03 new: argparse groups
# 1.60   2025-11-03 argparse texts revised

# ------------------------------------------------------------------
def argparse_process(dc=dc_var):                                        # function argparse_process
    """
    Defines the arguments for the program CTANLoadOut and starts it.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Workflow:
    --------
    + defines program parameter/options
    + gets parsed options

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.author_load_template   option -Al  (author template for load)
    + dc.author_out_template    option -Ao  (author template for output)
    + dc.author_template        option -A   (general author template)
    + dc.btype                  option -b
    + dc.debugging	        option -dbg (Flag: debugging)
    + dc.direc	                option -d   (name of the OS directory)
    + dc.download	        option -f   (Flag: PDF download)
    + dc.integrity	        option -c   (Flag: integrity check)
    + dc.key_load_template	option -kl  (key template for load)
    + dc.key_out_template	option -ko  (key template for output)
    + dc.key_template	        option -k   (general key template)
    + dc.license_load_template	option -Ll  (license name template for
                                            load)
    + dc.license_out_template	option -Lo  (license name template for
                                            output)
    + dc.license_template	option -L   general license name template)
    + dc.lists	                option -n   (Flag: special lists are
                                            generated)
    + dc.make_output	        option -mo  (Flag: CTANLoad is not
                                            started)
    + dc.make_topics	        variable for -mt (Flag:  topic lists are
                                            generated
    + dc.mode	                variable for -m (mode)
    + dc.name_load_template     option -tl  (name template for output
                                            files for load)
    + dc.name_out_template      option -to  (name template for output
                                            files for output)
    + dc.name_template	        option -t   (general name template for
                                            output files)
    + dc.no_files	        variable for -nf (Flag: files are not
                                            generated)
    + dc.number	                option -n   (maximum number of files for
                                            loading)
    + dc.output_name	        option -o   (generic file name)
    + dc.pdf_output	        option -p   (Flag: PDF out is generated)
    + dc.regenerate	        option -r   (pickle files are to be
                                            regenerated)
    + dc.skip	                variable for -s (specified CTAN fields are
                                            skipped)
    + dc.skip_biblatex	        variable for -sb (specified BibLaTeX
                                            fields are skipped)
    + dc.statistics	        option -stat  (statistics output)
    + dc.timeout	        option -tout (timeout)
    + dc.timeout10	        timeout *10
    + dc.timeout5	        timeout *5
    + dc.verbose	        option -v   (Flag: output is verbose)
    + dc.year_load_template	option -yl  (year template for load)
    + dc.year_load_template	option -yl  (year template for load)
    + dc.year_template	        option -y   (gheneral year template)

    Messages:
    --------
    There are no specific messages.
    """

# 2.7    2026-07-19 new functions (which group specific instructions)
# 2.7.1  2026-07-19 definitions of argparse_process,
#                   argparse_postprocessing, pre_make_calls, make_calls

    if dc.debugging:
        print("+++ >CTANLoadOut:argparse_process")                        # -dbg

    parser = argparse.\
             ArgumentParser(formatter_class = \
                        argparse.RawDescriptionHelpFormatter,
                        description     = f"{PROGRAMNAME}\nVersion:" +\
                        f" {PROGRAM_VERSION}" +\
                        f" ({PROGRAM_DATE})\n\n{PROGRAM_TEXT}  ",
                        prog    = PROGRAMNAME,
                        epilog  = "Thanks for using %(prog)s!",
                        )
    parser._optionals.title  = 'Global options (without any processing)'

    parser.add_argument("-a", "--author",                               # option -a/--author
                    help    = AUTHOR_TEXT,
                    action  = 'version',
                    version = PROGRAM_AUTHOR+" ("+AUTHOIR_EMAIL + ", "+\
                              AUTHOR_INST + ")")

    parser.add_argument("-dbg", "--debugging",                          # option -dbg/--debugging
                        help    = argparse.SUPPRESS,                    # will be suppressed in help
                        dest    = "debugging",
                        action  = "store_true",
                        default = DEBUGGING_DEFAULT)

    parser.add_argument("-V", "--version",                              # option -V/--version
                    help    = VERSION_TEXT,
                    action  = 'version',
                    version = '%(prog)s ' + PROGRAM_VERSION + " (" +\
                              PROGRAM_DATE + ")")

    # ..................................................................
    group1 = parser.add_argument_group("Other global options")

    group1.add_argument("-d", "--directory",                            # option -d/--directory
                        metavar = "<directory>",
                        help    = DIREC_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "direc",
                        action  = "store",
                        default = DIREC_DEFAULT)

    group1.add_argument("-mo", "--make_output",                         # option -mo/--make_output
                        help    = MAKE_OUTPUT_TEXT + " -- Default: " +\
                        "%(default)s",
                        dest    = "make_output",
                        action  = "store_true",
                        default = MAKE_OUTPUT_DEFAULT)

    group1.add_argument("-o", "--output",                               # option -o/--output
                        metavar = "<output name>",
                        help    = OUTPUT_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "output_name",
                        action  = "store",
                        default = OUTPUT_NAME_DEFAULT)

    group1.add_argument("-tout", "--timeout",                           # option -tout/--timeout
                        metavar = "<timeout>",
                        help    = TIMEOUT_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "timeout",
                        action  = "store",
                        type    = float,
                        default = TIMEOUT_DEFAULT)

    group1.add_argument("-stat", "--statistics",                        # option -stat/--statistics
                        help    = STATISTICS_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "statistics",
                        action  = "store_true",
                        default = STATISTICS_DEFAULT)

    group1.add_argument("-v", "--verbose",                              # option -v/--verbose
                        help    = VERBOSE_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "verbose",
                        action  = "store_true",
                        default = VERBOSE_DEFAULT)

    # ..................................................................
    group2 = parser.add_argument_group("Options for CTANLoad + CTANOut")

    group2.add_argument("-A", "--author_template",                      # option -A/--author_template
                    metavar = "author template",
                    help    = AUTHOR_TEMPLATE_TEXT + " -- Default: " +\
                             "%(default)s",
                    dest    = "author_template",
                    action  = "store",
                    default = AUTHOR_TEMPLATE_DEFAULT)

    group2.add_argument("-k", "--key_template",                         # option -k/--key_template
                        metavar = "<key template>",
                        help    = KEY_TEMPLATE_TEXT + " -- Default: " +\
                                  "%(default)s",
                        dest    = "key_template",
                        action  = "store",
                        default = KEY_TEMPLATE_DEFAULT)

    group2.add_argument("-L", "--license_template",                     # option -L/--license_template
                    metavar = "<license template>",
                    help    = LICENSE_TEMPLATE_TEXT + " -- Default: " +\
                              "%(default)s",
                    dest    = "license_template",
                    action = "store",
                    default = LICENSE_TEMPLATE_DEFAULT)

    group2.add_argument("-t", "--name_template",                        # option -t/--template
                    metavar = "<name template>",
                    help    = NAME_TEMPLATE_TEXT + " -- Default: " +\
                              "%(default)s",
                    dest    = "name_template",
                    action  = "store",
                    default = NAME_TEMPLATE_DEFAULT)

    group2.add_argument("-y", "--year_template",                        # option -y/--year_template
                    metavar = "<year template>",
                    help    = YEAR_TEMPLATE_TEXT + " -- Default: " +\
                              "%(default)s",
                    dest    = "year_template",
                    action  = "store",
                    default = YEAR_TEMPLATE_DEFAULT)

    # ..................................................................
    group3 = parser.add_argument_group("Options for CTANLoad")

    group3.add_argument("-Al", "--author_load_template",                # option -Al/--author_load_template
                        metavar = "<author load template>",
                        help    = AUTHOR_LOAD_TEMPLATE_TEXT + \
                                  " -- Default: " +  "%(default)s",
                        dest    = "author_load_template",
                        action  = "store",
                        default = AUTHOR_LOAD_TEMPLATE_DEFAULT)

    group3.add_argument("-f", "--download_files",                       # option -f/--download_files
                        help    = DOWNLOAD_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "download_files",
                        action  = "store_true",
                        default = DOWNLOAD_DEFAULT)

    group3.add_argument("-kl", "--key_load_template",                   # option -kl/--key_load_template
                        metavar = "<key load temolate>",
                        help    = KEY_LOAD_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "key_load_template",
                        action  = "store",
                        default = KEY_LOAD_TEMPLATE_DEFAULT)

    group3.add_argument("-Ll", "--license_load_template",               # option -Ll/--license_load_template
                        metavar = "<license load template>",
                        help    = LICENSE_LOAD_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "license_load_template",
                        action  = "store",
                        default = LICENSE_LOAD_TEMPLATE_DEFAULT)

    group3.add_argument("-n", "--number",                               # option -n/--number
                        metavar = "<number>",
                        help    = NUMBER_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "number",
                        action  = "store",
                        type    = int,
                        default = NUMBER_DEFAULT)

    group3.add_argument("-tl", "--name_load_template",                  # option -tl/--template_load
                        metavar = "<name load template>",
                        help    = NAME_LOAD_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "name_load_template",
                        action  = "store",
                        default = NAME_LOAD_TEMPLATE_DEFAULT)

    group3.add_argument("-yl", "--year_load_template",                  # option -yl/--year_load_template
                        metavar = "<year load template>",
                        help    = YEAR_LOAD_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "year_load_template",
                        action  = "store",
                        default = YEAR_LOAD_TEMPLATE_DEFAULT)

    # ..................................................................
    group4 = parser.add_argument_group("Options for CTANOut")

    group4.add_argument("-Ao", "--author_out_template",                 # option -Ao/--author_out_template
                        metavar = "<author out template>",
                        help    = AUTHOR_OUT_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "author_out_template",
                        action  = "store",
                        default = AUTHOR_OUT_TEMPLATE_DEFAULT)

    group4.add_argument("-b", "--btype",                                # option -b/--btype
                    help    = BTYPE_TEXT + " -- Default: " + \
                              "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan",
                               "@www"],
                    dest    = "btype",
                    action  = "store",
                    default = BTYPE_DEFAULT)

    group4.add_argument("-ko", "--key_out_template",                    # option -ko/--key_out_template
                        metavar = "<key out template>",
                        help    = KEY_OUT_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "key_out_template",
                        action  = "store",
                        default = KEY_OUT_TEMPLATE_DEFAULT)

    group4.add_argument("-Lo", "--license_out_template",                # option -Lo/--license_out_template
                        metavar = "<license out template>",
                        help    = LICENSE_OUT_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "license_out_template",
                        action  = "store",
                        default = LICENSE_OUT_TEMPLATE_DEFAULT)

    group4.add_argument("-m", "--mode",                                 # option -m/--mode
                    help    = MODE_TEXT + " -- Default: " + \
                             "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "ris",
                               "plain", "txt", "BibLaTeX", "biblatex",
                               "bib", "Excel", "excel", "csv", "tsv"],
                    dest    = "mode",
                    action  = "store",
                    default = MODE_DEFAULT)

    group4.add_argument("-mt", "--make_topics",                         # option -mt/--make_topics
                        help    = TOPICS_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "make_topics",
                        action  = "store_true",
                        default = MAKE_TOPICS_DEFAULT)

    group4.add_argument("-nf", "--no_files",                            # option -nf/--no_files
                        help    = NO_FILES_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "no_files",
                        action  = "store_true",
                        default = NO_FILES_DEFAULT)

    group4.add_argument("-s", "--skip",                                 # option -s/--skip
                        metavar = "<skip>",
                        help    = SKIP_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "skip",
                        action  = "store",
                        default = SKIP_DEFAULT)

    group4.add_argument("-sb", "--skip_biblatex",                       # option -sb/--skip_biblatex
                    metavar = "<skip biblatex>",
                    help    = SKIP_BIBLATEX_TEXT + " -- Default: " + \
                             "%(default)s",
                    dest    = "skip_biblatex",
                    action  = "store",
                    default = SKIP_BIBLATEX_DEFAULT)

    group4.add_argument("-to", "--name_out_template",                   # option -to/--template_out
                        metavar = "<name out template>",
                        help    = NAME_OUT_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "name_out_template",
                        action = "store",
                        default = NAME_OUT_TEMPLATE_DEFAULT)

    group4.add_argument("-yo", "--year_out_template",                   # option -yo/--year_out_template
                        metavar = "<year out template>",
                        help    = YEAR_OUT_TEMPLATE_TEXT + \
                                  " -- Default: " + "%(default)s",
                        dest    = "year_out_template",
                        action  = "store",
                        default = YEAR_OUT_TEMPLATE_DEFAULT)

    # ..................................................................
    group5 = parser.add_argument_group("Options for special actions")

    group5.add_argument("-c", "--check_integrity",                      # option -i/--integrity
                        help    = INTEGRITY_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "check_integrity",
                        action  = "store_true",
                        default = INTEGRITY_DEFAULT)

    group5.add_argument("-l", "--lists",                                # option -l/--lists
                        help    = LISTS_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "lists",
                        action  = "store_true",
                        default = LISTS_DEFAULT)

    group5.add_argument("-p", "--pdf_output",                           # option -p/--pdf_output
                        help    = PDF_OUTPUT_TEXT + " -- Default: " + \
                                 "%(default)s",
                        dest    = "pdf_output",
                        action  = "store_true",
                        default = PDF_OUTPUT_DEFAULT)

    group5.add_argument("-r", "--regenerate_pickle_files",              # option -r/--regenerate_pickle_files
                        help    = REGENERATE_TEXT + " -- Default: " + \
                                  "%(default)s",
                        dest    = "regenerate_pickle_files",
                        action  = "store_true",
                        default = REGENERATE_DEFAULT)


    # ------------------------------------------------------------------
    # Getting parsed options

    # 1.50.3 2024.04-23 new section in arparse processing: new options
    #                   -tout and --timeout + corr. assigmnent to
    #                   timeout
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class

    args                  = parser.parse_args()

    dc.author_template       = args.author_template                     # option -A
    dc.author_load_template  = args.author_load_template                # option -Al
    dc.author_out_template   = args.author_out_template                 # option -Ao

    dc.license_template      = args.license_template                    # option -L
    dc.license_load_template = args.license_load_template               # option -Ll
    dc.license_out_template  = args.license_out_template                # option -Lo

    dc.name_template         = args.name_template                       # option -t
    dc.name_load_template    = args.name_load_template                  # option -tl
    dc.name_out_template     = args.name_out_template                   # option -to

    dc.key_template          = args.key_template                        # option -k
    dc.key_out_template      = args.key_out_template                    # option -ko
    dc.key_load_template     = args.key_load_template                   # option -kl

    dc.year_template         = args.year_template                       # option -y
    dc.year_load_template    = args.year_load_template                  # option -yl
    dc.year_out_template     = args.year_out_template                   # option -yo

    dc.btype                 = args.btype                               # option -b
    dc.direc                 = args.direc                               # option -d
    dc.download              = args.download_files                      # option -f

    dc.integrity             = args.check_integrity                     # option -c
    dc.lists                 = args.lists                               # option -l
    dc.make_output           = args.make_output                         # option -mo
    dc.make_topics           = args.make_topics                         # option -mt
    dc.mode                  = args.mode                                # option -m
    dc.number                = int(args.number)                         # option -n
    dc.no_files              = args.no_files                            # option -nf
    dc.output_name           = args.output_name                         # option -o
    dc.pdf_output            = args.pdf_output                          # option -p
    dc.regenerate            = args.regenerate_pickle_files             # option -r
    dc.skip                  = args.skip                                # option -s
    dc.skip_biblatex         = args.skip_biblatex                       # option -sb
    dc.statistics            = args.statistics                          # option -stat

    dc.verbose               = args.verbose                             # option -v
    dc.debugging             = args.debugging                           # option -dbg

    dc.timeout               = int(args.timeout)                        # option -tout

    dc.timeout5              = dc.timeout * 5
    dc.timeout10             = dc.timeout * 10

    # ------------------------------------------------------------------
    # Corrects direc

    dc.direc = dc.direc.strip()                                         # correct/expand OS folder name (-d)
    if dc.direc[len(dc.direc) - 1] != DIREC_SEP:
        dc.direc += DIREC_SEP

    if dc.debugging:
        print("+++ <CTANLoadOut:argparse_process")                      # -dbg


#===================================================================
# check values     --> noch aktualisieren + verschieben

#        load  check output compile
# -a     x     x     x      -

# -A     x     -     x      -
# -Al    x     -     -      -
# -Ao    -     -     x      -

# -b     -     -     x      -
# -c     -     x     -      -
# -d     x     -     x      x
# -dbg   x     x     x      -
# -f     x     x     -      -

# -k     x     -     x      -
# -kl    x     -     -      -
# -ko    -     -     x      -

# -l     -     x     -      -

# -L     x     -     x      -
# -Ll    x     -     -      -
# -Lo    -     -     x      -

# -m     -     -     x      -
# -mo    -     -     x      -
# -mt    -     -     x      -

# -n     x     -     -      -
# -nf    -     -     x      -
# -o     x     x     x      x
# -p     -     -     x      x
# -s     -     -     x      -
# -stat  x     x     x      -

# -t     x     -     x      -
# -to    -     -     x      -
# -tl    x     -     -      -

# -tout  x     x     x      x

# -y     x     -     x      -
# -yo    -     -     x      -
# -yl    x     -     -      -

# -v     x     x     x      -
# -V     x     x     x      -


#===================================================================
# argparse postprocessing

# ------------------------------------------------------------------
def argparse_postprocessing(dc=dc_var):                                 # function argparse_postprocessing
    """
    Postprocesses some parameters for the program CTANLoadOut.

    Standardizes modes. resets modes, options, ... depending on -mt,
    -p, -b, -sb

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Workflow:
    --------
    + standardizes modes
    + resets modes, options, ...

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.btype           option -b
    + dc.call	         list with program arguments
    + dc.make_topics	 variable for -mt (Flag:  topic lists are
                         generated
    + dc.mode	         variable for -m (mode)
    + dc.pdf_output	 option -p     (Flag: PDF out is generated)
    + dc.skip_biblatex	 variable for -sb (specified BibLaTeX fields are
                         skipped)
    + dc.verbose	 option -v     (Flag: output is verbose)

    Message:
    -------
    + CTANLoadOut] Warning: '{0} {1}' changed to '{2}'(due to {3})
    """

    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class
    # 2.7    2026-07-19 new functions (which group specific
    #                   instructions)
    # 2.7.1  2026-07-19 definitions of argparse_process,
    #                   argparse_postprocessing, pre_make_calls,
    #                   make_calls

    if dc.debugging:
        print("+++ >CTANLoadOut:argparse_postprocessing")               # -dbg

    # ------------------------------------------------------------------
    # standardizes modes

    # 1.53   2024-06-11 additional values for -m: tsv, csv

    if dc.mode in ["LaTeX", "latex", "tex"]:                            # LaTeX, latex, tex --> LaTeX
        dc.mode = "LaTeX"
    elif dc.mode in ["BibLaTeX", "biblatex", "bib"]:                    # BibLaTeX, biblatex, bib --> BibLaTeX
        dc.mode = "BibLaTeX"
    elif dc.mode in ["Excel", "excel", "csv", "tsv"]:                   # Excel, excel, tsv --> Excel
        dc.mode = "Excel"
    elif dc.mode in ["RIS", "ris"]:                                     # RIS, ris --> RIS
        dc.mode = "RIS"
    elif dc.mode in ["plain", "txt"]:                                   # plain, txt --> plain
        dc.mode = "plain"
    else:
        pass

    # ------------------------------------------------------------------
    # resets modes, options, ...
    # depending on -mt, -p, -b, -sb

##    if dc.verbose:
##        print("-" * SEPLINE_LENGTH)

    dc.call                  = sys.argv                                 # gets call and its options    --> Platz noch genauer überlegen
    dc.delete_temporary_file = True                                     # flag: in remove_LaTeX_file and remove_other_file

    if (dc.make_topics != MAKE_TOPICS_DEFAULT):                         # resets -m to LaTeX, if -mt is set
        if dc.mode != "LaTeX":
            if dc.verbose:
                print(ERR_MODE.format('-m', dc.mode, '-m LaTeX', '-mt'))
            dc.call.append("-m")
            dc.call.append("LaTeX")
            dc.mode = "LaTeX"
    if (dc.pdf_output != PDF_OUTPUT_DEFAULT):                           # resets -m to LaTeX, if -p is set
        if dc.mode != "LaTeX":
            if dc.verbose:
                print(ERR_MODE.format('-m', dc.mode, '-m LaTeX', '-p'))
                print(ERR_MODE.format('-mt =', dc.make_topics,
                                      True, '-p'))
            dc.call.append("-m")
            dc.call.append("LaTeX")
            dc.call.append("-mt")
            dc.make_topics = True
            dc.mode        = "LaTeX"
    if (dc.btype != BTYPE_DEFAULT):                                     # resets -m to BibLaTeX, if -b is set
        if dc.mode != "BibLaTeX":
            if dc.verbose:
                print(ERR_MODE.format('-m', dc.mode, '-m BibLaTeX',
                                      "'-b'"))
            dc.call.append("-m");
            dc.call.append("BibLaTeX")
            dc.mode = "BibLaTeX"
    if (dc.skip_biblatex != SKIP_BIBLATEX_DEFAULT):                     # resets -m to BibLaTeX, if -sb is set
        if dc.mode != "BibLaTeX":
            if dc.verbose:
                print(ERR_MODE.format('-m', dc.mode, '-m BibLaTeX',
                                      "'-sb'"))
            dc.call.append("-m");
            dc.call.append("BibLaTeX")
            dc.mode = "BibLaTeX"

    if dc.verbose:
        print("-" * SEPLINE_LENGTH)

    if dc.debugging:
        print("+++ <CTANLoadOut:argparse_postprocessing")               # -dbg


#===================================================================
# Sets load, check, compile, regeneration, and output (status flags).
# corrections where arguments have been combined
# inspects simple options -v, -l, -c, , -f, -p, -r
# constructs callx
# sets status flags
# some other resettings (options, callx, ...)
# inspects -l, -mo, -nf

# ------------------------------------------------------------------
def pre_make_calls(dc=dc_var):                                          # function pre_make_calls
    """
    Prepares dc.callx and a few other variables for further processing.

    Sets the boolean variables load, check, compile, regeneration, and output (status flags).
    In addition:
    + Inspects the simple options -v, -l, -c, , -f, -p, -r.
    + Constructs callx (set).
    + Resets some other things (options, callx, ...).
    + Inspects the options -l, -mo, -nf.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Workflow:
    --------
    + sets dc.callx
    + sets the boolean variables dc.load, dc.output, dc.compile,
      dc.check, and dc.regenerationn
    + some other resettings

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.callx	         set with original a/o computed arguments
    + dc.check   	 flag: CTANLOad, check
    + dc.compile	 flag: compilation   
    + dc.download	 option -f     (Flag: PDF download)
    + dc.integrity	 option -c     (Flag: integrity check)
    + dc.lists	         option -n     (Flag: special lists are
                                       generated)
    + dc.load	         flag: CTANLOad, load
    + dc.output	         flag: CTANOut
    + dc.pdf_output	 option -p     (Flag: PDF out is generated)
    + dc.regenerate      option -r     (pickle files are to be
                                       regenerated)
    + dc.regeneration    flag: CTANLOad, regeneration
    + dc.verbose	 option -v     (Flag: output is verbose)
    + dc.callx	         set with original a/o computed arguments
    + dc.check	         flag: CTANLOad, check
    + dc.lists	         option -n     (Flag: special lists are
                                       generated)
    + dc.load	         flag: CTANLOad, load
    + dc.make_output	 option -mo    (Flag: CTANLoad is not started)
    + dc.make_topics	 variable for -mt (Flag:  topic lists are
                                          generated)
    + dc.no_files	 variable for -nf (Flag: files are not generated)
    + dc.pdf_output	 option -p     (Flag: PDF out is generated)
    + dc.verbose	 option -v     (Flag: output is verbose)

    Message:
    -------
    + CTANLoadOut] Warning: '{0} {1}' changed to '{2}'(due to {3})
    """

    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class
    # 2.7    2026-07-19 new functions (which group specific
    #                   instructions)
    # 2.7.1  2026-07-19 definitions of argparse_process,
    #                   argparse_postprocessing, pre_make_calls,
    #                   make_calls

    # ------------------------------------------------------------------
    # inspects simple options -v, -l, -c, , -f, -p, -r
    # constructs callx
    # sets status flags

    # 2.1    2026-04-15 corrections where arguments have been combined

    if dc.debugging:
        print("+++ >CTANLoadOut:pre_make_calls")                        # -dbg

    dc.callx            = set(dc.call[1:])                              # copy (set type)

    if dc.verbose != VERBOSE_DEFAULT:                                   # -v
        dc.callx.add("-v")
    if dc.lists != LISTS_DEFAULT:                                       # -l
        dc.callx.add("-l")
    if dc.integrity != INTEGRITY_DEFAULT:                               # -c
        dc.callx.add("-c")
    if dc.download != DOWNLOAD_DEFAULT:                                 # -f
        dc.callx.add("-f")
    if dc.pdf_output != PDF_OUTPUT_DEFAULT:                             # -p
        dc.callx.add("-p")
    if dc.regenerate != REGENERATE_DEFAULT:                             # -r
        dc.callx.add("-r")

    dc.load             = dc.callx & SET_LOAD         != EMPTY_SET      # there are options given for load
    dc.output           = dc.callx & SET_OUTPUT       != EMPTY_SET      # there are options given for output
    dc.compile          = dc.callx & SET_COMPILE      != EMPTY_SET      # there are options given for compile
    dc.check            = dc.callx & SET_CHECK        != EMPTY_SET      # there are options given for check
    dc.regeneration     = dc.callx & SET_REGENERATION != EMPTY_SET      # there are options given for regeneration

    # ------------------------------------------------------------------
    # some other resettings (options, callx, ...)
    # inspects -l, -mo, -nf

    if dc.load and dc.output and (dc.lists == LISTS_DEFAULT):           # load, output, -l ==> check = True, -l = True
        if dc.verbose:
            print(ERR_MODE.format("check =", dc.check, True,
                                  "load & output"))
            print(ERR_MODE.format("-l =", dc.lists, True,
                                  "load & output"))
        dc.callx.add("-l")
        dc.check = True
        dc.lists = True

    if (dc.make_output != MAKE_OUTPUT_DEFAULT):                         # -mo ==> load = False
        if dc.verbose:
            print(ERR_MODE.format("load =", dc.load, False, "'-mo'"))
        dc.load = False

    if dc.no_files != NO_FILES_DEFAULT:                                 # -nf
        if dc.pdf_output != PDF_OUTPUT_DEFAULT:                         # -p
            if dc.verbose:
                print(ERR_MODE.format("-p =", dc.pdf_output,
                                      PDF_OUTPUT_DEFAULT, "-nf"))
            dc.pdf_output = PDF_OUTPUT_DEFAULT
        if dc.make_topics != MAKE_TOPICS_DEFAULT:                       #   -mt
            if dc.verbose:
                print(ERR_MODE.format("-mt =", dc.make_topics,
                                      MAKE_TOPICS_DEFAULT, "-nf"))
            dc.make_topics = MAKE_TOPICS_DEFAULT

    if dc.debugging:
        print("+++ <CTANLoadOut:pre_make_calls")                        # -dbg


#===================================================================
# make calls: Construct the calls

# 2.13    2026-07-25 Break the function 'make_calls' into some
#                    functions.
# 2.13.1  2026-07-25 Definition of the new functionsn make_call_load(),
#                    make_call_check(), make_call_output(),
#                    make_call_compile(), make_call_regeneration()
# 2.13.5  2026-07-26 Remove the remnants of the 'make_calls' function.
                            
# ------------------------------------------------------------------
# (A) call_load:  constructs the call for loading (call_load)
# (B) call_check: constructs the call for checking (call_check)
# (C) call_output: constructs the call for output generating
#                  (call_output)
# (D) call_regeneration: constructs the call for regeneration
#                        (call_regneration)
# (E, F) call_compile + call_index: constructs the calls for
#                                   compiling and index
#                                   (call_compile, call_index)

# ------------------------------------------------------------------
def make_call_check(dc=dc_var):                                         # function make_call_check
    """
    (B) constructs the call for checking (call_check).

    In particular, dc.call_check is generated.
    The function inspects the options -v, -stat, -c, -l, -d, -o, -dbg.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.call_check              collection with options for check
    + dc.debugging	         option -dbg   (Flag: debugging)
    + dc.direc	                 option -d     (name of the OS directory)
    + dc.integrity	         option -c     (Flag: integrity check)
    + dc.lists	                 option -n     (Flag: special lists are
                                               generated)
    + dc.output_name	         option -o     (generic file name)
    + dc.statistics	         option -stat  (statistics output)

    Messages:
    --------
    There are no specific messages.
    """

    # 2.13    2026-07-25 Break the function 'make_calls' into some
    #                    functions.
    # 2.13.1  2026-07-25 Definition of the new functionsn
    #                    make_call_load(), make_call_check(),
    #                    make_call_output(), make_call_compile(),
    #                    make_call_regeneration()
    # 2.13.3  2026-07-25 Add documentation and comments to functions.

    dc.call_check        = []                                           # (B) initialize call_check

    if dc.debugging:
        print("+++ >CTANLoadOut:call_check")                            # -dbg

    dc.call_check = [sys.executable, "CTANLoad.py"]
    if dc.verbose != VERBOSE_DEFAULT:                                   # -v
        dc.call_check.append("-v")
    if dc.statistics != STATISTICS_DEFAULT:                             # -stat
        dc.call_check.append("-stat")
    if dc.integrity != INTEGRITY_DEFAULT:                               # -c
        dc.call_check.append("-c")
    if dc.lists != LISTS_DEFAULT:                                       # -l
        dc.call_check.append("-l")
    if dc.direc != DIREC_DEFAULT:                                       # -d
        dc.call_check.append("-d")
        dc.call_check.append(dc.direc)
    if dc.output_name != OUTPUT_NAME_DEFAULT:                           # -o
        dc.call_check.append("-o")
        dc.call_check.append(dc.output_name)
    if dc.debugging != DEBUGGING_DEFAULT:                               # -dbg
        dc.call_check.append("-dbg")

    if dc.debugging:
        print("+++ <CTANLoadOut:call_check")                            # -dbg

# ------------------------------------------------------------------
def make_call_compile(dc=dc_var):                                       # function make_call_compile
    """
    (E, F) Constructs the calls for compiling and index.

    In particular, the sequences dc.call_compile and
    dc.call_index are generated.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.call_compile            collection with options for compile
    + dc.call_index	         collection with options for index
    + dc.call_load	         collection with options for load
    + dc.debugging	         option -dbg   (Flag: debugging)
    + dc.direc	                 option -d     (name of the OS directory)
    + dc.output_name	         option -o     (generic file name)

    Messages:
    --------
    There are no specific messages.
    """

    # 2.13    2026-07-25 Break the function 'make_calls' into some
    #                    functions.
    # 2.13.1  2026-07-25 Definition of the new functionsn
    #                    make_call_load(), make_call_check(),
    #                    make_call_output(), make_call_compile(),
    #                    make_call_regeneration()
    # 2.13.3  2026-07-25 Add documentation and comments to functions.

    dc.call_compile      = []                                           # (E) initialize call_compile
    dc.call_index        = []                                           # (F) initialize call_index

    if dc.debugging:
        print("+++ >CTANLoadOut:call_compile")                          # -dbg

    direc_comp      = re.sub(r"\\", "/", dc.direc)
    dc.call_compile = [LATEX_PROCESSOR,
                direc_comp + dc.output_name + ".tex"]
    dc.call_index   = INDEX_PROCESSOR + SPACE + direc_comp + \
                dc.output_name + ".idx" + SPACE + "-o " + SPACE + \
                direc_comp + dc.output_name  + ".ind"

    if dc.debugging:
        print("+++ <CTANLoadOut:call_compile")                          # -dbg
        
# ------------------------------------------------------------------
def make_call_load(dc=dc_var):                                          # function make_call_load
    """
    (A) Constructs the call for loading (call_load).

    In particular, the sequence dc.call_load is generated.
    The function inspects the relevant options -d, -n, -o, -f, -stat,
    -v, -dbg.
    It also inspects -t | -tl | -to, -k | -kl | -ko, -A | -Al | -Ao,
    -L | -Ll | -Lo, -y | -yl | -yo

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Function:
    --------
    There is an inner function named 'inner_load'. She selects the
    appropriate one from the three variations available.
        
    This concerns only the options t | -tl | -to, -k | -kl | -ko,
    -A | -Al | -Ao, -L | -Ll | -Lo, -y | -yl | -yo

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.author_load_template    option -Al    (author template for
                                 load)
    + dc.author_out_template     option -Ao    (author template for
                                 output)
    + dc.author_template         option -A     (general author template)
    + dc.call_load	         collection with options for load
    + dc.download	         option -f     (Flag: PDF download)
    + dc.integrity	         option -c     (Flag: integrity check)
    + dc.key_load_template	 option -kl    (key template) for load
    + dc.key_out_template	 option -ko    (key template for output)
    + dc.key_template	         option -k     (general key template)
    + dc.license_load_template   option -Ll    (license name template
                                               for load)
    + dc.license_out_template	 option -Lo    (license name template for
                                               output)
    + dc.license_template	 option -L     (general license name template)
    + dc.lists	                 option -n     (Flag: special lists are
                                               generated)
    + dc.name_load_template	 option -tl    (name template for output
                                               files for load)
    + dc.name_out_template	 option -to    (name template for ou  tput 
                                               files for output)
    + dc.name_template	         option -t     (general name template for
                                               output files)
    + dc.number	                 option -n     (maximum number of files
                                               for loading)
    + dc.statistics	         option -stat  (statistics output)
    + dc.verbose	         option -v     (Flag: output is verbose)
    + dc.year_load_template	 option -yl    (year template for load)
    + dc.year_load_template	 option -yl    (year template for load)
    + dc.year_template	         option -y     (gheneral year template)

    Messages:
    --------
    There are no specific messages.
    """

    # 2.13    2026-07-25 Break the function 'make_calls' into some
    #                    functions.
    # 2.13.1  2026-07-25 Definition of the new functionsn
    #                    make_call_load(), make_call_check(),
    #                    make_call_output(), make_call_compile(),
    #                    make_call_regeneration()
    # 2.13.3  2026-07-25 Add documentation and comments to functions.
    
    # ..................................................................
    def inner_load(s:str):                                              # inner function inner_load
        """
        auxiliary function: it selects the appropriate one from the
        three variations available.
        
        This concerns only the options t | -tl | -to, -k | -kl | -ko,
        -A | -Al | -Ao, -L | -Ll | -Lo, -y | -yl | -yo
        
        This function is only available within the 'make_calls'
        function.

        Parameter:
        ---------
        s   str
            is a single character that identifies the option in
            question. no default
        """
        
        t = dc.call_load
        t.append(s)
        if a2:
            t.append(w2)
        elif a1:
            t.append(w1)
        elif a3:
            t.append(w1)
        else:
            t.append(w1) 

    # ..................................................................
    dc.call_load = []                                                   # (A) initialize call_load

    if dc.debugging:
        print("+++ >CTANLoadOut:call_load")                             # -dbg

    dc.call_load = [sys.executable, "CTANLoad.py"]
    if dc.direc != DIREC_DEFAULT:                                       # -d
        dc.call_load.append("-d")
        dc.call_load.append(dc.direc)
    if dc.number != NUMBER_DEFAULT:                                     # -n
        dc.call_load.append("-n")
        dc.call_load.append(str(dc.number))
    if dc.output_name != OUTPUT_NAME_DEFAULT:                           # -o
        dc.call_load.append("-o")
        dc.call_load.append(dc.output_name)
    if dc.download != DOWNLOAD_DEFAULT:                                 # -f
        dc.call_load.append("-f")
    if dc.statistics != STATISTICS_DEFAULT:                             # -stat
        dc.call_load.append("-stat")
    if dc.verbose != VERBOSE_DEFAULT:                                   # -v
        dc.call_load.append("-v")
    if dc.debugging != DEBUGGING_DEFAULT:                               # -dbg
        dc.call_load.append("-dbg")

    # inspects -t | -tl | -to
    w1 = dc.name_template
    w2 = dc.name_load_template
    w3 = dc.name_out_template
    a1 = dc.name_template      != NAME_TEMPLATE_DEFAULT                 # -t  is given
    a2 = dc.name_load_template != NAME_LOAD_TEMPLATE_DEFAULT            # -tl  is given
    a3 = dc.name_out_template  != NAME_OUT_TEMPLATE_DEFAULT             # -to  is given

    inner_load("-t")
    
    # inspects -k | -kl | -ko
    w1 = dc.key_template
    w2 = dc.key_load_template
    w3 = dc.key_out_template
    a1 = dc.key_template      != KEY_TEMPLATE_DEFAULT                   # -k  is given
    a2 = dc.key_load_template != KEY_LOAD_TEMPLATE_DEFAULT              # -kl  is given
    a3 = dc.key_out_template  != KEY_OUT_TEMPLATE_DEFAULT               # -ko  is given

    inner_load("-k")

    # inspects -A | -Al | -Ao
    w1 = dc.author_template
    w2 = dc.author_load_template
    w3 = dc.author_out_template
    a1 = dc.author_template      != AUTHOR_TEMPLATE_DEFAULT             # -A  is given
    a2 = dc.author_load_template != AUTHOR_LOAD_TEMPLATE_DEFAULT        # -Al  is given
    a3 = dc.author_out_template  != AUTHOR_OUT_TEMPLATE_DEFAULT         # -Ao  is given
    
    inner_load("-A")

    # inspects -L | -Ll | -Lo
    w1 = dc.license_template
    w2 = dc.license_load_template
    w3 = dc.license_out_template
    a1 = dc.license_template      != LICENSE_TEMPLATE_DEFAULT           # -L  is given
    a2 = dc.license_load_template != LICENSE_LOAD_TEMPLATE_DEFAULT      # -Ll  is given
    a3 = dc.license_out_template  != LICENSE_OUT_TEMPLATE_DEFAULT       # -Lo  is given
    
    inner_load("-L")

    # inspects -y | -yl | -yo
    w1 = dc.year_template
    w2 = dc.year_load_template
    w3 = dc.year_out_template
    a1 = dc.year_template      != YEAR_TEMPLATE_DEFAULT                 # -y  is given
    a2 = dc.year_load_template != YEAR_LOAD_TEMPLATE_DEFAULT            # -yl  is given
    a3 = dc.year_out_template  != YEAR_OUT_TEMPLATE_DEFAULT             # -yo  is given
    
    inner_load("-y")

    if dc.debugging:
        print("+++ <CTANLoadOut:call_load")                             # -dbg

# ------------------------------------------------------------------
def make_call_output(dc=dc_var):                                        # function make_call_output
    """
    (C) Constructs the call for output generating (call_output).

    In particular, the sequence  dc.call_output is generated.
    The function inspects the options -v, -stat, -b, -sb, , -d, -o, -s,
    -mt, -nf.
    Also the options -t | -tl | -to, -k | -kl | -ko, -A | -Al | -Ao,
    -L | -Ll | -Lo, -y | -yl | -yo

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Function:
    --------
    There is an inner function named 'inner_out'. She selects the
    appropriate one from the three variations available.
        
    This concerns only the options t | -tl | -to, -k | -kl | -ko,
    -A | -Al | -Ao, -L | -Ll | -Lo, -y | -yl | -yo

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.author_load_template    option -Al    (author template for
                                 load)
    + dc.author_out_template     option -Ao    (author template for
                                 output)
    + dc.author_template         option -A     (general author template)
    + dc.btype                   option -b
    + dc.call_output	         collection with options for output
    + dc.call_regeneration	 collection with options for regeneration
    + dc.compile	         flag: compilation
    + dc.debugging	         option -dbg   (Flag: debugging)
    + dc.direc	                 option -d     (name of the OS directory)
    + dc.key_load_template	 option -kl    (key template) for load
    + dc.key_out_template	 option -ko    (key template for output)
    + dc.key_template	         option -k     (general key template)
    + dc.license_load_template   option -Ll    (license name template
                                               for load)
    + dc.license_out_template	 option -Lo    (license name template for
                                               output)
    + dc.license_template	 option -L     (general license name template)
    + dc.make_topics	         variable for -mt (Flag:  topic lists are
                                               generated
    + dc.mode	                 variable for -m (mode)
    + dc.name_load_template	 option -tl    (name template for output
                                               files for load)
    + dc.name_out_template	 option -to    (name template for ou  tput
                                               files for output)
    + dc.name_template	         option -t     (general name template for
                                               output files)
    + dc.no_files	         variable for -nf (Flag: files are not
                                               generated)
    + dc.output_name	         option -o     (generic file name)
    + dc.skip	                 variable for -s (specified CTAN fields
                                               are skipped)
    + dc.skip_biblatex	         variable for -sb (specified BibLaTeX
                                               fields are skipped)
    + dc.statistics	         option -stat  (statistics output)
    + dc.verbose	         option -v     (Flag: output is verbose)
    + dc.year_load_template	 option -yl    (year template for load)
    + dc.year_load_template	 option -yl    (year template for load)
    + dc.year_template	         option -y     (gheneral year template)

    Messages:
    --------
    There are no specific messages.
    """

    # 2.13    2026-07-25 Break the function 'make_calls' into some
    #                    functions.
    # 2.13.1  2026-07-25 Definition of the new functionsn
    #                    make_call_load(), make_call_check(),
    #                    make_call_output(), make_call_compile(),
    #                    make_call_regeneration()
    # 2.13.3  2026-07-25 Add documentation and comments to functions.

    # ..................................................................
    def inner_output(s:str):                                            # inner function inner_output
        """
        auxiliary function: It selects the appropriate one from the
        three variations available.
        
        This concerns only the options t | -tl | -to, -k | -kl | -ko,
        -A | -Al | -Ao, -L | -Ll | -Lo, -y | -yl | -yo
        
        This function is only available within the 'make_calls'
        function.

        Parameter:
        ---------
        s   str
            is a single character that identifies the option in
            question.
            no default
        """
        
        t = dc.call_output
        t.append(s)
        if a3:
            t.append(w3)
        elif a1:
            t.append(w1)
        elif a2: 
            t.append(w1)
        else:
            t.append(w1)

    # ..................................................................
    dc.call_output       = []                                           # (C) initialize call_output

    if dc.debugging:
        print("+++ >CTANLoadOut:call_output")                           # -dbg

    dc.call_output = [sys.executable, "CTANOut.py"]
    if dc.verbose != VERBOSE_DEFAULT:                                   # -v
        dc.call_output.append("-v")
    if dc.statistics != STATISTICS_DEFAULT:                             # -stat
        dc.call_output.append("-stat")
    if dc.btype != BTYPE_DEFAULT:                                       # -b
        dc.call_output.append("-b")
        dc.call_output.append(dc.btype)
    if dc.skip_biblatex != SKIP_BIBLATEX_DEFAULT:                       # -sb
        dc.call_output.append("-sb")
        dc.call_output.append(dc.skip_biblatex)
    if dc.direc != DIREC_DEFAULT:                                       # -d
        dc.call_output.append("-d")
        dc.call_output.append(dc.direc)
    if dc.output_name != OUTPUT_NAME_DEFAULT:                           # -o
        dc.call_output.append("-o")
        dc.call_output.append(dc.output_name)
    if dc.mode != MODE_DEFAULT:                                         # -m
        dc.call_output.append("-m")
        dc.call_output.append(dc.mode)
    if dc.skip != SKIP_DEFAULT:                                         # -s
        dc.call_output.append("-s")
        dc.call_output.append(dc.skip)
    if dc.make_topics != MAKE_TOPICS_DEFAULT:                           # -mt
        dc.call_output.append("-mt")
    if dc.debugging != DEBUGGING_DEFAULT:                               # -dbg
        dc.call_output.append("-dbg")
    if dc.no_files != NO_FILES_DEFAULT:                                 # -nf
        dc.call_output.append("-nf")

    # processes -t | -to | -tl
    w1 = dc.name_template
    w2 = dc.name_load_template
    w3 = dc.name_out_template
    a1 = dc.name_template      != NAME_TEMPLATE_DEFAULT                 # -t  is given
    a2 = dc.name_load_template != NAME_LOAD_TEMPLATE_DEFAULT            # -tl  is given
    a3 = dc.name_out_template  != NAME_OUT_TEMPLATE_DEFAULT             # -to  is given

    inner_output("-t")
        
    # processes -k | -ko | -kl
    w1 = dc.key_template
    w2 = dc.key_load_template
    w3 = dc.key_out_template
    a1 = dc.key_template      != KEY_TEMPLATE_DEFAULT                   # -k  is given
    a2 = dc.key_load_template != KEY_LOAD_TEMPLATE_DEFAULT              # -kl  is given
    a3 = dc.key_out_template  != KEY_OUT_TEMPLATE_DEFAULT               # -ko  is given

    inner_output("-k")

    # processes -A a7o -Ao | -Al
    w1 = dc.author_template
    w2 = dc.author_load_template
    w3 = dc.author_out_template
    a1 = dc.author_template      != AUTHOR_TEMPLATE_DEFAULT             # -A  is given
    a2 = dc.author_load_template != AUTHOR_LOAD_TEMPLATE_DEFAULT        # -Al  is given
    a3 = dc.author_out_template  != AUTHOR_OUT_TEMPLATE_DEFAULT         # -Ao  is given

    inner_output("-A")

    # processes -L | -Lo | -Ll
    w1 = dc.license_template
    w2 = dc.license_load_template
    w3 = dc.license_out_template
    a1 = dc.license_template      != LICENSE_TEMPLATE_DEFAULT           # -L  is given
    a2 = dc.license_load_template != LICENSE_LOAD_TEMPLATE_DEFAULT      # -Ll  is given
    a3 = dc.license_out_template  != LICENSE_OUT_TEMPLATE_DEFAULT       # -Lo  is given

    inner_output("-L")

    # processes -y | -yl | -yo
    w1 = dc.year_template
    w2 = dc.year_load_template
    w3 = dc.year_out_template
    a1 = dc.year_template      != YEAR_TEMPLATE_DEFAULT                 # -y  is given
    a2 = dc.year_load_template != YEAR_LOAD_TEMPLATE_DEFAULT            # -yl  is given
    a3 = dc.year_out_template  != YEAR_OUT_TEMPLATE_DEFAULT             # -yo  is given

    inner_output("-y")

    if dc.debugging:
        print("+++ <CTANLoadOut:call_output")                           # -dbg

# ------------------------------------------------------------------
def make_call_regeneration(dc=dc_var):                                  # function make_call_regeneration
    """
    (D) Constructs the call for regeneration (call_regneration).

    In particular, the sequence dc.call_regeneration is generated.
    The function inspects the options -v, -stat, -r, -n, -d, -o, -dbg.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variable in the data class dc:
    ---------------------------------------------------------------
    + dc.call_regeneration	 collection with options for regeneration
    + dc.debugging	         option -dbg   (Flag: debugging)
    + dc.direc	                 option -d     (name of the OS directory)
    + dc.number	                 option -n     (maximum number of files
    + dc.output_name	         option -o     (generic file name)
    + dc.statistics	         option -stat  (statistics output)
    + dc.verbose	         option -v     (Flag: output is verbose)

    Messages:
    --------
    There are no specific messages.
    """

    # 2.13    2026-07-25 Break the function 'make_calls' into some
    #                    functions.
    # 2.13.1  2026-07-25 Definition of the new functionsn
    #                    make_call_load(), make_call_check(),
    #                    make_call_output(), make_call_compile(),
    #                    make_call_regeneration()
    # 2.13.3  2026-07-25 Add documentation and comments to functions.

    dc.call_regeneration = []                                           # (D) initialize call_regeneration

    if dc.debugging:
        print("+++ >CTANLoadOut:call_regeneration")                     # -dbg

    dc.call_regeneration = [sys.executable, "ctanload.py"]
    if dc.verbose != VERBOSE_DEFAULT:                                   # -v
        dc.call_regeneration.append("-v")
    if dc.statistics != STATISTICS_DEFAULT:                             # -stat
        dc.call_regeneration.append("-stat")
    if dc.regenerate != REGENERATE_DEFAULT:                             # -r
        dc.call_regeneration.append("-r")
    if dc.number != NUMBER_DEFAULT:                                     # -n
        dc.call_regeneration.append("-n")
        dc.call_regeneration.append(str(dc.number))
    if dc.direc != DIREC_DEFAULT:                                       # -d
        dc.call_regeneration.append("-d")
        dc.call_regeneration.append(dc.direc)
    if dc.output_name != OUTPUT_NAME_DEFAULT:                           # -o
        dc.call_regeneration.append("-o")
        dc.call_regeneration.append(dc.output_name)
    if dc.debugging != DEBUGGING_DEFAULT:                               # -dbg
        dc.call_regeneration.append("-dbg")

    if dc.debugging:
        print("+++ <CTANLoadOut:call_regeneration")                     # -dbg

        
# ==================================================================
# processes the call sedquences
# + func_call_check(...)
# + func_call_compile(...)
# + func_call_load(...)
# + func_call_output(...)
# + func_call_regeneration(...)

# ------------------------------------------------------------------
def func_call_check(dc=dc_var):                                         # function func_call_check()
    """
    CTANLoad (Check) is processed.

    The function 'func_call_check' starts and controls a subprocess with
    the call sequence 'call_check'.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    + dc.call_check      collection with options for check
    + dc.debugging	 option -dbg   (Flag: debugging)
    + dc.timeout10	 timeout *10
    + dc.timeout5	 timeout *5
    + dc.verbose	 option -v     (Flag: output is verbose)

    Possible messages:
    -----------------
    + Error: called process '{call_load[1]}' not found
    + Error: program terminated
    + Error: file '{call_load[0]}' not found
    + Error: timeout error
    + Error: keyboard interrupt
    + Error: unicode decode error
    + Error: any unspecified error
    + Info: CTANLoad (Check) completed
    """

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check],
    #                   [..., compilation],  [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of
    #                   subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True,
    #                   timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut,
    #                   check], [..., compilation], [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [...,
    #                   regeneration]: stdout is linked to a temporary
    #                   auxiliary file that is processed line by line
    # 1.47   2024-04-17 addition: [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]:
    #                   except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault -->
    #                   timeout etc
    # 1.51   2024-05-94 new section in exception handling:
    #                   UnicodeDecodeError
    # 2.5    2026-07-17 backtracing
    # 2.5.2  2026-07-17 call traceback.print_exc()
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class

    if dc.debugging:
        print("+++ >CTANLoadOut:func_call_check")                       # -dbg

    print("-" * SEPLINE_LENGTH)

    print("[CTANLoadOut, check] Info: CTANLoad (Check)")

    try:
        with TemporaryFile("r+", encoding=ENC) as f:                    # temporary file
            process_check  = subprocess.run(dc.call_check, check=True,
                                encoding=ENC, stderr=subprocess.PIPE,
                                stdout=f, text=True,timeout=dc.timeout10,
                                universal_newlines=True)                # processes call_check in a subprocess
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
            check_errormessage = process_check.stderr                   # possible error message
            if len(check_errormessage) > 0:
                print(check_errormessage)
    except subprocess.CalledProcessError as exc:                        # process error
        if dc.verbose:
            print("[CTANLoadOut, check] Error: called process",
                  f" '{dc.call_check[1]}' not found,", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if dc.verbose:
            print("[CTANLoadOut, check] Error:",
                  f" file '{dc.call_check[0]}' not found", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeoutInfo: CTANLoad (Check) completed
        if dc.verbose:
            print("[CTANLoadOut, check] Error: timeout error",
                  dc.timeout5, exc)
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if dc.verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if dc.verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc, traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except Exception as exc:                                            # any unspecified error
        if dc.verbose:
            print("[CTANLoadOut, check] Error: any unspecified error",
                  exc, traceback.print_exc())
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated

    if dc.verbose:
        print("\n" + "[CTANLoadOut, check] ",
              "Info: CTANLoad (Check) completed")

    if dc.debugging:
        print("+++ <CTANLoadOut:func_call_check")                       # -dbg

# ------------------------------------------------------------------
def func_call_compile(dc=dc_var):                                       # function func_call_compile
    """
    Compiles the generated LaTeX source file with LuaLaTeX.

    The function 'func_call_compile' starts and controls a subprocess
    with the call sequences 'call_compile' and 'call_index'.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Calls:
    -----
    + remove_LaTeX_file(...)

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    + dc.call_compile    collection with options for compile
    + dc.call_index	 collection with options for index
    + dc.debugging	 option -dbg   (Flag: debugging)
    + dc.direc	         option -d     (name of the OS directory)
    + dc.output_name	 option -o     (generic file name)
    + dc.statistics	 option -stat  (statistics output)
    + dc.timeout	 option -tout (timeout)
    + dc.timeout10	 timeout *10
    + dc.verbose	 option -v     (Flag: output is verbose)

    Possible messages:
    -----------------
    + Error: called process '{call_load[1]}' not found
    + Error: program terminated
    + Error: file '{call_load[0]}' not found
    + Error: timeout error
    + Error: keyboard interrupt
    + Error: unicode decode error
    + Error: any unspecified error
    + Warning: LaTeX file '{file_name}' without content, no compilation
    + Warning: LaTeX file '{file_name}' does not exist, no compilation
    """

    # 1.44 2024-04-10 Time measurement for compilations; corresponding
    #                 statistical output in each case
    # 1.45   2024-04-13 new concept for [CTANLoadOut, check],
    #                   [..., compilation],  [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of
    #                   subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True,
    #                   timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut,
    #                   check], [..., compilation], [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.47   2024-04-17 addition: [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]:
    #                   except KeyboardInterrupt
    # 1.48   2024-04-22 compiles related subprocesses revised: now
    #                   more against coding errors
    # 1.49   2024-04-22 .pdf and .log files removed before step2 and
    #                   step3 in compilation subprocess
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault -->
    #                   timeout etc
    # 1.51   2024-05-94 new section in exception handling:
    #                   UnicodeDecodeError
    # 1.58   2025-10-05 time specification with unit
    # 2.5    2026-07-17 backtracing
    # 2.5.2  2026-07-17 call traceback.print_exc()
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class
    # 2.17    2026-08-22 name and size of the resulting PDF file

    if dc.debugging:
        print("+++ >CTANLoadOut:func_call_compile")                     # -dbg

    print("-" * SEPLINE_LENGTH)

    print("[CTANLoadOut, compilation] Info: Compilation")

    file_name:str       = dc.direc + dc.output_name + ".tex"
    file_name_log:str   = dc.direc + dc.output_name + ".log"
    file_name_ilg:str   = dc.direc + dc.output_name + ".ilg"

    if path.exists(file_name):
        if path.getsize(file_name) > MIN_TEX_SIZE:

            # step 1
            for e in [".aux", ".idx", ".ind", ".log", ".ilg", ".pdf",
                      ".out", ".bbl", ".indlualatex"]:
                remove_LaTeX_file(e)

            if dc.verbose:
                print("." * SEPLINE_LENGTH)

            print(EMPTY)
            print("[CTANLoadOut, compilation] Info:", LATEX_PROCESSOR)
            if dc.verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      dc.call_compile)

            startcompiletotal   = time.time()                           # sets begin of total time
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_compile1 = subprocess.run(dc.call_compile,
                            timeout=dc.timeout10, check=True,
                            capture_output=True)                        # processes call_compile in a subprocess
                compile1_errormessage = \
                                process_compile1.stderr.decode(ENC)
                compile1_message      = \
                                process_compile1.stdout.decode(ENC)     # possible error message
                if len(compile1_errormessage) > 0:
                    if dc.verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              " error in compilation")
                    sys.exit()
                else:
                    if dc.verbose:
                        print("[CTANLoadOut, compilation] Info: more" +\
                              f" information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation]",
                              "Info: Compilation OK")
            except subprocess.CalledProcessError as exc:                # process error
                if dc.verbose:
                    print("[CTANLoadOut, compilation] ",
                          "Error: called process",
                          f" '{dc.call_compile[1]}' not found,", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if dc.verbose:
                    print("[CTANLoadOut, compilation] Error: file" +\
                          f" '{dc.call_compile[0]}' not found", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except subprocess.TimeoutExpired as exc:                    # timeout
                if dc.verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: timeout error", dc.timeout10, exc)
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated\
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except Exception as exc:                                    # any unspecified error
                if dc.verbose:
                    print("[CTANLoadOut, compilation] Error: any",
                          "unspecified error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated

            if dc.statistics:                                           # outputs the compilation statistics
                PP         = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()

                print("\nStatistics (compilation):")
                tmp_ct = endcompiletotal-startcompiletotal
                tmp_pt = endcompileprocess-startcompileprocess
                print("total time (compilation): ".ljust(LEFT + 3),
                      str(round(tmp_ct, 2)).rjust(PP), "s")
                print("process time (compilation): ".ljust(LEFT + 3),
                      str(round(tmp_pt, 2)).rjust(PP), "s")

# ...................................................................
            # step 2
            if dc.verbose:
                print("." * SEPLINE_LENGTH)
            for e in [".log", ".pdf"]:
                remove_LaTeX_file(e)

            if dc.verbose:
                print("." * SEPLINE_LENGTH)

            print("[CTANLoadOut, compilation] Info:", LATEX_PROCESSOR)
            if dc.verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      dc.call_compile)

            startcompiletotal   = time.time()                           # sets begin of total time
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_compile2 = subprocess.run(dc.call_compile,
                                timeout=dc.timeout10, check=True,
                                capture_output=True)                    # processes call_compile in a subprocess
                compile2_errormessage = \
                                process_compile2.stderr.decode(ENC)
                compile2_message      = \
                                process_compile2.stdout.decode(ENC)
                                                                        # possible error message
                if len(compile2_errormessage) > 0:
                    if dc.verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              "error in compilation")
                    sys.exit()
                else:
                    if dc.verbose:
                        print("[CTANLoadOut, compilation] Info: more",
                              f"information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation]",
                              "Info: Compilation OK")
            except subprocess.CalledProcessError as exc:                # process error
                if dc.verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: called process",
                          f"'{dc.call_compile[1]}' not found,", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if dc.verbose:
                    print("[CTANLoadOut, compilation] Error: file",
                          f"'{dc.call_compile[0]}' not found", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except subprocess.TimeoutExpired as exc:                    # timeout
                if dc.verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: timeout error", dc.timeout10, exc)
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except Exception as exc:                                    # any unspecified error
                if dc.verbose:
                    print("[CTANLoadOut, compilation] Error:",
                          "any unspecified error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated

            if dc.statistics:                                           # outputs the compilation statistics
                PP  = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()

                print("\nStatistics (compilation):")
                tmp_ct = endcompiletotal-startcompiletotal
                tmp_pt = endcompileprocess-startcompileprocess

                print("total time (compilation): ".ljust(LEFT + 3),
                      str(round(tmp_ct, 2)).rjust(PP), "s")
                print("process time (compilation): ".ljust(LEFT + 3),
                      str(round(tmp_pt, 2)).rjust(PP), "s")

# ...................................................................
            # step 3
            if dc.verbose:
                print("." * SEPLINE_LENGTH)
            print("[CTANLoadOut, index] Info:", INDEX_PROCESSOR)
            if dc.verbose:
                print("[CTANLoadOut, index] Info: Program call:",
                      dc.call_index)

            startcompiletotal   = time.time()                           # sets begin of total time
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_index      = subprocess.run(dc.call_index,
                                     timeout=dc.timeout, check=True,
                                     capture_output=True,
                                     universal_newlines=True)           # processes call_index in a subprocess
                index_errormessage = process_index.stderr               # possible error message
                index_message      = process_index.stdout
            except subprocess.CalledProcessError as exc:                # process error
                if dc.verbose:
                    print("[CTANLoadOut, index] Error: called process",
                          f"'{dc.call_index[1]}' not found,", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if dc.verbose:
                    print("[CTANLoadOut, index] Error: file",
                          f"'{dc.call_index[0]}' not found", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated
            except subprocess.TimeoutExpired as exc:                    # timeout
                if dc.verbose:
                    print("[CTANLoadOut, index] Error: timeout error",
                          dc.timeout, exc)
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except Exception as exc:                                    # any unspecified error
                if dc.verbose:
                    print("[CTANLoadOut, index]",
                          "Error: any unspecified error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated

            if dc.verbose:
                print("[CTANLoadOut, index] Info: more information",
                      f"in '{file_name_ilg}'")
                print("[CTANLoadOut, index] Info: Makeindex OK")

            if dc.statistics:                                           # outputs the compilation statistics
                PP = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()

                print("\nStatistics (index generation):")
                tmp_ct = endcompiletotal-startcompiletotal
                tmp_pt = endcompileprocess-startcompileprocess

                print("total time (index generation): ".ljust(LEFT + 3),
                      str(round(tmp_ct, 2)).rjust(PP), "s")
                print("process time (index generation): ".\
                      ljust(LEFT + 3),
                      str(round(tmp_pt, 2)).rjust(PP), "s")

# ...................................................................
            # step 4
            if dc.verbose:
                print("." * SEPLINE_LENGTH)

            for e in [".log", ".pdf"]:
                remove_LaTeX_file(e)

            if dc.verbose:
                print("." * SEPLINE_LENGTH)
            print("[CTANLoadOut, compilation] Info:", LATEX_PROCESSOR)
            if dc.verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      dc.call_compile)

            startcompiletotal   = time.time()                           # sets begin of total time\
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_compile3 = subprocess.run(dc.call_compile,
                                timeout=dc.timeout10, check=True,
                                capture_output=True)                    # processes call_compile in a subprocess
                compile3_errormessage = \
                                process_compile3.stderr.decode(ENC)
                compile3_message      = \
                                process_compile3.stdout.decode(ENC)     # possible error message
                if len(compile3_errormessage) > 0:
                    if dc.verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              "error in compilation")
                    sys.exit()
                else:
                    if dc.verbose:
                        print("[CTANLoadOut, compilation] Info: more",
                              f"information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation]",
                              "Info: result in '" +\
                              dc.direc + dc.output_name + ".pdf'")
                        print("[CTANLoadOut, compilation]",
                              "Info: Compilation OK")
            except subprocess.CalledProcessError as exc:                # process error
                if dc.verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: called process",
                          f"'{dc.call_compile[1]}' not found,", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if dc.verbose:
                    print("[CTANLoadOut, compilation] Error: file"
                          f"'{dc.call_compile[0]}' not found", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated\
            except subprocess.TimeoutExpired as exc:                    # timeout
                if dc.verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: timeout error", dc.timeout10, exc)
                sys.exit("[CTANLoadOut, compilation] " +
                         "Error: program terminated")                   # program terminated
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if dc.verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except Exception as exc:                                    # any unspecified error
                if dc.verbose:
                    print("[CTANLoadOut, compilation] Error:",
                          "any unspecified error", exc,
                          traceback.print_exc())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated

            if dc.statistics:                                           # outputs the compilation statistics
                PP         = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()

                print("\nStatistics (compilation):")
                tmp_ct = endcompiletotal-startcompiletotal
                tmp_pt = endcompileprocess-startcompileprocess

                print("total time (compilation): ".ljust(LEFT + 3),
                      str(round(tmp_ct, 2)).rjust(PP), "s")
                print("process time (compilation): ".ljust(LEFT + 3),
                      str(round(tmp_pt, 2)).rjust(PP), "s")
                tmp = path.getsize(dc.direc + dc.output_name + ".pdf")
                print("name of the PDF file:".ljust(LEFT + 4),
                      dc.direc + dc.output_name + ".pdf")
                print("size of PDF file (in bytes):".ljust(LEFT + 4),
                      tmp)
        else:
            if dc.verbose: print("[CTANLoadOut, compilation]",
                              "Warning: LaTeX file",
                              f"'{file_name}' without content,",
                              "no compilation")
    else:
        if dc.verbose: print("[CTANLoadOut, compilation]",
                          "Warning: LaTeX file",
                          f"'{file_name}' does not exist, ",
                          "no compilation")

# ...................................................................
    if dc.verbose:
        print("." * SEPLINE_LENGTH)


    for e in [".aux", ".idx", ".ind", ".out", ".bbl", ".indlualatex"]:  # remove some LaTeX files
        remove_LaTeX_file(e)

    if dc.debugging:
        print("+++ <CTANLoadOut:func_call_compile")                     # -dbg

# ------------------------------------------------------------------
def func_call_load(dc=dc_var):                                          # function func_call_load()
    """
    CTANLoad (for loading) is processed.

    The function 'func_call_load' starts and controls a subprocess with
    the call sequence 'call_load'.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    + dc.call_load	 collection with options for load
    + dc.debugging	 option -dbg   (Flag: debugging)
    + dc.timeout10	 timeout *10
    + dc.verbose	 option -v     (Flag: output is verbose)

    Possible messages:
    -----------------
    + Error: called process '{call_load[1]}' not found
    + Error: program terminated
    + Error: file '{call_load[0]}' not found
    + Error: timeout error
    + Error: keyboard interrupt
    + Error: unicode decode error
    + Error: any unspecified error
    + Info: CTANLoad (Load) completed
    """

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check],
    #                   [..., compilation],  [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of
    #                   subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True,
    #                   timeout=<number>traceback.print_exc()
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut,
    #                   check], [..., compilation], [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [...,
    #                   regeneration]: stdout is linked to a temporary
    #                   auxiliary file that is processed line by line
    # 1.46   2024-04-16 additional parameter errors="ignore" for
    #                   'with TemporaryFile' in func_call_load,
    #                   func_call_output
    # 1.47   2024-04-17 addition: [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]:
    #                   except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault -->
    #                   timeout etc
    # 1.51   2024-05-94 new section in exception handling:
    #                   UnicodeDecodeError
    # 2.5    2026-07-17 backtracing
    # 2.5.2  2026-07-17 call traceback.print_exc()
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class

    if dc.debugging:
        print("+++ >CTANLoadOut:func_call_load")                        # -dbg

    print("-" * SEPLINE_LENGTH)

    print("[CTANLoadOut, load] Info: CTANLoad (Load)")

    try:
        with TemporaryFile("r+", encoding=ENC, errors="ignore") as f:   # temporary file
            process_load = subprocess.run(dc.call_load, check=True,
                            encoding=ENC, stderr=subprocess.PIPE,
                            stdout=f, text=True, timeout=dc.timeout10, 
                            universal_newlines=True)                    # processes call_load in a subprocess
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
            load_errormessage = process_load.stderr                     # possible error messageError: unicode decode error
            if len(load_errormessage) > 0:
                print(load_errormessage)
    except subprocess.CalledProcessError as exc:                        # process error
        if dc.verbose:
            print("[CTANLoadOut, load] Error: called process",
                  f" '{dc.call_load[1]}' not found,", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if dc.verbose:
            print("[CTANLoadOut, load] Error:"
                  f" file '{dc.call_load[0]}' not found", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if dc.verbose:
            print("[CTANLoadOut, load] Error: timeout error",
                  dc.timeout10, exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if dc.verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if dc.verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc, traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except Exception as exc:                                            # any unspecified error
        if dc.verbose:
            print("[CTANLoadOut, load] Error: any unspecified error",
                  exc, traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated

    if dc.verbose:
        print("\n" + "[CTANLoadOut,",
              "load] Info: CTANLoad (Load) completed")

    if dc.debugging:
        print("+++ <CTANLoadOut:func_call_load")                        # -dbg

# ------------------------------------------------------------------
def func_call_output(dc=dc_var):                                        # function func_call_output
    """
    CTANOut is processed.

    The function 'func_call_output' starts and controls a subprocess
    with the call sequence 'call_output'.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Calls:
    -----
    + remove_other_file(...)
    + remove_LaTeX_file(...)

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    + dc.call_output	 collection with options for output
    + dc.debugging	 option -dbg   (Flag: debugging)
    + dc.mode	         variable for -m (mode)
    + dc.timeout	 option -tout (timeout)
    + dc.timeout10	 timeout *10
    + dc.verbose	 option -v     (Flag: output is verbose)

    Possible messages:
    -----------------
    + Error: called process '{call_load[1]}' not found
    + Error: program terminated
    + Error: file '{call_load[0]}' not found
    + Error: timeout error
    + Error: keyboard interrupt
    + Error: unicode decode error
    + Error: any unspecified error
    + Info: CTANOut completed
    """

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check],
    #                   [..., compilation],  [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of
    #                   subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True,
    #                   timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut,
    #                   check], [..., compilation], [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [...,
    #                   regeneration]: stdout is linked to a temporary
    #                   auxiliary file that is processed line by line
    # 1.46   2024-04-16 additional parameter errors="ignore" for
    #                   'with TemporaryFile' in func_call_load,
    #                   func_call_output
    # 1.47   2024-04-17 addition: [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]:
    #                   except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault -->
    #                   timeout etc
    # 1.51   2024-05-94 new section in exception handling:
    #                   UnicodeDecodeError
    # 2.5    2026-07-17 backtracing
    # 2.5.2  2026-07-17 call traceback.print_exc()
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class

    if dc.debugging:
        print("+++ >CTANLoadOut:func_call_output")                      # -dbg

    print("-" * SEPLINE_LENGTH)

    print("[CTANLoadOut, output] Info: CTANOut")

    # removes some relevant files
    if dc.mode == "BibLaTeX":
        remove_other_file(".bib")
    elif dc.mode == "LaTeX":
        for e in [".tex", ".tap", ".top", ".xref", ".stat", ".tlp",
                  ".lic"]:
            remove_LaTeX_file(e)
    elif dc.mode == "RIS":
        remove_other_file(".ris")
    elif dc.mode == "plain":
        remove_other_file(".txt")
    elif dc.mode == "Excel":
        remove_other_file(".tsv")
    else:
        pass

    try:
        with TemporaryFile("r+", encoding=ENC,
                           errors="ignore") as f:                       # temporary file
            process_out = subprocess.run(dc.call_output, check=True,
                            encoding=ENC, stderr=subprocess.PIPE,
                            stdout=f, text=True,timeout=dc.timeout10, 
                            universal_newlines=True)                    # processes call_output in a subprocess
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
    except subprocess.CalledProcessError as exc:                        # process error
        if dc.verbose:
            print("[CTANLoadOut, output] Error: called process" +\
                  f" '{dc.call_output[1]}' not found,", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if dc.verbose:
            print("[CTANLoadOut, output] Error:",
                  f" file '{dc.call_output[0]}' not found", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if dc.verbose:
            print("[CTANLoadOut, output] Error: timeout error",
                  dc.timeout, exc)
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if dc.verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if dc.verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc, traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except Exception as exc:                                            # any unspecified error
        if dc.verbose:
            print("[CTANLoadOut, output] Error: any unspecified error",
                  exc, traceback.print_exc())
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated

    if dc.verbose:
        print("\n" + "[CTANLoadOut, output] Info: CTANOut completed")

    if dc.debugging:
        print("+++ <CTANLoadOut:func_call_output")                      # -dbg

# ------------------------------------------------------------------
def func_call_regeneration(dc=dc_var):                                  # function func_call_regeneration
    """
    CTANLoad (Regeneration) is processed.

    The function 'func_call_regeneration' starts and controls a
    subprocess with the call sequence 'call_regeneration'.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    + dc.call_regeneration collection with options for regeneration
    + dc.debugging	   option -dbg   (Flag: debugging)
    + dc.regeneration	   flag: CTANLOad, regeneration
    + dc.timeout10	   timeout *10
    + dc.verbose	   option -v     (Flag: output is verbose)

    Possible messages:
    -----------------
    + Error: called process '{call_load[1]}' not found
    + Error: program terminated
    + Error: file '{call_load[0]}' not found
    + Error: timeout error
    + Error: keyboard interrupt
    + Error: unicode decode error
    + Error: any unspecified error
    + Info: CTANLoad (Regeneration) completed
    """

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check],
    #                   [..., compilation],  [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of
    #                   subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True,
    #                   timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut,
    #                   check], [..., compilation], [..., index],
    #                   [..., load], [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [...,
    #                   regeneration]: stdout is linked to a temporary
    #                   auxiliary file that is processed line by line
    # 1.47   2024-04-17 addition: [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]:
    #                   except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault -->
    #                   timeout etc
    # 1.51   2024-05-94 new section in exception handling:
    #                   UnicodeDecodeError
    # 2.5    2026-07-17 backtracing
    # 2.5.2  2026-07-17 call traceback.print_exc()
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class

    if dc.debugging:
        print("+++ >CTANLoadOut:func_call_regneration")                 # -dbg

    print("-" * SEPLINE_LENGTH)

    print("[CTANLoadOut, regeneration] Info: CTANLoad (Regeneration)")

    try:
        with TemporaryFile("r+", encoding=ENC) as f:                    # temporary file
            process_regeneration = subprocess.run(dc.call_regeneration,
                                    check=True, encoding=ENC,
                                    stderr=subprocess.PIPE, stdout=f,
                                    text=True,timeout=dc.timeout10,
                                    universal_newlines=True)            # processes call_regeneration in a subprocess
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
            regeneration_errormessage = process_regeneration.stderr     # possible error message
            if len(regeneration_errormessage) > 0:
                print(regeneration_errormessage)
    except subprocess.CalledProcessError as exc:                        # process error
        if dc.verbose:
            print("[CTANLoadOut, regeneration] Error: called process",
                  f" '{dc.call_regeneration[1]}' not found,", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, dc.regeneration] " +\
                 "Error: program terminated")                           # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if dc.verbose:
            print("[CTANLoadOut, regeneration] Error:",
                  f" file '{dc.call_regeneration[0]}' not found", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, regeneration] " +\
                 "Error: program terminated")                           # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if dc.verbose:
            print("[CTANLoadOut, regeneration] Error: timeout error",
                  dc.timeout10, exc)
        sys.exit("[CTANLoadOut, regeneration] " +\
                 "Error: program terminated")                           # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if dc.verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if dc.verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc, traceback.print_exc())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except Exception as exc:                                            # any unspecified error
        if dc.verbose:
            print("[CTANLoadOut, regeneration] " +\
                  "Error: any unspecified error", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoadOut, regeneration] " +\
                 "Error: program terminated")                           # program terminated

    if dc.verbose:
        print("\n" + "[CTANLoadOut, regeneration] Info:" +\
              " CTANLoad (Regeneration) completed")

    if dc.debugging:
        print("+++ <CTANLoadOut:func_call_regneration")                 # -dbg


# =================================================================
# main functions
# + head(...
# + main(...)

# ------------------------------------------------------------------
def head(dc=dc_var):                                                    # function head
    """
    Shows the given options.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Calls:
    -----
    + fold(...)


    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    + dc.author_load_template   option -Al    (author template for load)
    + dc.author_out_template    option -Ao    (author template for
                                              output)
    + dc.author_template        option -A     (general author template)
    + dc.btype                  option -b
    + dc.call	                list with program arguments
    + dc.check	                flag: CTANLOad, check
    + dc.compile	        flag: compilation
    + dc.debugging	        option -dbg   (Flag: debugging)
    + dc.direc	 option -d      (name of the OS directory)
    + dc.key_load_template      option -kl    (key template) for load
    + dc.key_out_template	option -ko    (key template for output)
    + dc.key_template	        option -k     (general key template)
    + dc.license_load_template	option -Ll    (license name template for
                                              load)
    + dc.license_out_template	option -Lo    (license name template for
                                              output)
    + dc.license_template	option -L     (general license name template)
    + dc.load	                flag: CTANLOad, load
    + dc.mode	                variable for -m (mode)
    + dc.name_load_template	option -tl    (name template for output
                                              files for load)
    + dc.name_out_template	option -to    (name template for output files
                                              for output)
    + dc.name_template	        option -t     (general name template for
                                              output files)
    + dc.number	                option -n     (maximum number of files
                                              for loading)
    + dc.output	                flag: CTANOut
    + dc.output_name	        option -o     (generic file name)
    + dc.regeneration	        flag: CTANLOad, regeneration
    + dc.skip	                variable for -s (specified CTAN fields are
                                              skipped)
    + dc.skip_biblatex	        variable for -sb (specified BibLaTeX
                                              fields are skipped)
    + dc.timeout	        option -tout (timeout)
    + dc.verbose	        option -v     (Flag: output is verbose)
    + dc.year_load_template	option -yl    (year template for load)
    + dc.year_load_template	option -yl    (year template for load)
    + dc.year_template	        option -y     (gheneral year template)

    Messages:
    --------
    There are no specific messages.
    """

    # 2.2    2026-07-16 more f-strings
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class
    # 2.15   2026-08-20 Revise the options log 

    if dc.debugging:
        print("+++ >CTANLoadOut:head")                                  # -dbg

    dc.call[0] = "CTANLoadOut.py"

    if dc.verbose:
        print(EMPTY)
##        print("[CTANLoadOut] Info: Program call:", dc.call)
        if dc.btype != BTYPE_DEFAULT:                 # -b
            tmp_b = f"({BTYPE_TEXT})"
            print(f'  {"-b":5} {tmp_b:70} {dc.btype}')

        if dc.integrity != INTEGRITY_DEFAULT:       # -c (Flag)
            tmp_c = f"({INTEGRITY_TEXT})"
            print(f'  {"-c":5} {tmp_c:70}')

        if dc.direc != DIREC_DEFAULT:             # -d
            tmp_d = f"({DIREC_TEXT})"
            print(f'  {"-d":5} {tmp_d:70} {dc.direc}')

        if dc.download != DOWNLOAD_DEFAULT:        # -f (Flag)
            tmp_f = f"({DOWNLOAD_TEXT})"
            print(f'  {"-f":5} {tmp_f:70}')

        if dc.lists != LISTS_DEFAULT:                 # -l (Flag)
            tmp_l = "(" + (LISTS_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-l":5} {tmp_l:70}')

        if dc.mode != MODE_DEFAULT:                  # -m
            tmp_m = f"({MODE_TEXT})"
            print(f'  {"-m":5} {tmp_m:70} {dc.mode}')

        if dc.make_output != MAKE_OUTPUT_DEFAULT:          # -mo (Flag)
            tmp_mo = "(" + (MAKE_OUTPUT_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-mo":5} {tmp_mo:70}')

        if dc.make_topics != MAKE_TOPICS_DEFAULT:          # -mt (Flag)
            tmp_mt = "(" + (TOPICS_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-mt":5} {tmp_mt:70}')

        if dc.number != NUMBER_DEFAULT:                # -n
            tmp_n = f"({NUMBER_TEXT})"
            print(f'  {"-n":5} {tmp_n:70} {dc.number}')

        if dc.no_files != NO_FILES_DEFAULT:             # -nf (Flag)
            tmp_nf = "(" + (NO_FILES_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-nf":5} {tmp_nf:70}')

        if dc.output_name != OUTPUT_NAME_DEFAULT:                # -o
            tmp_o = "(" + (OUTPUT_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-o":5} {tmp_o:70} {dc.output_name}')

        if dc.pdf_output != PDF_OUTPUT_DEFAULT:            # -p (Flag)
            tmp_p = f"({PDF_OUTPUT_TEXT})"
            print(f'  {"-p":5} {tmp_p:70}')

        if dc.regenerate != REGENERATE_DEFAULT:     # -r (Flag)
            tmp_r = f"({REGENERATE_TEXT})"
            print(f'  {"-r":5} {tmp_r:70}')

        if dc.skip != SKIP_DEFAULT:                  # -s
            tmp_s = f"({SKIP_TEXT})"
            print(f'  {"-s":5} {tmp_s:70} {dc.skip}')

        if dc.skip_biblatex != SKIP_BIBLATEX_DEFAULT:        # -sb
            tmp_sb = f"({SKIP_BIBLATEX_TEXT})"
            print(f'  {"-sb":5} {tmp_sb:70} {dc.skip_biblatex}')

        if dc.statistics != STATISTICS_DEFAULT:         # -stat (Flag)
            tmp_stat = f"({STATISTICS_TEXT})"
            print(f'  {"-stat":5} {tmp_stat:70}')


        if dc.timeout != TIMEOUT_DEFAULT:            # -tout
            tmp_tout = f"({TIMEOUT_TEXT})"
            print(f'  {"-tout":5} {tmp_tout:70} {dc.timeout}')

        if dc.verbose != VERBOSE_DEFAULT:               # -v (Flag)
            tmp_v = f"({VERBOSE_TEXT})"
            print(f'  {"-v":5} {tmp_v:70}')


        if dc.author_template != AUTHOR_TEMPLATE_DEFAULT:       # -A (authors)
            tmp_A = f"({AUTHOR_TEMPLATE_TEXT})"
            print(f'  {"-A":5} {tmp_A:70} {fold(dc.author_template)}')

        if dc.author_load_template != AUTHOR_LOAD_TEMPLATE_DEFAULT: # -Al (authors)
            tmp_Al = f"({AUTHOR_LOAD_TEMPLATE_TEXT})"
            print(f'  {"-Al":5} {tmp_Al:69} ',
                  f'{fold(dc.author_load_template)}')

        if dc.author_out_template != AUTHOR_OUT_TEMPLATE_DEFAULT:  # -Ao (authors)
            tmp_Ao = f"({AUTHOR_OUT_TEMPLATE_TEXT})"
            print(f'  {"-Ao":5} {tmp_Ao:69} ',
                  f'{fold(dc.author_out_template)}')


        if dc.key_template != KEY_TEMPLATE_DEFAULT:          # -k (keys)
            tmp_k = "(" + (KEY_TEMPLATE_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-k":5} {tmp_k:70} {fold(dc.key_template)}')

        if dc.key_load_template != KEY_LOAD_TEMPLATE_DEFAULT:    # -kl (keys)
            tmp_kl  = "(" + (KEY_LOAD_TEMPLATE_TEXT + ")")[0:65]+ELLIPSIS
            tmp_kl2 = fold(dc.key_load_template)
            print(f'  {"-kl":5} {tmp_kl:70} {tmp_kl2}')

        if dc.key_out_template != KEY_OUT_TEMPLATE_DEFAULT:     # -ko (keys)
            tmp_ko = "(" + (KEY_OUT_TEMPLATE_TEXT + ")")[0:65]+ ELLIPSIS
            tmp_ko2 = fold(dc.key_out_template)
            print(f'  {"-ko":5} {tmp_ko:70} {tmp_ko2}')


        if dc.license_template != LICENSE_TEMPLATE_DEFAULT:      # -L (licenses)
            tmp_L = f"({LICENSE_TEMPLATE_TEXT})"
            print(f'  {"-L":5} {tmp_L:70} {fold(dc.license_template)}')

        if dc.license_load_template != LICENSE_LOAD_TEMPLATE_DEFAULT:# -Ll (licenses)
            tmp_Ll = f"({LICENSE_LOAD_TEMPLATE_TEXT})"
            print(f'  {"-Ll":5} {tmp_Ll:69} ',
                  f'{fold(dc.license_load_template)}')

        if dc.license_out_template != LICENSE_OUT_TEMPLATE_DEFAULT: # -Lo (licenses)
            tmp_Lo = f"({LICENSE_OUT_TEMPLATE_TEXT})"
            print(f'  {"-Lo":5} {tmp_Lo:69} ',
                  f'{fold(dc.license_out_template)}')


        if dc.name_template != NAME_TEMPLATE_DEFAULT:         # -t (names)
            tmp_t = f"({NAME_TEMPLATE_TEXT})"
            print(f'  {"-t":5} {tmp_t:70} {fold(dc.name_template)}')

        if dc.name_load_template != NAME_LOAD_TEMPLATE_DEFAULT:   # -tl (names)
            tmp_tl  = f"({NAME_LOAD_TEMPLATE_TEXT})"
            tmp_tl2 = fold(dc.name_load_template)
            print(f'  {"-tl":5} {tmp_tl:70} {tmp_tl2}')

        if dc.name_out_template != NAME_OUT_TEMPLATE_DEFAULT:    # -to (names)
            tmp_to = f"({NAME_OUT_TEMPLATE_TEXT})"
            print(f'  {"-to":5} {tmp_to:70} {fold(dc.name_out_template)}')


        if dc.year_template != YEAR_TEMPLATE_DEFAULT:         # -y (years)
            tmp_y = f"({YEAR_TEMPLATE_TEXT})"
            print(f'  {"-y":5} {tmp_y:70} {fold(dc.year_template)}')

        if dc.year_load_template != YEAR_LOAD_TEMPLATE_DEFAULT:   # -yl (years)
            tmp_yl  = f"({YEAR_LOAD_TEMPLATE_TEXT})"
            tmp_yl2 = fold(dc.year_load_template)
            print(f'  {"-yl":5} {tmp_yl:70} {tmp_yl2}')

        if dc.year_out_template != YEAR_OUT_TEMPLATE_DEFAULT:    # -yo (years)
            tmp_yo  = f"({YEAR_OUT_TEMPLATE_TEXT})"
            tmp_yo2 = fold(dc.year_out_template)
            print(f'  {"-yo":5} {tmp_yo:70} {tmp_yo2}')

        print("\n")

    if dc.verbose:
        if dc.regeneration:
            print("[CTANLoadOut] Info: CTANLoad (Regeneration)",
                  "is to be processed")
        if dc.load:
            print("[CTANLoadOut] Info: CTANLoad (Load)",
                  "is to be processed")
        if dc.check:
            print("[CTANLoadOut] Info: CTANLoad (Check)",
                  "is to be processed")
        if dc.output:
            print("[CTANLoadOut] Info: CTANOut",
                  "is to be processed")
        if dc.compile:
            print("[CTANLoadOut] Info: LuaLaTeX and MakeIndex",
                  "are to be processed")

    if dc.debugging:
        print("+++ <CTANLoadOut:head")                                  # -dbg

# ------------------------------------------------------------------
def main(dc=dc_var):                                                    # main function
    """
    Main Function

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Calls:
    -----
    + argparse_postprocessing()
    + argparse_process()
    + head()
    + func_call_regeneration()
    + func_call_load
    + func_call_check
    + func_call_output
    + func_call_compile
    + pre_make_calls()
    + make_call_load()
    + make_call_check()
    + make_call_output()
    + make_call_compile()
    + make_call_regeneration()

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    + dc.check	         flag: CTANLOad, check
    + dc.compile	 flag: compilation
    + dc.debugging	 flag -dbg (debugging)
    + dc.direc	         option -d (name of the OS directory)
    + dc.load	         flag: CTANLOad, load
    + dc.output	         flag: CTANOut
    + dc.output_name	 option -o (generic file name)
    + dc.regeneration	 flag: CTANLOad, regeneration
    + dc.statistics	 flag -stat (statistics output)
    + dc.verbose	 flag -v (output is verbose)

    Message:
    -------
    + CTANLoadOut, compile] Warning: LaTeX file '{file_name}' without
      real content

    """

    # 1.58   2025-10-05 time specification with unit
    # 2.3    2026-07-16 actTime -> ACT_TIME; actDate -> ACT_DATE (and
    #                   is therefore recognisable as a constant)
    # 2.6    2026-07-18 data class used
    # 2.6.3  2026-07-18 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 2.6.4  2026-07-18 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"   
    # 2.6.6  2026-07-18 "global" statements removed
    # 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the
    #                   data class
    # 2.7    2026-07-19 new functions (which group specific
    #                   instructions)
    # 2.7.1  2026-07-19 definitions of argparse_process,
    #                   argparse_postprocessing, pre_make_calls,
    #                   make_calls
    # 2.7.2  2026-07-19 Accessing the new functions
    # 2.13    2026-07-25 Break the function 'make_calls' into some    
    #                    functions.
    # 2.13.2  2026-07-25 Accessing the new features in main()
    # 2.14    2026-08-19 Avoid compiling LaTeX files with no real content
    # 2.14.2  2026-08-19 additional query + new error message
    # 2.16    2026-08-21 Calculation and output of the input string

    if dc.debugging:
        print("+++ >CTANLoadOut:main")                                  # -dbg

    if dc.verbose:
        print("=" * SEPLINE_LENGTH, "\n")

    arguments = EMPTY
    
    tmp = sys.argv[:]
    for f in range(1, len(tmp)):
        if not "-" in tmp[f]:
            tmp[f] = '"' + tmp[f] + '"'
    arguments = "CTANLoadOut.py" + SPACE + SPACE.join(tmp[1:])          # get the parameters of function call

    print("[CTANLoadOut] Info: CTANLoadOut\n")
    print(f"[CTANLoadOut] Info: original call: {arguments}\n")

    file_name:str = dc.direc + dc.output_name + ".tex"

    argparse_process()                                                  # Defines the arguments for the program CTANLoadOut and starts it.
    argparse_postprocessing()                                           # Postprocesses some parameters for the program CTANLoadOut.
    pre_make_calls()                                                    # Prepares dc.callx + other variables for further processing.
    
    if dc.load:
        make_call_load()                                                # generates call_load
    if dc.check:
        make_call_check()                                               # generates call_check
    if dc.output:
        make_call_output()                                              # generates call_output
    if dc.compile:
        make_call_compile()                                             # generates call_compile
    if dc.regeneration:
        make_call_regeneration()                                        # generates call_regeneration
    
    head()                                                              # Shows the given options

    if dc.regeneration:                                                 
        func_call_regeneration()                                        # CTANLoad (Regeneration) is to be processed.
    if dc.load:                                                         
        func_call_load()                                                # CTANLoad is to be called
    if dc.check:                                                        
        func_call_check()                                               # check is to be processed
    if dc.output:                                                       
        func_call_output()                                              # CTANOut is to be called
    if dc.compile:
        if os.path.getsize(file_name) >= MIN_TEX_SIZE:
            func_call_compile()                                         # the LaTeX processor will produce a PDF file
        else:
            print("[CTANLoadOut, compile] Warning: LaTeX file",
                  f" '{file_name}' without real content")
        
    print("-" * SEPLINE_LENGTH)

    if dc.statistics:                                                   # outputs the statistics
        PP         = 5
        endtotal   = time.time()
        endprocess = time.process_time()

        print("\nStatistics (CTANLoadOut):")
        print("date | time:".ljust(LEFT + 3), ACT_DATE, "|", ACT_TIME)
        print("program | version | date:".ljust(LEFT + 3),
              PROGRAMNAME_EXT, "|",
              PROGRAM_VERSION, "|", PROGRAM_DATE)

        print("---")
        print("total time (CTANLoadOut): ".ljust(LEFT + 3),
              str(round(endtotal - starttotal, 2)).rjust(PP), "s")
        print("process time (CTANLoadOut): ".ljust(LEFT + 3),
              str(round(endprocess - startprocess, 2)).rjust(PP), "s")

    if dc.verbose:
        print("\n" + "[CTANLoadOut] Info: CTANLoadOut completed")

    if dc.debugging:
        print("+++ <CTANLoadOut:main")                                  # -dbg
        

#===================================================================
# Main Part

# main part ---> main

##if __name__ == "__main__":
##    try:
##        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
##        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
##    except:
##        pass
##
##    starttotal   = time.time()                  # sets begin of total time
##    startprocess = time.process_time()          # sets begin of process time
##
##    main()                                      # main part called
##    if verbose:
##        print("\n" + "[CTANLoadOut] Info: CTANLoadOut completed")
##else:
##    print("[CTANLoadOut] Error: tried to use the program indirectly")
try:
    sys.stdout = codecs.getwriter(ENC)(sys.stdout.detach())
    sys.stderr = codecs.getwriter(ENC)(sys.stderr.detach())
except:
    pass

starttotal   = time.time()                                              # sets begin of total time
startprocess = time.process_time()                                      # sets begin of process time

main()                                                                  # main part called


#===================================================================
# History:

# 0.1  2021-05-01 start
# 0.9  2021-05-04 first working version
# 1.0  2021-05-24 program completed
# 1.1  2021-05-28 compilation enabled
# 1.2  2021-05-31 some improvements (calls, compilation)
# 1.3  2021-06-12 auxiliary function fold: shorten long option lists for output
# 1.4  2021-06-20 some smaller errors/deficiencies corrected
# 1.5  2021-06-23 error correction
# 1.6  2021-06-24 adaption for the CTANLoad option -r
# 1.7  2021-06-25 some new handling of subprocesses
# 1.8  2021-06-25 transfer of options to CTANLoad (Regeneration) improved; handling of -r improved
# 1.9  2021-07-01 adaption of the option -k (CTANLoad); new options -ko and -kl
# 1.10 2021-07-01 new auxiliary function remove_LaTeX_file: remove specified temporary LaTeX files
# 1.11 2021-07-05 function fold restructured
# 1.12 2021-07-06 new error message: tried to use the program indirectly
# 1.13 2021-07-07 remove temporary files enhanced: new function remove_other_file; remove_LaTeX_file enhanced
# 1.14 2021-07-15 option -A as in CTANOut enabled (-Ao and -Al, too)
# 1.15 2021-07-15 parameter 'encoding="utf8"' in subprocess.run calls removed
# 1.16 2021-07-15 some output texts changed + error messages for program exits always verbose
# 1.17 2021-07-18 output (listing of program options) enhanced
# 1.18 2021-07-18 xyz.tex and all other LaTeX relevant files before compilation a/o -mt removed
# 1.19 2021-07-19 there is no compilation if -A a/o -k a/o -t results "no packages found"
# 1.20 2021-07-19 -mo now prevents unintended loading of CTANLoad
# 1.21 2021-11-27 -sb (CTANOut) enabled
# 1.22 2021-11-28 process time and total time can be computed
# 1.23 2021-11-28 greater parts of comment blocks moved to external text files
# 1.24 2021-12-30 option -L enabled; changes in argparse, in the func_call_load and func_call_output functions
# 1.25 2022-01-02 argparse messages changed
# 1.26 2022-01-12 changes in func_call_compile, main, call_ouput
# 1.27 2022-01-22 corrections and changes of log output on terminal
# 1.28 2022-02-28 processing of -L, -Ll, -Lo (and related options) improved
# 1.29 2023-06-22 all Python comments revised
# 1.30 2023-06-22 new option -dbg (debugging) + processing
# 1.31 2023-06-22 processing of options improved; esp. to prevent collissions
# 1.32 2023-06-22 new option -nf (no files) installed + processing: relevant in CTANOut
# 1.33 2023-06-22 some additional requests/settings to avoid collissions of -nf with other options
# 1.34 2023-06-22 variable names (in the context of argparse) unified
# 1.35 2023-06-22 func_call_check improved
# 1.36 2023-06-22 new option -y (filtering on the base of years) + processing; relevant in CTANLoad and CTANOut
# 1.37 2023-06-26 some minor changes in statistics output
# 1.38 2023-06-28 fold() changed to adjust protocoll output
# 1.39 2023-07-01 messages with an additional identifier "[CTANLoadOut]"
# 1.40 2023-07-30 YEAR_TEMPLATE_DEFAULT adjusted to YEAR_TEMPLATE_DEFAULT in CTANLoad and CTANOut
# 1.41 2023-07-30 minor changes in message texts: to be executed --> is to be processed
# 1.42 2023-07-30 output of PROGRAMNAME_EXT / PROGRAM_VERSION / PROGRAM_DATE when -stat is set
# 1.43 2023-07-30 new concept for separation lines
# 1.44 2024-04-10 Time measurement for compilations; corresponding statistical output in each case

# 1.45   2024-04-13 new concept for [CTANLoadOut, check], [..., compilation], [..., index], [..., load], [..., output], [..., regeneration]
# 1.45.1 2024-04-13 everywhere: subprocess.run instead of subprocess.popen
# 1.45.2 2024-04-13 everywhere; parameter check=True, timeout=<number>
# 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut, check], [..., compilation], [..., index], [..., load], [..., output], [..., regeneration]
# 1.45.4 2024-04-13 better, more detailed handling of errors
# 1.45.5 2024-04-13 in [..., load], [..., output], [..., regeneration]: stdout is linked to a temporary auxiliary file that is processed line by line

# 1.46   2024-04-16 additional parameter 'errors="ignore"' for 'with TemporaryFile' in func_call_load, func_call_output
# 1.47   2024-04-17 addition: [CTANLoadOut, check], [..., compilation], [..., index], [..., load], [..., output], [..., regeneration]: except KeyboardInterrupt
# 1.48   2024-04-22 compiles related subprocesses revised: now more robust against coding errors
# 1.49   2024-04-22 .pdf and .log files removed before step2 and step3 in compilation subprocess

# 1.50   2024-04-23 tiout management revised
# 1.50.1 2024-04-23 variables renamed: timeoutDefault --> timeout etc
# 1.50.2 2024-04-23 new global variables: TIMEOUT_DEFAULT and TIMEOUT_TEXT
# 1.50.3 2024-04-23 new section in arparse processing: new options -tout and --timeout + corr. assigmnent to timeout

# 1.51   2024-05-94 new section in exception handling: UnicodeDecodeError
# 1.52   2024-06-02 BTYPE_DEFAULT changed to "@online"
# 1.53   2024-06-11 additional values for -m: tsv, csv
# 1.54   2024-06-12 some texts for -h and arparse changed

# 1.55   2024-07-20 argparse revised
# 1.55.1 2024-07-20 additional parameter in .ArgumentParser: prog, epilog, formatter_class
# 1.55.2 2024-07-20 subdivision into groups by .add_argument_group
# 1.55.3 2024-07-20 additional arguments in .add_argument (if it makes sense): type, metavar, action, dest

# 1.56   2025-02-09 everywhere: all source code lines wrapped at a maximum of 80 characters
# 1.57   2025-02-12 no test: __name__ == "__main__; ==> CTANLoad.py can be imported
# 1.58   2025-10-05 time specification with unit
# 1.59   2025-11-03 new: argparse groups
# 1.60   2025-11-03 argparse texts revised (x)
# 1.61   2025-11-17 texts changed: MAKE_OUTPUT_TEXT, PDF_OUTPUT_TEXT

# 2.0    2026-04-01 Complete revision (too many changes to list in the code)
# 2.0.1  2026-04-01 Functions with type annotations
# 2.0.2  2026-04-01 Variable annotations (where appropriate and possible)
# 2.0.3  2026-04-01 Constants in uppercase
# 2.0.4  2026-04-01 .format replaced with f-strings (where appropriate)
# 2.0.5  2026-04-01 __doc__ texts supplemented and standardised
# 2.0.6  2026-04-01 Standardised: Code up to a maximum of column 71
# 2.0.7  2026-04-01 Standardised: Comments from column 72 onwards

# 2.1    2026-04-15 corrections where arguments have been combined
# 2.2    2026-07-16 more f-strings
# 2.3    2026-07-16 actTime -> ACT_TIME; actDate -> ACT_DATE (and is therefore recognisable as a constant)
# 2.4    2026-07-16 encoding for subprocesses depends on operating system now

# 2.5    2026-07-17 backtracing
# 2.5.1  2026-07-17 new module traceback
# 2.5.2  2026-07-17 call traceback.print_exc()

# 2.6    2026-07-18 data class used
# 2.6.0  2026-07-18 new module dataclasses imported
# 2.6.1  2026-07-18 new class dataclass-variable (including all globally used variables) defined
# 2.6.2  2026-07-18 instance "dc_var" of this class created
# 2.6.3  2026-07-18 if necessary: Function definitions supplemented by the parameter "dc=dc_var"
# 2.6.4  2026-07-18 relevant local variables prefixed with "dc." and/or non-local with "dc_var"   
# 2.6.5  2026-07-18 original definitions of globally used variables removed
# 2.6.6  2026-07-18 "global" statements removed
# 2.6.7  2026-07-18 __doc__ texts supplemented/adapted to the data class

# 2.7    2026-07-19 new functions (which group specific instructions)
# 2.7.1  2026-07-19 definitions of argparse_process, argparse_postprocessing, pre_make_calls, make_calls
# 2.7.2  2026-07-19 Accessing the new functions

# 2.8    2026-07-19 data class dataclass_variable: converted to the existing global constants
# 2.9    2026-07-19 timout is float now

# 2.10   2026-07-20 Simplification of the 'make_calls' function
# 2.10.1  2026-07-20 in particular, (A) and (B) simplified
# 2.10.2  2026-07-20 new internal functions 'inner_load', 'inner_output'  for (A) and/or (B)

# 2.11    2026-07-21 New additional comments in 'make_calls' [(A), (B)]
# 2.12    2026-07-22 __doc__ text for module

# 2.13    2026-07-25 Break the function 'make_calls' into some functions.
# 2.13.2  2026-07-25 Accessing the new features in main()
# 2.13.3  2026-07-25 Add documentation and comments to functions.
# 2.13.4  2026-07-26 Take into account changes to the module’s __doc__ text.
# 2.13.5  2026-07-26 Remove the remnants of the 'make_calls' function.

# 2.14    2026-08-19 Avoid compiling LaTeX files with no real content
# 2.14.1  2026-08-19 new constant MIN_TEX_SIZE 
# 2.14.2  2026-08-19 additional query + new error message

# 2.15    2026-08-20 options log revised
# 2.16    2026-08-21 Calculation and output of the input string
# 2.17    2026-08-22 name and size of the resulting PDF file


# + offene Dateien auf jeden Fall schließen, auch wenn das Programm abgebrochen wurde

# ------------------------------------------------------------------
# Problems/Plans:
# + neuer Parameter für timeout (x)(?)
# + prüfen, ob ctanload -l -c aufgerufen werden muss (wenn CTANOut folgt)
# + ist -c gefährlich?
# + Programmabbruch bei -ko graphics oder -ko class (x)
# + Fehler bei LaTeX-Ausgabe: UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 262476: character maps to <undefined> (?)
# + argparse mit usage probieren: usage='%(prog)s [options]' (-)
# + initialer Test, ob CTAN verfügbar
# + Übersetzung (Compilierung) nur dann, wenn Pakete zu verarbeiten sind
# + Kriterien für Programmabbruch überprüfen sys.exit
# + Rolle call <--> callx überprüfen
# + alle Bereiche ausgiebig testen
# + call_chek mit -c ergänzen (nicht notwendig)
