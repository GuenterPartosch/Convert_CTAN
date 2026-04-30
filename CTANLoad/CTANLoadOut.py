#!/usr/bin/python3
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

"""
CTANLoadOut.py
(C) Günter Partosch, 2021|2022|2023|2024|2025/2026

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

CTANLoadOut.py may be started by:

1. python -u CTANLoadOut.py <option(s)>
-- always works
2. CTANLoadOut.py <option(s)>
-- if the OS knows how to handle Python files (files with the name
   extension .py)
4. menu_CTANLoadOut.py

 ---------------------------------------------------------------
 Requirements:
 + operating system windows 10/11 or Linux (like Linux Mint or Ubuntu or
   Debian)
 + wget a/o wget2 installed
 + Python installation 3.10 or newer
 + a series of Python modules (see the import instructions below)

 ---------------------------------------------------------------
CTANLoadOut.py needs the programs CTANLoad.py and CTANOut.py a/o the
excxutables CTANLoad and CTANOut.

see also CTANLoadOut-changes.txt
         CTANLoadOut-messages.txt
         CTANLoadOut.man

         CTANLoadOut-examples.txt
         CTANLoadOut-examples.bat
         CTANLoadOut-modules.txt
         CTAN-files.txt
"""


#===================================================================
# Moduls needed

import argparse                                                         # argument parsing
import sys                                                              # system calls
import platform                                                         # getting OS informations
import subprocess                                                       # handling of sub-processes
import re                                                               # regular expression
import os                                                               # deleting a file on disk, for instance
from os import path                                                     # path informations
import codecs                                                           # needed for full UTF-8 output# on stdout
import time                                                             # gets time|date of a file
from tempfile import TemporaryFile                                      # temporary file for subprocess.run


#===================================================================
# Settings

PROGRAMNAME_EXT   = "CTANLoadOut.py"                                    # program name (with extension)
PROGRAMNAME       = "CTANLoadOut"
PROGRAM_VERSION   = "2.1"
PROGRAM_DATE      = "2026-04-15"
PROGRAM_AUTHOR    = "Günter Partosch"
AUTHOIR_EMAIL     = "Guenter.Partosch@web.de\n(formerly " +\
                     "Guenter.Partosch@hrz.uni-giessen.de)"
AUTHOR_INST       = "formerly " + \
                    "Justus-Liebig-Universität, Hochschulrechenzentrum"

operatingsys:str  = platform.system()                                   # Operating system on which the program runs
call:list         = sys.argv                                            # get call and its options
actDate:str       = time.strftime("%Y-%m-%d")                           # actual date of program execution
actTime:str       = time.strftime("%X")                                 # actual time of program execution
empty_set         = set()                                               # set without any element

LATEX_PROCESSOR   = "lualatex"                                          # default LaTeX processor
INDEX_PROCESSOR   = "makeindex"                                         # default index processor

EMPTY             = ""
SPACE             = " "
ELLIPSIS          = " ..."
ENC               = "utf-8"

LEFT              = 35                                                  # width of labels in verbose output
SEPLINE_LENGTH    = 80                                                  # length of separation line in output

call_check:str    = EMPTY                                               # initialization
call_load:str     = EMPTY                                               # initialization
call_output:str   = EMPTY                                               # initialization
call_compile:str  = EMPTY                                               # initialization
call_index:str    = EMPTY                                               # initialization

delete_temporary_file:bool = True                                       # flag: in remove_LaTeX_file and remove_other_file

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
AUTHOR_TEMPLATE_TEXT      = "[CTANLoad and CTANOut] Name template " +\
                            "for authors"                               # option -A

LICENSE_LOAD_TEMPLATE_TEXT= "[CTANLoad] Name template for licenses"     # option -Ll
LICENSE_OUT_TEMPLATE_TEXT = "[CTANOut] Name template for licenses"      # option -Lo
LICENSE_TEMPLATE_TEXT     = "[CTANLoad and CTANOut] Name template " +\
                            "for licenses"                              # option -L

KEY_LOAD_TEMPLATE_TEXT    = "[CTANLoad] Template for keys"              # option -kl
KEY_OUT_TEMPLATE_TEXT     = "[CTANOut] Template for keys"               # option -ko
KEY_TEMPLATE_TEXT         = "[CTANLoad and CTANOut] Template for keys"  # option -k

NAME_LOAD_TEMPLATE_TEXT   = "[CTANLoad] Template for package names"     # option -tl
NAME_OUT_TEMPLATE_TEXT    = "[CTANOut] Template for package names"      # option -to
NAME_TEMPLATE_TEXT        = "[CTANLoad and CTANOut] Template for " +\
                            "package names"                             # option -t

YEAR_TEMPLATE_TEXT        = "[CTANLoad and CTANOut] Template for years" # option -y
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
YEAR_OUT_TEMPLATE_DEFAULT    = YEAR_LOAD_TEMPLATE_DEFAULT               # default for year_out_template (-yo) [four digits]

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


if operatingsys == "Windows":
    direc_sep      = "\\"
else:
    direc_sep      = "/"

DIREC_DEFAULT                = ACT_DIREC + direc_sep                    # default for -d (OS output folder)


#===================================================================
# Parsing the arguments

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

parser = argparse.\
         ArgumentParser(formatter_class = \
                        argparse.RawDescriptionHelpFormatter,
                        description     = f"{PROGRAMNAME}\nVersion:" +\
                        f" {PROGRAM_VERSION}" +\
                        f" ({PROGRAM_DATE})\n\n{PROGRAM_TEXT}  ",
                        prog    = PROGRAMNAME,
                        epilog  = "Thanks for using %(prog)s!",
                        )
parser._optionals.title   = 'Global options (without any processing)'

parser.add_argument("-a", "--author",                                   # option -a/--author
                    help    = AUTHOR_TEXT,
                    action  = 'version',
                    version = PROGRAM_AUTHOR+" ("+AUTHOIR_EMAIL + ", "+\
                              AUTHOR_INST + ")")

parser.add_argument("-dbg", "--debugging",                              # option -dbg/--debugging
                    help    = argparse.SUPPRESS,                        # will be suppressed in help
                    dest    = "debugging",
                    action  = "store_true",
                    default = DEBUGGING_DEFAULT)

parser.add_argument("-V", "--version",                                  # option -V/--version
                    help    = VERSION_TEXT,
                    action  = 'version',
                    version = '%(prog)s ' + PROGRAM_VERSION + " (" +\
                              PROGRAM_DATE + ")")

# ..................................................................
group1 = parser.add_argument_group("Other global options")

group1.add_argument("-d", "--directory",                                # option -d/--directory
                    metavar = "<directory>",
                    help    = DIREC_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "direc",
                    action  = "store",
                    default = DIREC_DEFAULT)

group1.add_argument("-mo", "--make_output",                             # option -mo/--make_output
                    help    = MAKE_OUTPUT_TEXT + " -- Default: " +\
                    "%(default)s",
                    dest    = "make_output",
                    action  = "store_true",
                    default = MAKE_OUTPUT_DEFAULT)

group1.add_argument("-o", "--output",                                   # option -o/--output
                    metavar = "<output name>",
                    help    = OUTPUT_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "output_name",
                    action  = "store",
                    default = OUTPUT_NAME_DEFAULT)

group1.add_argument("-tout", "--timeout",                               # option -tout/--timeout
                    metavar = "<timeout>",
                    help    = TIMEOUT_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "timeout",
                    action  = "store",
                    type    = float,
                    default = TIMEOUT_DEFAULT)

group1.add_argument("-stat", "--statistics",                            # option -stat/--statistics
                    help    = STATISTICS_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "statistics",
                    action  = "store_true",
                    default = STATISTICS_DEFAULT)

group1.add_argument("-v", "--verbose",                                  # option -v/--verbose
                    help    = VERBOSE_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "verbose",
                    action  = "store_true",
                    default = VERBOSE_DEFAULT)

# ..................................................................
group2 = parser.add_argument_group("Options for CTANLoad and CTANOut")

group2.add_argument("-A", "--author_template",                          # option -A/--author_template
                    metavar = "author template",
                    help    = AUTHOR_TEMPLATE_TEXT + " -- Default: " +\
                             "%(default)s",
                    dest    = "author_template",
                    action  = "store",
                    default = AUTHOR_TEMPLATE_DEFAULT)

group2.add_argument("-k", "--key_template",                             # option -k/--key_template
                    metavar = "<key template>",
                    help    = KEY_TEMPLATE_TEXT + " -- Default: " +\
                              "%(default)s",
                    dest    = "key_template",
                    action  = "store",
                    default = KEY_TEMPLATE_DEFAULT)

group2.add_argument("-L", "--license_template",                         # option -L/--license_template
                    metavar = "<license template>",
                    help    = LICENSE_TEMPLATE_TEXT + " -- Default: " +\
                              "%(default)s",
                    dest    = "license_template",
                    action = "store",
                    default = LICENSE_TEMPLATE_DEFAULT)

group2.add_argument("-t", "--name_template",                            # option -t/--template
                    metavar = "<name template>",
                    help    = NAME_TEMPLATE_TEXT + " -- Default: " +\
                              "%(default)s",
                    dest    = "name_template",
                    action  = "store",
                    default = NAME_TEMPLATE_DEFAULT)

group2.add_argument("-y", "--year_template",                            # option -y/--year_template
                    metavar = "<year template>",
                    help    = YEAR_TEMPLATE_TEXT + " -- Default: " +\
                              "%(default)s",
                    dest    = "year_template",
                    action  = "store",
                    default = YEAR_TEMPLATE_DEFAULT)

# ..................................................................
group3 = parser.add_argument_group("Options for CTANLoad")

group3.add_argument("-Al", "--author_load_template",                    # option -Al/--author_load_template
                    metavar = "<author load template>",
                    help    = AUTHOR_LOAD_TEMPLATE_TEXT + \
                              " -- Default: " +  "%(default)s",
                    dest    = "author_load_template",
                    action  = "store",
                    default = AUTHOR_LOAD_TEMPLATE_DEFAULT)

group3.add_argument("-f", "--download_files",                           # option -f/--download_files
                    help    = DOWNLOAD_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "download_files",
                    action  = "store_true",
                    default = DOWNLOAD_DEFAULT)

group3.add_argument("-kl", "--key_load_template",                       # option -kl/--key_load_template
                    metavar = "<key load temolate>",
                    help    = KEY_LOAD_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "key_load_template",
                    action  = "store",
                    default = KEY_LOAD_TEMPLATE_DEFAULT)

group3.add_argument("-Ll", "--license_load_template",                   # option -Ll/--license_load_template
                    metavar = "<license load template>",
                    help    = LICENSE_LOAD_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "license_load_template",
                    action  = "store",
                    default = LICENSE_LOAD_TEMPLATE_DEFAULT)

group3.add_argument("-n", "--number",                                   # option -n/--number
                    metavar = "<number>",
                    help    = NUMBER_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "number",
                    action  = "store",
                    type    = int,
                    default = NUMBER_DEFAULT)

group3.add_argument("-tl", "--name_load_template",                      # option -tl/--template_load
                    metavar = "<name load template>",
                    help    = NAME_LOAD_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "name_load_template",
                    action  = "store",
                    default = NAME_LOAD_TEMPLATE_DEFAULT)

group3.add_argument("-yl", "--year_load_template",                      # option -yl/--year_load_template
                    metavar = "<year load template>",
                    help    = YEAR_LOAD_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "year_load_template",
                    action  = "store",
                    default = YEAR_LOAD_TEMPLATE_DEFAULT)

# ..................................................................
group4 = parser.add_argument_group("Options for CTANOut")

group4.add_argument("-Ao", "--author_out_template",                     # option -Ao/--author_out_template
                    metavar = "<author out template>",
                    help    = AUTHOR_OUT_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "author_out_template",
                    action  = "store",
                    default = AUTHOR_OUT_TEMPLATE_DEFAULT)

group4.add_argument("-b", "--btype",                                    # option -b/--btype
                    help    = BTYPE_TEXT + " -- Default: " + \
                              "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan",
                               "@www"],
                    dest    = "btype",
                    action  = "store",
                    default = BTYPE_DEFAULT)

group4.add_argument("-ko", "--key_out_template",                        # option -ko/--key_out_template
                    metavar = "<key out template>",
                    help    = KEY_OUT_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "key_out_template",
                    action  = "store",
                    default = KEY_OUT_TEMPLATE_DEFAULT)

group4.add_argument("-Lo", "--license_out_template",                    # option -Lo/--license_out_template
                    metavar = "<license out template>",
                    help    = LICENSE_OUT_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "license_out_template",
                    action  = "store",
                    default = LICENSE_OUT_TEMPLATE_DEFAULT)

group4.add_argument("-m", "--mode",                                     # option -m/--mode
                    help    = MODE_TEXT + " -- Default: " + \
                             "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "ris",
                               "plain", "txt", "BibLaTeX", "biblatex",
                               "bib", "Excel", "excel", "csv", "tsv"],
                    dest    = "mode",
                    action  = "store",
                    default = MODE_DEFAULT)

group4.add_argument("-mt", "--make_topics",                             # option -mt/--make_topics
                    help    = TOPICS_TEXT + " -- Default: " + \
                              "%(default)s",
                    action  = "store_true",
                    default = MAKE_TOPICS_DEFAULT)

group4.add_argument("-nf", "--no_files",                                # option -nf/--no_files
                    help    = NO_FILES_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "no_files",
                    action  = "store_true",
                    default = NO_FILES_DEFAULT)

group4.add_argument("-s", "--skip",                                     # option -s/--skip
                    metavar = "<skip>",
                    help    = SKIP_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "skip",
                    action  = "store",
                    default = SKIP_DEFAULT)

group4.add_argument("-sb", "--skip_biblatex",                           # option -sb/--skip_biblatex
                    metavar = "<skip biblatex>",
                    help    = SKIP_BIBLATEX_TEXT + " -- Default: " + \
                             "%(default)s",
                    dest    = "skip_biblatex",
                    action  = "store",
                    default = SKIP_BIBLATEX_DEFAULT)

group4.add_argument("-to", "--name_out_template",                       # option -to/--template_out
                    metavar = "<name out template>",
                    help    = NAME_OUT_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "name_out_template",
                    action = "store",
                    default = NAME_OUT_TEMPLATE_DEFAULT)

group4.add_argument("-yo", "--year_out_template",                       # option -yo/--year_out_template
                    metavar = "<year out template>",
                    help    = YEAR_OUT_TEMPLATE_TEXT + \
                              " -- Default: " + "%(default)s",
                    dest    = "year_out_template",
                    action  = "store",
                    default = YEAR_OUT_TEMPLATE_DEFAULT)

# ..................................................................
group5 = parser.add_argument_group("Options for special actions")

group5.add_argument("-c", "--check_integrity",                          # option -i/--integrity
                    help    = INTEGRITY_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "check_integrity",
                    action  = "store_true",
                    default = INTEGRITY_DEFAULT)

group5.add_argument("-l", "--lists",                                    # option -l/--lists
                    help    = LISTS_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "lists",
                    action  = "store_true",
                    default = LISTS_DEFAULT)

group5.add_argument("-p", "--pdf_output",                               # option -p/--pdf_output
                    help    = PDF_OUTPUT_TEXT + " -- Default: " + \
                             "%(default)s",
                    dest    = "pdf_output",
                    action  = "store_true",
                    default = PDF_OUTPUT_DEFAULT)

group5.add_argument("-r", "--regenerate_pickle_files",                  # option -r/--regenerate_pickle_files
                    help    = REGENERATE_TEXT + " -- Default: " + \
                              "%(default)s",
                    dest    = "regenerate_pickle_files",
                    action  = "store_true",
                    default = REGENERATE_DEFAULT)


# ------------------------------------------------------------------
# Getting parsed options

# 1.50.3 2024.04-23 new section in arparse processing: new options 
#                   -tout and --timeout + corr. assigmnent to timeout

args                  = parser.parse_args()

author_template       = args.author_template                            # option -A
author_load_template  = args.author_load_template                       # option -Al
author_out_template   = args.author_out_template                        # option -Ao

license_template      = args.license_template                           # option -L
license_load_template = args.license_load_template                      # option -Ll
license_out_template  = args.license_out_template                       # option -Lo

name_template         = args.name_template                              # option -t
name_load_template    = args.name_load_template                         # option -tl
name_out_template     = args.name_out_template                          # option -to

key_template          = args.key_template                               # option -k
key_out_template      = args.key_out_template                           # option -ko
key_load_template     = args.key_load_template                          # option -kl

year_template         = args.year_template                              # option -y
year_load_template    = args.year_load_template                         # option -yl
year_out_template     = args.year_out_template                          # option -yo

btype                 = args.btype                                      # option -b
direc                 = args.direc                                      # option -d
download              = args.download_files                             # option -f

integrity             = args.check_integrity                            # option -c
lists                 = args.lists                                      # option -l
make_output           = args.make_output                                # option -mo
make_topics           = args.make_topics                                # option -mt
mode                  = args.mode                                       # option -m
number                = int(args.number)                                # option -n
no_files              = args.no_files                                   # option -nf
output_name           = args.output_name                                # option -o
pdf_output            = args.pdf_output                                 # option -p
regenerate            = args.regenerate_pickle_files                    # option -r
skip                  = args.skip                                       # option -s
skip_biblatex         = args.skip_biblatex                              # option -sb
statistics            = args.statistics                                 # option -stat

verbose               = args.verbose                                    # option -v
debugging             = args.debugging                                  # option -dbg

timeout               = int(args.timeout)                               # option -tout
timeout5              = timeout * 5                                     #
timeout10             = timeout * 10                                    #

# ------------------------------------------------------------------
# Correct direc

direc = direc.strip()                                                   # correct/expand OS folder name (-d)
if direc[len(direc) - 1] != direc_sep:
    direc += direc_sep


#===================================================================
# check values

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

# ------------------------------------------------------------------
# unifies modes

# 1.53   2024-06-11 additional values for -m: tsv, csv

if mode in ["LaTeX", "latex", "tex"]:                                   # LaTeX, latex, tex --> LaTeX
    mode = "LaTeX"
elif mode in ["BibLaTeX", "biblatex", "bib"]:                           # BibLaTeX, biblatex, bib --> BibLaTeX
    mode = "BibLaTeX"
elif mode in ["Excel", "excel", "csv", "tsv"]:                          # Excel, excel, tsv --> Excel
    mode = "Excel"
elif mode in ["RIS", "ris"]:                                            # RIS, ris --> RIS
    mode = "RIS"
elif mode in ["plain", "txt"]:                                          # plain, txt --> plain
    mode = "plain"
else:
    pass

# ------------------------------------------------------------------
# resets modes
print(EMPTY)

if verbose:
    print("-" * SEPLINE_LENGTH)

if (make_topics != MAKE_TOPICS_DEFAULT):                                # resets -m to LaTeX, if -mt is set
    if mode != "LaTeX":
        if verbose:
            print(ERR_MODE.format('-m', mode, '-m LaTeX', '-mt'))
        call.append("-m")
        call.append("LaTeX")
        mode = "LaTeX"
if (pdf_output != PDF_OUTPUT_DEFAULT):                                  # resets -m to LaTeX, if -p is set
    if mode != "LaTeX":
        if verbose:
            print(ERR_MODE.format('-m', mode, '-m LaTeX', '-p'))
            print(ERR_MODE.format('-mt =', make_topics, True, '-p'))
        call.append("-m")
        call.append("LaTeX")
        call.append("-mt")
        make_topics = True
        mode        = "LaTeX"
if (btype != BTYPE_DEFAULT):                                            # resets -m to BibLaTeX, if -b is set
    if mode != "BibLaTeX":
        if verbose:
            print(ERR_MODE.format('-m', mode, '-m BibLaTeX', "'-b'"))
        call.append("-m");
        call.append("BibLaTeX")
        mode = "BibLaTeX"
if (skip_biblatex != SKIP_BIBLATEX_DEFAULT):                            # resets -m to BibLaTeX, if -sb is set
    if mode != "BibLaTeX":
        if verbose:
            print(ERR_MODE.format('-m', mode, '-m BibLaTeX', "'-sb'"))
        call.append("-m");
        call.append("BibLaTeX")
        mode = "BibLaTeX"

# ------------------------------------------------------------------
# set load, check, compile, regeneration, and output

callx            = set(call[1:])                                        # copy (set type)

# corrections where arguments have been combined

# 2.1    2026-04-15 corrections where arguments have been combined 

if verbose != VERBOSE_DEFAULT:                                          # -v
    callx.add("-v")
if lists != LISTS_DEFAULT:                                              # -l
    callx.add("-l")
if integrity != INTEGRITY_DEFAULT:                                      # -c
    callx.add("-c")
if download != DOWNLOAD_DEFAULT:                                        # -f
    callx.add("-f")
if pdf_output != PDF_OUTPUT_DEFAULT:                                    # -p
    callx.add("-p")
if regenerate != REGENERATE_DEFAULT:                                    # -r
    callx.add("-r")
 
set_load         = {'-A', '--author_template', '-Al',
                    '--author_load_template', '-L',
                    '--license_template',  '-Ll',
                    '--license_load_template', '-f',
                    '--download_files', '-k', '--key_template',
                    '-kl', '--key_load_template', '-n', '--number',
                    '-t', '--template', '-tl', '--template_load',
                    '-dbg', '--debugging', '-y', '--year_template',
                    '-yl', '--year_load_template'}                      # possible Arguments for load
set_check        = {'-c','--check_integrity', '-l','--lists'}           # possible arguments for check
set_output       = { '-A', '--author_template', '-Ao',
                     '--author_out_template', '-b', '--btype', '-k',
                     '--key_template', '-ko', '--key_out_template',
                     '-L', '--license_template', '-Lo',
                     '--license_out_template', '-m', '--mode', '-mo',
                     '--make_output', '-mt', '--make_topics', '-s',
                     '--skip', '-sb', '--skip_biblatex' '-t',
                     '--template', '-to', '--template_out', '-dbg',
                     '--debugging', '-nf', 'no_files', '-y',
                     '--year_template', '-yo', '--year_out_template' }  # possible arguments for output
set_compile      = {'-p', '--pdf_output'}                               # possible arguments for compile
set_regeneration = {'-r', '--regenerate_pickle_files' }                 # possible arguments for regeneration

load             = callx & set_load         != empty_set                # there are options given for load
output           = callx & set_output       != empty_set                # there are options given for output
compile          = callx & set_compile      != empty_set                # there are options given for compile
check            = callx & set_check        != empty_set                # there are options given for check
regeneration     = callx & set_regeneration != empty_set                # there are options given for regeneration

# ------------------------------------------------------------------
# some other resettings

if load and output and (lists == LISTS_DEFAULT):                        # load, output, -l ==> check = True, -l = True
    if verbose:
        print(ERR_MODE.format("check =", check, True, "load & output"))
        print(ERR_MODE.format("-l =", lists, True, "load & output"))
    callx.add("-l")
    check = True
    lists = True

if (make_output != MAKE_OUTPUT_DEFAULT):                                # -mo ==> load = False
    if verbose:
        print(ERR_MODE.format("load =", load, False, "'-mo'"))
    load = False

if no_files != NO_FILES_DEFAULT:                                        # -nf ==> -p = True, -mt = True
    if pdf_output != PDF_OUTPUT_DEFAULT:                                # -p
        if verbose:
            print(ERR_MODE.format("-p =", pdf_output,
                                  PDF_OUTPUT_DEFAULT, "-nf"))
        pdf_output = PDF_OUTPUT_DEFAULT
    if make_topics != MAKE_TOPICS_DEFAULT:                              #   -mt
        if verbose:
            print(ERR_MODE.format("-mt =", make_topics,
                                  MAKE_TOPICS_DEFAULT, "-nf"))
        make_topics = MAKE_TOPICS_DEFAULT


#===================================================================
# Construct the calls

call_load         = EMPTY                                               # (A)
call_check        = EMPTY                                               # (B)
call_output       = EMPTY                                               # (C)
call_regeneration = EMPTY                                               # (D)
call_compile      = EMPTY                                               # (E)
call_index        = EMPTY                                               # (F)

# ------------------------------------------------------------------
# (A) call_load
# constructs the call for loading
# changes call_load

if load:
    if debugging:
        print("+++ >CTANLoadOut:call_load")                             # -dbg
    call_load = [sys.executable, "CTANLoad.py"]
    if direc != DIREC_DEFAULT:                                          # -d
        call_load.append("-d")
        call_load.append(direc)
    if number != NUMBER_DEFAULT:                                        # -n
        call_load.append("-n")
        call_load.append(str(number))
    if output_name != OUTPUT_NAME_DEFAULT:                              # -o
        call_load.append("-o")
        call_load.append(output_name)
    if download != DOWNLOAD_DEFAULT:                                    # -f
        call_load.append("-f")
    if statistics != STATISTICS_DEFAULT:                                # -stat
        call_load.append("-stat")
    if verbose != VERBOSE_DEFAULT:                                      # -v
        call_load.append("-v")
    if debugging != DEBUGGING_DEFAULT:                                  # -dbg
        call_load.append("-dbg")

    # process -t | -tl | -to
    w1 = name_template
    w2 = name_load_template
    w3 = name_out_template
    A1 = name_template      != NAME_TEMPLATE_DEFAULT                    # -t  is given
    A2 = name_load_template != NAME_LOAD_TEMPLATE_DEFAULT               # -tl  is given
    A3 = name_out_template  != NAME_OUT_TEMPLATE_DEFAULT                # -to  is given
    if A1:
        if A2 and A3:
            call_load.append("-t"); call_load.append(w2)                # -t
        elif A2 and not A3:
            call_load.append("-t"); call_load.append(w2)                # -t
        elif not A2 and A3:
            call_load.append("-t"); call_load.append(w1)                # -t
        elif not A2 and not A3:
            call_load.append("-t"); call_load.append(w1)                # -t
    else:
        if A2 and A3:
            call_load.append("-t"); call_load.append(w2)                # -t
        elif A2 and not A3:
            call_load.append("-t"); call_load.append(w2)                # -t
        elif not A2 and A3:
            pass

    # process -k | -kl | -ko
    w1 = key_template
    w2 = key_load_template
    w3 = key_out_template
    A1 = key_template      != KEY_TEMPLATE_DEFAULT                      # -k  is given
    A2 = key_load_template != KEY_LOAD_TEMPLATE_DEFAULT                 # -kl  is given
    A3 = key_out_template  != KEY_OUT_TEMPLATE_DEFAULT                  # -ko  is given
    if A1:
        if A2 and A3:
            call_load.append("-k"); call_load.append(w2)                # -k
        elif A2 and not A3:
            call_load.append("-k"); call_load.append(w2)                # -k
        elif not A2 and A3:
            call_load.append("-k"); call_load.append(w1)                # -k
        elif not A2 and not A3:
            call_load.append("-k"); call_load.append(w1)                # -k
    else:
        if A2 and A3:
            call_load.append("-k"); call_load.append(w2)                # -k
        elif A2 and not A3:
            call_load.append("-k"); call_load.append(w2)                # -k
        elif not A2 and A3:
            pass

    # process -A | -Al | -Ao
    w1 = author_template
    w2 = author_load_template
    w3 = author_out_template
    A1 = author_template      != AUTHOR_TEMPLATE_DEFAULT                # -A  is given
    A2 = author_load_template != AUTHOR_LOAD_TEMPLATE_DEFAULT           # -Al  is given
    A3 = author_out_template  != AUTHOR_OUT_TEMPLATE_DEFAULT            # -Ao  is given
    if A1:
        if A2 and A3:
            call_load.append("-A"); call_load.append(w2)                # -A
        elif A2 and not A3:
            call_load.append("-A"); call_load.append(w2)                # -A
        elif not A2 and A3:
            call_load.append("-A"); call_load.append(w1)                # -A
        elif not A2 and not A3:
            call_load.append("-A"); call_load.append(w1)                # -A
    else:
        if A2 and A3:
            call_load.append("-A"); call_load.append(w2)                # -A
        elif A2 and not A3:
            call_load.append("-A"); call_load.append(w2)                # -A
        elif not A2 and A3:
            pass

    # process -L | -Ll | -Lo
    w1 = license_template
    w2 = license_load_template
    w3 = license_out_template
    A1 = license_template      != LICENSE_TEMPLATE_DEFAULT              # -L  is given
    A2 = license_load_template != LICENSE_LOAD_TEMPLATE_DEFAULT         # -Ll  is given
    A3 = license_out_template  != LICENSE_OUT_TEMPLATE_DEFAULT          # -Lo  is given
    if A1:
        if A2 and A3:
            call_load.append("-L"); call_load.append(w2)                # -L
        elif A2 and not A3:
            call_load.append("-L"); call_load.append(w2)                # -L
        elif not A2 and A3:
            call_load.append("-L"); call_load.append(w1)                # -L
        elif not A2 and not A3:
            call_load.append("-L"); call_load.append(w1)                # -L
    else:
        if A2 and A3:
            call_load.append("-L"); call_load.append(w2)                # -L
        elif A2 and not A3:
            call_load.append("-L"); call_load.append(w2)                # -L
        elif not A2 and A3:
            pass

    # process -y | -yl | -yo
    w1 = year_template
    w2 = year_load_template
    w3 = year_out_template
    A1 = year_template      != YEAR_TEMPLATE_DEFAULT                    # -y  is given
    A2 = year_load_template != YEAR_LOAD_TEMPLATE_DEFAULT               # -yl  is given
    A3 = year_out_template  != YEAR_OUT_TEMPLATE_DEFAULT                # -yo  is given
    if A1:
        if A2 and A3:
            call_load.append("-y"); call_load.append(w2)                # -y
        elif A2 and not A3:
            call_load.append("-y"); call_load.append(w2)                # -y
        elif not A2 and A3:
            call_load.append("-y"); call_load.append(w1)                # -y
        elif not A2 and not A3:
            call_load.append("-y"); call_load.append(w1)                # -y
    else:
        if A2 and A3:
            call_load.append("-y"); call_load.append(w2)                # -y
        elif A2 and not A3:
            call_load.append("-y"); call_load.append(w2)                # -y
        elif not A2 and A3:
            pass

    if debugging:
        print("+++ <CTANLoadOut:call_load")                             # -dbg

# ------------------------------------------------------------------
# (B) call_check
# constructs the call for checking
# changes call_check

if check:
    if debugging:
        print("+++ >CTANLoadOut:call_check")                            # -dbg
    call_check = [sys.executable, "CTANLoad.py"]
    if verbose != VERBOSE_DEFAULT:                                      # -v
        call_check.append("-v")
    if statistics != STATISTICS_DEFAULT:                                # -stat
        call_check.append("-stat")
    if integrity != INTEGRITY_DEFAULT:                                  # -c
        call_check.append("-c")
    if lists != LISTS_DEFAULT:                                          # -l
        call_check.append("-l")
    if direc != DIREC_DEFAULT:                                          # -d
        call_check.append("-d")
        call_check.append(direc)
    if output_name != OUTPUT_NAME_DEFAULT:                              # -o
        call_check.append("-o")
        call_check.append(output_name)
    if debugging != DEBUGGING_DEFAULT:                                  # -dbg
        call_check.append("-dbg")

    if debugging:
        print("+++ <CTANLoadOut:call_check")                            # -dbg

# ------------------------------------------------------------------
# (C) call_output
# constructs the call for output generating
# changes call_output

if output:
    if debugging:
        print("+++ >CTANLoadOut:call_output")                           # -dbg
    call_output = [sys.executable, "CTANOut.py"]
    if verbose != VERBOSE_DEFAULT:                                      # -v
        call_output.append("-v")
    if statistics != STATISTICS_DEFAULT:                                # -stat
        call_output.append("-stat")
    if btype != BTYPE_DEFAULT:                                          # -b
        call_output.append("-b")
        call_output.append(btype)
    if skip_biblatex != SKIP_BIBLATEX_DEFAULT:                          # -sb
        call_output.append("-sb")
        call_output.append(skip_biblatex)
    if direc != DIREC_DEFAULT:                                          # -d
        call_output.append("-d")
        call_output.append(direc)
    if output_name != OUTPUT_NAME_DEFAULT:                              # -o
        call_output.append("-o")
        call_output.append(output_name)
    if mode != MODE_DEFAULT:                                            # -m
        call_output.append("-m")
        call_output.append(mode)
    if skip != SKIP_DEFAULT:                                            # -s
        call_output.append("-s")
        call_output.append(skip)
    if make_topics != MAKE_TOPICS_DEFAULT:                              # -mt
        call_output.append("-mt")
    if debugging != DEBUGGING_DEFAULT:                                  # -dbg
        call_output.append("-dbg")
    if no_files != NO_FILES_DEFAULT:                                    # -nf
        call_output.append("-nf")

    # process -t | -to | -tl
    w1 = name_template
    w2 = name_load_template
    w3 = name_out_template
    A1 = name_template      != NAME_TEMPLATE_DEFAULT                    # -t  is given
    A2 = name_load_template != NAME_LOAD_TEMPLATE_DEFAULT               # -tl  is given
    A3 = name_out_template  != NAME_OUT_TEMPLATE_DEFAULT                # -to  is given
    if A1:
        if A2 and A3:
            call_output.append("-t"); call_output.append(w3)            # -t
        elif A2 and not A3:
            call_output.append("-t"); call_output.append(w1)            # -t
        elif not A2 and A3:
            call_output.append("-t"); call_output.append(w3)            # -t
        elif not A2 and not A3:
            call_output.append("-t"); call_output.append(w1)            # -t
    else:
        if A2 and A3:
            call_output.append("-t"); call_output.append(w3)            # -t
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-t"); call_output.append(w3)            # -t

    # process -k | -ko | -kl
    w1 = key_template
    w2 = key_load_template
    w3 = key_out_template
    A1 = key_template      != KEY_TEMPLATE_DEFAULT                      # -k  is given
    A2 = key_load_template != KEY_LOAD_TEMPLATE_DEFAULT                 # -kl  is given
    A3 = key_out_template  != KEY_OUT_TEMPLATE_DEFAULT                  # -ko  is given
    if A1:
        if A2 and A3:
            call_output.append("-k"); call_output.append(w3)            # -k
        elif A2 and not A3:
            call_output.append("-k"); call_output.append(w1)            # -k
        elif not A2 and A3:
            call_output.append("-k"); call_output.append(w3)            # -k
        elif not A2 and not A3:
            call_output.append("-k"); call_output.append(w1)            # -k
    else:
        if A2 and A3:
            call_output.append("-k"); call_output.append(w3)            # -k
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-k"); call_output.append(w3)            # -k

    # process -A a7o -Ao | -Al
    w1 = author_template
    w2 = author_load_template
    w3 = author_out_template
    A1 = author_template      != AUTHOR_TEMPLATE_DEFAULT                # -A  is given
    A2 = author_load_template != AUTHOR_LOAD_TEMPLATE_DEFAULT           # -Al  is given
    A3 = author_out_template  != AUTHOR_OUT_TEMPLATE_DEFAULT            # -Ao  is given
    if A1:
        if A2 and A3:
            call_output.append("-A"); call_output.append(w3)            # -A
        elif A2 and not A3:
            call_output.append("-A"); call_output.append(w1)            # -A
        elif not A2 and A3:
            call_output.append("-A"); call_output.append(w3)            # -A
        elif not A2 and not A3:
            call_output.append("-A"); call_output.append(w1)            # -A
    else:
        if A2 and A3:
            call_output.append("-A"); call_output.append(w3)            # -A
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-A"); call_output.append(w3)            # -A

    # process -L | -Lo | -Ll
    w1 = license_template
    w2 = license_load_template
    w3 = license_out_template
    A1 = license_template      != LICENSE_TEMPLATE_DEFAULT              # -L  is given
    A2 = license_load_template != LICENSE_LOAD_TEMPLATE_DEFAULT         # -Ll  is given
    A3 = license_out_template  != LICENSE_OUT_TEMPLATE_DEFAULT          # -Lo  is given
    if A1:
        if A2 and A3:
            call_output.append("-L"); call_output.append(w3)            # -L
        elif A2 and not A3:
            call_output.append("-L"); call_output.append(w1)            # -L
        elif not A2 and A3:
            call_output.append("-L"); call_output.append(w3)            # -L
        elif not A2 and not A3:
            call_output.append("-L"); call_output.append(w1)            # -L
    else:
        if A2 and A3:
            call_output.append("-L"); call_output.append(w3)            # -L
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-L"); call_output.append(w3)            # -L

    # process -y | -yl | -yo
    w1 = year_template
    w2 = year_load_template
    w3 = year_out_template
    A1 = year_template      != YEAR_TEMPLATE_DEFAULT                    # -y  is given
    A2 = year_load_template != YEAR_LOAD_TEMPLATE_DEFAULT               # -yl  is given
    A3 = year_out_template  != YEAR_OUT_TEMPLATE_DEFAULT                # -yo  is given
    if A1:
        if A2 and A3:
            call_output.append("-y"); call_output.append(w3)            # -y
        elif A2 and not A3:
            call_output.append("-y"); call_output.append(w1)            # -y
        elif not A2 and A3:
            call_output.append("-y"); call_output.append(w3)            # -y
        elif not A2 and not A3:
            call_output.append("-y"); call_output.append(w1)            # -y
    else:
        if A2 and A3:
            call_output.append("-y"); call_output.append(w3)            # -y
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-y"); call_output.append(w3)            # -y

    if debugging:
        print("+++ <CTANLoadOut:call_output")                           # -dbg

# ------------------------------------------------------------------
# (E, F) call_compile + call_index

if compile:
    if debugging:
        print("+++ >CTANLoadOut:call_compilation")                      # -dbg
    direc_comp   = re.sub(r"\\", "/", direc)
    call_compile = [LATEX_PROCESSOR, direc_comp + output_name + ".tex"]
    call_index   = INDEX_PROCESSOR + SPACE + direc_comp + output_name +\
                   ".idx" + SPACE + "-o " + SPACE + direc_comp +\
                   output_name  + ".ind"

    if debugging:
        print("+++ <CTANLoadOut:call_compilation")                      # -dbg

# ------------------------------------------------------------------
# (D) call_regeneration
# constructs the call for regneration
# changes call_regeneration

if regeneration:
    if debugging:
        print("+++ >CTANLoadOut:call_regeneration")                     # -dbg
    call_regeneration = [sys.executable, "ctanload.py"]
    if verbose != VERBOSE_DEFAULT:                                      # -v
        call_regeneration.append("-v")
    if statistics != STATISTICS_DEFAULT:                                # -stat
        call_regeneration.append("-stat")
    if regenerate != REGENERATE_DEFAULT:                                # -r
        call_regeneration.append("-r")
    if number != NUMBER_DEFAULT:                                        # -n
        call_regeneration.append("-n")
        call_regeneration.append(str(number))
    if direc != DIREC_DEFAULT:                                          # -d
        call_regeneration.append("-d")
        call_regeneration.append(direc)
    if output_name != OUTPUT_NAME_DEFAULT:                              # -o
        call_regeneration.append("-o")
        call_regeneration.append(output_name)
    if debugging != DEBUGGING_DEFAULT:                                  # -dbg
        call_regeneration.append("-dbg")

    if debugging:
        print("+++ <CTANLoadOut:call_regeneration")                     # -dbg


#===================================================================
# Auxiliary functions

def fold(s:str) ->str:                                                  # function fold
    """
    auxiliary function: Shortens/foldens long option values for output.

    parameter:
    s: string, to be folded

    Returns a folded string.

    no messages
    """

    if debugging:
        print("+++ >CTANLoadOut:func_call_load")                        # -dbg

    OFFSET   = 79 * SPACE
    MAXLEN   = 70
    SEP      = "|"
    parts    = s.split(SEP)
    line:str = EMPTY
    out:str  = EMPTY
    for f in range(0,len(parts) ):
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
def remove_LaTeX_file(t:str):                                           # function remove_LaTeX_file
    """
    auxiliary function: Removes named LaTeX file.

    parameter:
    t: name of the file to be removed (str)

    message:
    + Warning: LaTeX file '{args.output_name + t}' removed
    """

    # external methods/functions:
    # path.exists
    # os.remove

    if debugging:
        print("+++ >CTANLoadOut:func_call_load")                        # -dbg

    if delete_temporary_file:
        if t in LATEX_FILES:
            if path.exists(args.output_name + t):
                os.remove(args.output_name + t)
                if verbose:
                    print("[CTANLoadOut] Warning: LaTeX file",
                          f" '{args.output_name + t}' removed")
            else:
                pass

# ------------------------------------------------------------------
def remove_other_file(t:str):                                           # function remove_other_file
    """
    auxiliary function: Removes named other file.

    parameter:
    t: file to be removed (str)

    message:
    + Warning: file '{args.output_name + t}' removed.
    """

    # external methods/functions:
    # path.exists
    # os.remove

    if debugging:
        print("+++ >CTANLoadOut:func_call_load")                        # -dbg

    if delete_temporary_file:
        if t in OTHER_FILES:
            if path.exists(args.output_name + t):
                os.remove(args.output_name + t)
                if verbose:
                    print("[CTANLoadOut] Warning: file",
                          f" '{args.output_name + t}' removed")
            else:
                pass


#===================================================================
# Functions

# ------------------------------------------------------------------
def func_call_load():                                                   # function func_call_load()
    """
    CTANLoad is processed.

    no parameters

    possible messages:
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

    # external methods/functions:
    # subprocess.run
    # sys.exit

    print("-" * SEPLINE_LENGTH)
    
    if debugging:
        print("+++ >CTANLoadOut:func_call_load")                        # -dbg

    print("[CTANLoadOut, load] Info: CTANLoad (Load)")

    try:
        with TemporaryFile("r+", encoding=ENC, errors="ignore") as f:   # temporary file
            process_load = subprocess.run(call_load, check=True,
                            encoding=ENC, stderr=subprocess.PIPE,
                            stdout=f, text=True,timeout=timeout10,
                            universal_newlines=True)                    # call load
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
            load_errormessage = process_load.stderr                     # possible error messageError: unicode decode error
            if len(load_errormessage) > 0:
                print(load_errormessage)
    except subprocess.CalledProcessError as exc:                        # process error
        if verbose:
            print("[CTANLoadOut, load] Error: called process",
                  f" '{call_load[1]}' not found,", sys.exc_info()[0])
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if verbose:
            print("[CTANLoadOut, load] Error:"
                  f" file '{call_load[0]}' not found", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if verbose:
            print("[CTANLoadOut, load] Error: timeout error", timeout10)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except:                                                             # any unspecified error
        if verbose:
            print("[CTANLoadOut, load] Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
        
    if verbose:
        print("\n" + "[CTANLoadOut,",
              "load] Info: CTANLoad (Load) completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_load")                        # -dbg

# ------------------------------------------------------------------
def func_call_check():                                                  # function func_call_check()
    """
    CTANLoad (Check) is processed.

    no parameters

    possible messages:
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

    # external methods/functions:
    # subprocess.run
    # sys.exit

    print("-" * SEPLINE_LENGTH)
    
    if debugging:
        print("+++ >CTANLoadOut:func_call_check")                       # -dbg

    print("[CTANLoadOut, check] Info: CTANLoad (Check)")

    try:
        with TemporaryFile("r+", encoding=ENC) as f:                    # temporary file
            process_check  = subprocess.run(call_check, check=True,
                                encoding=ENC, stderr=subprocess.PIPE,
                                stdout=f, text=True,timeout=timeout10,
                                universal_newlines=True)                # call check
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
            check_errormessage = process_check.stderr                   # possible error message
            if len(check_errormessage) > 0:
                print(check_errormessage)
    except subprocess.CalledProcessError as exc:                        # process error
        if verbose:
            print("[CTANLoadOut, check] Error: called process",
                  f" '{call_check[1]}' not found,", sys.exc_info()[0])
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if verbose:
            print("[CTANLoadOut, check] Error:",
                  f" file '{call_check[0]}' not found", exc)
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeoutInfo: CTANLoad (Check) completed
        if verbose:
            print("[CTANLoadOut, check] Error: timeout error", timeout5)
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except:                                                             # any unspecified error
        if verbose:
            print("[CTANLoadOut, check] Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, check] Error: program terminated")      # program terminated
    if verbose:
        print("\n" + "[CTANLoadOut, check] ",
              "Info: CTANLoad (Check) completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_check")                       # -dbg

# ------------------------------------------------------------------
def func_call_regeneration():                                           # function func_call_regeneration
    """
    CTANLoad (Regeneration) is processed.

    no parameters

    possible messages:
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

    # external methods/functions:
    # subprocess.run
    # sys.exit

    print("-" * SEPLINE_LENGTH)

    if debugging:
        print("+++ >CTANLoadOut:func_call_regneration")                 # -dbg

    print("[CTANLoadOut, regeneration] Info: CTANLoad (Regeneration)")

    try:
        with TemporaryFile("r+", encoding=ENC) as f:                    # temporary file
            process_regeneration = subprocess.run(call_regeneration,
                                    check=True, encoding=ENC,
                                    stderr=subprocess.PIPE, stdout=f,
                                    text=True,timeout=timeout10,
                                    universal_newlines=True)            # call regeneration
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
            regeneration_errormessage = process_regeneration.stderr     # possible error message
            if len(regeneration_errormessage) > 0:
                print(regeneration_errormessage)
    except subprocess.CalledProcessError as exc:                        # process error
        if verbose:
            print("[CTANLoadOut, regeneration] Error: called process",
                  f" '{call_regeneration[1]}' not found,",
                  sys.exc_info()[0])
        sys.exit("[CTANLoadOut, regeneration] " +\
                 "Error: program terminated")                           # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if verbose:
            print("[CTANLoadOut, regeneration] Error:",
                  f" file '{call_regeneration[0]}' not found", exc)
        sys.exit("[CTANLoadOut, regeneration] " +\
                 "Error: program terminated")                           # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if verbose:
            print("[CTANLoadOut, regeneration] Error: timeout error",
                  timeout10)
        sys.exit("[CTANLoadOut, regeneration] " +\
                 "Error: program terminated")                           # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except:                                                             # any unspecified error
        if verbose:
            print("[CTANLoadOut, regeneration] " +\
                  "Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, regeneration] " +\
                 "Error: program terminated")                           # program terminated
        
    if verbose:
        print("\n" + "[CTANLoadOut, regeneration] Info:" +\
              " CTANLoad (Regeneration) completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_regneration")                 # -dbg

# ------------------------------------------------------------------
def func_call_output():                                                 # function func_call_output
    """
    CTANOut is processed.

    no parameters

    possible messages:
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

    # func_call_output ---> remove_other_file
    # func_call_output ---> remove_LaTeX_file

    # --------------------------------------------
    # external methods/functions:
    # subprocess.run
    # sys.exit

    print("-" * SEPLINE_LENGTH)
    
    if debugging:
        print("+++ >CTANLoadOut:func_call_output")                      # -dbg

    print("[CTANLoadOut, output] Info: CTANOut")

    # removes some relevant files
    if mode == "BibLaTeX":
        remove_other_file(".bib")
    elif mode == "LaTeX":
        for e in [".tex", ".tap", ".top", ".xref", ".stat", ".tlp",
                  ".lic"]:
            remove_LaTeX_file(e)
    elif mode == "RIS":
        remove_other_file(".ris")
    elif mode == "plain":
        remove_other_file(".txt")
    elif mode == "Excel":
        remove_other_file(".tsv")
    else:
        pass

    try:
        with TemporaryFile("r+", encoding=ENC,
                           errors="ignore") as f:                       # temporary file
            process_out = subprocess.run(call_output, check=True,
                            encoding=ENC, stderr=subprocess.PIPE,
                            stdout=f, text=True,timeout=timeout10,
                            universal_newlines=True)                    # call output
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                print(line, end=EMPTY)
    except subprocess.CalledProcessError as exc:                        # process error
        if verbose:
            print("[CTANLoadOut, output] Error: called process" +\
                  f" '{call_output[1]}' not found,",
                  sys.exc_info()[0])
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated
    except FileNotFoundError as exc:                                    # file not found
        if verbose:
            print("[CTANLoadOut, output] Error:",
                  f" file '{call_output[0]}' not found", exc)
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if verbose:
            print("[CTANLoadOut, output] Error: timeout error", timeout)
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error",
                  exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")       # program terminated
    except:                                                             # any unspecified error
        if verbose:
            print("[CTANLoadOut, output] Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, output] Error: program terminated")     # program terminated
        
    if verbose:
        print("\n" + "[CTANLoadOut, output] Info: CTANOut completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_output")                      # -dbg

# ------------------------------------------------------------------
def func_call_compile():                                                # function func_call_compile
    """
    Compiles the generated LaTeX file.

    no parameters

    possible messages:
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

    # func_call_compile ---> remove_LaTeX_file

    # --------------------------------------------
    # external methods/functions:
    # path.exists

    if debugging:
        print("+++ >CTANLoadOut:func_call_compile")                     # -dbg

    print("-" * SEPLINE_LENGTH)
    
    print("[CTANLoadOut, compilation] Info: Compilation")

    file_name:str       = direc + output_name + ".tex"
    file_name_log:str   = direc + output_name + ".log"
    file_name_ilg:str   = direc + output_name + ".ilg"

    if path.exists(file_name):
        if path.getsize(file_name) > 3000:

            # step 1
            for e in [".aux", ".idx", ".ind", ".log", ".ilg", ".pdf",
                      ".out", ".bbl", ".indlualatex"]:
                remove_LaTeX_file(e)

            if verbose:
                print("." * SEPLINE_LENGTH)

            print(EMPTY)
            print("[CTANLoadOut, compilation] Info:", LATEX_PROCESSOR)
            if verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      call_compile)

            startcompiletotal   = time.time()                           # sets begin of total time
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_compile1      = subprocess.run(call_compile,
                                        timeout=timeout10, check=True,
                                        capture_output=True)            # call compile
                compile1_errormessage = \
                                process_compile1.stderr.decode(ENC)
                compile1_message      = \
                                process_compile1.stdout.decode(ENC)     # possible error message
                if len(compile1_errormessage) > 0:
                    if verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              " error in compilation")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoadOut, compilation] Info: more" +\
                              f" information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation] ",
                              "Info: Compilation OK")
            except subprocess.CalledProcessError as exc:                # process error
                if verbose:
                    print("[CTANLoadOut, compilation] ",
                          "Error: called process",
                          f" '{call_compile[1]}' not found,",
                          sys.exc_info()[0])
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: file" +\
                          f" '{call_compile[0]}' not found", exc)
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except subprocess.TimeoutExpired as exc:                    # timeout
                if verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: timeout error", timeout10)
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated\
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except:                                                     # any unspecified error
                if verbose:
                    print("[CTANLoadOut, compilation] Error: any",
                          "unspecified error", sys.exc_info())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated

            if statistics:                                              # outputs the compilation statistics
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
            if verbose:
                print("." * SEPLINE_LENGTH)
            for e in [".log", ".pdf"]:
                remove_LaTeX_file(e)

            if verbose:
                print("." * SEPLINE_LENGTH)

            print("[CTANLoadOut, compilation] Info:", LATEX_PROCESSOR)
            if verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      call_compile)

            startcompiletotal   = time.time()                           # sets begin of total time
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_compile2      = subprocess.run(call_compile,
                                        timeout=timeout10, check=True,
                                        capture_output=True)            # call compile
                compile2_errormessage = \
                                process_compile2.stderr.decode(ENC)
                compile2_message      = \
                                process_compile2.stdout.decode(ENC)
                                                                        # possible error message
                if len(compile2_errormessage) > 0:
                    if verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              "error in compilation")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoadOut, compilation] Info: more",
                              f"information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation]",
                              "Info: Compilation OK")
            except subprocess.CalledProcessError as exc:                # process error
                if verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: called process",
                          f"'{call_compile[1]}' not found,",
                          sys.exc_info()[0])
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: file",
                          f"'{call_compile[0]}' not found", exc)
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except subprocess.TimeoutExpired as exc:                    # timeout
                if verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: timeout error", timeout10)
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except:                                                     # any unspecified error
                if verbose:
                    print("[CTANLoadOut, compilation] Error:",
                          "any unspecified error",
                          sys.exc_info())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated

            if statistics:                                              # outputs the compilation statistics
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
            # step 3
            if verbose:
                print("." * SEPLINE_LENGTH)
            print("[CTANLoadOut, index] Info:", INDEX_PROCESSOR)
            if verbose:
                print("[CTANLoadOut, index] Info: Program call:",
                      call_index)

            startcompiletotal   = time.time()                           # sets begin of total time
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_index      = subprocess.run(call_index,
                                     timeout=timeout, check=True,
                                     capture_output=True,
                                     universal_newlines=True)           # call index
                index_errormessage = process_index.stderr               # possible error message
                index_message      = process_index.stdout
            except subprocess.CalledProcessError as exc:                # process error
                if verbose:
                    print("[CTANLoadOut, index] Error: called process",
                          f"'{call_index[1]}' not found,",
                          sys.exc_info()[0])
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if verbose:
                    print("[CTANLoadOut, index] Error: file",
                          f"'{call_index[0]}' not found", exc)
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated
            except subprocess.TimeoutExpired as exc:                    # timeout
                if verbose:
                    print("[CTANLoadOut, index] Error: timeout error",
                          timeout)
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except:                                                     # any unspecified error
                if verbose:
                    print("[CTANLoadOut, index]",
                          "Error: any unspecified error",sys.exc_info())
                sys.exit("[CTANLoadOut, index] " +\
                         "Error: program terminated")                   # program terminated

            if verbose:
                print("[CTANLoadOut, index] Info: more information",
                      f"in '{file_name_ilg}'")
                print("[CTANLoadOut, index] Info: Makeindex OK")

            if statistics:                                              # outputs the compilation statistics
                PP         = 5
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
            if verbose:
                print("." * SEPLINE_LENGTH)
                
            for e in [".log", ".pdf"]:
                remove_LaTeX_file(e)

            if verbose:
                print("." * SEPLINE_LENGTH)
            print("[CTANLoadOut, compilation] Info:", LATEX_PROCESSOR)
            if verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      call_compile)

            startcompiletotal   = time.time()                           # sets begin of total time\
            startcompileprocess = time.process_time()                   # sets begin of process time

            try:
                process_compile3      = subprocess.run(call_compile,
                                        timeout=timeout10, check=True,
                                        capture_output=True)            # call compile
                compile3_errormessage = \
                                process_compile3.stderr.decode(ENC)
                compile3_message      = \
                                process_compile3.stdout.decode(ENC)     # possible error message
                if len(compile3_errormessage) > 0:
                    if verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              "error in compilation")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoadOut, compilation] Info: more",
                              f"information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation]",
                              "Info: result in '" +\
                              direc + output_name + ".pdf'")
                        print("[CTANLoadOut, compilation]",
                              "Info: Compilation OK")
            except subprocess.CalledProcessError as exc:                # process error
                if verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: called process",
                          f"'{call_compile[1]}' not found,",
                          sys.exc_info()[0])
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated
            except FileNotFoundError as exc:                            # file not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: file"
                          f"'{call_compile[0]}' not found", exc)
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated\
            except subprocess.TimeoutExpired as exc:                    # timeout
                if verbose:
                    print("[CTANLoadOut, compilation]",
                          "Error: timeout error", timeout10)
                sys.exit("[CTANLoadOut, compilation] " +
                         "Error: program terminated")                   # program terminated
            except KeyboardInterrupt as exc:                            # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except UnicodeDecodeError as exc:                           # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load]",
                          "Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] " +\
                         "Error: program terminated")                   # program terminated
            except:                                                     # any unspecified error
                if verbose:
                    print("[CTANLoadOut, compilation] Error:",
                          "any unspecified error",
                          sys.exc_info())
                sys.exit("[CTANLoadOut, compilation] " +\
                         "Error: program terminated")                   # program terminated

            if statistics:                                              # outputs the compilation statistics
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
        else:
            if verbose: print("[CTANLoadOut, compilation]",
                              "Warning: LaTeX file",
                              f"'{file_name}' without content,",
                              "no compilation")
    else:
        if verbose: print("[CTANLoadOut, compilation] ",
                          "Warning: LaTeX file",
                          f"'{file_name}' does not exist, ",
                          "no compilation")

# ...................................................................
    if verbose:
        print("." * SEPLINE_LENGTH)
    # remove some LaTeX files
    for e in [".aux", ".idx", ".ind", ".out", ".bbl", ".indlualatex"]:
        remove_LaTeX_file(e)

    if debugging:
        print("+++ <CTANLoadOut:func_call_compile")                     # -dbg

# ------------------------------------------------------------------
def head():                                                             # function head
    """
    Shows the given options.

    no parameters

    no messages
    """

    # head ---> fold

    if debugging:
        print("+++ >CTANLoadOut:head")                                  # -dbg

    call[0] = "CTANLoadOut.py"
    print("[CTANLoadOut] Info: CTANLoadOut")
    
    if verbose:
        print(EMPTY)
        print("[CTANLoadOut] Info: Program call:", call)
        if ("-c" in callx) or ("--check_integrity" in call):            # -c (Flag)
            tmp_c = "(" + INTEGRITY_TEXT + ")"
            print(f'  {"-c":5} {tmp_c:70}')

        if ("-f" in callx) or ("--download_files" in call):             # -f (Flag)
            tmp_f = "(" + DOWNLOAD_TEXT + ")"
            print(f'  {"-f":5} {tmp_f:70}')

        if ("-l" in callx) or ("--lists" in call):                      # -l (Flag)
            tmp_l = "(" + (LISTS_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-l":5} {tmp_l:70}')

        if ("-mo" in call) or ("--make_output" in call):                # -mo (Flag)
            tmp_mo = "(" + (MAKE_OUTPUT_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-mo":5} {tmp_mo:70}')

        if ("-mt" in call) or ("--make_topics" in call):                # -mt (Flag)
            tmp_mt = "(" + (TOPICS_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-mt":5} {tmp_mt:70}')

        if ("-nf" in call) or ("--no_files" in call):                   # -nf (Flag)
            tmp_nf = "(" + (NO_FILES_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-nf":5} {tmp_nf:70}')

        if ("-p" in callx) or ("--pdf_output" in call):                 # -p (Flag)
            tmp_p = "(" + PDF_OUTPUT_TEXT + ")"
            print(f'  {"-p":5} {tmp_p:70}')

        if ("-r" in call) or ("--regenerate_pickle_files" in call):     # -r (Flag)
            tmp_r = "(" + REGENERATE_TEXT + ")"
            print(f'  {"-r":5} {tmp_r:70}')

        if ("-stat" in call) or ("--statistics" in call):               # -stat (Flag)
            tmp_stat = "(" + STATISTICS_TEXT + ")"
            print(f'  {"-stat":5} {tmp_stat:70}')

        if ("-v" in call) or ("--verbose" in call):                     # -v (Flag)
            tmp_v = "(" + VERBOSE_TEXT + ")"
            print(f'  {"-v":5} {tmp_v:70}')


        if ("-b" in call) or ("--btype" in call):                        # -b
            tmp_b = "(" + BTYPE_TEXT + ")"
            print(f'  {"-b":5} {tmp_b:70} {btype}')

        if ("-d" in call) or ("--directory" in call):                    # -d
            tmp_d = "(" + DIREC_TEXT + ")"
            print(f'  {"-d":5} {tmp_d:70} {direc}')

        if ("-m" in call) or ("--mode" in call):                        # -m
            tmp_m = "(" + MODE_TEXT + ")"
            print(f'  {"-m":5} {tmp_m:70} {mode}')

        if ("-n" in call) or ("--number" in call):                      # -n
            tmp_n = "(" + NUMBER_TEXT + ")"
            print(f'  {"-n":5} {tmp_n:70} {number}')

        if ("-o" in call) or ("--output" in call):                      # -o
            tmp_o = "(" + (OUTPUT_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-o":5} {tmp_o:70} {args.output_name}')

        if ("-s" in call) or ("--skip" in call):                        # -s
            tmp_s = "(" + SKIP_TEXT + ")"
            print(f'  {"-s":5} {tmp_s:70} {skip}')

        if ("-sb" in call) or ("--skip_biblatex" in call):              # -sb
            tmp_sb = "(" + SKIP_BIBLATEX_TEXT + ")"
            print(f'  {"-sb":5} {tmp_sb:70} {skip_biblatex}')

        if ("-tout" in call) or ("--timeout" in call):                  # -tout
            tmp_tout = "(" + TIMEOUT_TEXT + ")"
            print(f'  {"-tout":5} {tmp_tout:70} {timeout}')


        if ("-k" in call) or ("--key_template" in call):                # -k (keys)
            tmp_k = "(" + (KEY_TEMPLATE_TEXT + ")")[0:65] + ELLIPSIS
            print(f'  {"-k":5} {tmp_k:70} {fold(key_template)}')

        if ("-kl" in call) or ("--key_load_template" in call):          # -kl (keys)
            tmp_kl = "(" + (KEY_LOAD_TEMPLATE_TEXT + ")")[0:65]+ELLIPSIS
            print(f'  {"-kl":5} {tmp_kl:70} {fold(key_load_template)}')

        if ("-ko" in call) or ("--key_out_template" in call):           # -ko (keys)
            tmp_ko = "(" + (KEY_OUT_TEMPLATE_TEXT + ")")[0:65]+ ELLIPSIS
            print(f'  {"-ko":5} {tmp_ko:70} {fold(key_out_template)}')


        if ("-t" in call) or ("--name_template" in call):               # -t (names)
            tmp_t = "(" + NAME_TEMPLATE_TEXT + ")"
            print(f'  {"-t":5} {tmp_t:70} {fold(name_template)}')

        if ("-tl" in call) or ("--name_load_template" in call):         # -tl (names)
            tmp_tl = "(" + NAME_LOAD_TEMPLATE_TEXT + ")"
            print(f'  {"-tl":5} {tmp_tl:70} {fold(name_load_template)}')

        if ("-to" in call) or ("--name_out_template" in call):          # -to (names)
            tmp_to = "(" + NAME_OUT_TEMPLATE_TEXT + ")"
            print(f'  {"-to":5} {tmp_to:70} {fold(name_out_template)}')

        if ("-A" in call) or ("--author_template" in call):             # -A (authors)
            tmp_A = "(" + AUTHOR_TEMPLATE_TEXT + ")"
            print(f'  {"-A":5} {tmp_A:70} {fold(author_template)}')

        if ("-Al" in call) or ("--author_load_template" in call):       # -Al (authors)
            tmp_Al = "(" + AUTHOR_LOAD_TEMPLATE_TEXT + ")"
            print(f'  {"-Al":5} {tmp_Al:69} ',
                  f'{fold(author_load_template)}')

        if ("-Ao" in call) or ("--author_out_template" in call):        # -Ao (authors)
            tmp_Ao = "(" + AUTHOR_OUT_TEMPLATE_TEXT + ")"
            print(f'  {"-Ao":5} {tmp_Ao:69} ',
                  f'{fold(author_out_template)}')

        if ("-L" in call) or ("--license_template" in call):            # -L (licenses)
            tmp_L = "(" + LICENSE_TEMPLATE_TEXT + ")"
            print(f'  {"-L":5} {tmp_L:70} {fold(license_template)}')

        if ("-Ll" in call) or ("--license_load_template" in call):      # -Ll (licenses)
            tmp_Ll = "(" + LICENSE_LOAD_TEMPLATE_TEXT +")"
            print(f'  {"-Ll":5} {tmp_Ll:69} ',
                  f'{fold(license_load_template)}')

        if ("-Lo" in call) or ("--license_out_template" in call):       # -Lo (licenses)
            tmp_Lo = "(" + LICENSE_OUT_TEMPLATE_TEXT + ")"
            print(f'  {"-Lo":5} {tmp_Ll:69} ',
                  f'{fold(license_out_template)}')

        if ("-y" in call) or ("--year_template" in call):               # -y (years)
            tmp_y = "(" + YEAR_TEMPLATE_TEXT + ")"
            print(f'  {"-y":5} {tmp_y:70} {fold(year_template)}')

        if ("-yl" in call) or ("--year_load_template" in call):         # -yl (years)
            tmp_yl = "(" + YEAR_LOAD_TEMPLATE_TEXT + ")"
            print(f'  {"-yl":5} {tmp_yl:70} {fold(year_load_template)}')

        if ("-yo" in call) or ("--year_out_template" in call):          # -yo (years)
            tmp_yo = "(" + YEAR_OUT_TEMPLATE_TEXT + ")"
            print(f'  {"-yo":5} {tmp_yo:70} {fold(year_out_template)}')


        print("\n")

        if regeneration:
            print("[CTANLoadOut] Info: CTANLoad (Regeneration)",
                  "is to be processed")
        if load:
            print("[CTANLoadOut] Info: CTANLoad (Load)",
                  "is to be processed")
        if check:
            print("[CTANLoadOut] Info: CTANLoad (Check)",
                  "is to be processed")
        if output:
            print("[CTANLoadOut] Info: CTANOut",
                  "is to be processed")
        if compile:
            print("[CTANLoadOut] Info: LuaLaTeX and MakeIndex",
                  "are to be processed")

    if debugging:
        print("+++ <CTANLoadOut:head")                                  # -dbg

# ------------------------------------------------------------------
def main():                                                             # main function
    """
    Main Function

    no parameters

    no messages
    """

    # main ---> head
    # main ---> func_call_regeneration
    # main ---> func_call_load
    # main ---> func_call_check
    # main ---> func_call_output
    # main ---> func_call_compile

    # 1.58   2025-10-05 time specification with unit

    if debugging:
        print("+++ >CTANLoadOut:main")                                  # -dbg

    file_name:str = direc + output_name + ".tex"

    if verbose:
        print("=" * SEPLINE_LENGTH, "\n")
    head()

    if regeneration:                                                    # -r has been set
        func_call_regeneration()
    if load:                                                            # CTANLoad is to be called
        func_call_load()
    if check:                                                           # -l | -c has been set
        func_call_check()
    if output:                                                          # CTANOut is to be called
        func_call_output()
    if compile:                                                         # the LaTeX processor will produce a PDF file
        func_call_compile()
    print("-" * SEPLINE_LENGTH)

    if statistics:                                                      # outputs the statistics
        PP         = 5
        endtotal   = time.time()
        endprocess = time.process_time()

        print("\nStatistics (CTANLoadOut):")
        print("date | time:".ljust(LEFT + 3), actDate, "|", actTime)
        print("program | version | date:".ljust(LEFT + 3),
              PROGRAMNAME_EXT, "|",
              PROGRAM_VERSION, "|", PROGRAM_DATE)

        print("---")
        print("total time (CTANLoadOut): ".ljust(LEFT + 3),
              str(round(endtotal-starttotal, 2)).rjust(PP), "s")
        print("process time (CTANLoadOut): ".ljust(LEFT + 3),
              str(round(endprocess-startprocess, 2)).rjust(PP), "s")

    if debugging:
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
if verbose:
    print("\n" + "[CTANLoadOut] Info: CTANLoadOut completed")



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

# ------------------------------------------------------------------
# Problems/Plans:
# + neuer Parameter für timeout (x)(?)
# + prüfen, ob ctanload -l -c aufgerufen werden muss (wenn CTANOut folgt)
# + ist -c gefährlich?
# + Programmabbruch bei -ko graphics oder -ko class (x)
# + Fehler bei LaTeX-Ausgabe: UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 262476: character maps to <undefined> (?)
# + Programmabbruch bei Suchanfragen mit Umlauten, Eszet, diakritischen Buchstaben
# + argparse mit usage probieren: usage='%(prog)s [options]' (-)
# + initialer Test, ob CTAN verfügbar
# + Voß wird nicht weitergereicht 
