#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANLoad+Out.py
# (C) Günter Partosch, 2021

# History:
# 2021-05-01: 0.1: start
# 2021-05-04: 0.9: first working version
# 2021-05-24: 1.0: program completed
# 2021-05-28: 1.1: compilation enabled
# 2021-05-31: 1.2: some improvements (calls, compilation)

# Problems/Plans:
# * -b nur für -m bib zulassen
# * -mt nur für -m latex zulassen
# + für ctanout anderer Default für -t (x)
# + anderes Trennzeichen für Compilation und Makeindex (x)
# + prüfen, ob ctanload -l -c aufgerufen werden muss (wenn CTANOut folgt)
# + ist -c gefährlich?

# ------------------------------------------------------------------
# Moduls needed

import argparse                    # argument parsing
import sys                         # system calls
import platform                    # get OS informations
import subprocess                  # handling of sub-processes
import re                          # regular expression

# ------------------------------------------------------------------
# Usage
#
# usage: CTANLoad+Out.py [-h] [-a] [-b {@online,@software,@misc,@ctan,@www}] [-c] [-d DIREC] [-f] [-k FILTER_KEY] [-l]
#                        [-m {LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,biblatex,bib,Excel,excel}] [-mo] [-mt]
#                        [-n NUMBER] [-o OUTPUT_NAME] [-p] [-s SKIP] [-stat] [-t TEMPLATE] [-tl TEMPLATE_LOAD]
#                        [-to TEMPLATE_OUT] [-V] [-v]
# 
# [CTANLoad+Out.py; Version: 1.2 (2021-05-31)] Combine the tasks of CTANLoad (Load XLM and PDF documentation files from
# CTAN a/o generate some special lists, and prepare data for CTANOut) and CTANOut (Convert CTAN XLM package files to some formats)
# 
# Optional parameters:
#   -h, --help            show this help message and exit
#   -a, --author          Show author of the program and exit
#   -b {@online,@software,@misc,@ctan,@www}, --btype {@online,@software,@misc,@ctan,@www}
#                         Type of BibLaTex entries to be generated (valid only for '-m BibLaTeX'/'--mode BibLaTeX'); Default:
#   -c, --check_integrity
#                         Flag: Check the integrity of the 2nd .pkl file; Default: False
#   -d DIREC, --directory DIREC
#                         Directory for input and output file; Default: ./
#   -f, --download_files  Flag: Download associated documentation files (PDF) ; Default: False
#   -k FILTER_KEY, --key FILTER_KEY
#                         Template for output filtering on the base of keys; Default: ^.+$
#   -l, --lists           Flag: Generate some special lists and prepare files for CTANOut; Default: False
#   -m {LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,biblatex,bib,Excel,excel},
#                         --mode {LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,biblatex,bib,Excel,excel}
#                         Target format; Default: RIS
#   -mo, --make_output    Flag: generate output (RIS, LaTeX, BibLaTeX, Excel, plain) via CTANOut; Default: False
#   -mt, --make_topics    Flag: generate topic lists (meaning of topics + cross-reference (topics/packages, authors/packages);
#                         valid only for '-m
#                         LaTeX'/'--mode LaTeX'; Default: False
#   -n NUMBER, --number NUMBER
#                         Maximum number of file downloads; Default: 250
#   -o OUTPUT_NAME, --output OUTPUT_NAME
#                         Generic name for output files (without extensions); Default: all
#   -p, --pdf_output      Flag: Generate PDF output; Default: False
#   -s SKIP, --skip SKIP  Skip specified CTAN fields; Default: []
#   -stat, --statistics   Flag: Print statistics on terminal; Default: False
#   -t TEMPLATE, --template TEMPLATE
#                         Template for package names (in CTANLoad and CTANOut); Default:
#   -tl TEMPLATE_LOAD, --template_load TEMPLATE_LOAD
#                         Template for package names (in CTANLoad and CTANOut); Default:
#   -to TEMPLATE_OUT, --template_out TEMPLATE_OUT
#                         Template for package names (in CTANLoad and CTANOut); Default:
#   -V, --version         Show version of the program and exit
#   -v, --verbose         Flag: Output is verbose; Default: False


#===================================================================
# Settings

programname       = "CTANLoad+Out.py"
programversion    = "1.2"
programdate       = "2021-05-31"
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
call_check        = empty
call_load         = empty
call_output       = empty
call_compile      = empty
call_index        = empty

err_mode          = "Warning: '{0} {1}' changed to '{2}'\n"

# ------------------------------------------------------------------
# Texts for argument parsing and help

author_text        = "Show author of the program and exit."
btype_text         = "Type of BibLaTex entries to be generated [valid only for '-m BibLaTeX'/'--mode BibLaTeX']"
direc_text         = "Directory for input and output file"
key_text           = "Template for output filtering on the base of keys"
mode_text          = "Target format"
number_text        = "Maximum number of file downloads"
output_text        = "Generic name for output files [without extensions]"
program_text       = "Combine the tasks of CTANLoad [Load XLM and PDF documentation files from CTAN a/o generate some special lists, and prepare data for CTANOut] and CTANOut [Convert CTAN XLM package files to some formats]."
skip_text          = "Skip specified CTAN fields."
template_text      = "Template for package names [in CTANLoad and CTANOut]"
template_out_text  = "Template for package names in CTANOut"
template_load_text = "Template for package names in CTANLoad"
version_text       = "Show version of the program and exit."

download_text      = "Flag: Download associated documentation files [PDF]."
integrity_text     = "Flag: Check the integrity of the 2nd .pkl file."
lists_text         = "Flag: Generate some special lists and prepare files for CTANOut."
make_output_text   = "Flag: Generate output [RIS, LaTeX, BibLaTeX, Excel, plain] via CTANOut."
pdf_text           = "Flag: Generate PDF output."
statistics_text    = "Flag: Print statistics on terminal."
topics_text        = "Flag: Generate topic lists [meaning of topics + cross-reference (topics/packages, authors/packages); only for -m LaTeX])."
verbose_text       = "Flag: Output is verbose."

# ------------------------------------------------------------------
# Defaults/variables for argparse

download_default      = False            # flag: download PDF files
integrity_default     = False            # flag: integrity check
lists_default         = False            # flag: generate special lists
make_output_default   = False            # Flag: generate output (RIS, LaTeX, BibLaTeX, Excel, plain)
make_topics_default   = False            # flag: make topics output
pdf_default           = False            # flag: produce PDF output
statistics_default    = False            # flag: output statistics
verbose_default       = False            # flag: output is verbose

btype_default         = empty            # default for option -b (BibLaTeX entry type)
filter_key_default    = """^.+$"""       # default for option -k
mode_default          = "RIS"            # default for option -m 
number_default        = 250              # default for option -n (maximum number of files to be loaded)
output_name_default   = "all"            # default for option -o (generic file name)
skip_default          = "[]"             # default for option -s
template_default      = empty            # default for option -t
template_load_default = template_default # default for option -tl 
template_out_default  = """^.+$"""       # default for option -to

act_direc             = "."

if operatingsys == "Windows":    
    direc_sep      = "\\"
else:
    direc_sep      = "/"
    
direc_default        = act_direc + direc_sep # default for -d (output directory)


#===================================================================
# Parsing the arguments

parser = argparse.ArgumentParser(description = "[" + programname + "; " + "Version: " + programversion + " (" + programdate + ")] " + program_text)
parser._optionals.title   = 'Optional parameters'

parser.add_argument("-a", "--author",                      # Parameter -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = programauthor + " (" + authoremail + ", " + authorinstitution + ")")

parser.add_argument("-b", "--btype",                       # Parameter -b/--btype
                    help    = btype_text + "; Default: " + "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan", "@www"],
                    dest    = "btype",
                    default = btype_default)

parser.add_argument("-c", "--check_integrity",             # Parameter -i/--integrity
                    help    = integrity_text + "; Default: " + "%(default)s",
##                    help    = argparse.SUPPRESS,
                    action  = "store_true",
                    default = integrity_default)

parser.add_argument("-d", "--directory",                   # Parameter -d/--directory
                    help    = direc_text + "; Default: " + "%(default)s",
                    dest    = "direc",
                    default = direc_default)

parser.add_argument("-f", "--download_files",              # Parameter -f/--download_files
                    help    = download_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = download_default)

parser.add_argument("-k", "--key",                         # Parameter -k/--key
                    help    = key_text + "; Default: " + "%(default)s",
                    dest    = "filter_key",
                    default = filter_key_default)

parser.add_argument("-l", "--lists",                       # Parameter -l/--lists
                    help = lists_text + "; Default: " + "%(default)s",
                    action = "store_true",
                    default = lists_default)

parser.add_argument("-m", "--mode",                        # Parameter -m/--mode
                    help    = mode_text + "; Default: " + "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "ris", "plain", "txt", "BibLaTeX", "biblatex", "bib", "Excel", "excel"],
                    dest    = "mode",
                    default = mode_default)

parser.add_argument("-mo", "--make_output",                # Parameter -mo/--make_output
                    help    = make_output_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_output_default)

parser.add_argument("-mt", "--make_topics",                # Parameter -mt/--make_topics
                    help    = topics_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_topics_default)

parser.add_argument("-n", "--number",                      # Parameter -n/--number
                    help    = number_text + "; Default: " + "%(default)s",
                    dest    = "number",
                    default = number_default)

parser.add_argument("-o", "--output",                      # Parameter -o/--output
                    help    = output_text + "; Default: " + "%(default)s",
                    dest    = "output_name",
                    default = output_name_default)

parser.add_argument("-p", "--pdf_output",                  # Parameter -p/--pdf_output
                    help    = pdf_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = pdf_default)

parser.add_argument("-s", "--skip",                        # Parameter -s/--skip
                    help    = skip_text + "; Default: " + "%(default)s",
                    dest    = "skip",
                    default = skip_default)

parser.add_argument("-stat", "--statistics",               # Parameter -stat/--statistics
                    help    = statistics_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics_default)

parser.add_argument("-t", "--template",                    # Parameter -t/--template
                    help    = template_text + "; Default: " + "%(default)s",
                    dest    = "template",
                    default = template_default)

parser.add_argument("-tl", "--template_load",              # Parameter -tl/--template_load
                    help    = template_load_text + "; Default: " + "%(default)s",
                    dest    = "template_load",
                    default = template_load_default)

parser.add_argument("-to", "--template_out",               # Parameter -to/--template_out
                    help    = template_out_text + "; Default: " + "%(default)s",
                    dest    = "template_out",
                    default = template_out_default)

parser.add_argument("-V", "--version",                     # Parameter -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + programversion + " (" + programdate + ")")

parser.add_argument("-v", "--verbose",                     # Parameter -v/--verbose
                    help = verbose_text + "; Default: " + "%(default)s",
                    action = "store_true",
                    default = verbose_default)

# ------------------------------------------------------------------
# Getting parsed values

args            = parser.parse_args()

btype           = args.btype                  # Parameter -b
direc           = args.direc                  # Parameter -d
download        = args.download_files         # Parameter -f
filter_key      = args.filter_key             # Parameter -k
integrity       = args.check_integrity        # Parameter -c
lists           = args.lists                  # Parameter -l
make_output     = args.make_output            # Parameter -mo
make_topics     = args.make_topics            # Parameter -mt
mode            = args.mode                   # Parameter -m
number          = int(args.number)            # Parameter -n
output_name     = args.output_name            # Parameter -o
pdf_output      = args.pdf_output             # Parameter -p
skip            = args.skip                   # Parameter -s
statistics      = args.statistics             # Parameter -stat
template        = args.template               # Parameter -t
template_load   = args.template_load          # Parameter -tl
template_out    = args.template_out           # Parameter -to
verbose         = args.verbose                # Parameter -v

# ------------------------------------------------------------------
# Correct direc

direc = direc.strip()                         # correct directory name (-d)
if direc[len(direc) - 1] != direc_sep:
    direc += direc_sep
    

#===================================================================
# check values

#        load  check output compile
# -a     x     x     x      -
# -b     -     -     x      -
# -c     -     x     -      -
# -d     x     -     x      x
# -f     x     x     -      -
# -k     -     -     x      -
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

if mode in ["LaTeX", "latex", "tex"]:
    mode = "latex"
elif mode in ["BibLaTeX", "biolatex", "bib"]:
    mode = "biblatex"
elif mode in ["Excel", "excel", "tsv"]:
    mode = "excel"
elif mode in ["RIS", "ris"]:
    mode = "ris"
elif mode in ["plain", "txt"]:
    mode = "plain"
else:
    pass

if ("-p" in call) or ("-mt" in call):
    if mode != "latex":
        if verbose:
            print(err_mode.format('-m', mode, '-m latex'))
    call.append("-m");
    mode = "latex"
if "-b" in call:
    if mode != "biblatex":
        if verbose:
            print(err_mode.format('-m', mode, '-m biblatex'))
    call.append("-m");
    mode = "biblatex"
    
# ------------------------------------------------------------------
# set load, check, compile and output

callx       = set(call[1:])

set_load    = {'-f', '-n', '--download_files', '--number', '-t', '--template', '-tl', '--template_load'}
set_check   = {'-l', '-c', '--lists', '--check_integrity'}
set_output  = {'-b', '-k', '-m', '-mt', '-p', '-s', '--btype', '--key', '--mode', '--make_topics', '--pdf_output', '--skip', 
               '-t', '--template', '-mo', 'make_output', '-to', '--template_out'}
set_compile = {'-p', '--pdf_output'}

load        = callx & set_load    != empty_set
output      = callx & set_output  != empty_set
compile     = callx & set_compile != empty_set
check       = callx & set_check   != empty_set


#===================================================================
# Construct the calls

t  = (template      != template_default)
tl = (template_load != template_load_default)
to = (template_out  != template_out_default)

# ------------------------------------------------------------------
# call_load

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

# ------------------------------------------------------------------
# call_check

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
if filter_key != filter_key_default:                  # -k
    call_output.append("-k")
    call_output.append(filter_key)
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

# ------------------------------------------------------------------
# call_compile + call_index

direc_comp   = re.sub(r"\\", "/", direc)
call_compile = latex_processor + space + direc_comp + output_name  + ".tex"
call_index   = index_processor + space + direc_comp + output_name  + ".idx" + space + "-o " + space + direc_comp + output_name  + ".ind"


#===================================================================
# calls

# ------------------------------------------------------------------
# call ctanload+out

def head():
    """Report the given arguments."""
    
    print("+ CTANLoad+Out")
    print("+ Call:", call)
    if verbose:
        if ("-b" in call) or ("--btype" in call):           print("  {0:5} {2:55} {1}".format("-b", btype, "(" + btype_text + ")"))             # -b
        if ("-c" in call) or ("--check_integrity" in call): print("  {0:5} {1:55}".format("-c", "(" + integrity_text + ")"))                    # -c
        if ("-d" in call) or ("--directory" in call):       print("  {0:5} {2:55} {1}".format("-d", direc, "(" + direc_text + ")"))             # -d
        if ("-f" in call) or ("--download_files" in call):  print("  {0:5} {1:55}".format("-f", "(" + download_text + ")"))                     # -f
        if ("-k" in call) or ("--key" in call):             print("  {0:5} {2:55} {1}".format("-k", filter_key, "(" + key_text + ")"))          # -k
        if ("-l" in call) or ("--lists" in call):           print("  {0:5} {1:55}".format("-l", "(" + lists_text + ")"))                        # -l 
        if ("-m" in call) or ("--mode" in call):            print("  {0:5} {2:55} {1}".format("-m", mode, "(" + mode_text + ")"))               # -m
        if ("-mo" in call) or ("--make_output" in call):    print("  {0:5} {1:55}".format("-mo", "(" + make_output_text + ")"))                 # -mo
        if ("-mt" in call) or ("--make_topics" in call):    print("  {0:5} {1:55}".format("-mt", "(" + topics_text + ")"))                      # -mt
        if ("-n" in call) or ("--number" in call):          print("  {0:5} {2:55} {1}".format("-n", number, "(" + number_text + ")"))           # -n
        if ("-o" in call) or ("--output" in call):          print("  {0:5} {2:55} {1}".format("-o", args.output_name, "(" + output_text + ")")) # -o
        if ("-p" in call) or ("--pdf_output" in call):      print("  {0:5} {1:55}".format("-p", "(" + pdf_text + ")"))                          # -p
        if ("-s" in call) or ("--skip" in call):            print("  {0:5} {2:55} {1}".format("-s", skip, "(" + skip_text + ")"))               # -s
        if ("-stat" in call) or ("--statistics" in call):   print("  {0:5} {1:55}".format("-stat", "(" + statistics_text + ")"))                # -stat
        if ("-t" in call) or ("--template" in call):        print("  {0:5} {2:55} {1}".format("-t", template, "(" + template_text + ")"))       # -t
        if ("-tl" in call) or ("--template_load" in call):  print("  {0:5} {2:55} {1}".format("-tl", template_load, "(" + template_load_text + ")"))  # -tl
        if ("-to" in call) or ("--template_out" in call):   print("  {0:5} {2:55} {1}".format("-to", template_out, "(" + template_out_text + ")"))    # -to
        if ("-v" in call) or ("--verbose" in call):         print("  {0:5} {1:55}".format("-v", "(" + verbose_text + ")"))                      # -v
        print("\n")

        if load:    print("+ CTANLoad to be executed")
        if check:   print("+ CTANLoad (Check) to be executed")
        if output:  print("+ CTANOut to be executed")
        if compile: print("+ XeLaTeX and MakeIndex to be executed")
        print("\n")

# ------------------------------------------------------------------
def func_call_load():
    """CTANLoad is processed."""

    print("-" * 80)
    print("+ CTANLoad")
    print("+ Call:", call_load[1:])
    try:                                                  
        process_load      = subprocess.run(call_load, capture_output=True, encoding="utf8", universal_newlines=True)
        load_message      = process_load.stdout
        load_errormessage = process_load.stderr
        if len(load_errormessage) > 0:
            print("+ Error:")
            print(load_errormessage)
            sys.exit()
        else:
            if verbose:
                print(load_message)
                print("+ OK")
    except:
        print("+ Error in CTANLoad")
        sys.exit()

# ------------------------------------------------------------------
def func_call_check():
    """CTANLoad (Check) is processed."""

    print("-" * 80)
    print("+ CTANLoad, check")
    print("+ Call:", call_check[1:])
    try:                                                  
        process_check      = subprocess.Popen(call_check, stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf8", universal_newlines=True)
        check_errormessage = process_check.stderr.read()
        check_message      = process_check.stdout.read()
        if len(check_errormessage) > 0:
            print("+ Error:")
            print(check_errormessage)
            sys.exit()
        else:
            if verbose:
                print(check_message)
                print("+ OK")
        process_check.communicate()
    except:
        print("+ Error in CTANLoad")
        sys.exit()

# ------------------------------------------------------------------
def func_call_output():
    """CTANOut is processed."""
    
    print("-" * 80)
    print("+ CTANOut")
    print("+ Call:", call_output[1:])
    try:                                                  
        process_output      = subprocess.run(call_output, capture_output=True, encoding="utf8", universal_newlines=True)
        output_errormessage = process_output.stderr
        output_message      = process_output.stdout
        if len(output_errormessage) > 0:
            print("+ Error:")
            print(output_errormessage)
            sys.exit()
        else:
            if verbose:
                print(output_message)
                print("+ OK")
    except:
        print("+ Error in CTANOut")
        sys.exit()

# ------------------------------------------------------------------
def func_call_compile():
    """Compiles the generated LaTeX file."""

    print("-" * 80)
    print("+ Compilation")
    print("+ XeLaTeX")
    print("+ Call:", call_compile)

    try:                                                  
        process_compile1      = subprocess.run(call_compile, capture_output=True, encoding="utf8", universal_newlines=True)
        compile1_errormessage = process_compile1.stderr
        compile1_message      = process_compile1.stdout
        if len(compile1_errormessage) > 0:
            print("+ Error:")
            print(compile1_errormessage)
            sys.exit()
        else:
            if verbose:
                print("+ more information in", direc_comp + output_name + ".log")
                print("\n+ OK")
    except:
        print("+ Error in compilation")
        print("+ more information in", direc_comp + output_name + ".log")
        sys.exit()

# ...................................................................
    print("." * 80)
    print("+ XeLaTeX")
    print("+ Call:", call_compile)

    try:                                                  
        process_compile2      = subprocess.run(call_compile, capture_output=True, encoding="utf8", universal_newlines=True)
        compile2_errormessage = process_compile2.stderr
        compile2_message      = process_compile2.stdout
        if len(compile2_errormessage) > 0:
            print("+ Error:")
            print(compile2_errormessage)
            sys.exit()
        else:
            if verbose:
                print("+ more information in", direc_comp + output_name + ".log")
                print("\n+ OK")
    except:
        print("+ Error in compilation")
        print("+ more information in", direc_comp + output_name + ".log")
        sys.exit()

# ...................................................................
    print("." * 80)
    print("+ Makeindex")
    print("+ Call:", call_index)

    try:                                                  
        process_index      = subprocess.run(call_index, capture_output=True, encoding="utf8", universal_newlines=True)
        index_errormessage = process_index.stderr
        index_message      = process_index.stdout
##        if len(index_errormessage) > 0:
##            print("+ Error:")
##            print(index_errormessage)
##            sys.exit()
##        else:
##            print(index_message)
##            print("+ OK")
    except:
        print("+ Error in makeindex")
        sys.exit()
    if verbose:
        print("+ more information in", direc_comp + output_name + ".ilg")
        print("\n+ OK")

# ...................................................................
    print("." * 80)
    print("+ XeLaTeX")
    print("+ Call:", call_compile)

    try:                                                  
        process_compile3      = subprocess.run(call_compile, capture_output=True, encoding="utf8", universal_newlines=True)
        compile3_errormessage = process_compile3.stderr
        compile3_message      = process_compile3.stdout
        if len(compile3_errormessage) > 0:
            print("+ Error:")
            print(compile3_errormessage)
            sys.exit()
        else:
            if verbose:
                print("+ more information in", direc_comp + output_name + ".log") 
                print("+ result in", direc_comp + output_name + ".pdf")
                print("\n+ OK")
    except:
        print("+ Error in compilation")
        print("+ more information in", direc_comp + output_name + ".log")
        sys.exit()

# ------------------------------------------------------------------
def main():
    """Main Function"""
    print("=" * 80)
    head()
    if load:
        func_call_load()
    if check:
        func_call_check()
    if output:
        func_call_output()
    if compile:
        func_call_compile()
    print("=" * 80)

  
###===================================================================
### Main Part

if __name__ == "__main__":
    main()
