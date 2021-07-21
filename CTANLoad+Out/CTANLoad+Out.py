#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANLoad+Out.py
# (C) Günter Partosch, 2021

# Problems/Plans:
# + prüfen, ob ctanload -l -c aufgerufen werden muss (wenn CTANOut folgt)
# + ist -c gefährlich?

# ------------------------------------------------------------------
# History:

# 0.1  2021-05-01 start
# 0.9  2021-05-04 first working version
# 1.0  2021-05-24 program completed
# 1.1  2021-05-28 compilation enabled
# 1.2  2021-05-31 some improvements (calls, compilation)
# 1.3  2021-06-12 auxiliary function fold: shorten long option values for output
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
# 1.18 2021-07-18 xyz.tex and all other LaTeX relevant files before compilation a/o -mt deleted
# 1.19 2021-07-19 there is no compilation if -A a/o -k a/o -t results "no packages found"
# 1.20 2021-07-19 -mo now prevents loading by CTANLoad

# ------------------------------------------------------------------
# Messages (CTANLoad+Out)
# 
# Fatal error:
# Error: Error in <step>
# Error: tried to use the program indirectly
#
# Information:
# Info: <step> OK
# Info: Call: <call>
# Info: <step> to be executed
# Info: <step>
# Info: more information in '<log file>'
# Info: result in '<file>'
#
# Warning:
# Warning: LaTeX file '<file>' does not exist
# Warning: LaTeX file '<file>' removed
# Warning: file '<file>' removed
 
# ------------------------------------------------------------------
# Functions in CTANLoad+Out.py

# fold(s)                      auxiliary function shorten long option value text for output
# func_call_check()            CTANLoad (Check) is processed.
# func_call_compile()          Compile the generated LaTeX file.
# func_call_load()             CTANLoad is processed.      
# func_call_output()           CTANOut is processed.
# func_call_regeneration()     CTANLoad (Regeneration) is processed.
# head()                       show the given options
# main()                       main function
# remove_LaTeX_file(t)         auxiliary function; remove some temporary LaTeX files

# ------------------------------------------------------------------
# Examples (CTANLoad+Out)
# 
# CTANLoad+Out -r
#   + regeneration of the 2 pickle files                                           [-r]
#   + a lot of new PDF files
#   + results in CTAN.pkl and CTAN2.pkl
#   + without statistics
#   + not verbose
# 
# CTANLoad+Out -r -v -stat
#   + regeneration of the 2 pickle files                                           [-r]
#   + a lot of new PDF files
#   + results in CTAN.pkl and CTAN2.pkl
#   + with statistics                                                              [-stat]
#   + verbose                                                                      [-v]
# 
# CTANLoad+Out -l
#   + CTAN.pkl rewritten
#   + all.loa, all.lop, all.lok, all.lol, all.lpt, all.lap rewritten               [-l]
#   + without statistics
#   + not verbose
# 
# CTANLoad+Out -l -v -stat
#   + CTAN.pkl rewritten
#   + all.loa, all.lop, all.lok, all.lol, all.lpt, all.lap rewritten               [-l]
#   + with statistics
#   + verbose                                                                      [-v]
# 
# CTANLoad+Out -mt -p
#   + no XML/PDF file from CTAN is downloaded
#   + 1st step:
#   + all XML/PDF files in the current directory are processed
#   + output format is LaTeX (implicitely)                                         [-mt]
#   + temporary output file is all.tex
#   + all.top,  all.xref, all.tap are generated (will be included in all.tex)      [-mt]
#   + 2nd step:
#   + all.tex is completely compiled                                     [-p]
#   + output file is all.pdf
#   + without statistics
#   + not verbose
# 
# CTANLoad+Out -mt -m latex -p -v -stat
#   + no XML/PDF file from CTAN is downloaded
#   + 1st step:
#   + all XML files in the current directory are processed
#   + output format is LaTeX                                                       [-m]
#   + temporary output file is all.tex
#   + all.top,  all.xref, all.tap are generated (will be included in all.tex)      [-mt]
#   + 2nd step:
#   + all.tex is completely compiled                                               [-p]
#   + output file is all.pdf
#   + with statistics                                                              [-stat]
#   + verbose                                                                      [-v]
# 
# CTANLoad+Out -to latex -m bib -v -stat
#   + no XML/PDF file from CTAN is downloaded
#   + all local XML fies which match the name template "latex" are processed       [-to]
#   + output format is BibLaTeX
#   + output file is all.bib                                                       [-m]
#   + with statistics                                                              [-stat]
#   + verbose                                                                      [-v]
# 
# CTANLoad+Out -t "latex|ltx|l3|lt3" -f -m tex -mt -v -stat
#   + 1st step:
#   + XML file with the name template "latex|ltx|l3|lt3" are downloaded from CTAN        [-t]
#   + associated PDF files are downloaded, too                                           [-f]
#   + 2nd step:
#   + all local XML files which match the name template "latex|ltx|l3|lt3" are processed [-t]
#   + all.top, all.xref, all.tap are generated (will be included in all.tex)             [-mt]
#   + output format is LaTeX                                                             [-m]
#   + output file is all.tex
#   + with statistics                                                                    [-stat]
#   + verbose                                                                            [-v]
# 
# CTANLoad+Out -t pgf -l -c -mt -p -v -stat
#   + 1st step:
#   + XML file with the name template "pgf" are downloaded from CTAN              [-t]
#   + 2nd step:
#   + all.loa, all.lop, all.lok, all.lol, all.lpt, all.lap rewritten              [-l]
#   + a consistency check is done                                                 [-c]
#   + 3rd step:
#   + all local XML files wwith the template "pgf" are processed                  [-t]
#   + all.top, all.xref, all.tap are generated (will be included in all.tex)      [-mt]
#   + output format is LaTeX (implicitely)                                                                 
#   + temporary output file is all.tex
#   + 4th step:
#   + all.tex is completely compiled                                              [-p]
#   + output file is all.pdf
#   + with statistics                                                             [-stat]
#   + verbose                                                                     [-v]
# 
# CTANLoad+Out -k latex -m txt -v 
#   + 1st step:
#   + download all XML packages which match the topic "latex"                     [-k]
#   + 2nd step:
#   + all local XML files with the topic "latex" are processed                    [-k]
#   + output format is plain                                                      [-m]
#   + output file is all.txt
#   + without statistics
#   + verbose                                                                     [-v]
#
# CTANLoad+Out -k latex -f -v -stat -mt -p
#   + 1st step:
#   + download all XML packages which match the topic "LaTeX"                     [-k]
#   + load the associated information files (PDF)                                 [-f]
#   + 2nd step:
#   + process all local XML files with the topic "latex"                          [-k]
#   + output format is LaTeX (implicitely)                                                                 
#   + temporary output file is all.tex
#   + all.top, all.xref, all.tap are generated (will be included in all.tex)      [-mt]
#   + 3th step:
#   + all.tex is completely compiled                                              [-p]
#   + output file is all.pdf
#   + verbose                                                                     [-v]
#   + with statistics                                                             [-stat]
#
# CTANLoad+Out -k chinese -t "^zh" -f -v -stat
#   + 1st step:
#   + download all XML packages which match the topic "chinese"                   [-k]
#   + load only CTAN XML files with the name template "^zh"                       [-t]
#   + load the associated information files (PDF)                                 [-f]
#   + 2nd step:
#   + process all local XML packages which match the topic "chinese"              [-k]
#   + process only local XML files with the name template "^zh"                   [-t]
#   + output format is RIS (default)                                                                 
#   + output file is all.ris
#   + verbose                                                                     [-v]
#   + with statistics                                                             [-stat]
#
# CTANLoad+Out -ko "latex" -m bib -v
#   + process all XML files in the current directory with the topic "latex"       [-ko]
#   + output format is BibLaTeX                                                   [-m]                                                           
#   + output file is all.bib
#   + verbose                                                                     [-v]
#   + without statistics
#
# CTANLoad+Out -A "Knuth" -f -v -stat -m latex -mt -p -k "collection" -t "knuth"
#   + 1st step:
#   + download all XML packages which match the topic "collection"                [-k]
#   + download only packages which match the author name template "Knuth"         [-A]
#   + download only packages with the name template "knuth"                       [-t]
#   + load the associated information files (PDF)                                 [-f]
#   + 2nd step:
#   + process all local XML files which match the topic "collection"              [-k]
#   + download local XML files which match the author name template "Knuth"       [-A]
#   + download local XML files with the name template "knuth"                     [-t]
#   + output format is LaTeX                                                      [-m]            
#   + temporary output file is all.tex
#   + all.top, all.xref, all.tap are generated (will be included in all.tex)      [-mt]
#   + 3th step:
#   + all.tex is completely compiled                                              [-p]
#   + output file is all.pdf
#   + verbose                                                                     [-v]
#   + with statistics                                                             [-stat]

# Regular expressions
# -------------------
# The options -t (a/o -to and -tl) and -k (a/o -ko and -kl) need regular expressions as values.
# such as
#
# -k latex                matches all topic names which contain "latex"
# -t "latex|ltx|l3|lt3"   matches all file names which contain "latex", "ltx", "l3" or "t3"
# -t "^.+$"               matches all file names
# -t "^{a-b]"             matches all file names which begin with letters a-b


#===================================================================
# Usage
# =====

# usage: CTANLoad+Out.py [-h] [-a] [-A AUTHOR_TEMPLATE]
#                        [-Al AUTHOR_LOAD_TEMPLATE] [-Ao AUTHOR_OUT_TEMPLATE]
#                        [-b {@online,@software,@misc,@ctan,@www}] [-c]
#                        [-d DIREC] [-f] [-k KEY] [-kl KEY_LOAD] [-ko KEY_OUT]
#                        [-l]
#                        [-m {LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,biblatex,bib,Excel,excel}]
#                        [-mo] [-mt] [-n NUMBER] [-o OUTPUT_NAME] [-p] [-r]
#                        [-s SKIP] [-stat] [-t TEMPLATE] [-tl TEMPLATE_LOAD]
#                        [-to TEMPLATE_OUT] [-V] [-v]
# 
# [CTANLoad+Out.py; Version: 1.20 (2021-07-19)] Combines the tasks of CTANLoad
# [Load XLM and PDF documentation files from CTAN a/o generates some special
# lists, and prepares data for CTANOut] and CTANOut [Convert CTAN XLM package
# files to some formats].
# 
# Optional parameters:
#   -h, --help            show this help message and exit
#   -a, --author          Show author of the program and exit.
#   -A AUTHOR_TEMPLATE, --author_template AUTHOR_TEMPLATE
#                         Name template for authors [in CTANLoad and CTANOut] -
#                         Default:
#   -Al AUTHOR_LOAD_TEMPLATE, --author_load_template AUTHOR_LOAD_TEMPLATE
#                         Name template for authors (CTANLoad) - Default:
#   -Ao AUTHOR_OUT_TEMPLATE, --author_out_template AUTHOR_OUT_TEMPLATE
#                         Name template for authors (CTANOutd) - Default:
#   -b {@online,@software,@misc,@ctan,@www}, --btype {@online,@software,@misc,@ctan,@www}
#                         Type of BibLaTex entries to be generated [valid only
#                         for '-m BibLaTeX'/'--mode BibLaTeX'] - Default:
#   -c, --check_integrity
#                         Flag: Check the integrity of the 2nd .pkl file. -
#                         Default: False
#   -d DIREC, --directory DIREC
#                         OS Directory for input and output files - Default: .\
#   -f, --download_files  Flag: Download associated documentation files [PDF]. -
#                         Default: False
#   -k KEY, --key KEY     Template for output filtering on the base of keys [in
#                         CTANLoad and CTANOut] - Default:
#   -kl KEY_LOAD, --key_load KEY_LOAD
#                         Template for output filtering on the base of keys [in
#                         CTANLoad] - Default:
#   -ko KEY_OUT, --key_out KEY_OUT
#                         Template for output filtering on the base of keys [in
#                         CTANOut] - Default: ^.+$
#   -l, --lists           Flag: Generate some special lists and prepare files
#                         for CTANOut. - Default: False
#   -m {LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,biblatex,bib,Excel,excel}, --mode {LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,biblatex,bib,Excel,excel}
#                         Target format - Default: RIS
#   -mo, --make_output    Flag: Generate output [RIS, LaTeX, BibLaTeX, Excel,
#                         plain] via CTANOut. - Default: False
#   -mt, --make_topics    Flag: Generate topic lists [meaning of topics + cross-
#                         reference (topics/packages, authors/packages); only
#                         for -m LaTeX]). - Default: False
#   -n NUMBER, --number NUMBER
#                         Maximum number of file downloads - Default: 250
#   -o OUTPUT_NAME, --output OUTPUT_NAME
#                         Generic name for output files [without extensions] -
#                         Default: all
#   -p, --pdf_output      Flag: Generate PDF output. - Default: False
#   -r, --regenerate_pickle_files
#                         Flag: Regenerate the two pickle files. - Default:
#                         False
#   -s SKIP, --skip SKIP  Skip specified CTAN fields. - Default: []
#   -stat, --statistics   Flag: Print statistics on terminal. - Default: False
#   -t TEMPLATE, --template TEMPLATE
#                         Template for package names [in CTANLoad and CTANOut] -
#                         Default:
#   -tl TEMPLATE_LOAD, --template_load TEMPLATE_LOAD
#                         Template for package names in CTANLoad - Default:
#   -to TEMPLATE_OUT, --template_out TEMPLATE_OUT
#                         Template for package names in CTANOut - Default: ^.+$
#   -V, --version         Show version of the program and exit.
#   -v, --verbose         Flag: Output is verbose. - Default: False
 

#===================================================================
# Moduls needed

import argparse                    # argument parsing
import sys                         # system calls
import platform                    # get OS informations
import subprocess                  # handling of sub-processes
import re                          # regular expression
import os                          # delete a file on disk, for instance
from os import path                # path informations


#===================================================================
# Settings

programname       = "CTANLoad+Out.py"
programversion    = "1.20"
programdate       = "2021-07-19"
programauthor     = "Günter Partosch"
authoremail       = "Guenter.Partosch@hrz.uni-giessen.de"
authorinstitution = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"

operatingsys      = platform.system()
call              = sys.argv
empty_set         = set()
latex_processor   = "xelatex"
index_processor   = "makeindex"
empty             = ""
space             = " "
ellipse           = " ..."
call_check        = empty
call_load         = empty
call_output       = empty
call_compile      = empty
call_index        = empty
delete_temporary_file  = True

err_mode          = "+ Warning: '{0} {1}' changed to '{2} (due to {3})'\n"
latex_files       = [".aux", ".bib", ".ilg", ".log", ".idx", ".ind", ".out", ".tex", ".pdf", ".tap", ".top", ".xref"]
other_files       = [".ris", ".bib", ".txt", ".tsv"]

# ------------------------------------------------------------------
# Texts for argument parsing and help

author_load_template_text = "Name template for authors (CTANLoad)"                    # Parameter -Al
author_out_template_text  = "Name template for authors (CTANOutd)"                    # Parameter -Ao
author_template_text      = "Name template for authors [in CTANLoad and CTANOut]"     # Parameter -A

author_text               = "Show author of the program and exit."
btype_text                = "Type of BibLaTex entries to be generated [valid only for '-m BibLaTeX'/'--mode BibLaTeX']"
direc_text                = "OS Directory for input and output files"
download_text             = "Flag: Download associated documentation files [PDF]."
integrity_text            = "Flag: Check the integrity of the 2nd .pkl file."

key_load_text             = "Template for output filtering on the base of keys [in CTANLoad]"
key_out_text              = "Template for output filtering on the base of keys [in CTANOut]"
key_text                  = "Template for output filtering on the base of keys [in CTANLoad and CTANOut]"

##key_text                  = "Template for topic names [in CTANLoad and CTANOut]"
lists_text                = "Flag: Generate some special lists and prepare files for CTANOut."
make_output_text          = "Flag: Generate output [RIS, LaTeX, BibLaTeX, Excel, plain] via CTANOut."
mode_text                 = "Target format"
number_text               = "Maximum number of file downloads"
output_text               = "Generic name for output files [without extensions]"
pdf_text                  = "Flag: Generate PDF output."
program_text              = "Combines the tasks of CTANLoad [Load XLM and PDF documentation files from CTAN a/o generates some special lists, and prepares data for CTANOut] and CTANOut [Convert CTAN XLM package files to some formats]."
regenerate_text           = "Flag: Regenerate the two pickle files."
skip_text                 = "Skip specified CTAN fields."
statistics_text           = "Flag: Print statistics on terminal."

template_load_text        = "Template for package names in CTANLoad"
template_out_text         = "Template for package names in CTANOut"
template_text             = "Template for package names [in CTANLoad and CTANOut]"

topics_text               = "Flag: Generate topic lists [meaning of topics + cross-reference (topics/packages, authors/packages); only for -m LaTeX])."
verbose_text              = "Flag: Output is verbose."
version_text              = "Show version of the program and exit."

# ------------------------------------------------------------------
# Defaults/variables for argparse

author_load_template_default = ""               # default for author load name template (-Al)
author_out_template_default  = ""               # default for author out name template (-Ao)
author_template_default      = ""               # default for author name template (-A)

btype_default                = empty            # default for option -b (BibLaTeX entry type)
download_default             = False            # flag: download PDF files
integrity_default            = False            # flag: integrity check

key_default                  = empty            # default for option -k
key_load_default             = key_default      # default for option -kl
key_out_default              = """^.+$"""       # default for option -ko

lists_default                = False            # flag: generate special lists
make_output_default          = False            # Flag: generate output (RIS, LaTeX, BibLaTeX, Excel, plain)
make_topics_default          = False            # flag: make topics output
mode_default                 = "RIS"            # default for option -m 
number_default               = 250              # default for option -n (maximum number of files to be loaded)
output_name_default          = "all"            # default for option -o (generic file name)
pdf_default                  = False            # flag: produce PDF output
regenerate_default           = False            # default for option -r    (no regeneration)
skip_default                 = "[]"             # default for option -s
statistics_default           = False            # flag: output statistics

template_default             = empty            # default for option -t
template_load_default        = template_default # default for option -tl 
template_out_default         = """^.+$"""       # default for option -to

verbose_default              = False            # flag: output is verbose

act_direc             = "."

if operatingsys == "Windows":    
    direc_sep      = "\\"
else:
    direc_sep      = "/"
    
direc_default         = act_direc + direc_sep # default for -d (OS output directory)


#===================================================================
# Parsing the arguments

parser = argparse.ArgumentParser(description = "[" + programname + "; " + "Version: " + programversion + " (" + programdate + ")] " + program_text)
parser._optionals.title   = 'Optional parameters'

parser.add_argument("-a", "--author",                      # Parameter -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = programauthor + " (" + authoremail + ", " + authorinstitution + ")")

parser.add_argument("-A", "--author_template",             # Parameter -A/--author_template
                    help    = author_template_text + " - Default: " + "%(default)s",
                    dest    = "author_template",
                    default = author_template_default)

parser.add_argument("-Al", "--author_load_template",       # Parameter -Al/--author_load_template
                    help    = author_load_template_text + " - Default: " + "%(default)s",
                    dest    = "author_load_template",
                    default = author_load_template_default)

parser.add_argument("-Ao", "--author_out_template",        # Parameter -Ao/--author_out_template
                    help    = author_out_template_text + " - Default: " + "%(default)s",
                    dest    = "author_out_template",
                    default = author_out_template_default)

parser.add_argument("-b", "--btype",                       # Parameter -b/--btype
                    help    = btype_text + " - Default: " + "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan", "@www"],
                    dest    = "btype",
                    default = btype_default)

parser.add_argument("-c", "--check_integrity",             # Parameter -i/--integrity
                    help    = integrity_text + " - Default: " + "%(default)s",
##                    help    = argparse.SUPPRESS,
                    action  = "store_true",
                    default = integrity_default)

parser.add_argument("-d", "--directory",                   # Parameter -d/--directory
                    help    = direc_text + " - Default: " + "%(default)s",
                    dest    = "direc",
                    default = direc_default)

parser.add_argument("-f", "--download_files",              # Parameter -f/--download_files
                    help    = download_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = download_default)

parser.add_argument("-k", "--key",                         # Parameter -k/--key
                    help    = key_text + " - Default: " + "%(default)s",
                    dest    = "key",
                    default = key_default)

parser.add_argument("-kl", "--key_load",                   # Parameter -kl/--key_load
                    help    = key_load_text + " - Default: " + "%(default)s",
                    dest    = "key_load",
                    default = key_load_default)

parser.add_argument("-ko", "--key_out",                    # Parameter -ko/--key_out
                    help    = key_out_text + " - Default: " + "%(default)s",
                    dest    = "key_out",
                    default = key_out_default)

parser.add_argument("-l", "--lists",                       # Parameter -l/--lists
                    help = lists_text + " - Default: " + "%(default)s",
                    action = "store_true",
                    default = lists_default)

parser.add_argument("-m", "--mode",                        # Parameter -m/--mode
                    help    = mode_text + " - Default: " + "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "ris", "plain", "txt", "BibLaTeX", "biblatex", "bib", "Excel", "excel"],
                    dest    = "mode",
                    default = mode_default)

parser.add_argument("-mo", "--make_output",                # Parameter -mo/--make_output
                    help    = make_output_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_output_default)

parser.add_argument("-mt", "--make_topics",                # Parameter -mt/--make_topics
                    help    = topics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_topics_default)

parser.add_argument("-n", "--number",                      # Parameter -n/--number
                    help    = number_text + " - Default: " + "%(default)s",
                    dest    = "number",
                    default = number_default)

parser.add_argument("-o", "--output",                      # Parameter -o/--output
                    help    = output_text + " - Default: " + "%(default)s",
                    dest    = "output_name",
                    default = output_name_default)

parser.add_argument("-p", "--pdf_output",                  # Parameter -p/--pdf_output
                    help    = pdf_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = pdf_default)

parser.add_argument("-r", "--regenerate_pickle_files",     # Parameter -r/--regenerate_pickle_files
                    help    = regenerate_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = regenerate_default)

parser.add_argument("-s", "--skip",                        # Parameter -s/--skip
                    help    = skip_text + " - Default: " + "%(default)s",
                    dest    = "skip",
                    default = skip_default)

parser.add_argument("-stat", "--statistics",               # Parameter -stat/--statistics
                    help    = statistics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics_default)

parser.add_argument("-t", "--template",                    # Parameter -t/--template
                    help    = template_text + " - Default: " + "%(default)s",
                    dest    = "template",
                    default = template_default)

parser.add_argument("-tl", "--template_load",              # Parameter -tl/--template_load
                    help    = template_load_text + " - Default: " + "%(default)s",
                    dest    = "template_load",
                    default = template_load_default)

parser.add_argument("-to", "--template_out",               # Parameter -to/--template_out
                    help    = template_out_text + " - Default: " + "%(default)s",
                    dest    = "template_out",
                    default = template_out_default)

parser.add_argument("-V", "--version",                     # Parameter -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + programversion + " (" + programdate + ")")

parser.add_argument("-v", "--verbose",                     # Parameter -v/--verbose
                    help = verbose_text + " - Default: " + "%(default)s",
                    action = "store_true",
                    default = verbose_default)

# ------------------------------------------------------------------
# Getting parsed values

args            = parser.parse_args()

author_template      = args.author_template   # parameter -A
author_load_template = args.author_template   # parameter -Al
author_out_template  = args.author_template   # parameter -Ao

btype           = args.btype                  # Parameter -b
direc           = args.direc                  # Parameter -d
download        = args.download_files         # Parameter -f

key             = args.key                    # Parameter -k
key_out         = args.key_out                # Parameter -ko
key_load        = args.key_load               # Parameter -kl

integrity       = args.check_integrity        # Parameter -c
lists           = args.lists                  # Parameter -l
make_output     = args.make_output            # Parameter -mo
make_topics     = args.make_topics            # Parameter -mt
mode            = args.mode                   # Parameter -m
number          = int(args.number)            # Parameter -n
output_name     = args.output_name            # Parameter -o
pdf_output      = args.pdf_output             # Parameter -p
regenerate      = args.regenerate_pickle_files# parameter -r
skip            = args.skip                   # Parameter -s
statistics      = args.statistics             # Parameter -stat

template        = args.template               # Parameter -t
template_load   = args.template_load          # Parameter -tl
template_out    = args.template_out           # Parameter -to

verbose         = args.verbose                # Parameter -v

# ------------------------------------------------------------------
# Correct direc

direc = direc.strip()                         # correct OS directory name (-d)
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
# -f     x     x     -      -
# -k     x     -     x      -
# -kl    x     -     -      -
# -ko    -     -     x      -
# -l     -     x     -      -
# -m     -     -     x      -
# -mo    -     -     x      -
# -mt    -     -     x      -
# -n     x     -     -      -
# -o     x     x     x      x
# -p     -     -     x      x
# -s     -     -     x      -
# -stat  x     x     x      -
# -t     x     -     x      -
# -to    -     -     x      -
# -tl    x     -     -      -
# -v     x     x     x      -
# -V     x     x     x      -

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

if ("-p" in call) or ("--pdf" in call) or ("-mt" in call) or ("--make_topics" in call):  # reset -m to LaTeX, if -p or -mt is set
    if mode != "LaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m LaTeX', "'-mt'/'-p'"))
        call.append("-m")
        call.append("LaTeX")
        mode = "LaTeX"
if ("-b" in call) or ("--btype" in call):                      # reset -m to BibLaTeX, if -b is set
    if mode != "BibLaTeX":
        if verbose:
            print(err_mode.format('-m', mode, '-m BibLaTeX', "'-b'"))
        call.append("-m");
        call.append("BibLaTeX")
        mode = "BibLaTeX"
##if (mode != "LaTeX") and (("-p" in call) or ("--pdf" in call)):
   
# ------------------------------------------------------------------
# set load, check, compile, regeneration, and output

callx       = set(call[1:])

set_load         = {'-t', '--template', '-tl', '--template_load', '-k', '--key', '-kl', '--key_load', '-A', '--author_template', '-Al', '--author_load_template'}
set_check        = {'-l', '-c', '--lists', '--check_integrity'}
set_output       = {'-b',  '-k', '-m', '-mt', '-p', '-s', '--btype', '--key', '--mode', '--make_topics', '--pdf_output', '--skip', 
                    '-mo', '--make_output', '-to', '--template_out', '-ko', '--key_out', '-Ao', '--author_out_template'}
set_compile      = {'-p', '--pdf_output'}
set_regeneration = {'-r', '--regenerate_pickle_files'}

load          = callx & set_load         != empty_set
output        = callx & set_output       != empty_set
compile       = callx & set_compile      != empty_set
check         = callx & set_check        != empty_set
regeneration  = callx & set_regeneration != empty_set

if ('-mo' in callx) or ('--make_output' in callx):
    load = False
    if verbose:
        print(err_mode.format("load", "=True", False, "'-mo'"))


#===================================================================
# Construct the calls

t  = (template      != template_default)
tl = (template_load != template_load_default)
to = (template_out  != template_out_default)

call_load         = empty
call_check        = empty
call_output       = empty
call_regeneration = empty
call_compile      = empty
call_index        = empty

# ------------------------------------------------------------------
# call_load
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
    if template_load != template_load_default:            # -tl
        call_load.append("-t")
        call_load.append(template_load)
    else:
        if template != template_default:                  
            call_load.append("-t")
            call_load.append(template)

    if key_load != key_load_default:                      # -k/-kl
        call_load.append("-k")
        call_load.append(key_load)
    else:
        if key != key_default:                  
            call_load.append("-k")
            call_load.append(key)

    if author_load_template != author_load_template_default:  # -A/-Al
        call_load.append("-A")
        call_load.append(author_load_template)
    else:
        if author_template != author_template_default:                  
            call_load.append("-A")
            call_load.append(author_template)

# ------------------------------------------------------------------
# call_check
# construct the call for checking

if check:
    call_check = [sys.executable, "ctanload.py"]
    if verbose != verbose_default:                        # .v
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

# ------------------------------------------------------------------
# call_output
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
    if template_out != template_out_default:              # -to
        call_output.append("-t")
        call_output.append(template_out)
    else:
        if template != template_default:                  
            call_output.append("-t")
            call_output.append(template)
    if key_out != key_out_default:                        # -k/-ko
        call_output.append("-k")
        call_output.append(key_out)
    else:
        if key != key_default:                  
            call_output.append("-k")
            call_output.append(key)

    if author_out_template != author_out_template_default: # -A/-ko
        call_output.append("-A")
        call_output.append(author_out_template)
    else:
        if author_template != author_template_default:                  
            call_output.append("-A")
            call_output.append(author_template)


# ------------------------------------------------------------------
# call_compile + call_index

if compile:
    direc_comp   = re.sub(r"\\", "/", direc)
    call_compile = latex_processor + space + direc_comp + output_name  + ".tex"
    call_index   = index_processor + space + direc_comp + output_name  + ".idx" + space + "-o " + space + direc_comp + output_name  + ".ind"

# ------------------------------------------------------------------
# call_regeneration
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


#===================================================================
# Auxiliary function

##def fold(s):                                                                    # function fold: auxiliary function: shorten long option value text for output
##    """auxiliary function: shorten long option value text for output"""
##    
##    maxlen = 65
##    offset = "\n" + 64 * " "
##    tmp    = s[:]
##    all    = ""
##    while len(tmp) > maxlen:
##        all = all + tmp[0 : maxlen] + offset
##        tmp = tmp[maxlen :]
##    return all + tmp
def fold(s):                                               # function fold: auxiliary function: shorten long option values for output
    """auxiliary function: shorten long option values for output"""
    
    offset = 64 * " "
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
def remove_LaTeX_file(t):                                                       # auxiliary function: remove named LaTeX file.
    """auxiliary function: remove named LaTeX file."""
    
    if delete_temporary_file:
        if t in latex_files:
            if path.exists(args.output_name + t):
                os.remove(args.output_name + t)
                if verbose:
                    print("* Warning: LaTeX file '{}' removed".format(args.output_name + t))
            else:
                pass

# ------------------------------------------------------------------
def remove_other_file(t):                                                       # auxiliary function: remove named LaTeX file.
    """auxiliary function: remove named other file."""

    if delete_temporary_file:
        if t in other_files:
            if path.exists(args.output_name + t):
                os.remove(args.output_name + t)
                if verbose:
                    print("* Warning: file '{}' removed".format(args.output_name + t))
            else:
                pass


#===================================================================
# Functions

# ------------------------------------------------------------------
def func_call_load():                                                           # function func_call_load(): CTANLoad is processed.      
    """CTANLoad is processed."""

    print("-" * 80)
    print("* Info: CTANLoad (Load)")

    try:
        process_load      = subprocess.run(call_load, capture_output=True, universal_newlines=True)
        load_message      = process_load.stdout
        load_errormessage = process_load.stderr
        if len(load_errormessage) > 0:
            print("* Error: Error in CTANLoad (Load):")
            print(load_errormessage)
            sys.exit()
        else:
            print(load_message)
    except:
        sys.exit("* Error: Error in CTANLoad (Load)")
    if verbose:
        print("* Info: CTANLoad (Load) completed")

# ------------------------------------------------------------------
def func_call_check():                                                          # function func_call_check(): CTANLoad (Check) is processed.
    """CTANLoad (Check) is processed."""

    print("-" * 80)
    print("* Info: CTANLoad (Check)")

    try:                                                  
        process_check      = subprocess.run(call_check, universal_newlines=True)
    except:
        sys.exit("* Error: Error in CTANLoad (Check)")
    if verbose:
        print("* Info: CTANLoad (Check) completed")

# ------------------------------------------------------------------
def func_call_regeneration():                                                   # function func_call_regeneration(): CTANLoad (Regeneration) is processed.
    """CTANLoad (Regeneration) is processed."""

    print("-" * 80)
    print("* Info: CTANLoad (Regeneration)")

    try:                                                  
        process_regeneration      = subprocess.run(call_regeneration, capture_output=True, universal_newlines=True)
        regeneration_errormessage = process_regeneration.stderr
        regeneration_message      = process_regeneration.stdout
        if len(regeneration_errormessage) > 0:
            print("* Error: Error in CTANLoad (Regeneration)")
            print(regeneration_errormessage)
            sys.exit()
        else:
            print(regeneration_message)
    except:
        sys.exit("* Error: Error in CTANLoad (Regeneration)")
    if verbose:
        print("* Info: CTANLoad (Regeneration) completed")

# ------------------------------------------------------------------
def func_call_output():                                                         # function func_call_output(): CTANOut is processed.
    """CTANOut is processed."""

    print("-" * 80)
    print("* Info: CTANOut")
    if mode == "BibLaTeX":
        remove_other_file(".bib")
    elif mode == "LaTeX":
        remove_LaTeX_file(".tex")
        remove_LaTeX_file(".tap")
        remove_LaTeX_file(".top")
        remove_LaTeX_file(".xref")
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
            print("* Error: Error in CTANOut")
            print(output_errormessage)
            sys.exit()
        else:
            print(output_message)
    except:
        sys.exit("* Error: Error in CTANOut")
    if verbose:
        print("* Info: CTANOut completed")

# ------------------------------------------------------------------
def func_call_compile():                                                        # function: Compile the generated LaTeX file.
    """Compile the generated LaTeX file."""

    print("-" * 80)
    print("* Info: Compilation")
    for e in [".aux", ".idx", ".ind", ".log", ".ilg", ".pdf", ".out"]:
        remove_LaTeX_file(e)
    print("\n* Info: XeLaTeX")
    if verbose:
        print("* Info: Call:", call_compile)

    try:                                                  
        process_compile1      = subprocess.run(call_compile, capture_output=True, universal_newlines=True)
        compile1_errormessage = process_compile1.stderr
        compile1_message      = process_compile1.stdout
        if len(compile1_errormessage) > 0:
            print("* Error: Error in compilation")
            print(compile1_errormessage)
            sys.exit()
        else:
            if verbose:
                print("* Info: more information in '" + direc + output_name + ".log'\n")
                print("* Info: Compilation OK")
    except:
        if verbose:
            print("* Info: more information in '" + direc + output_name + ".log'")
        sys.exit("* Error: Error in compilation")

# ...................................................................
    print("." * 80)
    print("* Info: XeLaTeX")
    if verbose:
        print("* Info: Call:", call_compile)

    try:                                                  
        process_compile2      = subprocess.run(call_compile, capture_output=True, universal_newlines=True)
        compile2_errormessage = process_compile2.stderr
        compile2_message      = process_compile2.stdout
        if len(compile2_errormessage) > 0:
            print("* Error: Error in compilation:")
            print(compile2_errormessage)
            sys.exit()
        else:
            if verbose:
                print("* Info: more information in '" + direc + output_name + ".log'\n")
                print("* Info: Compilation OK")
    except:
        if verbose:
            print("* Info: more information in '" + direc + output_name + ".log'")
        sys.exit("* Error: Error in compilation")

# ...................................................................
    print("." * 80)
    print("* Info: Makeindex")
    if verbose:
        print("* Info: Call:", call_index)

    try:                                                  
        process_index      = subprocess.run(call_index, capture_output=True, universal_newlines=True)
        index_errormessage = process_index.stderr
        index_message      = process_index.stdout
    except:
        if verbose:
            print("* Info: more information in '" + direc + output_name + ".ilg'\n")
        sys.exit("* Error: Error in Makeindex")
    if verbose:
        print("* Info: more information in '" + direc + output_name + ".ilg'\n")
        print("* Info: Makeindex OK")

# ...................................................................
    print("." * 80)
    print("* Info: XeLaTeX")
    if verbose:
        print("* Info: Call:", call_compile)

    try:                                                  
        process_compile3      = subprocess.run(call_compile, capture_output=True, universal_newlines=True)
        compile3_errormessage = process_compile3.stderr
        compile3_message      = process_compile3.stdout
        if len(compile3_errormessage) > 0:
            print("* Error: Error in compilation:")
            print(compile3_errormessage)
            sys.exit()
        else:
            if verbose:
                print("* Info: more information in '" + direc + output_name + ".log'") 
                print("* Info: result in '" + direc + output_name + ".pdf'\n")
                print("* Info: Compilation OK")
    except:
        if verbose:
            print("* Info: more information in '" + direc + output_name + ".log'")
        sys.exit("* Error: Error in compilation")

# ...................................................................
    for e in [".aux", ".idx", ".ind", ".out"]:
        remove_LaTeX_file(e)

# ------------------------------------------------------------------
def head():                                                                     # function head: show the given options
    """Show the given options."""
    
    print("* Info: CTANLoad+Out")
    if verbose:
        print("* Info: Call:", call)
        if ("-c" in call) or ("--check_integrity" in call): print("  {0:5} {1:55}".format("-c", "(" + integrity_text + ")"))                         # -c
        if ("-f" in call) or ("--download_files" in call):  print("  {0:5} {1:55}".format("-f", "(" + download_text + ")"))                          # -f
        if ("-l" in call) or ("--lists" in call):           print("  {0:5} {1:55}".format("-l", "(" + (lists_text + ")")[0:50] + ellipse))           # -l 
        if ("-mo" in call) or ("--make_output" in call):    print("  {0:5} {1:55}".format("-mo", "(" + (make_output_text + ")")[0:50] + ellipse))    # -mo
        if ("-mt" in call) or ("--make_topics" in call):    print("  {0:5} {1:55}".format("-mt", "(" + (topics_text + ")")[0:50] + ellipse))         # -mt
        if ("-p" in call) or ("--pdf_output" in call):      print("  {0:5} {1:55}".format("-p", "(" + pdf_text + ")"))                               # -p
        if ("-r" in call) or ("--regenerate_pickle_files" in call): print("  {0:5} {1:55}".format("-r", "(" + regenerate_text + ")"))                # -v
        if ("-stat" in call) or ("--statistics" in call):   print("  {0:5} {1:55}".format("-stat", "(" + statistics_text + ")"))                     # -stat
        if ("-v" in call) or ("--verbose" in call):         print("  {0:5} {1:55}".format("-v", "(" + verbose_text + ")"))                           # -v
        if ("-b" in call) or ("--btype" in call):           print("  {0:5} {2:55} {1}".format("-b", btype, "(" + btype_text + ")"))                  # -b
        if ("-d" in call) or ("--directory" in call):       print("  {0:5} {2:55} {1}".format("-d", direc, "(" + direc_text + ")"))                  # -d
        if ("-m" in call) or ("--mode" in call):            print("  {0:5} {2:55} {1}".format("-m", mode, "(" + mode_text + ")"))                    # -m
        if ("-n" in call) or ("--number" in call):          print("  {0:5} {2:55} {1}".format("-n", number, "(" + number_text + ")"))                # -n
        if ("-o" in call) or ("--output" in call):          print("  {0:5} {2:55} {1}".format("-o", args.output_name, "(" + output_text + ")"))      # -o
        if ("-k" in call) or ("--key" in call):             print("  {0:5} {2:55} {1}".format("-k", fold(key), "(" + (key_text + ")")[0:50] + ellipse))  # -k
        if ("-kl" in call) or ("--key_load" in call):       print("  {0:5} {2:55} {1}".format("-k", fold(key_load), "(" + key_load_text + ")"))      # -kl
        if ("-ko" in call) or ("--key_out" in call):        print("  {0:5} {2:55} {1}".format("-k", fold(key_out), "(" + key_out_text + ")"))        # -ko
        if ("-s" in call) or ("--skip" in call):            print("  {0:5} {2:55} {1}".format("-s", skip, "(" + skip_text + ")"))                    # -s
        if ("-t" in call) or ("--template" in call):        print("  {0:5} {2:55} {1}".format("-t", fold(template), "(" + template_text + ")"))      # -t
        if ("-tl" in call) or ("--template_load" in call):  print("  {0:5} {2:55} {1}".format("-tl", template_load, "(" + template_load_text + ")")) # -tl
        if ("-to" in call) or ("--template_out" in call):   print("  {0:5} {2:55} {1}".format("-to", template_out, "(" + template_out_text + ")"))   # -to
        if ("-A" in call) or ("--author_template" in call):       print("  {0:5} {2:55} {1}".format("-A", fold(author_template), "(" + author_template_text + ")"))            # --A
        if ("-Al" in call) or ("-author_load_template" in call):  print("  {0:5} {2:55} {1}".format("-Al", fold(author_load_template), "(" + author_load_template_text + ")")) # -Al
        if ("-Ao" in call) or ("--author_outd_template" in call): print("  {0:5} {2:55} {1}".format("-Ao", fold(author_out_template), "(" + author_out_template_text + ")"))   # -Ao
        print("\n")

        if regeneration: print("* Info: CTANLoad (Regeneration) to be executed")
        if load:         print("* Info: CTANLoad (Load)         to be executed")
        if check:        print("* Info: CTANLoad (Check)        to be executed")
        if output:       print("* Info: CTANOut                 to be executed")
        if compile:      print("* Info: XeLaTeX and MakeIndex   to be executed")
        print("\n")
    
# ------------------------------------------------------------------
def main():                                                                     # main function
    """Main Function"""
    
    print("=" * 80)
    head()
    if regeneration:
        func_call_regeneration()
    if load:
        func_call_load()
    if check:
        func_call_check()
    if output:
        func_call_output()
    if compile:
        if path.exists(direc + output_name + ".tex"):
            func_call_compile()
        else:
            print("* Warning: LaTeX file '{0}' does not exist".format(direc + output_name + ".tex"))
    print("-" * 80)

  
#===================================================================
# Main Part

if __name__ == "__main__":
    main()
else:
    print("- Error: tried to use the program indirectly")
