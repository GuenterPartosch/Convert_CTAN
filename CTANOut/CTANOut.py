#!/usr/bin/python
# -*- coding: utf-8 -*-

# CTANOut.py
# (C) Günter Partosch, 2019/2020

# Problem:
# - Ausgabe des Namens, wenn givenname fehlt
# - year noch besser extrahieren
# - Idee: Klassenkonzept für die Ausgabe: für jeden Ausgabetyp eine eigene Klasse
# - bei BibLaTeX: BibTeX-Kürzel aus Namen + Jahr

# ------------------------------------------------------------------
# Usage

# usage: CTANOut.py [-h] [-a] [-V] [-b {@online,@software,@misc,@ctan}]
#                    [-d DIREC] [-k FILTER_KEY]
#                    [-m {LaTeX,RIS,plain,BibLaTeX,Excel}] [-o OUT_FILE]
#                    [-s SKIP] [-t NAME_TEMPLATE] [-mt] [-stat] [-v]
# 
# [CTANOut.py; Version: 1.64 (2020-07-14)] convert CTAN XLM package files to
# LaTeX, RIS, plain, BibLaTeX, Excel (tab separated)
# 
# Options:
#   -h, --help            show this help message and exit
#   -a, --author          show author of the program and exit
#   -V, --version         show version of the program and exit
#   -b {@online,@software,@misc,@ctan}, --btype {@online,@software,@misc,@ctan,@www}
#                         valid only for '-m BibLaTeX'/'--mode BibLaTeX': type
#                         of BibLaTex entries to be generated; Default:
#   -d DIREC, --directory DIREC
#                         directory for input and output files; Default: ./
#   -k FILTER_KEY, --key FILTER_KEY
#                         template for output filtering on the base of keys;
#                         Default: ^.+$
#   -m {LaTeX,RIS,plain,BibLaTeX,Excel}, --mode {LaTeX,RIS,plain,BibLaTeX,Excel}
#                         target format; Default: RIS
#   -o OUT_FILE, --output OUT_FILE
#                         generic name for output files (without extensions);
#                         Default: all
#   -s SKIP, --skip SKIP  skip specified CTAN fields; Default: []
#   -t NAME_TEMPLATE, --template NAME_TEMPLATE
#                         template for package names; Default: ^.+$
#   -mt, --make_topics    valid only for '-m LaTeX'/'--mode LaTeX': generate topic
#                         lists (meaning of topics + cross-reference
#                         (topics/packages, authors/packages); Default: False
#   -stat, --statistics   print statistics on terminal; Default: False
#   -v, --verbose         verbose output; Default: False

# ------------------------------------------------------------------
# Examples

# CTANOut
#     RIS is output format (default)
#     all.ris is output file
#     no statistics
#     without verbose output
#
# CTANOut -v
#     as bove
#     with verbose output (each processed package is shown)
#
# CTANOut -v -stat
#     as above
#     but additionallay with statistics
#
# CTANOut -m BibLaTeX
#     BibLaTeX is output format
#     no statistics
#     without verbose output
#
# CTANOut -m BibLaTeX -b @online -v
#     as above
#     but now with verbose output and @online for BibLaTeX type
#
# CTANOut -m BibLaTeX -b @online -s [texlive,license,miktex] -v -stat
#     as above
#     with statistics
#     skipped CTAN fields: texlive, license, and miktex
#
# CTANOut -m LaTeX -mt -v -stat
#     LaTeX is output format
#     special topic lists are generated
#     with statistics and verbose output
#
# CTANOut -m LaTeX -k LaTeX -mt
#     LaTeX is output format
#     special topic lists are generated
#     package names are filtered by key template "LaTeX"
#
# CTANOut -m LaTeX -t "l3|latex|ltx" -mt -v
#     processed packages: l3, latex, and ltx
#     LaTeX is output format
#     special topic lists are generated
#     package names are filtered by name template "LaTeX"
#
# CTANOut -m plain -v -stat -o myfile -s "[texlive,license,miktex]"
#     plain text is output format
#     myfile.txt is the name for the output file
#     skipped CTAN fields: texlive, license, and miktex
#     with statistics and verbose output

# ------------------------------------------------------------------
# Messages

# Fatal Error
# + pickle file 'CTAN.pkl' not found

# Information
# + list with authors and related packages (cross-reference list) created
# + list with topics and related packages (cross-reference list) created
# + packages processed
# + program call: CTANOut.py
# + program successfully completed
# + statistics written
# + topic list created

# Warnings
# + '-mt'/'--make_topics' valid only for '-m LaTeX'/'--mode LaTeX'; therefore ignored
# + '-b'/'--btype' valid only for '-m BibLaTeX'/'--mode BibLaTeX'; therefore ignored
# + XML file for package 'package' not found
# + key 'key' not found
# + no correct XML file for any specified package found

# ------------------------------------------------------------------
# Moduls needed

import xml.etree.ElementTree as ET              # XML processing
import pickle                                   # to read pickle data, time measure
import time                                     # to get time/date of a file
import re                                       # regular expression
import argparse                                 # argument parsing
import sys                                      # system calls
import platform                                 # get OS informations
import os                                       # OS relevant routines


#===================================================================
# Settings

programname       = "CTANOut.py"
programversion    = "1.64"
programdate       = "2020-07-14"
programauthor     = "Günter Partosch"
documentauthor    = "Günter Partosch"
authorinstitution = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"
authoremail       = "Guenter.Partosch@hrz.uni-giessen.de"
documenttitle     = "The CTAN book -- Packages on CTAN"
documentsubtitle  = "Collected, prepared and selected with the aid of the program "

operatingsys      = platform.system()           # operating system
call              = sys.argv                    # actual program call
calledprogram     = sys.argv[0]                 # name of program in call

# ------------------------------------------------------------------
# Global settings

ctanUrl           = "https://ctan.org"          # head of a CTAN url
ctanUrl2          = ctanUrl + "/tex-archive"    # head of another CTAN url
ctanUrl3          = ctanUrl2 + "/install"       # head of another CTAN url
ctanUrl4          = ctanUrl + "/pkg/"           # head of another CTAN url
labelwidth        = len("Documentation: ")      # width of the labels for LaTeX
actDate           = time.strftime("%Y-%m-%d")   # actual date of program execution
actTime           = time.strftime("%X")         # actual time of program execution

pickle_name1      = "CTAN.pkl"
pickle_name2      = "CTAN2.pkl"
list_info_files   = True                        # switch for RIS/BibLaTeX: XML_toc is to be proceed
info_files        = ""                          # for BibLaTeX: collector for info file names
ext               = ".xml"                      # file name extension for downloaded info files

maxcaptionlength  = 65                          # for LaTeX: max length for header lines
fieldwidth        = 10                          # for BibLaTeX: width of the field labels 

if operatingsys == "Windows":
    direc   = "./"
else:
    direc   = "./"

# ------------------------------------------------------------------
# Collect infos which cannot be output in another way

notice          = ""                            # collecting infos
author_str      = ""                            # collecting authors of a package
year_str        = ""                            # collecting year informations
version_str     = ""                            # collecting version strings
counter         = 1                             # counts packages
left            = 35                            # width of labels in verbose output

# ------------------------------------------------------------------
# Texts for argument parsing

author_text     = "show author of the program and exit"
direc_text      = "directory for input and output file"
key_text        = "template for output filtering on the base of keys"
mode_text       = "target format"
out_file        = "all"
out_text        = "generic name for output files (without extensions)"
program_text    = "convert CTAN XLM package files to LaTeX, RIS, plain, BibLaTeX, Excel (tab separated)"
skip_text       = "skip specified CTAN fields"
template_text   = "template for package names"
verbose_text    = "Flag: verbose output"
statistics_text = "Flag: print statistics on terminal"
version_text    = "Flag: show version of the program and exit"

btype_text      = "valid only for '-m BibLaTeX'/'--mode BibLaTeX': type of BibLaTex entries  to be generated"
topics_text     = "valid only for '-m LaTeX'/'--mode LaTeX': generate topic lists (meaning of topics + cross-reference (topics/packages, authors/packages)"

# ------------------------------------------------------------------
# Defaults for argument parsing and further processing

authorexists    = False                     # default for a global flag
btypedefault    = ""                        # default for BibLaTeX type
make_topics     = False                     # default for topics output
modedefault     = "RIS"                     # default for mode
name_template   = """^.+$"""                # default for file name template
out_default     = "all"                     # default for out file
filter_key      = """^.+$"""                # default for option -k
skip_default    = "[]"                      # default for option -s
verbose         = False                     # default for global flag: verbose output
statistics      = False                     # default for global flag: statistics output
default_text    = "no text"                 # default text for elements without embedded text
empty           = ""                        # default text when a not embedded text is required but not found
userunknown     = "N. N."                   # default text for elements without a correct author
package_id      = ""                        # ID of a package

name_default    = name_template             # copy of name_template
filter_default  = filter_key                # copy of filter_key

# ------------------------------------------------------------------
# Strings for Excel output

s_also          = ""                        # Element also
s_authorref     = ""                        # Element authorref
s_contact       = ""                        # Element contact
s_copyright     = ""                        # Element copyright
s_ctan          = ""                        # Element ctan
s_documentation = ""                        # Element documentation
s_home          = ""                        # Element home
s_id            = ""                        # Element id
s_install       = ""                        # Element install
s_keyval        = ""                        # Element keyval
s_license       = ""                        # Element license
s_miktex        = ""                        # Element miktex
s_texlive       = ""                        # Element texlive
s_version       = ""                        # Element version

# ------------------------------------------------------------------
# python directories and lists

languagecodes   = {"ar":"Arabic", "ar-dz":"Arabic (Algeria)", "bg":"Bulgerian", "bn":"Bengali",
                   "ca":"Catalan", "cs":"Czech", "da":"Danish", "de":"German", "de-de":"German",
                   "el":"Greek", "en":"English", "eo":"Esperanto", "en-gb":"British", "es":"Spanish",
                   "es-ve":"Spanish (Venezuela)", "et":"Estonian", "eu":"Basque", "fa":"Farsi",
                   "fa-ir":"Farsi (Iran)", "fi":"Finnish", "fr":"French", "hr":"Croatian",
                   "hu":"Hungarian", "hy":"Armenian", "it":"Italian", "ja":"Japanese",
                   "ka":"Georgian", "ko":"Korean", "lv":"Latvian", "mn":"Mongolian", "nl":"Dutch",
                   "nn-no":"Nynorsk", "pl":"Polish", "pt":"Portuguese",
                   "pt-br":"Portuguese (Brazilia)", "ru":"Russian", "sk":"Slovak", "sr":"Serbian",
                   "sr-sp":"Serbian", "th":"Thai", "tr":"Turkish", "uk":"Ukrainian", "vi":"Vietnamese",
                   "zh":"Chinese"}
usedTopics      = {}                        # python directory: collects used topics for all packages
usedPackages    = []                        # python list: collects used packages
usedAuthors     = {}                        # python directory: collects used authors for all packages
XML_toc         = {}                        # python directory: 

# usedTopics: python directory (unsorted)
#   each element: <key for topic>:<number>
# usedPackages: python list
#   each element: <package name>
# usedAuthors: python directory (unsorted)
#   each element: <key for author>:<tuple with givenname and familyname>


#===================================================================
# Parsing the arguments

parser = argparse.ArgumentParser(description = "[" + programname + "; " + "Version: " + programversion + " (" + programdate + ")] " + program_text)
parser._positionals.title = 'Positional parameters'
parser._optionals.title   = 'Options'

parser.add_argument("-a", "--author",       # Parameter -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = programauthor + " (" + authoremail + ", " + authorinstitution + ")")

parser.add_argument("-V", "--version",      # Parameter -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + programversion + " (" + programdate + ")")

parser.add_argument("-b", "--btype",        # Parameter -b/--btype
                    help    = btype_text + "; Default: " + "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan", "@www"],
                    dest    = "btype",
                    default = btypedefault)

parser.add_argument("-d", "--directory",    # Parameter -d/--directory
                    help    = direc_text + "; Default: " + "%(default)s",
                    dest    = "direc",
                    default = direc)

parser.add_argument("-k", "--key",          # Parameter -k/--key
                    help    = key_text + "; Default: " + "%(default)s",
                    dest    = "filter_key",
                    default = filter_key)

parser.add_argument("-m", "--mode",         # Parameter -m/--mode
                    help    = mode_text + "; Default: " + "%(default)s",
                    choices = ["LaTeX", "latex", "RIS", "plain", "BibLaTeX", "biblatex", "ris", "Excel"],
                    dest    = "mode",
                    default = modedefault)

parser.add_argument("-o", "--output",       # Parameter -o/--output
                    help    = out_text + "; Default: " + "%(default)s",
                    dest    = "out_file",
                    default = out_default)

parser.add_argument("-s", "--skip",         # Parameter -s/--skip
                    help    = skip_text + "; Default: " + "%(default)s",
                    dest    = "skip",
                    default = skip_default)

parser.add_argument("-t", "--template",     # Parameter -t/--template
                    help    = template_text + "; Default: " + "%(default)s",
                    dest    = "name_template",
                    default = name_template)

parser.add_argument("-mt", "--make_topics", # Parameter -mt/--make_topics
                    help    = topics_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_topics)

parser.add_argument("-stat", "--statistics",# Parameter -stat/--statistics
                    help    = statistics_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics)

parser.add_argument("-v", "--verbose",      # Parameter -v/--verbose
                    help    = verbose_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = verbose)

args          = parser.parse_args()

btype         = args.btype                  # Parameter -b
direc         = args.direc                  # Parameter -d
make_topics   = args.make_topics            # Parameter -mt
mode          = args.mode                   # Parameter -m
name_template = args.name_template          # Parameter -t
out_file      = args.out_file               # Parameter -o
filter_key    = args.filter_key             # Parameter -k
skip          = args.skip                   # Parameter -s
verbose       = args.verbose                # Parameter -v
statistics    = args.statistics             # Parameter -stat

if (btype == "") and (mode == "BibLaTeX"):  # for BibLaTeX: btype is set
    btype = "@online"                       #   btype is reset
if mode == "latex":                         # -m latex in call
    mode = "LaTeX"                          #   mode is reset
if mode == "ris":                           # -m ris in call
    mode = "RIS"                            #   mode is reset 
if mode == "biblatex":                      # -m biblatex in call
    mode = "BibLaTeX"                       #   mode is reset

# pre-compiled regular expressions
p2            = re.compile(name_template)   # regular expression based on -t
p3            = re.compile(filter_key)      # regular expression based on -k


#===================================================================
# Other settings

# ------------------------------------------------------------------
# Full name for the output file (with extensions)

if mode in ["LaTeX"]:                       # LaTeX
    out_file = out_file + ".tex" 
elif mode in ["RIS"]:                       # RIS
    out_file = out_file + ".ris"
elif mode in ["plain"]:                     # plain
    out_file = out_file + ".txt"
elif mode in ["Excel"]:                     # Excel
    out_file = out_file + ".csv"
elif mode in ["BibLaTeX"]:                  # BibLaTeX
    out_file = out_file + ".bib"

out = open(direc + out_file, encoding="utf-8", mode="w")

# ------------------------------------------------------------------
# Only for LaTeX (header of the LaTeX file)

if mode in ["LaTeX"]:                       # only for LaTeX
    classoptions = """                      
paper    = a4,    % paper A4
fontsize = 11pt,  % font size
parskip  = half,  % half parskip
index    = totoc, % index in TOC
headings = small, % small headers
DIV      = 12     % 12-strip layout"""
    usepkg  = """
\\usepackage[english]{babel}             % Language support
\\usepackage{fontspec}                   % font specification
\\usepackage{makeidx}                    % index generation
\\usepackage{lmodern}                    % font lmodern
\\usepackage[colorlinks=true]{hyperref}  % hypertext structures\n
\\newcommand{\inp}[1]{\\IfFileExists{#1}{\\input{#1}}{}}\n
\\makeindex\n"""
    title        = """
\\title{""" + documenttitle + """}
\\subtitle{""" + documentsubtitle + "\\texttt{" + programname + """}}
\\author{""" + documentauthor + """}
\\date{\\today}\n"""
    header       = "\n\\begin{document}\n" + "\\pagestyle{headings}\n" + "\\maketitle\n" + r"\inp{" + args.out_file + ".stat}\n" + "\\newpage\n"
    trailer      = ""
    if make_topics:                          # -mt is specified
        trailer = trailer + "\n\\newpage\n\\appendix"   
        trailer = trailer + "\n\\inp{" + args.out_file + ".top}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".xref}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".tap}"
    trailer = trailer + "\n\\printindex\n\\end{document}\n"

# ------------------------------------------------------------------
# Pickle-Load
# Get the structures authors, packages, topics, topicspackage, authorpackages (generated by CTANLoad.py)

# authors: python directory (sorted)
#   each element: <author key> <tuple with givenname and familyname> 
# packages: python directory (sorted)
#   each element: <package key> <tuple with package name and package title>
# topics: python directory (sorted)
#   each element: <topics name> <topics title>
# topicspackage: python directory (unsorted)
#   each element: <topic key> <list with package names>
# packagetopics: python directory (sorted)
#   each element: <topic key> <list with package names>
# authorpackages: python directory (unsorted)
#   each element: <author key> <list with package names>

try:                                        # try to open 1st pickle file 
    pickleFile1 = open(direc + pickle_name1, "br")
    (authors, packages, topics, topicspackage, packagetopics, authorpackages) = pickle.load(pickleFile1)
    pickleFile1.close()                     #   close file
except FileNotFoundError:                   # unable to open pickle file
    print("--- pickle file '" * pickle_name1 + "' not found")
    sys.exit("- program is terminated")

try:                                        # try to second open pickle file
    pickleFile2 = open(direc + pickle_name2, "br")
    XML_toc     = pickle.load(pickleFile2)
    pickleFile2.close()                     #   close file
except FileNotFoundError:                   # unable to open pickle file
    list_info_files = False
    print("--- pickle file '" * pickle_name2 + "' not found; local information files ignored")

# ------------------------------------------------------------------
# Only for LaTeX:
# * header of topic lists and topic cross-references
# * Open the files x.top, x.xref, x.stat, and x.tap

##if mode in ["LaTeX"] and make_topics:
    # xyz.top
##    tops = open(direc + args.out_file + ".top", encoding="utf-8", mode="w")
##    tops.write("% file: " + args.out_file + ".top" + "\n")
##    tops.write("% date: " + actDate + "\n")
##    tops.write("% time: " + actTime + "\n")
##    tops.write("% is called by " + args.out_file + ".tex" + "\n\n")
##    tops.write(r"\appendix" + "\n")
##    tops.write(r"\section{Used Topics, Short Explainations}" + "\n\n")
##    tops.write(r"\raggedright" + "\n")
##    tops.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxx}" + "\n")

    # xyz.xref
##    xref = open(direc + args.out_file + ".xref", encoding="utf-8", mode="w")
##    xref.write("% file: " + args.out_file + ".xref" + "\n")
##    xref.write("% date: " + actDate + "\n")
##    xref.write("% time: " + actTime + "\n")
##    xref.write("% is called by " + args.out_file + ".tex" + "\n\n")
##    xref.write(r"\section{Used Topics and related Packages}" + "\n\n")
##    xref.write(r"\raggedright" + "\n")
##    xref.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxx}" + "\n")

    # xyz.tap
##    tap = open(direc + args.out_file + ".tap", encoding="utf-8", mode="w")
##    tap.write("% file: " + args.out_file + ".tap" + "\n")
##    tap.write("% date: " + actDate + "\n")
##    tap.write("% time: " + actTime + "\n")
##    tap.write("% is called by " + args.out_file + ".tex" + "\n\n")
##    tap.write(r"\section{Authors and associated Packages}" + "\n\n")
##    tap.write(r"\raggedright" + "\n")
##    tap.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")

    # xyz.stat
##    stat = open(direc + args.out_file + ".stat", encoding="utf-8", mode="w")
##    stat.write("% file: " + args.out_file + ".stat" + "\n")
##    stat.write("% date: " + actDate + "\n")
##    stat.write("% time: " + actTime + "\n")
##    stat.write("% is called by " + args.out_file + ".tex" + "\n\n")
##    stat.write(r"\minisec{Parameters and Statistics}" + "\n\n")
##    stat.write(r"\raggedright" + "\n")
##    stat.write(r"\begin{tabular}{lrl}" + "\n")

# ------------------------------------------------------------------
# First line(s) on output  

def first_lines():
    """creates the first lines of output"""
    
    arguments   = ""
    tmp         = ""
    tmp_before  = ""
    e_parameter = ["-t","-k","--template","--key"]
     
    for f in range(1,len(call)):
        tmp = call[f]
        if tmp_before in e_parameter:
            tmp = '"' + tmp + '"'
        arguments = arguments + tmp + " "
        tmp_before = tmp
        
    if verbose:
        print("- program call: CTANOut.py", arguments)

    if verbose and (mode != "LaTeX") and make_topics:       # not LaTeX and -mt/--make_topics
        print("--- '-mt'/'--make_topics' valid only for '-m LaTeX'/'--mode LaTeX'; therefore ignored")

    if verbose and (mode != "BibLaTeX") and (btype != ""):  # not BibLaTeX and -b/--btype
        print("--- '-b'/'--btype' valid only for '-m BibLaTeX'/'--mode BibLaTeX'; therefore ignored")

    if mode in ["LaTeX"]:                                   # LaTeX
        out.write("% file: " + out_file + "\n")
        out.write("% date: " + actDate + "\n")
        out.write("% time: " + actTime + "\n\n")
        out.write("% generated by " + programname + " (version: "  + programversion + " of " + programdate + ")\n\n")
        out.write("% program call             : " + programname    + " " + arguments + "\n")
        out.write("% mode                     : " + mode           + "\n")
        out.write("% skipped CTAN fields      : " + skip           + "\n")
        if name_template != "":
            out.write("% filtered by name template: '"             + name_template + "'\n")
        if filter_key != "":
            out.write("% filtered by key template : '"             + filter_key + "'\n")
        out.write("\n% ---------------------------------------")
        out.write("\n% to be compiled with XeLaTeX or LuaLaTeX")
        out.write("\n% ---------------------------------------\n")
        out.write("\n" + r"\documentclass[" + classoptions + "\n]{scrartcl}\n")
        out.write(usepkg)
        out.write(title)
        out.write(header)
    elif mode in ["BibLaTeX"]:                               # BibLaTeX
        out.write("% generated by " + programname + " (version: "  + programversion + " of " + programdate + ")\n")
        out.write("% File                     : " + out_file + "\n")
        out.write("% Mode                     : " + mode + "\n")
        out.write("% Date                     : " + actDate + "\n")
        out.write("% Time                     : " + actTime + "\n\n")
        out.write("% Program Call             : " + programname + " " + arguments + "\n")
        out.write("% skipped CTAN fields      : " + skip + "\n")
        out.write("% type of BibLaTeX entries : " + btype          + "\n") 
        if name_template != "":
            out.write("% filtered by name template: " + name_template + "\n")
        if filter_key != "":
            out.write("% filtered by key template : " + filter_key + "\n")
        out.write("\n% actual mapping CTAN --> BibLaTeX\n")
        out.write("% alias         --> note\n")
        out.write("% also          --> related\n")
        out.write("% authorref     --> author\n")
        out.write("% caption       --> subtitle\n")
        out.write("% contact       --> note\n")
        out.write("% copyright     --> usera, year\n")
        out.write("% ctan          --> url, urldate\n")
        out.write("% description   --> abstract\n")
        out.write("% documentation --> note, file (if applicable)\n")
        out.write("% home          --> note, usere\n")
        out.write("% install       --> note, userf\n")
        out.write("% keyval        --> keywords\n")
        out.write("% license       --> note, userb\n")
        out.write("% miktex        --> note, userc\n")
        out.write("% name          --> title\n")
        out.write("% texlive       --> note, userd\n")
        out.write("% version       --> version, date\n\n")
        out.write("% a) The BibLaTeX field note is used for collecting the following CTAN items:\n")
        out.write("%    alias, contact, documentation, home, install, license, miktex, texlive\n")
        out.write("% b) The program uses the optional BibLaTeX fields usera, userb, userc, userd, usere, userf\n")
        out.write("\n% -------------------------------------")
        out.write("\n% to be compiled by XeLaTeX or LuaLaTeX")
        out.write("\n% -------------------------------------\n")
    elif mode in ["plain"]:                                  # plain
        out.write(documenttitle.center(80) + "\n" + (documentsubtitle + programname).center(80) + "\n\n")
        out.write("generated by " + programname + " (version: "  + programversion + " of " + programdate + ")\n")
        out.write("file                     : " + out_file + "; mode: " + mode + "; date: " + actDate + "; time: " + actTime + "\n")
        out.write("program call             : " + "CTAN-out.py " + arguments + "\n")
        out.write("skipped CTAN fields      : " + skip + "\n")
        if name_template != "":
            out.write("filtered by name template: " + name_template + "\n")
        if filter_key != "":
            out.write("filtered by key template : " + filter_key + "\n")
    elif mode in ["RIS"]:                                    # RIS
        pass                                                 #   for RIS do nothing
    elif mode in ["Excel"]:                                  # Excel
        out.write("id")
        for f in ["caption", "authorref", "version", "license", "contact", "copyright", "CTAN",
                  "documentation", "home", "install", "keyval", "mikTeX", "TeXLive", "also"]:
            out.write("\t" + f)
        out.write("\n")

#===================================================================
# Functions

# alias(k)           element <alias .../>
# also(k)            element <also .../>
# authorref(k)       element <authorref .../>
# caption(k)         element <caption> ... </caption>
# contact(k)         element <contact ...>
# copyrightT(k)      element <copyright .../>
# ctan(k, t)         element <ctan .../>
# description(k)     element <description ...> ... </description>
# documentation(k)   element <documentation ../.>
# entry(k, t)        elemend <entry ... </entry>
# home(k)            element <home .../>
# install(k)         element <install .../>
# keyval(k)          element <keyval .../>
# leading(k)         first lines of one package
# li(k)              element <li> ... </li>
# licenseT(k)        element <license .../>
# miktex(k)          element <miktex .../>
# mod_a(k)           element <a ...> ... </a>
# xref(k)            element <xref ...> ... </xref>
# mod_b(k)           element <b> ... </b>
# mod_backslash(s)   special processing of \ in the source text
# mod_br(k)          element <br/>
# mod_em(k)          element <em> ... </em>
# mod_i(k)           element <i> ... </i>
# mod_pre(k)         element <pre> ... </pre>
# mod_TeXchars(s)    prepare characters for LaTeX/BibLaTeX in a paragraph
# mod_tt(k)          element <tt> ... </tt>
# name(k)            element <name> ... </name>
# onepackage(s, t)   open a file with the package description and initialize XML processing
# p(k)               element <p> ... </p>
# TeXchars(s)        prepare characters for LaTeX/BibLaTeX
# texlive(k)         element <texlive .../>
# trailing(k, t)     last lines of a package part
# ul(k)              element <ul> ... </ul>
# version(k)         element <version .../>

# main --> first_lines
# main --> make_stat
# main --> make_statistics
# main --> make_tap
# main --> make_tops
# main --> make_xref
# main --> process_packages
#          process_packages --> onepackage
#                               onepackage --> entry
#                                              entry --> alias
#                                              entry --> also	
#                                                        also          --> TeXchars
#                                              entry --> authorref
#                                              entry --> caption
#                                                        caption       --> TeXchars
#                                              entry --> contact
#                                              entry --> copyrightT
#                                                        copyrighT     --> TeXchars
#                                              entry --> ctan
#                                              entry --> description
#                                                        description   --> p
#                                                        description   --> ul
#                                              entry --> documentation
#                                                        documentation --> TeXchars
#                                              entry --> home
#                                              entry --> install
#                                              entry --> keyval
#                                                        keyval        --> TeXchars
#                                              entry --> leading
#                                                        leading       --> TeXchars
#                                              entry --> licenseT
#                                              entry --> miktex
#                                                        miktex        --> TeXchars
#                                              entry --> name
#                                                        name          --> TeXchars
#                                              entry --> texlive
#                                                        texlive       --> TeXchars
#                                              entry --> trailing
#                                              entry --> version

# ul --> li
# li --> mod_TeXchars
# p  --> mod_TeXchars
#        mod_TeXchars --> mod_backslash
# p --> mod_a
# p --> mod_b
# p --> mod_br
# p --> mod_em
# p --> mod_i
# p --> mod_pre
# p --> mod_tt
# p --> mod_xref

# ------------------------------------------------------------------
def alias(k):                                     # element <alias .../>
    """processes the alias element."""

    global notice

    id  = k.get("id", "")                         # attribute id
    
    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                             
    else:
        tmp = default_text                        # if k.text is empty

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Alias] " + r"\texttt{" + tmp + "}\n")
        out.write(r"\index{Package!" + tmp + " (alias for " + package_id + ")}\n")
        out.write(r"\index{Alias!" + tmp + " (for " + package_id + ")}\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Alias: ".ljust(labelwidth) + tmp)
    elif mode in ["BibLaTeX"]:
        if notice != "":                          # accumulate notice string
            notice += " " * (fieldwidth + 2) + "Alias: " + tmp + ";\n"
        else:
            notice = "Alias: " + tmp + ";\n"
    else:
        pass                                      #   for Excel, BibLaTeX, RIS do nothing

# ------------------------------------------------------------------
def also(k):                                      # element <also .../>
    """Processes the also element."""

    # also --> TeXchars
    
    global s_also                                 # string for Excel

    refid = k.get("refid","")                     # attribute refid

    if mode in ["LaTeX"]:                         # LaTeX
        refid2 = re.sub("_", "-", refid)          #   substitute "_"
        tmp1   = TeXchars(packages[refid][0])
        tmp2   = TeXchars(packages[refid][1])
        out.write(r"\item[see also] see section~\ref{pkg:" + refid2 + r"} on page~\pageref{pkg:" + refid2 + r"}: (\texttt{" + tmp1 + "} -- " + tmp2 + ")\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "see also: ".ljust(labelwidth) + refid + " (" + packages[refid][0] + " -- " + packages[refid][1] + ")")
    elif mode in ["RIS"]:                         # RIS
        pass                                      #   for RIS do nothing
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        out.write("related".ljust(fieldwidth) + "= {" + refid + "},\n")
    elif mode in ["Excel"]:                       # Excel 
        if s_also != "":
            s_also += "; " + refid                # accumulate s_also string 
        else:
            s_also = refid

# ------------------------------------------------------------------
def authorref(k):                                 # element <authorref .../>
    """Processes the authorref element, constructs the complete name and usedAuthors entry."""
    
    global authorexists                           # flag
    global s_authorref                            # string for Excel
    global usedAuthors                            # directory: collects used authors

    # The element authorref has been changed: Now the attribute id is used, not key.

    key        = k.get("key", "")                 # attribute key
    xid        = k.get("id", "")                  # attribute id
    givenname  = k.get("givenname", "")           # attribute givenname
    familyname = k.get("familyname", "")          # attribute familyname
    active     = k.get("active", "")              # attribute active
    tmp        = givenname

    if (xid != "") and (xid in authors):          # attribut xid is used
        key = xid
        givenname, familyname = authors[xid]      #   find givenname, familyname in authors 
        tmp = givenname
    else:
        key = xid
        givenname, familyname = empty, userunknown#   givenname, familyname not found
        tmp = givenname

    if familyname != "":                          # constructs the complete name + usedAuthors entry
        tmp  += " " + familyname
        tmp2 = familyname + ", " + givenname
        usedAuthors[key] = (givenname, familyname)#   store actual author in usedAuthors
    else:
        tmp2             = tmp
        usedAuthors[key] = (givenname)            #   store actual author in usedAuthors

    if active == "false":
        tmp = tmp + " (not active)"

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Author] " + tmp + "\n")
        out.write(r"\index{Author!" + tmp2 + "}\n")
    elif mode in ["RIS"]:                         # RIS
        out.write("AU  - " + tmp2 + "\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Author: ".ljust(labelwidth) + tmp)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        pass                                      #   for BibLaTeX do nothing  
    elif mode in ["Excel"]:                       # Excel 
        if s_authorref != "":
            s_authorref += "; " + tmp             #   accumulate s_authorref string
        else:
            s_authorref = tmp

    authorexists = True

# ------------------------------------------------------------------
def caption(k):                                   # element <caption>...</caption>
    """Processes the caption element."""

    # caption --> TeXchars
    
    global s_caption                              # string for Excel

    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                              
    else:
        tmp = default_text                        #   if k.text is empty

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        tmp = re.sub("#", "\\#", tmp)
        out.write(r"\item[Caption] " + tmp + "\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Caption: ".ljust(labelwidth) + tmp)
    elif mode in ["RIS"]:                         # RIS
        pass                                      #   for RIS do nothing
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = TeXchars(tmp)
        tmp = re.sub("#", "\\#", tmp)
        out.write("subtitle".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_caption = tmp

# ------------------------------------------------------------------
def contact(k):                                   # element <contact .../>
    """Processes the contact element."""
    
    global notice
    global s_contact                              # string for Excel

    typeT = k.get("type", "")                     # attribute type (announce, bugs, development, repository, support)
    href  = k.get("href", "")                     # attribute href

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Contact] \textit{" + typeT + r"}: \url{" + href + "}\n")
        out.write(r"\index{Contact!" + typeT + "}\n")
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "Contact: " + typeT + ": " + href + ";\n"
##        out.write("L1  - " + href + "\n")
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if notice != "":                          # accumulate notice string
            notice += " " * (fieldwidth + 2) + "Contact: " + typeT + ": " + href + ";\n"
        else:
            notice = "Contact: " + typeT + ": " + href + ";\n"
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Contact: ".ljust(labelwidth) + typeT + ": " + href)
    elif mode in ["Excel"]:                       # Excel
        if s_contact != "":                       # accumulate s_contact string
            s_contact += "; " + typeT + ": " + href
        else:
            s_contact = typeT + ": " + href

# ------------------------------------------------------------------
def copyrightT(k):                                # element <copyright .../>
    """Processes the copyright element."""

    # copyrighT --> TeXchars
    
    global notice                                 # string for RIS
    global year_str
    global s_copyright                            # string for Excel

    owner    = k.get("owner", "")                 # attribute owner
    year     = k.get("year", "--")                # attribute year
    year_str = year

    tmp   = owner                                 
    if year != "":                                # construct owner (year)
        tmp = tmp + " (" + year + ")"

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = re.sub("_", r"\\_", tmp)
        tmp = TeXchars(tmp)
        out.write(r"\item[Copyright] " + tmp + "\n")
    elif mode in ["RIS"]:                         # RIS
        out.write("PY  - " + year + "\n")
        notice += "Copyright: " + tmp + ";\n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = re.sub("_", r"\\_", tmp)
        tmp = TeXchars(tmp)
        notice += "Copyright: " + tmp + ";\n" # accumulate notice string
        out.write("usera".ljust(fieldwidth) + "= {" + tmp + "},\n")
        out.write("year".ljust(fieldwidth) + "= {" + year + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Copyright: ".ljust(labelwidth) + tmp)
    elif mode in ["Excel"]:                       # Excel
        if s_copyright != "":
            s_copyright += "; " + tmp             # accumulate s_copyright string
        else:
            s_copyright = tmp

# ------------------------------------------------------------------
def ctan(k, t):                                   # element <ctan .../>
    """Processes the ctan element."""
    
    global s_ctan                                 # string for Excel
    global notice

    path = k.get("path", "")                      # attribute path
    file = k.get("file", "")                      # attribute file

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[on CTAN] " + r"\url{" + ctanUrl2 + path + "}\n")
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "on CTAN: " + ctanUrl2 + path + "\n"
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "on CTAN: ".ljust(labelwidth) + ctanUrl2 + path)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        out.write("url".ljust(fieldwidth) + "= {" + ctanUrl2 + path + "},\n")
        out.write("urldate".ljust(fieldwidth) + "= {" + t + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_ctan = ctanUrl2 + path

# ------------------------------------------------------------------
def description(k):                               # element <description ...> ... </description>
    """Processes the description element."""

    # description --> p
    # description --> ul
    
    language = k.get("language", "")              # attribute language

    if language in languagecodes:                 # convert language keys
        languagex = languagecodes[language]
    else:
        languagex = ""

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Description]" + languagex)
        if languagex != "":
            out.write(r"\index{Language in description/documentation!" + languagex + "}\n")
    elif mode in ["RIS"]:                         # RIS
        out.write("AB  - " + languagex + "\n")
    elif mode in ["plain"]:                       # plain
        out.write("\nDescription:".ljust(labelwidth) + languagex)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        out.write("abstract".ljust(fieldwidth)+ "= {" + languagex)
    elif mode in ["Excel"]:                       # Excel
        pass                                      #   for Excel do nothing

    for child2 in k:                              # fetch the sub-elements p a/o ul
        if child2.tag == "p":
            p(child2)
        elif child2.tag == "ul":
            ul(child2)

    if mode in ["BibLaTeX"]:                      # BibLaTeX
        out.write("},\n")

# ------------------------------------------------------------------
def documentation(k):                             # element <documentation .../>
    """Processes the documentation element."""

    # documentation --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX
    global info_files
    global XML_toc
    global s_documentation                        # string for Excel

    details = k.get("details", "")                # attribute details
    href    = k.get("href", "")                   # attribute href
    language= k.get("language", "")               # attribute language

    href2    = href.replace("ctan:/", ctanUrl2)
    p        = None

    if language in languagecodes:                 # converts language keys
        languagex = " (" + languagecodes[language] + ")"
    else:
        languagex = ""

    if languagex != "":
        p = re.search(languagecodes[language], details)

    if mode in ["LaTeX"]:                         # LaTeX
        details = TeXchars(details)
        if languagex != "":
            out.write(r"\index{Language in description/documentation!" + languagecodes[language] + "}\n")
        if p == None:                             #   no language found in details
            out.write(r"\item[Documentation]" + languagex + r" \textit{" + details + "}: " + r"\url{" + href2 + "}\n")
        else:
            out.write(r"\index{Language in description/documentation!" + p.group() + "}\n")
            out.write(r"\item[Documentation]" + r" \textit{" + details + "}: " + r"\url{" + href2 + "}\n")
    elif mode in ["RIS"]:                         # RIS
        if list_info_files:
            if href in XML_toc:
                tmp    = XML_toc[href]
                one_if = tmp[1] + "-" + tmp[2]    #   one info file
                fx     = os.path.abspath(one_if)
                out.write("L1  - " + fx + "\n")
        if p == None:                             #   no language found in details
            notice += " " * (fieldwidth + 2) + "Documentation" + languagex + ": " + details + ": " + href2 + "; \n"
        else:
            notice += " " * (fieldwidth + 2) + "Documentation" + ": " + details + ": " + href2 + "; \n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        details = TeXchars(details)
        if list_info_files:
            if href in XML_toc:
                tmp    = XML_toc[href]
                one_if = tmp[1] + "-" + tmp[2]    #   one info file
                if len(info_files) == 0:
                    info_files = one_if
                else:
                    info_files += ";" + one_if
        if p == None:                             #   no language found in details
            tmp = "Documentation" + languagex + ": " + details + ": " + href2 + "; \n"
        else:
            tmp = "Documentation" + ": " + details + ": " + href2 + "; \n"
        if notice != "":                          #   accumulate notice string
            notice += " " * (fieldwidth + 2) + tmp
        else:
            notice = tmp
    elif mode in ["plain"]:                       # plain
        if p == None:                             #   no language found in details
            out.write("\nDocumentation: ".ljust(labelwidth) + details + languagex + ": " + href2)
        else:
            out.write("\nDocumentation: ".ljust(labelwidth) + details + ": " + href2)
        if href in XML_toc:
            tmp    = XML_toc[href]
            one_if = tmp[1] + "-" + tmp[2]    #   one info file
            fx     = os.path.abspath(one_if)
            out.write("\n--local file: ".ljust(labelwidth + 1) + fx)
    elif mode in ["Excel"]:                       # Excel
        if s_documentation != "":                 #   accumulate s_documentation string
            s_documentation += "; " + details + ": " + href2
        else:
            s_documentation = details + ": " + href2

# -----------------------------------------------------------------
def entry(k, t):                                  # element <entry ...>...</entry>
    """Processes the main element entry."""

    # entry --> leading
    # entry --> description
    # entry --> name
    # entry --> alias
    # entry --> caption
    # entry --> authorref
    # entry --> copyrightT
    # entry --> licenseT
    # entry --> version
    # entry --> documentation
    # entry --> ctan
    # entry --> miktex
    # entry --> texlive
    # entry --> keyval
    # entry --> install
    # entry --> contact
    # entry --> also
    # entry --> home
    # entry --> trailing
    
    global notice, package_id
    global s_id, s_also, s_authorref, s_contact, s_copyright, s_ctan, s_documentation, s_home, s_home, s_home
    global s_install, s_keyval, s_license, s_miktex, s_texlive, s_version

    if mode in ["Excel"]:                         # initializes strings for Excel
        s_id            = k.get("id", "")         # attribute id
        s_contact       = ""
        s_home          = ""
        s_also          = ""
        s_authorref     = ""
        s_copyright     = ""
        s_ctan          = ""
        s_documentation = ""
        s_home          = ""
        s_install       = ""
        s_keyval        = ""
        s_license       = ""
        s_miktex        = ""
        s_home          = ""
        s_texlive       = ""
        s_version       = ""

    leading(k)
    package_id = k.get("id", "")

    for child in k:                               # calls the sub-elements
        if child.tag == "description":            # description
            if mode != "Excel":                   #   not for Excel
                if not child.tag in skip:
                    description(child)
        elif child.tag == "name":                 # name
            if not child.tag in skip:
                name(child)
        elif child.tag == "alias":                # alias
            if not child.tag in skip:
                alias(child)
        elif child.tag == "caption":              # caption
            if not child.tag in skip:
                caption(child)
        elif child.tag == "authorref":            # authorref
            if not child.tag in skip:
                authorref(child)
        elif child.tag == "copyright":            # copyright
            if not child.tag in skip:
                copyrightT(child)
        elif child.tag == "license":              # license
            if not child.tag in skip:
                licenseT(child)
        elif child.tag == "version":              # version
            if not child.tag in skip:
                version(child)
        elif child.tag == "documentation":        # documentation
            if not child.tag in skip:
                documentation(child)
        elif child.tag == "ctan":                 # ctan
            if not child.tag in skip:
                ctan(child, t)
        elif child.tag == "miktex":               # miktex
            if not child.tag in skip:
                miktex(child)
        elif child.tag == "texlive":              # texlive
            if not child.tag in skip:
                texlive(child)
        elif child.tag == "keyval":               # keyval
            if not child.tag in skip:
                keyval(child)
        elif child.tag == "install":              # install
            if not child.tag in skip:
                install(child)
        elif child.tag == "contact":              # contact
            if not child.tag in skip:
                contact(child)
        elif child.tag == "also":                 # also
            if not child.tag in skip:
                also(child)
        elif child.tag == "home":                 # home
            if not child.tag in skip:
                home(child)
    trailing(k, t)

# ------------------------------------------------------------------
def home(k):                                      # element <home .../>
    """Processes the home element."""
    
    global notice                                 # string for RIS/BibLaTeX
    global s_home                                 # string for Excel

    href = k.get("href", "")                      # attribute href

    if mode in ["LaTeX"]:                         # LaTeX 
        out.write(r"\item[Home page] " + r"\url{" + href + "}\n")
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "Home page: " + href + "; \n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        notice += " " * (fieldwidth + 2) + "Home page: " + href + "; \n"
        out.write("usere".ljust(fieldwidth) + "= {" + href + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Home page: ".ljust(labelwidth) + href)
    elif mode in ["Excel"]:                       # Excel
        s_home = href

# ------------------------------------------------------------------
def install(k):                                   # element <install .../>
    """Processes the install element."""
    
    global notice                                 # string for RIS/BibLaTeX
    global s_install                              # string for Excel

    path = k.get("path", "")                      # attribute path

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Installation] " + r"\url{" + ctanUrl3 + path + "}\n")
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "Installation: " + ctanUrl3 + path + "; \n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        notice += " " * (fieldwidth + 2) + "Installation: " + ctanUrl3 + path + "; \n"
        out.write("userf".ljust(fieldwidth) + "= {" + ctanUrl3 + path + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Installation: ".ljust(labelwidth) + ctanUrl3 + path)
    elif mode in ["Excel"]:                       # Excel
        s_install = ctanUrl3 + path

# ------------------------------------------------------------------
def keyval(k):                                    # element <keyval .../>
    """Processes the keyval element."""

    # keyval --> TeXchars
    
    global s_keyval                               # string for Excel
    global usedTopics                             # directory for collecting topics

    key   = k.get("key", "")                      # attribute key
    value = k.get("value", "")                    # attribute value

    tmp   = topics[value]
    if not value in usedTopics:                   # collects topics in usedTopics
        usedTopics[value] = 1
    else:
        usedTopics[value] = usedTopics[value] + 1

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        out.write(r"\item[Keyword] " + r"\texttt{" + value + "} (" + tmp + ")\n")
        out.write(r"\index{Topic!" + value + "}\n")
    elif mode in ["RIS"]:                         # RIS
        out.write("KW  - " + value + "\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Key: ".ljust(labelwidth) + value + " (" + topics[value] + ")")
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        pass                                      #   for BibLaTeX do nothing
    elif mode in ["Excel"]:                       # Excel
        if s_keyval != "":
            s_keyval += "; " + value    # accumulate s_keyval string
        else:
            s_keyval = value

# ------------------------------------------------------------------
def leading(k):                                   # first lines of one package
    """Analyzes the first lines of each package XML file and outputs some lines."""

    # leading --> TeXchars
    
    global authorexists                           # flag

    xname = k.get("id", "")                       # attribute id

    allauthors  = []                              # initialize some variables
    year        = ""
    year_string = ""
    authorexists= False
    
    usedPackages.append(xname)

    for child in k:                                           # find some supp. infos
        if child.tag == "caption":
            xcaption  = child.text                            # embedded text xcaption
            xcaption2 = xcaption
            if len(xcaption2) >= maxcaptionlength:
                xcaption2 = xcaption2[0:maxcaptionlength] + " ..."
            xcaption2 = TeXchars(xcaption2)
            xcaption2 = re.sub("#", "\\#", xcaption2)
            
        if child.tag == "authorref":                          # author(s) for mode=="BibLaTeX"
            onefamilyname = child.get("familyname", "")       # attribute familyname
            onegivenname  = child.get("givenname", "")        # attribute givenname
            active        = child.get("active", "true")       # attribute active
            oneauthor     = (onefamilyname, onegivenname)
            xid           = child.get("id", "")               # attribute id
            
            if (xid != "") and (xid in authors):
                onegivenname, onefamilyname = authors[xid]
                oneauthor = (onefamilyname, onegivenname)
            else:
                onegivenname, onefamilyname = empty, userunknown
                oneauthor = (onefamilyname, onegivenname)
                
            if active:
                allauthors.append(oneauthor)
                
        if child.tag == "version":                            # get version
            number    = child.get("number", "")               # attribute number
            date      = child.get("date", "")                 # attribute date
            if date != "":
                number += " (" + date + ")"
            if number != "":
                xcaption += "; version " + number

    if mode in ["BibLaTeX"]:                                  # BibLaTeX
        allauthors2 = []                                      # generate author string for the actual package
        for f in allauthors:
            f = list(f)
            
            if " " in f[0]:
                f[0] = "{" + f[0] + "}"
            if " " in f[1]:
                f[1] = "{" + f[1] + "}"
                
            if (f[0] != "") and (f[1] != ""):
                oneauthor = f[0] + ", " + f[1]
            elif (f[0] != "") and (f[1] == ""):
                oneauthor = f[0]
            else:
                oneauthor = f[1]

            allauthors2.append(oneauthor)
            
        if len(allauthors2) > 0:
            author_string = allauthors2[0]
        else:
            author_string = userunknown
            
        for f in range(1, len(allauthors2)):
            author_string = author_string + " and " + allauthors2[f]

    if mode in ["LaTeX"]:                                     # LaTeX
        xcaption = TeXchars(xcaption)
        xcaption = re.sub("#", "\\#", xcaption)
        xname1   = TeXchars(xname)
        xname2   = re.sub("_", "-", xname)
        out.write("\n%" + 80*"-")
        tmp = r"\texttt{" + xname1 + "} -- "
        out.write("\n" + r"\section[" + tmp + xcaption2 + "]{" + tmp + xcaption + r"}\label{pkg:" + xname2 + "}\n")
        out.write(r"\index{Package!" + xname1 + "}\n\n")
        out.write(r"\begin{labeling}{Documentation}" + "\n")
    elif mode in ["RIS"]:                                     # RIS
        out.write("\nTY  - COMP" + "\n")
        out.write("T1  - " + xname + "\n")
        out.write("T4  - " + xcaption + "\n")
    elif mode in ["plain"]:                                   # plain
        tmp = xname + " -- " + xcaption
        out.write("\n\n\n" + tmp)
        out.write("\n" + len(tmp) * "-")
    elif mode in ["BibLaTeX"]:                                # BibLaTeX
        out.write("\n" + btype + "{" + xname + ",\n")
        out.write("author".ljust(fieldwidth) + "= {" + author_string + "},\n")
    elif mode in ["Excel"]:                                   # Excel
        pass                                                  #   for Excel do nothing
    authorexists = False

# ------------------------------------------------------------------
def li(k):                                        # element <li>...</li>
    """Processes the li element."""

    # li --> mod_TeXchars

    mod_a(k)                                      # sub-element a
    mod_xref(k)                                   # sub-element xref
    mod_b(k)                                      # sub-element b
    mod_em(k)                                     # sub-element em
    mod_tt(k)                                     # sub-element tt
    mod_i(k)                                      # sub-element i

    tmptext = "".join(k.itertext()).rstrip()      # collects embedded strings

    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX / BibLaTeX
        tmptext = mod_TeXchars(tmptext)

    if mode in ["LaTeX"]:                         # LaTeX
        tmptext = r"\item " + tmptext + "\n"
        out.write(tmptext)
    elif mode in ["Excel", "RIS", "plain", "BibLaTeX"]:
                                                  # BibLaTeX / RIS / plain / Excel
        tmptext = re.sub("[ ]+", " ", tmptext)
        tmptext = re.sub("[\n]+", "", tmptext)
        tmptext = "+ " + tmptext + "\n"
        out.write(tmptext)

# ------------------------------------------------------------------
def licenseT(k):                                  # element <license .../>
    """Processes the license element."""
    
    global notice                                 # string for RIS/BibLaTeX
    global s_license                              # string for Excel

    typeT = k.get("type", "")                     # attribute type
    date  = k.get("date", "")                     # attribute date
    tmp   = typeT

    if date != "":                                # constructs lincense (date)
        tmp = tmp + " (" + date + ")"

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[License] " + tmp + "\n")
        out.write(r"\index{License!" + tmp + "}\n")
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "License: " + tmp + "; \n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if notice != "":
            notice += " " * (fieldwidth + 2) + "License: " + tmp + "; \n"
        else:
            notice = "License: " + tmp + "; \n"
        out.write("userb".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "License: ".ljust(labelwidth) + tmp)
    elif mode in ["Excel"]:                       # Excel
        s_license = tmp

# ------------------------------------------------------------------
def miktex(k):                                    # element <miktex .../>
    """Processes the miktex element."""

    # miktex --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX
    global s_miktex                               # string for Excel

    location = k.get("location", "")              # attribute location

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(location)
        out.write(r"\item[on Mik\TeX] " + r"\texttt{" + tmp + "}\n")
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "on MikTeX: " + location + "; \n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp    = TeXchars(location)
        notice += " " * (fieldwidth + 2) + "on MikTeX: " + tmp + "; \n"
        out.write("userc".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "on MikTeX: ".ljust(labelwidth) + location)
    elif mode in ["Excel"]:                       # Excel
        s_miktex = location

# ------------------------------------------------------------------
def mod_a(k):                                     # element <a ...> ... </a>
    """Processes the a element."""
    
    ll = list(k.iter("a"))                        # fetches all a elements; ##1: {; ##2: }

    for i in ll:
        tmp = i.attrib["href"]                    # attribute href
        p   = re.search("http", tmp)              # searches "http"
        
        if p == None:
            tmp2 = ctanUrl + tmp
        else:
            tmp2 = tmp

        if i.text == None:                        # no embedded text
            i.text = tmp                          #   get embedded text
            
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = re.sub("_", "-", i.text)     #   change embedded text
            i.text = "§§3href§§1" + tmp2 + "§§2§§1" + i.text + "§§2"
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = i.text + " (" + tmp2 + ")"   #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excek do nothing

# ------------------------------------------------------------------
def mod_xref(k):                                  # element <xref ...> ... </xref>
    """Processes the xref element."""
    
    # Now the element xref is used for inline-links, not a.
    
    ll = list(k.iter("xref"))                     # fetch all xref elements; ##1: {; ##2: }

    for i in ll:
        tmp  = i.attrib["refid"]                  # attribute refid
        tmp2 = ctanUrl4 + tmp
        
        if i.text == None:                        # no embedded textdef onepackage
            i.text = tmp                          #   get embedded text
            
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = re.sub("_", "-", i.text)     #   change embedded text
            i.text = "§§3href§§1" + tmp2 + "§§2§§1" + i.text + "§§2"
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = i.text + " (" + tmp2 + ")"   #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_b(k):                                     # element <b>...</b>
    """Processes the b element."""
    
    ll = list(k.iter("b"))                        # fetches all b elements

    for i in ll:                                  # loop: all b elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3textbf§§1" + i.text + "§§2"
                                                  # change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "''" + i.text + "''"         #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_backslash(s):                             # special processing von \ in the source text
    """Corrects \. """
    
    res = re.sub(r"\\", r"§§3textbackslash ",s)
    return res

# ------------------------------------------------------------------
def mod_br(k):                                    # element <br/>
    """Processes the br element."""
    
    ll = list(k.iter("br"))                       # fetches all b elements

    for i in ll:                                  # loop: all br elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3§§3"                     #   change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "\n"                         #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_em(k):                                    # element <em>...</em>
    """Processes the em element."""
    
    ll = list(k.iter("em"))                       # fetch all em elements

    for i in ll:                                  # loop: all em elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3emph§§1" + i.text + "§§2"#   change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "'" + i.text + "'"           #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_i(k):                                     # element <i>...</i>
    """Processes the i element."""
    
    ll = list(k.iter("i"))                        # fetch all i elements

    for i in ll:                                  # loop: all i elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3emph§§1" + i.text + "§§2"#   change embedded text 
        elif mode in ["RIS", "plain"]:            # RIS / plaindef onepackage
            i.text = "'" + i.text + "'"           #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_pre(k):                                   # element <pre>...</pre>
    """Processses the pre element."""
    
    ll = list(k.iter("pre"))                      # fetch all i elements

    for i in ll:                                  # all: all pre elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "\n§§3begin§§1verbatim§§2\n" + i.text + "\n§§3end§§1verbatim§§2\n"
                                                  # change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "\n" + i.text + "\n"         #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_TeXchars(s):                              # prepares characters for LaTeX/BibLaTeX in a paragraph
    """Prepares characters for LaTeX/BibLaTeX in a paragraph."""

    # mod_TeXchars --> mod_backslash
    
    tmp = s
    tmp = mod_backslash(tmp)                      # change \
    tmp = re.sub("[\[]", "[", tmp)                # change [
    tmp = re.sub("#", "§§3#", tmp)                # change #
    tmp = re.sub("}", "§§3} ", tmp)               # change }
    tmp = re.sub("{", "§§3{ ", tmp)               # change {
    tmp = re.sub(r"[\$]", "§§3$", tmp)            # change $
    tmp = re.sub("%", "§§3%", tmp)                # change %
    tmp = re.sub("_", "§§3_", tmp)                # change _
    tmp = re.sub("≥", "$>=$", tmp)                # change ≥
    tmp = re.sub("≤", "$<=$", tmp)                # change ≤
##    tmp = re.sub("&", "§§3&", tmp)       # <=======
    tmp = re.sub(r"\^", r"§§3textasciicircum ", tmp) # change ^
    tmp = re.sub("§§1", "{", tmp)                 # re-change {
    tmp = re.sub("§§2", "}", tmp)                 # re-change }
    tmp = re.sub("§§3", r"\\", tmp)               # re-change \
    tmp = re.sub("&", r"\&", tmp)                 # change &
    return tmp

# ------------------------------------------------------------------
def mod_tt(k):                                    # element <tt>...</tt>
    """Processes the tt element."""

    ll = list(k.iter("tt"))                       # fetch all tt elements

    for i in ll:                                  # loop: all tt elements
        tmp = i.text                              #   get embedded text
        
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3texttt§§1" + tmp + "§§2" #   change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "'" + tmp + "'"              #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def name(k):                                      # element <name>...</name>
    """Processes the name element."""

    # name --> TeXchars
    
    global s_name                                 # string for Excel

    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                              
    else:                                         #   k.text is empty
        tmp = default_text                        

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        out.write(r"\item[Name] \texttt{" + tmp + "}\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Name: ".ljust(labelwidth) + tmp)
    elif mode in ["RIS"]:                         # RIS
        pass                                      #   for RIS do nothing
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = TeXchars(tmp)
        out.write("title".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_name = k.text                           #   embedded text

# ------------------------------------------------------------------
def onepackage(s, t):
    """Load a package XML file and start parsing."""

    # onepackage --> entry
    
    global counter                                # counter for packages

    try:
        onePackage     = ET.parse(s + ext)        # parse XML file
    except:                                       # not successfull
        if verbose:
            print("----- XML file for package '" + s + "' not well-formed")
        return
    if verbose:
        print("    " + str(counter).ljust(5), "Package:", s.ljust(31), "Mode:", mode.ljust(7), "File:", out_file.ljust(15))

    counter        = counter + 1                  # increment counter
    onePackageRoot = onePackage.getroot()         # get XML root 
    entry(onePackageRoot, t)                      # begin with entry element

# ------------------------------------------------------------------
def p(k):                                         # element <p> ... </p>
    """Processes the p element."""

    # p --> mod_pre
    # p --> mod_br
    # p --> mod_a
    # p --> mod_xref
    # p --> mod_b
    # p --> mod_em
    # p --> mod_tt
    # p --> mod_i
    # p --> mod_TeXchars
    
    mod_pre(k)                                    # sub-element pre
    mod_br(k)                                     # sub-element br
    mod_a(k)                                      # sub-element a
    mod_xref(k)                                   # sub-element xref
    mod_b(k)                                      # sub-element b
    mod_em(k)                                     # sub-element em
    mod_tt(k)                                     # sub-element tt
    mod_i(k)                                      # sub-element i

    tmptext = "".join(k.itertext()).rstrip()      # collect all embedded texts

    if mode in ["LaTeX"]:                         # LaTeX
        tmptext = mod_TeXchars(tmptext)
        tmptext += "\n"
        out.write(tmptext)
    elif mode in ["plain"]:                       # plain
        tmptext += "\n"
        out.write(tmptext)
    elif mode in ["Excel"]:                       # Excel
        tmptext = re.sub("[ ]+", " ", tmptext)
        tmptext += "\n"
        out.write(tmptext)
    elif mode in ["RIS"]:                         # RIS
        tmptext = re.sub("[ ]+", " ", tmptext)
        tmptext = re.sub("[\n]+", "", tmptext)
        tmptext += "\n"
        out.write(tmptext)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmptext = mod_TeXchars(tmptext)
        tmptext = re.sub("[ ]+", " ", tmptext)
        tmptext = re.sub("[\n]+", "", tmptext)
        tmptext += "\n"
        out.write(tmptext)

# ------------------------------------------------------------------
def TeXchars(s):                                   # prepares characters for LaTeX/BibLaTeX
    tmp = s
    tmp = re.sub(r"\\", r"\\textbackslash ", tmp)
    tmp = re.sub("_", r"\\_", tmp)
    tmp = re.sub("&", r"\\&", tmp)
    tmp = re.sub(r"[\^]", r"\\textasciicircum ", tmp)
    tmp = re.sub("[$]", r"\\$", tmp)
    return tmp

# ------------------------------------------------------------------
def texlive(k):                                   # element <texlive .../>
    """Processes the texlive element."""

    # texlive --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX
    global s_texlive                              # string for Excel

    location = k.get("location", "")              # attribute location

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(location)
        out.write(r"\item[on \TeX Live] " + r"\texttt{" + tmp + "}\n")
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "on TeXLive: " + location + ";\n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = TeXchars(location)
        notice += " " * (fieldwidth + 2) + "on TeXLive: " + tmp + ";\n"
        out.write("userd".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "on TeXLive: ".ljust(labelwidth) + location)
    elif mode in ["Excel"]:                       # Excel
        s_texlive = location

# ------------------------------------------------------------------
def trailing(k, t):                               # last lines for the actual package
    """Completes the actual package."""
    
    global notice                                 # string for RIS/BibLaTeX + initialize
    global info_files
    global year_str
    global authorexists                           # flag

    kw = []                                       # keywords

    for child in k:                               # fetches and collects the keywords of a package
        if child.tag == "keyval":                 #   element keyval
            value = child.get("value", "")        #   attribute value
            kw.append(value + "; ")
    kw2 = "".join(kw)                             # collects all keywords in one string

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\end{labeling}" + "\n")
    elif mode in ["RIS"]:                         # RIS
        if not authorexists:
            out.write("AU  - " + userunknown + "\n")
        out.write("N1  - \n")                     # or U3
        out.write(notice + "\n")                  # or U3
        out.write("Y3  - " + t + "\n")
        out.write("ER  -\n\n")
    elif mode in ["plain"]:                       # plain
        pass                                      #   for plain do nothing
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        out.write("keywords".ljust(fieldwidth) + "= {" + kw2 + "},\n")
        out.write("note".ljust(fieldwidth) + "= {" + notice + "},\n")
        if info_files != "":
            out.write("file".ljust(fieldwidth) + "= {" + info_files + "},\n")
        out.write("}\n")
    elif mode in ["Excel"]:                       # Excel
        out.write(s_id)
        for f in [s_caption, s_authorref, s_version, s_license, s_contact, s_copyright, s_ctan,
                  s_documentation, s_home, s_install, s_keyval, s_miktex, s_texlive, s_also]:
            out.write("\t" + f)
        out.write("\n")

    notice      = ""                              # re-initalize variables
    info_files  = ""
    year        = ""
    year_str    = ""
    authorexists= False

# ------------------------------------------------------------------
def ul(k):                                        # element <ul>...</ul>
    """Processes the ul element."""

    # ul --> li

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\n\\begin{itemize}\n")
    if mode in ["RIS", "plain", "BibLaTeX"]:      # BibLaTeX / RIS / plain
        pass                                      #   for BibLaTeX / RIS / plain do nothing
    if mode in ["Excel"]:                         # Excel
        pass                                      #   for Excel do nothing

    for child in k:                               # searching for subelement li
        if child.tag == "li":                     #   child is li
            li(child)                             #   process this child

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\n\\end{itemize}\n")
    elif mode in ["RIS", "plain"]:                # RIS / plain
        pass                                      #   for RIS / plain do nothing
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        pass                                      #   for BibLaTeX do nothing
    elif mode in ["Excel"]:                       # Excel
        pass                                      #   for Excel do nothing

# ------------------------------------------------------------------
def version(k):                                   # element <version .../>
    """Processes the version element."""
    
    global notice                                 # string for RIS
    global version_str
    global s_version                              # string for Excel

    number = k.get("number", "")                  # attribute number
    date   = k.get("date", "")                    # attribute date
    tmp    = number

    if date != "":
        tmp = tmp + " (" + date + ")"             # version with date
    version_str = tmp

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Version] " + tmp + "\n")
    elif mode =="RIS":                            # RIS
        notice += " " * (fieldwidth + 2) + "Version: " + tmp + "; \n"
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "Version: ".ljust(labelwidth) + tmp)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        out.write("version".ljust(fieldwidth) + "= {" + tmp + "},\n")
        if date != "":
            out.write("date".ljust(fieldwidth) + "= {" + date + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_version = tmp

# ------------------------------------------------------------------
def make_tops():
    """Outputs the tops (.top) file."""
    
    # Topic list
    tops = open(direc + args.out_file + ".top", encoding="utf-8", mode="w")
    tops.write("% file: " + args.out_file + ".top" + "\n")
    tops.write("% date: " + actDate + "\n")
    tops.write("% time: " + actTime + "\n")
    tops.write("% is called by " + args.out_file + ".tex" + "\n\n")
    tops.write(r"\appendix" + "\n")
    tops.write(r"\section{Used Topics, Short Explainations}" + "\n\n")
    tops.write(r"\raggedright" + "\n")
    tops.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxx}" + "\n")

    for f in topics:
        if f in usedTopics:
            tmp = topics[f]
            tmp = re.sub(r"\\", r"\\textbackslash ", tmp)
            tops.write(r"\item[\texttt{" + f + "}] " + tmp)
            tops.write(r"\index{Topic!" + f + "}\n")
    tops.write(r"\end{labeling}" + "\n")
    tops.close()                                  # close file
    if verbose:
        print("--- topic list created")

# ------------------------------------------------------------------
def make_xref():
    """Outputs the xref (.xref) file."""
    
    # Topics/Packages cross-reference
    xref = open(direc + args.out_file + ".xref", encoding="utf-8", mode="w")
    xref.write("% file: " + args.out_file + ".xref" + "\n")
    xref.write("% date: " + actDate + "\n")
    xref.write("% time: " + actTime + "\n")
    xref.write("% is called by " + args.out_file + ".tex" + "\n\n")
    xref.write(r"\section{Used Topics and related Packages}" + "\n\n")
    xref.write(r"\raggedright" + "\n")
    xref.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxx}" + "\n")

    xref.write("\n")
    for f in topics:                              # loop: all topics
        if f in usedTopics:                       # topic is used?
            xref.write(r"\item[\texttt{" + f + "}] ")
            xref.write(r"\index{Topic!" + f + "}")
            tmp1 = topicspackage[f]               # get the packages for this topic
            for ff in tmp1:                       # loop: all packages with this topic
                if ff in usedPackages:            # package is used?
                    ff = re.sub("_", "-", ff)
                    xref.write(r"\texttt{" + ff + "} " + r"(\ref{pkg:" + ff + "}); ")
            xref.write("\n")
    xref.write(r"\end{labeling}" + "\n")
    xref.close()                                  # close file
    if verbose:
        print("--- list with topics and related packages (cross-reference list) created")

# ------------------------------------------------------------------
def make_tap():
    """Outputs the tap (.tap) file."""
    
    # Authors/Packages cross-reference
    
    tap = open(direc + args.out_file + ".tap", encoding="utf-8", mode="w")
    tap.write("% file: " + args.out_file + ".tap" + "\n")
    tap.write("% date: " + actDate + "\n")
    tap.write("% time: " + actTime + "\n")
    tap.write("% is called by " + args.out_file + ".tex" + "\n\n")
    tap.write(r"\section{Authors and associated Packages}" + "\n\n")
    tap.write(r"\raggedright" + "\n")
    tap.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")

    tap.write("\n")
    for f in authors:
        if f in usedAuthors:
            if authors[f][1] != "":
                tmp2 = authors[f][1] + ", " + authors[f][0]
            else:
                tmp2 = authors[f][0]
            tap.write(r"\item[" + tmp2 + "] ")
            tap.write(r"\index{Author!" + tmp2 + "}")
            tmp1 = authorpackages[f]
            for ff in tmp1:
                if ff in usedPackages:
                    ff = re.sub("_", "-", ff)
                    tap.write(r"\texttt{" + ff + "} " + r"(\ref{pkg:" + ff + "}); ")
            tap.write("\n")
    tap.write(r"\end{labeling}" + "\n")
    tap.close()                                   # close file
    if verbose:
        print("--- list with authors and related packages (cross-reference list) created")

# ------------------------------------------------------------------
def make_stat():
    """Outputs statistics in the stat (.stat) file."""
    
    # writstatistics in the stat (.stat) file

    text1 = ""
    text2 = ""
    text3 = ""
    
    stat = open(direc + args.out_file + ".stat", encoding="utf-8", mode="w")
    stat.write("% file: " + args.out_file + ".stat" + "\n")
    stat.write("% date: " + actDate + "\n")
    stat.write("% time: " + actTime + "\n")
    stat.write("% is called by " + args.out_file + ".tex" + "\n\n")
    stat.write(r"\minisec{Parameters and Statistics}" + "\n\n")
    stat.write(r"\raggedright" + "\n")
    stat.write(r"\begin{tabular}{lrl}" + "\n")

    stat.write("\n")
    stat.write("program name "                   + r"& \verb§" + str(programname) + r"§\\" + "\n")
    stat.write("program version "                + r"&" + programversion + " (" + programdate + r")\\"  "\n")
    stat.write("program author "                 + r"&" + programauthor + r"\\\\"  "\n\n")

    stat.write("date of program execution "      + r"&" + actDate + r"\\"  "\n")
    stat.write("time of program execution "      + r"&" + actTime + r"\\\\"  "\n")
    
    stat.write("mode "                           + r"& \verb§" + mode + r"§\\" + "\n")
    if name_template == name_default:
        text1 = "(all packages = default)"
    stat.write("template for package names "     + r"& \verb§" + name_template + r"§ & " + text1 + r"\\" + "\n")
    if filter_key == filter_default:
        text2 = "(all topics = default)"
    stat.write("template for topics "            + r"& \verb§" + filter_key + r"§ & " + text2 + r"\\" + "\n")
    stat.write("special lists used\\footnotemark{} "        + r"&" + str(make_topics) + r"\\" + "\n")
    if skip == skip_default:
        text3 = "(no skipped fields = default)"
    stat.write("skipped CTAN fields "            + r"& \verb§" + skip + r"§ & " + text3 + r"\\\\" + "\n")
    
    stat.write("number of authors, total on CTAN "    + r"&" + str(len(authors)).rjust(6) + r"\\" + "\n")
    stat.write("number of authors, cited here "       + r"&" + str(len(usedAuthors)).rjust(6)  + r"\\" + "\n")
    stat.write("number of packages, total on CTAN "   + r"&" + str(len(packages)).rjust(6)  + r"\\" + "\n")
    stat.write("number of packages, described here "  + r"&" + str(len(usedPackages)).rjust(6)  + r"\\" + "\n")
    stat.write("number of topics, total on CTAN "     + r"&" + str(len(topics)).rjust(6)  + r"\\" + "\n")
    stat.write("number of topics, used here "         + r"&" + str(len(usedTopics)).rjust(6)  + r"\\" + "\n")
    stat.write(r"\end{tabular}" + "\n")
    stat.write("\\footnotetext{special lists: topic list + list with topics and related packages (cross-reference list)" +
               " + list with authors and related packages (cross-reference list)}\n")
    stat.close()                                  # close statistics file 
    if verbose:
        print("--- statistics written")

# ------------------------------------------------------------------
def make_statistics():
    """Outputs statistics on terminal."""

    l = left
    r = 5
    
    # Statistics on terminal
    print("\nStatistics\n")
    print("target format:".ljust(l + 1), mode)
    print("output file:".ljust(l + 1), out_file, "\n")
    print("number of authors, total on CTAN:".ljust(l),  str(len(authors)).rjust(r))
    print("number of authors, cited here:".ljust(l),   str(len(usedAuthors)).rjust(r))
    print("number of packages, total on CTAN:".ljust(l), str(len(packages)).rjust(r))
    print("number of packages, described here:".ljust(l),  str(len(usedPackages)).rjust(r))
    print("number of topics, total on CTAN:".ljust(l),   str(len(topics)).rjust(r))
    print("number of topics, used here:".ljust(l),    str(len(usedTopics)).rjust(r))

# ------------------------------------------------------------------
def process_packages():
    """Global loop"""

    # process_packages --> onepackage
    
    key      = filter_key
    keyexist = False

    for f in packages:                           # all XML files in loop
        fext   = f + ext                         # XML file name (with extension)
        haskey = False
        if f in packagetopics:
            tmptopic = packagetopics[f]
            for g in tmptopic:                   
                haskey = haskey or p3.match(g)
        keyexist = keyexist or haskey

        try:
            if p2.match(f) and haskey:           # 
                ff       = open(direc + fext, encoding="utf-8", mode="r")
                mod_time = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(fext)))
                onepackage(f, mod_time)          # process loaded XML file 
                ff.close()                       # loaded XML file closed
        except FileNotFoundError:                # specified XML file not found
            if verbose:
                print("----- XML file for package '" + f + "' not found")

    if not keyexist:                             # no package found with the specified topic(s)
        if verbose:
            print("----- key '" + key + "' not found")

    if counter <= 1:                             # no specified package found <=== error1
        if verbose:
            print("----- no correct XML file for any specified package found")

    if verbose:
        print("--- packages processed")

# ------------------------------------------------------------------
def main():
    """Main function"""

    # main --> first_lines
    # main --> process_packages
    # main --> make_tops
    # main --> make_xref
    # main --> make_tap
    # main --> make_stat
    # main --> make_statistics

    starttotal   = time.time()
    startprocess = time.process_time()
    
    first_lines()             # first lines of output
    process_packages()        # process all packages

    # ------------------------------------------------------------------
    # Generates topic list, topics and their packages (cross-reference), finish
    #
    if mode in ["LaTeX"] and make_topics: 
        make_tops()           # Topic list
        make_xref()           # Topics/Packages cross-reference
        make_tap()            # Authors/Packages cross-reference
        make_stat()           # Statistics on file

    # ------------------------------------------------------------------
    # The end
    #
    if mode in ["LaTeX"]:     # LaTeX
        out.write(trailer)    # output trailer
    out.close()               # close file
    if verbose:
        print("- program successfully completed")

    # ------------------------------------------------------------------
    # Statistics on terminal
    #
    if statistics:            # flag -stat is set
        make_statistics()     # output statistics on terminal
        
        endtotal   = time.time()
        endprocess = time.process_time()
        print("--")
        print("total time: ".ljust(left + 1), round(endtotal-starttotal, 2))
        print("process time: ".ljust(left + 1), round(endprocess-startprocess, 2))

  
#===================================================================
# Main Part

if __name__ == "__main__":
    main()
