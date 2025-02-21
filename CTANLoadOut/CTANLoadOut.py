#!/usr/bin/python3
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

"""
CTANLoadOut.py
(C) Günter Partosch, 2021|2022|2023|2024|2025

CTANLoadOut.py is part of the CTAN bundle (CTANLoad.py, CTANOut.py,
CTANLoadOut.py, menu_CTANLoadOut.py).

CTANLoadOut.py combines the tasks of CTANLoayd.py and CTANOut.py:

CTANLoad.py: Loads XLM and PDF documentation files from CTAN a/o generates
             some special lists, and prepares data for CTANOut.
CTANOut.py:  Converts CTAN XLM package files to LaTeX, RIS, plain, BibLaTeX,
             Excel [tab separated].

CTANLoadOut.py must be located in the same OS directory as CTANLoad.py and
CTANOut.py.

CTANLoadOut.py may be started by:

1. python -u CTANLoadOut.py <option(s)>
-- always works
2. CTANLoadOut.py <option(s)>
-- if the OS knows how to handle Python files (files with the name extension .py)

4. menu_CTANLoadOut.py

 ---------------------------------------------------------------
 Requirements:
 + operating system windows 10/11 or Linux (like Linux Mint or Ubuntu or Debian)
 + wget a/o wget2 installed
 + Python installation 3.10 or newer
 + a series of Python modules (see the import instructions below)

 ---------------------------------------------------------------
CTANLoadOut.py needs the programs CTANLoad.py and CTANOut.py a/o the excxutables
CTANLoad and CTANOut-

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

import argparse                                 # argument parsing
import sys                                      # system calls
import platform                                 # getting OS informations
import subprocess                               # handling of sub-processes
import re                                       # regular expression
import os                                       # deleting a file on disk,
                                                # for instance
from os import path                             # path informations
import codecs                                   # needed for full UTF-8 output
                                                # on stdout
import time                                     # gets time|date of a file
from tempfile import TemporaryFile              # temporary file for
                                                # subprocess.run
                                                

#===================================================================
# Settings

programname_ext   = "CTANLoadOut.py"
programname       = "CTANLoadOut"
programversion    = "1.57"
programdate       = "2025-02-12"
programauthor     = "Günter Partosch"
authoremail       = "Guenter.Partosch@web.de\n(formerly " +\
                    "Guenter.Partosch@hrz.uni-giessen.de)"
authorinstitution = "formerly " + \
                    "Justus-Liebig-Universität, Hochschulrechenzentrum"

operatingsys      = platform.system()           # Operating system on which
                                                # the program runs
call              = sys.argv                    # get call and its options
actDate           = time.strftime("%Y-%m-%d")   # actual date of program
                                                # execution
actTime           = time.strftime("%X")         # actual time of program
                                                # execution
empty_set         = set()                       # set without any element

latex_processor   = "lualatex"                  # default LaTeX processor
index_processor   = "makeindex"                 # default index processor

empty             = ""
space             = " "
ellipse           = " ..."

left              = 35                          # width of labels in verbose
                                                # output
sepline_length    = 80                          # length of separation line in
                                                # output

call_check        = empty                       # initialization
call_load         = empty                       # initialization
call_output       = empty                       # initialization
call_compile      = empty                       # initialization
call_index        = empty                       # initialization

delete_temporary_file  = True                   # flag: in remove_LaTeX_file
                                                # and remove_other_file

err_mode          = "[CTANLoadOut] Warning: '{0} {1}' changed to '{2}' " + \
                    "(due to {3})"
latex_files       = [".aux", ".bib", ".ilg", ".log", ".idx", ".ilg", ".ind",
                     ".out", ".tex", ".pdf", ".stat", ".tap", ".top", ".xref"]
other_files       = [".ris", ".bib", ".txt", ".tsv"]

# ------------------------------------------------------------------
# Texts for argument parsing (argparse) and help

# 1.50.2 2024.04-23 new global variables: timeout_default and timeout_text
# 1.50.3 2024.04-23 new section in arparse processing: new options -tout and
#                   --timeout + corr. assigmnent to timeout
# 1.54   2024-06-12 some texts for -h and arparse changed

author_load_template_text = "[CTANLoad} Name template for authors"
                                                # option -Al
author_out_template_text  = "[CTANOut} Name template for authors"
                                                # option -Ao
author_template_text      = "[CTANLoad and CTANOut] Name template for authors"
                                                # option -A

license_load_template_text= "[CTANLoad] Name template for licenses"
                                                # option -Ll
license_out_template_text = "[CTANOut] Name template for licenses"
                                                # option -Lo
license_template_text     = "[CTANLoad and CTANOut] Name template for licenses"
                                                # option -L

key_load_template_text    = "[CTANLoad] Template for keys"
                                                # option -kl
key_out_template_text     = "[CTANOut] Template for keys"
                                                # option -ko
key_template_text         = "[CTANLoad and CTANOut] Template for keys"
                                                # option -k

name_load_template_text   = "[CTANLoad] Template for package names"
                                                # option -tl
name_out_template_text    = "[CTANOut] Template for package names"
                                                # option -to
name_template_text        = "[CTANLoad and CTANOut] Template for package names"
                                                # option -t

year_template_text        = "[CTANLoad and CTANOut] Template for years"
                                                # option -y
year_load_template_text   = "[CTANLoad] Template for years"
                                                # option -yl
year_out_template_text    = "[CTANOut] Template for years"
                                                # option -yo

author_text               = "[CTANLoadOut] Flag: Show author of the program" +\
                            " and exit."
                                                # option -a
download_text             = "[CTANLoad] Flag: Download associated" + \
                            " documentation files [PDF]."
                                                # option -f
integrity_text            = "[CTANLoad, check] Flag: Check the integrity of" + \
                            " the 2nd .pkl file."
                                                # option -c

lists_text                = "[CTANLoad, Check] Flag: Generate some special" +\
                            "lists and prepare files for CTANOut."
                                                # option -l
make_output_text          = "[CTANLoadOut] Flag: Do not activate CTANLoad."
                                                # option -mo
no_files_text             = "[CTANOut] Flag: Do not generate output files."
                                                # option -nf
pdf_output_text           = "[CTANOut] Flag: Generate PDF output viua LuaLaTeX."
                                                # option -p

regenerate_text           = "[CTANLoad, check] Flag: Regenerate the two" + \
                            " pickle files."
                                                # option -r
statistics_text           = "[CTANLoadOut] Flag: statistics on terminal."
                                                # option -stat
topics_text               = "[CTANOut] Flag: Generate topic lists [meaning" +\
                            " of topics + cross-reference (topics/packages," +\
                            " authors/packages); only for -m LaTeX]."
                                                # option -mt
verbose_text              = "[CTANLoadOut] Flag: Output is verbose."
                                                # option -v
version_text              = "[CTANLoadOut] Flag: Show version of the program" +\
                            " and exit."
                                                # option -V

btype_text                = "[CTANOut] Type of BibLaTex entries to be" + \
                            " generated [valid only for '-m BibLaTeX'/" + \
                            "'--mode BibLaTeX']"
                                                # option -b
direc_text                = "[CTANLoad and CTANOut] OS folder (directory)" +\
                            " for input and output files"
                                                # option -d
mode_text                 = "[CTANOut] Target format"
                                                # option -m
number_text               = "[CTANLoad] Maximum number of XML and PDF file" + \
                            " downloads"
                                                # option -n
output_text               = "[CTANLoad and CTANOut] Generic name for output" +\
                            " files [without extensions]"
                                                # option -o
skip_text                 = "[CTANOut] Skip specified CTAN fields."
                                                # option -s
skip_biblatex_text        = "[CTANOut] Skip specified BibLaTeX fields."
                                                # option -sb
timeout_text              = "[CTANLoad and CTANOut] default timeout (sec)" +\
                            " for subprocesses"
                                                # option -tout

program_text              = "Combines the tasks of CTANLoad  and CTANOut:\n" +\
                            " CTANLoad: Loads XLM and PDF documentation files" +\
                            " from CTAN a/o generates some special lists," +\
                            " and prepares data for CTANOut.\n" +\
                            " CTANOut:  Converts CTAN XLM package files to" + \
                            " some formats."

# ------------------------------------------------------------------
# Defaults/variables for argparse

# 1.50.2 2024.04-23 new global variables: timeout_default and timeout_text
# 1.50.3 2024.04-23 new section in arparse processing: new options -tout and
#                   --timeout + corr. assigmnent to timeout

author_template_default      = """^.+$"""       # default for author name
                                                # template (-A)
author_load_template_default = empty            # default for author load name
                                                # template (-Al)
author_out_template_default  = author_template_default
                                                # default for author out name
                                                # template (-Ao)

license_template_default     = """^.+$"""       # default for license name
                                                # template (-L)
license_load_template_default= empty            # default for license load
                                                # name template (-Ll)
license_out_template_default = license_template_default
                                                # default for license out
                                                # name template (-Lo)

key_template_default         = """^.+$"""       # default for option -k
key_load_template_default    = empty            # default for option -kl
key_out_template_default     = key_template_default
                                                # default for option -ko

name_template_default        = """^.+$"""       # default for option -t
name_load_template_default   = empty            # default for option -tl
name_out_template_default    = name_template_default
                                                # default for option -to

year_template_default        = """^19[89][0-9]|20[012][0-9]$"""
                                                # default for year template (-y)
                                                # [four digits]
year_load_template_default   = empty            # default for year_load_template
                                                # (-yl) [four digits]
year_out_template_default    = year_load_template_default
                                                # default for year_out_template
                                                # (-yo) [four digits]

btype_default                = "@online"        # default for option -b
                                                # (BibLaTeX entry type)
mode_default                 = "RIS"            # default for option -m
number_default               = 250              # default for option -n (maximum
                                                # number of files to be loaded)
output_name_default          = "all"            # default for option -o
                                                # (generic file name)
skip_default                 = "[]"             # default for option -s
skip_biblatex_default        = "[]"             # default for option -sb
timeout_default              = 60               # default for option -tout

download_default             = False            # flag: download PDF files
                                                # (option -f)
integrity_default            = False            # flag: integrity check
                                                # (option -c)
lists_default                = False            # flag: generate special lists
                                                # (option -l)
make_output_default          = False            # Flag: generate only output
                                                # (RIS, LaTeX, BibLaTeX, Excel,
                                                # plain)
make_topics_default          = False            # flag: make topics output
                                                # (option -mt)
no_files_default             = False            # flag: no output files
                                                # (option -nf)
pdf_output_default           = False            # flag: produce PDF output
                                                # (option -p)
regenerate_default           = False            # flag: regenerate pickle files
                                                # (option -r)
statistics_default           = False            # flag: output statistics
                                                # (option -stat)
verbose_default              = False            # flag: output is verbose
                                                # (option -v)
debugging_default            = False            # flag: debugging
                                                # (option -dbg)

act_direc                    = "."              # actual folder (directory) on OS

if operatingsys == "Windows":
    direc_sep      = "\\"
else:
    direc_sep      = "/"

direc_default                = act_direc + direc_sep
                                                # default for -d (OS output folder)


#===================================================================
# Parsing the arguments

# 1.50   2024-04-23 timeout management revised
# 1.50.3 2024.04-23 new section in arparse processing: new options -tout and
#                  --timeout + corr. assigmnent to timeout
# 1.53   2024-06-11 additional values for -m: tsv, csv
# 1.55   2024-07-20 argparse revised
# 1.55.1 2024-07-20 additional parameter in .ArgumentParser: prog, epilog,
#                   formatter_class
# 1.55.2 2024-07-20 subdivision into groups by .add_argument_group
# 1.55.3 2024-07-20 additional arguments in .add_argument (if it makes sense):
#                   type, metavar, action, dest

parser = argparse.ArgumentParser(formatter_class = argparse.\
                                 RawDescriptionHelpFormatter,
                                 description     = f"{programname}\nVersion:" +\
                                 f" {programversion}" +\
                                 f" ({programdate})\n\n{program_text}  ",
                                 prog            = programname,
                                 epilog          = "Thanks for using %(prog)s!",
                                 )
parser._optionals.title   = 'Global options (without any processing)'

parser.add_argument("-a", "--author",           # option -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = programauthor + " (" + authoremail + ", " +\
                    authorinstitution + ")")

parser.add_argument("-dbg", "--debugging",      # option -dbg/--debugging
                    help    = argparse.SUPPRESS,
                                                # will be suppressed in help
                    dest    = "debugging",
                    action  = "store_true",
                    default = debugging_default)

parser.add_argument("-V", "--version",          # option -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + programversion + " (" +\
                    programdate + ")")

# ..................................................................
group1 = parser.add_argument_group("Other global options")

group1.add_argument("-d", "--directory",        # option -d/--directory
                    metavar = "<directory>",
                    help    = direc_text + " -- Default: " + "%(default)s",
                    dest    = "direc",
                    action  = "store",
                    default = direc_default)

group1.add_argument("-mo", "--make_output",     # option -mo/--make_output
                    help    = make_output_text + " -- Default: " +\
                    "%(default)s",
                    dest    = "make_output",
                    action  = "store_true",
                    default = make_output_default)

group1.add_argument("-o", "--output",           # option -o/--output
                    metavar = "<output name>",
                    help    = output_text + " -- Default: " + "%(default)s",
                    dest    = "output_name",
                    action  = "store",
                    default = output_name_default)

group1.add_argument("-tout", "--timeout",       # option -tout/--timeout
                    metavar = "<timeout>",
                    help    = timeout_text + " -- Default: " + "%(default)s",
                    dest    = "timeout",
                    action  = "store",
                    type    = float,
                    default = timeout_default)

group1.add_argument("-stat", "--statistics",    # option -stat/--statistics
                    help    = statistics_text + " -- Default: " + "%(default)s",
                    dest    = "statistics",
                    action  = "store_true",
                    default = statistics_default)

group1.add_argument("-v", "--verbose",          # option -v/--verbose
                    help    = verbose_text + " -- Default: " + "%(default)s",
                    dest    = "verbose",
                    action  = "store_true",
                    default = verbose_default)

# ..................................................................
group2 = parser.add_argument_group("Options for CTANLoad and CTANOut")

group2.add_argument("-A", "--author_template",  # option -A/--author_template
                    metavar = "author template",
                    help    = author_template_text + " -- Default: " +\
                             "%(default)s",
                    dest    = "author_template",
                    action  = "store",
                    default = author_template_default)

group2.add_argument("-k", "--key_template",     # option -k/--key_template
                    metavar = "<key template>",
                    help    = key_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "key_template",
                    action  = "store",
                    default = key_template_default)

group2.add_argument("-L", "--license_template", # option -L/--license_template
                    metavar = "<license template>",
                    help    = license_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "license_template",
                    action = "store",
                    default = license_template_default)

group2.add_argument("-t", "--name_template",    # option -t/--template
                    metavar = "<name template>",
                    help    = name_template_text + " -- Default: " +\
                    "%(default)s",
                    dest    = "name_template",
                    action  = "store",
                    default = name_template_default)

group2.add_argument("-y", "--year_template",    # option -y/--year_template
                    metavar = "<year template>",
                    help    = year_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "year_template",
                    action  = "store",
                    default = year_template_default)

# ..................................................................
group3 = parser.add_argument_group("Options for CTANLoad")

group3.add_argument("-Al", "--author_load_template",
                                                # option -Al/
                                                # --author_load_template
                    metavar = "<author load template>",
                    help    = author_load_template_text + " -- Default: " +\
                             "%(default)s",
                    dest    = "author_load_template",
                    action  = "store",
                    default = author_load_template_default)

group3.add_argument("-f", "--download_files",   # option -f/--download_files
                    help    = download_text + " -- Default: " + "%(default)s",
                    dest    = "download_files",
                    action  = "store_true",
                    default = download_default)

group3.add_argument("-kl", "--key_load_template",
                                                # option -kl/--key_load_template
                    metavar = "<key load temolate>",
                    help    = key_load_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "key_load_template",
                    action  = "store",
                    default = key_load_template_default)

group3.add_argument("-Ll", "--license_load_template",
                                                # option -Ll/
                                                # --license_load_template
                    metavar = "<license load template>",
                    help    = license_load_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "license_load_template",
                    action  = "store",
                    default = license_load_template_default)

group3.add_argument("-n", "--number",           # option -n/--number
                    metavar = "<number>",
                    help    = number_text + " -- Default: " + "%(default)s",
                    dest    = "number",
                    action  = "store",
                    type    = int,
                    default = number_default)

group3.add_argument("-tl", "--name_load_template",
                                                # option -tl/--template_load
                    metavar = "<name load template>",
                    help    = name_load_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "name_load_template",
                    action  = "store",
                    default = name_load_template_default)

group3.add_argument("-yl", "--year_load_template",
                                                # option -yl/--year_load_template
                    metavar = "<year load template>",
                    help    = year_load_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "year_load_template",
                    action  = "store",
                    default = year_load_template_default)

# ..................................................................
group4 = parser.add_argument_group("Options for CTANOut")

group4.add_argument("-Ao", "--author_out_template",
                                                # option -Ao/
                                                # --author_out_template
                    metavar = "<author out template>",
                    help    = author_out_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "author_out_template",
                    action  = "store",
                    default = author_out_template_default)

group4.add_argument("-b", "--btype",            # option -b/--btype
                    help    = btype_text + " -- Default: " + "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan", "@www"],
                    dest    = "btype",
                    action  = "store",
                    default = btype_default)

group4.add_argument("-ko", "--key_out_template",
                                                # option -ko/--key_out_template
                    metavar = "<key out template>",
                    help    = key_out_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "key_out_template",
                    action  = "store",
                    default = key_out_template_default)

group4.add_argument("-Lo", "--license_out_template",
                                                # option -Lo/--license_out_template
                    metavar = "<license out template>",
                    help    = license_out_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "license_out_template",
                    action  = "store",
                    default = license_out_template_default)

group4.add_argument("-m", "--mode",             # option -m/--mode
                    help    = mode_text + " -- Default: " + "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "ris", "plain",
                               "txt", "BibLaTeX", "biblatex", "bib", "Excel",
                               "excel", "csv", "tsv"],
                    dest    = "mode",
                    action  = "store",
                    default = mode_default)

group4.add_argument("-mt", "--make_topics",     # option -mt/--make_topics
                    help    = topics_text + " -- Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_topics_default)

group4.add_argument("-nf", "--no_files",        # option -nf/--no_files
                    help    = no_files_text + " -- Default: " + "%(default)s",
                    dest    = "no_files",
                    action  = "store_true",
                    default = no_files_default)

group4.add_argument("-s", "--skip",             # option -s/--skip
                    metavar = "<skip>",
                    help    = skip_text + " -- Default: " + "%(default)s",
                    dest    = "skip",
                    action  = "store",
                    default = skip_default)

group4.add_argument("-sb", "--skip_biblatex",   # option -sb/--skip_biblatex
                    metavar = "<skip biblatex>",
                    help    = skip_biblatex_text + " -- Default: " + \
                             "%(default)s",
                    dest    = "skip_biblatex",
                    action  = "store",
                    default = skip_biblatex_default)

group4.add_argument("-to", "--name_out_template",
                                                # option -to/--template_out
                    metavar = "<name out template>",
                    help    = name_out_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "name_out_template",
                    action = "store",
                    default = name_out_template_default)

group4.add_argument("-yo", "--year_out_template",
                                                # option -yo/--year_out_template
                    metavar = "<year out template>",
                    help    = year_out_template_text + " -- Default: " +\
                              "%(default)s",
                    dest    = "year_out_template",
                    action  = "store",
                    default = year_out_template_default)

# ..................................................................
group5 = parser.add_argument_group("Options for special actions")

group5.add_argument("-c", "--check_integrity",  # option -i/--integrity
                    help    = integrity_text + " -- Default: " + "%(default)s",
                    dest    = "check_integrity",
                    action  = "store_true",
                    default = integrity_default)

group5.add_argument("-l", "--lists",            # option -l/--lists
                    help    = lists_text + " -- Default: " + "%(default)s",
                    dest    = "lists",
                    action  = "store_true",
                    default = lists_default)

group5.add_argument("-p", "--pdf_output",       # option -p/--pdf_output
                    help    = pdf_output_text + " -- Default: " + "%(default)s",
                    dest    = "pdf_output",
                    action  = "store_true",
                    default = pdf_output_default)

group5.add_argument("-r", "--regenerate_pickle_files",
                                                # option -r/
                                                # --regenerate_pickle_files
                    help    = regenerate_text + " -- Default: " + "%(default)s",
                    dest    = "regenerate_pickle_files",
                    action  = "store_true",
                    default = regenerate_default)


# ------------------------------------------------------------------
# Getting parsed options

# 1.50.3 2024.04-23 new section in arparse processing: new options -tout and
#                   --timeout + corr. assigmnent to timeout

args                  = parser.parse_args()
   
author_template       = args.author_template    # option -A
author_load_template  = args.author_load_template
                                                # option -Al
author_out_template   = args.author_out_template
                                                # option -Ao

license_template      = args.license_template   # option -L
license_load_template = args.license_load_template
                                                # option -Ll
license_out_template  = args.license_out_template
                                                # option -Lo

name_template         = args.name_template      # option -t
name_load_template    = args.name_load_template
                                                # option -tl
name_out_template     = args.name_out_template  # option -to

key_template          = args.key_template       # option -k
key_out_template      = args.key_out_template   # option -ko
key_load_template     = args.key_load_template  # option -kl

year_template         = args.year_template      # option -y
year_load_template    = args.year_load_template
                                                # option -yl
year_out_template     = args.year_out_template  # option -yo

btype                 = args.btype              # option -b
direc                 = args.direc              # option -d
download              = args.download_files     # option -f

integrity             = args.check_integrity    # option -c
lists                 = args.lists              # option -l
make_output           = args.make_output        # option -mo
make_topics           = args.make_topics        # option -mt
mode                  = args.mode               # option -m
number                = int(args.number)        # option -n
no_files              = args.no_files           # option -nf
output_name           = args.output_name        # option -o
pdf_output            = args.pdf_output         # option -p
regenerate            = args.regenerate_pickle_files
                                                # option -r
skip                  = args.skip               # option -s
skip_biblatex         = args.skip_biblatex      # option -sb
statistics            = args.statistics         # option -stat

verbose               = args.verbose            # option -v
debugging             = args.debugging          # option -dbg

timeout               = int(args.timeout)       # option -tout
timeout5              = timeout * 5             # 
timeout10             = timeout * 10            #

# ------------------------------------------------------------------
# Correct direc

direc = direc.strip()                           # correct/expand OS
                                                # folder name (-d)
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

if mode in ["LaTeX", "latex", "tex"]:           # LaTeX, latex, tex --> LaTeX
    mode = "LaTeX"
elif mode in ["BibLaTeX", "biblatex", "bib"]:   # BibLaTeX, biblatex, bib -->
                                                # BibLaTeX
    mode = "BibLaTeX"
elif mode in ["Excel", "excel", "csv", "tsv"]:  # Excel, excel, tsv --> Excel
    mode = "Excel"
elif mode in ["RIS", "ris"]:                    # RIS, ris --> RIS
    mode = "RIS"
elif mode in ["plain", "txt"]:                  # plain, txt --> plain
    mode = "plain"
else:
    pass

# ------------------------------------------------------------------
# resets modes
print(empty)

if verbose:
    print("-" * sepline_length)

if (make_topics != make_topics_default):        # resets -m to LaTeX,
                                                # if -mt is set
    if mode != "LaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m LaTeX', '-mt'))
        call.append("-m")
        call.append("LaTeX")
        mode = "LaTeX"
if (pdf_output != pdf_output_default):          # resets -m to LaTeX,
                                                # if -p is set
    if mode != "LaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m LaTeX', '-p'))
            print(err_mode.format('-mt =', make_topics, True, '-p'))
        call.append("-m")
        call.append("LaTeX")
        call.append("-mt")
        make_topics = True
        mode        = "LaTeX"
if (btype != btype_default):                    # resets -m to BibLaTeX,
                                                # if -b is set
    if mode != "BibLaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m BibLaTeX', "'-b'"))
        call.append("-m");
        call.append("BibLaTeX")
        mode = "BibLaTeX"
if (skip_biblatex != skip_biblatex_default):    # resets -m to BibLaTeX,
                                                # if -sb is set
    if mode != "BibLaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m BibLaTeX', "'-sb'"))
        call.append("-m");
        call.append("BibLaTeX")
        mode = "BibLaTeX"

# ------------------------------------------------------------------
# set load, check, compile, regeneration, and output

callx            = set(call[1:])                # copy (set type)

set_load         = {'-A', '--author_template', '-Al', '--author_load_template',
                    '-L', '--license_template',  '-Ll',
                    '--license_load_template', '-f', '--download_files', '-k',
                    '--key_template', '-kl', '--key_load_template', '-n',
                    '--number', '-t', '--template', '-tl', '--template_load',
                    '-dbg', '--debugging', '-y', '--year_template', '-yl',
                    '--year_load_template'}
set_check        = {'-c','--check_integrity', '-l','--lists'}
set_output       = { '-A', '--author_template', '-Ao', '--author_out_template',
                     '-b', '--btype', '-k', '--key_template', '-ko',
                     '--key_out_template', '-L', '--license_template', '-Lo',
                     '--license_out_template', '-m', '--mode', '-mo',
                     '--make_output', '-mt', '--make_topics', '-s', '--skip',
                     '-sb', '--skip_biblatex' '-t', '--template', '-to',
                     '--template_out', '-dbg', '--debugging', '-nf', 'no_files',
                     '-y', '--year_template', '-yo', '--year_out_template' }
set_compile      = {'-p', '--pdf_output'}
set_regeneration = {'-r', '--regenerate_pickle_files' }

load             = callx & set_load         != empty_set
                                                # there are options given
                                                # for load
output           = callx & set_output       != empty_set
                                                # there are options given
                                                # for output
compile          = callx & set_compile      != empty_set
                                                # there are options given
                                                # for compile
check            = callx & set_check        != empty_set
                                                # there are options given
                                                # for check
regeneration     = callx & set_regeneration != empty_set
                                                # there are options given
                                                # for regeneration

# ------------------------------------------------------------------
# some other resettings

if load and output and (lists == lists_default):
                                                # load, output, -l ==>
                                                # check = True, -l = True
    if verbose:
        print(err_mode.format("check =", check, True, "load & output"))
        print(err_mode.format("-l =", lists, True, "load & output"))
    callx.add("-l")
    check = True
    lists = True

if (make_output != make_output_default):        # -mo ==> load = False
    if verbose:
        print(err_mode.format("load =", load, False, "'-mo'"))
    load = False

if no_files != no_files_default:                # -nf ==> -p = True, -mt = True
    if pdf_output != pdf_output_default:        #   -p
        if verbose:
            print(err_mode.format("-p =", pdf_output, pdf_output_default, "-nf"))
        pdf_output = pdf_output_default
    if make_topics != make_topics_default:      #   -mt
        if verbose:
            print(err_mode.format("-mt =", make_topics, make_topics_default,
                                  "-nf"))
        make_topics = make_topics_default

#===================================================================
# Construct the calls

call_load         = empty    # (A)
call_check        = empty    # (B)
call_output       = empty    # (C)
call_regeneration = empty    # (D)
call_compile      = empty    # (E)
call_index        = empty    # (F)

# ------------------------------------------------------------------
# (A) call_load
# constructs the call for loading
# changes call_load

if load:
    if debugging:
        print("+++ >CTANLoadOut:call_load")     # -dbg                                    
    call_load = [sys.executable, "CTANLoad.py"]
    if direc != direc_default:                  # -d
        call_load.append("-d")
        call_load.append(direc)
    if number != number_default:                # -n
        call_load.append("-n")
        call_load.append(str(number))
    if output_name != output_name_default:      # -o
        call_load.append("-o")
        call_load.append(output_name)
    if download != download_default:            # -f
        call_load.append("-f")
    if statistics != statistics_default:        # -stat
        call_load.append("-stat")
    if verbose != verbose_default:              # -v
        call_load.append("-v")
    if debugging != debugging_default:          # -dbg
        call_load.append("-dbg")

    # process -t | -tl | -to
    w1 = name_template
    w2 = name_load_template
    w3 = name_out_template
    A1 = name_template      != name_template_default
                                                # -t  is given
    A2 = name_load_template != name_load_template_default
                                                # -tl  is given
    A3 = name_out_template  != name_out_template_default
                                                # -to  is given
    if A1:
        if A2 and A3:
            call_load.append("-t"); call_load.append(w2)
                                                # -t
        elif A2 and not A3:
            call_load.append("-t"); call_load.append(w2)
                                                # -t
        elif not A2 and A3:
            call_load.append("-t"); call_load.append(w1)
                                                # -t
        elif not A2 and not A3:
            call_load.append("-t"); call_load.append(w1)
                                                # -t
    else:
        if A2 and A3:
            call_load.append("-t"); call_load.append(w2)
                                                # -t
        elif A2 and not A3:
            call_load.append("-t"); call_load.append(w2)
                                                # -t
        elif not A2 and A3:
            pass

    # process -k | -kl | -ko
    w1 = key_template
    w2 = key_load_template
    w3 = key_out_template
    A1 = key_template      != key_template_default
                                                # -k  is given
    A2 = key_load_template != key_load_template_default
                                                # -kl  is given
    A3 = key_out_template  != key_out_template_default
                                                # -ko  is given
    if A1:
        if A2 and A3:
            call_load.append("-k"); call_load.append(w2)
                                                # -k
        elif A2 and not A3:
            call_load.append("-k"); call_load.append(w2)
                                                # -k
        elif not A2 and A3:
            call_load.append("-k"); call_load.append(w1)
                                                # -k
        elif not A2 and not A3:
            call_load.append("-k"); call_load.append(w1)
                                                # -k
    else:
        if A2 and A3:
            call_load.append("-k"); call_load.append(w2)
                                                # -k
        elif A2 and not A3:
            call_load.append("-k"); call_load.append(w2)
                                                # -k
        elif not A2 and A3:
            pass

    # process -A | -Al | -Ao
    w1 = author_template
    w2 = author_load_template
    w3 = author_out_template
    A1 = author_template      != author_template_default
                                                # -A  is given
    A2 = author_load_template != author_load_template_default
                                                # -Al  is given
    A3 = author_out_template  != author_out_template_default
                                                # -Ao  is given
    if A1:
        if A2 and A3:
            call_load.append("-A"); call_load.append(w2)
                                                # -A
        elif A2 and not A3:
            call_load.append("-A"); call_load.append(w2)
                                                # -A
        elif not A2 and A3:
            call_load.append("-A"); call_load.append(w1)
                                                # -A
        elif not A2 and not A3:
            call_load.append("-A"); call_load.append(w1)
                                                # -A
    else:
        if A2 and A3:
            call_load.append("-A"); call_load.append(w2)
                                                # -A
        elif A2 and not A3:
            call_load.append("-A"); call_load.append(w2)
                                                # -A
        elif not A2 and A3:
            pass

    # process -L | -Ll | -Lo
    w1 = license_template
    w2 = license_load_template
    w3 = license_out_template
    A1 = license_template      != license_template_default
                                                # -L  is given
    A2 = license_load_template != license_load_template_default
                                                # -Ll  is given
    A3 = license_out_template  != license_out_template_default
                                                # -Lo  is given
    if A1:
        if A2 and A3:
            call_load.append("-L"); call_load.append(w2)
                                                # -L
        elif A2 and not A3:
            call_load.append("-L"); call_load.append(w2)
                                                # -L
        elif not A2 and A3:
            call_load.append("-L"); call_load.append(w1)
                                                # -L
        elif not A2 and not A3:
            call_load.append("-L"); call_load.append(w1)
                                                # -L
    else:
        if A2 and A3:
            call_load.append("-L"); call_load.append(w2)
                                                # -L
        elif A2 and not A3:
            call_load.append("-L"); call_load.append(w2)
                                                # -L
        elif not A2 and A3:
            pass

    # process -y | -yl | -yo
    w1 = year_template
    w2 = year_load_template
    w3 = year_out_template
    A1 = year_template      != year_template_default
                                                # -y  is given
    A2 = year_load_template != year_load_template_default
                                                # -yl  is given
    A3 = year_out_template  != year_out_template_default
                                                # -yo  is given
    if A1:
        if A2 and A3:
            call_load.append("-y"); call_load.append(w2)
                                                # -y
        elif A2 and not A3:
            call_load.append("-y"); call_load.append(w2)
                                                # -y
        elif not A2 and A3:
            call_load.append("-y"); call_load.append(w1)
                                                # -y
        elif not A2 and not A3:
            call_load.append("-y"); call_load.append(w1)
                                                # -y
    else:
        if A2 and A3:
            call_load.append("-y"); call_load.append(w2)
                                                # -y
        elif A2 and not A3:
            call_load.append("-y"); call_load.append(w2)
                                                # -y
        elif not A2 and A3:
            pass
        
    if debugging:
        print("+++ <CTANLoadOut:call_load")     # -dbg                                    

# ------------------------------------------------------------------
# (B) call_check
# constructs the call for checking
# changes call_check

if check:
    if debugging:
        print("+++ >CTANLoadOut:call_check")    # -dbg
    call_check = [sys.executable, "CTANLoad.py"]
    if verbose != verbose_default:
                                                # -v
        call_check.append("-v")
    if statistics != statistics_default:        # -stat
        call_check.append("-stat")
    if integrity != integrity_default:          # -c
        call_check.append("-c")
    if lists != lists_default:                  # -l
        call_check.append("-l")
    if direc != direc_default:                  # -d
        call_check.append("-d")
        call_check.append(direc)
    if output_name != output_name_default:      # -o
        call_check.append("-o")
        call_check.append(output_name)
    if debugging != debugging_default:          # -dbg
        call_check.append("-dbg")

    if debugging:
        print("+++ <CTANLoadOut:call_check")    # -dbg

# ------------------------------------------------------------------
# (C) call_output
# constructs the call for output generating
# changes call_output

if output:
    if debugging:
        print("+++ >CTANLoadOut:call_output")   # -dbg
    call_output = [sys.executable, "CTANOut.py"]
    if verbose != verbose_default:              # -v
        call_output.append("-v")
    if statistics != statistics_default:        # -stat
        call_output.append("-stat")
    if btype != btype_default:                  # -b
        call_output.append("-b")
        call_output.append(btype)
    if skip_biblatex != skip_biblatex_default:  # -sb
        call_output.append("-sb")
        call_output.append(skip_biblatex)
    if direc != direc_default:                  # -d
        call_output.append("-d")
        call_output.append(direc)
    if output_name != output_name_default:      # -o
        call_output.append("-o")
        call_output.append(output_name)
    if mode != mode_default:                    # -m
        call_output.append("-m")
        call_output.append(mode)
    if skip != skip_default:                    # -s
        call_output.append("-s")
        call_output.append(skip)
    if make_topics != make_topics_default:      # -mt
        call_output.append("-mt")
    if debugging != debugging_default:          # -dbg
        call_output.append("-dbg")
    if no_files != no_files_default:            # -nf
        call_output.append("-nf")
    
    # process -t | -to | -tl
    w1 = name_template
    w2 = name_load_template
    w3 = name_out_template
    A1 = name_template      != name_template_default
                                                # -t  is given
    A2 = name_load_template != name_load_template_default
                                                # -tl  is given
    A3 = name_out_template  != name_out_template_default
                                                # -to  is given
    if A1:
        if A2 and A3:
            call_output.append("-t"); call_output.append(w3)
                                                # -t
        elif A2 and not A3:
            call_output.append("-t"); call_output.append(w1)
                                                # -t
        elif not A2 and A3:
            call_output.append("-t"); call_output.append(w3)
                                                # -t
        elif not A2 and not A3:
            call_output.append("-t"); call_output.append(w1)
                                                # -t
    else:
        if A2 and A3:
            call_output.append("-t"); call_output.append(w3)
                                                # -t
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-t"); call_output.append(w3)
                                                # -t

    # process -k | -ko | -kl
    w1 = key_template
    w2 = key_load_template
    w3 = key_out_template
    A1 = key_template      != key_template_default
                                                # -k  is given
    A2 = key_load_template != key_load_template_default
                                                # -kl  is given
    A3 = key_out_template  != key_out_template_default
                                                # -ko  is given
    if A1:
        if A2 and A3:
            call_output.append("-k"); call_output.append(w3)
                                                # -k
        elif A2 and not A3:
            call_output.append("-k"); call_output.append(w1)
                                                # -k
        elif not A2 and A3:
            call_output.append("-k"); call_output.append(w3)
                                                # -k
        elif not A2 and not A3:
            call_output.append("-k"); call_output.append(w1)
                                                # -k
    else:
        if A2 and A3:
            call_output.append("-k"); call_output.append(w3)
                                                # -k
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-k"); call_output.append(w3)
                                                # -k

    # process -A a7o -Ao | -Al
    w1 = author_template
    w2 = author_load_template
    w3 = author_out_template
    A1 = author_template      != author_template_default
                                                # -A  is given
    A2 = author_load_template != author_load_template_default
                                                # -Al  is given
    A3 = author_out_template  != author_out_template_default
                                                # -Ao  is given
    if A1:
        if A2 and A3:
            call_output.append("-A"); call_output.append(w3)
                                                # -A
        elif A2 and not A3:
            call_output.append("-A"); call_output.append(w1)
                                                # -A
        elif not A2 and A3:
            call_output.append("-A"); call_output.append(w3)
                                                # -A
        elif not A2 and not A3:
            call_output.append("-A"); call_output.append(w1)
                                                # -A
    else:
        if A2 and A3:
            call_output.append("-A"); call_output.append(w3)
                                                # -A
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-A"); call_output.append(w3)
                                                # -A

    # process -L | -Lo | -Ll
    w1 = license_template
    w2 = license_load_template
    w3 = license_out_template
    A1 = license_template      != license_template_default
                                                # -L  is given
    A2 = license_load_template != license_load_template_default
                                                # -Ll  is given
    A3 = license_out_template  != license_out_template_default
                                                # -Lo  is given
    if A1:
        if A2 and A3:
            call_output.append("-L"); call_output.append(w3)
                                                # -L
        elif A2 and not A3:
            call_output.append("-L"); call_output.append(w1)
                                                # -L
        elif not A2 and A3:
            call_output.append("-L"); call_output.append(w3)
                                                # -L
        elif not A2 and not A3:
            call_output.append("-L"); call_output.append(w1)
                                                # -L
    else:
        if A2 and A3:
            call_output.append("-L"); call_output.append(w3)
                                                # -L
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-L"); call_output.append(w3)
                                                # -L

    # process -y | -yl | -yo
    w1 = year_template
    w2 = year_load_template
    w3 = year_out_template
    A1 = year_template      != year_template_default
                                                # -y  is given
    A2 = year_load_template != year_load_template_default
                                                # -yl  is given
    A3 = year_out_template  != year_out_template_default
                                                # -yo  is given
    if A1:
        if A2 and A3:
            call_output.append("-y"); call_output.append(w3)
                                                # -y
        elif A2 and not A3:
            call_output.append("-y"); call_output.append(w1)
                                                # -y
        elif not A2 and A3:
            call_output.append("-y"); call_output.append(w3)
                                                # -y
        elif not A2 and not A3:
            call_output.append("-y"); call_output.append(w1)
                                                # -y
    else:
        if A2 and A3:
            call_output.append("-y"); call_output.append(w3)
                                                # -y
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-y"); call_output.append(w3)
                                                # -y

    if debugging:
        print("+++ <CTANLoadOut:call_output")   # -dbg

# ------------------------------------------------------------------
# (E, F) call_compile + call_index

if compile:
    if debugging:
        print("+++ >CTANLoadOut:call_compilation")
                                                # -dbg
    direc_comp   = re.sub(r"\\", "/", direc)
    call_compile = [latex_processor, direc_comp + output_name + ".tex"]
    call_index   = index_processor + space + direc_comp + output_name  +\
                   ".idx" + space + "-o " + space + direc_comp +\
                   output_name  + ".ind"

    if debugging:
        print("+++ <CTANLoadOut:call_compilation")
                                                # -dbg

# ------------------------------------------------------------------
# (D) call_regeneration
# constructs the call for regneration
# changes call_regeneration

if regeneration:
    if debugging:
        print("+++ >CTANLoadOut:call_regeneration")
                                                # -dbg
    call_regeneration = [sys.executable, "ctanload.py"]
    if verbose != verbose_default:              # -v
        call_regeneration.append("-v")
    if statistics != statistics_default:        # -stat
        call_regeneration.append("-stat")
    if regenerate != regenerate_default:        # -r
        call_regeneration.append("-r")
    if number != number_default:                # -n
        call_regeneration.append("-n")
        call_regeneration.append(str(number))
    if direc != direc_default:                  # -d
        call_regeneration.append("-d")
        call_regeneration.append(direc)
    if output_name != output_name_default:      # -o
        call_regeneration.append("-o")
        call_regeneration.append(output_name)
    if debugging != debugging_default:          # -dbg
        call_regeneration.append("-dbg")

    if debugging:
        print("+++ <CTANLoadOut:call_regeneration")
                                                # -dbg


#===================================================================
# Auxiliary functions

def fold(s):                                    # function fold: auxiliary
                                                # function: shortens/foldens
                                                # long option lists for output
    """auxiliary function: shortens/foldens long option values for output

    s: string, to be folded"""

    offset = 79 * space
    maxlen = 70
    sep    = "|"
    parts  = s.split(sep)
    line   = empty
    out    = empty
    for f in range(0,len(parts) ):
        if f != len(parts) - 1:
            line = line + parts[f] + sep
        else:
            line = line + parts[f]
        if len(line) >= maxlen:
            out = out +line+ "\n" + offset
            line = empty
    out = out + line
    return out

# ------------------------------------------------------------------
def remove_LaTeX_file(t):                       # auxiliary function
                                                # remove_LaTeX_file:
                                                # removes named LaTeX file.
    """auxiliary function: removes named LaTeX file.

    t: file to be removed"""

    # external methods/functions:
    # path.exists
    # os.remove

    if delete_temporary_file:
        if t in latex_files:
            if path.exists(args.output_name + t):
                os.remove(args.output_name + t)
                if verbose:
                    print("[CTANLoadOut] Warning: LaTeX file",
                          f" '{args.output_name + t}' removed")
            else:
                pass

# ------------------------------------------------------------------
def remove_other_file(t):                       # auxiliary function
                                                # remove_other_file:
                                                # removes named other file
    """auxiliary function: removes named other file.

    parameter:
    t: file to be removed """

    # external methods/functions:
    # path.exists
    # os.remove

    if delete_temporary_file:
        if t in other_files:
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
def func_call_load():                           # function func_call_load():
                                                # CTANLoad is processed.
    """CTANLoad is processed.

    no parameter"""

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check], [...,
    #                   compilation], [..., index], [..., load], [...,
    #                   output], [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True, timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [..., regeneration]:
    #                   stdout is linked to a temporary auxiliary file that is
    #                   processed line by line
    # 1.46   2024-04-16 additional parameter errors="ignore" for
    #                   'with TemporaryFile' in func_call_load, func_call_output
    # 1.47   2024-04-17 addition: [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]: except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault --> timeout etc
    # 1.51   2024-05-94 new section in exception handling: UnicodeDecodeError
    
    # external methods/functions:
    # subprocess.run
    # sys.exit

    print("-" * sepline_length)
    if debugging:
        print("+++ >CTANLoadOut:func_call_load")
                                                # -dbg

    print("[CTANLoadOut, load] Info: CTANLoad (Load)")

    try:
        with TemporaryFile("r+", encoding="utf-8", errors="ignore") as f:
                                                # temporary file
            process_load = subprocess.run(call_load, check=True,
                                          timeout=timeout10, encoding="utf-8",
                                          stdout=f, stderr=subprocess.PIPE,
                                          universal_newlines=True)
            f.seek(0)                           # rewind file
            for line in f.readlines():          # line by line
                print(line, end=empty)
            load_errormessage = process_load.stderr
                                                # possible error message
            if len(load_errormessage) > 0:
                print(load_errormessage)
    except subprocess.CalledProcessError as exc:
                                                # process not found
        if verbose:
            print("[CTANLoadOut, load] Error: called process",
                  f" '{call_load[1]}' not found,", sys.exc_info()[0])
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated    
    except FileNotFoundError as exc:            # file not found
        if verbose:
            print("[CTANLoadOut, load] Error:"
                  f" file '{call_load[0]}' not found", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except subprocess.TimeoutExpired as exc:    # timeout
        if verbose:
            print("[CTANLoadOut, load] Error: timeout error", timeout10)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except KeyboardInterrupt as exc:            # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except UnicodeDecodeError as exc:           # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except:                                     # any unspecified error
        if verbose:
            print("[CTANLoadOut, load] Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    if verbose:
        print("\n" + "[CTANLoadOut, load] Info: CTANLoad (Load) completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_load")
                                                # -dbg

# ------------------------------------------------------------------
def func_call_check():                          # function func_call_check():
                                                # CTANLoad (Check) is processed.
    """CTANLoad (Check) is processed.

    no parameter"""

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True, timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [..., regeneration]:
    #                   stdout is linked to a temporary auxiliary file that
    #                   is processed line by line
    # 1.47   2024-04-17 addition: [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]: except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault --> timeout etc
    # 1.51   2024-05-94 new section in exception handling: UnicodeDecodeError
    
    # external methods/functions:
    # subprocess.run
    # sys.exit

    print("-" * sepline_length)
    if debugging:
        print("+++ >CTANLoadOut:func_call_check")
                                                # -dbg

    print("[CTANLoadOut, check] Info: CTANLoad (Check)")

    try:
        with TemporaryFile("r+", encoding="utf-8") as f:
                                                # temporary file
            process_check  = subprocess.run(call_check, check=True,
                                            timeout=timeout5, stdout=f,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True)
            f.seek(0)                           # rewind file
            for line in f.readlines():          # line by line
                print(line, end=empty)
            check_errormessage = process_check.stderr
                                                # possible error message
            if len(check_errormessage) > 0:
                print(check_errormessage)
    except subprocess.CalledProcessError as exc:
                                                # process not found
        if verbose:
            print("[CTANLoadOut, check] Error: called process",
                  f" '{call_check[1]}' not found,", sys.exc_info()[0])
        sys.exit("[CTANLoadOut, check] Error: program terminated")
                                                # program terminated    
    except FileNotFoundError as exc:            # file not found
        if verbose:
            print("[CTANLoadOut, check] Error:",
                  f" file '{call_check[0]}' not found", exc)
        sys.exit("[CTANLoadOut, check] Error: program terminated")
                                                # program terminated
    except subprocess.TimeoutExpired as exc:    # timeout
        if verbose:
            print("[CTANLoadOut, check] Error: timeout error", timeout5)
        sys.exit("[CTANLoadOut, check] Error: program terminated")
                                                # program terminated
    except KeyboardInterrupt as exc:            # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except UnicodeDecodeError as exc:           # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except:                                     # any unspecified error
        if verbose:
            print("[CTANLoadOut, check] Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, check] Error: program terminated")
                                                # program terminated
    if verbose:
        print("\n" + "[CTANLoadOut, check] Info: CTANLoad (Check) completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_check")
                                                # -dbg

# ------------------------------------------------------------------
def func_call_regeneration():                   # function func_
                                                # call_regeneration(): CTANLoad
                                                # (Regeneration) is processed.
    """CTANLoad (Regeneration) is processed.

    no parameter"""

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True, timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [..., regeneration]:
    #                   stdout is linked to a temporary auxiliary file that
    #                   is processed line by line
    # 1.47   2024-04-17 addition: [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]: except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault --> timeout etc
    # 1.51   2024-05-94 new section in exception handling: UnicodeDecodeError

    # external methods/functions:
    # subprocess.run
    # sys.exit

    if debugging:
        print("+++ >CTANLoadOut:func_call_regneration")
                                                # -dbg
    print("-" * sepline_length)
    print("[CTANLoadOut, regeneration] Info: CTANLoad (Regeneration)")

    try:
        with TemporaryFile("r+", encoding="utf-8") as f:
                                                # temporary file
            process_regeneration = subprocess.run(call_regeneration, check=True,
                                                  timeout=timeout10, stdout=f,
                                                  stderr=subprocess.PIPE,
                                                  universal_newlines=True)
            f.seek(0)                           # rewind file
            for line in f.readlines():          # line by line
                print(line, end=empty)
            regeneration_errormessage = process_regeneration.stderr
                                                # possible error message
            if len(regeneration_errormessage) > 0:
                print(regeneration_errormessage)
    except subprocess.CalledProcessError as exc:
                                                # process not found
        if verbose:
            print("[CTANLoadOut, regeneration] Error: called process" +\
                  f" '{call_regeneration[1]}' not found,",
                  sys.exc_info()[0])
        sys.exit("[CTANLoadOut, regeneration] Error: program terminated")
                                                # program terminated    
    except FileNotFoundError as exc:            # file not found
        if verbose:
            print("[CTANLoadOut, regeneration] Error:",
                  f" file '{call_regeneration[0]}' not found", exc)
        sys.exit("[CTANLoadOut, regeneration] Error: program terminated")
                                                # program terminated
    except subprocess.TimeoutExpired as exc:    # timeout
        if verbose:
            print("[CTANLoadOut, regeneration] Error: timeout error", timeout10)
        sys.exit("[CTANLoadOut, regeneration] Error: program terminated")
                                                # program terminated
    except KeyboardInterrupt as exc:            # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except UnicodeDecodeError as exc:           # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except:                                     # any unspecified error
        if verbose:
            print("[CTANLoadOut, regeneration] Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, regeneration] Error: program terminated")
                                                # program terminated
    if verbose:
        print("\n" + "[CTANLoadOut, regeneration] Info:" +\
              " CTANLoad (Regeneration) completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_regneration")
                                                # -dbg

# ------------------------------------------------------------------
def func_call_output():                         # function func_call_output():
                                                # CTANOut is processed.
    """CTANOut is processed.

    no parameter"""

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True, timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.45.5 2024-04-13 in [..., load], [..., output], [..., regeneration]:
    #                   stdout is linked to a temporary auxiliary file that is
    #                   processed line by line
    # 1.46   2024-04-16 additional parameter errors="ignore" for
    #                   'with TemporaryFile' in func_call_load, func_call_output
    # 1.47   2024-04-17 addition: [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]: except KeyboardInterrupt
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault --> timeout etc
    # 1.51   2024-05-94 new section in exception handling: UnicodeDecodeError
    
    # func_call_output ---> remove_other_file
    # func_call_output ---> remove_LaTeX_file

    # --------------------------------------------
    # external methods/functions:
    # subprocess.run
    # sys.exit

    print("-" * sepline_length)
    if debugging:
        print("+++ >CTANLoadOut:func_call_output")
                                                # -dbg

    print("[CTANLoadOut, output] Info: CTANOut")

    # removes some relevant files
    if mode == "BibLaTeX":
        remove_other_file(".bib")
    elif mode == "LaTeX":
        for e in [".tex", ".tap", ".top", ".xref", ".stat", ".tlp", ".lic"]:
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
        with TemporaryFile("r+", encoding="utf-8", errors="ignore") as f:
                                                # temporary file
            process_out = subprocess.run(call_output, check=True,
                                         timeout=timeout, stdout=f,
                                         universal_newlines=True)
            f.seek(0)                           # rewind file
            for line in f.readlines():          # line by line
                print(line, end=empty)
    except subprocess.CalledProcessError as exc:
                                                # process not found
        if verbose:
            print("[CTANLoadOut, output] Error: called process" +\
                  f" '{call_output[1]}' not found,",
                  sys.exc_info()[0])
        sys.exit("[CTANLoadOut, output] Error: program terminated")
                                                # program terminated    
    except FileNotFoundError as exc:            # file not found
        if verbose:
            print("[CTANLoadOut, output] Error:",
                  f" file '{call_output[0]}' not found", exc)
        sys.exit("[CTANLoadOut, output] Error: program terminated")
                                                # program terminated
    except subprocess.TimeoutExpired as exc:    # timeout
        if verbose:
            print("[CTANLoadOut, output] Error: timeout error", timeout)
        sys.exit("[CTANLoadOut, output] Error: program terminated")
                                                # program terminated
    except KeyboardInterrupt as exc:            # keyboard interrupt
        if verbose:
            print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except UnicodeDecodeError as exc:           # unicode decode error
        if verbose:
            print("[CTANLoadOut, load] Error: unicode decode error", exc)
        sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
    except:                                     # any unspecified error
        if verbose:
            print("[CTANLoadOut, output] Error: any unspecified error",
                  sys.exc_info())
        sys.exit("[CTANLoadOut, output] Error: program terminated")
                                                # program terminated
    if verbose:
        print("\n" + "[CTANLoadOut, output] Info: CTANOut completed")

    if debugging:
        print("+++ <CTANLoadOut:func_call_output")
                                                # -dbg

# ------------------------------------------------------------------
def func_call_compile():                        # Compiles the generated
                                                # LaTeX file
    """Compiles the generated LaTeX file.

    no parameter"""

    # 1.44 2024-04-10 Time measurement for compilations; corresponding statistical output in each case

    # 1.45   2024-04-13 new concept for [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]
    # 1.45.1 2024-04-13 everywhere: subprocess.run instead of subprocess.popen
    # 1.45.2 2024-04-13 everywhere; parameter check=True, timeout=<number>
    # 1.45.3 2024-04-13 global variable timeoutDefault for [CTANLoadOut, check],
    #                   [..., compilation], [..., index], [..., load],
    #                   [..., output], [..., regeneration]
    # 1.45.4 2024-04-13 better, more detailed handling of errors
    # 1.47   2024-04-17 addition: [CTANLoadOut, check], [..., compilation],
    #                   [..., index], [..., load], [..., output],
    #                   [..., regeneration]: except KeyboardInterrupt
    # 1.48   2024-04-22 compiles related subprocesses revised: now more robust
    #                   against coding errors
    # 1.49   2024-04-22 .pdf and .log files removed before step2 and step3 in
    #                   compilation subprocess
    # 1.50.1 2024.04-23 variables renamed: timeoutDefault --> timeout etc
    # 1.51   2024-05-94 new section in exception handling: UnicodeDecodeError

    # func_call_compile ---> remove_LaTeX_file

    # --------------------------------------------
    # external methods/functions:
    # path.exists

    if debugging:
        print("+++ >CTANLoadOut:func_call_compile")
                                                # -dbg    

    print("-" * sepline_length)
    print("[CTANLoadOut, compilation] Info: Compilation")

    file_name       = direc + output_name + ".tex"
    file_name_log   = direc + output_name + ".log"
    file_name_ilg   = direc + output_name + ".ilg"

    if path.exists(file_name):
        if path.getsize(file_name) > 3000:

            # step 1
            for e in [".aux", ".idx", ".ind", ".log", ".ilg", ".pdf", ".out",
                      ".bbl", ".indlualatex"]:
                remove_LaTeX_file(e)

            if verbose:
                print("." * sepline_length)

            print(empty)
            print("[CTANLoadOut, compilation] Info:", latex_processor)
            if verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      call_compile)
                
            startcompiletotal   = time.time()   # sets begin of total time
            startcompileprocess = time.process_time()
                                                # sets begin of process time
          
            try:
                process_compile1      = subprocess.run(call_compile,
                                                       timeout=timeout10,
                                                       check=True,
                                                       capture_output=True)
                compile1_errormessage = process_compile1.stderr.decode("utf-8")
                compile1_message      = process_compile1.stdout.decode("utf-8")
                                                # possible error message
                if len(compile1_errormessage) > 0:
                    if verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              " error in compilation")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoadOut, compilation] Info: more" +\
                              f" information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation] Info: Compilation OK")
            except subprocess.CalledProcessError as exc:
                                                # process not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: called process" +\
                          f" '{call_compile[1]}' not found,",
                          sys.exc_info()[0])
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated    
            except FileNotFoundError as exc:    # file not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: file" +\
                          f" '{call_compile[0]}' not found", exc)
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated
            except subprocess.TimeoutExpired as exc:
                                                # timeout
                if verbose:
                    print("[CTANLoadOut, compilation] Error: timeout error",
                          timeout10)
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated
            except KeyboardInterrupt as exc:    # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except UnicodeDecodeError as exc:   # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load] Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except:                             # any unspecified error
                if verbose:
                    print("[CTANLoadOut, compilation] Error: any" +\
                          " unspecified error",
                          sys.exc_info())
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated

            if statistics:                      # outputs the compilation
                                                # statistics
                pp         = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()
                
                print("\nStatistics (compilation):")
                print("total time (compilation): ".ljust(left + 3),
                      str(round(endcompiletotal-startcompiletotal, 2)).rjust(pp),
                      "s")
                print("process time (compilation): ".ljust(left + 3),
                      str(round(endcompileprocess-startcompileprocess, 2)).\
                      rjust(pp), "s")

# ...................................................................
            # step 2
            if verbose:
                print("." * sepline_length)
            for e in [".log", ".pdf"]:
                remove_LaTeX_file(e)

            if verbose:
                print("." * sepline_length)
                
            print("[CTANLoadOut, compilation] Info:", latex_processor)
            if verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      call_compile)

            startcompiletotal   = time.time()   # sets begin of total time
            startcompileprocess = time.process_time()
                                                # sets begin of process time
          
            try:
                process_compile2      = subprocess.run(call_compile,
                                                       timeout=timeout10,
                                                       check=True,
                                                       capture_output=True)
                compile2_errormessage = process_compile2.stderr.decode("utf-8")
                compile2_message      = process_compile2.stdout.decode("utf-8")
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
                        print("[CTANLoadOut, compilation] Info: Compilation OK")
            except subprocess.CalledProcessError as exc:
                                                # process not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: called process",
                          f"'{call_compile[1]}' not found,",
                          sys.exc_info()[0])
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated    
            except FileNotFoundError as exc:    # file not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: file",
                          f"'{call_compile[0]}' not found", exc)
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated
            except subprocess.TimeoutExpired as exc:
                                                # timeout
                if verbose:
                    print("[CTANLoadOut, compilation] Error: timeout error",
                          timeout10)
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated
            except KeyboardInterrupt as exc:    # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except UnicodeDecodeError as exc:   # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load] Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except:                             # any unspecified error
                if verbose:
                    print("[CTANLoadOut, compilation] Error:",
                          "any unspecified error",
                          sys.exc_info())
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated

            if statistics:                      # outputs the compilation
                                                # statistics
                pp         = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()
                
                print("\nStatistics (compilation):")
                print("total time (compilation): ".ljust(left + 3),
                      str(round(endcompiletotal-startcompiletotal, 2)).rjust(pp),
                      "s")
                print("process time (compilation): ".ljust(left + 3),
                      str(round(endcompileprocess-startcompileprocess, 2)).\
                      rjust(pp), "s")

# ...................................................................
            # step 3
            if verbose:
                print("." * sepline_length)
            print("[CTANLoadOut, index] Info:", index_processor)
            if verbose:
                print("[CTANLoadOut, index] Info: Program call:", call_index)

            startcompiletotal   = time.time()   # sets begin of total time
            startcompileprocess = time.process_time()
                                                # sets begin of process time
          
            try:
                process_index      = subprocess.run(call_index, timeout=timeout,
                                                    check=True,
                                                    capture_output=True,
                                                    universal_newlines=True)
                index_errormessage = process_index.stderr
                                                # possible error message
                index_message      = process_index.stdout
            except subprocess.CalledProcessError as exc:
                                                # process not found
                if verbose:
                    print("[CTANLoadOut, index] Error: called process",
                          f"'{call_index[1]}' not found,", sys.exc_info()[0])
                sys.exit("[CTANLoadOut, index] Error: program terminated")
                                                # program terminated    
            except FileNotFoundError as exc:    # file not found
                if verbose:
                    print("[CTANLoadOut, index] Error: file",
                          f"'{call_index[0]}' not found", exc)
                sys.exit("[CTANLoadOut, index] Error: program terminated")
                                                # program terminated
            except subprocess.TimeoutExpired as exc:
                                                # timeout
                if verbose:
                    print("[CTANLoadOut, index] Error: timeout error", timeout)
                sys.exit("[CTANLoadOut, index] Error: program terminated")
                                                # program terminated
            except KeyboardInterrupt as exc:    # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except UnicodeDecodeError as exc:   # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load] Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except:                             # any unspecified error
                if verbose:
                    print("[CTANLoadOut, index] Error: any unspecified error",
                          sys.exc_info())
                sys.exit("[CTANLoadOut, index] Error: program terminated")
                                                # program terminated
                
            if verbose:
                print("[CTANLoadOut, index] Info: more information",
                      f"in '{file_name_ilg}'")
                print("[CTANLoadOut, index] Info: Makeindex OK")
                
            if statistics:                      # outputs the compilation
                                                # statistics
                pp         = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()
                
                print("\nStatistics (index generation):")
                print("total time (index generation): ".ljust(left + 3),
                      str(round(endcompiletotal-startcompiletotal, 2)).rjust(pp),
                      "s")
                print("process time (index generation): ".ljust(left + 3),
                      str(round(endcompileprocess-startcompileprocess, 2)).\
                      rjust(pp), "s")

# ...................................................................
            # step 4
            if verbose:
                print("." * sepline_length)
            for e in [".log", ".pdf"]:
                remove_LaTeX_file(e)

            if verbose:
                print("." * sepline_length)
            print("[CTANLoadOut, compilation] Info:", latex_processor)
            if verbose:
                print("[CTANLoadOut, compilation] Info: Program call:",
                      call_compile)

            startcompiletotal   = time.time()   # sets begin of total time
            startcompileprocess = time.process_time()
                                                # sets begin of process time
          
            try:
                process_compile3      = subprocess.run(call_compile,
                                                       timeout=timeout10,
                                                       check=True,
                                                       capture_output=True)
                compile3_errormessage = process_compile3.stderr.decode("utf-8")
                compile3_message      = process_compile3.stdout.decode("utf-8")
                                                # possible error message
                if len(compile3_errormessage) > 0:
                    if verbose:
                        print("[CTANLoadOut, compilation] Error:",
                              "error in compilation")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoadOut, compilation] Info: more",
                              f"information in '{file_name_log}'")
                        print("[CTANLoadOut, compilation] Info: result in '" +\
                              direc + output_name + ".pdf'")
                        print("[CTANLoadOut, compilation] Info: Compilation OK")
            except subprocess.CalledProcessError as exc:
                                                # process not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: called process",
                          f"'{call_compile[1]}' not found,",
                          sys.exc_info()[0])
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated    
            except FileNotFoundError as exc:    # file not found
                if verbose:
                    print("[CTANLoadOut, compilation] Error: file"
                          f"'{call_compile[0]}' not found", exc)
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated
            except subprocess.TimeoutExpired as exc:
                                                # timeout
                if verbose:
                    print("[CTANLoadOut, compilation] Error: timeout error",
                          timeout10)
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated
            except KeyboardInterrupt as exc:    # keyboard interrupt
                if verbose:
                    print("[CTANLoadOut, load] Error: keyboard interrupt", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except UnicodeDecodeError as exc:   # unicode decode error
                if verbose:
                    print("[CTANLoadOut, load] Error: unicode decode error", exc)
                sys.exit("[CTANLoadOut, load] Error: program terminated")
                                                # program terminated
            except:                             # any unspecified error
                if verbose:
                    print("[CTANLoadOut, compilation] Error:",
                          "any unspecified error",
                          sys.exc_info())
                sys.exit("[CTANLoadOut, compilation] Error: program terminated")
                                                # program terminated

            if statistics:                      # outputs the compilation
                                                # statistics
                pp         = 5
                endcompiletotal   = time.time()
                endcompileprocess = time.process_time()
                
                print("\nStatistics (compilation):")
                print("total time (compilation): ".ljust(left + 3),
                      str(round(endcompiletotal-startcompiletotal, 2)).rjust(pp),
                      "s")
                print("process time (compilation): ".ljust(left + 3),
                      str(round(endcompileprocess-startcompileprocess, 2)).\
                      rjust(pp), "s")
        else:
            if verbose: print("[CTANLoadOut, compilation] Warning: LaTeX file",
                              f"'{file_name}' without content, no compilation")
    else:
        if verbose: print("[CTANLoadOut, compilation] Warning: LaTeX file",
                          f"'{file_name}' does not exist, no compilation")

# ...................................................................
    if verbose:
        print("." * sepline_length)
    # remove some LaTeX files
    for e in [".aux", ".idx", ".ind", ".out", ".bbl", ".indlualatex"]:
        remove_LaTeX_file(e)

    if debugging:
        print("+++ <CTANLoadOut:func_call_compile")
                                                # -dbg    

# ------------------------------------------------------------------
def head():                                     # function head: shows the
                                                # called options
    """Shows the given options.

    no parameter"""

    # head ---> fold

    if debugging:
        print("+++ >CTANLoadOut:head")          # -dbg

    call[0] = "CTANLoadOut.py"
    print("[CTANLoadOut] Info: CTANLoadOut")
    if verbose:
        
        print(empty)
        print("[CTANLoadOut] Info: Program call:", call)
        if ("-c" in call) or ("--check_integrity" in call):
            print("  {0:5} {1:70}".format("-c", "(" + integrity_text + ")"))
                                                # -c (Flag)
        if ("-f" in call) or ("--download_files" in call):
            print("  {0:5} {1:70}".format("-f", "(" + download_text + ")"))
                                                # -f (Flag)
        if ("-l" in call) or ("--lists" in call):
            print("  {0:5} {1:70}".format("-l", "(" + \
                                          (lists_text + ")")[0:65] + ellipse))
                                                # -l (Flag)
        if ("-mo" in call) or ("--make_output" in call):
            print("  {0:5} {1:70}".format("-mo", "(" + (make_output_text + \
                                                        ")")[0:65] + ellipse))
                                                # -mo (Flag)
        if ("-mt" in call) or ("--make_topics" in call):
            print("  {0:5} {1:70}".format("-mt", "(" + (topics_text + \
                                                        ")")[0:65] + ellipse))
                                                # -mt (Flag)
        if ("-nf" in call) or ("--no_files" in call):
            print("  {0:5} {1:70}".format("-nf", "(" + (no_files_text + \
                                                        ")")[0:65] + ellipse))
                                                # -nf (Flag)
        if ("-p" in call) or ("--pdf_output" in call):
            print("  {0:5} {1:70}".format("-p", "(" + pdf_output_text + ")"))
                                                # -p (Flag)
        if ("-r" in call) or ("--regenerate_pickle_files" in call):
            print("  {0:5} {1:70}".format("-r", "(" + regenerate_text + ")"))
                                                # -r (Flag)
        if ("-stat" in call) or ("--statistics" in call):
            print("  {0:5} {1:70}".format("-stat", "(" + statistics_text + ")"))
                                                # -stat (Flag)
        if ("-v" in call) or ("--verbose" in call):
            print("  {0:5} {1:70}".format("-v", "(" + verbose_text + ")"))
                                                # -v (Flag)

        if ("-b" in call) or ("--btype" in call):
            print("  {0:5} {2:70} {1}".format("-b", btype,
                                              "(" + btype_text + ")"))
                                                # -b
        if ("-d" in call) or ("--directory" in call):
            print("  {0:5} {2:70} {1}".format("-d", direc,
                                              "(" + direc_text + ")"))
                                                # -d
        if ("-m" in call) or ("--mode" in call):
            print("  {0:5} {2:70} {1}".format("-m", mode, "(" + mode_text + ")"))
                                                # -m
        if ("-n" in call) or ("--number" in call):
            print("  {0:5} {2:70} {1}".format("-n", number,
                                              "(" + number_text + ")"))
                                                # -n
        if ("-o" in call) or ("--output" in call):
            print("  {0:5} {2:70} {1}".format("-o", args.output_name,
                                              "(" + output_text + ")"))
                                                # -o
        if ("-s" in call) or ("--skip" in call):
            print("  {0:5} {2:70} {1}".format("-s", skip, "(" + skip_text + ")"))
                                                # -s
        if ("-sb" in call) or ("--skip_biblatex" in call):
            print("  {0:5} {2:70} {1}".format("-sb", skip_biblatex,
                                              "(" + skip_biblatex_text + ")"))
                                                # -sb
        if ("-tout" in call) or ("--timeout" in call):
            print("  {0:5} {2:70} {1}".format("-tout", timeout,
                                              "(" + timeout_text + ")"))
                                                # -tout

        if ("-k" in call) or ("--key_template" in call):
            print("  {0:5} {2:70} {1}".format("-k", fold(key_template),
                                              "(" + (key_template_text + \
                                                     ")")[0:65] + ellipse))
                                                # -k (keys)
        if ("-kl" in call) or ("--key_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-kl", fold(key_load_template),
                                              "(" + (key_load_template_text + \
                                                     ")")[0:65] + ellipse))
                                                # -kl (keys)
        if ("-ko" in call) or ("--key_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-ko", fold(key_out_template),
                                              "(" + (key_out_template_text + \
                                                     ")")[0:65] + ellipse))
                                                # -ko (keys)

        if ("-t" in call) or ("--name_template" in call):
            print("  {0:5} {2:70} {1}".format("-t", fold(name_template),
                                              "(" + name_template_text + ")"))
                                                # -t (names)
        if ("-tl" in call) or ("--name_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-tl", fold(name_load_template),
                                              "(" + name_load_template_text + \
                                              ")"))
                                                # -tl (names)
        if ("-to" in call) or ("--name_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-to", fold(name_out_template),
                                              "(" + name_out_template_text + \
                                              ")"))
                                                # -to (names)

        if ("-A" in call) or ("--author_template" in call):
            print("  {0:5} {2:70} {1}".format("-A", fold(author_template),
                                              "(" + author_template_text + ")"))
                                                # -A (authors)
        if ("-Al" in call) or ("--author_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-Al", fold(author_load_template),
                                              "(" + author_load_template_text + \
                                              ")"))
                                                # -Al (authors)
        if ("-Ao" in call) or ("--author_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-Ao", fold(author_out_template),
                                              "(" + author_out_template_text + \
                                              ")"))
                                                # -Ao (authors)

        if ("-L" in call) or ("--license_template" in call):
            print("  {0:5} {2:70} {1}".format("-L", fold(license_template),
                                              "(" + license_template_text + ")"))
                                                # -L (licenses)
        if ("-Ll" in call) or ("--license_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-Ll", fold(license_load_template),
                                              "(" + license_load_template_text +\
                                              ")"))
                                                # -Ll (licenses)
        if ("-Lo" in call) or ("--license_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-Lo", fold(license_out_template),
                                              "(" + license_out_template_text + \
                                              ")"))
                                                # -Lo (licenses)

        if ("-y" in call) or ("--year_template" in call):
            print("  {0:5} {2:70} {1}".format("-y", fold(year_template),
                                              "(" + year_template_text + ")"))
                                                # -y (years)
        if ("-yl" in call) or ("--year_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-yl", fold(year_load_template),
                                              "(" + year_load_template_text + \
                                              ")"))
                                                # -yl (years)
        if ("-yo" in call) or ("--year_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-yo", fold(year_out_template),
                                              "(" + year_out_template_text + \
                                              ")"))
                                                # -yo (years)

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
        print("+++ <CTANLoadOut:head")          # -dbg

# ------------------------------------------------------------------
def main():                                     # main function
    """Main Function

    no parameter"""

    # main ---> head
    # main ---> func_call_regeneration
    # main ---> func_call_load
    # main ---> func_call_check
    # main ---> func_call_output
    # main ---> func_call_compile

    if debugging:
        print("+++ >CTANLoadOut:main")          # -dbg

    file_name = direc + output_name + ".tex"

    if verbose:
        print("=" * sepline_length, "\n")
    head()

    if regeneration:                            # -r has been set
        func_call_regeneration()
    if load:                                    # CTANLoad is to be called
        func_call_load()
    if check:                                   # -l | -c has been set
        func_call_check()
    if output:                                  # CTANOut is to be called
        func_call_output()
    if compile:                                 # the LaTeX processor will
                                                # produce a PDF file
        func_call_compile()
    print("-" * sepline_length)

    if statistics:                              # outputs the statistics
        pp         = 5
        endtotal   = time.time()
        endprocess = time.process_time()
        
        print("\nStatistics (CTANLoadOut):")
        print("date | time:".ljust(left + 3), actDate, "|", actTime)
        print("program | version | date:".ljust(left + 3), programname_ext, "|",
              programversion, "|", programdate)

        print("---")
        print("total time (CTANLoadOut): ".ljust(left + 3),
              str(round(endtotal-starttotal, 2)).rjust(pp), "s")
        print("process time (CTANLoadOut): ".ljust(left + 3),
              str(round(endprocess-startprocess, 2)).rjust(pp), "s")
           
    if debugging:
        print("+++ <CTANLoadOut:main")          # -dbg

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
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
except:
    pass

starttotal   = time.time()                  # sets begin of total time
startprocess = time.process_time()          # sets begin of process time

main()                                      # main part called
if verbose:
    print("\n" + "[CTANLoadOut] Info: CTANLoadOut completed")


#===================================================================

# Problems/Plans:
# + prüfen, ob ctanload -l -c aufgerufen werden muss (wenn CTANOut folgt)
# + ist -c gefährlich?
# + Index verweist auf Seitenummern; all.xref und all.tap auf Abschnittsnummer
# + Programmabbruch bei -ko graphics oder -ko class (x)
# + Fehler bei LaTeX-Ausgabe: UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 262476: character maps to <undefined> (?)
# + alle Textdateien überprüfen bzw. neu machen (x)
# + korrigiert: induziertes -l wird nicht weitergegeben (x)
# + erneuern: Change-Liste, Manpage
# + Programmabbruch bei Suchanfragen mit Umlauten, Eszet, diakritischen Buchstaben
# + zusätzliche Fehler-Abfrage? KeyboardInterrupt, UnicodeDecodeError in ...
# + neuer Parameter für timeout (x)
# + Text für -mo geändert (x)
# + argparse überarbeitet (x)
# + argparse-Gruppen (x)
# + Text pdf_output_text geändert
# + argparse mit usage probieren: usage='%(prog)s [options]'
# + initialer Test, ob CTAN verfügbar

# ------------------------------------------------------------------
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
# 1.40 2023-07-30 year_template_default adjusted to year_template_default in CTANLoad and CTANOut
# 1.41 2023-07-30 minor changes in message texts: to be executed --> is to be processed
# 1.42 2023-07-30 output of programname_ext / programversion / programdate when -stat is set
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
# 1.50.2 2024-04-23 new global variables: timeout_default and timeout_text
# 1.50.3 2024-04-23 new section in arparse processing: new options -tout and --timeout + corr. assigmnent to timeout

# 1.51   2024-05-94 new section in exception handling: UnicodeDecodeError
# 1.52   2024-06-02 btype_default changed to "@online"
# 1.53   2024-06-11 additional values for -m: tsv, csv
# 1.54   2024-06-12 some texts for -h and arparse changed

# 1.55   2024-07-20 argparse revised
# 1.55.1 2024-07-20 additional parameter in .ArgumentParser: prog, epilog, formatter_class
# 1.55.2 2024-07-20 subdivision into groups by .add_argument_group
# 1.55.3 2024-07-20 additional arguments in .add_argument (if it makes sense): type, metavar, action, dest

# 1.56   2025-02-09 everywhere: all source code lines wrapped at a maximum of 80 characters
# 1.57   2025-02-12 no test: __name__ == "__main__; ==> CTANLoad.py can be imported 
