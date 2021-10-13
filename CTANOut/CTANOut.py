#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANOut.py
# (C) Günter Partosch, 2019/2021

# Probleme/Ideen:
# - Idee: Klassenkonzept für die Ausgabe: für jeden Ausgabetyp eine eigene Klasse?
# - kann Zeitstempel bei XML/PDF-Dateien genutzt werden? wahrscheinlich nicht

# History
# ------------------------------------------------------------------
# 1.75 2021-05-14 more types for -m
# 1.76 2021-05-14 clean-up of variables
# 1.77 2021-05-15 more details in verbose mode for -mt
# 1.78 2021-05-15 output the call parameters in more details in verbose mode
# 1.79 2021-05-20 directory separator improved
# 1.80 2021-05-23 directory name improved
# 1.81 2021-05-24 directory handling (existance, installation) improved
# 1.82 2021-05-26 structure of CTAN.pkl adapted
# 1.83 2021-05-26 output of license information now with full text
# 1.84 2021-05-26 output and interpretaion of language codes improved
# 1.85 2021-05-27 correction of source errors in <version .../> in licenses.xml
# 1.86 2021-06-12 auxiliary function fold: shorten long option values for output
# 1.87 2021-06-12 messages classified: Warnings, Error, Infono package found which match
# 1.88 2021-06-13 string method str.format used (if applicable)
# 1.89 2021-06-18 some tiny improvements for output
# 1.90 2021-06-22 misc. smaller corrections
# 1.91 2021-06-24 additional minor corrections
# 1.82 2021-07-05 function fold restructured
# 1.93 2021-07-09 construct a unique author year string for BibLaTeX; two new auxiliary functions
# 1.94 2021-07-11 new functions: load_pickle1() and load_pickle2()
# 1.95 2021-07-12 new option -A; new functions: get_author_packages, get_name_packages, get_topic_packages; new procedure in process_packages
# 1.96 2021-07-14 new set of messages; new message no package found which match the specified '<kind of template>' template '<template>'
# 1.97 2021-07-15 error in make_xref() corrected
# 1.98 2021-07-16 verbose output enhanced (prevent the listing of non-existing packages); new function get_local_packages()
# 1.99 2021-07-19 make_stat, make_xref, make_tap respects option -A; output changed
# 1.100 2021-07-19 comments in BibLaTeX/LaTeX respects option -A
# 1.101 2021-07-19 new global variabel no_packages_processed: if set, all.tap,all.top,all.xref are not generated
# 1.102 2021-07-21 results are sorted
# 1.103 2021-07-21 only for LaTeX/BibLaTeX: output in comments is folded; new function comment_fold()
# 1.104 2021-07-21 only for LaTeX: output folded an 1st page of output; new function TeX_fold()
# 1.105 2021-07-26 results now alphabetically sorted; output improved

# ------------------------------------------------------------------
# Inspected CTAN elements

# also, authorref, caption, contact, copyright, ctan, description, documentation, home, keyval,
# license, miktex, name, texlive, version
# (useful for specifying a value list for the -s option)
#
# for example: -s "[description, version]"

# ------------------------------------------------------------------
# Messages

# Fatal Error
# Error: pickle file '<pickle file>' not found
# Error: tried to use the program indirectly

# Information
# Info: program successfully completed
# Info: file 'xyz.tap' created: [list with authors and related packages (cross-reference list)]
# Info: file 'xyz.top' created: [topic list]
# Info: file 'xyz.xref' created: [list with topics and related packages (cross-reference list)]
# Info: packages processed
# Info: program successfully completed
# Info: statistics written
# Info: statistics written

# Warnings
# Warning: 'option value' changed to 'option+value' (due to 'option')"
# Warning: XML file for package '<package>' not found
# Warning: XML file for package '<package>' not well-formed
# Warning: no correct local XML file for any specified package found
# Warning: no package found which matched the specified <kind of template> template '<template>'

# ------------------------------------------------------------------
# Usage
#
# usage: CTANOut.py [-h] [-a] [-A AUTHOR_TEMPLATE]
#                   [-b {@online,@software,@misc,@ctan,@www}] [-d DIREC]
#                   [-k FILTER_KEY]
#                   [-m {LaTeX,latex,tex,RIS,plain,txt,BibLaTeX,biblatex,bib,ris,Excel,excel,tsv}]
#                   [-mt] [-o OUT_FILE] [-s SKIP] [-t NAME_TEMPLATE] [-stat]
#                   [-v] [-V]
# 
# [CTANOut.py; Version: 1.105 (2021-07-26)] Convert CTAN XLM package files to
# LaTeX, RIS, plain, BibLaTeX, Excel [tab separated].
# 
# Options:
#   -h, --help            show this help message and exit
#   -a, --author          Show author of the program and exit.
#   -A AUTHOR_TEMPLATE, --author_template AUTHOR_TEMPLATE
#                         Name template for authors - Default:
#   -b {@online,@software,@misc,@ctan,@www}, --btype {@online,@software,@misc,@ctan,@www}
#                         Type of BibLaTex entries to be generated [only for -m
#                         BibLateX] - Default:
#   -d DIREC, --directory DIREC
#                         Directory for input and output files - Default: .\
#   -k FILTER_KEY, --key FILTER_KEY
#                         Template for output filtering on the base of keys -
#                         Default: ^.+$
#   -m {LaTeX,latex,tex,RIS,plain,txt,BibLaTeX,biblatex,bib,ris,Excel,excel,tsv}, --mode {LaTeX,latex,tex,RIS,plain,txt,BibLaTeX,biblatex,bib,ris,Excel,excel,tsv}
#                         Target format - Default: RIS
#   -mt, --make_topics    Flag: Generate topic lists [meaning of topics + cross-
#                         reference (topics/packages, authors/packages); only
#                         for -m LaTeX]). - Default: False
#   -o OUT_FILE, --output OUT_FILE
#                         Generic name for output files [without extensions] -
#                         Default: all
#   -s SKIP, --skip SKIP  Skip specified CTAN fields. - Default: []
#   -t NAME_TEMPLATE, --template NAME_TEMPLATE
#                         Template for package names - Default: ^.+$
#   -stat, --statistics   Flag: Print statistics on terminal. - Default: False
#   -v, --verbose         Flag: Output is verbose. - Default: False
#   -V, --version         Show version of the program and exit.
 
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
#     with verbose output (each processed package is shown)             [-v]
#
# CTANOut -v -stat
#     as above                                                          [-v]
#     but additionallay with statistics                                 [-stat]
#
# CTANOut -m BibLaTeX
#     BibLaTeX is output format                                         [-m]
#     no statistics
#     without verbose output
#
# CTANOut -m biblatex -b @online -v
#     as above                                                          [-m]
#     but now with verbose output and                                   [-v]
#     @online as BibLaTeX type                                          [-b]
#
# CTANOut -m bib -b @online -s [texlive,license,miktex] -v -stat
#     BibLaTeX is output format                                         [-m]
#     @online as BibLaTeX type                                          [-b]
#     with statistics                                                   [-stat]
#     skipped CTAN fields: texlive, license, and miktex                 [-s]
#
# CTANOut -m LaTeX -mt -v -stat
#     LaTeX is output format                                            [-m]
#     special topic lists are generated                                 [-mt]
#     with statistics and                                               [-stat]
#     verbose output                                                    [-v] 
#
# CTANOut -m latex -k LaTeX -mt
#     LaTeX is output format                                            [-m]
#     special topic lists are generated                                 [-mt]
#     packages are filtered by key template "LaTeX"                     [-k]
#
# CTANOut -m tex -t "l3|latex|ltx" -mt -v
#     packages with the name template "l3|latex|ltx"                    [-t]
#     LaTeX is output format                                            [-m]
#     special topic lists are generated                                 [-mt]
#     package names are filtered by name template "LaTeX"               [-t]
#
# CTANOut -m plain -v -stat -o myfile -s "[texlive,license,miktex]"
#     plain text is output format                                       [-m]
#     myfile.txt is the name for the output file                        [-o]
#     skipped CTAN fields: texlive, license, and miktex                 [-s]
#     with statistics and                                               [-stat]
#     verbose output                                                    [-v]
#
# CTANOut -A Knuth -k collection -t knuth -m bib -v -stat
#     packages with the author name template "Knuth"                    [-A]
#     only packages with the topic template "collection"                [-k]
#     only packages with the package name template "knuth"              [-t]
#     BibLaTeX is output format                                         [-m]
#     with statistics and                                               [-stat]
#     verbose output                                                    [-v]

# Regular expressions
# -------------------
# The options -t (a/o -to and -tl) and -k (a/o -ko and -kl) need regular expressions as values.
# such as
#
# -k latex                matches all topic names which contain "latex"
# -t "latex|ltx|l3|lt3"   matches all file names which contain "latex", "ltx", "l3|" or "t3"
# -t "^.+$"               matches all file names
# -t "^{a-b]"             matches all file names which begin with letters a-b


#===================================================================
# Modules needed

import xml.etree.ElementTree as ET           # XML processing
import pickle                                # read pickle data, time measure
import time                                  # get time/date of a file
import re                                    # regular expression
import argparse                              # argument parsing
import sys                                   # system calls
import platform                              # get OS informations
import os                                    # OS relevant routines
from os import path                          # path informations


#===================================================================
# Functions in CTANOut.py

# fold(s)            auxiliary function: shorten long option values for output
# get_authoryear(a,y) auxiliary function: construct a unique authoryear string (for BibLaTeX)
# get_local_packages(d) auxiliary function: get loal packages
# mod_TeXchars(s)    prepare characters for LaTeX/BibLaTeX in a paragraph
# TeXchars(s)        prepare characters for LaTeX/BibLaTeX

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
# li(k)              element <li> ... </li>
# licenseT(k)        element <license .../>
# mod_a(k)           element <a ...> ... </a>
# miktex(k)          element <miktex .../>
# mod_b(k)           element <b> ... </b>
# mod_br(k)          element <br/>
# mod_em(k)          element <em> ... </em>
# mod_i(k)           element <i> ... </i>
# mod_pre(k)         element <pre> ... </pre>
# mod_tt(k)          element <tt> ... </tt>
# mod_xref(k)        element <xref ...> ... </xref>
# name(k)            element <name> ... </name>
# p(k)               element <p> ... </p>
# texlive(k)         element <texlive .../>
# ul(k)              element <ul> ... </ul>
# version(k)         element <version .../>
# xref(k)            element <xref ...> ... </xref>

# first_lines()      Analyze the first lines of each package XML file and output some lines.
# get_pickle1()      load pickle file 1
# get_pickle2()      load pickle file 2
# get_year(s)        auxiliary function: get the most recent year in string s (only for BibLaTeX)
# leading(k)         first lines of one package
# main()             main function
# make_stat()        generate statistics file (xyz.stat for -m LaTeX a/o -m BibLaTeX).
# make_statistics()  generate general statitics part (-stat) on terminal
# make_tap()         generate xyz.tap
# make_tops()        generate xyz.top
# make_xref()        generate xyz.xref
# mod_backslash(s)   special processing of \ in the source text
# onepackage(s, t)   open a file with the package description and initialize XML processing
# process_packages() general loop
# trailing(k, t)     last lines of a package part

# main --> load_pickle1
# main --> load_pickle2
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
#                                                        leading       --> getyear
#                                                        leading       --> get_authoryear
#                                              entry --> licenseT
#                                              entry --> miktex
#                                                        miktex        --> TeXchars
#                                              entry --> name
#                                                        name          --> TeXchars
#                                              entry --> texlive
#                                                        texlive       --> TeXchars
#                                              entry --> trailing
#                                              entry --> version
#          process_packages --> get_topic_packages
#          process_packages --> get_name_packages
#          process_packages --> get_author_packages
#          process_packages --> get_local_packages

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


#===================================================================
# Settings

programname       = "CTANOut.py"
programversion    = "1.105"
programdate       = "2021-07-26"
programauthor     = "Günter Partosch"
documentauthor    = "Günter Partosch"
authorinstitution = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"
authoremail       = "Guenter.Partosch@hrz.uni-giessen.de"
documenttitle     = "The CTAN book -- Packages on CTAN"
documentsubtitle  = "Collected, prepared and selected with the aid of the program "

operatingsys      = platform.system()        # operating system
call              = sys.argv                 # actual program call
calledprogram     = sys.argv[0]              # name of program in call

# ------------------------------------------------------------------
# Global settings

ctanUrl           = "https://ctan.org"       # head of a CTAN url
ctanUrl2          = ctanUrl + "/tex-archive" # head of another CTAN url
ctanUrl3          = ctanUrl2 + "/install"    # head of another CTAN url
ctanUrl4          = ctanUrl + "/pkg/"        # head of another CTAN url
labelwidth        = len("Documentation: ")   # width of the labels for LaTeX
actDate           = time.strftime("%Y-%m-%d")# actual date of program execution
actTime           = time.strftime("%X")      # actual time of program execution

pickle_name1      = "CTAN.pkl"
pickle_name2      = "CTAN2.pkl"
list_info_files   = True                     # switch for RIS/BibLaTeX: XML_toc is to be proceeded
info_files        = ""                       # for BibLaTeX: collector for info file names
ext               = ".xml"                   # file name extension for downloaded info files
no_package_processed = False

maxcaptionlength  = 65                       # for LaTeX: max length for header lines
fieldwidth        = 10                       # for BibLaTeX: width of the field labels 

# ------------------------------------------------------------------
# Collect infos for elements which cannot be output in another way

notice          = ""                         # collecting infos
author_str      = ""                         # collecting authors of a package
year_str        = ""                         # collecting year informations
version_str     = ""                         # collecting version strings
counter         = 1                          # counts packages
left            = 35                         # width of labels in verbose output

# ------------------------------------------------------------------
# Texts for argument parsing

author_text          = "Show author of the program and exit."
author_template_text = "Name template for authors"
version_text         = "Show version of the program and exit."
verbose_text         = "Flag: Output is verbose."
statistics_text      = "Flag: Print statistics on terminal."   
topics_text          = "Flag: Generate topic lists [meaning of topics + cross-reference (topics/packages, authors/packages); only for -m LaTeX])."
btype_text           = "Type of BibLaTex entries to be generated [only for -m BibLateX]"
direc_text           = "Directory for input and output files"
key_text             = "Template for output filtering on the base of keys"
mode_text            = "Target format"
out_text             = "Generic name for output files [without extensions]"
program_text         = "Convert CTAN XLM package files to LaTeX, RIS, plain, BibLaTeX, Excel [tab separated]."
skip_text            = "Skip specified CTAN fields."
template_text        = "Template for package names"

# ------------------------------------------------------------------
# Defaults for argument parsing and further processing

make_topics_default     = False               # default for topics output (-mt)
verbose_default         = False               # default for global flag: verbose output (-v)
statistics_default      = False               # default for global flag: statistics output (-stat)
btype_default           = ""                  # default for BibLaTeX entry type (-b)
skip_default            = "[]"                # default for option -s
mode_default            = "RIS"               # default for option -m
name_template_default   = """^.+$"""          # default for file name template (-t)
out_default             = "all"               # default for out file
filter_key_default      = """^.+$"""          # default for topic filter (-k)
author_template_default = """^.+$"""          # default for author name template (-A)
##author_load_template_default = ""                  # default for author load name template (-Al)
##author_out_template_default  = ""                  # default for author out name template (-Ao)

act_direc       = "."                       # actual OS dirtectory
if operatingsys == "Windows":    
    direc_sep      = "\\"
else:
    direc_sep      = "/"
direc_default   = act_direc + direc_sep     # default for -d (output directory)

make_topics     = None                      # variable for -mt
verbose         = None                      # variable for -v
statistics      = None                      # variable for -stat
btype           = ""                        # variable for -b
skip            = ""                        # variable for -s
mode            = ""                        # variable for -m
name_template   = ""                        # variable for -t
author_template = ""                        # variable for -A
out_file        = ""                        # variable for -o
filter_key      = ""                        # variable for -k
direc           = ""                        # variable for -d

name_default    = name_template_default     # copy of name_template_default
filter_default  = filter_key                # copy of filter_key

default_text    = "no text"                 # default text for elements without embedded text
empty           = ""                        # default text in some cases
userunknown     = "N. N."                   # default text for elements without a correct author
ellipse         = " ..."
package_id      = ""                        # ID of a package
authorexists    = False                     # default for a global flag

err_mode        = "- Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
exclusion       = ["authors.xml", "topics.xml", "packages.xml", "licenses.xml"]

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
# python dictionaries and lists

languagecodes   = {"ar":"Arabic", "ar-dz":"Arabic (Algeria)", "bg":"Bulgarian", "bn":"Bengali",
                   "ca":"Catalan", "cs":"Czech", "da":"Danish", "de":"German", "de-de":"German (Germany)",
                   "el":"Greek", "en":"English", "eo":"Esperanto", "en-gb":"British", "es":"Spanish",
                   "es-ve":"Spanish (Venezuela)", "et":"Estonian", "eu":"Basque", "fa":"Farsi",
                   "fa-ir":"Farsi (Iran)", "fi":"Finnish", "fr":"French", "hi":"Hindi", "hr":"Croatian",
                   "hu":"Hungarian", "hy":"Armenian", "it":"Italian", "ja":"Japanese",
                   "ka":"Georgian", "ko":"Korean", "lv":"Latvian", "mn":"Mongolian", "mr":"Marathi", "nl":"Dutch",
                   "nn-no":"Nynorsk", "pl":"Polish", "pt":"Portuguese",
                   "pt-br":"Portuguese (Brazilia)", "ru":"Russian", "sk":"Slovak", "sr":"Serbian",
                   "sr-sp":"Serbian (Serbia)", "th":"Thai", "tr":"Turkish", "uk":"Ukrainian", "vi":"Vietnamese",
                   "zh":"Chinese", "zn-cn":"Chinese (China)", "de,en":"German + English", "zh,en":"Chinese + English",
                   "mr,hi":"Marathi + Hindi", "en,ja":"English + Japanese"}

usedTopics      = {}                        # Python dictionary:  collect used topics for all packages
usedPackages    = []                        # python list:        collect used packages
usedAuthors     = {}                        # Python dictionary:  collect used authors for all packages
# usedTopics: Python dictionary (unsorted)
#   each element: <key for topic>:<number>
# usedPackages: python list
#   each element: <package name>
# usedAuthors: Python dictionary (unsorted)
#   each element: <key for author>:<tuple with givenname and familyname>

allauthoryears  = {}                        # python dictionary:  collect author name / year pairs

XML_toc         = {}                        # python dictionary:  list of XML and PDF files: XML_toc[CTAN address]=(XML file, key, plain PDF file name)authors         = {}
packages        = {}                        # python dictionary:  each element: <package key> <tuple with package name and package title>
topics          = {}                        # python dictionary:  each element: <topics name> <topics title>
licenses        = {}                        # python dictionary:  each element: <license key> <license title>
topicspackage   = {}                        # python dictionary:  each element: <topic key> <list with package names>
packagetopics   = {}                        # python dictionary:  each element: <topic key> <list with package names>
authorpackages  = {}                        # python dictionary:  each element: <author key> <list with package names>
authors         = {}                        # python dictionary:  each element: <author key> <tuple with givenname and familyname> 
# authors: Python dictionary (sorted)
#   each element: <author key> <tuple with givenname and familyname> 
# packages: Python dictionary (sorted)
#   each element: <package key> <tuple with package name and package title>
# topics: Python dictionary (sorted)
#   each element: <topics name> <topics title>
# licenses: Python dictionary (sorted)
#   each element: <license key> <license title>
# topicspackage: Python dictionary (unsorted)
#   each element: <topic key> <list with package names>
# packagetopics: Python dictionary (sorted)
#   each element: <topic key> <list with package names>
# authorpackages: Python dictionary (unsorted)
#   each element: <author key> <list with package names>


#===================================================================
# Parsing the arguments

parser = argparse.ArgumentParser(description = "[" + programname + "; " + "Version: " + programversion + " (" + programdate + ")] " + program_text)
parser._positionals.title = 'Positional parameters'
parser._optionals.title   = 'Options'

parser.add_argument("-a", "--author",       # Parameter -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = programauthor + " (" + authoremail + ", " + authorinstitution + ")")

parser.add_argument("-A", "--author_template",             # Parameter -A/--author_template
                    help    = author_template_text + " - Default: " + "%(default)s",
                    dest    = "author_template",
                    default = author_template_default)

parser.add_argument("-b", "--btype",        # Parameter -b/--btype
                    help    = btype_text + " - Default: " + "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan", "@www"],
                    dest    = "btype",
                    default = btype_default)

parser.add_argument("-d", "--directory",    # Parameter -d/--directory
                    help    = direc_text + " - Default: " + "%(default)s",
                    dest    = "direc",
                    default = direc_default)

parser.add_argument("-k", "--key",          # Parameter -k/--key
                    help    = key_text + " - Default: " + "%(default)s",
                    dest    = "filter_key",
                    default = filter_key_default)

parser.add_argument("-m", "--mode",         # Parameter -m/--mode
                    help    = mode_text + " - Default: " + "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "plain", "txt", "BibLaTeX", "biblatex", "bib", "ris", "Excel", "excel", "tsv"],
                    dest    = "mode",
                    default = mode_default)

parser.add_argument("-mt", "--make_topics", # Parameter -mt/--make_topics
                    help    = topics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_topics_default)

parser.add_argument("-o", "--output",       # Parameter -o/--output
                    help    = out_text + " - Default: " + "%(default)s",
                    dest    = "out_file",
                    default = out_default)

parser.add_argument("-s", "--skip",         # Parameter -s/--skip
                    help    = skip_text + " - Default: " + "%(default)s",
                    dest    = "skip",
                    default = skip_default)

parser.add_argument("-t", "--template",     # Parameter -t/--template
                    help    = template_text + " - Default: " + "%(default)s",
                    dest    = "name_template",
                    default = name_template_default)

parser.add_argument("-stat", "--statistics",# Parameter -stat/--statistics
                    help    = statistics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics_default)

parser.add_argument("-v", "--verbose",      # Parameter -v/--verbose
                    help    = verbose_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = verbose_default)

parser.add_argument("-V", "--version",      # Parameter -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + programversion + " (" + programdate + ")")

# ------------------------------------------------------------------
# Getting parsed values

args            = parser.parse_args()
author_template = args.author_template        # parameter -A
btype           = args.btype                  # Parameter -b
direc           = args.direc                  # Parameter -d
make_topics     = args.make_topics            # Parameter -mt
mode            = args.mode                   # Parameter -m
name_template   = args.name_template          # Parameter -t
out_file        = args.out_file               # Parameter -o
filter_key      = args.filter_key             # Parameter -k
skip            = args.skip                   # Parameter -s
verbose         = args.verbose                # Parameter -v
statistics      = args.statistics             # Parameter -stat

# ------------------------------------------------------------------
# Resettings and settings

if mode in ["latex", "LaTeX", "tex"]:       # -m latex in call
    mode = "LaTeX"                          #   mode is reset
if mode in ["ris", "RIS"]:                  # -m ris in call
    mode = "RIS"                            #   mode is reset 
if mode in ["biblatex", "BibLaTeX", "bib"]: # -m biblatex in call
    mode = "BibLaTeX"                       #   mode is reset
if mode in ["excel", "Excel", "tsv"]:       # -m excel in call
    mode = "Excel"                          #   mode is reset
if mode in ["plain", "txt"]:                # -m plain in call
    mode = "plain"                          #   mode is reset
if (btype == "") and (mode == "BibLaTeX"):  # for BibLaTeX: if btype is set
    btype = "@www"                          #   btype is reset

if (btype != btype_default) and (mode != "BibLaTeX"): 
    if verbose:
        print(err_mode.format('-m', mode, '-m BibLaTeX', '-b')) # "- Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
    mode = "BibLaTeX"                       # mode is set to BibLaTeX if -b is given

if (make_topics != make_topics_default) and (mode != "LaTeX"):
    if verbose:
        print(err_mode.format('-m', mode, '-m LaTeX', '-mt'))
    mode = "LaTeX"                          # mode is set to LaTeX if -mt is given

# ------------------------------------------------------------------
# Correct directory name, test directory existence, and/or install directory

direc = direc.strip()                       # correct directory name (-d)
if direc[len(direc) - 1] != direc_sep:
    direc += direc_sep
if not path.exists(direc):                  # make OS directory, if necessary 
    try:
        os.mkdir(direc)
    except OSError:
        print ("- Warning: Creation of the OS directory '{0}' failed".format(direc))
    else:
        print ("- Info: Successfully created OS the directory '{0}' ".format(direc))

# ------------------------------------------------------------------
# pre-compiled regular expressions (based on specified options)

p2 = re.compile(name_template)   # regular expression based on -t
p3 = re.compile(filter_key)      # regular expression based on -k
p4 = re.compile("[- |.,a-z]")    # split a string to find year data
p5 = re.compile(author_template) # regular expression based on -A
p6 = re.compile("^.+[.]xml$")    # regular expression for local XML file names

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
%\\usepackage{lmodern}                   % font lmodern; not necessary
\\usepackage[colorlinks=true]{hyperref}  % hypertext structures\n
\\newcommand{\inp}[1]{\\IfFileExists{#1}{\\input{#1}}{}}\n
\\makeindex\n"""
    
    title        = """
\\title{""" + documenttitle + """}
\\subtitle{""" + documentsubtitle + "\\texttt{" + programname + """}}
\\author{""" + documentauthor + """}
\\date{\\today}\n"""
    
    header       = "\n\\begin{{document}}\n \\pagestyle{{headings}}\n \\maketitle\n \\inp{{{0}.stat}}\n \\newpage\n".format(args.out_file)
    trailer      = ""
    if make_topics:                          # if -mt is specified
        trailer = trailer + "\n\\newpage\n\\appendix"   
        trailer = trailer + "\n\\inp{" + args.out_file + ".top}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".xref}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".tap}"
    trailer = trailer + "\n\\printindex\n\\end{document}\n"


# ======================================================================
# auxiliary functions

# ------------------------------------------------------------------
def fold(s):                                               # function fold: auxiliary function: shorten long option values for output
    """auxiliary function: shorten/fold long option values for normal output"""
    
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
            out = out + line + "\n" + offset
            line = ""
    out = out + line            
    return out

# ------------------------------------------------------------------
def TeX_fold(s):                                               # function fold: auxiliary function: shorten long option values for output
    """auxiliary function: shorten/fold long option values in LaTeX tabular output"""
     
    offset = 64 * " "
    maxlen = 70
    sep    = "|"
    parts  = s.split(sep)
    line   = ""
    out    = ""
    for f in range(0,len(parts) ):
        if f != len(parts) - 1:
            line = line + "\\verb§" + parts[f] + sep + "§"
        else:
            line = line + "\\verb§" + parts[f] + "§"
        if len(line) >= maxlen:
            out = out + line + "\\\\\n" + offset + "&"
            line = ""
    out = out + line            
    return out

# ------------------------------------------------------------------
def comment_fold(s):                                            # function fold: auxiliary function: shorten long option values for output
    """auxiliary function: shorten/fold long option values in LaTeX comment output"""
     
    offset = 28 * " "
    maxlen = 120
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
            out = out + line + "\n%" + offset + ": "
            line = ""
    out = out + line            
    return out

# ------------------------------------------------------------------
def get_authoryear(a, y):
    """auxiliary function: construct a unique authoryear string (for BibLaTeX)
    perform some changes according to the BibLaTeX rules

    a: tuple author (name, givenname)
    y: int year"""

    global allauthoryears
    
    (name, givenname) = a
    if (name == "") and (givenname != ""):                       # if name ist not given
        name = givenname
        
    name = re.sub("工作室", "", name)                             # some changes  —
    name = re.sub("Jr", "", name)
    name = re.sub("[-., /'—]", "", name)
    name = re.sub("Ø", "O", name)
    name = re.sub("ß", "ss", name)
    name = re.sub("Á", "A", name)
    name = re.sub("à", "a", name)
    name = re.sub("á", "a", name)
    name = re.sub("ä", "ae", name)
    name = re.sub("ç", "c", name)
    name = re.sub("è", "e", name)
    name = re.sub("é", "e", name)
    name = re.sub("ì", "i", name)
    name = re.sub("í", "i", name)
    name = re.sub("ñ", "n", name)
    name = re.sub("ò", "o", name)
    name = re.sub("ó", "o", name)
    name = re.sub("õ", "o", name)
    name = re.sub("ö", "oe", name)
    name = re.sub("ø", "o", name)
    name = re.sub("ù", "u", name)
    name = re.sub("ú", "u", name)
    name = re.sub("ü", "ue", name)
    name = re.sub("ý", "y", name)
    name = re.sub("ć", "c", name)
    name = re.sub("č", "c", name)
    name = re.sub("ř", "r", name)
    name = re.sub("š", "s", name)
    name = re.sub("Ž", "Z", name)
    tmp  = name + str(y)                                         # construct an author year string
    if not (tmp in allauthoryears):                              # store it in a dictionary
        allauthoryears[tmp] = ord("a") - 1
    else:
        tmp2  = allauthoryears[tmp]                               # append a small letter (the next in the alphabet)
        tmp2 += 1
        allauthoryears[tmp] = tmp2
        if tmp2 <= 122: 
            tmp = name + str(y) + "." + chr(tmp2)
        else:
            remain = (tmp2 - 97) % 26 + 1
            times  = (tmp2 - 97) // 26
            tmp    = name + str(y) + "." + chr(times + 96) + chr(remain + 96)
    return tmp

# ------------------------------------------------------------------
def get_year(s):
    """auxiliary function: get the most recent year in string s (only for BibLaTeX)
    include decimal numbers in the intervall [1980, 2050]

    s: string"""
    
    nn    = p4.split(s)                                          # split the given string according p4
    years = []
    for i in nn:                                                 # loop over all elements
        if i.isdecimal():                                        # element is decimal
            if (1980 <= int(i)) and (int(i) <= 2050):            # element is in the intervall [1980, 2050]
                years.append(int(i))                             # element is collected
    if len(years) >= 1:
        return max(years)                                        # maximum is calculated
    else:
        return None
    
# ------------------------------------------------------------------
def get_local_packages(d):                                       # Function get_local_packages(d): auxiliary function: List all local packages in the OS directory 
    """auxiliary function: List all local packages in the OS directory d"""

    tmp  = os.listdir(d)                                         # get OS directory list
    tmp2 = []
    
    for f in tmp:
        if p6.match(f) and not f in exclusion:
            tmp3 = f[0:len(f) - 4]
            tmp2.append(tmp3)
    return set(tmp2)

# ------------------------------------------------------------------
def mod_backslash(s):                             # function: special processing von \ in the source text
    """special processing von \ in the source text"""
    
    res = re.sub(r"\\", r"§§3textbackslash ",s)
    return res

# ------------------------------------------------------------------
def mod_TeXchars(s):                              # function: prepare characters for LaTeX/BibLaTeX in a paragraph
    """Prepare characters for LaTeX/BibLaTeX in a paragraph."""

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
    tmp = re.sub(r"\^", r"§§3textasciicircum ", tmp) # change ^
    tmp = re.sub("§§1", "{", tmp)                 # re-change {
    tmp = re.sub("§§2", "}", tmp)                 # re-change }
    tmp = re.sub("§§3", r"\\", tmp)               # re-change \
    tmp = re.sub("&", r"{\\&}", tmp)              # change &
    return tmp

# ------------------------------------------------------------------
def TeXchars(s):                                   # function: prepare characters for LaTeX/BibLaTeX
    """prepares characters for LaTeX/BibLaTeX"""
    
    tmp = s
    tmp = re.sub(r"\\", r"\\textbackslash ", tmp)
    tmp = re.sub("_", r"\\_", tmp)
    tmp = re.sub("&", r"{\\&}", tmp)
    tmp = re.sub(r"[\^]", r"\\textasciicircum ", tmp)
    tmp = re.sub("[$]", r"\\$", tmp)
    return tmp


# ==================================================================
# main functions

# ------------------------------------------------------------------
def alias(k):                                     # function: element <alias .../>
    """Process the alias element."""

    global notice

    id  = k.get("id", "")                         # attribute id
    
    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                             
    else:
        tmp = default_text                        # if k.text is empty

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Alias] " + r"\texttt{" + tmp + "}\n")
        out.write("\\index{{Package!{0} (alias for {1})}}\n".format(tmp, package_id))
        out.write("\\index{{Alias!{0} (for {1})}}\n".format(tmp, package_id))
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
def also(k):                                      # function: element <also .../>
    """Process the also element."""

    # also --> TeXchars
    
    global s_also                                 # string for Excel

    refid = k.get("refid","")                     # attribute refid

    if mode in ["LaTeX"]:                         # LaTeX
        refid2 = re.sub("_", "-", refid)          #   substitute "_"
        if refid in packages:
            tmp1   = TeXchars(packages[refid][0])
            tmp2   = TeXchars(packages[refid][1])
            out.write("\\item[see also] see section~\\ref{{pkg:{0}}} on page~\\pageref{{pkg:{1}}}: (\\texttt{{{2}}} -- {3})\n".format(refid2, refid2, tmp1, tmp2))
    elif mode in ["plain"]:                       # plain
        if refid in packages:
            out.write("\n" + "see also: ".ljust(labelwidth) + refid + " (" + packages[refid][0] + " -- " + packages[refid][1] + ")")
    elif mode in ["RIS"]:                         # RIS
        pass                                      #   for RIS do nothing
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if refid in packages:
            out.write("related".ljust(fieldwidth) + "= {" + refid + "},\n")
    elif mode in ["Excel"]:                       # Excel
        if refid in packages:
            if s_also != "":
                s_also += "; " + refid            # accumulate s_also string 
            else:
                s_also = refid

# ------------------------------------------------------------------
def authorref(k):                                 # function: element <authorref .../>
    """Process the authorref element, construct the complete name and usedAuthors entry."""
    
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
        out.write("\\item[Author]{0}\n".format(tmp))
        out.write("\\index{{Author!{0}}}\n".format(tmp2)) ######
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
def caption(k):                                   # function: element <caption>...</caption>
    """Process the caption element."""

    # caption --> TeXchars
    
    global s_caption                              # string for Excel

    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                              
    else:
        tmp = default_text                        #   if k.text is empty

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        tmp = re.sub("#", "\\#", tmp)
        out.write("\\item[Caption] {0}\n".format(tmp))
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
def contact(k):                                   # function: element <contact .../>
    """Process the contact element."""
    
    global notice
    global s_contact                              # string for Excel

    typeT = k.get("type", "")                     # attribute type (announce, bugs, development, repository, support)
    href  = k.get("href", "")                     # attribute href

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[Contact] \\textit{{{0}}}: \\url{{{1}}}\n".format(typeT, href))
        out.write("\\index{{Contact!{0}}}\n".format(typeT))
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "Contact: " + typeT + ": " + href + ";\n"
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
def copyrightT(k):                                # function: element <copyright .../>
    """Process the copyright element."""

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
        out.write("\\item[Copyright] {0}\n".format(tmp))
    elif mode in ["RIS"]:                         # RIS
        out.write("PY  - {0}\n".format(year))
        notice += " " * (fieldwidth + 2) + "Copyright: " + tmp + ";\n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = re.sub("_", r"\\_", tmp)
        tmp = TeXchars(tmp)
        notice += "Copyright: " + tmp + ";\n"     # accumulate notice string
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
def ctan(k, t):                                   # function: element <ctan .../>
    """Process the ctan element."""
    
    global s_ctan                                 # string for Excel
    global notice

    path = k.get("path", "")                      # attribute path
    file = k.get("file", "")                      # attribute file

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[on CTAN] \\url{{{0}}}\n".format(ctanUrl2 + path))
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
def description(k):                               # function: element <description ...> ... </description>
    """Process the description element."""

    # description --> p
    # description --> ul
    
    language = k.get("language", "")              # attribute language

    if language in languagecodes:                 # convert language keys
        languagex = languagecodes[language]
    else:
        languagex = ""

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[Description]{0}".format(languagex))
        if languagex != "":
            out.write("\\index{{Language in description/documentation!{0}}}\n".format(languagex))
    elif mode in ["RIS"]:                         # RIS
        out.write("AB  - {0}\n".format(languagex))
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
def documentation(k):                             # function: element <documentation .../>
    """Process the documentation element."""

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
            out.write("\\index{{Language in description/documentation!{0}}}\n".format(languagecodes[language]))
        if p == None:                             #   no language found in details
            out.write("\\item[Documentation]{0} \\textit{{{1}}}: \\url{{{2}}}\n".format(languagex, details, href2))
        else:
            out.write("\\index{{Language in description/documentation!{0}}}\n".format(p.group()))
            out.write("\\item[Documentation] \\textit{{{0}}}: \\url{{{1}}}\n".format(details, href2))
    elif mode in ["RIS"]:                         # RIS
        if list_info_files:
            if href in XML_toc:
                tmp    = XML_toc[href]
                one_if = tmp[1] + "-" + tmp[2]    #   one info file
                fx     = os.path.abspath(one_if)
                out.write("L1  - {0}\n".format(fx))
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
            tmp = "Documentation{0}: {1}: {2}; \n".format(languagex, details, href2)
        else:
            tmp = "Documentation: {0}: {1}; \n".format(details, href2)
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
def entry(k, t):                                  # function: element <entry ...>...</entry>
    """Process the main element entry."""

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

    if mode in ["Excel"]:                         # initialize strings for Excel
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

    for child in k:                               # call the sub-elements
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
def first_lines():                                          # function: create the first lines of output.
    """create the first lines of output"""
    
    arguments   = ""
    tmp         = ""
    tmp_before  = ""
    e_parameter = ["-t","-k","--template","--key", "-s", "--skip"]
     
    for f in range(1,len(call)):
        tmp = call[f]
        if tmp_before in e_parameter:
            tmp = '"' + tmp + '"'
        arguments = arguments + tmp + " "
        tmp_before = tmp

    if verbose:
        print("- Program call:", programname, arguments)
        
    if verbose:                                             # header for terminal output
        print("\n- program call (with details): CTANOut.py")
        if ("-mt" in call) or ("--make_topics" in call):    print("  {0:5} {1:55}".format("-mt", "(" + (topics_text + ")")[0:50] + ellipse))
        if ("-stat" in call) or ("--statistics" in call):   print("  {0:5} {1:55}".format("-stat", "(" + statistics_text + ")"))
        if ("-v" in call) or ("--verbose" in call):         print("  {0:5} {1:55}".format("-v", "(" + verbose_text + ")"))
        if ("-d" in call) or ("--directory" in call):       print("  {0:5} {2:55} {1}".format("-d", direc, "(" + direc_text + ")"))
        if ("-m" in call) or ("--mode" in call):            print("  {0:5} {2:55} {1}".format("-m", mode, "(" + mode_text + ")"))
        if ("-o" in call) or ("--output" in call):          print("  {0:5} {2:55} {1}".format("-o", args.out_file, "(" + out_text + ")"))
        if ("-b" in call) or ("--btype" in call):           print("  {0:5} {2:55} {1}".format("-b", btype, "(" + (btype_text + ")")[0:50] + ellipse))
        if ("-k" in call) or ("--key" in call):             print("  {0:5} {2:55} {1}".format("-k", fold(filter_key), "(" + key_text + ")"))
        if ("-s" in call) or ("--skip" in call):            print("  {0:5} {2:55} {1}".format("-s", skip, "(" + skip_text + ")"))
        if ("-A" in call) or ("--author_template" in call): print("  {0:5} {2:55} {1}".format("-A", fold(author_template), "(" + author_template_text + ")"))
        if ("-t" in call) or ("--template" in call):        print("  {0:5} {2:55} {1}".format("-t", fold(name_template), "(" + template_text + ")"))
        print("\n")

    if mode in ["LaTeX"]:                                   # LaTeX
        out.write("% File: {0}\n\n".format(out_file))
        out.write("% Date: {0}\n".format(actDate))
        out.write("% Time: {0}\n\n".format(actTime))
        out.write("% generated by {0} (version  : {1} of {2})\n\n".format(programname, programversion, programdate))
        out.write("% Program call               : {0} {1}\n".format(programname, arguments))
        out.write("% mode                       : {0}\n".format(mode))
        out.write("% skipped CTAN fields        : {0}\n".format(skip))
        if name_template != "":
            out.write("% filtered by name template  : '{0}'\n".format(comment_fold(name_template)))
        if filter_key != "":
            out.write("% filtered by key template   : '{0}'\n".format(comment_fold(filter_key)))
        if author_template != "":
            out.write("% filtered by author template: '{0}'\n".format(comment_fold(author_template)))
        out.write("\n% ---------------------------------------")
        out.write("\n% to be compiled with XeLaTeX or LuaLaTeX")
        out.write("\n% ---------------------------------------\n")
        out.write("\n\\documentclass[{0}\n]{{scrartcl}}\n".format(classoptions))
        out.write(usepkg)
        out.write(title)
        out.write(header)
    elif mode in ["BibLaTeX"]:                              # BibLaTeX
        out.write("% generated by {0} (version: {1} of {2})\n".format(programname, programversion, programdate))
        out.write("% File                       : {0}\n".format(out_file))
        out.write("% Mode                       : {0}\n".format(mode))
        out.write("% Date                       : {0}\n".format(actDate))
        out.write("% Time                       : {0}\n\n".format(actTime))
        out.write("% Program Call               : {0} {1}\n".format(programname, arguments))
        out.write("% skipped CTAN fields        : {0}\n".format(skip))
        out.write("% Type of BibLaTeX entries   : {0}\n".format(btype))
        if name_template != "":
            out.write("% filtered by name template  : {0}\n".format(comment_fold(name_template)))
        if filter_key != "":
            out.write("% filtered by key template   : {0}\n".format(comment_fold(filter_key)))
        if author_template != "":
            out.write("% filtered by author template: {0}\n".format(comment_fold(author_template)))
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
        out.write("generated by {0} (version: {1} of {2})\n".format(programname, programversion, programdate))
        out.write("file                     : {0}; mode: {1}; date: {2}; time: {3}\n".format(out_file, mode, actDate, actTime))
        out.write("program call             : CTAN-out.py {0}\n".format(arguments))
        out.write("skipped CTAN fields      : {0}\n".format(skip))
        if name_template != "":
            out.write("filtered by name template: {0}\n".format(name_template))
        if filter_key != "":
            out.write("filtered by key template : {0}\n".format(filter_key))
    elif mode in ["RIS"]:                                    # RIS
        pass                                                 #   for RIS do nothing
    elif mode in ["Excel"]:                                  # Excel; write head of table
        out.write("id")
        for f in ["caption", "authorref", "version", "license", "contact", "copyright", "CTAN",
                  "documentation", "home", "install", "keyval", "mikTeX", "TeXLive", "also"]:
            out.write("\t" + f)
        out.write("\n")

# ------------------------------------------------------------------
def get_author_packages():                                   # Function get_author_packages: Get package names by specified author name template
    """Get package names by specified author name template."""
    
    author_pack = set()                                      # initialize set
    tmp_set     = set()                                      # initialize auxiliary set
    
    for f in authors:                                        # loop over authors
        (gn, fn) = authors[f]
        if fn != "":                                         # get familyname
            tmp_a = authors[f][1]
        else:
            tmp_a = authors[f][0]                            # if an incorrect entry is in authors
        if p5.match(tmp_a):                                  # member matches template
            tmp_set.add(f)                                   # built-up a new auxiliary set
    for f in tmp_set:                                        # loop over auxiliary set
        if f in authorpackages:                              # prevent a wrong entry                         
            for g in authorpackages[f]:
                author_pack.add(g)                           # built-up the resulting set
    if len(author_pack) == 0:
        if verbose:
            print("----- Warning: no package found which matched the specified {0} template '{1}'".format("author", author_template))
    return author_pack

# ------------------------------------------------------------------
def get_topic_packages():                                    # Function get_topic_packages: Get package names by specified topic template.
    """Get package names by specified topic template."""
    
    topic_pack = set()                                       # initialize set
    
    for f in topicspackage:                                  # loop over topicspackage
        if p3.match(f):                                      # member matches template
            for g in topicspackage[f]:                       # all packagexs for this entry
                topic_pack.add(g)                            # built-up the resulting set
    if len(topic_pack) == 0:
        if verbose:
            print("----- Warning: no package found which matched the specified {0} template '{1}'".format("topic", filter_key))
    return topic_pack

# ------------------------------------------------------------------
def get_name_packages():                                     # Function get_name_packages: Get package names by specified package name template.
    """Get package names by specified package name template."""
    
    name_pack = set()                                        # initialize set
    
    for f in packages:                                       # loop over packages
        if p2.match(f):                                      # member matches template
            name_pack.add(f)                                 # built-up the resulting set
    if len(name_pack) == 0:
        if verbose:
            print("----- Warning: no package found which matched the specified {0}+ template '{1}'".format("name", name_template))
    return name_pack

# ------------------------------------------------------------------
def load_pickle1():
    """Get the structures authors, packages, topics, topicspackage, authorpackages (generated by CTANLoad.py)"""

    global authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages
    
    # authors: Python dictionary (sorted)
    #   each element: <author key> <tuple with givenname and familyname> 
    # packages: Python dictionary (sorted)
    #   each element: <package key> <tuple with package name and package title>
    # topics: Python dictionary (sorted)
    #   each element: <topics name> <topics title>
    # licenses: Python dictionary (sorted)
    #   each element: <license key> <license title>
    # topicspackage: Python dictionary (unsorted)
    #   each element: <topic key> <list with package names>
    # packagetopics: Python dictionary (sorted)
    #   each element: <topic key> <list with package names>
    # authorpackages: Python dictionary (unsorted)
    #   each element: <author key> <list with package names>

    try:                                        # try to open 1st pickle file 
        pickleFile1 = open(direc + pickle_name1, "br")
        (authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages) = pickle.load(pickleFile1)
        pickleFile1.close()                     #   close file
    except FileNotFoundError:                   # unable to open pickle file
        print("--- Error: pickle file '{0}' not found".format(pickle_name1))
        sys.exit("- Error: program is terminated")

# ------------------------------------------------------------------
def load_pickle2():
    """get XML_toc (generated by CTANLoad.py)"""

    global XML_toc
    
    try:                                        # try to open second pickle file
        pickleFile2 = open(direc + pickle_name2, "br")
        XML_toc     = pickle.load(pickleFile2)
        pickleFile2.close()                     #   close file
    except FileNotFoundError:                   # unable to open pickle file
        list_info_files = False
        print("--- Warning: pickle file '{0}' not found; local information files ignored".format(pickle_name2))

# ------------------------------------------------------------------
def home(k):                                      # function: element <home .../>
    """Process the home element."""
    
    global notice                                 # string for RIS/BibLaTeX
    global s_home                                 # string for Excel

    href = k.get("href", "")                      # attribute href

    if mode in ["LaTeX"]:                         # LaTeX 
        out.write("\\item[Home page] \\url{{{0}}}\n".format(href))
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
def install(k):                                   # function: element <install .../>
    """Process the install element."""
    
    global notice                                 # string for RIS/BibLaTeX
    global s_install                              # string for Excel

    path = k.get("path", "")                      # attribute path

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[Installation] \\url{{{0}}}\n".format(ctanUrl3 + path))
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
def keyval(k):                                    # function: element <keyval .../>
    """Process the keyval element."""

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
        out.write("\\item[Keyword] \\texttt{{{0}}} ({1})\n".format(value, tmp))
        out.write("\\index{{Topic!{0}}}\n".format(value))
    elif mode in ["RIS"]:                         # RIS
        out.write("KW  - {0}\n".format(value))
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
def leading(k):                                               # function: first lines of one package
    """Analyze the first lines of each package XML file and print out some lines."""

    # leading --> TeXchars
    # leading --> get_year
    # leading --> get_authoryear
    
    global authorexists                                       # flag

    xname = k.get("id", "")                                   # attribute id

    allauthors  = []                                          # initialize some variables
    year        = ""
    year_string = ""
    authorexists= False
    date        = ""
    year        = ""
    date_year_strings = ""
    
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
            date_year_strings += "|" + date
            if date != "":
               number += " (" + date + ")"
            if number != "":
                xcaption += "; version " + number

        if child.tag == "copyright":
            owner    = child.get("owner", "")                 # attribute owner
            year     = child.get("year", "--")                # attribute year
            date_year_strings += "|" + year

    if mode == "BibLaTeX":
        if len(allauthors) > 0:
            first_author = allauthors[0]
        else:
            first_author = None
        if (date != "") or (year != "--"):
            tmp5 = get_year(date_year_strings)
            if (tmp5 != None) and (first_author != None):
                xname = get_authoryear(first_author, tmp5)
            elif (tmp5 == None) and (first_author != None):
                tmp5 = ""
                xname = get_authoryear(first_author, tmp5)

    if mode in ["BibLaTeX"]:                                  # BibLaTeX
        allauthors2 = []                                      # generate author string for the current package
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
        out.write("\n\\section[{0}{1}]{{{2}{3}}}\\label{{pkg:{4}}}\n".format(tmp, xcaption2, tmp, xcaption, xname2))
        out.write("\\index{{Package!{0}}}\n\n".format(xname1))
        out.write("\\begin{labeling}{Documentation}\n")
    elif mode in ["RIS"]:                                     # RIS
        out.write("\nTY  - COMP" + "\n")
        out.write("T1  - {0}\n".format(xname))
        out.write("T4  - {0}\n".format(xcaption))
    elif mode in ["plain"]:                                   # plain
        tmp = xname + " -- " + xcaption
        out.write("\n\n\n" + tmp)
        out.write("\n" + len(tmp) * "-")
    elif mode in ["BibLaTeX"]:                                # BibLaTeX
        out.write("\n{0}{{{1},\n".format(btype, xname))
        out.write("author".ljust(fieldwidth) + "= {" + author_string + "},\n")
    elif mode in ["Excel"]:                                   # Excel
        pass                                                  #   for Excel do nothing
    authorexists = False

# ------------------------------------------------------------------
def li(k):                                        # function: element <li>...</li>
    """Process the li element."""

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
        tmptext = "\\item {0}\n".format(tmptext)
        out.write(tmptext)
    elif mode in ["Excel", "RIS", "plain", "BibLaTeX"]:
                                                  # BibLaTeX / RIS / plain / Excel
        tmptext = re.sub("[ ]+", " ", tmptext)
        tmptext = re.sub("[\n]+", "", tmptext)
        tmptext = "+ " + tmptext + "\n"
        out.write(tmptext)

# ------------------------------------------------------------------
def licenseT(k):                                  # function: element <license .../>
    """Process the license element."""
    
    global notice                                 # string for RIS/BibLaTeX
    global s_license                              # string for Excel

    typeT = k.get("type", "")                     # attribute type
    date  = k.get("date", "")                     # attribute date
    tmp   = typeT

    if tmp in licenses:
        tmp   = licenses[tmp]
    
    if date != "":                                # constructs lincense (date)
        tmp = "{0} (1)".format(tmp, date)

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[License] {0}\n".format(tmp))
        out.write("\\index{{License!{0}}}\n".format(tmp))
    elif mode in ["RIS"]:                         # RIS
        notice += " " * (fieldwidth + 2) + "License: " + tmp + "; \n"
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if notice != "":
            notice += " " * (fieldwidth + 2) + "License: " + tmp + "; \n"
        else:
            notice = "License: {0}; \n".format(tmp)
        out.write("userb".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "License: ".ljust(labelwidth) + tmp)
    elif mode in ["Excel"]:                       # Excel
        s_license = tmp

# ------------------------------------------------------------------
def main():                    # function: Main function
    """Main function"""

    # main --> load_pickle1
    # main --> load_pickle2
    # main --> first_lines
    # main --> process_packages
    # main --> make_tops
    # main --> make_xref
    # main --> make_tap
    # main --> make_stat
    # main --> make_statistics

    starttotal   = time.time()
    startprocess = time.process_time()

    load_pickle1()
    load_pickle2()
    
    first_lines()             # first lines of output
    process_packages()        # process all packages

    # ------------------------------------------------------------------
    # Generate topic list, topics and their packages (cross-reference), finish
    #
    if mode in ["LaTeX"] and make_topics: 
        if not no_package_processed:
            make_tops()           # Topic list
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".top"))
            
        if not no_package_processed:
            make_xref()           # Topics/Packages cross-reference
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".xref"))
            
        if not no_package_processed:
            make_tap()            # Authors/Packages cross-reference
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".tap"))
        make_stat()           # Statistics file (xyz.stat)

    # ------------------------------------------------------------------
    # The end
    #
    if mode in ["LaTeX"]:     # LaTeX
        out.write(trailer)    # output trailer
    out.close()               # close file
    if verbose:
        print("- Info: program successfully completed")

    # ------------------------------------------------------------------
    # Statistics on terminal
    #
    if statistics:            # flag -stat is set
        make_statistics()     # output statistics on terminal
        
        endtotal   = time.time()
        endprocess = time.process_time()
        print("--")
        print("total time: ".ljust(left + 2), round(endtotal-starttotal, 2))
        print("process time: ".ljust(left + 2), round(endprocess-startprocess, 2))

# ------------------------------------------------------------------
def make_stat():                                  # function: Generate statistics in the stat (xyz.stat) file.
    """Generate statistics in the stat (xyz.stat) file."""
    
    # write statistics in the stat (.stat) file

    text1 = ""
    text2 = ""
    text3 = ""
    text4 = ""
    
    stat = open(direc + args.out_file + ".stat", encoding="utf-8", mode="w")
    stat.write("% file: '{0}.stat'\n".format(args.out_file))
    stat.write("% date: {0}\n".format(actDate))
    stat.write("% time: {0}\n".format(actTime))
    stat.write("% is called by '{0}.tex'\n\n".format(args.out_file))
    
    stat.write(r"\minisec{Parameters and statistics}" + "\n\n")
    stat.write(r"\raggedright" + "\n")
    stat.write(r"\begin{tabular}{lll}" + "\n")

    stat.write("\n")
    stat.write("program name "                   + r"& \verb§" + str(programname) + r"§\\" + "\n")
    stat.write("program version "                + r"&" + programversion + " (" + programdate + r")\\"  "\n")
    stat.write("program author "                 + r"&" + programauthor + r"\\\\"  "\n\n")

    stat.write("date of program execution "      + r"&" + actDate + r"\\"  "\n")
    stat.write("time of program execution "      + r"&" + actTime + r"\\\\"  "\n")
    
    stat.write("mode "                           + r"& \verb§" + mode + r"§\\" + "\n")
    stat.write("special lists used\\footnotemark{} "        + r"&" + str(make_topics) + r"\\" + "\n")
    if skip == skip_default:
        text3 = "(no skipped fields = default)"
    stat.write("skipped CTAN fields "            + r"& \verb§" + skip + r"§  " + text3 + r"\\" + "\n")
    
    if name_template == name_default:
        text1 = "(all packages = default)"
    stat.write("template for package names "     + r"& " + TeX_fold(name_template) + r" " + text1 + r"\\" + "\n")
    
    if filter_key == filter_key_default:
        text2 = "(all topics = default)"
    stat.write("template for topics "            + r"& " + TeX_fold(filter_key) + r"  " + text2 + r"\\" + "\n")

    if author_template == author_template_default:
        text4 = "(all authors = default)"
    stat.write("template for author names "     + r"& " + TeX_fold(author_template) + r"  " + text4 + r"\\\\" + "\n")

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
        print("--- Info: statistics written")

# ------------------------------------------------------------------
def make_statistics():                            # function: Generate statistics on terminal.
    """Generate statistics on terminal."""

    l = left + 1
    r = 5
    
    # Statistics on terminal
    print("\nStatistics\n")
    print("target format:".ljust(l + 1), mode)
    print("output file:".ljust(l + 1), direc + out_file, "\n")
    print("number of authors, total on CTAN:".ljust(l),  str(len(authors)).rjust(r))
    print("number of authors, cited here:".ljust(l),   str(len(usedAuthors)).rjust(r))
    print("number of packages, total on CTAN:".ljust(l), str(len(packages)).rjust(r))
    print("number of packages, collected here:".ljust(l),  str(len(usedPackages)).rjust(r))
    print("number of topics, total on CTAN:".ljust(l),   str(len(topics)).rjust(r))
    print("number of topics, used here:".ljust(l),    str(len(usedTopics)).rjust(r))

# ------------------------------------------------------------------
def make_tap():                                   # function: Generate the tap (xyz.tap) file.
    """Generate the tap (xyz.tap) file."""
    
    # Authors/Packages cross-reference
        
    tap = open(direc + args.out_file + ".tap", encoding="utf-8", mode="w")
    tap.write("% file: '{0}.tap'\n".format(args.out_file))
    tap.write("% date: {0}\n".format(actDate))
    tap.write("% time: {0}\n".format(actTime))
    tap.write("% is called by '{0}.tex'\n\n".format(args.out_file))
    tap.write(r"\section{Authors and associated packages}" + "\n\n")
    tap.write(r"\raggedright" + "\n")
    tap.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")

    tap.write("\n")
    for f in authors:
        if f in usedAuthors:
            if authors[f][1] != "":
                tmp2 = authors[f][1] + ", " + authors[f][0]
            else:
                tmp2 = authors[f][0]
            tap.write("\\item[{0}] ".format(tmp2))
            tap.write("\\index{{Author!{0}}}".format(tmp2))
            tmp1 = authorpackages[f]
            package_no = 0
            for ff in tmp1:
                if ff in usedPackages:
                    package_no += 1
            if package_no == 1:
                text1 = " package: "
            else:
                text1 = " packages: "
            tap.write(str(package_no) + text1)
            for ff in tmp1:
                if ff in usedPackages:
                    ff = re.sub("_", "-", ff)
                    tap.write("\\texttt{{{0}}}~(\\ref{{pkg:{0}}}); ".format(ff, ff))
            tap.write("\n")
    tap.write(r"\end{labeling}" + "\n")
    tap.close()                                   # close file
    if verbose:
        print("--- Info: file '{0}.tap' created: [list with authors and related packages (cross-reference list)]".format(direc + args.out_file))

# ------------------------------------------------------------------
def make_tops():                                  # function: Generate the tops (xyz.top) file.
    """Generate the tops (xyz.top) file."""
    
    # Topic list
    tops = open(direc + args.out_file + ".top", encoding="utf-8", mode="w")
    tops.write("% file: {0}.top\n".format(args.out_file))
    tops.write("% date: {0}\n".format(actDate))
    tops.write("% time: {0}\n".format(actTime))
    tops.write("% is called by {0}.tex\n\n".format(args.out_file))
    
    tops.write(r"\appendix" + "\n")
    tops.write(r"\section{Used topics, short explainations}" + "\n\n")
    tops.write(r"\raggedright" + "\n")
    tops.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxx}" + "\n")
  
    for f in topics:
        if f in usedTopics:
            tmp = topics[f]
            tmp = re.sub(r"\\", r"\\textbackslash ", tmp)
            tops.write("\\item[\\texttt{{{0}}}] {1}".format(f, tmp))
            tops.write("\\index{{Topic!{0}}}\n".format(f))
    tops.write(r"\end{labeling}" + "\n")
    tops.close()                                  # close file
    if verbose:
        print("--- Info: file '{0}.top' created: [topic list]".format(direc + args.out_file))

# ------------------------------------------------------------------
def make_xref():                                  # function: Generate the xref (xyz.xref) file.
    """Generate the xref (xyz.xref) file."""
    
    # Topics/Packages cross-reference
    xref = open(direc + args.out_file + ".xref", encoding="utf-8", mode="w")
    xref.write("% file: {0}.xref\n".format(args.out_file))
    xref.write("% date: {0}\n".format(actDate))
    xref.write("% time: {0}\n".format(actTime))
    xref.write("% is called by '{0}.tex'\n\n".format(args.out_file))
    xref.write(r"\section{Used topics and related packages}" + "\n\n")
    xref.write(r"\raggedright" + "\n")
    xref.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxx}" + "\n")
    xref.write("\n")
    for f in topics:                              # loop: all topics
        if f in usedTopics:                       # topic is used?
            xref.write("\\item[\\texttt{" + f + "}] \\index{{Topic!" + f + "}}")
            tmp1 = topicspackage[f]               # get the packages for this topic
            package_nr = 0
            for ff in tmp1:                       # loop: all packages with this topic
                if ff in usedPackages:            #    package is used?
                    package_nr += 1               #    count the packages
            if package_nr == 1:
                text1 = " package: "
            else:
                text1 = " packages: "
            xref.write(str(package_nr) + text1)
            for ff in tmp1:                       # loop: all packages with this topic
                if ff in usedPackages:            #    package is used?
                    ff = re.sub("_", "-", ff)
                    xref.write("\\texttt{{{0}}}~(\\ref{{pkg:{1}}}); ".format(ff, ff))
            xref.write("\n")
    xref.write(r"\end{labeling}" + "\n")
    xref.close()                                  # close file
    if verbose:
        print("--- Info: file '{0}.xref' created: [list with topics and related packages (cross-reference list)]".format(direc + args.out_file))

# ------------------------------------------------------------------
def miktex(k):                                    # function: element <miktex .../>
    """Process the miktex element."""

    # miktex --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX
    global s_miktex                               # string for Excel

    location = k.get("location", "")              # attribute location

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(location)
        out.write("\\item[on Mik\TeX] \\texttt{{{0}}}\n".format(tmp))
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
def mod_a(k):                                     # function: element <a ...> ... </a>
    """Process the a element."""
    
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
            i.text = "§§3href§§1{0}§§2§§1{1}§§2".format(tmp2, i.text)
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "{0} ({1})".format(i.text, tmp2)
                                                  #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excek do nothing

# ------------------------------------------------------------------
def mod_b(k):                                     # function: element <b>...</b>
    """Process the b element."""
    
    ll = list(k.iter("b"))                        # fetch all b elements

    for i in ll:                                  # loop: all b elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3textbf§§1{0}§§2".format(i.text)
                                                  # change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "''{0}''".format(i.text)     #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_br(k):                                    # function: element <br/>
    """Process the br element."""
    
    ll = list(k.iter("br"))                       # fetch all b elements

    for i in ll:                                  # loop: all br elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3§§3"                     #   change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "\n"                         #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_em(k):                                    # function: element <em>...</em>
    """Process the em element."""
    
    ll = list(k.iter("em"))                       # fetch all em elements

    for i in ll:                                  # loop: all em elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3emph§§1{0}§§2".format(i.text)
                                                  #   change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "'{0}'".format(i.text)       #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_i(k):                                     # function: element <i>...</i>
    """Process the i element."""
    
    ll = list(k.iter("i"))                        # fetch all i elements

    for i in ll:                                  # loop: all i elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3emph§§1{0}§§2".format(i.text)
                                                  #   change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plaindef 
            i.text = "'{0}'".format(i.text)       #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_pre(k):                                   # function: element <pre>...</pre>
    """Process the pre element."""
    
    ll = list(k.iter("pre"))                      # fetch all i elements

    for i in ll:                                  # all: all pre elements
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "\n§§3begin§§1verbatim§§2\n{0}\n§§3end§§1verbatim§§2\n".format(i.text)
                                                  # change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "\n{0}\n".format(i.text)     #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_tt(k):                                    # function: element <tt>...</tt>
    """Process the tt element."""

    ll = list(k.iter("tt"))                       # fetch all tt elements

    for i in ll:                                  # loop: all tt elements
        tmp = i.text                              #   get embedded text
        
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = "§§3texttt§§1{0}§§2".format(tmp)
                                                  #   change embedded text
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "'{0}'".format(tmp)          #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_xref(k):                                  # function: element <xref ...> ... </xref>
    """Process the xref element."""
    
    # Now the element xref is used for inline-links, not a.
    
    ll = list(k.iter("xref"))                     # fetch all xref elements; ##1: {; ##2: }

    for i in ll:
        tmp  = i.attrib["refid"]                  # attribute refid
        tmp2 = ctanUrl4 + tmp
        
        if i.text == None:                        # no embedded textdef 
            i.text = tmp                          #   get embedded text
            
        if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
            i.text = re.sub("_", "-", i.text)     #   change embedded text
            i.text = "§§3href§§1{0}§§2§§1{1}§§2".format(tmp2, i.text)
        elif mode in ["RIS", "plain"]:            # RIS / plain
            i.text = "{0} {1})".format(i.text, tmp2)
                                                  #   change embedded text
        elif mode in ["Excel"]:                   # Excel
            pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def name(k):                                      # function: element <name>...</name>
    """Process the name element."""

    # name --> TeXchars
    
    global s_name                                 # string for Excel

    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                              
    else:                                         #   k.text is empty
        tmp = default_text                        

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        out.write("\\item[Name] \\texttt{{{0}}}\n".format(tmp))
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
def onepackage(s, t):                             # function: load a package XML file and start parsing
    """Load a package XML file and start parsing."""

    # onepackage --> entry
    
    global counter                                # counter for packages

    left = 33

    try:
        onePackage     = ET.parse(s + ext)        # parse XML file
    except:                                       # not successfull
        if verbose:
            print("----- Warning: XML file for package '{0}' not well-formed".format(s))
        return
    if verbose:
        print("    " + str(counter).ljust(5), "Package:", s.ljust(left), "Mode:", mode.ljust(7), "File:", direc + out_file.ljust(15))

    counter        = counter + 1                  # increment counter
    onePackageRoot = onePackage.getroot()         # get XML root 
    entry(onePackageRoot, t)                      # begin with entry element

# ------------------------------------------------------------------
def p(k):                                         # function: element <p> ... </p>
    """Process the p element."""

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
def process_packages():                          # function: Global loop
    """Global loop"""

    global no_package_processed

    # process_packages --> onepackage
    # process_packages --> get_topic_packages
    # process_packages --> get_author_packages
    # process_packages --> get_name_packages
    # process_packages --> get_local_packages
    
    all_packages = set()                         # initialize set
    for f in packages:
        all_packages.add(f)                      # construct a set object (packages has not the right format)
        
    tmp_tp = all_packages.copy()                 # initialize tmp_tp
    tmp_ap = all_packages.copy()                 # initialize tmp_ap
    tmp_np = all_packages.copy()                 # initialize tmp_np

    if filter_key != filter_key_default:
        tmp_tp = get_topic_packages()            # get packages by topic
    if author_template != author_template_default:
        tmp_ap = get_author_packages()           # get packages by author name
    if name_template != name_template_default:
        tmp_np = get_name_packages()             # get packages by package name

    tmp_pp = tmp_tp & tmp_ap & tmp_np & get_local_packages(direc)
    tmp_p  = sorted(tmp_pp)                      # built an intersection
                                                 
    for f in tmp_p:                              # all XML files in loop
        fext   = f + ext                         # XML file name (with extension)

        try:                                     # try to open file
            ff       = open(direc + fext, encoding="utf-8", mode="r")
            mod_time = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(fext)))
            onepackage(f, mod_time)              # process loaded XML file 
            ff.close()                           # loaded XML file closed
        except FileNotFoundError:                # specified XML file not found
            if verbose:
                print("----- Warning: XML file for package '{0}' not found".format(f))

    if counter <= 1:                             # no specified package found <=== error1
        if verbose:
            print("----- Warning: no correct local XML file for any specified package found")
        no_package_processed = True

    if verbose:
        print("--- Info: packages processed")

# ------------------------------------------------------------------
def texlive(k):                                   # function: element <texlive .../>
    """Process the texlive element."""

    # texlive --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX
    global s_texlive                              # string for Excel

    location = k.get("location", "")              # attribute location

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(location)
        out.write("\\item[on \\TeX Live] \\texttt{{{0}}}\n".format(tmp))
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
def trailing(k, t):                               # function: last lines for the actual package
    """Complete the actual package."""
    
    global notice                                 # string for RIS/BibLaTeX + initialize
    global info_files
    global year_str
    global authorexists                           # flag

    kw = []                                       # keywords

    for child in k:                               # fetch and collect the keywords of a package
        if child.tag == "keyval":                 #   element keyval
            value = child.get("value", "")        #   attribute value
            kw.append(value + "; ")
    kw2 = "".join(kw)                             # collect all keywords in one string

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\end{labeling}" + "\n")
    elif mode in ["RIS"]:                         # RIS
        if not authorexists:
            out.write("AU  - {0}\n".format(userunknown))
        out.write("N1  - \n")                     # or U3
        out.write(notice + "\n")                  # or U3
        out.write("Y3  - {0}\n".format(t))
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
def ul(k):                                        # function: element <ul>...</ul>
    """Process the ul element."""

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
def version(k):                                   # function: element <version .../>
    """Process the version element."""
    
    global notice                                 # string for RIS
    global version_str
    global s_version                              # string for Excel

    number = k.get("number", "")                  # attribute number
    date   = k.get("date", "")                    # attribute date
    tmp    = number
    if mode in ["LaTeX", "BibLaTeX"]:             # for LaTeX/BibLaTeX
        tmp    = re.sub("_", r"\\_", tmp)         #   correction

    if date != "":
        tmp = tmp + " (" + date + ")"             # version with date
    version_str = tmp

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[Version] {0}\n".format(tmp))
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

  
#===================================================================
# Main Part

if __name__ == "__main__":
    main()
else:
    if verbose:
        print("- Error: tried to use the program indirectly")
