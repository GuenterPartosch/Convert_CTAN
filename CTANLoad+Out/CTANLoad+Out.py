#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANLoad+Out.py
# (C) Günter Partosch, 2021/2022/2023

# see also CTANLoad+Out-changes.txt
#          CTANLoad+Out-messages.txt
#          CTANLoad+Out.man
#          CTANLoad+Out-examples.txt
#          CTANLoad+Out-modules.txt
#          CTAN-files.txt


#===================================================================
# Moduls needed

import argparse                    # argument parsing
import sys                         # system calls
import platform                    # get OS informations
import subprocess                  # handling of sub-processes
import re                          # regular expression
import os                          # delete a file on disk, for instance
from os import path                # path informations
import codecs                      # needed for full UTF-8 output on stdout
import time                        # get time/date of a file


#===================================================================
# Settings

programname       = "CTANLoad+Out.py"
programversion    = "1.39"
programdate       = "2023-07-01"
programauthor     = "Günter Partosch"
authoremail       = "Guenter.Partosch@hrz.uni-giessen.de"
authorinstitution = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"

operatingsys      = platform.system()
call              = sys.argv                 # get call and its options
actDate           = time.strftime("%Y-%m-%d")# actual date of program execution
actTime           = time.strftime("%X")      # actual time of program execution
empty_set         = set()
latex_processor   = "lualatex"               # default LaTeX processor
index_processor   = "makeindex"              # default index processor

empty             = ""
space             = " "
ellipse           = " ..."

left              = 35                       # width of labels in verbose output
sepline_length    = 80                       # length of separation line in output

call_check        = empty                    # initialization
call_load         = empty                    # initialization
call_output       = empty                    # initialization
call_compile      = empty                    # initialization
call_index        = empty                    # initialization

delete_temporary_file  = True

err_mode          = "[CTANLoad+Out] Warning: '{0} {1}' changed to '{2} (due to {3})'"
latex_files       = [".aux", ".bib", ".ilg", ".log", ".idx", ".ilg", ".ind", ".out", ".tex", ".pdf", ".stat", ".tap", ".top", ".xref"]
other_files       = [".ris", ".bib", ".txt", ".tsv"]

# ------------------------------------------------------------------
# Texts for argument parsing and help

author_load_template_text = "[CTANLoad} Name template for authors"                    # option -Al
author_out_template_text  = "[CTANOut} Name template for authors"                     # option -Ao
author_template_text      = "[CTANLoad and CTANOut] Name template for authors"        # option -A

license_load_template_text= "[CTANLoad] Name template for licenses"                   # option -Ll
license_out_template_text = "[CTANOut] Name template for licenses"                    # option -Lo
license_template_text     = "[CTANLoad and CTANOut] Name template for licenses"       # option -L

key_load_template_text    = "[CTANLoad] Template for keys"                            # option -kl
key_out_template_text     = "[CTANOut] Template for keys"                             # option -ko
key_template_text         = "[CTANLoad and CTANOut] Template for keys"                # option -k

name_load_template_text   = "[CTANLoad] Template for package names"                   # option -tl
name_out_template_text    = "[CTANOut] Template for package names"                    # option -to
name_template_text        = "[CTANLoad and CTANOut] Template for package names"       # option -t

year_template_text        = "[CTANLoad and CTANOut] Template for years"               # option -y
year_load_template_text   = "[CTANLoad] Template for years"                           # option -yl
year_out_template_text    = "[CTANOut] Template for years"                            # option -yo

author_text               = "Flag: Shows author of the program and exits."            # option -a
download_text             = "Flag: Downloads associated documentation files [PDF]."   # option -f
integrity_text            = "Flag: Checks the integrity of the 2nd .pkl file."        # option -c
lists_text                = "Flag: Generates some special lists and prepare files for CTANOut."
                                                                                      # option -l
make_output_text          = "Flag: Generates only output [RIS, LaTeX, BibLaTeX, Excel, plain] via CTANOut."
                                                                                      # option -mo
no_files_text             = "Flag: Do not generate output files."                     # option -nf
pdf_output_text           = "Flag: Generates PDF output."                             # option -p

regenerate_text           = "Flag: Regenerates the two pickle files."                 # option -r
statistics_text           = "Flag: Prints statistics on terminal."                    # option -stat
topics_text               = "Flag: Generates topic lists [meaning of topics + cross-reference (topics/packages, authors/packages); only for -m LaTeX])."
                                                                                      # option -mt
verbose_text              = "Flag: Output is verbose."                                # option -v
version_text              = "Flag: Shows version of the program and exits."           # option -V

btype_text                = "Type of BibLaTex entries to be generated [valid only for '-m BibLaTeX'/'--mode BibLaTeX']"
                                                                                      # option -b
direc_text                = "OS Directory for input and output files"                 # option -d
mode_text                 = "Target format"                                           # option -m
number_text               = "Maximum number of file downloads"                        # option -n
output_text               = "Generic name for output files [without extensions]"      # option -o
skip_text                 = "Skips specified CTAN fields."                            # option -s
skip_biblatex_text        = "Skips specified BibLaTeX fields."                        # option -sb
program_text              = "Combines the tasks of CTANLoad [Load XLM and PDF documentation files from CTAN a/o generates some special lists, and prepares data for CTANOut] and CTANOut [Convert CTAN XLM package files to some formats]."

# ------------------------------------------------------------------
# Defaults/variables for argparse

author_template_default      = """^.+$"""                  # default for author name template (-A)
author_load_template_default = empty                       # default for author load name template (-Al)
author_out_template_default  = author_template_default     # default for author out name template (-Ao)

license_template_default     = """^.+$"""                  # default for license name template (-L)
license_load_template_default= empty                       # default for license load name template (-Ll)
license_out_template_default = license_template_default    # default for license out name template (-Lo)

key_template_default         = """^.+$"""                  # default for option -k
key_load_template_default    = empty                       # default for option -kl
key_out_template_default     = key_template_default        # default for option -ko

name_template_default        = """^.+$"""                  # default for option -t
name_load_template_default   = empty                       # default for option -tl
name_out_template_default    = name_template_default       # default for option -to

year_template_default        = """^19[89][0-9]|20[012][0-9]$"""
                                                           # default for year template (-y) [four digits]
year_load_template_default   = empty                       # default for year_load_template (-yl) [four digits]
year_out_template_default    = year_load_template_default  # default for year_out_template (-yo) [four digits]

btype_default                = empty                       # default for option -b (BibLaTeX entry type)
mode_default                 = "RIS"                       # default for option -m
number_default               = 250                         # default for option -n (maximum number of files to be loaded)
output_name_default          = "all"                       # default for option -o (generic file name)
skip_default                 = "[]"                        # default for option -s
skip_biblatex_default        = "[]"                        # default for option -sb

download_default             = False                       # flag: download PDF files      (option -f)
integrity_default            = False                       # flag: integrity check         (option -c)
lists_default                = False                       # flag: generate special lists  (option -l)
make_output_default          = False                       # Flag: generate only output (RIS, LaTeX, BibLaTeX, Excel, plain)
make_topics_default          = False                       # flag: make topics output      (option -mt)
no_files_default             = False                       # flag: no output files         (option -nf)
pdf_output_default           = False                       # flag: produce PDF output      (option -p)
regenerate_default           = False                       # flag: regenerate pickle files (option -r)
statistics_default           = False                       # flag: output statistics       (option -stat)
verbose_default              = False                       # flag: output is verbose       (option -v)
debugging_default            = False                       # flag: debugging               (option -dbg)

act_direc                    = "."                         # actual directory

if operatingsys == "Windows":
    direc_sep      = "\\"
else:
    direc_sep      = "/"

direc_default                = act_direc + direc_sep       # default for -d (OS output directory)


#===================================================================
# Parsing the arguments

parser = argparse.ArgumentParser(description = "[" + programname + "; " + "Version: " + programversion + " (" + programdate + ")] " + program_text)
parser._optionals.title   = 'Optional parameters'

parser.add_argument("-a", "--author",                      # option -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = programauthor + " (" + authoremail + ", " + authorinstitution + ")")

parser.add_argument("-A", "--author_template",             # option -A/--author_template
                    help    = author_template_text + " - Default: " + "%(default)s",
                    dest    = "author_template",
                    default = author_template_default)

parser.add_argument("-Al", "--author_load_template",       # option -Al/--author_load_template
                    help    = author_load_template_text + " - Default: " + "%(default)s",
                    dest    = "author_load_template",
                    default = author_load_template_default)

parser.add_argument("-Ao", "--author_out_template",        # option -Ao/--author_out_template
                    help    = author_out_template_text + " - Default: " + "%(default)s",
                    dest    = "author_out_template",
                    default = author_out_template_default)

parser.add_argument("-L", "--license_template",            # option -L/--license_template
                    help    = license_template_text + " - Default: " + "%(default)s",
                    dest    = "license_template",
                    default = license_template_default)

parser.add_argument("-Ll", "--license_load_template",      # option -Ll/--license_load_template
                    help    = license_load_template_text + " - Default: " + "%(default)s",
                    dest    = "license_load_template",
                    default = license_load_template_default)

parser.add_argument("-Lo", "--license_out_template",       # option -Lo/--license_out_template
                    help    = license_out_template_text + " - Default: " + "%(default)s",
                    dest    = "license_out_template",
                    default = license_out_template_default)

parser.add_argument("-b", "--btype",                       # option -b/--btype
                    help    = btype_text + " - Default: " + "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan", "@www"],
                    dest    = "btype",
                    default = btype_default)

parser.add_argument("-c", "--check_integrity",             # option -i/--integrity
                    help    = integrity_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = integrity_default)

parser.add_argument("-d", "--directory",                   # option -d/--directory
                    help    = direc_text + " - Default: " + "%(default)s",
                    dest    = "direc",
                    default = direc_default)

parser.add_argument("-f", "--download_files",              # option -f/--download_files
                    help    = download_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = download_default)

parser.add_argument("-k", "--key_template",                # option -k/--key_template
                    help    = key_template_text + " - Default: " + "%(default)s",
                    dest    = "key_template",
                    default = key_template_default)

parser.add_argument("-kl", "--key_load_template",          # option -kl/--key_load_template
                    help    = key_load_template_text + " - Default: " + "%(default)s",
                    dest    = "key_load_template",
                    default = key_load_template_default)

parser.add_argument("-ko", "--key_out_template",           # option -ko/--key_out_template
                    help    = key_out_template_text + " - Default: " + "%(default)s",
                    dest    = "key_out_template",
                    default = key_out_template_default)

parser.add_argument("-l", "--lists",                       # option -l/--lists
                    help = lists_text + " - Default: " + "%(default)s",
                    action = "store_true",
                    default = lists_default)

parser.add_argument("-m", "--mode",                        # option -m/--mode
                    help    = mode_text + " - Default: " + "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "ris", "plain", "txt", "BibLaTeX", "biblatex", "bib", "Excel", "excel"],
                    dest    = "mode",
                    default = mode_default)

parser.add_argument("-mo", "--make_output",                # option -mo/--make_output
                    help    = make_output_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_output_default)

parser.add_argument("-mt", "--make_topics",                # option -mt/--make_topics
                    help    = topics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_topics_default)

parser.add_argument("-n", "--number",                      # option -n/--number
                    help    = number_text + " - Default: " + "%(default)s",
                    dest    = "number",
                    default = number_default)

parser.add_argument("-nf", "--no_files",                   # option -nf/--no_files
                    help    = no_files_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = no_files_default)

parser.add_argument("-o", "--output",                      # option -o/--output
                    help    = output_text + " - Default: " + "%(default)s",
                    dest    = "output_name",
                    default = output_name_default)

parser.add_argument("-p", "--pdf_output",                  # option -p/--pdf_output
                    help    = pdf_output_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = pdf_output_default)

parser.add_argument("-r", "--regenerate_pickle_files",     # option -r/--regenerate_pickle_files
                    help    = regenerate_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = regenerate_default)

parser.add_argument("-s", "--skip",                        # option -s/--skip
                    help    = skip_text + " - Default: " + "%(default)s",
                    dest    = "skip",
                    default = skip_default)

parser.add_argument("-sb", "--skip_biblatex",              # option -sb/--skip_biblatex
                    help    = skip_biblatex_text + " - Default: " + "%(default)s",
                    dest    = "skip_biblatex",
                    default = skip_biblatex_default)

parser.add_argument("-stat", "--statistics",               # option -stat/--statistics
                    help    = statistics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics_default)

parser.add_argument("-t", "--name_template",               # option -t/--template
                    help    = name_template_text + " - Default: " + "%(default)s",
                    dest    = "name_template",
                    default = name_template_default)

parser.add_argument("-tl", "--name_load_template",         # option -tl/--template_load
                    help    = name_load_template_text + " - Default: " + "%(default)s",
                    dest    = "name_load_template",
                    default = name_load_template_default)

parser.add_argument("-to", "--name_out_template",          # option -to/--template_out
                    help    = name_out_template_text + " - Default: " + "%(default)s",
                    dest    = "name_out_template",
                    default = name_out_template_default)

parser.add_argument("-V", "--version",                     # option -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + programversion + " (" + programdate + ")")

parser.add_argument("-v", "--verbose",                     # option -v/--verbose
                    help = verbose_text + " - Default: " + "%(default)s",
                    action = "store_true",
                    default = verbose_default)

parser.add_argument("-y", "--year_template",               # option -y/--year_template
                    help    = year_template_text + " - Default: " + "%(default)s",
                    dest    = "year_template",
                    default = year_template_default)

parser.add_argument("-yl", "--year_load_template",         # option -yl/--year_load_template
                    help    = year_load_template_text + " - Default: " + "%(default)s",
                    dest    = "year_load_template",
                    default = year_load_template_default)

parser.add_argument("-yo", "--year_out_template",          # option -yo/--year_out_template
                    help    = year_out_template_text + " - Default: " + "%(default)s",
                    dest    = "year_out_template",
                    default = year_out_template_default)

parser.add_argument("-dbg", "--debugging",                 # option -dbg/--debugging
                    help    = argparse.SUPPRESS,           # will be suppressed in help
                    action  = "store_true",
                    default = debugging_default)

# ------------------------------------------------------------------
# Getting parsed options

args                  = parser.parse_args()
   
author_template       = args.author_template        # option -A
author_load_template  = args.author_load_template   # option -Al
author_out_template   = args.author_out_template    # option -Ao

license_template      = args.license_template       # option -L
license_load_template = args.license_load_template  # option -Ll
license_out_template  = args.license_out_template   # option -Lo

name_template         = args.name_template          # option -t
name_load_template    = args.name_load_template     # option -tl
name_out_template     = args.name_out_template      # option -to

key_template          = args.key_template           # option -k
key_out_template      = args.key_out_template       # option -ko
key_load_template     = args.key_load_template      # option -kl

year_template         = args.year_template          # option -y
year_load_template    = args.year_load_template     # option -yl
year_out_template     = args.year_out_template      # option -yo

btype                 = args.btype                  # option -b
direc                 = args.direc                  # option -d
download              = args.download_files         # option -f

integrity             = args.check_integrity        # option -c
lists                 = args.lists                  # option -l
make_output           = args.make_output            # option -mo
make_topics           = args.make_topics            # option -mt
mode                  = args.mode                   # option -m
number                = int(args.number)            # option -n
no_files              = args.no_files               # option -nf
output_name           = args.output_name            # option -o
pdf_output            = args.pdf_output             # option -p
regenerate            = args.regenerate_pickle_files# option -r
skip                  = args.skip                   # option -s
skip_biblatex         = args.skip_biblatex          # option -sb
statistics            = args.statistics             # option -stat

verbose               = args.verbose                # option -v
debugging             = args.debugging              # option -dbg

# ------------------------------------------------------------------
# Correct direc

direc = direc.strip()                               # correct/expand OS directory name (-d)
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

# -y     x     -     x      -
# -yo    -     -     x      -
# -yl    x     -     -      -

# -v     x     x     x      -
# -V     x     x     x      -

# ------------------------------------------------------------------
# unify modes
if mode in ["LaTeX", "latex", "tex"]:                          # LaTeX, latex, tex --> LaTeX
    mode = "LaTeX"
elif mode in ["BibLaTeX", "biolatex", "bib"]:                  # BibLaTeX, biblatex, bib --> BibLaTeX
    mode = "BibLaTeX"
elif mode in ["Excel", "excel", "tsv"]:                        # Excel, excel, tsv --> Excel
    mode = "Excel"
elif mode in ["RIS", "ris"]:                                   # RIS, ris --> RIS
    mode = "RIS"
elif mode in ["plain", "txt"]:                                 # plain, txt --> plain
    mode = "plain"
else:
    pass

# ------------------------------------------------------------------
# reset modes
print(empty)
if (make_topics != make_topics_default):                       # reset -m to LaTeX, if -mt is set
    if mode != "LaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m LaTeX', '-mt'))
        call.append("-m")
        call.append("LaTeX")
        mode = "LaTeX"
if (pdf_output != pdf_output_default):                         # reset -m to LaTeX, if -p is set
    if mode != "LaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m LaTeX', '-p'))
            print(err_mode.format('-mt =', make_topics, True, '-p'))
        call.append("-m")
        call.append("LaTeX")
        call.append("-mt")
        make_topics = True
        mode        = "LaTeX"
if (btype != btype_default):                                   # reset -m to BibLaTeX, if -b is set
    if mode != "BibLaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m BibLaTeX', "'-b'"))
        call.append("-m");
        call.append("BibLaTeX")
        mode = "BibLaTeX"
if (skip_biblatex != skip_biblatex_default):                   # reset -m to BibLaTeX, if -sb is set
    if mode != "BibLaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m BibLaTeX', "'-sb'"))
        call.append("-m");
        call.append("BibLaTeX")
        mode = "BibLaTeX"

# ------------------------------------------------------------------
# set load, check, compile, regeneration, and output

callx            = set(call[1:])                               # copy (set type)

set_load         = {'-A', '--author_template', '-Al', '--author_load_template', '-L', '--license_template', '-Ll', '--license_load_template',
                    '-f', '--download_files', '-k', '--key_template', '-kl', '--key_load_template', '-n', '--number', '-t', '--template', '-tl',
                    '--template_load', '-dbg', '--debugging', '-y', '--year_template', '-yl', '--year_load_template'}
set_check        = {'-c','--check_integrity', '-l','--lists'}
set_output       = { '-A', '--author_template', '-Ao', '--author_out_template', '-b', '--btype', '-k', '--key_template', '-ko', '--key_out_template',
                     '-L', '--license_template', '-Lo', '--license_out_template', '-m', '--mode', '-mo', '--make_output', '-mt', '--make_topics',
                     '-s', '--skip', '-sb', '--skip_biblatex' '-t', '--template', '-to', '--template_out', '-dbg', '--debugging', '-nf',
                     'no_files', '-y', '--year_template', '-yo', '--year_out_template' }
set_compile      = {'-p', '--pdf_output'}
set_regeneration = {'-r', '--regenerate_pickle_files' }

load             = callx & set_load         != empty_set
output           = callx & set_output       != empty_set
compile          = callx & set_compile      != empty_set
check            = callx & set_check        != empty_set
regeneration     = callx & set_regeneration != empty_set

# ------------------------------------------------------------------
# some other resettings
if load and output and (lists == lists_default):               # load, output, -l ==> check = True, -l = True
    if verbose:
        print(err_mode.format("check =", check, True, "load & output"))
        print(err_mode.format("-l =", lists, True, "load & output"))
    callx.add("-l")
    check = True

if (make_output != make_output_default):                       # -mo ==> load = False
    if verbose:
        print(err_mode.format("load =", load, False, "'-mo'"))
    load = False

if no_files != no_files_default:                               # -nf ==> -p = True, -mt = True
    if pdf_output != pdf_output_default:                       #   -p
        if verbose:
            print(err_mode.format("-p =", pdf_output, pdf_output_default, "-nf"))
        pdf_output = pdf_output_default
    if make_topics != make_topics_default:                     #   -mt
        if verbose:
            print(err_mode.format("-mt =", make_topics, make_topics_default, "-nf"))
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
# construct the call for loading

if load:
    call_load = [sys.executable, "ctanload.py"]
    if direc != direc_default:                            # -d
        call_load.append("-d")
        call_load.append(direc)
    if number != number_default:                          # -n
        call_load.append("-n")
        call_load.append(str(number))
    if output_name != output_name_default:                # -o
        call_load.append("-o")
        call_load.append(output_name)
    if download != download_default:                      # -f
        call_load.append("-f")
    if statistics != statistics_default:                  # -stat
        call_load.append("-stat")
    if verbose != verbose_default:                        # -v
        call_load.append("-v")
    if debugging != debugging_default:                    # -dbg
        call_load.append("-dbg")

    # process -t a/o -tl a/o -to
    w1 = name_template
    w2 = name_load_template
    w3 = name_out_template
    A1 = name_template      != name_template_default
    A2 = name_load_template != name_load_template_default
    A3 = name_out_template  != name_out_template_default
    if A1:
        if A2 and A3:
            call_load.append("-t"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-t"); call_load.append(w2)
        elif not A2 and A3:
            call_load.append("-t"); call_load.append(w1)
        elif not A2 and not A3:
            call_load.append("-t"); call_load.append(w1)
    else:
        if A2 and A3:
            call_load.append("-t"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-t"); call_load.append(w2)
        elif not A2 and A3:
            pass

    # process -k a/o -kl a/o -ko
    w1 = key_template
    w2 = key_load_template
    w3 = key_out_template
    A1 = key_template      != key_template_default
    A2 = key_load_template != key_load_template_default
    A3 = key_out_template  != key_out_template_default
    if A1:
        if A2 and A3:
            call_load.append("-k"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-k"); call_load.append(w2)
        elif not A2 and A3:
            call_load.append("-k"); call_load.append(w1)
        elif not A2 and not A3:
            call_load.append("-k"); call_load.append(w1)
    else:
        if A2 and A3:
            call_load.append("-k"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-k"); call_load.append(w2)
        elif not A2 and A3:
            pass

    # process -A a/o -Al a/o -Ao
    w1 = author_template
    w2 = author_load_template
    w3 = author_out_template
    A1 = author_template      != author_template_default
    A2 = author_load_template != author_load_template_default
    A3 = author_out_template  != author_out_template_default
    if A1:
        if A2 and A3:
            call_load.append("-A"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-A"); call_load.append(w2)
        elif not A2 and A3:
            call_load.append("-A"); call_load.append(w1)
        elif not A2 and not A3:
            call_load.append("-A"); call_load.append(w1)
    else:
        if A2 and A3:
            call_load.append("-A"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-A"); call_load.append(w2)
        elif not A2 and A3:
            pass

    # process -L a/o -Ll a/o -Lo
    w1 = license_template
    w2 = license_load_template
    w3 = license_out_template
    A1 = license_template      != license_template_default
    A2 = license_load_template != license_load_template_default
    A3 = license_out_template  != license_out_template_default
    if A1:
        if A2 and A3:
            call_load.append("-L"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-L"); call_load.append(w2)
        elif not A2 and A3:
            call_load.append("-L"); call_load.append(w1)
        elif not A2 and not A3:
            call_load.append("-L"); call_load.append(w1)
    else:
        if A2 and A3:
            call_load.append("-L"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-L"); call_load.append(w2)
        elif not A2 and A3:
            pass

    # process -y a/o -yl a/o -yo
    w1 = year_template
    w2 = year_load_template
    w3 = year_out_template
    A1 = year_template      != year_template_default
    A2 = year_load_template != year_load_template_default
    A3 = year_out_template  != year_out_template_default
    if A1:
        if A2 and A3:
            call_load.append("-y"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-y"); call_load.append(w2)
        elif not A2 and A3:
            call_load.append("-y"); call_load.append(w1)
        elif not A2 and not A3:
            call_load.append("-y"); call_load.append(w1)
    else:
        if A2 and A3:
            call_load.append("-y"); call_load.append(w2)
        elif A2 and not A3:
            call_load.append("-y"); call_load.append(w2)
        elif not A2 and A3:
            pass

# ------------------------------------------------------------------
# (B) call_check
# construct the call for checking

if check:
    call_check = [sys.executable, "ctanload.py"]
    if verbose != verbose_default:                        # -v
        call_check.append("-v")
    if statistics != statistics_default:                  # -stat
        call_check.append("-stat")
    if integrity != integrity_default:                    # -c
        call_check.append("-c")
    if lists != lists_default:                            # -l
        call_check.append("-l")
    if direc != direc_default:                            # -d
        call_check.append("-d")
        call_check.append(direc)
    if output_name != output_name_default:                # -o
        call_check.append("-o")
        call_check.append(output_name)
    if debugging != debugging_default:                    # -dbg
        call_check.append("-dbg")

# ------------------------------------------------------------------
# (C) call_output
# construct the call for output generating

if output:
    call_output = [sys.executable, "ctanout.py"]
    if verbose != verbose_default:                        # -v
        call_output.append("-v")
    if statistics != statistics_default:                  # -stat
        call_output.append("-stat")
    if btype != btype_default:                            # -b
        call_output.append("-b")
        call_output.append(btype)
    if skip_biblatex != skip_biblatex_default:            # -sb
        call_output.append("-sb")
        call_output.append(skip_biblatex)
    if direc != direc_default:                            # -d
        call_output.append("-d")
        call_output.append(direc)
    if output_name != output_name_default:                # -o
        call_output.append("-o")
        call_output.append(output_name)
    if mode != mode_default:                              # -m
        call_output.append("-m")
        call_output.append(mode)
    if skip != skip_default:                              # -s
        call_output.append("-s")
        call_output.append(skip)
    if make_topics != make_topics_default:                # -mt
        call_output.append("-mt")
    if debugging != debugging_default:                    # -dbg
        call_output.append("-dbg")
    if no_files != no_files_default:                      # -nf
        call_output.append("-nf")
    
    # process -t a/o -to a/o -tl
    w1 = name_template
    w2 = name_load_template
    w3 = name_out_template
    A1 = name_template      != name_template_default
    A2 = name_load_template != name_load_template_default
    A3 = name_out_template  != name_out_template_default
    if A1:
        if A2 and A3:
            call_output.append("-t"); call_output.append(w3)
        elif A2 and not A3:
            call_output.append("-t"); call_output.append(w1)
        elif not A2 and A3:
            call_output.append("-t"); call_output.append(w3)
        elif not A2 and not A3:
            call_output.append("-t"); call_output.append(w1)
    else:
        if A2 and A3:
            call_output.append("-t"); call_output.append(w3)
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-t"); call_output.append(w3)

    # process -k a/o -ko a/o -kl
    w1 = key_template
    w2 = key_load_template
    w3 = key_out_template
    A1 = key_template      != key_template_default
    A2 = key_load_template != key_load_template_default
    A3 = key_out_template  != key_out_template_default
    if A1:
        if A2 and A3:
            call_output.append("-k"); call_output.append(w3)
        elif A2 and not A3:
            call_output.append("-k"); call_output.append(w1)
        elif not A2 and A3:
            call_output.append("-k"); call_output.append(w3)
        elif not A2 and not A3:
            call_output.append("-k"); call_output.append(w1)
    else:
        if A2 and A3:
            call_output.append("-k"); call_output.append(w3)
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-k"); call_output.append(w3)

    # process -A a7o -Ao a/o -Al
    w1 = author_template
    w2 = author_load_template
    w3 = author_out_template
    A1 = author_template      != author_template_default
    A2 = author_load_template != author_load_template_default
    A3 = author_out_template  != author_out_template_default
    if A1:
        if A2 and A3:
            call_output.append("-A"); call_output.append(w3)
        elif A2 and not A3:
            call_output.append("-A"); call_output.append(w1)
        elif not A2 and A3:
            call_output.append("-A"); call_output.append(w3)
        elif not A2 and not A3:
            call_output.append("-A"); call_output.append(w1)
    else:
        if A2 and A3:
            call_output.append("-A"); call_output.append(w3)
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-A"); call_output.append(w3)

    # process -L a/o -Lo a/o -Ll
    w1 = license_template
    w2 = license_load_template
    w3 = license_out_template
    A1 = license_template      != license_template_default
    A2 = license_load_template != license_load_template_default
    A3 = license_out_template  != license_out_template_default
    if A1:
        if A2 and A3:
            call_output.append("-L"); call_output.append(w3)
        elif A2 and not A3:
            call_output.append("-L"); call_output.append(w1)
        elif not A2 and A3:
            call_output.append("-L"); call_output.append(w3)
        elif not A2 and not A3:
            call_output.append("-L"); call_output.append(w1)
    else:
        if A2 and A3:
            call_output.append("-L"); call_output.append(w3)
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-L"); call_output.append(w3)

    # process -y a/o -yl a/o -yo
    w1 = year_template
    w2 = year_load_template
    w3 = year_out_template
    A1 = year_template      != year_template_default
    A2 = year_load_template != year_load_template_default
    A3 = year_out_template  != year_out_template_default
    if A1:
        if A2 and A3:
            call_output.append("-y"); call_output.append(w3)
        elif A2 and not A3:
            call_output.append("-y"); call_output.append(w1)
        elif not A2 and A3:
            call_output.append("-y"); call_output.append(w3)
        elif not A2 and not A3:
            call_output.append("-y"); call_output.append(w1)
    else:
        if A2 and A3:
            call_output.append("-y"); call_output.append(w3)
        elif A2 and not A3:
            pass
        elif not A2 and A3:
            call_output.append("-y"); call_output.append(w3)

# ------------------------------------------------------------------
# (E, F) call_compile + call_index

if compile:
    direc_comp   = re.sub(r"\\", "/", direc)
    call_compile = latex_processor + space + direc_comp + output_name  + ".tex"
    call_index   = index_processor + space + direc_comp + output_name  + ".idx" + space + "-o " + space + direc_comp + output_name  + ".ind"

# ------------------------------------------------------------------
# (D) call_regeneration
# construct the call for regneration

if regeneration:
    call_regeneration = [sys.executable, "ctanload.py"]
    if verbose != verbose_default:                        # -v
        call_regeneration.append("-v")
    if statistics != statistics_default:                  # -stat
        call_regeneration.append("-stat")
    if regenerate != regenerate_default:                  # -r
        call_regeneration.append("-r")
    if number != number_default:                          # -n
        call_regeneration.append("-n")
        call_regeneration.append(str(number))
    if direc != direc_default:                            # -d
        call_regeneration.append("-d")
        call_regeneration.append(direc)
    if output_name != output_name_default:                # -o
        call_regeneration.append("-o")
        call_regeneration.append(output_name)
    if debugging != debugging_default:                    # -dbg
        call_regeneration.append("-dbg")


#===================================================================
# Auxiliary function

def fold(s):                                              # function fold: auxiliary function: shorten long option lists for output
    """auxiliary function: shorten long option values for output

    s: string, to be folded"""

    offset = 79 * " "
    maxlen = 70
    sep    = "|"
    parts  = s.split(sep)
    line   = ""
    out    = ""
    for f in range(0,len(parts) ):
        if f != len(parts) - 1:
            line = line + parts[f] + sep
        else:
            line = line + parts[f]
        if len(line) >= maxlen:
            out = out +line+ "\n" + offset
            line = ""
    out = out + line
    return out

# ------------------------------------------------------------------
def remove_LaTeX_file(t):                                 # auxiliary function remove_LaTeX_file: removes named LaTeX file.
    """auxiliary function: remove named LaTeX file.

    t: file to be removed"""

    # external methods/functions:
    # path.exists
    # os.remove

    if delete_temporary_file:
        if t in latex_files:
            if path.exists(args.output_name + t):
                os.remove(args.output_name + t)
                if verbose:
                    print("[CTANLoad+Out] Warning: LaTeX file '{}' removed".format(args.output_name + t))
            else:
                pass

# ------------------------------------------------------------------
def remove_other_file(t):                                 # auxiliary function remove_other_file: removes named other file
    """auxiliary function: remove named other file.

    t: file to be removed """

    # external methods/functions:
    # path.exists
    # os.remove

    if delete_temporary_file:
        if t in other_files:
            if path.exists(args.output_name + t):
                os.remove(args.output_name + t)
                if verbose:
                    print("[CTANLoad+Out] Warning: file '{}' removed".format(args.output_name + t))
            else:
                pass


#===================================================================
# Functions

# ------------------------------------------------------------------
def func_call_load():                                     # function func_call_load(): CTANLoad is processed.
    """CTANLoad is processed."""

    # external methods/functions:
    # subprocess.run
    # sys.exit

    if verbose:
        print("-" * sepline_length)
    print("[CTANLoad+Out] Info: CTANLoad (Load)")

    try:
        process_load      = subprocess.run(call_load, capture_output=True, universal_newlines=True)
        load_message      = process_load.stdout
        load_errormessage = process_load.stderr
        if len(load_errormessage) > 0:
            print(load_errormessage)
            sys.exit()
        else:
            print(load_message)
    except:
        sys.exit("[CTANLoad+Out] Error: Error in CTANLoad (Load)")

    if verbose:
        print("\n" + "[CTANLoad+Out] Info: CTANLoad (Load) completed")

# ------------------------------------------------------------------
def func_call_check():                                    # function func_call_check(): CTANLoad (Check) is processed.
    """CTANLoad (Check) is processed."""

    # external methods/functions:
    # subprocess.run
    # sys.exit

    if verbose:
        print("-" * sepline_length)
    print("[CTANLoad+Out] Info: CTANLoad (Check)")

    try:
        process_check      = subprocess.run(call_check, universal_newlines=True)
        check_message      = process_check.stdout
        check_errormessage = process_check.stderr
        if check_errormessage != None:
            print(check_errormessage)
            sys.exit()
        elif check_message != None:
            print(check_message)
    except:
        sys.exit("[CTANLoad+Out] Error: Error in CTANLoad (Check)")

    if verbose:
        print("\n" + "[CTANLoad+Out] Info: CTANLoad (Check) completed")

# ------------------------------------------------------------------
def func_call_regeneration():                             # function func_call_regeneration(): CTANLoad (Regeneration) is processed.
    """CTANLoad (Regeneration) is processed."""

    # external methods/functions:
    # subprocess.run
    # sys.exit

    if verbose:
        print("-" * sepline_length)
    print("[CTANLoad+Out] Info: CTANLoad (Regeneration)")

    try:
        process_regeneration      = subprocess.run(call_regeneration, capture_output=True, universal_newlines=True)
        regeneration_errormessage = process_regeneration.stderr
        regeneration_message      = process_regeneration.stdout
        if len(regeneration_errormessage) > 0:
            print("[CTANLoad+Out] Error: Error in CTANLoad (Regeneration)")
            print(regeneration_errormessage)
            sys.exit()
        else:
            print(regeneration_message)
    except:
        sys.exit("[CTANLoad+Out] Error: Error in CTANLoad (Regeneration)")

    if verbose:
        print("\n" + "[CTANLoad+Out] Info: CTANLoad (Regeneration) completed")

# ------------------------------------------------------------------
def func_call_output():                                   # function func_call_output(): CTANOut is processed.
    """CTANOut is processed."""

    # func_call_output ---> remove_other_file
    # func_call_output ---> remove_LaTeX_file

    # --------------------------------------------
    # external methods/functions:
    # subprocess.run
    # sys.exit

    if verbose:
        print("-" * sepline_length)
    print("[CTANLoad+Out] Info: CTANOut")

    # remove some relevant files
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
        process_output      = subprocess.run(call_output, capture_output=True, universal_newlines=True)
        output_errormessage = process_output.stderr
        output_message      = process_output.stdout
        if len(output_errormessage) > 0:
            print("[CTANLoad+Out] Error: Error in CTANOut")
            print(output_errormessage)
            sys.exit()
        else:
            print(output_message)
    except:
        sys.exit("[CTANLoad+Out] Error: Error in CTANOut")

    if verbose:
        print("\n" + "[CTANLoad+Out] Info: CTANOut completed")

# ------------------------------------------------------------------
def func_call_compile():                                  # Compiles the generated LaTeX file
    """Compile the generated LaTeX file."""

    # func_call_compile ---> remove_LaTeX_file

    # --------------------------------------------
    # external methods/functions:
    # path.exists

    if verbose:
        print("-" * sepline_length)
    print("[CTANLoad+Out] Info: Compilation")

    file_name     = direc + output_name + ".tex"
    file_name_log = direc + output_name + ".log"
    file_name_ilg = direc + output_name + ".ilg"

    if path.exists(file_name):
        if path.getsize(file_name) > 3000:

            # step 1
            for e in [".aux", ".idx", ".ind", ".log", ".ilg", ".pdf", ".out", ".bbl", ".indlualatex"]:
                remove_LaTeX_file(e)

            print("[CTANLoad+Out] Info: " + latex_processor)
            if verbose:
                print("[CTANLoad+Out] Info: Program call:", call_compile)

            try:
                process_compile1      = subprocess.run(call_compile, capture_output=True, universal_newlines=True)
                compile1_errormessage = process_compile1.stderr
                compile1_message      = process_compile1.stdout
                if len(compile1_errormessage) > 0:
                    print("[CTANLoad+Out] Error: Error in compilation")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_log))
                        print("[CTANLoad+Out] Info: Compilation OK")
            except:
                if verbose:
                    print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_log))
                sys.exit("[CTANLoad+Out] Error: Error in compilation")

# ...................................................................
            # step 2
            if verbose:
                print("." * sepline_length)
            print("[CTANLoad+Out] Info: " + latex_processor)
            if verbose:
                print("[CTANLoad+Out] Info: Program call:", call_compile)

            try:
                process_compile2      = subprocess.run(call_compile, capture_output=True, universal_newlines=True)
                compile2_errormessage = process_compile2.stderr
                compile2_message      = process_compile2.stdout
                if len(compile2_errormessage) > 0:
                    print("[CTANLoad+Out] Error: Error in compilation")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_log))
                        print("[CTANLoad+Out] Info: Compilation OK")
            except:
                if verbose:
                    print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_log))
                sys.exit("[CTANLoad+Out] Error: Error in compilation")

# ...................................................................
            # step 3
            if verbose:
                print("." * sepline_length)
            print("[CTANLoad+Out] Info: " + index_processor)
            if verbose:
                print("[CTANLoad+Out] Info: Program call:", call_index)

            try:
                process_index      = subprocess.run(call_index, capture_output=True, universal_newlines=True)
                index_errormessage = process_index.stderr
                index_message      = process_index.stdout
            except:
                if verbose:
                    print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_ilg))
                sys.exit("[CTANLoad+Out] Error: Error in Makeindex")
            if verbose:
                print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_ilg))
                print("[CTANLoad+Out] Info: Makeindex OK")

# ...................................................................
            # step 4
            if verbose:
                print("." * sepline_length)
            print("[CTANLoad+Out] Info: " + latex_processor)
            if verbose:
                print("[CTANLoad+Out] Info: Program call:", call_compile)

            try:
                process_compile3      = subprocess.run(call_compile, capture_output=True, universal_newlines=True)
                compile3_errormessage = process_compile3.stderr
                compile3_message      = process_compile3.stdout
                if len(compile3_errormessage) > 0:
                    print("[CTANLoad+Out] Error: Error in compilation:")
                    sys.exit()
                else:
                    if verbose:
                        print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_log))
                        print("[CTANLoad+Out] Info: result in '" + direc + output_name + ".pdf'")
                        print("[CTANLoad+Out] Info: Compilation OK\n")
            except:
                if verbose:
                    print("[CTANLoad+Out] Info: more information in '{0}'".format(file_name_log))
                sys.exit("[CTANLoad+Out] Error: Error in compilation")
        else:
            if verbose: print("[CTANLoad+Out] Warning: LaTeX file '{0}' without content, no compilation".format(file_name))
    else:
        if verbose: print("[CTANLoad+Out] Warning: LaTeX file '{0}' does not exist, no compilation".format(file_name))

# ...................................................................
    # remove some LaTeX files
    for e in [".aux", ".idx", ".ind", ".out", ".bbl", ".indlualatex"]:
        remove_LaTeX_file(e)

# ------------------------------------------------------------------
def head():                                               # function head: shows the called options
    """Show the given options."""

    # head ---> fold

    call[0] = "CTANLoad+Out.py"
    print("[CTANLoad+Out] Info: CTANLoad+Out")
    if verbose:
        print("date/time:".ljust(left + 1), actDate, actTime)
        print("program/version:".ljust(left + 1), programname, "/", programversion, "\n")

        
        print("[CTANLoad+Out] Info: Program call:", call)
        if ("-c" in call) or ("--check_integrity" in call):
            print("  {0:5} {1:70}".format("-c", "(" + integrity_text + ")"))                                                          # -c (Flag)
        if ("-f" in call) or ("--download_files" in call):
            print("  {0:5} {1:70}".format("-f", "(" + download_text + ")"))                                                           # -f (Flag)
        if ("-l" in call) or ("--lists" in call):
            print("  {0:5} {1:70}".format("-l", "(" + (lists_text + ")")[0:65] + ellipse))                                            # -l (Flag)
        if ("-mo" in call) or ("--make_output" in call):
            print("  {0:5} {1:70}".format("-mo", "(" + (make_output_text + ")")[0:65] + ellipse))                                     # -mo (Flag)
        if ("-mt" in call) or ("--make_topics" in call):
            print("  {0:5} {1:70}".format("-mt", "(" + (topics_text + ")")[0:65] + ellipse))                                          # -mt (Flag)
        if ("-nf" in call) or ("--no_files" in call):
            print("  {0:5} {1:70}".format("-nf", "(" + (no_files_text + ")")[0:65] + ellipse))                                        # -nf (Flag)
        if ("-p" in call) or ("--pdf_output" in call):
            print("  {0:5} {1:70}".format("-p", "(" + pdf_output_text + ")"))                                                         # -p (Flag)
        if ("-r" in call) or ("--regenerate_pickle_files" in call):
            print("  {0:5} {1:70}".format("-r", "(" + regenerate_text + ")"))                                                         # -r (Flag)
        if ("-stat" in call) or ("--statistics" in call):
            print("  {0:5} {1:70}".format("-stat", "(" + statistics_text + ")"))                                                      # -stat (Flag)
        if ("-v" in call) or ("--verbose" in call):
            print("  {0:5} {1:70}".format("-v", "(" + verbose_text + ")"))                                                            # -v (Flag)

        if ("-b" in call) or ("--btype" in call):
            print("  {0:5} {2:70} {1}".format("-b", btype, "(" + btype_text + ")"))                                                   # -b
        if ("-d" in call) or ("--directory" in call):
            print("  {0:5} {2:70} {1}".format("-d", direc, "(" + direc_text + ")"))                                                   # -d
        if ("-m" in call) or ("--mode" in call):
            print("  {0:5} {2:70} {1}".format("-m", mode, "(" + mode_text + ")"))                                                     # -m
        if ("-n" in call) or ("--number" in call):
            print("  {0:5} {2:70} {1}".format("-n", number, "(" + number_text + ")"))                                                 # -n
        if ("-o" in call) or ("--output" in call):
            print("  {0:5} {2:70} {1}".format("-o", args.output_name, "(" + output_text + ")"))                                       # -o
        if ("-s" in call) or ("--skip" in call):
            print("  {0:5} {2:70} {1}".format("-s", skip, "(" + skip_text + ")"))                                                     # -s
        if ("-sb" in call) or ("--skip_biblatex" in call):
            print("  {0:5} {2:70} {1}".format("-sb", skip_biblatex, "(" + skip_biblatex_text + ")"))                                  # -sb

        if ("-k" in call) or ("--key_template" in call):
            print("  {0:5} {2:70} {1}".format("-k", fold(key_template), "(" + (key_template_text + ")")[0:65] + ellipse))             # -k (keys)
        if ("-kl" in call) or ("--key_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-kl", fold(key_load_template), "(" + (key_load_template_text + ")")[0:65] + ellipse))  # -kl (keys)
        if ("-ko" in call) or ("--key_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-ko", fold(key_out_template), "(" + (key_out_template_text + ")")[0:65] + ellipse))    # -ko (keys)

        if ("-t" in call) or ("--name_template" in call):
            print("  {0:5} {2:70} {1}".format("-t", fold(name_template), "(" + name_template_text + ")"))                             # -t (names)
        if ("-tl" in call) or ("--name_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-tl", fold(name_load_template), "(" + name_load_template_text + ")"))                  # -tl (names)
        if ("-to" in call) or ("--name_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-to", fold(name_out_template), "(" + name_out_template_text + ")"))                    # -to (names)

        if ("-A" in call) or ("--author_template" in call):
            print("  {0:5} {2:70} {1}".format("-A", fold(author_template), "(" + author_template_text + ")"))                         # -A (authors)
        if ("-Al" in call) or ("--author_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-Al", fold(author_load_template), "(" + author_load_template_text + ")"))              # -Al (authors)
        if ("-Ao" in call) or ("--author_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-Ao", fold(author_out_template), "(" + author_out_template_text + ")"))                # -Ao (authors)

        if ("-L" in call) or ("--license_template" in call):
            print("  {0:5} {2:70} {1}".format("-L", fold(license_template), "(" + license_template_text + ")"))                       # -L (licenses)
        if ("-Ll" in call) or ("--license_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-Ll", fold(license_load_template), "(" + license_load_template_text + ")"))            # -Ll (licenses)
        if ("-Lo" in call) or ("--license_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-Lo", fold(license_out_template), "(" + license_out_template_text + ")"))              # -Lo (licenses)

        if ("-y" in call) or ("--year_template" in call):
            print("  {0:5} {2:70} {1}".format("-y", fold(year_template), "(" + year_template_text + ")"))                             # -y (years)
        if ("-yl" in call) or ("--year_load_template" in call):
            print("  {0:5} {2:70} {1}".format("-yl", fold(year_load_template), "(" + year_load_template_text + ")"))                  # -yl (years)
        if ("-yo" in call) or ("--year_out_template" in call):
            print("  {0:5} {2:70} {1}".format("-yo", fold(year_out_template), "(" + year_out_template_text + ")"))                    # -yo (years)

        print("\n")

        if regeneration: print("[CTANLoad+Out] Info: CTANLoad (Regeneration) to be executed")
        if load:         print("[CTANLoad+Out] Info: CTANLoad (Load)         to be executed")
        if check:        print("[CTANLoad+Out] Info: CTANLoad (Check)        to be executed")
        if output:       print("[CTANLoad+Out] Info: CTANOut                 to be executed")
        if compile:      print("[CTANLoad+Out] Info: LuaLaTeX and MakeIndex  to be executed")

# ------------------------------------------------------------------
def main():                                       # main function
    """Main Function"""

    # main ---> head
    # main ---> func_call_regeneration
    # main ---> func_call_load
    # main ---> func_call_check
    # main ---> func_call_output
    # main ---> func_call_compile

    file_name = direc + output_name + ".tex"

    if verbose:
        print("=" * sepline_length)
    head()

    if regeneration:                              # -r has been called
        func_call_regeneration()
    if load:
        func_call_load()
    if check:                                     # -l a/o -c has been called
        func_call_check()
    if output:
        func_call_output()
    if compile:                                   # the LaTeX processor will produce a PDF file
        func_call_compile()
    if verbose:
        print("-" * sepline_length)
           

#===================================================================
# Main Part

if __name__ == "__main__":
    try:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    except:
        pass
    
    starttotal   = time.time()                    # set begin of total time
    startprocess = time.process_time()            # set begin of process time

    main()                                        # main part called
    if statistics:                                # output the rest of statistics
        pp         = 6
        endtotal   = time.time()
        endprocess = time.process_time()
        print("---")
        print("total time (CTANLoad+Out): ".ljust(left + 3), str(round(endtotal-starttotal, 2)).rjust(pp))
        print("process time (CTANLoad+Out): ".ljust(left + 3), str(round(endprocess-startprocess, 2)).rjust(pp))
    if verbose:
        print("\n" + "[CTANLoad+Out] Info: CTANLoad+Out completed.")
else:
    print("[CTANLoad+Out] Error: tried to use the program indirectly")


#===================================================================

# Problems/Plans:
# + prüfen, ob ctanload -l -c aufgerufen werden muss (wenn CTANOut folgt)
# + ist -c gefährlich?
# + Index verweist auf Seitenummern; all.xref und all.tap auf Abschnittsnummer
# + Programmabbruch bei -ko graphics oder -ko class (x)
# + Fehler bei LaTeX-Ausgabe: UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 262476: character maps to <undefined>
# + alle Textdateien überprüfen bzw. neu machen (x)
# + year_template_default angepasst an CTANLoad und CTANOut (x)

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
# 1.39 2ß23-07-01 messages with an additional identifier "[CTANLoad+Out]"
