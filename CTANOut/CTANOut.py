#!/usr/bin/python3
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

"""
CTANOut.py
(C) Günter Partosch, 2019|2021|2022|2023|2024|2025/2026

CTANOut.py is part of the CTAN bundle (CTANLoad.py, CTANOut.py,
CTANLoadOut.py, menu_CTANLoadOut.py).

CTANOut.py converts CTAN XLM package files to LaTeX, RIS, plain,
BibLaTeX, Excel [tab separated].

Call of CTANLoad.py
-------------------
CTANOut.py may be started by:

1. python -u CTANOut.py <option(s)>
-- always works
2. CTANOut.py <option(s)>
-- if the OS knows how to handle Python files (files with the name
   extension .py)
3. CTANOut <option(s)>
-- if there is an executable (in Windows a file with the name
   extension .exe)

Compilation:
-----------
 CTANout.py may be compiled by

 (a) pyinstaller
 pyinstaller --paths ... CTANOut.py -F
 --> provides CTANOut.exe (Windows)
 pyinstaller works under Linux in a similar way

 (b) nuitka

 (c) PyPy
 is only suitable to a limited extent, as only a limited Python can be
 interpreted

 --> provides CTANOut.exe (Windows) a/o CTANOut (Linux)

 Requirements:
 ------------
 + operating system windows 10/11 or Linux (like Linux Mint or Ubuntu or
   Debian)
 + wget a/o wget2 is installed and located in the current directory or
   in the path
 + Python installation 3.10 or newer
 + a series of Python modules (see the import instructions below)

Class:
-----
dataclass_variable          data class 

with method:
-----------
report                      Outputs the current values of the variables defined in
                            'dataclass_variable'.

Functions:
---------
argparse_process(dc=dc_var)             Defines the arguments for the
                                        program CTANOut and starts.
argparse_postprocess(dc=dc_var)         Postprocesses some parameters
                                        for the program CTANOut.
bibfield_test(s, f, dc=dc_var) ->bool   auxiliary function: output text
                                        is not empty and field is not to
                                        be skipped
biblatex_citationkey(dc=dc_var)         auxiliary function: Generates a
                                        set with citations keys for all
                                        packages
comment_fold(s, dc=dc_var) ->str        auxiliary function:
                                        shortens/folds long option
                                        values in LaTeX comment output
first_lines(dc=dc_var)                  function: creates the first
                                        lines of output.
fold(s, dc=dc_var) ->str                auxiliary function fold:
                                        shortens long option values for
                                        output 
gen_fold(s, o, dc=dc_var)               auxiliary function gen_fold:
                                        folds content of <p>, <li>, <dd>
                                        (mode dependant)
get_author_packages(dc=dc_var) ->set    Function get_author_packages:
                                        Gets package names by specified
                                        author name template
get_authoryear(a, y, dc=dc_var) ->str   auxiliary function
                                        get_authoryear: constructs a
                                        unique authoryear string
get_license_packages(dc=dc_var) ->set   Function get_license_packages:
                                        Gets package names by specified
                                        license template.
get_local_packages(d, dc=dc_var)        auxiliary function
                                        get_local_packages(d): Lists all
                                        local packages
get_name_packages(dc=dc_var) ->set      Function get_name_packages:
                                        Gets package names by specified
                                        package name template.
get_topic_packages(dc=dc_var) ->set     Function get_topic_packages:
                                        Gets package names by specified
                                        topic template.
get_year(s, dc=dc_var) ->int            auxiliary function: gets the
                                        most recent year in string s
                                        (only for BibLaTeX)
get_year_packages(, dc=dc_var) ->set    Function get_package_set:
                                        Analyzes dictionary yearpackages
load_pickle1(dc=dc_var)                 Function load_pickle1: l
                                        oads/unpacks pickle file 1
load_pickle2(dc=dc_var)                 Function load_pickle2:
                                        loads/unpacks pickle file 2
main(dc=dc_var)                         Main function (calls the other
                                        functions)
make_classoptions(dc=dc_var) -> str     auxiliary function: creates the
                                        uspackage part for LaTeX output.
make_header(dc=dc_var) -> str           auxiliary function: creates the
                                        document header part for LaTeX
                                        output.
make_lics(dc=dc_var)                    function: Generates the lics
                                        (xyz.lic) file.
make_stat(dc=dc_var)                    function: generates statistics
                                        in the stat file (xyz.stat)
make_statistics(dc=dc_var)              function: Generates statistics
                                        on terminal.
make_tap(dc=dc_var)                     function: Generates the tap
                                        (xyz.tap) file.
make_title(dc=dc_var) ->str             auxiliary function: creates the
                                        title part for LaTeX output.
make_tlp(dc=dc_var)                     function: Generates the tlp
                                        (xyz.tlp) file
make_tops(dc=dc_var)                    function: Generates the tops
                                        (xyz.top) file.
make_trailer(dc=dc_var) ->str           auxiliary function: creates the
                                        document trailer part for LaTeX
                                        output.
make_usepkg(dc=dc_var) ->str            auxiliary function: creates the
                                        uspackage part for LaTeX output.
make_xref(dc=dc_var)                    function: Generates the xref
                                        (xyz.xref) file.
onepackage(s, t, dc=dc_var)             function: loads a package XML
                                        file and start parsing
process_packages(dc=dc_var)             function: Global loop (over all
                                        selected packaged)
test_embedded(k, pp, dc=dc_var)         auxiliary function:
                                        tests current knot for embedded
                                        material
TeX_fold(s, dc=dc_var)                  auxiliary function TeX_fold:
                                        shortens/folds long option
                                        values in LaTeX tabular output
TeXchars(s, dc=dc_var)                  auxiliary function: prepares
                                        characters for LaTeX/BibLaTeX
TeXchars_restore(s, dc=dc_var) ->str    auxiliary function: restores
                                        characters for LaTeX/BibLaTeX
trailing(k, t, p, dc=dc_var)            function: last lines for the
                                        actual package
------------------------------------------------------------------
alias(k, dc=dc_var)                     function: processes element
                                        <alias .../>
also(k, dc=dc_var)                      function: processes element
                                        <also .../>
authorref(k, dc=dc_var)                 function: processes element
                                        <authorref .../>
caption(k, dc=dc_var)                   function: processes element
                                        <caption>...</caption>
contact(k, dc=dc_var)                   function: processes element
                                        <contact .../>
copyrightT(k, p, dc=dc_var)             function: processes element
                                        <copyright .../>
ctan(k, t, dc=dc_var)                   function: processes element
                                        <ctan .../>
description(k, pp, dc=dc_var)           function: processes element
                                        <description> ... </description>
documentation(k, dc=dc_var)             function: processes element
                                        <documentation .../>
entry(k, t, p, dc=dc_var)               function: processes element
                                        <entry ...>...</entry>
home(k, dc=dc_var)                      function: processes element
                                        <home .../>
install(k, dc=dc_var)                   function: processes element
                                        <install .../>
keyval(k, dc=dc_var)                    function: processes element
                                        <keyval .../>
leading(k, p, t, dc=dc_var)             function: first lines for
                                        package output
licenseT(k, dc=dc_var)                  function: processes element
                                        <license .../>
miktex(k, dc=dc_var)                    function: processes element
                                        <miktex .../>
name(k, dc=dc_var)                      function: processes element
                                        <name>...</name>
texlive(k, dc=dc_var)                   function: processes element
                                        <texlive .../>
version(k, p, dc=dc_var)                function: processes
                                        <version .../> element
------------------------------------------------------------------
innertext(k, start, pp, dc=dc_var)      function innertext: looks for
                                        embedded text and elements and
                                        returns an evaluated string
mod_a(k, pp, dc=dc_var)                 function: processes element
                                        <a ...> ... </a>
mod_b(k, pp, dc=dc_var)                 function: processes element
                                        <b>...</b>
mod_br(k, pp, dc=dc_var)                function: processes element
                                        <br/>
mod_code(k, pp, dc=dc_var)              function: processes element
                                        <code>...</code>
mod_dd(k, pp, dc=dc_var)                function: processes element
                                        <dd>...</dd>
mod_dl(k, pp, dc=dc_var)                function: processes element
                                        <dl>...</dl>
mod_dt(k, pp, dc=dc_var)                function: processes element
                                        <dt>...</dt>
mod_em(k, pp, dc=dc_var)                function: processes element
                                        <em>...</em>
mod_i(k, pp, dc=dc_var)                 function: processes element
                                        <i>...</i>
mod_li(k, pp, dc=dc_var)                function: processes element
                                        <li>...</li>
mod_pre(k, pp, dc=dc_var)               function: processes element
                                        <pre>...</pre>
mod_small(k, pp, dc=dc_var)             function: processes element
                                        <small>...</small>
mod_TeXchars1(s, dc=dc_var) ->str       auxiliary function: prepares
                                        characters for LaTeX/BibLaTeX
                                        in a paragraph
mod_TeXchars2(s, dc=dc_var) ->str       auxiliary function: prepares
                                        characters for LaTeX/BibLaTeX
mod_tt(k, pp, dc=dc_var)                function: processes element
                                        <tt>...</tt>
mod_xref(k, pp, dc=dc_var)              function: processes element
                                        <xref ...> ... </xref>
mod_ol(k, pp, dc=dc_var)                function: processes element
                                        <ol>...</ol>
mod_p(k, pp, dc=dc_var)                 function: processes element
                                        <p> ... </p>
mod_ul(k, pp, dc=dc_var)                function: processes element
                                        <ul>...</ul>

see also:
--------
+ installation.txt
+ firststeps.txt
+ call.txt
+ wget.txt
+ CTAN-files.txt
+ CTAN-corrected-files.txt
+ CTAN-elements.txt

+ CTANOut-changes.txt
+ CTANOut-messages.txt
+ CTANOut.man
+ CTANOut-examples.txt
+ CTANOut-examples.bat
+ CTANOut-mappings.txt
+ CTANOut-modules.txt
"""

#===================================================================
# Contents
#
# A.  Modules needed
# B.  python dictionaries, tuples and lists
# C.  Settings
# C.1 Global settings
# C.2 Collect infos for elements which cannot be output in another way
# C.3 Texts for argument parsing
# C.4 Defaults for argument parsing and further processing
# C.5 python dictionaries and lists
# C.6 Strings for Excel output
# D.  Parsing the arguments
# D.1 Getting parsed values
# D.2 Resettings and settings
# D.3 Correct folder name, test folder existence, and/or install folder
# D.4 pre-compiled regular expressions (based on specified options)
# E.  Other settings
# E.1 Preambel for LaTeX output
# E.2 Only for LaTeX (header and trailer of the LaTeX file)
# F.  auxiliary functions
# G.  main functions
# H.  functions in the context of description
# I.  Main Part
# History


#===================================================================
# A. Modules needed

# 3.3    2026-07-09 data class used
# 3.3.0  2026-07-09 new module dataclasses
# 3.7    2026-07-13 backtracing
# 3.7.1  2026-07-13 new module traceback

import xml.etree.ElementTree as ET                                      # XML processing
import pickle                                                           # read pickle data, time measure
import time                                                             # get time|date of a file
import re                                                               # regular expression
import argparse                                                         # argument parsing
import sys                                                              #  system calls
import platform                                                         # get OS informations
import os                                                               # OS relevant routines
from os import path                                                     # path informations
import codecs                                                           # needed for full UTF-8 output on stdout
from dataclasses import dataclass, field                                # Python data classes
import traceback                                                        # error backtracing  ---> modules


#===================================================================
# B. python dictionaries, tuples and lists

# usedTopics: Python dictionary (unsorted)
#   each element: <key for topic>:<number>
# usedPackages: Python list
#   each element: <package name>
# usedAuthors: Python dictionary (unsorted)
#   each element: <key for author>:<tuple with givenname and familyname>
# usedLicenses: Python dictionary

# allauthoryears: Python dictionary
#   each element: allauthoryears[(<author>,<year>] = <appendix>
# citation_keys: Python dictionary
#   each element: citation_keys[package] = (<author>, <year>,
#   <appendix>)

# authors: Python dictionary (sorted)
#   each element: <author key>:<tuple with givenname and familyname>
# packages: Python dictionary (sorted)
#   each element: <package key>:<tuple with package name and package
#   title>
# topics: Python dictionary (sorted)
#   each element: <topics name>:<topics title>
# licenses: Python dictionary (sorted)
#   each element: <license key>:(<license title>, <free>)
# topicspackages: Python dictionary (unsorted)
#   each element: <topic key>:<list with package names>
# packagetopics: Python dictionary (sorted)
#   each element: <topic key>:<list with package names>
# authorpackages: Python dictionary (unsorted)
#   each element: <author key>:<list with package names>
# licensepackages: Python dictionary (mostly sorted)
#   each element: <license key>:<list with package names>
# yearpackages: Python dictionary
#   each element: <year>:<list of package names>


#===================================================================
# C. Settings

# 3.1    2026-07-05 ACT_PROGRAMNAME depends on OPERATINGSYS now

PROGRAM_NAME            = "CTANOut.py"
PROGRAM_VERSION         = "3.13"
PROGRAM_DATE            = "2026-08-21"
PROGRAM_AUTHOR          = "Günter Partosch"
DOCUMENT_AUTHOR         = "Developers and contributors for" + \
                          " {\\TeX}, {\\LaTeX}, \\& Co"
DOCUMENTAUTHOR_TXT      = "Developers and contributors for" + \
                          " TeX, LaTeX, & Co"
AUTHOR_INSTITUTION      = "formerly: Justus-Liebig-Universität " +\
                          "Gießen, Hochschulrechenzentrum"
AUTHOR_EMAIL            = "Guenter.Partosch@web.de;\nformerly:" + \
                          " Guenter.Partosch@hrz.uni-giessen.de"
DOCUMENT_TITLE          = "The CTAN book -- Packages on CTAN"
DOCUMENT_SUBTITLE       = "Collected, prepared and selected with" + \
                          " the aid of the program "

OPERATINGSYS            = platform.system()                             # operating system
CALL                    = sys.argv                                      # actual program call 
CALLEDPROGRAM           = sys.argv[0]                                   # name of called program (with path)
if OPERATINGSYS == "Windows":
    ACT_PROGRAMNAME     = CALLEDPROGRAM.split("\\")[-1]             
else:
    ACT_PROGRAMNAME     = CALLEDPROGRAM.split("/")[-1]

# ------------------------------------------------------------------
# C.1 Global settings

CTAN_URL                = "https://ctan.org"                            # head of a CTAN url
CTAN_URL2               = CTAN_URL + "/tex-archive"                     # head of another CTAN url
CTAN_URL3               = CTAN_URL2 + "/install"                        # head of another CTAN url
CTAN_URL4               = CTAN_URL + "/pkg/"                            # head of another CTAN url
ACT_DATE                = time.strftime("%Y-%m-%d")                     # actual date of program execution 
ACT_TIME                = time.strftime("%X")                           # actual time of program execution 

PICKLE_NAME1            = "CTAN.pkl"                                    # default name of the 1st pickle file
PICKLE_NAME2            = "CTAN2.pkl"                                   # default name of the 2nd pickle file
EMPTY                   = ""                                            # default text in some cases
BLANK                   = " "                                           # default text in some other cases
FILE_ENCODING           = "UTF-8"                                       # encoding of output file
EXT                     = ".xml"                                        # file name extension for info files to be downloaded

# ------------------------------------------------------------------
# C.2 Collect infos for elements which cannot be output in another way

# 2.70   2025-11-03 argparse texts revised

YEAR_DEFAULT            = "1970"                                        # default text for year (internal)
YEAR_DEFAULT2           = "without year"                                # default text for year (for output)
MAX_DEFAULT             = "2050"                                        # maximum value for year
DEFAULT_TEXT            = "no text"                                     # default text for elements without embedded text
AUTHOR_UNKNOWN          = "N. N."                                       # default text for author
DATE_DEFAULT            = YEAR_DEFAULT + "-01-01"                       # default text for date
ELLIPSIS                = " ..."                                        # ellipsis

NLS                     = "nls"                                         # no language specified

ERR_MODE_TEXT           = "[CTANOut] Warning: '{0} \"{1}\" ' " +\
                          "changed to '{2}' (due to '{3}')"
EXCLUSION               = ["authors.xml", "topics.xml", "packages.xml",
                          "licenses.xml"]                               

MAX_CAPTION_LENGTH      = 60                                            # for LaTeX: max length for header lines
FIELD_WIDTH             = 10                                            # for BibLaTeX: width of the field labels
RIS_FIELDWIDTH          = 5                                             # for RIS: width of the field labels
TXT_FIELDWIDTH          = 18                                            # for plain: width of the field labels
TEX_FIELDWIDTH          = 10                                            # for LaTeX: width of the field labels
LEFT                    = 35                                            # width of labels in verbose output
LABEL_WIDTH             = len("Web page on CTAN: ")                     # width of the longest label for LaTeX
CASES                   = {"BibLaTeX":FIELD_WIDTH + 2,
                           "LaTeX":TEX_FIELDWIDTH,
                           "RIS":RIS_FIELDWIDTH + 1,
                           "plain":TXT_FIELDWIDTH,
                           "Excel":0 }                                  # dict: length of left indentations 

# ------------------------------------------------------------------
# C.3 Texts for argument parsing

# 2.62   2024-07-26 some smaller text changes for argparse
# 2.70   2025-11-03 argparse texts revised

AUTHOR_TEXT             = "Shows author of the program and exits."
BTYPE_TEXT              = "Type of BibLaTex entries to be generated" +\
                          " [only for BibLateX mode]"
DIREC_TEXT              = "Folder for input and output files"
MODE_TEXT               = "Target format"
OUT_TEXT                = "Generic name [without extensions] for " +\
                          "output files"
PROGRAM_TEXT            = "Converts CTAN XLM package files to " +\
                          "LaTeX, RIS, plain, BibLaTeX, Excel " +\
                          "[tab separated]."
SKIP_BIBLATEX_TEXT      = "Skips specified BibLaTeX fields."
SKIP_TEXT               = "Skips specified CTAN fields."
VERSION_TEXT            = "Shows version of the program and exit."

AUTHOR_TEMPLATE_TEXT    = "Template for output filtering on the " +\
                          "base of author names"
KEY_TEMPLATE_TEXT       = "Template for output filtering on the " +\
                          "base of keys"
LICENSE_TEMPLATE_TEXT   = "Template for output filtering on the " +\
                          "base of license names"
TEMPLATE_TEXT           = "Template for output filtering on the " +\
                          "base of package names"
YEAR_TEMPLATE_TEXT      = "Template for output filtering on the " +\
                          "base of years"

NO_FILES_TEXT           = "Flag: Do not generate output files."
STATISTICS_TEXT         = "Flag: Prints statistics on terminal."
TOPICS_TEXT             = "Flag: Generates topic lists [meaning of" + \
                          " topics|licenses + cross-references" + \
                          " (topics|packages, uthors|packages," + \
                          " licenses|packages); only for -m LaTeX])."
VERBOSE_TEXT            = "Flag: Output is verbose."

# ------------------------------------------------------------------
# C.4 Defaults for argument parsing and further processing

MAKE_TOPICS_DEFAULT      = False                                        # default for topics output (-mt)
VERBOSE_DEFAULT          = False                                        # default for flag: verbose output (-v)
STATISTICS_DEFAULT       = False                                        # default for flag: statistics output (-stat)
NO_FILES_DEFAULT         = False                                        # default for option -nf
LICENSE_TEMPLATE_DEFAULT = """^.+$"""                                   # default for option -L (license name template)
NAME_TEMPLATE_DEFAULT    = """^.+$"""                                   # default for file name template (-t) [at least one character]
KEY_TEMPLATE_DEFAULT     = """^.+$"""                                   # default for topic filter (-k) [at least one character]
AUTHOR_TEMPLATE_DEFAULT  = """^.+$"""                                   # default for author name template (-A) [at least one character]
YEAR_TEMPLATE_DEFAULT    = """^19[89][0-9]|20[012][0-9]$"""             # default for year template (-y) [four digits]
BTYPE_DEFAULT            = "@online"                                    # default for BibLaTeX entry type (-b)
SKIP_DEFAULT             = "[]"                                         # default for option -s
SKIP_BIBLATEX_DEFAULT    = "[]"                                         # default for option -sb
MODE_DEFAULT             = "RIS"                                        # default for option -m
OUT_DEFAULT              = "all"                                        # default for generic output file name (-o)
DEBUGGING_DEFAULT        = False                                        # default for debugging (-dbg)

NAME_DEFAULT            = NAME_TEMPLATE_DEFAULT                         # copy of NAME_TEMPLATE_DEFAULT

ACT_DIREC                = "."                                          # actual OS folder
if OPERATINGSYS == "Windows":
    DIREC_SEP      = "\\"                                               # folder separator (Windows) 
else:
    DIREC_SEP      = "/"                                                # folder separator (else)
DIREC_DEFAULT           = ACT_DIREC + DIREC_SEP                         # default for -d (output folder) 

# ------------------------------------------------------------------
# C.5 python dictionaries and lists

# 2.54    2024-02-18 new language codes: en,fr and es-pe
# 2.64    2025-01-27 languages "en,zh", "yue", "zh-tw" now in
#                    LANGUAGECODES

LANGUAGECODES = {"af":"Afrikaans", "am":"Amharic", "ar":"Arabic",
    "ar-dz":"Arabic (Algeria)", "az":"Azerbaijani", "be":"Belarusian",
    "bg":"Bulgarian", "bn":"Bengali", "br":"Breton", "bs":"Bosnian",
    "bs-Cyrl":"Bosnian (Cyrillic)", "bs-Latn":"Bosnian (Latin)",
    "ca":"Catalan", "co":"Corsican", "cop":"Coptic", "cs":"Czech",
    "cu":"Church Slavic", "cy":"Welsh", "da":"Danish", "de":"German",
    "de,en":"German + English", "de-at":"German (Austria)",
    "de-chg":"Swiss High German", "de-de":"German (Germany)",
    "dsb":"Lower Sorbian", "el":"Greek", "en":"English",
    "en,fr":"English + French", "en,ja":"English + Japanese",
    "en,ru":"English + Russian", "en,zh": "English+Chinese",
    "en-gb":"English (Great britain)", "eo":"Esperanto", "es":"Spanish",
    "es-mx":"Spanish (Mexico)", "es-pe":"Spanish (Peru)",
    "es-ve":"Spanish (Venezuela)", "et":"Estonian", "eu":"Basque",
    "fa":"Farsi", "fa":"Persian", "fa-ir":"Farsi (Iran)",
    "fi":"Finnish", "fo":"Faroese", "fr":"French",
    "fr-ca":"French (Canada)", "fr-ch":"French (Switzerland)",
    "fr-lu":"French (Luxembourg)", "fy":"Western Frisian", "ga":"Irish",
    "gd":"Gaelic, Scottish Gaelic", "gl":"Galician", "he":"Hebrew",
    "hi":"Hindi", "hr":"Croatian", "hsb":"Upper Sorbian",
    "hu":"Hungarian", "hy":"Armenian", "id":"Indonesian",
    "is":"Icelandic", "it":"Italian", "ja":"Japanese", "jv":"Javanese",
    "ka":"Georgian", "kk":"Kazakh", "ko":"Korean", "ks":"Kashmiri",
    "ku":"Kurdish", "kw":"Cornish", "ky":"Kirghiz", "la":"Latin",
    "lb":"Luxembourgish", "li":"Limburgish", "lt":"Lithuanian",
    "lv":"Latvian", "mk":"Macedonian", "mn":"Mongolian", "mr":"Marathi",
    "mr,hi":"Marathi + Hindi", "mt":"Maltese", "my":"Burmese",
    "nb":"Norwegian Bokmål", "nl":"Dutch", "nn":"Norwegian Nynorsk",
    "nn-no":"Nynorsk", "no":"Norwegian", "oc":"Occitan", "pl":"Polish",
    "ps":"Pashto", "pt":"Portuguese", "pt-br":"Portuguese (Brazilia)",
    "pt-pt":"Portuguese (Portugal)", "ro":"Romanian", "ru":"Russian",
    "sa":"Sanskrit", "sc":"Sardinian", "se":"Northern Sami",
    "sk":"Slovak", "sl":"Slovenian", "sq":"Albanian", "sr":"Serbian",
    "sr-Cyrl":"Serbian (Cyrillic)", "sr-Latn":"Serbian (Latin)",
    "sr-sp":"Serbian (Serbia)", "sv":"Swedish", "ta":"Tamil",
    "tg":"Tajik", "th":"Thai", "tk":"Turkmen", "tr":"Turkish",
    "uk":"Ukrainian", "ur":"Urdu", "uz":"Uzbek", "vi":"Vietnamese",
    "yi":"Yiddish", "yue": "Cantonese", "zh":"Chinese",
    "zh,en":"Chinese + English", "zh,ja":"Chinese + Japanese",
    "zh-cn":"Chinese (China)", "zh-tw": "Chinese (Taiwan)",
    NLS:"no language specified"}  

# ------------------------------------------------------------------
# C.6 Strings for Excel output

S_ALIAS_TEXT             = "alias"                                      # string for Excel header:  alias element
S_ALSO_TEXT              = "also"                                       # string for Excel header:  also element
S_AUTHOR_TEXT            = "author"                                     # string for Excel header:  authoref elements (collected)
S_CAPTION_TEXT           = "caption"                                    # string for Excel header:  caption element
S_CONTACT_TEXT           = "contact"                                    # string for Excel header:  contact element
S_COPYRIGHT_TEXT         = "copyright"                                  # string for Excel header:  copyright elements (collected)
S_CTAN_TEXT              = "CTAN"                                       # string for Excel header:  ctan element
S_DOCUMENTATION_TEXT     = "documentation"                              # string for Excel header:  documentation elements (collected)
S_HOME_TEXT              = "home"                                       # string for Excel header:  home element
S_ID_TEXT                = "id"                                         # string for Excel header:  id attribute in entry element
S_INSTALL_TEXT           = "install"                                    # string for Excel header:  install element
S_KEYVAL_TEXT            = "keyval"                                     # string for Excel header:  keyval elements (collected)
S_LANGUAGE_TEXT          = "language"                                   # string for Excel header:  extracted from documentation and description (collected)
S_LASTACCESS_TEXT        = "lastaccess"                                 # string for Excel header:  day of last download
S_LASTCHANGES_TEXT       = "lastchanges"                                # string for Excel header:  extracted from version element
S_LICENSE_TEXT           = "license"                                    # string for Excel header:  license elements (collected)
S_MIKTEX_TEXT            = "MikTeX"                                     # string for Excel header:  miktex element
S_NAME_TEXT              = "name"                                       # string for Excel header:  name element
S_TEXLIVE_TEXT           = "TeXLive"                                    # string for Excel header:  texlive element
S_VERSION_TEXT           = "version"                                    # string for Excel header:  version element
S_YEAR_TEXT              = "year"                                       # string for Excel header:  extracted from copyright and version


#===================================================================
# D data class dataclass_variable

# 3.3    2026-07-09 data class used
# 3.3.1  2026-07-09 new class dataclass-variable (including all globally
#                   used variables) derfined
# 3.8    2026-08-05 default values for variables in dataclass_variable
#                   on the basis of constants now
# 3.11   2026-08-16 Calculation and output of the input string
# 3.11.2 2026-08-16 variable 'arguments' now in dataclass_variable
# 3.13   2026-08-21 type annotation of skip, skip_biblatex in
#                   dataclass_variable corrected

# ------------------------------------------------------------------
@dataclass
class dataclass_variable():                                             # class dataclass_var
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
    
    # ------------------------------------------------------------------
    # D.1 Collect infos for elements which cannot be output in
    #     another way
    
    list_info_files:bool    = True                                      # switch for RIS/BibLaTeX: XML_toc is to be proceeded
    no_package_processed:bool = False                                   # Flag: if no package is processed 

    also_str:str            = EMPTY                                     # collects all also items for a package
    arguments:str           = EMPTY                                     # arguments of the program call
    author_str:str          = EMPTY                                     # collecting authors of a package class
    authorexists            = None                                      # flag; True, if an author exists
    contact_str:str         = EMPTY                                     # collects contact information 
    copyright_str:str       = EMPTY                                     # collects all copyright items for a package 
    date_str:str            = EMPTY                                     # collects date information 
    description_str:str     = EMPTY                                     # collects description content 
    info_files:list         = field(default_factory=list)               # default for each package: collection of local info files| 
    language_set:set        = field(default_factory=set)                # default for each package: collection of language items 
    level:str               = EMPTY                                     # level of itemize/enumerate (<ol>, <ul>) 
    license_str:str         = EMPTY                                     # collects all license items for a package 
    notice:str              = EMPTY                                     # collecting infos (RIS|BibLaTeX) 
    package_id:str          = EMPTY                                     # ID of a package 
    version_str:str         = DATE_DEFAULT                              # collects all version items for a package 
    year_str:str            = YEAR_DEFAULT                              # default for each package: concatenation of year items 

    # ------------------------------------------------------------------
    # D.2 some counters
    
    counter:int             = 1                                         # counter for  packages
    no_ap:int               = 0                                         # number of packages selected per author names
    no_lp:int               = 0                                         # number of packages selected per licenses
    no_ly:int               = 0                                         # number of packages selected per years
    no_np:int               = 0                                         # number of packages selected per n<mes
    no_tp:int               = 0                                         # number of packages selected per topics

    # ------------------------------------------------------------------
    # D.3 pre-compiled regular expressions (based on specified options)

    # Change: 2.56    2024-02-18 "[\^s]+" changed to "r[\^]+"

    p2:re.Pattern  = EMPTY                                              # regular expression based on -t
    p3:re.Pattern  = EMPTY                                              # regular expression based on -k
    p4:re.Pattern  = EMPTY                                              # split a string to find year data
    p5:re.Pattern  = EMPTY                                              # regular expression based on -A
    p6:re.Pattern  = EMPTY                                              # regular expression for local XML file names
    p7:re.Pattern  = EMPTY                                              # regular expression: test of "white space"
    p8:re.Pattern  = EMPTY                                              # regular expression: processing of "§§=xx"
    p9:re.Pattern  = EMPTY                                              # regular expression based on -L
    p10:re.Pattern = EMPTY                                              # regular expression based on -y

    # ------------------------------------------------------------------
    # D.4 Defaults for argument parsing (argparse) and further
    #     processing

    author_template:str     = AUTHOR_TEMPLATE_DEFAULT                   # variable for -A 
    btype:str               = BTYPE_DEFAULT                             # variable for -b 
    debugging:bool          = DEBUGGING_DEFAULT                         # variable for -dbg
    direc:str               = DIREC_DEFAULT                             # variable for -d 
    key_template:str        = KEY_TEMPLATE_DEFAULT                      # variable for -k 
    license_template:str    = LICENSE_TEMPLATE_DEFAULT                  # variable for -L
    make_topics:bool        = MAKE_TOPICS_DEFAULT                       # variable for -mt 
    mode:str                = MODE_DEFAULT                              # variable for -m
    name_template:str       = NAME_TEMPLATE_DEFAULT                     # variable for -t 
    no_files:bool           = NO_FILES_DEFAULT                          # variable for -nf
    out_file:str            = OUT_DEFAULT                               # variable for -o
    out_file_ext:str        = EMPTY                                     # out_file with name extension
    skip:list               = field(default_factory=list)               # variable for -s 
    skip_biblatex:list      = field(default_factory=list)               # variable for -sb 
    statistics:bool         = STATISTICS_DEFAULT                        # variable for -stat 
    verbose:bool            = VERBOSE_DEFAULT                           # variable for -v 
    year_template:str       = YEAR_TEMPLATE_DEFAULT                     # variable for -y

    # ------------------------------------------------------------------
    # D.5 define a file handler for out_file
    
    out:_io.TextIOWrapper   = None

    # ------------------------------------------------------------------
    # D.6 Python dictionaries and lists

    usedTopics:dict         = field(default_factory=dict)               # Python dictionary: collect used topics for all packages 
    usedPackages:list       = field(default_factory=list)               # python list: collect used packages 
    usedAuthors:dict        = field(default_factory=dict)               # Python dictionary: collect used authors for all packages 
    usedLicenses:dict       = field(default_factory=dict)               # Python dictionary: collect used licenses for all packages 

    allauthoryears:dict     = field(default_factory=dict)               # Python dictionary: each element: allauthoryears [(<author>,<year>] = <appendix>  
    authorpackages:dict     = field(default_factory=dict)               # python dictionary: each element: <author key>:<list with package names> 
    authors:dict            = field(default_factory=dict)               # python dictionary: each element: <author key>:<tuple with givenname and familyname>
    citation_keys:dict      = field(default_factory=dict)               # Python dictionary: each element: citation_keys[package] =l (<author>, <year>, <appendix>) 
    licensepackages:dict    = field(default_factory=dict)               # Python dictionary (mostly sorted): each element: <license key>:<list with package names>
    licenses:dict           = field(default_factory=dict)               # python dictionary: each element: <license key>:<license title> 
    packages:dict           = field(default_factory=dict)               # python dictionary: each element: <package key>:<tuple with package name and package title> 
    packagetopics:dict      = field(default_factory=dict)               # python dictionary: each element: <topic key>:<list with package names> 
    topics:dict             = field(default_factory=dict)               # python dictionary: each element: <topics name>:<topics title> 
    topicspackages:dict     = field(default_factory=dict)               # python dictionary: each element: <topic key>:<list of package names>
    XML_toc:dict            = field(default_factory=dict)               # python dictionary: list of XML and PDF files: XML_toc[CTAN address]=(XML file, key, plain PDF file name) 
    yearpackages:dict       = field(default_factory=dict)               # python dictionary: each element: <year>: <list of package names> 

    # ------------------------------------------------------------------
    # D.7 Strings for Excel output

    s_alias:str             = EMPTY                                     # alias element 
    s_also:str              = EMPTY                                     # also element 
    s_author:str            = EMPTY                                     # authoref elements (collected) 
    s_caption:str           = EMPTY                                     # caption element 
    s_contact:str           = EMPTY                                     # contact element 
    s_copyright:str         = EMPTY                                     # copyright elements (collected) 
    s_ctan:str              = EMPTY                                     # ctan element 
    s_lastaccess:str        = EMPTY                                     # day of last download 
    s_documentation:str     = EMPTY                                     # documentation elements (collected) 
    s_year:str              = EMPTY                                     # extracted from copyright and version 
    s_language:str          = EMPTY                                     # extracted from documentation and description (collected) 
    s_lastchanges:str       = EMPTY                                     # extracted from version element 
    s_home:str              = EMPTY                                     # home element 
    s_id:str                = EMPTY                                     # id attribute in entry element 
    s_install:str           = EMPTY                                     # install element 
    s_keyval:str            = EMPTY                                     # keyval elements (collected) 
    s_license:str           = EMPTY                                     # license elements (collected) 
    s_miktex:str            = EMPTY                                     # miktex element 
    s_name:str              = EMPTY                                     # name element 
    s_texlive:str           = EMPTY                                     # texlive element 
    s_version:str           = EMPTY                                     # version element 

    # ------------------------------------------------------------------
    def report(self, full:bool=False):                                  # function dataclass_variable.report
        """
        Outputs the current values of the variables defined in
        'dataclass_variable'.

        Parameter:
        ---------
        full : bool:
               if True, all menbers of sets, lists, tuples, and
               dictionaries, else only the lengths.
               default: False
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
# 3.3    2026-07-09 data class used
# 3.3.2  2026-07-09 instance "dc_var" of this class created

dc_var = dataclass_variable()


#===================================================================
# E. Parsing the arguments

# ------------------------------------------------------------------
# E.1 defining argparse arguments

# ------------------------------------------------------------------
def argparse_process(dc=dc_var):                                        # function argparse_process
    """
    Defines the arguments for the program CTANOut and starts.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Workflow:
    --------
    + E.1 Defines argparse arguments.
    + E.2 Determines variable values from the given arguments.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """
    # 3.5    2026-07-13 new function: argparse_process
    # 3.5.1  2026-07-13 Defines the arguments for the program CTANOut
    #                   and starts.
    # 3.11   2026-08-16 Calculation and output of the input string
    # 3.11.1 2026-08-16 moved from first_lines to argparse_postprocess

    parser = argparse.ArgumentParser(formatter_class = \
             argparse.RawDescriptionHelpFormatter,
             prog = (PROGRAM_NAME.split("."))[0],
             description = "{0}\nVersion: {1} ({2})\n\n{3}".\
             format("%(prog)s", PROGRAM_VERSION, \
                    PROGRAM_DATE, PROGRAM_TEXT),
             epilog = "Thanks for using %(prog)s!",
             )
    parser._optionals.title  = 'Global options (without any actions)'

    parser.add_argument("-a", "--author",                               # Parameter -a|--author
            help    = AUTHOR_TEXT,
            action  = 'version',
            version = f"{PROGRAM_AUTHOR} ({AUTHOR_EMAIL}, " +\
                      f"{AUTHOR_INSTITUTION})")

    parser.add_argument("-dbg", "--debugging",                          # Parameter -dbg|--debugging
            help    = argparse.SUPPRESS,
            action  = "store_true",
            dest    = "debugging",
            default = DEBUGGING_DEFAULT)

    parser.add_argument("-stat", "--statistics",                        # Parameter -stat|--statistics
            help    = STATISTICS_TEXT + " -- Default: " + "%(default)s",
            action  = "store_true",
            dest    = "statistics",
            default = STATISTICS_DEFAULT)

    parser.add_argument("-v", "--verbose",                              # Parameter -v|--verbose
            help    = VERBOSE_TEXT + " -- Default: " + "%(default)s",
            action  = "store_true",
            dest    = "verbose",
            default = VERBOSE_DEFAULT)

    parser.add_argument("-V", "--version",                              # Parameter -V|--version
            help    = VERSION_TEXT,
            action  = 'version',
            version = '%(prog)s ' + PROGRAM_VERSION + " (" + \
                      PROGRAM_DATE + ")")

    group1 = parser.add_argument_group("Options related to output")

    group1.add_argument("-A", "--author_template",                      # Parameter -A|--author_template
            metavar = "<author template>",
            help    = AUTHOR_TEMPLATE_TEXT + " -- Default: " + \
                      "%(default)s",
            dest    = "author_template",
            default = AUTHOR_TEMPLATE_DEFAULT)

    group1.add_argument("-b", "--btype",                                # Parameter -b|--btype
            metavar = "<btype>",
            help    = BTYPE_TEXT + " -- Default: " + "%(default)s",
            choices = ["@online", "@software", "@misc", "@ctan",
                       "@www","@electronic"],
            action  = "store",
            dest    = "btype",
            default = BTYPE_DEFAULT)

    group1.add_argument("-d", "--directory",                            # Parameter -d|--directory (folder)
            metavar = "<OS directory (folder)>",
            help    = DIREC_TEXT + " -- Default: " + "%(default)s",
            action  = "store",
            dest    = "direc",
            default = DIREC_DEFAULT)

    group1.add_argument("-k", "--key_template",                         # Parameter -k|--key_template
            metavar = "<key template>",
            help    = KEY_TEMPLATE_TEXT + " -- Default: " + \
                      "%(default)s",
            action  = "store",
            dest    = "key_template",
            default = KEY_TEMPLATE_DEFAULT)

    group1.add_argument("-L", "--license_template",                     # Parameter -L|--license_template
            metavar = "<license template>",
            help    = LICENSE_TEMPLATE_TEXT + " -- Default: " +\
                      "%(default)s",
            action  = "store",
            dest    = "license_template",
            default = LICENSE_TEMPLATE_DEFAULT)

    group1.add_argument("-m", "--mode",                                 # Parameter -m|--mode
            metavar = "<mode>",
            help    = MODE_TEXT + " -- Default: " + "%(default)s",
            choices = ["LaTeX", "latex", "tex", "RIS", "plain",
                       "txt","BibLaTeX", "biblatex", "bib",
                       "ris", "Excel","excel", "tsv", "csv"],
            action  = "store",
            dest    = "mode",
            default = MODE_DEFAULT)

    group1.add_argument("-mt", "--make_topics",                         # Parameter -mt|--make_topics
            help    = TOPICS_TEXT + " -- Default: " + "%(default)s",
            action  = "store_true",
            dest    = "make_topics",
            default = MAKE_TOPICS_DEFAULT)

    group1.add_argument("-nf", "--no_files",                            # Parameter -nf|--no_files
            help    = NO_FILES_TEXT + " -- Default: " + "%(default)s",
            action  = "store_true",
            dest    = "no_files",
            default = NO_FILES_DEFAULT)

    group1.add_argument("-o", "--output",                               # Parameter -o|--output
            metavar = "<output>",
            help    = OUT_TEXT + " -- Default: " + "%(default)s",
            action  = "store",
            dest    = "out_file",
            default = OUT_DEFAULT)

    group1.add_argument("-s", "--skip",                                 # Parameter -s|--skip
            metavar = "<skip>",
            help    = SKIP_TEXT + " -- Default: " + "%(default)s",
            action  = "store",
            dest    = "skip",
            default = SKIP_DEFAULT)

    group1.add_argument("-sb", "--skip_biblatex",                       # Parameter -sb|--skip_biblatex
            metavar ="<skip biblatex>",
            help    = SKIP_BIBLATEX_TEXT + " -- Default: " + \
                      "%(default)s",
            action  = "store",
            dest    = "skip_biblatex",
            default = SKIP_BIBLATEX_DEFAULT)

    group1.add_argument("-t", "--name_template",                        # Parameter -t|--name_template
            metavar = "<name template>",
            help    = TEMPLATE_TEXT + " -- Default: " + "%(default)s",
            action  = "store",
            dest    = "name_template",
            default = NAME_TEMPLATE_DEFAULT)

    group1.add_argument("-y", "--year_template",                        # Parameter -y|--year_template
            metavar = "<year template>",
            help    = YEAR_TEMPLATE_TEXT + " -- Default: " + \
                      "%(default)s",
            action  = "store",
            dest    = "year_template",
            default = YEAR_TEMPLATE_DEFAULT)


    # ------------------------------------------------------------------
    # E.2 Determines variable values from the given arguments.

    args                = parser.parse_args()
    dc.author_template  = args.author_template                          # parameter -A
    dc.btype            = args.btype                                    # Parameter -b
    dc.direc            = args.direc                                    # Parameter -d
    dc.key_template     = args.key_template                             # Parameter -k
    dc.license_template = args.license_template                         # parameter -L
    dc.year_template    = args.year_template                            # parameter -y
    dc.make_topics      = args.make_topics                              # Parameter -mt
    dc.mode             = args.mode                                     # Parameter -m
    dc.name_template    = args.name_template                            # Parameter -t
    dc.no_files         = args.no_files                                 # Parameter -nf
    dc.out_file         = args.out_file                                 # Parameter -o
    dc.skip             = args.skip                                     # Parameter -s
    dc.skip_biblatex    = args.skip_biblatex                            # Parameter -sb
    dc.statistics       = args.statistics                               # Parameter -stat
    dc.verbose          = args.verbose                                  # Parameter -v
    dc.debugging        = args.debugging                                # parameter -dbg


#===================================================================
# F. resettings and settings

# ------------------------------------------------------------------
def argparse_postprocess(dc=dc_var):                                    # function argparse_postprocess
    """
    Postprocesses some parameters for the program CTANOut.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Workflow:
    --------
    + F.1 Normalizes mode values.
    + F.2 Corrects special combinations.
    + F.3 Corrects folder names, test folder existence, and/or
    +     install folder.
    + F.4 Defines pre-compiled regular expressions (based on specified
          options).
    + F.5 Other settings: sets ull name for the output file
    #     (with file name extensions).
    

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.6    2026-07-13 new function: argparse_postprocess
    # 3.6.1  2026-07-13 Postprocesses some parameters for the program
    #                   CTANOut.
    # 3.10   2026-08-15 log output of the options in the call revised
    
    # ------------------------------------------------------------------
    # F.1 normalize mode values

    if dc.mode in ["latex", "LaTeX", "tex"]:                            # -m latex in call
        dc.mode = "LaTeX"                                               # mode is reset
    if dc.mode in ["ris", "RIS"]:                                       # -m ris in call
        dc.mode = "RIS"                                                 # mode is reset
    if dc.mode in ["biblatex", "BibLaTeX", "bib"]:                      # -m biblatex in call
        dc.mode = "BibLaTeX"                                            # mode is reset
    if dc.mode in ["excel", "Excel", "tsv", "csv"]:                     # -m excel in call
        dc.mode = "Excel"                                               # mode is reset
    if dc.mode in ["plain", "txt"]:                                     # -m plain in call
        dc.mode = "plain"                                               # mode is reset

    # --------------------------------------------------------.----------
    # F.2 correct special combinations

    dc.arguments = EMPTY

    for f in range(1, len(CALL)):
        if not "-" in CALL[f]:
            CALL[f] = '"' + CALL[f] + '"'
    dc.arguments = BLANK.join(CALL[1:])                                 # get the parameters of function call

    if dc.verbose:
        print("[CTANOut] Info: program call:", ACT_PROGRAMNAME,
              dc.arguments)

    if (dc.no_files != NO_FILES_DEFAULT):                               # files are processed
        if (dc.btype != BTYPE_DEFAULT):
            if dc.verbose:                                              # "- [CTANOut] Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
                print(ERR_MODE_TEXT.format('-b', dc.btype,
                                           BTYPE_DEFAULT, '-nf'))
            dc.btype = BTYPE_DEFAULT                                    # btype is reset

        if (dc.skip_biblatex != SKIP_BIBLATEX_DEFAULT):
            if dc.verbose:                                              # "- [CTANOut] Warning:'{0} {1}' changed to '{2}' (due to '{3}')"
                print(ERR_MODE_TEXT.\
                      format('-sb', dc.skip_biblatex,
                             SKIP_BIBLATEX_DEFAULT, '-nf'))
            dc.skip_biblatex = SKIP_BIBLATEX_DEFAULT                    # skip_biblatex is reset

        if (dc.make_topics != MAKE_TOPICS_DEFAULT):
            if dc.verbose:                                              # "- [CTANOut] Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
                print(ERR_MODE_TEXT.format('-mt', dc.make_topics,
                                           MAKE_TOPICS_DEFAULT, '-nf'))
            dc.make_topics = MAKE_TOPICS_DEFAULT                        #  make_topics is reset

        if (dc.mode != MODE_DEFAULT):
            if dc.verbose:                                              # "- [CTANOut] Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
                print(ERR_MODE_TEXT.format('-m', dc.mode, '-m RIS',
                                           '-nf'))
            dc.mode  = MODE_DEFAULT                                     #   mode is set to RIS if -m is given

    if (dc.skip_biblatex != SKIP_BIBLATEX_DEFAULT) and \
        (dc.mode != "BibLaTeX"):                                        # all BibLaTeX files are processed
        if dc.verbose:                                                  # "- [CTANOut] Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
            print(ERR_MODE_TEXT.format('-m', dc.mode, '-m BibLaTeX',
                                       '-sb'))
        dc.mode  = "BibLaTeX"                                           # mode is set to BibLaTeX if -sb is given

    if (dc.btype != BTYPE_DEFAULT) and (dc.mode != "BibLaTeX"):
        if dc.verbose:                                                  # "- [CTANOut] Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
            print(ERR_MODE_TEXT.format('-m', dc.mode, '-m BibLaTeX',
                                       '-b'))
        dc.mode = "BibLaTeX"                                            # mode is set to BibLaTeX if -b is given

    if (dc.make_topics != MAKE_TOPICS_DEFAULT) and \
       (dc.mode != "LaTeX"):
        if dc.verbose:
            print(ERR_MODE_TEXT.format('-m', dc.mode, '-m LaTeX',
                                       '-mt'))
        dc.mode = "LaTeX"                                               # mode is set to LaTeX if -mt is given

    # ------------------------------------------------------------------
    # F.3 Correct folder name, test folder existence, and/or install
    # folder

    # 2.65   2025-02-06 wherever appropriate: string interpolation with 
    #                   f-strings instead of .format
    # 3.2    2026-07-09 try ... except enhanced; new error message
    # 3.7    2026-07-13 backtracing
    # 3.7.2  2026-07-13 traceback.print_exc()

    dc.direc = dc.direc.strip()                                         # strip folder name (-d)
    if dc.direc[len(dc.direc) - 1] != DIREC_SEP:                        # append a separator, if necessary
        dc.direc += DIREC_SEP

    if not path.exists(dc.direc):
        try:
            os.mkdir(dc.direc)                                          # create OS folder, if necessary
        except OSError:
            print(f"[CTANOut] Warning: Creation of the OS folder ",
                  f"'{dc.direc}' failed.")
        except Exception as err:
            print("[CTANOut] Warning: Any unspecified error:",
                  "argparse_postprocess,", err, traceback.print_exc())
        else:
            print(f"[CTANOut] Info: Successfully the OS folder ",
                  f"'{dc.direc}' created.")

    # ------------------------------------------------------------------
    # F.4 pre-compiled regular expressions (based on specified options)

    # Change: 2.56    2024-02-18 "[\^s]+" changed to "r[\^]+"

    dc.p2  = re.compile(dc.name_template)                               # regular expression based on -t
    dc.p3  = re.compile(dc.key_template)                                # regular expression based on -k
    dc.p4  = re.compile("[- |.,a-z]")                                   # split a string to find year data
    dc.p5  = re.compile(dc.author_template)                             # regular expression based on -A
    dc.p6  = re.compile("^.+[.]xml$")                                   # regular expression for local XML file names
    dc.p7  = re.compile(r"[\s]+")                                       # regular expression: test of "white space"
    dc.p8  = re.compile("§§=([1-2][0-9]|[1-9])")                        # regular expression: processing of "§§=xx"
    dc.p9  = re.compile(dc.license_template)                            # regular expression based on -L
    dc.p10 = re.compile(dc.year_template)                               # regular expression based on -y


    # ------------------------------------------------------------------
    # F.5 Other settings: Full name for the output file
    # (with file name extensions)

    if dc.mode in ["LaTeX"]:                                            # LaTeX
        dc.out_file_ext = dc.out_file + ".tex"
    elif dc.mode in ["RIS"]:                                            # RIS
        dc.out_file_ext = dc.out_file + ".ris"
    elif dc.mode in ["plain"]:                                          # plain
        dc.out_file_ext = dc.out_file + ".txt"
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.out_file_ext = dc.out_file + ".csv"
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        dc.out_file_ext = dc.out_file + ".bib"


#===================================================================
# G. Preambel for LaTeX output
# make_usepkg, make_classoptions, make_title, make_header, make_trailer

# ------------------------------------------------------------------
def make_usepkg(dc=dc_var) ->str:                                       # function make_usepkp
    """
    auxiliary function: creates the uspackage part for LaTeX output.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    The function returns a string (usepackage).
    
    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """
    
    # 3.4    2026-07-10 handling of LaTeX source code texts improved
    # 3.4.1  2026-07-10 texts for header, classoptions, title, usepkp,
    #                   trailer simplified
    # 3.4.2  2026-07-10 new functions for: make_...

    if dc.debugging:
        print("+++ -CTANOut:make_usepkg")

    tmp = r"""
\usepackage[silent]{fontspec}                        % font specif.
\defaultfontfeatures{Scale=MatchUppercase,
                      Ligatures=TeX,
                      Renderer=HarfBuzz}
\usepackage[bidi=basic]{babel}                       % language support
\babelprovide[import, onchar=ids fonts]{hindi}
\babelprovide[import, onchar=ids fonts]{chinese}
\babelprovide[import, onchar=ids fonts]{russian}

\babelfont[hindi]{rm}{Shobhika}                      % hindi font
\babelfont[chinese]{rm}{FandolSong}                  % chinese font
\babelfont[russian]{rm}{FreeSerif}                   % russian font
\babelfont[english]{rm}[Ligatures=Common]{FreeSerif} % serif font
\babelfont[english]{sf}[Ligatures=Common]{FreeSans}  % sans-serif font
\babelfont[english]{tt}[Scale=0.95]{FreeMono}        % mono-spaced font

\usepackage{makeidx}                                 % index generation
\usepackage[colorlinks=true]{hyperref}               % hypertext
                                                     % structures

\newcommand{\inp}[1]{\IfFileExists{#1}
            {\input{#1}}{}}

\makeindex
"""
    return tmp

# ------------------------------------------------------------------
def make_classoptions(dc=dc_var) ->str:                                 # function make_classoptions
    """
    auxiliary function: creates the uspackage part for LaTeX output.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    The function returns a string (classoptions).
    
    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """
    
    # 3.4    2026-07-10 handling of LaTeX source code texts improved
    # 3.4.1  2026-07-10 texts for header, classoptions, title, usepkp,
    #                   trailer simplified
    # 3.4.2  2026-07-10 new functions for: make_...

    if dc.debugging:
        print("+++ -CTANOut:classoptions")

    tmp = """
\\documentclass[
paper    = a4,       % paper A4
fontsize = 11pt,     % font size
parskip  = half,     % half parskip
numbers  = noenddot, % no dot after section number
index    = totoc,    % index in TOC
headings = small,    % small headers
DIV      = 12,       % 12-strip page layout
english
]{scrartcl}
"""
    return tmp

# ------------------------------------------------------------------
def make_title(dc=dc_var) ->str:                                        # function make_title
    """
    auxiliary function: creates the title part for LaTeX output.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    The function returns a string (title).
    
    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """
    
    # 3.4    2026-07-10 handling of LaTeX source code texts improved
    # 3.4.1  2026-07-10 texts for header, classoptions, title, usepkp,
    #                   trailer simplified
    # 3.4.2  2026-07-10 new functions for: make_...

    if dc.debugging:
        print("+++ -CTANOut:make_title")

    tmp = f"""
\\title{{{DOCUMENT_TITLE}}}
\\subtitle{{{DOCUMENT_SUBTITLE}  \\texttt{{{PROGRAM_NAME}}}}}
\\author{{{DOCUMENT_AUTHOR}}}
\\date{{\\today}}
"""
    return tmp
    
# ------------------------------------------------------------------
def make_header(dc=dc_var) ->str:                                       # function make_header
    """
    auxiliary function: creates the document header part for LaTeX
    output.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    The function returns a string (header).
    
    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """
    
    # 3.4    2026-07-10 handling of LaTeX source code texts improved
    # 3.4.1  2026-07-10 texts for header, classoptions, title, usepkp,
    #                   trailer simplified
    # 3.4.2  2026-07-10 new functions for: make_...

    if dc.debugging:
        print("+++ -CTANOut:make_header")

    tmp  = f"""
\\begin{{document}}
\\pagestyle{{headings}}
\\maketitle
\\inp{{{dc.out_file}.stat}}
\\newpage
"""
    return tmp

# ------------------------------------------------------------------
def make_trailer(dc=dc_var) ->str:                                      # function make_trailer
    """
    auxiliary function: creates the document trailer part for
    LaTeX output.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    The function returns a string (document trailer).
    
    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """
    
    # 3.4    2026-07-10 handling of LaTeX source code texts improved
    # 3.4.1  2026-07-10 texts for header, classoptions, title, usepkp,
    #                   trailer simplified
    # 3.4.2  2026-07-10 new functions for: make_...

    if dc.debugging:
        print("+++ -CTANOut:make_trailer")

    if dc.make_topics:
        tmp = f"""
\\newpage
\\appendix
\\inp{{{dc.out_file}.top}}
\\inp{{{dc.out_file}.xref}}
\\inp{{{dc.out_file}.tap}}
\\inp{{{dc.out_file}.lic}}
\\inp{{{dc.out_file}.tlp}}
\\printindex
\\end{{document}}
        """
    else:
        tmp = f"""
\\newpage
\\appendix
\\printindex
\\end{{document}}
        """
    return tmp


# ======================================================================
# H. auxiliary functions


# ------------------------------------------------------------------
def bibfield_test(s:str, f:str, dc=dc_var) ->bool:                      # function bibfield_test
    """
    Tests if the text s is not empty and the BibLaTeX field f is not
    to be skipped.

    Parameters:
    ----------
    s    str
         string to be tested
    f    str
         relevant BibLaTeX field
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns True, if the text s is not empty and field f is not to be
    skipped

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:bibfield_test")

    return (s != EMPTY) and (not f in dc.skip_biblatex)

# ------------------------------------------------------------------
def biblatex_citationkey(dc=dc_var):                                    # function biblatex_citationkey
    """
    auxiliary: Generates a set with citations keys for all packages.

    dc.citation_keys[package] = (name, year, appendix)

    Inspects the authorref, version, copyright elements.
    Rewrites the dc.citation_keys set.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.citation_keys  set: citation keys
    dc.debugging      flag: debugging
    dc.verbose        Flag: output is verbose

    Calls:
    -----
    + get_year()
    + get_authoryear()

    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.2     2026-07-09 try ... except enhanced; new error message
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut: >CTANOut:biblatex_citationkey")

    author_id_default:str = AUTHOR_UNKNOWN
    citation_key          = {}

    tmp = get_local_packages(dc.direc)                                  # get a folder list

    for f in tmp:                                                       # dafaults for the actual package
        auth         = []
        vers         = EMPTY
        copyr        = EMPTY
        author       = EMPTY
        givenname    = EMPTY
        familyname   = EMPTY
        version_date = EMPTY
        ff           = dc.direc + f + EXT

        try:
            op = ET.parse(ff)                                           # parse XML file
            OK = True
        except exception as err:                                        # not successfull
            if dc.verbose:
                print("[CTANOut] Warning: XML file for",
                      f"package '{ff}' not well-formed", err)
            OK = False

        if OK:                                                          # XML fil can be parsed
            opRoot = op.getroot()                                       # analyze package file
            for child in opRoot:
                if child.tag == "authorref":                            # element <authorref ...>
                    author_id = child.get("id", author_id_default)
                    auth.append(author_id)
                elif child.tag == "version":                            # element <version ...>
                    version_date = child.get("date", "")
                elif child.tag == "copyright":                          # element <copyright ...>
                    copyright_year = child.get("year", YEAR_DEFAULT)
                    copyr          = copyr + BLANK + copyright_year

            if len(auth) == 0:                                          # if no author is specified
                familyname = author_id_default
                givenname  = author_id_default
            else:
                id         = auth[0]
                if id in dc.authors:
                    givenname, familyname = dc.authors[id]              # get the author's name
                else:
                    givenname, familyname = EMPTY, AUTHOR_UNKNOWN

            year = version_date + BLANK + copyr                         # string to be analyzed
            if (year == BLANK) or (year == EMPTY):                      # if any year is not specified
                year = YEAR_DEFAULT
            year             = get_year(year)                           # get the year
            tmp              = get_authoryear(familyname, year)
            dc.citation_keys[f] = tmp
    if dc.verbose:
        print("[CTANOut] Info: all package files analyzed and",
              "set citation_keys created.")

    if dc.debugging:
        print("+++ <CTANOut: >CTANOut:biblatex_citationkey")

# ------------------------------------------------------------------
def comment_fold(s:str, dc=dc_var) ->str:                               # function comment_fold
    """
    Shortens|folds a string with long option values (in LaTeX comment
    output).

     Parameters:
    ----------
    s    str
         Text to be folded a/o shortened
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a folded/shortened string.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:comment_fold")

    OFFSET    = 29 * BLANK
    MAXLEN    = 120
    SEP       = "|"
    parts     = s.split(SEP)
    line:str  = EMPTY
    out:str   = EMPTY

    for f in range(0, len(parts)):
        if f != len(parts) - 1:
            line = line + parts[f] + SEP
        else:
            line = line + parts[f]
        if len(line) >= MAXLEN:
            out  = out + line + "\n%" + OFFSET + ": "
            line = EMPTY
    out = out + line
    return out

# ------------------------------------------------------------------
def fold(s:str, dc=dc_var) ->str:                                       # function fold
    """
    Shortens|folds strings with long option values (for normal output).

    Parameters:
    ----------
    s    str
         string to be folded a/o shortened
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns the folded/shortened string.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:fold")

    OFFSET     = 69 * BLANK                                             # left indentation
    MAXLEN     = 70                                                     # maximal lined length
    SEP        = "|"                                                    # split on sep
    parts:list = s.split(SEP)
    line:str   = EMPTY
    out:str    = EMPTY

    for f in range(0, len(parts)):
        if f != len(parts) - 1:
            line = line + parts[f] + SEP
        else:
            line = line + parts[f]
        if len(line) >= MAXLEN:
            out  = out + line + "\n" + OFFSET
            line = EMPTY
    out = out + line
    return out

# ------------------------------------------------------------------
def gen_fold(s:str, o:int, dc=dc_var) ->str:                            # function gen_fold
    """
    Folds the content of <p>, <li>, <dd> (mode dependant).

    Parameters:
    ----------
    s    str
         string (content of <p>, <li>, <dd>) to be folded
         no default
    o    int
         controls the offset on the left side
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns the folded string.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:gen_fold")

    OFFSET     = "§§=" + str(o)
    MAXLEN     = 100                                                    # maximal line length
    SEP        = BLANK                                                  # seperation character for output
    parts:list = dc.p7.split(s)                                            # split on P7
    line:str   = EMPTY
    out:str    = EMPTY

    if len(s) >= MAXLEN:
        for f in range(0, len(parts)):
            if f != len(parts) - 1:
                line = line + parts[f] + SEP
            else:
                line = line + parts[f]
            if len(line) > MAXLEN:
                out  = out + line + "§§-" + OFFSET
                line = EMPTY
        out = out + line
    else:
        out = s
    return out

# ------------------------------------------------------------------
def get_authoryear(a:str, y:int, dc=dc_var) ->tuple:                    # function get_authoryear
    """
    Constructs a unique authoryear string (for BibLaTeX).

    Performs some changes according to the BibLaTeX rules.
    Rewrites the variable dc.allauthoryears.

    Parameters:
    ----------
    a    str
         familyname
         no default
    y    int
         year
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns the tuple (name, year, appendix).

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    if dc.debugging:
        print("+++ -CTANOut:get_authoryear")

    name = a
    if name == EMPTY:                                                   # if name is not specified
        name = AUTHOR_UNKNOWN

    name = re.sub("Jr", "", name)                                       # some changes
    name = re.sub("[-., /'—]", "", name)
    name = re.sub("Á", "A", name)
    name = re.sub("Å", "A", name)
    name = re.sub("É", "E", name)
    name = re.sub("Ó", "O", name)
    name = re.sub("Ö", "Oe", name)
    name = re.sub("Ø", "O", name)
    name = re.sub("Ø", "O", name)
    name = re.sub("ß", "ss", name)
    name = re.sub("à", "a", name)
    name = re.sub("á", "a", name)
    name = re.sub("ã", "a", name)
    name = re.sub("Ä", "Ae", name)
    name = re.sub("ä", "ae", name)
    name = re.sub("ç", "c", name)
    name = re.sub("ç", "c", name)
    name = re.sub("è", "e", name)
    name = re.sub("è", "e", name)
    name = re.sub("é", "e", name)
    name = re.sub("é", "e", name)
    name = re.sub("ê", "e", name)
    name = re.sub("ë", "e", name)
    name = re.sub("ì", "i", name)
    name = re.sub("í", "i", name)
    name = re.sub("í", "i", name)
    name = re.sub("ï", "i", name)
    name = re.sub("ñ", "n", name)
    name = re.sub("ñ", "n", name)
    name = re.sub("ò", "o", name)
    name = re.sub("ò", "o", name)
    name = re.sub("ó", "o", name)
    name = re.sub("ó", "o", name)
    name = re.sub("ô", "o", name)
    name = re.sub("õ", "o", name)
    name = re.sub("õ", "o", name)
    name = re.sub("Ö", "Oe", name)
    name = re.sub("ö", "oe", name)
    name = re.sub("ø", "o", name)
    name = re.sub("ø", "o", name)
    name = re.sub("ù", "u", name)
    name = re.sub("ù", "u", name)
    name = re.sub("ú", "u", name)
    name = re.sub("ú", "u", name)
    name = re.sub("Ü", "Ue", name)
    name = re.sub("ü", "ue", name)
    name = re.sub("ý", "y", name)
    name = re.sub("ý", "y", name)
    name = re.sub("ć", "c", name)
    name = re.sub("ć", "c", name)
    name = re.sub("č", "c", name)
    name = re.sub("č", "c", name)
    name = re.sub("ě", "e", name)
    name = re.sub("ī", "I", name)
    name = re.sub("Ł", "L", name)
    name = re.sub("ł", "l", name)
    name = re.sub("ń", "n", name)
    name = re.sub("ř", "r", name)
    name = re.sub("ř", "r", name)
    name = re.sub("Š", "S", name)
    name = re.sub("š", "s", name)
    name = re.sub("š", "s", name)
    name = re.sub("ũ", "u", name)
    name = re.sub("Ž", "Z", name)
    name = re.sub("Ž", "Z", name)
    name = re.sub("ž", "z", name)
    name = re.sub("ế", "e", name)
    name = re.sub("ồ", "o", name)
    name = re.sub("—", "", name)
    name = re.sub("’", "", name)
    name = re.sub("工作室", "", name)

    if str(y) == YEAR_DEFAULT:
        y = EMPTY
    tmp  = (name, str(y))                                               # construct an author year tuple
    if not (tmp in dc.allauthoryears):                                  # store it in a dictionary
        dc.allauthoryears[tmp] = ord("a") - 1
    else:
        tmp2  = dc.allauthoryears[tmp]                                  # append a small letter
        tmp2 += 1                                                       # (the next in the alphabet)
        dc.allauthoryears[tmp] = tmp2
        if tmp2 <= 122:
            tmp = (name, str(y), "." + chr(tmp2))
        else:                                                           # add a second letter
            remain = (tmp2 - 97) % 26 + 1
            times  = (tmp2 - 97) // 26
            tmp    = (name, str(y),
                      "." + chr(times + 96) + chr(remain + 96))
    return tmp

# ------------------------------------------------------------------
def get_local_packages(d:str, dc=dc_var) ->set:                         # function get_local_packages(d)
    """
    Lists all local packages in the current OS folder d.

    Parameters:
    ----------
    d    str
         name of the OS folder to be analyzed
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a set (= local packages).

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    if dc.debugging:
        print("+++ -CTANOut:get_local_packages")

    tmp  = os.listdir(d)                                                # get local OS folder list
    tmp2 = []

    for f in tmp:                                                       # check all the files
        if dc.p6.match(f) and not (f in EXCLUSION):                        # name matches
            tmp3 = f[0:len(f) - 4]
            tmp2.append(tmp3)
    return set(tmp2)

# ------------------------------------------------------------------
def get_year_packages(dc=dc_var) ->set:                                 # function get_package_set
    """
    Analyzes dictionary 'yearpackages' for year templates.

    Rewrites the variable set dc.yearpackages.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a set of selected packages.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.yearpackages  python dictionary: each element:
                     <year>: <list of package names> 
    dc.verbose       Flag: output is verbose
    dc.debugging     flag: debugging

    Poosible message:
    ----------------
    + Warning: no package found which matches the specified {year}
               template '{dc.year_template}'
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:get_year_packages")

    tmp = set()
    for f in dc.yearpackages:                                           # loop over all the year-package correspondences
        if dc.p10.match(f):                                                # check: year matches year_template
            tmp2 = set(dc.yearpackages[f])
            tmp = tmp | tmp2
    if len(tmp) == 0:
        if dc.verbose:
            tmp_y = "year"
            print("--- Warning: no package found which matches the",
                  f"specified {tmp_y} template '{dc.year_template}'")

    return tmp

# ------------------------------------------------------------------
def get_year(s:str, dc=dc_var) ->int:                                   # function get_year
    """
    Gets the most recent year in string s (only for BibLaTeX).

    Includes decimal numbers in the intervall
    [YEAR_DEFAULT, MAX_DEFAULT].

    Parameters:
    ----------
    s    str
         string to be analyzed
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns the maximum year in s (int).

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:get_year")

    nn:list    = dc.p4.split(s)                                            # split the given string according p4: re.compile("[- |.,a-z]")
    years:list = []
    yd:int     = int(YEAR_DEFAULT)

    for i in nn:                                                        # loop over all elements
        if i.isdecimal():                                               # element is decimal
            if (yd <= int(i)) and (int(i) <= int(MAX_DEFAULT)):         # element is in the intervall [YEAR_DEFAULT, MAX_DEFAULT]?
                years.append(int(i))                                    # element is collected
    if len(years) >= 1:                                                 # there is at least one year
        return max(years)                                               # maximum is calculated
    else:                                                               # there is no year
        return YEAR_DEFAULT

# ------------------------------------------------------------------
def TeX_fold(s:str, dc=dc_var) ->str:                                   # function TeX_fold
    """
    Shortens|folds strings with long option values (in LaTeX tabular
    output).

    Parameters:
    ----------
    s    str
         TeX string to be folded
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Returns:
    -------
    Returns a folded string (str).

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:TeX_fold")

    OFFSET     = 64 * BLANK                                             # left indendation
    MAXLEN     = 65                                                     # maximal line length
    SEP        = "|"                                                    # separator in input and output
    parts:list = s.split(SEP)
    line:str   = EMPTY
    out:str    = EMPTY

    for f in range(0,len(parts) ):
        if f != len(parts) - 1:
            line = line + "\\verb§" + parts[f] + SEP + "§"
        else:
            line = line + "\\verb§" + parts[f] + "§"
        if len(line) >= MAXLEN:
            out  = out + line + "\\\\\n" + OFFSET + "&"
            line = EMPTY
    out = out + line
    return out

# ------------------------------------------------------------------
def TeXchars(s:str, dc=dc_var) ->str:                                   # function TeXchars
    """
    Prepares characters for LaTeX|BibLaTeX (with the exception of
    description).

    s    str
         string with characters which are to be prepared for
         LaTeX|BibLaTeX
         no ddefault
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a changed string.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:TeXchars")

    tmp = s
    tmp = re.sub(r"\\", r"{\\textbackslash}", tmp)
    tmp = re.sub("_", r"\\_", tmp)
    tmp = re.sub("&", r"{\\&}", tmp)
    tmp = re.sub(r"[\^]", r"{\\textasciicircum}", tmp)
    tmp = re.sub("[$]", r"\\$", tmp)
    return tmp


# ==================================================================
# I. main functions

# ------------------------------------------------------------------
def alias(k:xml.etree.ElementTree.Element, dc=dc_var):                  # function alias
    """
    Processes the 'alias' element.

    Inspects embedded text and the ambedded attribute id.
    Rewrites the variables dc.notice, dc.s_alias, dc.package_id.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable' 
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice      string for RIS|BibLaTeX: collection for
                   N1 a/o note
    dc.s_alias     string for Excel: alias
    dc.package_id  string: package id
    dc.debugging   flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:alias")

    id  = k.get("id", EMPTY)                                            # get attribute id

    if len(k.text) > 0:                                                 # get embedded text
        tmp = k.text
    else:
        tmp = DEFAULT_TEXT                                              # if k.text is empty

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(r"\item[Alias] " + r"\texttt{" + tmp + "}\n")
        dc.out.write(f"\\index{{Package!{tmp} " +\
                  f"(alias for {dc.package_id})}}\n")
        dc.out.write(f"\\index{{Alias!{tmp} (for {dc.package_id})}}\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        if tmp != EMPTY:
            dc.out.write("\n" + "alias: ".ljust(LABEL_WIDTH) + tmp)
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (FIELD_WIDTH + 2)}Alias: {tmp}"
        else:
            dc.notice = f"Alias: {tmp}"
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH+1)}Alias: {tmp}"
        else:
            dc.notice = f"Alias: {tmp}"
    elif dc.mode in ["Excel"]:                                          # Excel
        if dc.s_alias != EMPTY:
            dc.s_alias += f"; {tmp}"                                    # accumulate s_alias string
        else:
            dc.s_alias = tmp

    if dc.debugging:
        print("+++ <CTANOut:alias")

# ------------------------------------------------------------------
def also(k:xml.etree.ElementTree.Element, dc=dc_var):                   # function also
    """
    Processes the 'also' elements.

    Fetches the local attribute refid.
    Rewrites the variables dc.s_also, dc.notice, dc.also_str.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.s_also      string for Eccel: also
    dc.notice      string for RIS|BibLaTeX: collection for N1 a/o note
    dc.also_str    string: collect also
    dc.debugging   flag: debugging

    CValls:
    ------
    + TeXchars

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:also")

    refid = k.get("refid",EMPTY)                                        # get attribute refid

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        refid2 = re.sub("_", "-", refid)                                # substitute "_"
        if refid in dc.packages:
            tmp1   = TeXchars(dc.packages[refid][0])
            tmp2   = TeXchars(dc.packages[refid][1])
            dc.out.write(f"\\item[see also] see " +\
                      f"section~\\ref{{pkg:{refid2}}}" + \
                      f" on page~\\pageref{{pkg:{refid2}}}:" + \
                      f" (\\texttt{{{tmp1}}} -- {tmp2})\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        if refid in dc.packages:
            dc.out.write("\n" + "see also: ".ljust(LABEL_WIDTH) + \
                      refid + " (" + dc.packages[refid][0] + " -- " + \
                      dc.packages[refid][1] + ")")
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:                                          # accumulate notice string}
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH+1)}Also: {refid}"
        else:
            dc.notice = f"Also: {refid}"
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        if refid in dc.packages:
            tmp = EMPTY.join(dc.citation_keys[refid])
            if dc.also_str != EMPTY:
                dc.also_str += f"; {tmp}"                               # accumulate also_str string
            else:
                dc.also_str = tmp
    elif dc.mode in ["Excel"]:                                          # Excel
        if refid in dc.packages:
            if dc.s_also != EMPTY:
                dc.s_also += f"; {refid}"                               # accumulate s_also string
            else:
                dc.s_also = refid

    if dc.debugging:
        print("+++ <CTANOut:also")

# ------------------------------------------------------------------
def authorref(k:xml.etree.ElementTree.Element, dc=dc_var):              # function authorref
    """
    Processes the 'authorref elements', constructs the complete name and
    dc.usedAuthors entry.

    Fetches the local attributes key, id, givenname, familyname, active.
    Rewrites the variables dc.authorexists, dc.s_author, dc.usedAuthors.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.authorexists   flag; True, if an author exists
    dc.s_author       string for Excel: authorref
    dc.usedAuthors    dictionary: collects used authors
    dc.debugging      flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 2.58   2024-02-28 in authorref and copyrighT: enable processing 
    #                   of "_" in author|owner names
    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:authorref")

    key        = k.get("key", EMPTY)                                    # get attribute key
    xid        = k.get("id", EMPTY)                                     # get attribute id
    givenname  = k.get("givenname", EMPTY)                              # get attribute givenname
    familyname = k.get("familyname", EMPTY)                             # get attribute familyname
    active     = k.get("active", EMPTY)                                 # get attribute active
    tmp        = givenname

    if (xid != EMPTY) and (xid in dc.authors):                          # attribute xid is used
        key = xid
        givenname, familyname = dc.authors[xid]                         # find givenname, familyname in authors
        tmp = givenname
    else:
        key = xid
        givenname, familyname = EMPTY, AUTHOR_UNKNOWN                   # givenname, familyname not found
        tmp = givenname

    if familyname != EMPTY:                                             # constructs the complete name + usedAuthors entry
        tmp  += BLANK + familyname
        tmp2 = familyname + ", " + givenname
        dc.usedAuthors[key] = (givenname, familyname)                   # store actual author in usedAuthors
    else:
        tmp2             = tmp
        dc.usedAuthors[key] = (givenname)                               # store actual author in usedAuthors

    if active == "false":
        tmp = tmp + " (not active)"

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        tmp2 = TeXchars(tmp2)
        dc.out.write(f"\\item[author] {tmp2}\n")
        dc.out.write(f"\\index{{Author!{tmp2}}}\n")
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        dc.out.write("AU  - " + tmp2 + "\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "author: ".ljust(LABEL_WIDTH) + tmp)
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        pass                                                            # for BibLaTeX do nothing
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    dc.authorexists = True

    if dc.debugging:
        print("+++ <CTANOut:authorref")

# ------------------------------------------------------------------
def caption(k:xml.etree.ElementTree.Element, dc=dc_var):                # function caption
    """
    Processes the 'caption' element (sub title).

    Fetches any embedded text.
    Rewrites the variable dc.s_caption.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.s_caption    string for Excel: caption
    dc.debugging    flag: debugging

    Calls:
    -----
    + TeXchars
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:caption")

    if len(k.text) > 0:                                                 # get embedded text
        tmp = k.text.strip()
    else:
        tmp = DEFAULT_TEXT                                              # if k.text is empty

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        tmp = TeXchars(tmp)
        tmp = re.sub("#", "\\#", tmp)
        dc.out.write(f"\\item[caption] {tmp}\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "caption: ".ljust(LABEL_WIDTH) + tmp)
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        dc.out.write(f"T2  - {tmp}\n"         )                         # subtitle
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        tmp = TeXchars(tmp)
        tmp = re.sub("#", "\\#", tmp)

        if bibfield_test(tmp, "subtitle"):                              # subtitle
            dc.out.write("subtitle".ljust(FIELD_WIDTH) + "= {" + tmp + \
                      "}, \n")
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_caption = tmp

    if dc.debugging:
        print("+++ <CTANOut:caption")

# ------------------------------------------------------------------
def contact(k:xml.etree.ElementTree.Element, dc=dc_var):                # function contact
    """
    Processes the 'contact' elements.

    Fetches the local attributes type, href.
    Rewrites the variables dc.notice, dc.contact_str, dc.s_contact.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice        string for RIS|BibLaTeX: collection for N1
                     a/o note
    dc.contact_str   string: collect contact
    dc.s_contact     string for Excel: contact element
    dc.debugging     flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:contact")

    typeT = k.get("type", EMPTY)                                        # get attribute type (announce, bugs, development, repository, support)
    href  = k.get("href", EMPTY)                                        # get attribute href

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(f"\\item[contact] \\textit{{{typeT}}}: " +\
                  f"\\url{{{href}}}\n")
        dc.out.write(f"\\index{{Contact!{typeT}}}\n")
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f"\\\\\n{BLANK * (RIS_FIELDWIDTH + 1)}" +\
                      f"Contact: {typeT}: {href}"
        else:
            dc.notice = f"Contact: {typeT}: "                           # href
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        if dc.contact_str != EMPTY:                                     # accumulate contact_str string
            dc.contact_str += f"; {typeT}: {href}"
        else:
            dc.contact_str = f"{typeT}: {href}"
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "contact: ".ljust(LABEL_WIDTH) + typeT + \
                  ": " + href)
    elif dc.mode in ["Excel"]:                                          # Excel
        if dc.s_contact != EMPTY:                                       # accumulate s_contact string
            dc.s_contact += f"; {typeT}: {href}"
        else:
            dc.s_contact = f"{typeT}: {href}"

    if dc.debugging:
        print("+++ <CTANOut:contact")

# ------------------------------------------------------------------
def copyrightT(k:xml.etree.ElementTree.Element, p:str, dc=dc_var):      # function copyrightT
    """
    Processes the 'copyright' element.

    Fetches the emebedded attributes owner, year.
    Rewrites the variables dc.notice, dc.copyright_str, dc.s_copyright,
    dc.year_str.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    p    str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice           string for RIS|BibLaTeX: collection for N1
                        a/o note
    dc.copyright_str    string: collect copyright
    dc.s_copyright      string for Excel: copyright
    dc.year_str         string: collect all year items for a package
    dc.debugging        flag: debugging

    Calls:
    -----
    + TeXchars

    Messages:
    --------
    There are no specific messages.
    """

    # 2.58    2024-02-28 in authorref and copyrighT: enable processing 
    #                    of "_" in author|owner names
    # 2.65    2025-02-06 wherever appropriate: string interpolation with
    #                    f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:copyrightT")

    owner    = k.get("owner", EMPTY)                                    # get attribute owner
    year     = k.get("year", "--")                                      # get attribute year

    dc.year_str = dc.year_str + "|" + year                              # append year to year_str

    tmp   = owner
    if year != "--":                                                    # construct "owner (year)"
        tmp = tmp + " (" + year + ")"
    tmp = re.sub("[ \t]+", BLANK, tmp)

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        tmp = TeXchars(tmp)
        dc.out.write(f"\\item[copyright] {tmp}\n")
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK*(RIS_FIELDWIDTH + 1)}" +\
                         f"Copyright: {tmp}"
        else:
            dc.notice = f"Copyright: {tmp}"
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        tmp = re.sub("_", r"\\_", tmp)
        tmp = TeXchars(tmp)
        if dc.copyright_str != EMPTY:                                   # accumulate copyright string
            dc.copyright_str += f"; {tmp}"
        else:
            dc.copyright_str = tmp
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "copyright: ".ljust(LABEL_WIDTH) + tmp)
    elif dc.mode in ["Excel"]:                                          # Excel
        if dc.s_copyright != EMPTY:                                     # accumulate s_copyright string
            dc.s_copyright += f"; {tmp}"
        else:
            dc.s_copyright = tmp

    if dc.debugging:
        print("+++ <CTANOut:copyrightT")

# ------------------------------------------------------------------
def ctan(k:xml.etree.ElementTree.Element, t:str, dc=dc_var):            # function ctan
    """
    Processes the 'ctan' element.

    Fetches the local attributes path and file.
    Rewrites the variables dc.s_ctan, dc.notice.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    t    str
         current package date
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.s_ctan     string for Excel: ctan
    dc.notice     string for RIS|BibLaTeX: collection for N1
                  a/o note
    dc.debugging  flag: debugging

    Calls:
    -----
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:ctan")

    xpath = k.get("path", EMPTY)                                        # get attribute path
    file  = k.get("file", EMPTY)                                        # get attribute file

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(f"\\item[on CTAN] \\url{{{CTAN_URL2 + xpath}}}\n")
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}on CTAN: "+\
                      f"{CTAN_URL2}{xpath}"
        else:
            dc.notice = f"on CTAN: {CTAN_URL2}{xpath}"
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "on CTAN: ".ljust(LABEL_WIDTH) + 
                  CTAN_URL2 + xpath)
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        if bibfield_test(CTAN_URL2 + xpath, "userc"):                   # userc
            dc.out.write("userc".ljust(FIELD_WIDTH) + "= {" + \
                      CTAN_URL2 + xpath + "},\n")
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_ctan = CTAN_URL2 + xpath

    if dc.debugging:
        print("+++ <CTANOut:ctan")

# ------------------------------------------------------------------
def documentation(k:xml.etree.ElementTree.Element, dc=dc_var):          # function documentation
    """
    Processes the 'documentation' elements.

    Fetches the local attributes details, href, language.
    Rewrites the variables dc.notice, dc.language_set, dc.info_files,
    dc.XML_toc.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice           string for RIS|BibLaTeX: collection for N1
                        a/o note
    dc.language_set     set: collect language
    dc.info_files       list of local PDF files
    dc.XML_toc          python dictionary:  list of XML and PDF files:
                        dc.XML_toc[CTAN address]=(XML file, key, plain
                        PDF file name)
    dc.s_documentation  string for Excel: documentation
    dc.debugging        flag: debugging
    dc.verbose          Flag: output is verbose

    Calls:
    -----
    + TeXchars

    Possible message:
    ----------------
    + Warning: unknown language code '{language}' in '{tmp_d}'; ignored
    """

    # 2.65    2025-02-06 wherever appropriate: string interpolation with
    #                    f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:documentation")

    details  = k.get("details", EMPTY)                                  # get attribute details
    href     = k.get("href", EMPTY)                                     # get attribute href
    language = k.get("language", NLS)                                   # get attribute language

    href2    = href.replace("ctan:/", CTAN_URL2)
    p        = None

    if language in LANGUAGECODES:                                       # convert language keys
        tmp_l     = LANGUAGECODES[language]
        languagex = f"({tmp_l})"
        dc.language_set.add(language)
    else:
        languagex = EMPTY
        if language != EMPTY:
            if dc.verbose:
                tmp_d = "documentation"
                print("----- Warning: unknown language",
                      f"code '{language}' in '{tmp_d}'; ignored")

    if languagex != EMPTY:                                              # gives <re.Match object; span=(18, 24), match='French'>, for instance
        p = re.search(LANGUAGECODES[language], details)

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        details = TeXchars(details)
        if p == None:                                                   # no language found in details
            dc.out.write(f"\\item[documentation]  {languagex}" +\
                      f" \\textit{{{details}}}: \\url{{{href2}}}\n")
        else:
            dc.out.write("\\item[documentation]" +\
                      f" \\textit{{{details}}}: \\url{{{href2}}}\n")
        if href in dc.XML_toc:
            tmp    = dc.XML_toc[href]
            one_if = tmp[1] + "-" + tmp[2]                              # one info file
            fx2    = "./" + one_if
            dc.out.write("\\item[-- local file]".\
                      ljust(LABEL_WIDTH + 1) + " \\verb|" + fx2 + "|\n")
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        if dc.list_info_files:
            dc.out.write(f"UR  - {href2}\n")
            if href in dc.XML_toc:
                tmp    = dc.XML_toc[href]
                one_if = tmp[1] + "-" + tmp[2]                          # one info file
                fx     = os.path.abspath(one_if)
                dc.out.write(f"L1  - {fx}\n")
        if p == None:                                                   # no language found in details
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}" +\
                      f"Documentation {languagex}: {details}: {href2}"  # accumulate notice string
        else:
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}" +\
                      f"Documentation: {details}: {href2}"              # accumulate notice string
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        details = TeXchars(details)
        if dc.list_info_files:
            if href in dc.XML_toc:
                tmp        = dc.XML_toc[href]
                one_if     = f"{tmp[1]}-{tmp[2]}"
                                                                        # one info file
                dc.info_files += [one_if]
        if p == None:                                                   # no language found in details
            tmp = f"Documentation {languagex}: {details}: {href2}"
        else:
            tmp = f"Documentation: {details}: {href2}"

        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (FIELD_WIDTH + 2)}{tmp}"
        else:
            dc.notice = tmp
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        if p == None:                                                   # no language found in details
            dc.out.write("\ndocumentation: ".ljust(LABEL_WIDTH + 1) + \
                      details + BLANK + languagex + ": " + href2)
        else:
            dc.out.write("\ndocumentation: ".ljust(LABEL_WIDTH + 1) + \
                      details + ": " + href2)
        if href in dc.XML_toc:
            tmp    = dc.XML_toc[href]
            one_if = tmp[1] + "-" + tmp[2]                              # one info file
            dx     = "./" + one_if
            dc.out.write("\n-- local file: ".ljust(LABEL_WIDTH + 1) + dx)
    elif dc.mode in ["Excel"]:                                          # Excel
        if dc.s_documentation != EMPTY:                                 # accumulate s_documentation string
            dc.s_documentation += f"; {details}: {href2}"
        else:
            dc.s_documentation = f"{details}: {href2}"

    if dc.debugging:
        print("+++ <CTANOut:documentation")

# -----------------------------------------------------------------
def entry(k:xml.etree.ElementTree.Element, t:str, p:str, dc=dc_var):    # function entry
    """
    Processes the main element 'entry'.

    Fetches the local attribute id.
    Fetches the embedded text.
    Rewrites many variables.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    t    str
         current package date
         no default
    p    str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging        flag: debugging
    dc.notice           string for RIS|BibLaTeX: collection for N1  a/o note
    dc.package_id       string: package id
    dc.s_alias          string for Excel: alias element
    dc.s_also           string for Excel: also element 
    dc.s_author         string for Excel: authoref elements (collected)
    dc.s_caption        string for Excel: caption element 
    dc.s_contact        string for Excel: contact element
    dc.s_copyright      string for Excel: copyright elements (collected)
    dc.s_ctan           string for Excel: ctan element
    #dc.s_date           string for Excel: 
    dc.s_documentation  string for Excel: documentation elements (collected) 
    dc.s_home           string for Excel: home element
    dc.s_id             string for Excel: id attribute in entry element
    dc.s_install        string for Excel: install element
    dc.s_keyval         string for Excel: keyval elements (collected)
    dc.s_language       string for Excel: extracted from documentation
                        and description (collected) 
    dc.s_lastaccess     string for Excel: day of last download 
    dc.s_lastchanges    string for Excel: extracted from version element 
    dc.s_license        string for Excel: license elements (collected)
    dc.s_miktex         string for Excel: miktex element
    dc.s_name           string for Excel: name element
    dc.s_texlive        string for Excel: texlive element
    dc.s_version        string for Excel: version element   
    dc.s_year           string for Excel: extracted from copyright and
                        version 

    Calls:
    -----
    + leading
    + description
    + name
    + alias
    + caption
    + authorref
    + copyrightT
    + licenseT
    + version
    + documentation
    + ctan
    + miktex
    + texlive
    + keyval
    + install
    + contact
    + also
    + home
    + trailing

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:entry")

    if dc.mode in ["Excel"]:                                            # initialize strings for Excel;
        dc.s_id                     = k.get("id", EMPTY)                # get attribute id
        dc.s_alias                  = EMPTY                             # alias element
        dc.s_also                   = EMPTY                             # also element
        dc.s_author                 = EMPTY                             # authoref elements (collected)
        dc.s_caption                = EMPTY                             # caption element
        dc.s_contact                = EMPTY                             # contact element
        dc.s_copyright              = EMPTY                             # copyright elements (collected)
        dc.s_ctan                   = EMPTY                             # ctan element
        #dc.s_date                   = EMPTY                             # xx element
        dc.s_documentation          = EMPTY                             # documentation elements (collected)
        dc.s_home                   = EMPTY                             # home element
        dc.s_install                = EMPTY                             # install element
        dc.s_keyval                 = EMPTY                             # keyval elements (collected)
        dc.s_language               = EMPTY                             # extracted from documentation and description (collected)
        dc.s_license                = EMPTY                             # license elements (collected)
        dc.s_miktex                 = EMPTY                             # miktex element
        dc.s_name                   = EMPTY                             # name element
        dc.s_texlive                = EMPTY                             # texlive element
        dc.s_version                = EMPTY                             # version element
        dc.s_year                   = EMPTY                             # extracted from copyright and version
        dc.s_lastchanges            = EMPTY                             # extracted from version element
        dc.s_lastaccess             = EMPTY                             # day of last download

    leading(k, p, t)
    dc.package_id = k.get("id", EMPTY)                                  # get attribute id

    for child in k:                                                     # call the sub-elements
        if child.tag == "description":                                  # description
            if dc.mode != "Excel":                                      # not for Excel
                if not child.tag in dc.skip:
                    description(child, p)
        elif child.tag == "name":                                       # name
            if not child.tag in dc.skip:
                name(child)
        elif child.tag == "alias":                                      # alias
            if not child.tag in dc.skip:
                alias(child)
        elif child.tag == "caption":                                    # caption
            if not child.tag in dc.skip:
                caption(child)
        elif child.tag == "authorref":                                  # authorref
            if not child.tag in dc.skip:
                authorref(child)
        elif child.tag == "copyright":                                  # copyright
            if not child.tag in dc.skip:
                copyrightT(child, p)
        elif child.tag == "license":                                    # license
            if not child.tag in dc.skip:
                licenseT(child)
        elif child.tag == "version":                                    # version
            if not child.tag in dc.skip:
                version(child, p)
        elif child.tag == "documentation":                              # documentation
            if not child.tag in dc.skip:
                documentation(child)
        elif child.tag == "ctan":                                       # ctan
            if not child.tag in dc.skip:
                ctan(child, t)
        elif child.tag == "miktex":                                     # miktex
            if not child.tag in dc.skip:
                miktex(child)
        elif child.tag == "texlive":                                    # texlive
            if not child.tag in dc.skip:
                texlive(child)
        elif child.tag == "keyval":                                     # keyval
            if not child.tag in dc.skip:
                keyval(child)
        elif child.tag == "install":                                    # install
            if not child.tag in dc.skip:
                install(child)
        elif child.tag == "contact":                                    # contact
            if not child.tag in dc.skip:
                contact(child)
        elif child.tag == "also":                                       # also
            if not child.tag in dc.skip:
                also(child)
        elif child.tag == "home":                                       # home
            if not child.tag in dc.skip:
                home(child)
    trailing(k, t, p)

    if dc.debugging:
        print("+++ <CTANOut:entry")

# ------------------------------------------------------------------
def first_lines(dc=dc_var):                                             # function first_lines()
    """
    Creates the first lines of output.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    Flag: output is verbose

    Calls:
    -----
    + make_usepkg()                                    
    + make_header()
    + make_title()
    + make_classoptions()
    
    Possible messages:
    -----------------
    + Info: Program call: <act_programname> <arguments>
    + Info: program call (with details): <PROGRAM_NAME>
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.4    2026-07-10 handling of LaTeX source code texts improved
    # 3.4.3  2026-07-10 call the new functions
    # 3.11   2026-08-16 Calculation and output of the input string
    # 3.11.1 2026-08-16 moved from first_lines to argparse_postprocess

    if dc.debugging:
        print("+++ >CTANOut:first_lines")

    if dc.verbose:                                                      # header for terminal output
        print("\n" + "[CTANOut] Info: program call (with details): ",
              PROGRAM_NAME)
        if dc.make_topics != MAKE_TOPICS_DEFAULT:                       # -mt
            tmp_mt = "(" + (TOPICS_TEXT + ")")[0:50] + ELLIPSIS
            print(f'  {"-mt":5} {tmp_mt:60}')
        if dc.no_files != NO_FILES_DEFAULT:                            # -nf
            tmp_nf = "(" + NO_FILES_TEXT + ")"
            print(f'  {"-nf":5} {tmp_nf:60}')
        if dc.statistics != STATISTICS_DEFAULT:                        # -stat
            tmp_stat = "(" + STATISTICS_TEXT + ")"
            print(f'  {"-stat":5} {tmp_stat:60}')
        if dc.verbose != VERBOSE_DEFAULT:                              # -v
            tmp_v = "(" + VERBOSE_TEXT + ")"
            print(f'  {"-v":5} {tmp_v:60}')
        if dc.mode != MODE_DEFAULT:                                    # -m
            tmp_m = "(" + MODE_TEXT + ")"
            print(f'  {"-m":5} {tmp_m:60} {dc.mode}')

        if dc.verbose != VERBOSE_DEFAULT:                              # -A
            tmp_A = "(" + AUTHOR_TEMPLATE_TEXT + ")"
            print(f'  {"-A":5} {tmp_A:60} {fold(dc.author_template)}')
        if dc.license_template != LICENSE_TEMPLATE_DEFAULT:             # -L
            tmp_L= "(" + LICENSE_TEMPLATE_TEXT + ")"
            print(f'  {"-L":5} {tmp_L:60} {fold(dc.license_template)}')
        if dc.name_template != NAME_TEMPLATE_DEFAULT:                   # -t
            tmp_t = "(" + TEMPLATE_TEXT + ")"
            print(f'  {"-t":5} {tmp_t:60} {fold(dc.name_template)}')
        if dc.key_template != KEY_TEMPLATE_DEFAULT:                    # -k
            tmp_k = "(" + KEY_TEMPLATE_TEXT + ")"
            print(f'  {"-k":5} {tmp_k:60} {fold(dc.key_template)}')
        if dc.year_template != YEAR_TEMPLATE_DEFAULT:                  # -y
            tmp_y = "(" + YEAR_TEMPLATE_TEXT + ")"
            print(f'  {"-y":5} {tmp_y:60} {fold(dc.year_template)}')

        if dc.direc != DIREC_DEFAULT:                                   # -d
            tmp_d = "(" + DIREC_TEXT + ")"
            print(f'  {"-d":5} {tmp_d:60} {dc.direc}')
        if dc.out_file != OUT_DEFAULT:                                  # -o
            tmp_o = "(" + OUT_TEXT + ")"
            print(f'  {"-o":5} {tmp_o:60} {dc.out_file}')
        if dc.skip != SKIP_DEFAULT:                                     # -s
            tmp_s = "(" + SKIP_TEXT + ")"
            print(f'  {"-s":5} {tmp_s:60} {dc.skip}')
        if dc.skip_biblatex != SKIP_BIBLATEX_DEFAULT:                   # -sb
            tmp_sb = "(" + SKIP_BIBLATEX_TEXT + ")"
            print(f'  {"-sb":5} {tmp_sb:60} {dc.skip_biblatex}')
        if dc.btype != BTYPE_DEFAULT:                                   # -b
            tmp_b = "(" + (BTYPE_TEXT + ")")[0:50] + ELLIPSIS
            print(f'  {"-b":5} {tmp_b:60} {dc.btype}')
        print("\n")

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        usepkg       = make_usepkg()                                    
        header       = make_header()
        title        = make_title()
        classoptions = make_classoptions()
        dc.out.write(f"% File                   : {dc.out_file}\n")
        dc.out.write(f"% Encoding               : {FILE_ENCODING}\n")
        dc.out.write(f"% Date                   : {ACT_DATE}\n")
        dc.out.write(f"% Time                   : {ACT_TIME}\n\n")

        dc.out.write(f"% generated by           : {PROGRAM_NAME}\n")
        dc.out.write(f"% Program author         : {PROGRAM_AUTHOR}\n")
        dc.out.write(f"% Program version        : {PROGRAM_VERSION}\n")
        dc.out.write(f"% Program date           : {PROGRAM_DATE}\n\n")

        dc.out.write(f"% Program call           : {PROGRAM_NAME}" +\
                  f" {dc.arguments}\n")
        dc.out.write(f"% mode                   : {dc.mode}\n")
        dc.out.write(f"% skipped CTAN fields    : {dc.skip}\n")
        if dc.name_template != EMPTY:                                   # name_template
            dc.out.write("% filtered by name template   :"  +\
                      f" '{comment_fold(dc.name_template)}'\n")
        if dc.key_template != EMPTY:                                    # key_template
            dc.out.write("% filtered by key template    :" +\
                      f" '{comment_fold(dc.key_template)}'\n")
        if dc.author_template != EMPTY:                                 # autor_template
            dc.out.write("% filtered by author template :" +\
                      f" '{comment_fold(dc.author_template)}'\n")
        if dc.license_template != EMPTY:                                # icense_template
            dc.out.write("% filtered by license template:" +\
                      f" '{comment_fold(dc.license_template)}'\n")
        if dc.year_template != EMPTY:                                   # year_template
            dc.out.write("% filtered by year template   :" +\
                      f" '{comment_fold(dc.year_template)}'\n")
        dc.out.write("\n% --------------------------")
        dc.out.write("\n% to be compiled by LuaLaTeX")
        dc.out.write("\n% --------------------------\n")
##        dc.out.write(f"\n\\documentclass[{classoptions}\n]{{scrartcl}}\n")
        dc.out.write(classoptions)
        dc.out.write(usepkg)
        dc.out.write(title)
        dc.out.write(header)
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        dc.out.write(f"% File                   : {dc.out_file}\n")
        dc.out.write(f"% Encoding               : {FILE_ENCODING}\n")
        dc.out.write(f"% Date                   : {ACT_DATE}\n")
        dc.out.write(f"% Time                   : {ACT_TIME}\n\n")

        dc.out.write(f"% generated by           : {PROGRAM_NAME}\n")
        dc.out.write(f"% Program author         : {PROGRAM_AUTHOR}\n")
        dc.out.write(f"% Program version        : {PROGRAM_VERSION}\n")
        dc.out.write(f"% Program date           : {PROGRAM_DATE}\n\n")

        dc.out.write(f"% Program Call           : {PROGRAM_NAME} " +\
                  f"{dc.arguments}\n")
        dc.out.write(f"% Mode                   : {dc.mode}\n")
        dc.out.write(f"% skipped CTAN fields    : {dc.skip}\n")
        dc.out.write(f"% skipped BibLaTeX fields: {dc.skip_biblatex}\n")
        dc.out.write(f"% Type of BibLaTeX entries : {dc.btype}\n")
        if dc.name_template != EMPTY:                                   # name_template
            dc.out.write("% filtered by name template   :" +\
                      f" '{comment_fold(dc.name_template)}'\n")
        if dc.key_template != EMPTY:                                    # key_template
            dc.out.write("% filtered by key template    :" +\
                      f" '{comment_fold(dc.key_template)}'\n")
        if dc.author_template != EMPTY:                                 # author_template
            dc.out.write(f"% filtered by author template :" +\
                      f"' {comment_fold(dc.author_template)}'\n")
        if dc.license_template != EMPTY:                                # license_template
            dc.out.write("% filtered by license template:" +\
                      f"' {comment_fold(dc.license_template)}'\n")
        if dc.year_template != EMPTY:                                   # year_template
            dc.out.write("% filtered by year template   :" +\
                      f" '{comment_fold(dc.year_template)}'\n")
        dc.out.write("\n% actual mapping CTAN --> BibLaTeX fields\n")
        dc.out.write("% alias         --> embedded in 'note'\n")
        dc.out.write("% also          --> 'related'\n")
        dc.out.write("% authorref     --> collected in 'author'\n")
        dc.out.write("% caption       --> 'subtitle'\n")
        dc.out.write("% contact       --> collected in 'userd'\n")
        dc.out.write("% copyright     --> 'usera'; 'year' " + \
                  "(if applicable)\n")
        dc.out.write("% ctan          --> 'userc'\n")
        dc.out.write("""% description   --> 'abstract'; collected in
%                   'language' (if applicable)\n""")
        dc.out.write("""% documentation --> embedded in 'note'; local
%                   download in 'file' (if applicable);
%                   collected in 'language' (if applicable)\n""")
        dc.out.write("% home          --> 'usere'\n")
        dc.out.write("% install       --> 'userf'\n")
        dc.out.write("% keyval        --> collected in 'keywords'\n")
        dc.out.write("% license       --> 'userb'\n")
        dc.out.write("% miktex        --> embedded in 'note'\n")
        dc.out.write("% name          --> 'title'\n")
        dc.out.write("% texlive       --> embedded in 'note'\n")
        dc.out.write("% version       --> 'version'; 'year' " +\
                  "(if applicable)\n\n")
        dc.out.write("% a) If available, the program outputs the " +\
                  "following\n")
        dc.out.write("%    BibLaTex fields:\n")
        dc.out.write("%    abstract,author,date,file,keywords," +\
                  "language,note,\n")
        dc.out.write("%    related,subtitle,title,url,urldate,usera," +\
                  "userb,userc,\n")
        dc.out.write("%    userd,usere,userf,version,year\n")
        dc.out.write("% b) The BibLaTeX field 'note' is used for " +\
                  "collecting the\n")
        dc.out.write("%    following CTAN items:\n")
        dc.out.write("%    alias, contact, documentation, home, " +\
                  "install, \n")
        dc.out.write("%    license, miktex, texlive\n")
        dc.out.write("% c) The program uses the optional BibLaTeX " +\
                  "fields usera,\n")
        dc.out.write("%    userb, userc, userd, usere, userf\n")
        dc.out.write("\n% -----------------------")
        dc.out.write("\n% to be compiled by biber")
        dc.out.write("\n% -----------------------\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write(DOCUMENT_TITLE.center(80) + "\n" + \
                (DOCUMENT_SUBTITLE + PROGRAM_NAME).center(80) + "\n\n")
        dc.out.write(DOCUMENTAUTHOR_TXT.center(80) + "\n\n")

        dc.out.write(f"% File                    : {dc.out_file}\n")
        dc.out.write(f"% Encoding                : {FILE_ENCODING}\n")
        dc.out.write(f"% Date                    : {ACT_DATE}\n")
        dc.out.write(f"% Time                    : {ACT_TIME}\n\n")

        dc.out.write(f"% generated by            : {PROGRAM_NAME}\n")
        dc.out.write(f"% Program author          : {PROGRAM_AUTHOR}\n")
        dc.out.write(f"% Program version         : {PROGRAM_VERSION}\n")
        dc.out.write(f"% Program date            : {PROGRAM_DATE}\n\n")
        dc.out.write(f"% Program call            : " +\
                  f"{PROGRAM_NAME} {dc.arguments}\n")
        dc.out.write(f"% Mode                    : {dc.mode}\n")
        dc.out.write(f"% skipped CTAN fields     : {dc.skip}\n")
        if dc.name_template != EMPTY:                                   # name_template
            dc.out.write("% filtered by name template   :" +\
                      f" '{comment_fold(dc.name_template)}'\n")
        if dc.key_template != EMPTY:                                    # key_template
            dc.out.write("% filtered by key template    :" +\
                      f" '{comment_fold(dc.key_template)}'\n")
        if dc.author_template != EMPTY:                                 # author_template
            dc.out.write("% filtered by author template :" +\
                      f" '{comment_fold(dc.author_template)}'\n")
        if dc.license_template != EMPTY:                                # license_template
            dc.out.write("% filtered by license template:" + \
                      f" '{comment_fold(dc.license_template)}'\n")
        if dc.year_template != EMPTY:                                   # year_template
            dc.out.write("% filtered by year template   :" +\
                      f" '{comment_fold(dc.year_template)}'\n")
    elif dc.mode in ["RIS"] :                                           # RIS
        pass                                                            # for RIS do nothing
    elif dc.mode in ["Excel"] and not dc.no_files:                      # Excel: write head of table
        dc.out.write(S_ID_TEXT)
        for f in [S_AUTHOR_TEXT, S_NAME_TEXT, S_CAPTION_TEXT,
                  S_YEAR_TEXT, S_LASTCHANGES_TEXT, S_LANGUAGE_TEXT,
                  S_LASTACCESS_TEXT, S_VERSION_TEXT, S_KEYVAL_TEXT,
                  S_ALIAS_TEXT, S_ALSO_TEXT, S_CONTACT_TEXT,
                  S_COPYRIGHT_TEXT, S_CTAN_TEXT, S_DOCUMENTATION_TEXT,
                  S_HOME_TEXT, S_INSTALL_TEXT, S_LICENSE_TEXT,
                  S_MIKTEX_TEXT, S_TEXLIVE_TEXT]:
            dc.out.write("\t" + f)
        dc.out.write("\n")

    if dc.debugging:
        print("+++ <CTANOut:first_lines")

# ------------------------------------------------------------------
def get_author_packages(dc=dc_var) ->set:                               # function get_author_packages
    """
    Gets package names by specified author name template.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a set (authors and associated packages).

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.verbose    Flag: output is verbose
    dc.debugging  flag: debugging

    Possible message:
    ----------------
    + Warning: no package found which matches the specified {tmp_a}
               template '{dc.author_template}'
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.9    2026-08-19 minor corrections in error messages

    if dc.debugging:
        print("+++ -CTANOut:get_author_packages")

    author_pack = set()                                                 # initialize set
    tmp_set     = set()                                                 # initialize auxiliary set

    for f in dc.authors:                                                # loop over authors
        (gn, fn) = dc.authors[f]
        if fn != EMPTY:                                                 # get familyname
            tmp_a = dc.authors[f][1]
        else:
            tmp_a = dc.authors[f][0]                                    # if an incorrect entry is in authorsset
        if dc.p5.match(tmp_a):                                             # member matches template
            tmp_set.add(f)                                              # built-up a new auxiliary set

    for f in tmp_set:                                                   # loop over auxiliary set
        if f in dc.authorpackages:                                      # prevent a wrong entry
            for g in dc.authorpackages[f]:
                author_pack.add(g)                                      # built-up the resulting set
    if len(author_pack) == 0:
        if dc.verbose:
            tmp_a = "author"
            print("----- Warning: no package found which matches the",
                  f"specified {tmp_a} template '{dc.author_template}'")
    return author_pack

# ------------------------------------------------------------------
def get_name_packages(dc=dc_var) ->set:                                 # function get_name_packages
    """
    Gets package names by specified package name template.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Reurns a set (name of packages).

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose

    Possible message:
    ----------------
    + Warning: no package found which matches the specified {tmp_n}
               template '{dc.name_template}'
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.9    2026-08-19 minor corrections in error messages

    if dc.debugging:
        print("+++ -CTANOut:get_name_packages")

    name_pack = set()                                                   # initialize set

    for f in dc.packages:                                               # loop over packages
        if dc.p2.match(f):                                              # member matches template
            name_pack.add(f)                                            # built-up the resulting set
    if len(name_pack) == 0:
        if dc.verbose:
            tmp_n = "name"
            print("----- Warning: no package found which matches the",
                  f"specified {tmp_n} template '{dc.name_template}'")
    return name_pack

# ------------------------------------------------------------------
def get_topic_packages(dc=dc_var) ->set:                                # function get_topic_packages
    """
    Gets package names by specified topic template.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a set (used topics and related packages).

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose

    Possible message:
    ----------------
    + Warning: no package found which matches thespecified {tmp_t}
               template '{dc.key_template}'
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.9    2026-08-19 minor corrections in error messages

    if dc.debugging:
        print("+++ -CTANOut:get_topic_packages")

    topic_pack = set()                                                  # initialize set

    for f in dc.topicspackages:                                         # loop over topicspackages
        if dc.p3.match(f):                                                 # member matches template
            for g in dc.topicspackages[f]:                              # all packagexs for this entry
                topic_pack.add(g)                                       # built-up the resulting set
    if len(topic_pack) == 0:
        if dc.verbose:
            tmp_t = "topic"
            print("----- Warning: no package found which matches the",
                  f"specified {tmp_t} template '{dc.key_template}'")
    return topic_pack

# ------------------------------------------------------------------
def get_license_packages(dc=dc_var) ->set:                              # function get_license_packages
    """
    Gets package names by specified license template.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a set (used licenses and related packages).

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose

    Possible message:
    ----------------
    + Warning: no package found which matches the specified {tmp_l}
               template '{dc.key_template}'"
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.9    2026-08-19 minor corrections in error messages

    if dc.debugging:
        print("+++ -CTANOut:get_license_packages")

    license_pack = set()                                                # initialize set

    for lic in dc.licensepackages:                                      # loop over licensepackages
        lic2 = dc.licenses[lic][0]
        lic3 = dc.licenses[lic][1]
        if lic3 == "true":
            lic3 = "free"
        else:
            lic3 = "not free"
        if dc.p9.match(lic2) or dc.p9.match(lic) or dc.p9.match(lic3):           # collect packages with specified licenses
            for g in dc.licensepackages[lic]:
                license_pack.add(g)
    if len(license_pack) == 0:
        if dc.verbose:
            tmp_l = "license"
            print("----- Warning: no package found which matches the",
                  f"specified {tmp_l} template '{dc.license_template}'")
    return license_pack

# ------------------------------------------------------------------
def home(k:xml.etree.ElementTree.Element, dc=dc_var):                   # function home
    """
    Processes the 'home' element.

    Fetches the local attribute href.
    Rewrites the variables dc.notice, dc.s_home.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice      string for RIS|BibLaTeX: collection for N1 a/o note
    dc.s_home      string for Excel: home
    dc.debugging   flag: debugging

    Calls:
    -----
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:home")

    href = k.get("href", EMPTY)                                         # get attribute href

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(f"\\item[home page] \\url{{{href}}}\n")
    elif dc.mode in ["RIS"]:                                            # RIS"usere
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}" +\
                      f"Home page: {href}"
        else:
            dc.notice = f"Home page: {href}"
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        if bibfield_test(href, "usere"):                                # usere
            dc.out.write("usere".ljust(FIELD_WIDTH) + "= {" + \
                         href+ "},\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "home page: ".ljust(LABEL_WIDTH) + href)
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_home = href

    if dc.debugging:
        print("+++ <CTANOut:home")

# ------------------------------------------------------------------
def install(k:xml.etree.ElementTree.Element, dc=dc_var):                # function install
    """
    Processes the 'install' element.

    Fetches the local attribute path.
    Rewrites the variables dc.notice, dc.s_install.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice      string for RIS|BibLaTeX: collection for N1 a/o note
    dc.s_install   string for Excel: install
    dc.debugging   flag: debugging

    Calls:
    -----
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:install")

    xpath = k.get("path", EMPTY)                                        # get attribute path

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(f"\\item[installation]" +\
                  f"\\url{{{CTAN_URL3 + xpath}}}\n")
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}" +\
                      f"Installation: {CTAN_URL3} + {xpath}"            # accumulate notice string
        else:
            dc.notice = f"Installation: {CTAN_URL3}{xpath}"
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        if bibfield_test(CTAN_URL3 + xpath, "userf"):                   # userf
            dc.out.write("userf".ljust(FIELD_WIDTH) + "= {" +\
                      CTAN_URL3 + xpath + "},\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "installation: ".ljust(LABEL_WIDTH) + \
                  CTAN_URL3 + xpath)
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_install = CTAN_URL3 + xpath

    if dc.debugging:
        print("+++ <CTANOut:install")

# ------------------------------------------------------------------
def keyval(k:xml.etree.ElementTree.Element, dc=dc_var):                 # function keyval
    """
    Processes the 'keyval' elements.

    fetches the local attributes key, value.
    Rewrites the variables dc.s_keyval, dc.usedTopics, dc.topics.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.s_keyval    string for Excel: keyval
    dc.usedTopics  dictionary for collecting topics
    dc.topics      dictionary with unknown topics
    dc.debugging   flag: debugging

    Calls:
    -----
    + TeXchars

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:keyval")

    key   = k.get("key", EMPTY)                                         # get attribute key
    value = k.get("value", EMPTY)                                       # get attribute value

    if value in dc.topics:
        tmp   = dc.topics[value]
    else:
        tmp           = value + "(unknown)"                             # correction, if topic is unknown
        dc.topics[value] = tmp

    if not value in dc.usedTopics:                                      # collects topics in usedTopics
        dc.usedTopics[value] = 1
    else:
        dc.usedTopics[value] = dc.usedTopics[value] + 1

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        tmp = TeXchars(tmp)
        dc.out.write(f"\\item[keyword] \\texttt{{{value}}} ({tmp})\n")
        dc.out.write(f"\\index{{Topic!{value}}}\n")
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        dc.out.write(f"KW  - {value}\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "keyword: ".ljust(LABEL_WIDTH) + value + \
                  " (" + dc.topics[value] + ")")
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        pass                                                            # for BibLaTeX do nothing
    elif dc.mode in ["Excel"]:                                          # Excel
        pass

    if dc.debugging:
        print("+++ <CTANOut:keyval")

# ------------------------------------------------------------------
def leading(k:xml.etree.ElementTree.Element, p:str, t:str, dc=dc_var):  # function leading
    """
    Analyzes the first lines of each XML package file and print out
    some lines.

    Fetches the local attribute id.
    Inspects the elements caption, authorref.
    Rewrites the variables dc.authorexists, dc.s_lastaccess,
    dc.s_author.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    p    str
         name of the current package
         no default
    t    str
         current package date
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.authorexists    flag; True, if an author exists
    dc.s_lastaccess    string for Excel: Last access
    dc.s_author        string for Excel: authorref   
    dc.debugging       flag: debugging

    Calls:
    -----
    + TeXchars
    + get_year
    + get_authoryear
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:leading")

    xname = k.get("id", EMPTY)                                          # get attribute id
    xpath = CTAN_URL4 + p

    allauthors:list   = []                                              # initialize some variables
    year:str          = EMPTY
    date:str          = EMPTY
    year:str          = EMPTY
    xcaption:str      = EMPTY
    dc.authorexists   = False

    dc.usedPackages.append(xname)                                       # collect used packages

    for child in k:                                                     # find some supp. infos
        if child.tag == "caption":
            xcaption  = child.text                                      # embedded text xcaption
            xcaption2 = xcaption
            if len(xcaption2) >= MAX_CAPTION_LENGTH:
                xcaption2 = xcaption2[0 : MAX_CAPTION_LENGTH] + "xyz"
            xcaption2 = TeXchars(xcaption2)
            xcaption2 = re.sub("#", "\\#", xcaption2)

        if child.tag == "authorref":                                    # author(s) for mode=="BibLaTeX"
            onefamilyname = child.get("familyname", EMPTY)              # get attribute familyname
            onegivenname  = child.get("givenname", EMPTY)               # get attribute givenname
            active        = child.get("active", "true")                 # get attribute active
            oneauthor     = (onefamilyname, onegivenname)               # new variable
            xid           = child.get("id", EMPTY)                      # get attribute id

            if (xid != EMPTY) and (xid in dc.authors):
                onegivenname, onefamilyname = dc.authors[xid]
                oneauthor = (onefamilyname, onegivenname)
            else:
                onegivenname, onefamilyname = EMPTY, AUTHOR_UNKNOWN
                oneauthor = (onefamilyname, onegivenname)

            if active:
                allauthors.append(oneauthor)

    if dc.mode in ["BibLaTeX", "Excel"]:                                # BibLaTeX
        allauthors2 = []                                                # generate author string for  the current package
        for f in allauthors:
            f = list(f)

            if (BLANK in f[0]) and (dc.mode in ["BibLaTeX"]):
                f[0] = "{" + f[0] + "}"
            if (BLANK in f[1]) and (dc.mode in ["BibLaTeX"]):
                f[1] = "{" + f[1] + "}"

            if (f[0] != EMPTY) and (f[1] != EMPTY):
                 oneauthor = f[0] + ", " + f[1]
            elif (f[0] != EMPTY) and (f[1] == EMPTY):
                oneauthor = f[0]
            else:
                oneauthor = f[1]

            allauthors2.append(oneauthor)

        if len(allauthors2) > 0:
            author_string = allauthors2[0]
        else:
            author_string = AUTHOR_UNKNOWN

        if dc.mode in ["Excel"]:
            for f in range(1, len(allauthors2)):
                author_string = author_string + "; " + allauthors2[f]
        else:
            for f in range(1, len(allauthors2)):
                author_string = author_string + " and " + allauthors2[f]

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        xcaption  = TeXchars(xcaption)
        xcaption  = re.sub("#", "\\#", xcaption)
        xcaption2 = xcaption2.replace("xyz", "\\ldots")
        xname1    = TeXchars(xname)
        xname2    = re.sub("_", "-", xname)
        dc.out.write("\n%" + 80*"-")
        tmp       = r"\texttt{" + xname1 + "} -- "
##        dc.out.write(f"\n\\section[{tmp}{xcaption2}]{{{tmp}{xcaption}}}" +\
##                  f"\\label{{pkg:{xname2}}}\n")                         # (***)
        dc.out.write(f"""
\\section[{tmp}{xcaption2}]{{{tmp}{xcaption}}}\\label{{pkg:{xname2}}}
""")                         
        dc.out.write(f"\\index{{Package!{xname1}}}\n\n")
        dc.out.write("\\begin{labeling}{Web page on CTAN}\n")
        dc.out.write("\\item[Web page on CTAN] \\url{" + xpath + "}\n")
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        dc.out.write("TY  - ICOMM" + "\n")                              # header with type
        dc.out.write(f"UR  - {xpath}\n")                                # main URL
        dc.out.write(f"Y3  - {t}\n")                                    # date of last access
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        tmp = xname + " -- " + xcaption
        dc.out.write("\n\n\n" + tmp)
        dc.out.write("\n" + len(tmp) * "-")
        dc.out.write("\n" + "Web page on CTAN: ".ljust(LABEL_WIDTH) +\
                     xpath)
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        tmp7 = EMPTY.join(dc.citation_keys[p])                          # find citation key
        dc.out.write(f"\n{dc.btype}{{{tmp7},\n")                        # 1st line of citation

        if bibfield_test(author_string, "author"):                      # author
            dc.out.write("author".ljust(FIELD_WIDTH) + "= {" + \
                      author_string +  "},\n")                          # author(s)

        if bibfield_test(xpath, "url"):                                 # url
            dc.out.write("url".ljust(FIELD_WIDTH) + "= {" + xpath + \
                         "},\n")

        if bibfield_test(t, "urldate"):                                 # urldate (=date of last access)
            dc.out.write("urldate".ljust(FIELD_WIDTH) + "= {" + t + \
                         "},\n")
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_author     = author_string                                 #
        dc.s_lastaccess = t                                             #
    dc.authorexists = False

    if dc.debugging:
        print("+++ <CTANOut:leading")

# ------------------------------------------------------------------
def licenseT(k:xml.etree.ElementTree.Element, dc=dc_var):               # function licenseT
    """
    Processes the 'license' elements.

    Fetches the embedded attibutes type, date.
    Rewrites the variables dc.notice, dc.license_str, dc.s_license,
    dc.usedLicenses, dc.licenses.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var
    
    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice        string for RIS|BibLaTeX: collection for N1 a/o note
    dc.license_str   string: collect license
    dc.s_license     string for Excel: license
    dc.usedLicenses  Python dictionary:  collect used dc.licenses for all packages
    dc.licenses      dictionary: lice nses[key]=(description, status)
    dc.debugging     flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:licenseT")

    typeT     = k.get("type", EMPTY)                                    # get attribute type; get a license key
    tmp       = typeT

    if tmp in dc.licenses:
        tmpname   = dc.licenses[tmp][0]                                 # name of license
        tmpstatus = dc.licenses[tmp][1]                                 # status of license: free|not free
    else:
        tmpname   = typeT                                               # correction, if licenced key is unknown
        tmpstatus = "(unclear)"
        dc.licenses[tmp] = (tmpname, tmpstatus)

    if tmpstatus == "true":
        tmpstatus = "(free)"
    elif tmpstatus =="false":
        tmpstatus = "(not free)"
    else:
        pass

    if tmp in dc.licenses:                                              # look in dictionary
        tmp2 = f"{tmp} = {tmpname} {tmpstatus}"

    if not typeT in dc.usedLicenses:                                    # collects licenses in usedLicenses
        dc.usedLicenses[typeT] = 1
    else:
        dc.usedLicenses[typeT] = dc.usedLicenses[typeT] + 1

    if dc.license_str != EMPTY:                                         # for BibLaTeX
        dc.license_str += f"; {tmp}{BLANK}{tmpstatus}"                  # accumulate license string
    else:
        dc.license_str = f"{tmp}{BLANK}{tmpstatus}"

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(f"\\item[license] {tmp2}\n")
        dc.out.write(f"\\index{{License!{tmp}}}\n")
        dc.out.write(f"\\index{{License!{tmpname}}}\n")
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}License:" +\
                      f" {tmp2}"                                        # accumulate notice string
        else:
            dc.notice = f"License: {tmp2}"
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        pass
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "license: ".ljust(LABEL_WIDTH) + tmp2)
    elif dc.mode in ["Excel"]:                                          # Excel
        if dc.s_license != EMPTY:                                       # accumulate dc.s_license string
            dc.s_license += f"; {tmp2}"
        else:
            dc.s_license = tmp2

    if dc.debugging:
        print("+++ <CTANOut:licenseT")

# ------------------------------------------------------------------
def load_pickle1(dc=dc_var):                                            # function load_pickle1
    """
    Gets the structures dc.authors, dc.packages, dc.topics,
    dc.topicspackages, dc.authorpackages, dc.licensepackages
    (generated by CTANLoad.py).

    Rewrites the variables dc.authors, dc.packages, dc.topics,
    dc.licenses, dc.topicspackages, dc.packagetopics, dc.authorpackages,
    dc.licensepackages, dc.yearpackages.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.authors           python dictionary: each element: <author key>:<tuple with givenname and familyname
    dc.packages          python dictionary: each element: <package key>:<tuple with package name and packages
    dc.topics            python dictionary: each element: <topics name>:<topics title>
    dc.licenses          python dictionary: each element: <license key>:<license title>
    dc.topicspackages    python dictionary: each element: <topic key>:<list of package names>
    dc.packagetopics     python dictionary: each element: <topic key>:<list with package names>   
    dc.authorpackages    python dictionary: each element: <author key>:<list with package names>
    dc.licensepackages   Python dictionary (mostly sorted): each element: <license key>:<list with package names>
    dc.yearpackages      python dictionary: each element: <year>: <list of package names> 
    dc.debugging         flag: debugging

    Possible message:
    ----------------
    + Error: pickle file '{PICKLE_NAME1}' not found
    + Warning: Any unspecified error
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.2    2026-07-09 try ... except enhanced; new error message
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.7    2026-07-13 backtracing
    # 3.7.2  2026-07-13 traceback.print_exc()


    if dc.debugging:
        print("+++ >CTANOut:load_pickle1")

    # authors: Python dictionary (sorted)
    #   each element: <author key>:<tuple with givenname and familyname>
    # packages: Python dictionary (sorted)
    #   each element: <package key>:<tuple with package name and
    #                 package title>
    # topics: Python dictionary (sorted)
    #   each element: <topics name>:<topics title>
    # licenses: Python dictionary (sorted)
    #   each element: <license key>:<license title>
    # topicspackages: Python dictionary (unsorted)
    #   each element: <topic key>:<list with package names>
    # packagetopics: Python dictionary (sorted)
    #   each element: <topic key>:<list with package names>
    # authorpackages: Python dictionary (unsorted)
    #   each element: <author key>:<list with package names>
    # licensepackages: Python dictionary (mostly sorted)
    #   each element: <license key>:<list with package names>
    # yearpackages: Python dictionary
    #   each element: <year>:<list with package names>

    try:                                                                # try to open 1st pickle file
        pickleFile1 = open(dc.direc + PICKLE_NAME1, "br")
        (dc.authors, dc.packages, dc.topics, dc.licenses, dc.topicspackages, \
        dc.packagetopics, dc.authorpackages, dc.licensepackages, dc.yearpackages) =\
        pickle.load(pickleFile1)
        pickleFile1.close()                                             # close file
    except FileNotFoundError:                                           # unable to open pickle file
        print(f"--- Error: pickle file '{PICKLE_NAME1}' not found")
        sys.exit("[CTANOut] Error: program is terminated")
    except Exception as err:
        print("[CTANOut] Warning: Any unspecified error:",
              "load_pickle1,", err, traceback.print_exc())

    if dc.debugging:
        print("+++ <CTANOut:load_pickle1")

# ------------------------------------------------------------------
def load_pickle2(dc=dc_var):                                            # function load_pickle2
    """
    Gets dc.XML_toc (generated by CTANLoad.py).

    Rewrites the the dictionary dc.XML_toc.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.XML_toc    python dictionary:  list of XML and PDF files:
                  dc.XML_toc[CTAN address]= (XML file, key,
                  plain PDF file name)
    dc.debugging  flag: debugging

    Possible message:
    ----------------
    + Warning: pickle file '{PICKLE_NAME2}' not found; local
               information files ignored
    + Warning: Any unspecified error
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 3.2    2026-07-09 try ... except enhanced; new error message
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.7    2026-07-13 backtracing
    # 3.7.2  2026-07-13 traceback.print_exc()


    if dc.debugging:
        print("+++ >CTANOut:load_pickle2")

    try:                                                                # try to open second pickle file
        pickleFile2 = open(dc.direc + PICKLE_NAME2, "br")
        dc.XML_toc     = pickle.load(pickleFile2)
        pickleFile2.close()                                             # close file
    except FileNotFoundError:                                           # unable to open pickle file
        dc.list_info_files = False
        print(f"--- Warning: pickle file '{PICKLE_NAME2}' not found;",
              "local information files ignored")
    except Exception as err:
        print("[CTANOut] Warning: Any unspecified error: ",
              "load_pickle2,", err, traceback.print_exc())

    if dc.debugging:
        print("+++ <CTANOut:load_pickle2")

# ------------------------------------------------------------------
def main(dc=dc_var):                                                    # function main
    """
    Main function (calls the other functions)

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose
    
    Calls:
    -----
    + argparse_postprocess
    + argparse_process
    + biblatex_citationkey
    + first_lines
    + load_pickle1
    + load_pickle2
    + make_lic
    + make_stat
    + make_statistics
    + make_tap
    + make_tlp
    + make_tops
    + make_xref
    + process_packages

    Possible messages:
    -----------------
    + Warning: no file '{tmp_f}' created
    + Info: CTANOut program successfully completed.
    """

    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 2.69   2025-03-24 time specification with unit
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.4    2026-07-10 handling of LaTeX source code texts improved
    # 3.4.3  2026-07-10 call the new functions
    # 3.5    2026-07-13 new function: argparse_process
    # 3.5.2  2026-07-13 call argparse_process
    # 3.6    2026-07-13 new function: argparse_postprocess
    # 3.6.2  2026-07-13 calls argparse_postprocess

    if dc.debugging:
        print("+++ >CTANOut:main")

    starttotal   = time.time()                                          # set begin of total time
    startprocess = time.process_time()                                  # set begin of process time

    argparse_process()                                                  # defines program arguments and starts
    argparse_postprocess()                                              # postprocesses arguments
    if not dc.no_files:
        dc.out = open(dc.direc + dc.out_file_ext,
                   encoding=FILE_ENCODING, mode="w")                    # open output file
    load_pickle1()                                                      # load pickle file 1
    load_pickle2()                                                      # load pickle file 21
    if dc.mode == "BibLaTeX":
        biblatex_citationkey()                                          # generate BibLaTeX citation keys

    first_lines()                                                       # first lines of output
    process_packages()                                                  # process all packages

    # ------------------------------------------------------------------
    # Generate topic list, topics and their packages (cross-reference),
    # finish
    #
    if dc.mode in ["LaTeX"] and dc.make_topics:
        if not dc.no_package_processed:
            if not dc.no_files:
                make_tops()                                             # Topic list
        else:
            if dc.verbose:
                tmp_f = dc.direc + dc.out_file + ".top"
                print(f"--- Warning: no file '{tmp_f}' created")

        if not dc.no_package_processed:
            if not dc.no_files:
                make_xref()                                             # Topics|Packages cross-reference
        else:
            if dc.verbose:
                tmp_f = dc.direc + dc.out_file + ".xref"
                print(f"--- Warning: no file '{tmp_f}' created")

        if not dc.no_package_processed:
            if not dc.no_files:
                make_tap()                                              # Authors|Packages cross-reference
        else:
            if dc.verbose:
                tmp_f = dc.direc + dc.out_file + ".tap"
                print(f"--- Warning: no file '{tmp_f}' created")

        if not dc.no_package_processed:
            if not dc.no_files:
                make_lics()                                             # License list cross-reference
        else:
            if dc.verbose:
                tmp_f = dc.direc + dc.out_file + ".lic"
                print(f"--- Warning: no file '{tmp_f}' created")

        if not dc.no_package_processed:
            if not dc.no_files:
                make_tlp()                                              # Licenses|Packages cross-reference
        else:
            if dc.verbose:
                tmp_f = dc.direc + dc.out_file + ".tlp"
                print(f"--- Warning: no file '{tmp_f}' created")
        if not dc.no_files:
            make_stat()                                                 # Statistics file (xyz.stat)

    # ------------------------------------------------------------------
    # The end
    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        trailer = make_trailer()                                        # (**)
        dc.out.write(trailer)                                           # output trailer
        dc.out.close()                                                  # close output file
    if dc.verbose:
        print("[CTANOut] Info: CTANOut program successfully completed.")

    # ------------------------------------------------------------------
    # Statistics on terminal
    #
    
    if dc.statistics:                                                   # flag -stat is set
        PP = 6
        make_statistics()                                               # output statistics on terminal

        endtotal   = time.time()
        endprocess = time.process_time()
        print("--")
        print("total time (CTANOut): ".ljust(LEFT + 1),
              str(round(endtotal-starttotal, 2)).rjust(PP), "s")
        print("process time (CTANOut): ".ljust(LEFT + 1),
              str(round(endprocess-startprocess, 2)).rjust(PP), "s")

    if dc.debugging:
        print("+++ <CTANOut:main")

# ------------------------------------------------------------------
def make_stat(dc=dc_var):                                               # function make_stat
    """
    Generates statistics in the stat file (xyz.stat).

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose
    
    Possible message:
    ----------------
    + Info: file '{tmp_d}' written:[dc.statistics]
    """

    # 2.59   2024-03-26 in make_stat, make_tap, make_tlp, make_tops,
    #                   make_lics, make_xref: Small additions to the
    #                   output texts
    # 2.61   2024-04-12 smaller changes in make_statistics
    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 2.71   2025-11-05 footnote text in make_stat corrected
    # 2.74   2025-12-03 reference to LaTeX in the files xyz.top,
    #                    xyz.xref, xyz.tap, xyz.lic, xyz.tlp, xyz.stat
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:make_stat")

    # write statistics in the stat (.stat) file

    text1:str = EMPTY
    text2:str = EMPTY
    text3:str = EMPTY
    text4:str = EMPTY
    text5:str = EMPTY
    text6:str = EMPTY

    stat = open(dc.direc + dc.out_file + ".stat", encoding=FILE_ENCODING,
                mode="w")
    stat.write(f"% file: '{dc.out_file}.stat' (in LaTeX format)\n")
    stat.write(f"% date: {ACT_DATE}\n")
    stat.write(f"% time: {ACT_TIME}\n")
    stat.write(f"% is called by '{dc.out_file}.tex'\n\n")

    stat.write(r"\minisec{Parameters and statistics}" + "\n\n")
    stat.write(r"\raggedright" + "\n")
    stat.write(r"\begin{tabular}{lll}" + "\n")

    stat.write("\n")
    stat.write("program name "  + r"& \verb§" + \
               str(PROGRAM_NAME) + r"§\\" + "\n")
    stat.write("program version " + r"&" + PROGRAM_VERSION + " (" + \
               PROGRAM_DATE + r")\\"  "\n")
    stat.write("program author " + r"&" + PROGRAM_AUTHOR + r"\\\\"  "\n")
    stat.write("program date " + r"&" + PROGRAM_DATE + r"\\\\"  "\n\n")

    stat.write("date of program execution " + r"&" + \
               ACT_DATE + r"\\"  "\n")                                  # date of program execution
    stat.write("time of program execution " + r"&" + ACT_TIME + \
               r"\\\\"  "\n")                                           # time of program execution

    stat.write("mode " + r"& \verb§" + dc.mode + r"§\\" + "\n")
    stat.write("special lists used\\footnotemark{} " + r"&" + \
               str(dc.make_topics) + r"\\" + "\n")                      # special lists used

    if dc.skip == SKIP_DEFAULT:
        text3 = "(no fields skipped = default)"
    stat.write("skipped CTAN fields " + r"& \verb§" + \
               dc.skip + r"§  " + text3 + r"\\" + "\n\n")               # skipped CTAN fields

    if dc.name_template == NAME_DEFAULT:                                # name template is not specified
        text1 = "(all packages = default)"
    stat.write("template for package names " + r"& " + \
               TeX_fold(dc.name_template) + BLANK + text1 + r"\\" +\
               "\n")

    if dc.key_template == KEY_TEMPLATE_DEFAULT:                         # key template is not specified
        text2 = "(all topics = default)"
    stat.write("template for topics " + r"& " + \
               TeX_fold(dc.key_template) + r"  " + text2 + r"\\" + "\n")

    if dc.author_template == AUTHOR_TEMPLATE_DEFAULT:                   # author template is not specified
        text4 = "(all authors = default)"
    stat.write("template for author names " + r"& " + \
               TeX_fold(dc.author_template) + r"  " + text4 + r"\\" + \
               "\n")

    if dc.license_template == LICENSE_TEMPLATE_DEFAULT:                 # license template is not specified
        text5 = "(all licenses = default)"
    stat.write("template for licenses " + r"& " + \
               TeX_fold(dc.license_template) + r"  " + text5 + r"\\" +\
               "\n")

    if dc.year_template == YEAR_TEMPLATE_DEFAULT:                       # year template is not specified
        text6 = "(all years = default)"
    stat.write("template for years " + r"& " + \
               TeX_fold(dc.year_template) + r"  " + text6 + \
               r"\\\\"+"\n\n")

    stat.write("number of authors, total on CTAN " + r"&" + \
               str(len(dc.authors)).rjust(6) + r"\\" + "\n")            # number of authors, total on CTAN
    stat.write("number of authors, cited here " + r"&" + \
               str(len(dc.usedAuthors)).rjust(6)  + r"\\" + "\n")       # number of authors, cited here
    stat.write("number of packages, total on CTAN " + r"&" + \
               str(len(dc.packages)).rjust(6)  + r"\\" + "\n")          # number of packages, total on CTAN
    stat.write("number of packages, processed locally " + r"&" + \
               str(len(dc.usedPackages)).rjust(6)  + r"\\" + "\n")      # number of packages, processed locally

    stat.write("number of topics, total on CTAN " + r"&" + \
               str(len(dc.topics)).rjust(6)  + r"\\" + "\n")            # number of topics, total on CTAN
    stat.write("number of topics, used here " + r"&" + \
               str(len(dc.usedTopics)).rjust(6)  + r"\\" + "\n")        # number of topics, used here

    stat.write("number of licenses, total on CTAN " + r"&" + \
               str(len(dc.licenses)).rjust(6)  + r"\\" + "\n")          # number of licenses, total on CTAN
    stat.write("number of licenses, used here " + r"&" + \
               str(len(dc.usedLicenses)).rjust(6)  + r"\\" + "\n")      # number of licenses, used here
    stat.write(r"\end{tabular}" + "\n")
    stat.write(	"""\\footnotetext{special lists: topics|licenses and
              their explanations -- topics|authors|licenses and related
              dc.packages(cross-reference lists)}\n""")
    stat.close()                                                        # close statistics file
    if dc.verbose:
        tmp_d = dc.direc + dc.out_file + ".stat"
        print(f"--- Info: file '{tmp_d}' written: [statistics]")

    if dc.debugging:
        print("+++ <CTANOut:make_stat")

# ------------------------------------------------------------------
def make_statistics(dc=dc_var):                                         # function make_statistics
    """
    Generates statistics (on terminal).

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.12   2026-08-20 Name and size of the results PDF file

    if dc.debugging:
        print("+++ >CTANOut:make_statistics")

    L = LEFT + 3
    R = 6

    # Statistics on terminal
    print("\nStatistics:")
    print("date | time:".ljust(L + 1), ACT_DATE, "|", ACT_TIME)
    print("program | version | date:".ljust(L + 1), PROGRAM_NAME, "|",
          PROGRAM_VERSION, "|", PROGRAM_DATE)
    if not dc.no_files:                                                 # there is a output file
        print("target format:".ljust(L + 1), dc.mode)
        print("name of the resulting output file:".ljust(L + 1),
              dc.direc + dc.out_file_ext)                               # name of output file
        tmp = path.getsize(dc.direc + dc.out_file_ext)
        print("size of the output file (in bytes):".ljust(L + 1),
               f"{tmp}\n")                                              # size of output file
    else:
        print(BLANK)
    print("number of authors, total on CTAN:".ljust(L),
          str(len(dc.authors)).rjust(R))
    print("number of authors, cited here:".ljust(L),
          str(len(dc.usedAuthors)).rjust(R))
    print("number of packages, total on CTAN:".ljust(L),
          str(len(dc.packages)).rjust(R))
    print("number of packages, processed locally:".ljust(L),
          str(len(dc.usedPackages)).rjust(R))
    print("number of topics, total on CTAN:".ljust(L),
          str(len(dc.topics)).rjust(R))
    print("number of topics, used here:".ljust(L),
          str(len(dc.usedTopics)).rjust(R))
    print("number of licenses, total on CTAN:".ljust(L),
          str(len(dc.licenses)).rjust(R))
    print("number of licenses, used here:".ljust(L),
          str(len(dc.usedLicenses)).rjust(R))
    print(EMPTY)
    if dc.name_template != NAME_TEMPLATE_DEFAULT:                       # name template is specified
        print("no. of packages (based on names):".ljust(L),
              str(dc.no_np).rjust(R))
    if dc.key_template != KEY_TEMPLATE_DEFAULT:                         # key template is specified
        print("no. of packages (based on keys):".ljust(L),
              str(dc.no_tp).rjust(R))
    if dc.license_template != LICENSE_TEMPLATE_DEFAULT:                 # license template is specified
        print("no. of packages (based on licenses):".ljust(L),
              str(dc.no_lp).rjust(R))
    if dc.author_template != AUTHOR_TEMPLATE_DEFAULT:                   # author template is specified
        print("no. of packages (based on authors):".ljust(L),
              str(dc.no_ap).rjust(R))
    if dc.year_template != YEAR_TEMPLATE_DEFAULT:                       # year template is specified
        print("no. of packages (based on years):".ljust(L),
              str(dc.no_ly).rjust(R))

    if dc.debugging:
        print("+++ <CTANOut:make_statistics")

# ------------------------------------------------------------------
def make_tap(dc=dc_var):                                                # function make_tap
    """
    Generates the tap (xyz.tap) file (Authors|Packages cross-reference).
    
    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose
    
    Possible message:
    ----------------
    + Info: file '{dc.direc + dc.out_file}.tap' created: [list with
            dc.authors and related packages (cross-reference list)]"
    """

    # 2.57   2024-02-28 Change in make_tap: enable processing of "_" in
    #                   author names
    # 2.59   2024-03-26 in make_stat, make_tap, make_tlp, make_tops,
    #                   make_lics, make_xref: Small additions to the
    #                   output texts
    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 2.74   2025-12-03 reference to LaTeX in the files xyz.top,
    #                   xyz.xref, xyz.tap, xyz.lic, xyz.tlp, xyz.stat
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:make_tap")

    # Authors|Packages cross-reference

    tap = open(dc.direc + dc.out_file + ".tap", encoding=FILE_ENCODING,
               mode="w")
    tap.write(f"% file: '{dc.out_file}.tap' (in LaTeX format)\n")
    tap.write(f"% date: {ACT_DATE}\n")
    tap.write(f"% time: {ACT_TIME}\n")
    tap.write(f"% is called by '{dc.out_file}.tex'\n\n")
    tap.write(r"\section{Authors and associated packages}" + "\n\n")
    tap.write("""\\textit{Note: The numbers do not refer to page
              numbers, but to section numbers. A click on this number
              leads to the corresponding package description.}\n\n""")
    tap.write(r"\raggedright" + "\n")
    tap.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxxxx}" + "\n")

    tap.write("\n")
    for f in dc.authors:                                                # all authors
        if f in dc.usedAuthors:                                         # all used authors
            if dc.authors[f][1] != EMPTY:
                tmp2 = dc.authors[f][1] + ", " + dc.authors[f][0]
            else:
                tmp2 = dc.authors[f][0]
            tmp2 = TeXchars(tmp2)
            tap.write(f"\\item[{tmp2}] ")
            tmp1 = dc.authorpackages[f]
            package_no = 0
            for ff in tmp1:
                if ff in dc.usedPackages:
                    package_no += 1
            if package_no == 1:
                text1 = " package: "
            else:
                text1 = " packages: "
            tap.write(str(package_no) + text1)
            for ff in tmp1:
                if ff in dc.usedPackages:
                    ff = re.sub("_", "-", ff)
                    tap.write(f"\\texttt{{{ff}}}~(\\ref{{pkg:{ff}}}); ")
            tap.write("\n")
    tap.write(r"\end{labeling}" + "\n")
    tap.close()                                                         # close file
    if dc.verbose:
        print(f"--- Info: file '{dc.direc + dc.out_file}.tap' " +\
              "created: [list with dc.authors and related packages " +\
              "(cross-reference list)]")

    if dc.debugging:
        print("+++ <CTANOut:make_tap")

# ------------------------------------------------------------------
def make_tlp(dc=dc_var):                                                # function make_tlp
    """
    Generates the (xyz.tlp) file (Licenses|Packages cross-reference).
    
    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose
    
    Possible message:
    ----------------
    + Info: file '{dc.direc + dc.out_file}.tlp' created: [list with
            licenses and related packages (cross-reference list)]
    """

    # 2.59   2024-03-26 in make_stat, make_tap, make_tlp, make_tops,
    #                   make_lics, make_xref: Small additions to the
    #                   output texts
    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 2.74   2025-12-03 reference to LaTeX in the files xyz.top,
    #                   xyz.xref, xyz.tap, xyz.lic, xyz.tlp, xyz.stat
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:make_tlp")

    # Authors|Packages cross-reference

    tlp = open(dc.direc + dc.out_file + ".tlp",
               encoding=FILE_ENCODING, mode="w")
    tlp.write(f"% file: '{dc.out_file}.tlp' (in LaTeX format)\n")
    tlp.write(f"% date: {ACT_DATE}\n")
    tlp.write(f"% time: {ACT_TIME}\n")
    tlp.write(f"% is called by '{dc.out_file}.tex'\n\n")
    tlp.write(r"\section{Licenses and associated packages}" + "\n\n")
    tlp.write("""\\textit{Note: The numbers do not refer to page
              numbers, but to section numbers. A click on this number
              leads to the corresponding package description.}\n\n""")
    tlp.write(r"\raggedright" + "\n")

    tlp.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxxxx}" + "\n")
    for f in dc.licenses:                                               # loop: all licenses
        if f in dc.usedLicenses:                                        # license is used?
            tlp.write("\\item[\\texttt{" + f + "}]")
            tmp1 = dc.licensepackages[f]                                # get the packages for this license
            package_no = 0

            for ff in tmp1:
                if ff in dc.usedPackages:
                    package_no += 1
            if package_no == 1:
                text1 = " package: "
            else:
                text1 = " packages: "
            tlp.write(str(package_no) + text1)

            for ff in tmp1:                                             # loop: all packages with this license name
                if ff in dc.usedPackages:
                    ff = re.sub("_", "-", ff)
                    tlp.write(f"\\texttt{{{ff}}}~(\\ref{{pkg:{ff}}}); ")
            tlp.write("\n")
    tlp.write(r"\end{labeling}" + "\n")

    tlp.close()                                                         # close file
    if dc.verbose:
        print(f"--- Info: file '{dc.direc + dc.out_file}.tlp' created:"+\
              " [list with licenses and related packages " +\
              "(cross-reference list)]")

    if dc.debugging:
        print("+++ <CTANOut:make_tlp")

# ------------------------------------------------------------------
def make_tops(dc=dc_var):                                               # function make_tops
    """
    Generates the tops (xyz.top) file.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose
    
    Possible message:
    ----------------
    + Info: file '{dc.direc + dc.out_file}.top' created: [topics and
            their explainations]
    """

    # 2.59   2024-03-26 in make_stat, make_tap, make_tlp, make_tops, 
    #                   make_lics,, make_xref: Small additions to the
    #                   output texts
    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 2.74   2025-12-03 reference to LaTeX in the files xyz.top,
    #                   xyz.xref, xyz.tap, xyz.lic, xyz.tlp, xyz.stat
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:make_tops")

    # Topic list
    tops = open(dc.direc + dc.out_file + ".top",
                encoding=FILE_ENCODING, mode="w")

    tops.write(f"% file: {dc.out_file}.top (in LaTeX format)\n")
    tops.write(f"% date: {ACT_DATE}\n")
    tops.write(f"% time: {ACT_TIME}\n")
    tops.write(f"% is called by {dc.out_file}.tex\n\n")

    tops.write(r"\section{Used topics, short explainations}" + "\n\n")
    tops.write(r"\raggedright" + "\n")
    tops.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxxxx}" + "\n")

    for f in dc.topics:                                                 # all topics
        if f in dc.usedTopics:                                          #  all used topics
            tmp = dc.topics[f]
            tmp = re.sub(r"\\", r"\\textbackslash ", tmp)
            tops.write(f"\\item[\\texttt{{{f}}}] {tmp}\n")
    tops.write(r"\end{labeling}" + "\n")
    tops.close()                                                        # close file
    if dc.verbose:
        print(f"--- Info: file '{dc.direc + dc.out_file}.top' created:"+\
              " [topics and their explainations]")

    if dc.debugging:
        print("+++ <CTANOut:make_tops")

# ------------------------------------------------------------------
def make_lics(dc=dc_var):                                               # function make_lics
    """
    Generates the tops (xyz.lic) file (License list).

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose
    
    Possible message:
    ----------------
    + Info: file '{dc.direc + dc.out_file}.lic' created: [licenses and
            their explainations]
    """

    # 2.59    2024-03-26 in make_stat, make_tap, make_tlp, make_tops, 
    #                    make_lics,, make_xref: Small additions to the
    #                    output texts
    # 2.65    2025-02-06 wherever appropriate: string interpolation with
    #                    f-strings instead of .format
    # 2.74    2025-12-03 reference to LaTeX in the files xyz.top,
    #                    xyz.xref, xyz.tap, xyz.lic, xyz.tlp, xyz.stat
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:make_lics")

    # License list
    lics = open(dc.direc + dc.out_file + ".lic", encoding=FILE_ENCODING,
                mode="w")

    lics.write(f"% file: {dc.out_file}.lic (in LaTeX format)\n")
    lics.write(f"% date: {ACT_DATE}\n")
    lics.write(f"% time: {ACT_TIME}\n")
    lics.write(f"% is called by {dc.out_file}.tex\n\n")

    lics.write(r"\section{Used licenses, short explainations}" + "\n\n")
    lics.write(r"\raggedright" + "\n")
    lics.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxxxx}" + "\n")

    for f in dc.licenses:                                               # all topics
        if f in dc.usedLicenses:                                        #  all used topics
            tmp  = dc.licenses[f][0]
            tmp2 = dc.licenses[f][1]
            if tmp2 == "true":
                tmp3 = "free"
            else:
                tmp3 = "not free"
            lics.write(f"\\item[\\texttt{{{f}}}] {tmp} ({tmp3})\n")
    lics.write(r"\end{labeling}" + "\n")
    lics.close()                                                        # close file
    if dc.verbose:
        print(f"--- Info: file '{dc.direc + dc.out_file}.lic' created:"+\
              " [licenses and their explainations]")

    if dc.debugging:
        print("+++ <CTANOut:make_lics")

# ------------------------------------------------------------------
def make_xref(dc=dc_var):                                               # function make_xref
    """
    Generates the xref (xyz.xref) file.
    (Topics|Packages cross-reference)

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose
    
    Possible merssage:
    -----------------
    + Info: file '{dc.direc + dc.out_file}.xref' created: [list with
            topics and  related packages (cross-reference list)]
    """

    # 2.59   2024-03-26 in make_stat, make_tap, make_tlp, make_tops, 
    #                   make_lics,, make_xref: Small additions to the
    #                   output texts
    # 2.65   2025-02-06 wherever appropriate: string interpolation with
    #                   f-strings instead of .format
    # 2.74   2025-12-03 reference to LaTeX in the files xyz.top,
    #                   xyz.xref, xyz.tap, xyz.lic, xyz.tlp, xyz.stat
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:make_xref")

    # Topics|Packages cross-reference
    xref = open(dc.direc + dc.out_file + ".xref", encoding=FILE_ENCODING,
                mode="w")

    xref.write(f"% file: {dc.out_file}.xref (in LaTeX format)\n")
    xref.write(f"% date: {ACT_DATE}\n")
    xref.write(f"% time: {ACT_TIME}\n")
    xref.write(f"% is called by '{dc.out_file}.tex'\n\n")
    xref.write(r"\section{Used topics and related packages}" + "\n\n")
    xref.write("""\\textit{Note: The numbers do not refer to
              page numbers, but to  section numbers. A click on this
              number leads to the corresponding package
              description.}\n\n""")
    xref.write(r"\raggedright" + "\n")
    xref.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxxxx}" + "\n")
    xref.write("\n")

    for f in dc.topics:                                                 # loop: all topics
        if f in dc.usedTopics:                                          # topic is used?
            xref.write("\\item[\\texttt{" + f + "}]")
            tmp1 = dc.topicspackages[f]                                 # get the packages for this topic
            package_nr = 0
            for ff in tmp1:                                             # loop: all packages with this topic
                if ff in dc.usedPackages:                               #    package is used?
                    package_nr += 1                                     #    count the packages
            if package_nr == 1:
                text1 = " package: "
            else:
                text1 = " packages: "
            xref.write(str(package_nr) + text1)
            for ff in tmp1:                                             # loop: all packages with this topic
                if ff in dc.usedPackages:                               #    package is used?
                    ff = re.sub("_", "-", ff)
                    xref.write(f"\\texttt{{{ff}}}~" +\
                               f"(\\ref{{pkg:{ff}}}); ")
            xref.write("\n")
    xref.write(r"\end{labeling}" + "\n")
    xref.close()                                                        # close file
    if dc.verbose:
        print(f"--- Info: file '{dc.direc + dc.out_file}.xref' " +\
              "created: [list with topics and .related packages " +\
              "(cross-reference list)]")

    if dc.debugging:
        print("+++ <CTANOut:make_xref")

# ------------------------------------------------------------------
def miktex(k:xml.etree.ElementTree.Element, dc=dc_var):                 # function miktex
    """
    Processes the 'miktex' element.

    Fetches the local attribute location.
    Rewrites the variables dc.notice, dc.s_miktex.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice     string for RIS|BibLaTeX: collection for N1 a/o note
    dc.s_miktex   string for Excel: miktex
    dc.debugging  flag: debugging

    Calls:
    -----
    + TeXchars

    Messages:
    --------
    There are no specific messages.
    """

    # 2.55    2024-02-18 Mik\TeX escaped to Mik\\TeX
    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:miktex")

    location = k.get("location", EMPTY)                                 # get attribute location

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        tmp = TeXchars(location)
        dc.out.write(f"\\item[on Mik\\TeX] \\texttt{{{tmp}}}\n")
    elif dc.mode in ["RIS"]:                                            # RIS{
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}on " +\
                      f"MikTeX: {location}"
        else:
            dc.notice = f"on MikTeX: {location}"
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        tmp    = TeXchars(location)
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (FIELD_WIDTH + 2)}on " +\
                         f"MikTeX: {tmp}"
        else:
            dc.notice = f"on MikTeX: {tmp}"
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "on MikTeX: ".ljust(LABEL_WIDTH) + location)
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_miktex = location

    if dc.debugging:
        print("+++ <CTANOut:miktex")

# ------------------------------------------------------------------
def name(k:xml.etree.ElementTree.Element, dc=dc_var):                   # function name
    """
    Processes the 'name' element.

    Fetches embedded text.
    Rewrites the variable dc.s_name.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.s_name     string for Excel: name
    dc.debugging  flag: debugging

    Calls:
    -----
    + TeXchars
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:name")

    if len(k.text) > 0:                                                 # get embedded text
        tmp = k.text
    else:                                                               # k.text is empty
        tmp = DEFAULT_TEXT                                              # default text

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        tmp = TeXchars(tmp)                                             # clean-up embedded text
        dc.out.write(f"\\item[name] \\texttt{{{tmp}}}\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "name: ".ljust(LABEL_WIDTH) + tmp)
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        dc.out.write(f"T1  - {tmp}\n")                                  # main title
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        tmp = TeXchars(tmp)                                             # clean-up embedded text
        if bibfield_test(tmp, "title"):                                 # title
            dc.out.write("title".ljust(FIELD_WIDTH) + "= {" + \
                         tmp + "},\n")
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_name = k.text                                              # embedded text

    if dc.debugging:
        print("+++ <CTANOut:name")

# ------------------------------------------------------------------
def onepackage(s:str, t:str, dc=dc_var):                                # function onepackage
    """
    Loads a package XML file and starts parsing.

    Rewrites the variable dc.counter.

    Parameters:
    ----------
    s: package name (str)
    t    str
         current package date
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.counter    counter for packages
    dc.debugging  flag: debugging
    dc.verbose    flag: output is verbose

    Calls:
    -----
    + TeXchars
    + bibfield_test

    Possible message:
    ----------------
    + Warning: XML file for package '{s}' not well-formed
    """

    # 2.65    2025-02-06 wherever appropriate: string interpolation with
    #                    f-strings instead of .format
    # 3.2     2026-07-09 try ... except enhanced; new error message
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:onepackage")

    LEFT  = 33
    LEFT2 = 2
    LEFT3 = 7
    LEFT4 = 15
    try:
        onePackage     = ET.parse(dc.direc + s + EXT)                   # parse XML file
    except exception as err:                                            # not successfull
        if dc.verbose:
            print(f"----- Warning: XML file for package '{s}' " +\
                  "not well-formed", err)
    if dc.verbose:
        if not dc.no_files:
            print("    " + str(dc.counter).ljust(LEFT2), "package:",
                  s.ljust(LEFT), "mode:", dc.mode.ljust(LEFT3), "file:",
                  dc.direc + dc.out_file_ext.ljust(LEFT4))
        else:
            print("    " + str(dc.counter).ljust(LEFT2), "package:",
                  s.ljust(LEFT))

    dc.counter     = dc.counter + 1                                     # increment counter
    onePackageRoot = onePackage.getroot()                               # get XML root
    entry(onePackageRoot, t, s)                                         # begin with entry element

    if dc.debugging:
        print("+++ <CTANOut:onepackage")

# ------------------------------------------------------------------
def process_packages(dc=dc_var):                                        # function process_packages
    """
    Global loop (over all selected packages)

    Rewrites the variables dc.no_package_processed, dc.no_tp, dc.no_ap,
    dc.no_np, no_lp, dc.no_ly.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.no_package_processed Flag: if there is no correct XML file
    dc.no_tp                number of packages selected per topics
    dc.no_ap                number of packages selected per author names
    dc.no_np                number of packages selected per names
    dc.no_lp                number of packages selected per licenses
    dc.no_ly                number of packages selected per years
    dc.debugging            flag: debugging
    dc.verbose              flag: output is verbose

    Calls:
    -----
    + onepackage
    + get_topic_packages
    + get_author_packages
    + get_name_packages
    + get_local_packages
    + get_license_packages
    + get_year_packages

     Possible messages:
    -----------------
    + Warning: XML file for package '{f}' not found
    + Warning: no correct local XML file for any specified package found
    + Info: packages processed
    + Warning: Any unspecified error
    """

    # 2.65    2025-02-06 wherever appropriate: string interpolation with
    #                    f-strings instead of .format
    # 3.2     2026-07-09 try ... except enhanced; new error message
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class
    # 3.7    2026-07-13 backtracing
    # 3.7.2  2026-07-13 traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANOut:process_packages")

    all_packages = set()                                                # initialize set
    for f in dc.packages:
        all_packages.add(f)                                             # construct a set object (packages have not the right format)

    tmp_tp = all_packages.copy()                                        # initialize tmp_tp
    tmp_ap = all_packages.copy()                                        # initialize tmp_ap
    tmp_np = all_packages.copy()                                        # initialize tmp_np
    tmp_lp = all_packages.copy()                                        # initialize tmp_lp
    tmp_ly = all_packages.copy()                                        # initialize tmp_ly

    if dc.key_template != KEY_TEMPLATE_DEFAULT:
        tmp_tp = get_topic_packages()                                   # get packages by topic
    if dc.author_template != AUTHOR_TEMPLATE_DEFAULT:
        tmp_ap = get_author_packages()                                  # get packages by author name
    if dc.name_template != NAME_TEMPLATE_DEFAULT:
        tmp_np = get_name_packages()                                    # get packages by package name
    if dc.license_template != LICENSE_TEMPLATE_DEFAULT:
        tmp_lp = get_license_packages()                                 # get packages by license name
    if dc.year_template != YEAR_TEMPLATE_DEFAULT:
        tmp_ly = get_year_packages()                                    # get packages by year

    tmp_pp = tmp_tp & tmp_ap & tmp_np & tmp_lp & tmp_ly & \
             get_local_packages(dc.direc)
    tmp_p  = sorted(tmp_pp)                                             # built an intersection

    for f in tmp_p:                                                     # all XML files in loop
        fext = f + EXT                                                  # XML file name (with extension)

        try:                                                            # try to open file
            ff       = open(dc.direc + fext, encoding=FILE_ENCODING,
                            mode="r")
            mod_time = time.strftime('%Y-%m-%d',
                                    time.gmtime(os.path.getmtime(fext)))
            onepackage(f, mod_time)                                     # process loaded XML file
            ff.close()                                                  # loaded XML file closed
        except FileNotFoundError:                                       # specified XML file not found
            if dc.verbose:
                print(f"----- Warning: XML file for package '{f}'",
                      "not found")
        except Exception as err:
            print("[CTANOut] Warning: Any unspecified error: ",
                  "process_packages,", err, traceback.print_exc() )

    dc.no_tp = len(tmp_tp)                                              # number of packages with dc.key_template
    dc.no_ap = len(tmp_ap)                                              # number of packages with dc.author_template
    dc.no_np = len(tmp_np)                                              # number of packages with dc.name_template
    dc.no_lp = len(tmp_lp)                                              # number of packages with dc.license_template
    dc.no_ly = len(tmp_ly)                                              # number of packages with dc.year_template

    if dc.counter <= 1:                                                 # no specified package found <=== error1
        if dc.verbose:
            print("----- Warning: no correct local XML file for any",
                  "specified package found")
        dc.no_package_processed = True

    if dc.verbose:
        print("--- Info: packages processed.")

    if dc.debugging:
        print("+++ <CTANOut:process_packages")

# ------------------------------------------------------------------
def texlive(k:xml.etree.ElementTree.Element, dc=dc_var):                # function texlive
    """
    Processes the 'texlive' element.

    Fetches the local attribute loacation.
    Rewrites the variables dc.notice, dc.s_texlive.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice      string for RIS|BibLaTeX: collection for N1 a/o note
    dc.s_texlive   string for Excel: texlive
    dc.debugging   flag: debugging

    Calls:
    -----
    + TeXchars

    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:texlive")

    location = k.get("location", EMPTY)                                 # get attribute location

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        tmp = TeXchars(location)
        dc.out.write(f"\\item[on \\TeX Live] \\texttt{{{tmp}}}\n")
    elif dc.mode in ["RIS"]:                                            # RIS
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}" +\
                      f"on TeXLive: {location}"
        else:
            dc.notice = f"on TeXLive: {location}"
    elif dc.mode in ["BibLaTeX"]:                                       # BibLaTeX
        tmp = TeXchars(location)
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (FIELD_WIDTH +2)}on " +\
                         f"TeXLive: {tmp}"
        else:
            dc.notice = f"on TeXLive: {tmp}"
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "on TeXLive: ".ljust(LABEL_WIDTH) + \
                     location)
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_texlive = location

    if dc.debugging:
        print("+++ <CTANOut:texlive")

# ------------------------------------------------------------------
def trailing(k:xml.etree.ElementTree.Element, t:str, p:str, dc=dc_var): # function trailing
    """
    Completes the actual package.

    Inspects the element 'keyval'.
    Rewrites many variables.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    t    str
         current package date
         no default
    p    str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice              string for RIS|BibLaTeX: collection for
                           N1 a/o note
    dc.info_files          list of local PDF files
    dc.language_set        set: collect language
    dc.year_str            string: collect all year items for a package
    dc.version_str         string: collect all version items for a
                           package
    dc.date_str            string: collect date
    dc.also_str            string: collect also
    dc.license_str         string: collect license
    dc.copyright_str       string: collect copyright
    dc.description_str     string: collect description
    dc.authorexists        flag; True, if an author exists
    dc.contact_str         string: collect contact
    dc.debugging           flag: debugging

    Calls:
    -----
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:trailing")

    kw:list = []                                                        # keywords

    dc.language_set.discard(EMPTY)
    if len(dc.language_set) > 1:
        dc.language_set.discard(NLS)
    lang      = sorted(list(dc.language_set))
    lang_str  = EMPTY                                                   # construct lang_str; used for Excel
    lang_str2 = EMPTY                                                   # used for RIS, BibLaTeX
    lang_str3 = EMPTY                                                   # used for LaTeX, plain
    for f in lang:
        if lang_str != EMPTY:
            lang_str = lang_str + "; " + f
        else:
            lang_str = f
        if lang_str2 != EMPTY:
           lang_str2 = lang_str2 + "; " + LANGUAGECODES[f]
        else:
            lang_str2 = LANGUAGECODES[f]
        if lang_str3 != EMPTY:
            lang_str3 = lang_str3 + "; " + f"{f}: {LANGUAGECODES[f]}"
        else:
            lang_str3 = f"{f}: {LANGUAGECODES[f]}"

    act_year = get_year(dc.year_str)                                    # calculate actual year (on the base of year_str and version_str)

    for child in k:                                                     # fetch and collect the package's keywords
        if child.tag == "keyval":                                       #   element keyval
            value = child.get("value", EMPTY)                           #   get attribute value
            if kw == []:
                kw.append(value)
            else:
                kw.append("; " + value)
    kw2 = EMPTY.join(kw)                                                # collect all keywords in one string

    if str(act_year) == YEAR_DEFAULT:
        if dc.mode in ["RIS", "BibLaTeX"]:
            act_year = EMPTY
        else:
            act_year = YEAR_DEFAULT2
    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(f"\\item[language(s)] {lang_str2}\n")
        for f in dc.language_set:
            tmp_l = LANGUAGECODES[f]
            tmp_t = "Language in description/documentation"
            dc.out.write(f"\\index{{{tmp_t}!{tmp_l}}}\n")
        if (str(act_year) != EMPTY) and (dc.date_str == EMPTY):         # year
            dc.out.write(f"\\item[year] {act_year}\n")
            dc.out.write("\\index{Year!" + str(act_year) + "}\n")
        dc.out.write(f"\\item[last access] {t}\n")                      # date of last access
        dc.out.write(r"\end{labeling}" + "\n")
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        if not dc.authorexists:
            dc.out.write(f"AU  - {AUTHOR_UNKNOWN}\n")
        dc.out.write("N1  - " + dc.notice.strip() + "\n")               # N1
        dc.out.write(f"LA  - {lang_str2}\n")
        if (str(act_year) != EMPTY) and (dc.date_str == EMPTY):
            dc.out.write(f"PY  - {act_year}\n")
        dc.out.write("ER  -\n\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        if (str(act_year) != EMPTY) and (dc.date_str == EMPTY):
            dc.out.write("\n" + "year: ".ljust(LABEL_WIDTH) + \
                         str(act_year))
        dc.out.write("\n" + "language(s): ".ljust(LABEL_WIDTH) + \
                     lang_str3)
        dc.out.write("\n" + "last access: ".ljust(LABEL_WIDTH) + t)
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        if bibfield_test(dc.description_str, "abstract"):               # abstract
            dc.out.write(dc.description_str)
            dc.out.write("},\n")

        if bibfield_test(str(act_year), "year") and \
           (dc.date_str == EMPTY):# year
            dc.out.write("year".ljust(FIELD_WIDTH) + "= {" + \
                      str(act_year) + "},\n")

        if bibfield_test(lang_str2, "language"):                        # language
            dc.out.write("language".ljust(FIELD_WIDTH) + "= {" + \
                      lang_str2 + "},\n")

        if bibfield_test(kw2, "keywords"):                              # keywords
            dc.out.write("keywords".ljust(FIELD_WIDTH) + "= {" + \
                      kw2 + "},\n")

        if bibfield_test(dc.copyright_str, "usera"):                    # usera
            dc.copyright_str = re.sub("@", "'at'", dc.copyright_str)
            dc.out.write("usera".ljust(FIELD_WIDTH) + "= {" + \
                      dc.copyright_str + "},\n")

        if bibfield_test(dc.license_str, "userb"):                      # userb
            dc.out.write("userb".ljust(FIELD_WIDTH) + "= {" + \
                      dc.license_str + "},\n")

        if bibfield_test(dc.contact_str, "userd"):                      # userd
            dc.out.write("userd".ljust(FIELD_WIDTH) + "= {" + \
                      dc.contact_str + "},\n")

        if bibfield_test(dc.also_str, "related"):                       # related
            dc.out.write("related".ljust(FIELD_WIDTH) + "= {" + \
                      dc.also_str + "},\n")

        if bibfield_test(dc.notice.strip(), "note"):                    # note
            dc.notice = re.sub("@", "'at'", dc.notice.strip())
            dc.out.write("note".ljust(FIELD_WIDTH) + "= {" + \
                      dc.notice.strip() + "},\n")

        if len(dc.info_files) > 0:
            tmp = EMPTY
            for f in dc.info_files:
                fx = os.path.abspath(f)
                fx = re.sub(r"\\", "/", fx)
                fx = re.sub(":", "\\:", fx)
                fx = ":" + fx + ":PDF"
                if tmp != EMPTY:
                    tmp += f"; {fx}"
                else:
                    tmp = fx
            if bibfield_test(tmp, "file"):                              # file
                dc.out.write("file".ljust(FIELD_WIDTH) + "= {" + \
                          tmp + "},\n")
        dc.out.write("}\n")
    elif dc.mode in ["Excel"] and not dc.no_files:                      # Excel
        dc.s_language = lang_str
        dc.s_keyval   = kw2
        dc.s_year     = str(act_year)
        dc.out.write(dc.s_id)
        for f in [dc.s_author, dc.s_name, dc.s_caption, dc.s_year,
                dc.s_lastchanges, dc.s_language, dc.s_lastaccess,
                dc.s_version, dc.s_keyval, dc.s_alias, dc.s_also,
                dc.s_contact, dc.s_copyright, dc.s_ctan,
                dc.s_documentation, dc.s_home, dc.s_install,
                dc.s_license, dc.s_miktex, dc.s_texlive]:
            dc.out.write("\t" + f)
        dc.out.write("\n")

    dc.notice          = EMPTY                                          # re-initialize notice
    dc.info_files      = []                                             # re-initialize info_files
    dc.language_set    = {NLS}                                          # re-initialize language_set
    year               = EMPTY                                          # re-initialize year
    dc.authorexists    = False                                          # re-initialize authorexists
    dc.year_str        = YEAR_DEFAULT                                   # re-initialize year_str
    dc.date_str        = EMPTY                                          # re-initialize date_str
    dc.also_str        = EMPTY                                          # re-initialize also_str
    dc.version_str     = DATE_DEFAULT                                   # re-initialize version_str
    dc.license_str     = EMPTY                                          # re-initialize license_str
    dc.copyright_str   = EMPTY                                          # re-initialize copyright_str
    dc.description_str = EMPTY                                          # re-initialize description_str
    dc.contact_str     = EMPTY                                          # re-initialize contact_str

    if dc.debugging:
        print("+++ <CTANOut:trailing")

# ------------------------------------------------------------------
def version(k:xml.etree.ElementTree.Element, p:str, dc=dc_var):         # function version
    """
    Processes the 'version' element.

    Fetches the embedded attribues number, date.
    Rewrites the variables dc.notice, dc.date_str, dc.version_str,
    dc.s_version, dc.s_lastchanges, dc.s_year.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    p    str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.notice          string for RIS|BibLaTeX: collection for
                       N1 a/o note
    dc.date_str        string: collect date
    dc.version_str     string: collect all version items for a package
    dc.s_version       string for Excel: version
    dc.s_lastchanges   string for Excel: last changes
    dc.s_year          string for Eccel: year
    dc.debugging       flag: debugging

    Calls:
    -----
    + bibfield_test

    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:version")

    number:str = k.get("number", EMPTY)                                 # get attribute number
    date:str   = k.get("date", EMPTY)                                   # get attribute date
    tmp:str    = number                                                 # version number

    if dc.mode in ["LaTeX", "BibLaTeX"] and not dc.no_files:            # for LaTeX|BibLaTeX correction
        tmp    = re.sub("_", r"\\_", tmp)                             

    if date != EMPTY:
        tmp = tmp + " (" + date + ")"                                   # version with date

    dc.version_str = dc.version_str + "|" + date                        # append date to version_str
    dc.date_str    = date
    year        = str(get_year(dc.date_str))

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        dc.out.write(f"\\item[version] {tmp}\n")
        if date != EMPTY:
            dc.out.write(f"\\item[last changes] {date}\n")
            if year != YEAR_DEFAULT:
                dc.out.write(f"\\item[year] {year}\n")
                dc.out.write("\\index{Year!" + year + "}\n")
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        if dc.notice != EMPTY:                                          # accumulate notice string
            dc.notice += f";\n{BLANK * (RIS_FIELDWIDTH + 1)}" +\
                         f"Version: {tmp}"
        else:
            dc.notice = f"Version: {tmp}"
        if date != EMPTY:
            dc.out.write(f"Y2  - {date}\n")
            if year != YEAR_DEFAULT:
                dc.out.write(f"PY  - {year}\n")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        dc.out.write("\n" + "version: ".ljust(LABEL_WIDTH) + \
                     tmp.strip())
        if date != EMPTY:
            dc.out.write("\n" + "last changes: ".ljust(LABEL_WIDTH) + \
                         date)
            if year != YEAR_DEFAULT:
                dc.out.write("\n" + "year:".ljust(LABEL_WIDTH) + year)
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        if bibfield_test(tmp.strip(), "version"):                       # version
            dc.out.write("version".ljust(FIELD_WIDTH) + "= {" + \
                      tmp.strip() + "},\n")
        if bibfield_test(date, "date"):                                 # date
            dc.out.write("date".ljust(FIELD_WIDTH) + "= {" + \
                         date + "},\n")
        if bibfield_test(year, "year") and (year != YEAR_DEFAULT):      # year
            dc.out.write("year".ljust(FIELD_WIDTH) + "= {" + \
                         year + "},\n")
    elif dc.mode in ["Excel"]:                                          # Excel
        dc.s_version = tmp.strip()
        if date != EMPTY:
            dc.s_lastchanges = date
            if year != YEAR_DEFAULT:
                dc.s_year = year

    if dc.debugging:
        print("+++ <CTANOut:version")


# ======================================================================
#  J. functions in the context of description

# 2.72    2025-11-21 in comment: List of TeX character conversions
# 2.73    2025-11-21 in comment: List of §§ constructions

# Conversions of TeX characters
# -----------------------------
# §§1	{	# restore {
# §§2	}	# restore }
# §§3	\	# restore \
# §§4	$	# restore $
# §§5	&	# restore &
# §§6	#	# restore #
# §§7	_	# restore _
# §§8	^	# restore ^
# §§9	%	# restore %
# §§0	~	# restore ~
# §§-	\n	# restore \n

# ------------------------------------------------------------------
def description(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):    # function description
    """
    Processes the 'description' elements.

    Fetches embedded text and the embbeded attribute language.
    Rewrites the variables dc.language_set, dc.description_str,
    dc.level.

    Parameters: 
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.language_set        set: collect language
    dc.description_str     string: collect description
    dc.level               string: level of itemize|enumerate
                           (<ol>, <ul>)
    dc.debugging           flag: debugging
    dc.verbose             flag: output is verbose

    Calls:
    -----
    + innertext
    + TeXchars_restore

    Possible message:
    ----------------
    + Warning: unknown language code '{language}' in 'description';
               ignored
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:description")

    language = k.get("language", NLS)                                   # get attribute language

    if language in LANGUAGECODES:                                       # convert language keys
        languagex = LANGUAGECODES[language]
        dc.language_set.add(language)                                   # collect languages uniqly
    else:
        languagex = EMPTY
        if language != EMPTY:
            if dc.verbose:
                tmp_d = "description"
                print("----- Warning: unknown language" + \
                      f" code '{language}' in '{description}'; ignored")

    dc.level = EMPTY                                                    # initialize variable

    tmptext = innertext(k, k.text, pp).strip()                          # get embedded text and sub-elements
    tmptext = re.sub("[ \t]+\n", "\n", tmptext)
    tmptext = TeXchars_restore(tmptext)                                 # restore changed characters
    tmptext = re.sub("[\n]+[ ]*[\n]+", "\n\n", tmptext)

    if dc.mode in ["LaTeX"] and not dc.no_files:                        # LaTeX
        if languagex != EMPTY:
            dc.out.write(f"\\item[description] ({languagex}) ")
        else:
            dc.out.write("\\item[description] ")
    elif dc.mode in ["RIS"] and not dc.no_files:                        # RIS
        if languagex != EMPTY:
            dc.out.write(f"AB  - ({languagex}) ")
        else:
            dc.out.write("AB  - ")
    elif dc.mode in ["plain"] and not dc.no_files:                      # plain
        if languagex != EMPTY:
            dc.out.write("\ndescription:".ljust(LABEL_WIDTH + 1) + \
                         "(" + languagex + ") ")
        else:
            dc.out.write("\ndescription:".ljust(LABEL_WIDTH + 1))
    elif dc.mode in ["BibLaTeX"] and not dc.no_files:                   # BibLaTeX
        if languagex != EMPTY:
            tmptext2 = "(" + languagex + ") "
        else:
            tmptext2 = EMPTY
        if not "abstract" in dc.skip_biblatex:
            if dc.description_str != EMPTY:
                dc.description_str += \
                    f"\n\n{BLANK * (FIELD_WIDTH + 2)}" +\
                    f"{tmptext2}{tmptext.strip()}"                      # accumulate description string
            else:
                dc.description_str = \
                    "abstract".ljust(FIELD_WIDTH)+ "= {"+\
                    tmptext2 + tmptext.strip()
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.mode in ["LaTeX", "RIS", "plain"] and not dc.no_files:
        if tmptext != EMPTY:
            dc.out.write(tmptext.strip() + "\n")

    if dc.debugging:
        print("+++ <CTANOut:description")

# ------------------------------------------------------------------
def innertext(k:xml.etree.ElementTree.Element, start:NoneType|str,
              pp:str, dc=dc_var) ->str:                                 # function innertext
    """
    Acts as an interface during the processing of
    <description>...</description>.

    It scans the body of description and calls recursively other
    functions.

    Rewrites the variable dc.level.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    start NoneType|str
          start of scanning
          no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    It returns a processed string.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.level      string: level of itemize|enumerate (<ol>, <ul>)
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:innertext")

    tmp = start

    if tmp is None:
        tmp = EMPTY

    for child in k:
        if child.tag == "em":                                           # sub-element em
            mod_em(child, pp)
        elif child.tag == "a":                                          # sub-element a
            mod_a(child, pp)
        elif child.tag == "i":                                          # sub-element i
            mod_i(child, pp)
        elif child.tag == "tt":                                         # sub-element tt
            mod_tt(child, pp)
        elif child.tag == "xref":                                       # sub-element xref
            mod_xref(child, pp)
        elif child.tag == "pre":                                        # sub-element pre
            mod_pre(child, pp)
        elif child.tag == "code":                                       # sub-element code
            mod_code(child, pp)
        elif child.tag == "b":                                          # sub-element b
            mod_b(child, pp)
        elif child.tag == "br":                                         # sub-element br
            mod_br(child, pp)
        elif child.tag == "small":                                      # sub-element small
            mod_small(child, pp)
        elif child.tag == "p":                                          # sub-element p
            dc.level = EMPTY
            mod_p(child, pp)
        elif child.tag == "ul":                                         # sub-element ul
            oldlevel = dc.level
            if oldlevel == EMPTY:
                dc.level = "ul"
            elif oldlevel == "ul-li":
                dc.level = "li-ul"
            else:
                dc.level = None
            mod_ul(child, pp)
            dc.level = oldlevel
        elif child.tag == "ol":                                         # sub-element ol
            oldlevel = dc.level
            if oldlevel == EMPTY:
                dc.level = "ol"
            elif oldlevel == "ol-li":
                dc.level = "li-ol"
            else:
                dc.level = None
            mod_ol(child, pp)
            dc.level = oldlevel
        elif child.tag == "li":                                         # sub-element li
            oldlevel = dc.level
            if oldlevel == "ul":
                dc.level = "ul-li"
            elif oldlevel == "ol":
                dc.level = "ol-li"
            elif oldlevel == "li-ul":
                dc.level = "ul-li2"
            elif oldlevel == "li-ol":
                dc.level = "ol-li2"
            else:
                dc.level = None
            mod_li(child, pp)
            dc.level = oldlevel
        elif child.tag == "dl":                                         # sub-element dl
            dc.level = EMPTY
            mod_dl(child, pp)
        elif child.tag == "dt":                                         # sub-element dt
            mod_dt(child, pp)
        elif child.tag == "dd":                                         # sub-element dd
            mod_dd(child, pp)

        if child.text != None:
            tmp = tmp + child.text.strip()
        if child.tail != None:
            tmp += child.tail.strip()
    return tmp

# ------------------------------------------------------------------
def mod_a(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):          # function mod_a
    """
    Processes the 'a' element.

    Fetches any embedded text and the local attribute 'href'.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_a")

    # mod_b --> innertext

    tmp = k.get("href", EMPTY)                                          # get attribute href
    p   = re.search("http", tmp)                                        # searches "http" in string

    if p == None:                                                       # build complete URL
        tmp2 = CTAN_URL + tmp
    else:
        tmp2 = tmp

    if k.text == None:                                                  # no embedded text
        k.text = tmp                                                    # get embedded text

    tmp3 = innertext(k, k.text, pp).strip()                             # get embedded text and sub-elements

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        tmp3   = re.sub("_", "-", tmp3)                                 # change embedded text
        k.text = f"§§=1§§3href§§1{tmp2}§§2§§1{tmp3}§§2§§=1"
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = f"§§=1{tmp3} ({tmp2})§§=1"                             # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excek do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_a")

# ------------------------------------------------------------------
def mod_b(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):          # function mod_b
    """
    Processes the 'b' element.

    Fetches any embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_b")

    # mod_b --> innertext

    tmp = innertext(k, k.text, pp).strip()                              # get embedded text and sub-elements

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        k.text = f"§§=1§§3textbf§§1{tmp}§§2§§=1"                        # change embedded text
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = f"§§=1'{tmp}'§§=1"                                     # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_b")

# ------------------------------------------------------------------
def mod_br(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_br
    """
    Processes the 'br' element.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_br")

    width = CASES[dc.mode]                                              # ??

    if dc.mode in ["LaTeX"]:                                            # LaTeX 
        k.text = "§§3§§3 "                                              # change embedded text
    elif dc.mode in ["BibLaTeX"]:                                       # RIS 
        k.text = "§§3§§3-"                                              # change embedded text
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = "§§-"                                                  # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_br")

# ------------------------------------------------------------------
def mod_code(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):       # function mod_code
    """
    Processes the 'code' element.

    Fetches any embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_code")

    # mod_pre --> mod_TeXchars2

    tmp   = k.text
    tmp   = mod_TeXchars2(tmp)
    tmp   = re.sub("\n[ ]+", "§§-", tmp)
    width = CASES[dc.mode]
    tmpbl = "§§=" + str(width)


    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        if ("\n" in tmp.strip()) or ("§§-" in tmp.strip()):
            k.text = "§§-" + tmpbl + f"§§3begin§§1verbatim§§2{tmp}" + \
                     tmpbl + "§§3end§§1verbatim§§2§§-"
        else:
            k.text = f"§§=1§§3verb|{tmp.strip()}|§§=1"
    elif dc.mode in ["RIS", "plain"]:                                   # RIS / plain|
        if "\n" in tmp.strip():
            k.text = f"§§-{tmp.strip()}§§-"                             # change embedded text
        else:
            k.text = f"§§=1|{tmp.strip()}|§§=1"
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_code")

# ------------------------------------------------------------------
def mod_dd(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_dd
    """
    Processes the 'dd' sub-element.

    Fetches embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_dd")

    # mod_dd --> innertext
    # mod_dd --> mod_TeXchars1
    # mod_dd --> gen_fold

    tmp   = innertext(k, k.text, pp).strip()                            # get embedded text and sub-elements
    tmp   = mod_TeXchars1(tmp)
    tmp   = re.sub("[\n]+", BLANK, tmp)
    tmp   = re.sub("[ \t]+", BLANK, tmp)
    width = CASES[dc.mode]
    tmpbl = "§§=" + str(width)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX|BibLaTeX
        k.text = tmp
    if dc.mode in ["RIS", "plain"]:                                     # RIS | plain
        tmp = gen_fold(tmp, width)
        k.text = tmp
    if dc.mode in ["Excel"]:                                            # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_dd")

# ------------------------------------------------------------------
def mod_dl(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_dl
    """
    Processes the 'ol' element.

    Fetches embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_dl")

    # mod_dl --> innertext

    tmp   = innertext(k, k.text, pp).strip()                            # get embedded text and sub-elements
    tmp   = re.sub("[\n]+", BLANK, tmp)
    tmp   = re.sub("[ \t]+", BLANK, tmp)
    width = CASES[dc.mode]
    tmpbl = "§§=" + str(width)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX|BibLaTeX
        tmp = "§§-" + tmpbl + f"§§3begin§§1description§§2{tmp}§§-" + \
              tmpbl + "§§3end§§1description§§2§§-§§-"
        k.text = tmp
    if dc.mode in ["RIS", "plain"]:                                     # RIS | plain
        k.text = "§§-" + tmpbl + tmp
    if dc.mode in ["Excel"]:                                            # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_dl")

# ------------------------------------------------------------------
def mod_dt(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_dt
    """
    Processes the 'dt' sub-element.

    Fetches embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_dt")

    # mod_dt --> innertext

    tmp   = innertext(k, k.text, pp).strip()                            # get embedded text and sub-elements
    width = CASES[dc.mode]
    tmpbl = "§§=" + str(width)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX/BibLaTeX
        k.text = "§§-" + tmpbl + f"§§3item[{tmp}] "
    if dc.mode in ["RIS", "plain"]:                                     # BibLaTeX | RIS | plain
        k.text = "§§-" + tmpbl + "+ " + tmp + ": "
    if dc.mode in ["Excel"]:                                            # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_dt")

# ------------------------------------------------------------------
def mod_em(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_em
    """
    Processes the 'em' element.

    Fetches any embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_em")

    # mod_em --> innertext

    tmp = innertext(k, k.text, pp).strip()                              # get embedded text and sub-elements

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        k.text = f"§§=1§§3emph§§1{tmp}§§2§§=1"                          # change embedded text
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = f"§§=1'{tmp}'§§=1"                                     # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_em")

# ------------------------------------------------------------------
def mod_i(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):          # function mod_i
    """
    Processes the 'i' element.

    Fetches any embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_xref --> innertext

    if dc.debugging:
        print("+++ >CTANOut:mod_i")

    tmp = innertext(k, k.text, pp).strip()                              # get embedded text and sub-elements

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        k.text = f"§§=1§§3emph§§1{tmp}§§2§§=1"                          # change embedded text
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = f"§§=1'{tmp}'§§=1"                                     # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_i")

# ------------------------------------------------------------------
def mod_li(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_li
    """
    Processes the 'li' element.

    Fetches embedded text.
    Rewrites the variable dc.level.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.level      string: level of itemize|enumerate (<ol>, <ul>)
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.6  2026-07-09 "global" statements removed
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_li --> innertext
    # mod_li --> mod_TeXchars1
    # mod_li --> test_embedded
    # mod_li --> gen_fold

    if dc.debugging:
        print("+++ >CTANOut:mod_li")

    tmptext = innertext(k, k.text, pp).strip()                          # get embedded text and sub-elements
    tmppref = EMPTY

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        tmptext = mod_TeXchars1(tmptext)
    tmptext = re.sub("\n", BLANK, tmptext)
    tmptext = re.sub("[ \t]+", BLANK, tmptext)

    width = CASES[dc.mode]
    tmpbl = "§§=" + str(width)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX|BibLaTeX
        tmptext = "§§-" + tmpbl + f"§§3item {tmptext}"
        k.text  = tmptext
    elif dc.mode in ["RIS", "plain"]:                                   # RIS|plain
        if dc.level == "ul-li2":
            tmppref ="++"
            tmptext = gen_fold(tmptext, width + 3)
        elif dc.level == "ul-li":
            tmppref ="+"
            if not test_embedded(k, pp):
                tmptext = gen_fold(tmptext, width + 2)
        elif dc.level == "ol-li2":
            tmppref ="**"
            tmptext = gen_fold(tmptext, width + 2)
        elif dc.level == "ol-li":
            tmppref ="*"
            if not test_embedded(k, pp):
                tmptext = gen_fold(tmptext, width + 3)
        tmptext = "§§-" + tmpbl + tmppref + BLANK * 2 + tmptext
        k.text  = tmptext
    elif dc.mode in ["Excel"] :                                         # Excel
        pass

    if dc.debugging:
        print("+++ <CTANOut:mod_li")

# ------------------------------------------------------------------
def mod_pre(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):        # function mod_pre
    """
    Processes the 'pre' element.

    Fetches any embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_pre --> mod_TeXchars2

    if dc.debugging:
        print("+++ >CTANOut:mod_pre")

    tmp       = k.text
    tmp       = mod_TeXchars2(tmp)
    tmp       = re.sub("\n[ ]+", "§§-", tmp)

    width:int = CASES[dc.mode]
    tmpbl:str = "§§=" + str(width)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        if ("\n" in tmp.strip()) or ("§§-" in tmp.strip()):
            k.text = "§§-" + tmpbl + f"§§3begin§§1verbatim§§2{tmp}" + \
                     tmpbl + "§§3end§§1verbatim§§2§§-"
        else:
            k.text = f"§§=1§§3verb|{tmp.strip()}|§§=1"
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        if "\n" in tmp.strip():
            k.text = f"§§-{tmp.strip()}§§-"                             # change embedded text
        else:
            k.text = f"§§=1|{tmp.strip()}|§§=1"
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_pre")

# ------------------------------------------------------------------
def mod_small(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):      # function mod_small
    """
    Processes the 'small' element.

    Fetches any embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_small --> innertext

    if dc.debugging:
        print("+++ >CTANOut:mod_small")

    tmp = innertext(k, k.text, pp).strip()                              # get embedded text and sub-elements

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        k.text = f"§§=1§§1§§3small {tmp}§§2§§=1"                        # change embedded text
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = f"§§=1'{tmp}'§§=1"                                     # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing
    if dc.debugging:
        print("+++ <CTANOut:mod_small")

# ------------------------------------------------------------------
def mod_TeXchars1(s:str, dc=dc_var) ->str:                              # function mod_TeXchars1
    r"""
    auxilary function: Prepares characters for LaTeX|BibLaTeX (only for
    description - intended for printing).

    characrers to be prepared:
    -------------------------
    $ ---> \$   --->
    { ---> \{   ---> \textbraceleft
    } ---> \}   ---> \textbraceright
    # ---> \#   --->
    \ ---> ...  ---> \textbackslash
    & ---> \&   --->
    _ ---> \_   --->
    ^ ---> \^{} ---> \textasciicircum
    % ---> \%   --->
    ~ ---> \~{} ---> \textasciitilde

    \ ---> §§3
    { ---> §§1
    } ---> §§2

    Parameters:
    ----------
    s    str
         string with characters to be prepared
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a changed string,

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.56   2024-02-18 "[\[] --> r"[\[]
    # 2.72   2025-11-21 in comment: List of TeX character conversions
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_TeXchars1")

    tmp = s
    tmp = re.sub(r"[\[]", "[", tmp)                                     # change [
    tmp = re.sub("≥", "§§4>=§§4", tmp)                                  # change ≥
    tmp = re.sub("≤", "§§4<=§§4", tmp)                                  # change ≤
    tmp = re.sub("#", "§§3§§6", tmp)                                    # change #
    tmp = re.sub("_", "§§3§§7", tmp)                                    # change _
    tmp = re.sub("~", "§§1§§3textasciitilde§§2", tmp)                   # change ~
    tmp = re.sub("&", "§§3§§5", tmp)                                    # change &
    tmp = re.sub("%", "§§3§§9", tmp)                                    # change %
    tmp = re.sub("{", "§§1§§3textbraceleft§§2", tmp)                    # change {
    tmp = re.sub("}", "§§1§§3textbraceright§§2", tmp)                   # change }
    tmp = re.sub(r"[\^]", "§§1§§3textasciicircum§§2", tmp)              # change ^
    tmp = re.sub("[$]", "§§3§§4", tmp)                                  # change $
    tmp = re.sub(r"\\", "§§1§§3textbackslash§§2", tmp)                  # change \
    tmp = re.sub("“", "``", tmp)                                        # change “
    tmp = re.sub("”", "''", tmp)                                        # change ”
    tmp = re.sub("`", "'", tmp)                                         # change `
    tmp = re.sub("´", "'", tmp)                                         # change ´
    return tmp

# ------------------------------------------------------------------
def mod_TeXchars2(s:str, dc=dc_var) ->str:                              # function mod_TeXchars2
    r"""
    auxiliary function: Prepares characters for LaTeX|BibLaTeX (only for
    description - intended for usage by LaTeX).

    Changed characters:
    ------------------
    "\^" --> r"\^"
    "[\^]" --> r"[\^]"
    "[\[] --> r"[\[]

    Parameters:
    ----------
    s    str
         string with characters to be prepared
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Returns a changed string s.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
      
    Messages:
    --------
    There are no specific messages.
    """

    # 2.56   2024-02-18 "\^" --> r"\^"; "[\^]" --> r"[\^]";
    #                   "[\[] --> r"[\[]
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_TeXchars2")

    tmp = s
    tmp = re.sub("{", "§§1", tmp)                                       # change    {
    tmp = re.sub("}", "§§2", tmp)                                       # change    }
    tmp = re.sub(r"\\", "§§3", tmp)                                     # change    \
    tmp = re.sub("[$]", "§§4", tmp)                                     # change    $
    tmp = re.sub("&", "§§5", tmp)                                       # change    &
    tmp = re.sub("#", "§§6", tmp)                                       # change    #
    tmp = re.sub("_", "§§7", tmp)                                       # change    _
    tmp = re.sub(r"\^", "§§8", tmp)                                     # change    ^
    tmp = re.sub("%", "§§9", tmp)                                       # change    %
    tmp = re.sub("~", "§§0", tmp)                                       # change    ~
    tmp = re.sub("“", "``", tmp)                                        # change    “
    tmp = re.sub("”", "''", tmp)                                        # change    ”
    tmp = re.sub("`", "'", tmp)                                         # change    `
    tmp = re.sub("´", "'", tmp)                                         # change    ´
    return tmp

# ------------------------------------------------------------------
def mod_tt(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_tt
    """
    Processes the 'tt' element.

    Fetches embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_tt --> innertext
    # mod_tt --> mod_TeXchars1

    if dc.debugging:
        print("+++ >CTANOut:mod_tt")

    tmp = innertext(k, k.text, pp).strip()                              # get embedded text and sub-elements

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        tmp    = mod_TeXchars1(tmp)                                     # change embedded text
        k.text = f"§§=1§§3texttt§§1{tmp}§§2§§=1"
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = f"§§=1{tmp}§§=1"                                       # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_tt")

# ------------------------------------------------------------------
def mod_xref(k:xml.tree.ElementTree.Element, pp:str, dc=dc_var):        # function mod_xref
    """
    Processes the 'xref' element.

    Fetches any embedded text and the attribute 'refid'.

    Parameters:
    ----------
    k: current knot (xml.tree.ElementTree.Element)
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67   2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_xref --> innertext

    if dc.debugging:
        print("+++ >CTANOut:mod_xref")

    tmp  = k.get("refid", EMPTY)                                        # get attribute refid
    tmp2 = CTAN_URL4 + tmp                                              # build the complete URL

    if k.text == None:                                                  # no embedded text
        k.text = tmp                                                    # get embedded text

    tmp3 = innertext(k, k.text, pp).strip()                             # get embedded text and
                                                                        # sub-elements

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX | BibLaTeX
        tmp3   = re.sub("_", "-", tmp3)                                 # hange embedded text
        k.text = f"§§=1§§3href§§1{tmp2}§§2§§1{tmp3}§§2§§=1"
    elif dc.mode in ["RIS", "plain"]:                                   # RIS | plain
        k.text = f"§§=1{tmp3} ({tmp2})§§=1"                             # change embedded text
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # for Excek do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_xref")
 
# ------------------------------------------------------------------
def mod_ol(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_ol
    """
    Processes the 'ol' element.

    Fetches embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_ol --> innertext

    if dc.debugging:
        print("+++ >CTANOut:mod_ol")

    tmp   = innertext(k, k.text, pp).strip()                            # get embedded text and sub-elements

    tmp   = re.sub("[\n]+", BLANK, tmp)
    tmp   = re.sub("[ \t]+", BLANK, tmp)
    width = CASES[dc.mode]
    tmpbl = "§§=" + str(width)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX|BibLaTeX
        k.text = "§§-" + tmpbl + f"§§3begin§§1enumerate§§2{tmp}§§-" + \
                 tmpbl + "§§3end§§1enumerate§§2§§-"
    if dc.mode in ["RIS", "plain"]:                                     # RIS | plain
        k.text = tmp + "§§-"
    if dc.mode in ["Excel"]:                                            # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_ol")

# ------------------------------------------------------------------
def mod_p(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):          # function mod_p
    """
    Processes the 'p' element.

    Fetches embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # mod_p --> innertext
    # mod_p --> mod_TeXchars1
    # mod_p --> test_embedded
    # mod_p --> gen_fold

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ >CTANOut:mod_p")

    tmptext = innertext(k, k.text, pp).strip()                          # get embedded text and
                                                                        # sub-elements
    width   = CASES[dc.mode]

    tmptext = re.sub("[\n]+", BLANK, tmptext)
    tmptext = re.sub("[ ]+", BLANK, tmptext)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX
        tmptext  = mod_TeXchars1(tmptext)
        if not test_embedded(k, pp):
            tmptext = gen_fold(tmptext, width)
        tmptext += "§§-§§-§§=" + str(width)
        k.text   = tmptext
    elif dc.mode in ["plain", "RIS"]:                                   # plain|RIS
        if not test_embedded(k, pp):
            tmptext = gen_fold(tmptext, width)
        tmptext += "§§-§§-§§=" + str(width)
        k.text   = tmptext
    elif dc.mode in ["Excel"]:                                          # Excel
        pass                                                            # do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_p")

# ------------------------------------------------------------------
def mod_ul(k:xml.etree.ElementTree.Element, pp:str, dc=dc_var):         # function mod_ul:
    """
    Processes the 'ul' element.

    Fetches any embedded text.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging
    
    Messages:
    --------
    There are no specific messages.
    """

    # 2.67    2025-02-11 more f-strings
    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    # mod_ul --> innertext

    if dc.debugging:
        print("+++ >CTANOut:mod_ul")

    tmp   = innertext(k, k.text, pp).strip()                            # get embedded text and sub-elements

    tmp   = re.sub("[\n]+", BLANK, tmp)
    tmp   = re.sub("[ \t]+", BLANK, tmp)

    width:int = CASES[dc.mode]
    tmpbl:str = "§§=" + str(width)

    if dc.mode in ["LaTeX", "BibLaTeX"]:                                # LaTeX|BibLaTeX
        k.text = "§§-" + tmpbl + f"§§3begin§§1itemize§§2{tmp}§§-" + \
                 tmpbl + "§§3end§§1itemize§§2§§-"
    if dc.mode in ["RIS", "plain"]:                                     # RIS | plain
        k.text = tmp + "§§-"
    if dc.mode in ["Excel"]:                                            # Excel
        pass                                                            # for Excel do nothing

    if dc.debugging:
        print("+++ <CTANOut:mod_ul")

# ------------------------------------------------------------------
def test_embedded(k:xml.etree.ElementTree.Element, pp:str,
                  dc=dc_var) ->bool:                                    # function: test_embedded
    """
    auxiliary function: Tests current knot for embedded material.

    Parameters:
    ----------
    k    xml.etree.ElementTree.Element
         current knot
         no default
    pp   str
         name of the current package
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    -------
    Resturns TRUE, if there are embedded elements in k.

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:test_embedded")

    tmp:bool = False
    for child in k:
        tmp = tmp or (child.tag in ["ol", "ul", "li", "pre", "code"])
    return tmp

# ------------------------------------------------------------------
def TeXchars_restore(s:str, dc=dc_var) ->str:                           # function TeXchars_restore
    """
    auxiliary function: Restores characters (only for LaTeX|BibLaTeX).

    Parameters:
    ----------
    s    str
         string with characters to be restored
         no default
    dc   instance of the data class 'dataclass_variable'
         default: dc_var

    Returns:
    ------- 
    string with restored characters

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging  flag: debugging

    Messages:
    --------
    There are no specific messages.
    """

    # 3.3    2026-07-09 data class used
    # 3.3.3  2026-07-09 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.3.4  2026-07-09 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data
    #                   class

    if dc.debugging:
        print("+++ -CTANOut:TeXchars_restore")

    tmp  = s
    tmp  = re.sub("§§=12(§§=1)?", BLANK * 12, tmp)
    tmp  = re.sub("§§=10(§§=1)?", BLANK * 10, tmp)
    tmp  = re.sub("§§=18(§§=1)?", BLANK * 18, tmp)
    tmp2 = dc.p8.findall(tmp)                                              # find "§§=xx"
    for i in tmp2:
        tmp = re.sub("§§=" + str(i), BLANK * int(i), tmp)
                                                                        # change "§§=xx" to blanks
    tmp = re.sub("§§1", "{", tmp)                                       # restore {
    tmp = re.sub("§§2", "}", tmp)                                       # restore }
    tmp = re.sub("§§3", r"\\", tmp)                                     # restore \
    tmp = re.sub("§§4", "$", tmp)                                       # restore $
    tmp = re.sub("§§5", "&", tmp)                                       # restore &
    tmp = re.sub("§§6", "#", tmp)                                       # restore #
    tmp = re.sub("§§7", "_", tmp)                                       # restore _
    tmp = re.sub("§§8", "^", tmp)                                       # restore ^
    tmp = re.sub("§§9", "%", tmp)                                       # restore %
    tmp = re.sub("§§0", "~", tmp)                                       # restore ~
    tmp = re.sub("§§-", "\n", tmp)                                      # restore \n
    return tmp


#===================================================================
# K. Main Part

# 2.68   2025-02-12 no test: __name__ == "__main__; ==> CTANLoad.py can be
#                   imported

##if __name__ == "__main__":
##    try:
##        pass
##    except:
##        pass
##    main()
##else:
##    if verbose:
##        print("[CTANOut] Error: tried to use the program indirectly")
main()


#===================================================================
# L. History

# ------------------------------------------------------------------
# 1.75 2021-05-14 more types for -m
# 1.76 2021-05-14 clean-up of variables
# 1.77 2021-05-15 more details in verbose mode for -mt
# 1.78 2021-05-15 output the call parameters in more details in verbose mode
# 1.79 2021-05-20 folder separator improved
# 1.80 2021-05-23 folder name improved
# 1.81 2021-05-24 folder handling (existance, installation) improved
# 1.82 2021-05-26 structure of CTAN.pkl adapted
# 1.83 2021-05-26 output of license information now with full text
# 1.84 2021-05-26 output and interpretaion of language codes improved
# 1.85 2021-05-27 correction of source errors in <version .../> in licenses.xml
# 1.86 2021-06-12 auxiliary function fold: shorten long option values for output
# 1.87 2021-06-12 messages classified: Warnings, Error, Info; no package found which match
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
# 1.99 2021-07-19 make_stat, make_xref, make_tap respect option -A; output changed
# 1.100 2021-07-19 comments in BibLaTeX/LaTeX respects option -A
# 1.101 2021-07-20 new global variabel no_packages_processed: if set, all.tap,all.top,all.xref are not generated
# 1.102 2021-07-21 results are sorted
# 1.103 2021-07-21 only for LaTeX/BibLaTeX: output in comments is folded; new function comment_fold()
# 1.104 2021-07-21 only for LaTeX: output folded an 1st page of output; new function TeX_fold()
# 1.105 2021-07-26 results now alphabetically sorted; output improved
# 1.106 2021-09-25 output of year in BibLaTeX enhanced
# 1.107 2021-10-10 changes in get_year: analyze element year, too
# 1.108 2021-10-10 completion of language_keys
# 1.109 2021-10-10 element documentation indexed
# 1.110 2021-10-11 output in Hindi now possible
# 1.111 2021-10-11 section headers (for LaTeX) improved
# 1.112 2021-10-11 error messages actualized
# 1.113 2021-10-12 output headers for LaTeX and BibLaTeX enhanced
# 1.114 2021-10-12 new function biblatex_citationkey: generate valid citation keys + corresponding changes in 'leading', 'main', and 'also'
# 1.115 2021-10-12 function 'leading' cleaned
# 1.116 2021-10-12 comment blocks re-organized
# 1.117 2021-10-12 document strings in functions enhanced
# 1.118 2021-10-12 in comment block: list of functions and function tree actualized
# 1.119 2021-10-13 RIS output: a) type changed to ICOMM; b) UR output: now for main document and CTAN element <documentation .../>
# 1.120 2021-10-14 RIS output: field "PY  -" settled now with year (collected from <version.../> and <copyright ... />)
# 1.121 2021-10-14 RIS output: "L4  -" changed to "L2  -"
# 1.122 2021-10-15 RIS output: output "Y2  - " (from <version ... />); implements "last change"
# 1.123 2021-10-15 RIS output: <also ...> mapped into notice (= "N1  -")
# 1.124 2021-10-17 RIS output: LA output improved; BibLaTeX output: 'file' output improved
# 1.125 2021-10-20 language codes es-mx, sl and zh-cn added
# 1.126 2021-10-20 output of title/subtitle a/o T1/T2: output now harmonized in functions 'name'/'caption'
# 1.127 2021-10-20 now harmonized: output of 'language' a/o 'LA' in function 'trailing'
# 1.128 2021-10-21 Excel: output and processing extended, improved and enhanced; new call parameter -m csv
# 1.129 2021-10-22 RIS: better values for 'PY' and 'LA'; mapping of <also .../>; better values for 'Y2' and 'Y3'
# 1.130 2021-10-23 RIS: 'N1' re-arranged; fieldwidth (label width) changed; 'L1' output corrected
# 1.131 2021-10-24 date of last access in RIS/BibLaTeX: 'Y2' and 'date' unified
# 1.132 2021-10-24 output of URL and date of last access in RIS/BibLaTeX: 'UR' and 'Y3' a/o 'url' and 'urldate'
# 1.133 2021-10-25 BibLaTeX: licenses collected and output in 'userb'; 'note' corrected; comment block at the beginning re-arranged; 'year' output improved
# 1.134 2021-10-25 BibLaTeX: 'language' output enhanced
# 1.135 2021-10-26 function 'leading': trimmed; determination of author(s) improved; 'userunknown' renamed to 'authorunknown'
# 1.136 2021-10-27 TeX output: additionally URL of Web page on CTAN, year and last access date
# 1.137 2021-10-28 plain output: additionally URL of Web page on CTAN, year and last access date
# 1.138 2021-10-28 RIS and BibLaTeX output: unnecessary empty output lines suppressed
# 1.139 2021-10-29 Excel output: some improvements and a few corrections
# 1.140 2021-10-29 output of keywords, language(s), local file name(s), and 'note' a/o 'N1'  improved
# 1.141 2021-11-01 supplementary notes at the beginning of xyz.xref and xyz.tap
# 1.142 2021-11-01 aesthetic repairs for the processing of <description ...> ...</description> with 'language' attribute
# 1.143 2021-11-02 function 'mod_xref' modified
# 1.144 2021-11-02 full UTF-8 output on stdout enabled
# 1.145 2021-11-03 function 'description', 'p', 'ul', and 'li': output of multiple spaces and empty lines revised
# 1.146 2021-11-03 BibLaTeX: mapping of 'description' to 'abstract' improved
# 1.147 2021-11-05 BibLaTeX: "@" substituted to 'at' in 'note' and 'usera' output
# 1.148 2021-11-05 correct processing of multiple CTAN field 'also' for BibLaTeX/Excel; correct processing of multiple CTAN 'alias' for Excel
# 1.149 2021-11-05 correct processing of multiple CTAN field 'description' for all modes
# 1.150 2021-11-05 correction for option -b: '@online' as new default; '@electronic' as new choose
# 1.151 2021-11-06 new option -sb (--skip_biblatex): additional function 'bibfield_test'; additional requests
# 1.153 2021-11-06 BibLaTeX/plain/LaTeX/RIS/Excel: interaction between 'year' und 'date' harmonized
# 1.154 2021-11-08 LaTeX: index for 'year' now; index for CTAN field documentation no longer in use
# 1.155 2021-11-08 BibLaTeX: some items no longer collected in 'note', but in 'usera', 'userb', 'userc', 'userd', 'usere', 'userf'
# 1.156 2021-11-11 new examples for option '-sb'
# 1.157 2021-11-11 BibLaTeX: output of 'file' corrected; now jabref compatible
# 1.158 2021-11-13 mapping CTAN --> BibLaTeX changed: now 'texlive', 'miktex' --> embedded in 'note'; ctan --> 'userc'; 'contact' --> collected in 'userd'
# 1.159 2021-11-19 LaTeX output: "--local file" now with relativ path
# 1.160 2021-11-20 'year' in LaTeX/plain: "without year" if it is appropiate
# 1.161 2021-11-21 for all modes: empty output for abstract/description corrected
# 1.162 2021-11-28 greater parts of comment blocks moved to external text files

# 2.0     2022-01-02 new concept for the processing of <description> ... </description>; content recursively processed
# 2.1     2022-01-02 functions mod_backslash and mod_TeXchars removed
# 2.2     2022-01-02 new functions: mod_TeXchars1, mod_TeXchars2, TeXchars_restore (change and restore the content of elements)
# 2.3     2022-01-03 functions renamed: p --> mod_p; ol --> mod_ol; ul --> mod_ul; dl --> mod_dl; li --> mod_li; dd --> mod_dd; dt --> mod_dt
# 2.4     2022-01-03 new function: innertext (scans the body of description and calls recursively other functions for the sub-elements)
# 2.5     2022-01-04 new function: mod_small (processing of <small> ...</small>)
# 2.6     2022-01-04 new functions: mod_dl, mod_dt, mod_dd (processing of <dl>, <dt>, and <dd>)
# 2.7     2022-01-06 nested <ol>/<ul> can be processed
# 2.8     2022-01-07 left indentation of <li> (mode dependant)
# 2.9     2022-01-09 new function gen_fold (folds content of <li>)
# 2.10    2022-01-10 new function test_embedded (controls the call of gen_fold in <p>, <li>, <dd>)
# 2.11    2022-01-11 new language code "zn,ja"
# 2.12    2022-01-26 texts for the -h option changed
# 2.13    2022-01-28 left indentation for all modes tuned
# 2.14    2022-01-28 additionally: output of date and time in statistics on output (-stat)
# 2.15    2022-02-02 additional license information: now with free a/o not free
# 2.16    2022-02-05 additional texts at the top of output files
# 2.17    2022-02-07 messages in get_topic_packages, get_name_packages, and get_author_packages changed

# 2.18    2022-02-15 new option -L (selection of packages by licenses)
# 2.18.1  2022-02-15 new variables: LICENSE_TEMPLATE_TEXT, LICENSE_TEMPLATE_DEFAULT, dc.license_template (used by argparse); licensepackages
# 2.18.2  2022-02-15 new section for specifying -L by argparse
# 2.18.3  2022-02-15 new function get_license_packages (collecting packages for specified licenses)
# 2.18.4  2022-02-15 changes in load_pickle1: new CTAN.pkl component licensepackages
# 2.18.5  2022-02-15 new variable p9 [re.compile(dc.license_template)]; allows filtering by license template
# 2.18.6  2022-02-15 changes in first_lines, licenseT3rocess_packages, make_stat, make_statistics, and process_packages
# 2.18.7  2022-02-16 shorttitlde and status can be used for -L, too

# 2.19    2022-02-19 error in make_stat corrected
# 2.20    2022-02-21 some corrections in make_stat

# 2.21    2022-02-23 in LaTeX mode: output of licenses and related packages (tlp) + output of licenses and explainations (lic)
# 2.21.1  2022-02-03 new function make_tlp; changes in main(); new file xyz.tlp; called in LaTeX document (option -mt)
# 2.21.2  2022-02-23 new function make_lics; changes in main(); new file xyz.lic; called in LaTeX document (option -mt)
# 2.21.3  2022-02-23 additions and corrections in make_tlp, make_tap, make_lics, make_xref

# 2.22    2022-03-01 additions and corrections in make_stat
# 2.23    2022-03-01 texts for argparse and terminal log changed
# 2.24    2022-03-01 corrections in first_lines (plain, BibLaTeX)
# 2.25    2022-03-15 LaTeX header/preambel changed (fonts, languages)no_package_processed 
# 2.26    2022-03-20 error in mod_pre and mod_code corrected
# 2.27    2022-03-25 error in the processing of -mt option corrected
# 2.28    2022-03-30 BibLaTeX: "1970" removed from BiobTeX key; get_authorkey changed
# 2.29    2022-04-10 BibLaTeX: additional request in biblatex_citationkey, if id is unknown
# 2.30    2022-09-25 list of language codes extended
# 2.31    2022-09-26 error for index entry in description function repaired
# 2.32    2022-09-27 new option --no:files: generate no files; new variable; changes in some functions
# 2.33    2022-09-28 some enhancements in "Resettings and Settings" (if -nf is set)
# 2.34    2022-09-30 processing of unknown/wrong language in description a/o documentation improved
# 2.35    2023-06-11 due to -nf: changes in statistics output (parameter -stat)

# 2.36    2023-06-11 changes in rendering of description content
# 2.36.1  2023-06-11 interaction of §§= and TeXchars_restore improved
# 2.36.2  2023-06-11 indentation in description in some places corrected
# 2.36.3  2023-06-11 line breaks in <pre> are removed; changes in mod_pre, mod_code

# 2.37    2023-06-11 LaTeX procession
# 2.37.1  2023-06-11 corrected: without -mt no proper file end for LaTeX
# 2.37.2  2023-06-11 LaTeX header changed (fonts, languages)

# 2.38    2023-06-11 Workaround if language key, topic key, author key, license key are unknown
# 2.39    2023-06-11 Error in trailing function: if languagecode is unknown; workaround

# 2.40    2023-06-11 new option -y (filtering on the base of year templates
# 2.40.1  2023-06-11 some changes in relevant functions (interaction of different filter operations improved)
# 2.40.2  2023-06-11 related changes in the statistics part (option -stat)

# 2.41    2023-06-15 CTANLoad-changes.txt, CTANLoad-examples.txt, CTANLoad-functions.txt changed
# 2.42    2023-06-15 output on terminal changed
# 2.43    2023-06-15 new option -dbg/--debugging: debugging mode enabled
# 2.44    2023-06-15 output on xyz.stat changed
# 2.45    2023-06-26 some changes in statistics output
# 2.46    2023-06-28 fold() changed to adjust protocoll output
# 2.47    2023-07-06 xyz.lic, xyz.tap, xyz.tlp, xyz.top, xyz.xref now without any \index entry
# 2.48    2023-07-07 variable year_default_template redefined
# 2.49    2023-07-08 messages now with the signature [CTANOut]
# 2.50    2023-07-08 \index entries in xyz.xref, xyz.lic, xyz.tlp removed

# 2.51    2023-07-08 new concept for the handling of languages
# 2.51.1  2023-07-08 new default language: nls
# 2.51.2  2023-07-09 new concept for the language handling in documentation a/o descrpition
# 2.51.3  2023-07-10 language \index entries in LaTeX mode improved
# 2.51.4  2023-07-10 language \item entries in LaTeX mode improved
# 2.51.5  2023-07-10 in RIS/plain/BibLaTeX mode: smaller errors in the output of documentation a/o description corrected
# 2.68   2025-02-12 no test: __name__ == "__main__; ==> CTANLoad.py can be imported

# 2.52    2023-07-16 language en,ru now in LANGUAGECODES
# 2.53    2023-07-28 output of -stat now with program date
# 2.54    2024-02-18 new language codes: en,fr and es-pe
# 2.55    2024-02-18 \inp ecaped to \\inp, Mik\TeX escaped to Mik\\TeX
# 2.56    2024-02-18 "[\^s]+" changed to "r[\^]+"; "\^" --> r"\^"; "[\^]" --> r"[\^]"; "[\[] --> r"[\[]"
# 2.57    2024-02-28 in make_tap: enable processing of "_" in author names
# 2.58    2024-02-28 in authorref and copyrighT: enable processing of "_" in author/owner names
# 2.59    2024-03-26 in make_stat, make_tap, make_tlp, make_tops, make_lics, make_xref: Small additions to the output texts
# 2.60    2024-03-28 all __doc__ texts of the functions completed (parameters and global variables)
# 2.61    2024-04-12 smaller changes in make_statistics
# 2.62    2024-07-26 some smaller text changes for argparse

# 2.63    2024-07-26 argparse revised
# 2.63.1  2024-07-26 additional parameter in .ArgumentParser: prog, epilog, formatter_class  
# 2.63.2  2024-07-26 subdivision into groups by .add_argument_group
# 2.63.3  2024-07-26 additional arguments in .add_argument (if it makes sense): type, metavar, action, dest

# 2.64    2025-01-27 languages "en,zh", "yue", "zh-tw" now in LANGUAGECODES
# 2.65    2025-02-06 wherever appropriate: string interpolation with f-strings instead of .format
# 2.66    2025-02-06 everywhere: all source code lines wrapped at a maximum of 80 characters
# 2.67    2025-02-11 more f-strings
# 2.68    2025-02-12 no test: __name__ == "__main__; ==> CTANLoad.py can be imported
# 2.69    2025-03-24 time specification with unit
# 2.70    2025-11-03 argparse texts revised
# 2.71    2025-11-05 footnote text in make_stat corrected
# 2.72    2025-11-21 in comment: List of TeX character conversions
# 2.73    2025-11-21 in comment: List of §§ constructions
# 2.74    2025-12-03 reference to LaTeX in the files xyz.top, xyz.xref, xyz.tap, xyz.lic, xyz.tlp, xyz.stat

# 3.0    2026-04-01 Complete revision (too many changes to list in the code)
# 3.0.1  2026-04-01 Functions with type annotations
# 3.0.2  2026-04-01 Variable annotations (where appropriate and possible)
# 3.0.3  2026-04-01 Constants in uppercase
# 3.0.4  2026-04-01 .format replaced with f-strings (where appropriate)
# 3.0.5  2026-04-01 __doc__ texts supplemented and standardised
# 3.0.6  2026-04-01 Standardised: Code up to a maximum of column 71
# 3.0.7  2026-04-01 Standardised: Comments from column 72 onwards

# 3.1    2026-07-05 ACT_PROGRAMNAME depends on OPERATING_SYSTEM now
# 3.2    2026-07-09 try ... except enhanced; new error message

# 3.3    2026-07-09 data class used
# 3.3.0  2026-07-09 new module dataclasses
# 3.3.1  2026-07-09 new class dataclass-variable (including all globally used variables) derfined
# 3.3.2  2026-07-09 instance "dc_var" of this class created
# 3.3.3  2026-07-09 if necessary: Function definitions supplemented by the parameter "dc=dc_var"
# 3.3.4  2026-07-09 relevant local variables prefixed with "dc." and/or non-local with "dc_var"   
# 3.3.5  2026-07-09 original definitions of globally used variables removed
# 3.3.6  2026-07-09 "global" statements removed
# 3.3.7  2026-07-09 __doc__ texts supplemented/adapted to the data class

# 3.4    2026-07-10 handling of LaTeX source code texts improved
# 3.4.1  2026-07-10 texts for header, classoptions, title, usepkp, trailer simplified
# 3.4.2  2026-07-10 new functions for: make_...
# 3.4.3  2026-07-10 call the new functions

# 3.5    2026-07-13 new function: argparse_process
# 3.5.1  2026-07-13 Defines the arguments for the program CTANOut and starts.
# 3.5.2  2026-07-13 calls argparse_process

# 3.6    2026-07-13 new function: argparse_postprocess
# 3.6.1  2026-07-13 Postprocesses some parameters for the program CTANOut.
# 3.6.2  2026-07-13 calls argparse_postprocess

# 3.7    2026-07-13 backtracing
# 3.7.1  2026-07-13 new module traceback
# 3.7.2  2026-07-13 call traceback.print_exc()

# 3.8    2026-08-05 default values for variables in dataclass_variable on the basis of constants now
# 3.9    2026-08-19 minor corrections in error messages

# 3.10   2026-08-15 log output of the options in the call revised

# 3.11   2026-08-16 Calculation and output of the input string
# 3.11.1 2026-08-16 moved from first_lines to argparse_postprocess
# 3.11.2 2026-08-16 variable 'arguments' now in dataclass_variable

# 3.12   2026-08-20 Name and size of the results PDF file
# 3.13   2026-08-21 type annotation of skip, skip_biblatex in ataclass_variable corrected


# ------------------------------------------------------------------
# - m=LaTeX: mehr Texte in """-"""-Notation (x)
# + Zählung der Kommentare korrigieren


# Probleme/Ideen:

# + anfängliche Änderungen mit Warning spiegeln sich nicht in Aufruf-Überschrift wider
# - Idee: Klassenkonzept für die Ausgabe: für jeden Ausgabetyp eine eigene Klasse?
# - NotImplementedError siehe https://realpython.com/python-built-in-exceptions/
# - kann Zeitstempel bei XML/PDF-Dateien genutzt werden? wahrscheinlich nicht (?)
# - <ol>/<ul> gescchachtelt; Stack verwenden (?)
# - <ol> sollte bei RIS und plain Nummern erzeugen
# - lualatex-Ausgabe: missing character
# - Fehler bei BibLateX: author nicht normgerecht?
# - skip_biblatex auch für andere Modus?
# - generelleres Konzept: Ausgabe + Reihenfolge der auszugebenden Items auch bei anderen Modus?
# - neue Funktionen: argparse-Postprodessing, LaTeX-Vorbereitung
# - neue Meldung  ...any dokumentieren (x)
# - m==Excel kontrollieren

# - BibLaTeX: Probleme noch bei Mehrfach-related (laut jabref)
# - Protokollausgabe der Aufrufparameter: Änderungen berücksichtigen?

# - korrigieren: auch URLs mit "+" laden (auch für andere unzulässige Zeichen)
# - bestimmte Ergebnisse in die zwischenablage liefern?
# - Konzept der <year>-Suche überdenken
# - für BibLaTeX auch ?
# - unterschiedliche Ergebnisse für "2024|2025" und "202[45]"
# + Suche unabhängig von Groß/Kleinschreibung
# + Index verweist auf Seitenummern; all.xref und all.tap auf Abschnittsnummer
