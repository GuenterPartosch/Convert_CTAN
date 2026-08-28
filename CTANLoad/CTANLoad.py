#!/usr/bin/python3
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

"""
CTANLoad.py
(C) Günter Partosch, 2019, 2021-2026

CTANLoad.py is part of the CTAN bundle (CTANLoad.py, CTANOut.py,
CTANLoadOut.py, menu_CTANLoadOut.py).

CTANLoad.py loads XLM and PDF documentation files from
CTAN a/o generates some special lists, and prepares data for CTANOut.

Call of CTANLoad.py
-------------------
CTANLoad.py may be started by:

1. python -u CTANLoad.py <option(s)>
-- always works
2. CTANLoad.py <option(s)>
-- if the OS knows how to handle Python files (files with the name
   extension .py)
3. CTANLoad <option(s)>
-- if there is an executable (in Windows a file with the name
   extension .exe)

Compilation:
-----------
 CTANLoad.py may be compiled by

 (a) pyinstaller
 pyinstaller --paths ... CTANLoad.py -F
 --> provides CTANLoad.exe (Windows)
 pyinstaller works under Linux in a similar way

 (b) nuitka

 (c) not PyPy
 is only suitable to a limited extent, as only a limited Python can be
 interpreted

 --> provides CTANLoad.exe (Windows) a/o CTANLoad (Linux)

Requirements:
------------
 + operating system windows 10/11 or Linux (like Linux Mint or Ubuntu
   or Debian)

 + wget a/o wget2 is installed
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
analyze_XML_file(file)      Function analyze_XML_file(file): Analyzes
                            a XML package file
call_check()                Function call_check: Processes all necessary
                            steps for a integrity check
call_load()                 Function call_load: Processes all steps for
                            a complete ctanload call
call_plain()                Function call_plain: Processes all steps for
                            a plain call
check_integrity(always=False) Function check_integrity(): Checks
                            integrity (tests for inconsistencies)
dload_authors()             Function dload_authors(): Downloads XML file
                            'authors' from CTAN and generate dictionary
                            'authors'.
dload_document_file(href, key, name, XML_file)  Function
                            dload_document_file(href, key, name):
                            Downloads one information file (PDF) from
                            CTAN.
dload_licenses()            Function dload_licenses: Downloads XML file
                            'licenses' from CTAN and generates
                            dictionary 'licenses'.
dload_packages()            Function dload_packages: Downloads XML file
                            'packages' from CTAN and generates
                            dictionary 'packages'.
dload_topics()              Function dload_topics(): Downloads XML file
                            'topics' from CTANB and generates
                            dictionary 'topics'.
dload_XML_files(p)          Function dload_XML_files: Downloads XML
                            package files.
fold(s)                     Function fold(): Auxiliary function:
                            Shortens/folds long option values for output.
generate_lists()            Function generate_lists: Generates some
                            special files (with lists).
generate_pickle1()          Function generate_pickle1
generate_pickle2()          Function generate_pickle2
generate_topicspackages()   Function generate_topicspackages:
                            Generates/rewrites topicspackages,
                            packagetopics, authorpackages,
                            licensepackages, and yearpackages.
get_package_set()           Function get_package_set: Analyzes
                            dictionary 'packages' for name templates.
get_PDF_files(d)            Function get_PDF_files(d): Lists all PDF
                            files in a specified OS folder.
get_XML_files(d)            Function get_XML_files: Lists all XML files
                            in the current OS folder.
get_xyz_lap()               Function get_xyz_lap: Loads and analyzes
                            xyz.lap for author templates.
get_xyz_llp()               Function get_xyz_llp: Loads and analyzes
                            xyz.llp for liocense templates.
get_xyz_lpt()               Function get_xyz_lpt: Loads and analyzes
                            xyz.lpt for topic templates.
get_year_set()              Function get_package_set: Analyzes
                            dictionary 'yearpackages' for year templates.
load_XML_toc()              Function load_XML_toc(): Loads pickle file 2
                            (which contains XML_toc).
main()                      Function main(): Main Function (calls the
                            other functions).
make_statistics()           Function make_statistics(): Prints
                            statistics on terminal.
regenerate_pickle_files()   Function regenerate_pickle_files:
                            Regenerates corrupted pickle files.
set_PDF_toc()               set_PDF_toc: Fills PDF_toc on the basis of
                            XML_toc.
test_clipboard()            auxiliary function: Sents a program call
                            to clipboard.
verify_PDF_files()          Function verify_PDF_files: Checks actualized
                            PDF_toc/delete a PDF file if necessary.

see also:
--------
+ installation.txt
+ firststeps.txt
+ call.txt
+ wget.txt
+ CTAN-files.txt

+ CTANLoad-changes.txt
+ CTANLoad-examples.txt
+ CTANLoad-examples.bat
+ CTANLoad-functions.txt
+ CTANLoad-messages.txt
+ CTANLoad-modules.txt
+ CTANLoad.man
"""


# ==================================================================
# Imports

# 3.5    2026-07-02 data class used
# 3.5.0  2026-07-13 new module dataclasses
# 3.7    2026-07-13 backtracing
# 3.7.1  2026-07-13 new module traceback

import argparse                                                         # parse arguments
import os                                                               # delete a file on disk, for instance
from os import path                                                     # path informations
import pickle                                                           # read/write pickle data
import platform                                                         # get OS informations
import random                                                           # used for random integers
import re                                                               # handle regular expressions
import subprocess                                                       # handling of sub-processes
import sys                                                              # system calls
import time                                                             # used for random seed, time measurement
import xml.etree.ElementTree as ET                                      # XML processing
from threading import Thread                                            # handling of threads
import pyperclip3 as pc                                                 # writing to clipboard
from dataclasses import dataclass, field                                # Python data classes are used
import traceback                                                        # error backtracing  ---> modules


# ==================================================================
# Global settings

# ------------------------------------------------------------------
# The program

# 3.6    2026-07-05 ACT_PROGRAMNAME depends on OPERATINGSYS now

PRG_NAME        = "CTANLoad.py"
PRG_AUTHOR      = "Günter Partosch"
PRG_EMAIL       = "Guenter.Partosch@web.de;\nformerly:" + \
                  " Guenter.Partosch@hrz.uni-giessen.de"
PRG_VERSION     = "3.12"
PRG_DATE        = "2026-08-15"
PRG_INST        = "formerly: Justus-Liebig-Universität Gießen," +\
                  " Hochschulrechenzentrum"

OPERATINGSYS    = platform.system()                                     # actual operating system
call            = sys.argv
CALLEDPROGRAM   = sys.argv[0]                                           # name of called program
if OPERATINGSYS == "Windows":
    ACT_PROGRAMNAME = CALLEDPROGRAM.split("\\")[-1]
else:
    ACT_PROGRAMNAME = CALLEDPROGRAM.split("/")[-1]
PARAMETERS      = call[1:]                                              # all parts of call (with the xception of the first)
call[0]         = ACT_PROGRAMNAME                                       # actual name (with path) of the called program

# 2.24   2024-03-04 wget processor and subprocess timeout now
#                   configurable

WGET            = "wget2"                                               # wget processor
TIMEOUT_DEFAULT = 60                                                    # default for timeout in subprocess (in sec.)

EMPTY           = ""
BLANK           = " "

# ------------------------------------------------------------------
# Texts for argparse and help

# 2.54   2025-11-03 argparse texts revised

AUTHOR_TEMPLATE_TEXT  = "Author template for package XML files"
LICENSE_TEMPLATE_TEXT = "License template for package XML files"
KEY_TEMPLATE_TEXT     = "Key template for package XML files"
NAME_TEMPLATE_TEXT    = "Name template for package XML files"
YEAR_TEXT             = "Template for filtering on the base of years"

AUTHOR_TEXT           = "Author of the program"
VERSION_TEXT          = "Version of the program"
OUTPUT_TEXT           = "Generic file name for output files"
NUMBER_TEXT           = "Maximum number of file downloads"
DIREC_TEXT            = "Folder for output files in the OS"
PROGRAM_TEXT          = "Program loads XLM and PDF documentation " +\
                        "files from CTAN a/o generates some " +\
                        "special lists, and prepares data for CTANOut."
VERBOSE_TEXT          = "Flag: Output is verbose."
DOWNLOAD_TEXT         = "Flag: Downloads associated documentation " +\
                        "files [PDF]."
LISTS_TEXT            = "Flag: Generates some special lists " +\
                        "and prepare files for CTANOut."
STATISTICS_TEXT       = "Flag: Prints statistics."
INTEGRITY_TEXT        = "Flag: Checks the integrity of the " +\
                        "2nd .pkl file."
REGENERATE_TEXT       = "Flag: Regenerates the two pickle files."

# -----------------------------------------------------------------
# Defaults for argparse

DOWNLOAD_DEFAULT         = False                                        # default for option -f (no PDF download)
INTEGRITY_DEFAULT        = False                                        # default for option -c (no integrity check)
LISTS_DEFAULT            = False                                        # default for option -n (special lists are not generated)
NUMBER_DEFAULT           = 250                                          # default for option -n (maximum number of files to be loaded)
OUTPUT_NAME_DEFAULT      = "all"                                        # default for option -o (generic file name)
STATISTICS_DEFAULT       = False                                        # default for option -stat (no statistics output)
NAME_TEMPLATE_DEFAULT    = EMPTY                                        # default for option -t (name template for file loading)
AUTHOR_TEMPLATE_DEFAULT  = EMPTY                                        # default for option -A (author name template)
LICENSE_TEMPLATE_DEFAULT = EMPTY                                        # default for option -L (license name template)
KEY_TEMPLATE_DEFAULT     = EMPTY                                        # default for option -k (key template for file loading)
YEAR_TEMPLATE_DEFAULT    = """^19[89][0-9]|20[012][0-9]$"""             # default for option -y (year template [four digits])
VERBOSE_DEFAULT          = False                                        # default for option -n (output is not verbose)
REGENERATE_DEFAULT       = False                                        # default for option -r (no regeneration)
DEBUGGING_DEFAULT        = False                                        # default for option -dbg (no debugging)

ACT_DIREC           = "."
if OPERATINGSYS == "Windows":
    DIREC_SEP      = "\\"                                               
else:
    DIREC_SEP      = "/"
DIREC_DEFAULT       = ACT_DIREC + DIREC_SEP                             # default for -d (output OS folder)

# ------------------------------------------------------------------
# Settings for wget (authors, packages, topics)

CTANURL             = "https://ctan.org"                                # head of a CTAN url
CTANURL2            = CTANURL + "/tex-archive"                          # head of another CTAN url
CALL1               = "wget https://ctan.org/xml/2.0/"                  # base wget call for authors, packages, ...
CALL2               = "wget https://ctan.org/xml/2.0/pkg/"              # base wget call for package files
PARAMETER           = "?no-dtd=true --no-check-certificate -O "         # additional parameter for wget

# ------------------------------------------------------------------
# other settings

PKL_FILE            = "CTAN.pkl"                                        # name of 1st pickle file
PKL_FILE2           = "CTAN2.pkl"                                       # name of 2nd pickle file

ACT_DATE            = time.strftime("%Y-%m-%d")                         # actual date of program execution
ACT_TIME            = time.strftime("%X")                               # actual time of program execution

EXT                 = ".xml"                                            # file name extension for downloaded XML files
RNDG                = 2                                                 # optional rounding of float numbers
LEFT                = 35                                                # width of labels in statistics
ELLIPSE             = " ..."                                            # abbreviate texts

RESET_TEXT          = "[CTANLoad] Warning: '{0}' reset to {1} " +\
                      "(due to {2})"
EXCLUSION           = ["authors.xml", "topics.xml", "packages.xml",
                       "licenses.xml"]                                  # XML files which are not package files

random.seed(time.time())                                                # seed for random number generation


# ==================================================================
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
    c) access: ... dc_var.name_template ...
    """

    # 3.5    2026-07-02 data class used
    # 3.5.1  2026-07-02 new class dataclass-variable (including all
    #                   globally used variables) derfined
    # 3.5.2  2026-07-02 instance "dc_var" of this class created
    # 3.10   2026-08-05 correction in dataclass_variable: collections
    #                   with default factory

    # ------------------------------------------------------------------
    # variables/defaults for argparse
    author_template:str     = AUTHOR_TEMPLATE_DEFAULT                   # option -A    (author name template)
    debugging:bool          = DEBUGGING_DEFAULT                         # option -dbg  (debugging)
    direc:str               = DIREC_DEFAULT                             # option -d    (name of the OS directory)
    download:bool           = DOWNLOAD_DEFAULT                          # option -f    (no PDF download)
    integrity:bool          = INTEGRITY_DEFAULT                         # option -c    (no integrity check)
    key_template:str        = KEY_TEMPLATE_DEFAULT                      # option -k    (key template)
    license_template:str    = LICENSE_TEMPLATE_DEFAULT                  # option -L    (license name template)
    lists:bool              = LISTS_DEFAULT                             # option -n    (special lists are not generated)
    name_template:str       = NAME_TEMPLATE_DEFAULT                     # option -t    (name template for file loading)
    number:int              = NUMBER_DEFAULT                            # option -n    (maximum number of files to be loaded)
    output_name:str         = OUTPUT_NAME_DEFAULT                       # option -o    (generic file name)
    regenerate:bool         = REGENERATE_DEFAULT                        # option -r    (pickle files are to be regenerated)
    statistics:bool         = STATISTICS_DEFAULT                        # option -stat (no statistics output)
    verbose:bool            = VERBOSE_DEFAULT                           # option -v    (output is verbose)
    year_template:str       = YEAR_TEMPLATE_DEFAULT                     # option -y    (year template)

    # ------------------------------------------------------------------
    # other settings
    counter:int         = 0                                             # counter for downloaded XML files (in the actual session)
    pdfcounter:int      = 0                                             # counter for downloaded PDF files (in the actual session)
    pdfctrerr:int       = 0                                             # counter for not downloaded PDF files (in the actual session)
    corrected:int       = 0                                             # counter of corrected entries in XML_toc (in the actual session)
    ok:bool             = None                                          # global flag: status of processing
    no_error:bool       = None                                          # global flag: no error

    # ------------------------------------------------------------------
    # some other counters
    no_tp:int       = 0                                                 # number of packages selected per topics
    no_ap:int       = 0                                                 # number of packages selected per author names
    no_np:int       = 0                                                 # number of packages selected per n<mes
    no_lp:int       = 0                                                 # number of packages selected per licenses
    no_ly:int       = 0                                                 # number of packages selected per years
  
    # ------------------------------------------------------------------
    # Dictionaries, tuples and sets
    authorpackages:dict       = field(default_factory=dict)             # Python dictionary: list of authors and their packages
    licensepackages:dict      = field(default_factory=dict)             # Python dictionary: list of licenses and their packages
    authors:dict              = field(default_factory=dict)             # Python dictionary: list of authors
    packages:dict             = field(default_factory=dict)             # Python dictionary: list of packages
    licenses:dict             = field(default_factory=dict)             # Python dictionary: list of licenses
    packagetopics:dict        = field(default_factory=dict)             # Python dictionary: list of packages and their topics
    topics:dict               = field(default_factory=dict)             # Python dictionary: list of topics
    topicspackages:dict       = field(default_factory=dict)             # Python dictionary: list of topics and their packages
    yearpackages:dict         = field(default_factory=dict)             # Python dictionary: list of years and their packagesauthorpackage_file
    XML_toc:dict              = field(default_factory=dict)             # Python dictionary: list of PDF files:  XML_toc[href]=...PDF file
    PDF_toc:dict              = field(default_factory=dict)             # Python dictionary: list of PDF files: PDF_toc[lfn]=...package file
    PDF_notloaded:set         = field(default_factory=set)              # Python set: list of PDF files: PDF not downloaded
    not_well_formed:set       = field(default_factory=set)              # Python set: list of XML files: XML file not well-formed/EMPTY
    file_not_found:set        = field(default_factory=set)              # Python set: list of packages: XML file for package not found
    PDF_XML:set               = field(default_factory=set)              # Python set: list of XML files: inconsistencies with PDF files for packages
    all_XML_files:tuple       = field(default_factory=tuple)            # Python tuple: list with the names of all XML files
    selected_packages_lpt:set = field(default_factory=set)              # Python set: list of packages with selected topics
    selected_packages_lap:set = field(default_factory=set)              # Python set: list of packages with selected authors
    selected_packages_llp:set = field(default_factory=set)              # Python set: list of packages with selected licenses

    # ------------------------------------------------------------------
    def report(self, full:bool=False):
        """
        Outputs the current values of the variables defined in
        'dataclass_variable'.

        Parameter:
        ---------
        full : bool:
               if True, all menbers of sets, lists, tuples, and
               dictionaries, else only their lengths.
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
    # XML_toc
    #   Structure:                 XML_toc[href] = (XML file, key,
    #                              onename)
    #   generated and changed in:  analyze_XML_file(file),
    #                              check_integrity()
    #   inspected in:              analyze_XML_file(file),
    #                              check_integrity()
    #   stored in pickle file:     generate_pickle2()
    #   loaded from pickle file:   load_XML_toc()
    #
    # PDF_toc
    #   Structure:                 PDF_toc[fkey + "-" + onename] = file
    #   generated in:              get_PDF_files(d)
    #   changed in                 analyze_XML_file(file),
    #                              check_integrity()
    #   inspected in:              check_integrity()
    #
    # dc.authors: Python dictionary (sorted)
    #   each element: [author key]: <tuple with givenname and
    #                 familyname>
    #
    # dc.packages: Python dictionary (sorted)
    #   each element: [package key]: <tuple with package name and
    #                 package title>
    #
    # dc.licenses: Python dictionary (sorted)
    #   each element: [license key]: <license title>
    #
    # dc.topics: Python dictionary (sorted)
    #   each element: [topics name]: <topics title>
    #
    # dc.topicspackages: Python dictionary (unsorted)
    #   each element: [topic key]: <list with package names>
    #
    # dc.packagetopics: Python dictionary (sorted)
    #   each element: [topic key]: <list with package names>
    #
    # dc.authorpackages: Python dictionary (unsorted)
    #   each element: [author key]: <list with package names>
    #
    # dc.licensepackages: Python dictionary (mostly sorted)
    #   each element: [license key]: <list with package names>
    #
    # dc.yearpackages: Python dictionary
    #   each element: [year]: <list with package names>

    # 1st pickle file:
    #   name:      CTAN.pkl
    #   contains:  authors, packages, topics, licenses, topicspackages,
    #              packagetopics, authorpackages, licensepackages,
    #              yearpackages
    #
    # 2nd pickle file:
    #   name:      CTAN2.pkl
    #   contains:  XML_toc

# ------------------------------------------------------------------
dc_var = dataclass_variable()                                           # generate instance of dataclass_variable

# 3.5    2026-07-02 data class used
# 3.5.2  2026-07-02 instance "dc_var" of this class created


# ==================================================================
# argparse
# parse options and processes them

# 2.44   2024-07-26 argparse revised
# 2.44.1 2024-07-26 additional parameter in .ArgumentParser: prog, 
#                   epilog, formatter_class
# 2.44.2 2024-07-26 subdivision-groups by .add_argument_group
# 2.44.3 2024-07-26 additional arguments in .add_argument (if it makes 
#                   sense):type, metavar, action, dest
# 2.54   2025-11-03 argparse texts revised

parser = argparse.ArgumentParser(formatter_class = \
                                 argparse.RawDescriptionHelpFormatter,
                        prog = (PRG_NAME.split("."))[0],
                        description = f"{"%(prog)s"}\nVersion: "+\
                                 f"{PRG_VERSION} " +\
                                 f"({PRG_DATE})\n\n{PROGRAM_TEXT}",
                        epilog = "Thanks for using %(prog)s!",
                        )
parser._optionals.title   = 'Global options (without any processing)'

parser.add_argument("-a", "--author",                                   # Parameter -a/--author
                    help    = AUTHOR_TEXT,
                    action  = 'version',
                    version = PRG_AUTHOR + " (" + PRG_EMAIL + ", " + \
                    PRG_INST + ")")

parser.add_argument("-dbg", "--debugging",                              # Parameter -dbg/--debugging
                    help    = argparse.SUPPRESS,
                    action  = "store_true",
                    dest    = "debugging",
                    default = DEBUGGING_DEFAULT)

parser.add_argument("-stat", "--statistics",                            # Parameter -stat/--statistics
                    help    = STATISTICS_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store_true",
                    dest    = "statistics",
                    default = STATISTICS_DEFAULT)

parser.add_argument("-v", "--verbose",                                  # Parameter -v/--verbose
                    help    = VERBOSE_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store_true",
                    dest    = "verbose",
                    default = VERBOSE_DEFAULT)

parser.add_argument("-V", "--version",                                  # Parameter -V/--version
                    help    = VERSION_TEXT,
                    action  = 'version',
                    version = '%(prog)s ' + PRG_VERSION + \
                    " (" + PRG_DATE + ")")

group1 = parser.add_argument_group("Options related to loading")

group1.add_argument("-A", "--author_template",                          # Parameter -A/--author_template
                    metavar = "<author template>",
                    help    = AUTHOR_TEMPLATE_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store",
                    dest    = "author_template",
                    default = AUTHOR_TEMPLATE_DEFAULT)

group1.add_argument("-f", "--download_files",                           # Parameter -f/--download_files
                    help    = DOWNLOAD_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store_true",
                    dest    = "download_files",
                    default = DOWNLOAD_DEFAULT)

group1.add_argument("-k", "--key_template",                             # Parameter -k/--key_template
                    metavar = "<key template>",
                    help    = KEY_TEMPLATE_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store",
                    dest    = "key_template",
                    default = KEY_TEMPLATE_DEFAULT)

group1.add_argument("-d", "--directory",                                # Parameter -d/--directory (folder)
                    metavar = "<directory>",
                    help    = DIREC_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store",
                    dest    = "direc",
                    default = DIREC_DEFAULT)

group1.add_argument("-L", "--license_template",                         # Parameter -L/--license_template
                    metavar = "<license template>",
                    help    = LICENSE_TEMPLATE_TEXT + " -- Default: " \
                    + "%(default)s",
                    action  = "store",
                    dest    = "license_template",
                    default = LICENSE_TEMPLATE_DEFAULT)

group1.add_argument("-n", "--number",                                   # Parameter -n/--number
                    metavar = "<number>",
                    help    = NUMBER_TEXT+" -- Default: "+"%(default)s",
                    action  = "store",
                    dest    = "number",
                    type    = int,
                    default = NUMBER_DEFAULT)

group1.add_argument("-o", "--output",                                   # Parameter -o/--output
                    metavar = "<output>",
                    help    = OUTPUT_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store",
                    dest    = "output_name",
                    default = OUTPUT_NAME_DEFAULT)

group1.add_argument("-t", "--name_template",                            # Parameter -t/--name_template
                    metavar = "<name template>",
                    help    = NAME_TEMPLATE_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store",
                    dest    = "name_template",
                    default = NAME_TEMPLATE_DEFAULT)

group1.add_argument("-y", "--year_template",                            # Parameter -y/--year_template
                    metavar = "<year template>",
                    help    = YEAR_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store",
                    dest    = "year_template",
                    default = YEAR_TEMPLATE_DEFAULT)

group2 = parser.add_argument_group("Options for special actions")

group2.add_argument("-c", "--check_integrity",                          # Parameter -c/--check_integrity
                    help    = INTEGRITY_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store_true",
                    dest    = "check_integrity",
                    default = INTEGRITY_DEFAULT)

group2.add_argument("-l", "--lists",                                    # Parameter -l/--lists
                    help    = LISTS_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store_true",
                    dest    = "lists",
                    default = LISTS_DEFAULT)

group2.add_argument("-r", "--regenerate_pickle_files",                  # Parameter -r/--regenerate_pickle_files
                    help    = REGENERATE_TEXT + " -- Default: " + \
                    "%(default)s",
                    action  = "store_true",
                    dest    = "regenerate_pickle_files",
                    default = REGENERATE_DEFAULT)


#===================================================================
# Getting parsed values

# 3.5    2026-07-02 data class used
# 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
#                   and/or non-local with "dc_var"


args                    = parser.parse_args()                           # all the parameters of programm call

dc_var.author_template  = args.author_template                          # parameter -A
dc_var.license_template = args.license_template                         # parameter -L
dc_var.direc            = args.direc                                    # parameter -d
dc_var.download         = args.download_files                           # parameter -f
dc_var.integrity        = args.check_integrity                          # parameter -c
dc_var.key_template     = args.key_template                             # parameter -k
dc_var.lists            = args.lists                                    # parameter -l
dc_var.number           = int(args.number)                              # parameter -n
dc_var.regenerate       = args.regenerate_pickle_files                  # parameter -r
dc_var.statistics       = args.statistics                               # parameter -stat
dc_var.name_template    = args.name_template                            # parameter -k
dc_var.verbose          = args.verbose                                  # parameter -v
dc_var.year_template    = args.year_template                            # parameter -y
dc_var.debugging        = args.debugging                                # parameter -dbg


# ==================================================================
# more
# Correct OS folder name, test OS folder existence a/o install OS folder

# 2.49   2025-02-11 more f-strings
# 3.3    2026-05-08 print statements containing \+ have been simplified

dc_var.direc              = dc_var.direc.strip()                        # correct OS folder name (-d)
if dc_var.direc[len(dc_var.direc) - 1] != DIREC_SEP:
    dc_var.direc += DIREC_SEP
if not path.exists(dc_var.direc):
    try:
        os.mkdir(dc_var.direc)
    except OSError as err:
        print(f"[CTANLoad] Warning: Creation of the OS folder",
              f"'{dc_var.direc}' failed", err)
    else:
        print(f"[CTANLoad] Info: Successfully created the OS folder",
              f"'{dc_var.direc}' ")

dc_var.output_name        = dc_var.direc + args.output_name             # parameter -d


#===================================================================
# additional files, if you want to search topics a/a authors and their
# corresponding packages

topicpackage_file:str   = dc_var.output_name + ".lpt"                   # name of a the xyz.lpt file
authorpackage_file:str  = dc_var.output_name + ".lap"                   # name of a the xyz.lap file
licensepackage_file:str = dc_var.output_name + ".llp"                   # name of a the xyz.llp file


#===================================================================
# special regular expressions

p2           = re.compile(dc_var.name_template)                         # regular expression based on parameter -t
p3           = re.compile("^[0-9]{10}-.+[.]pdf$")                       # regular expression for local PDF file names
p4           = re.compile("^.+[.]xml$")                                 # regular expression for local XML file names
p5           = re.compile(dc_var.key_template)                          # regular expression for topics
p6           = re.compile(dc_var.author_template)                       # regular expression for author names
p7           = re.compile(dc_var.license_template)                      # regular expression for licenses
p9           = re.compile(dc_var.year_template)                         # regular expression
p10          = re.compile(YEAR_TEMPLATE_DEFAULT)                        # regular expression based on -y


#===================================================================
# Auxiliary function

# ------------------------------------------------------------------
def test_clipboard(dc=dc_var):                                          # auxiliary function test_clipboard()
    """
    Constructs a program call of CTANLoad.py and sents it to clipboard.

    The function works on the base of some special messages (file not
    found, not well-formed, ...)

    an installed xclip is required on linux systems.

    Parameter:
    ---------
    dc   instance of the data class  'dataclass_var'
         default: dc_var

    The function needs access to a variable in the data class dc:
    ------------------------------------------------------------
    dc.debugging   bool:
                   global flag: debugging enabled  

    Possible message:
    ----------------
    + Warning: An error occured
    """

    # 2.33   2024-03-05 test_clipboard() made more robust
    # 2.41   2024-03-25 test_clipboard: outputs an explanatory text to 
    #                   clipboard if there is nothing to do
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.4    2026-06-30 unspecified "except:" replaced by
    #                   "except Exception as err:"
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:test_clipboard")

    tmpset  = set()
    TMPSTR1 = 'python -u ctanload.py -t "'
    TMPSTR2 = '" -f -v -stat'
    tmpstr  = EMPTY
    tmpset  = dc.file_not_found | dc.not_well_formed | dc.PDF_XML       # union of sets
    TMPSTR3 = 'echo "Nothing to do"'
    
    for f in tmpset:                                                    # construct the chain for parameter -t
        if tmpstr == EMPTY: 
            tmpstr = f
        else:
            tmpstr += "$|^" + f
    try:                                                                # Construct the complete call
        if tmpstr != EMPTY:
            tmpstr = "^" + tmpstr + "$"
            pc.copy(TMPSTR1 + tmpstr + TMPSTR2)
        else:
            pc.copy(TMPSTR3)
    except Exception as err:
        print("""
"--- Warning: An error occured:
Nothing has been sent to clipboard.
Maybe, on Linux systems you have to install xclip before.""", err)

    if dc.debugging:
        print("+++ <CTANLoad:test_clipboard")

# ------------------------------------------------------------------
def fold(s:str) ->str:                                                  # auxiliary function fold()
    """
    auxiliary function: Shortens/foldens long option values for output.

    Parameter:
    ---------
    s (str): paragraph to be folded

    Returns:
    -------
    Returns a folded string.

    Messages:
    --------
    There are no specific messages.
    """

    OFFSET   = 64 * " "
    MAXLEN   = 70
    SEP      = "|"                                                      # separator for split
    parts    = s.split(SEP)                                             # split s on sep
    line:str = EMPTY
    out:str  = EMPTY
    
    for f in range(0, len(parts)):
        if f != len(parts) - 1:
            line = line + parts[f] + SEP
        else:
            line = line + parts[f]
        if len(line) >= MAXLEN:
            out  = out + line+ "\n" + OFFSET
            line = EMPTY
    out = out + line
    return out


# ==================================================================
# Functions for main part

# ------------------------------------------------------------------
def analyze_XML_file(file:str, dc=dc_var):                              # Function analyze_XML_file(file)
    """
    Analyzes a XML package file for documentation (PDF) files.

    Rewrites the variables dc.XML_toc and dc.PDF_toc in the data
    class dc.

    Parameters:
    ----------
    file (str): name of the XML file to be parsed/analyzed
                no default
    dc        : instance of the data class 'dataclass_var'
                default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.XML_toc          Python dictionary:
                        collection for XML files
    dc.PDF_toc          Python dictionary:
                        collection for PDF files
    dc.not_well_formed  Python list:
                        contains empty or not well-formed XML files
    dc.debugging        bool:
                        Flag: debugging enabled
    dc.verbose          bool:
                        global flag: output is verbose

    Call:
    ----
    + dload_document_file

    Possible messages:
    -----------------
    + Warning: local XML file '{0}' not found
    + Warning: local XML file for package '{0}' EMPTY or not well-formed
    """

    # 2.32   2024-03-05 in analyze_XML_file: addition to  the 
    #                   not_well_formed set corrected
    # 2.36   2024-03-15 in analyze_XML_file: exception handling extended
    #                   (parsing a XML file)
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.4    2026-06-30 unspecified "except:" replaced by
    #                   "except Exception as err:"
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:analyze_XML_file")

    error:bool = False

    try:                                                                # tries to open and parse a XML file
        f              = open(file, encoding="utf-8", mode="r")         # opens the XML file
        onePackage     = ET.parse(f)                                    # parses the XML file
        onePackageRoot = onePackage.getroot()                           # gets root
    except FileNotFoundError:                                           # file not found
        if dc.verbose:
            print(f"--- Warning: local XML file '{file}' not found")
    except Exception as err:                                                             # parsing not successfull
        if dc.verbose:
            print("---- Warning: local XML file for",
                  f"package '{file}' empty or not well-formed", err)
        error = True
        dc.not_well_formed.add(re.sub(".xml", EMPTY, file))             # appends name of file to the not_well_formed set

    if not error:
        ll           = list(onePackageRoot.iter("documentation"))       # all documentation elements == all documentation childs

        for g in ll:                                                    # loop: all documentation childs
            href = g.get("href", EMPTY)                                 # gets href attribute
            if ".pdf" in href:                                          # there is ".pdf" in the string ==> PDF file
                fnames  = re.split("/", href)                           # splits this string at "/"
                href2   = href.replace("ctan:/", CTANURL2)              # constructs the correct URL
                if href in dc.XML_toc:                                  # href allready used?
                    (tmp, fkey, onename) = dc.XML_toc[href]             # gets the components
                    onename = onename.replace("+", "-")
                else:                                                   # href not allready used?
                    onename = fnames[len(fnames) - 1]                   # gets the file name
                    fkey    = str(random.randint(1000000000,
                                                 9999999999))           # constructs a random file name
                    onename = onename.replace("+", "-")
                    dc.XML_toc[href] = (file, fkey, onename)            # stores this new file name
                if dc.download:
                    if dload_document_file(href2, fkey, onename, file): # loads the PDF document
                        dc.PDF_toc[fkey + "-" + onename] = file
        f.close()                                                       # closes the analyzed XML file

    if dc.debugging:
        print("+++ <CTANLoad:analyze_XML_file")

# ------------------------------------------------------------------
def call_check(dc=dc_var):                                              # Function call_check
    """
    Processes all necessary steps for a integrity check.

    Rewrites the variables dc.PDF_toc, dc.XML_toc, dc.authors,
    dc.licenses, dc.packages, dc.topics,  dc.topicspackages,
    dc.packagetopics, dc.number, dc.counter, dc.pdfcounter,
    dc.yearpackages in the data class dc.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.PDF_toc         Python dictionary:
                       for PDF files
    dc.XML_toc         Python dictionary:
                       for XML files
    dc.authors         Python dictionary:
                       collection with authors
    dc.licenses        Python dictionary:
                       collection with licenses
    dc.packages        Python dictionary:
                       collection with packages
    dc.topics          Python dictionary:
                       collection with topics
    dc.topicspackages  Python dictionary:
                       collection of topics and their corresponding packages
    dc.packagetopics   Python dictionary:
                       list of packages and their topics
    dc.number          int:
                       maximum number of files to be loaded
    dc.counter         int:
                       counter for downloadd XML and PDF files
    dc.pdfcounter      int:
                       counter for downloaded PDF files
    dc.yearpackages    Python dictionary:
                       list of years and their corresponding packages
    dc.debugging       bool:
                       Flag: debugging 

    Calls:
    -----
    + get_PDF_files
    + dload_topics
    + dload_authors
    + dload_licenses
    + dload_packages
    + generate_topicspackages
    + generate_pickle1
    + generate_lists
    + check_integrity

    Messages:
    --------
    There are no specific messages.
    """
    
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:call_check")

    get_PDF_files(dc.direc)                                             # gets a list with all the PDF files in direc
    dload_topics()                                                      # loads the file topics.xml
    dload_authors()                                                     # loads the file authors.xml
    dload_licenses()                                                    # load sthe file licenses.xml
    dload_packages()                                                    # loads the file packages.xml
    generate_topicspackages()                                           # Generates dc.topicspackages, ...

    thr3 = Thread(target=generate_pickle1)                              # dumps dc.authors, dc.packages, dc.topics, dc.licenses, dc.topicspackages, dc.packagetopics,
                                                                        # dc.authorpackages, dc.licensepackages, dc.yearpackages
    thr3.start()
    thr3.join()

    if dc.lists:                                                        # if lists are to be generated
        generate_lists()                                                # generates x.loa, x.lop, x.lok, x.lol, x.lpt, x.lap, x.llp

    if dc.integrity:                                                    # if the integrity is to be checked
        check_integrity()                                               # when indicated: remove files or entries

    if dc.debugging:
        print("+++ <CTANLoad:call_check")

# ------------------------------------------------------------------
def call_load(dc=dc_var):                                               # Function call_load
    """
    Processes all steps for a complete ctanload call (without integrity
    check).

    Rewrites the variables dc.PDF_toc, dc.XML_toc, dc.authors,
    dc.licenses, dc.packages,  dc.topics, dc.topicspackages, dc.number,
    dc.counter, dc.pdfcounter, dc.yearpackages, dc.no_tp, dc.no_ap,
    dc.no_np, dc.no_lp, dc.no_ly in the data class dc.

    Parameter:
    ---------
    dc   nstance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.PDF_toc          Python dictionary:
                        for PDF files
    dc.XML_toc          Python dictionary:
                        for XML files
    dc.authors          Python dictionary:
                        collection with authors
    dc.licenses         Python dictionary:
                        collection with licenses
    dc.packages         Python dictionary:
                        collection with packages
    dc.topics           Python dictionary:
                        collection with topics
    dc.topicspackages   Python dictionary:
                        collection of topics and their corresponding packages
    dc.number           int:
                        maximum number of files to be loaded
    dc.counter          int:
                        counter for downloadd XML and PDF files
    dc.pdfcounter       int:
                        counter for downloaded PDF files
    dc.yearpackages     Python dictionary:
                        list of years and their corr. packages
    dc.no_tp            int:
                        number of packages selected per topics
    dc.no_ap            int:
                        number of packages selected per author names
    dc.no_np            int:
                        number of packages selected per n<mes
    dc.no_lp            int:
                        number of packages selected per licenses
    dc.no_ly            int:
                        number of packages selected per years
    dc.debugging        bool:
                        global flag: debugging enabled
    dc.verbose          bool:
                        global flag: output is verbose

    Calls:
    -----
    +  get_PDF_files
    +  dload_topics
    +  dload_authors
    +  dload_licenses
    +  dload_packages
    +  load_XML_toc
    +  set_PDF_toc
    +  dload_XML_files
    +  generate_pickle1
    +  generate_pickle2
    +  get_xyz_lpt
    +  get_xyz_lap
    +  get_xyz_llp
    +  get_year_set
    
    Possible message:
    ----------------
    + Warning: no correct XML file for any specified package found
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:call_load")

    get_PDF_files(dc.direc)                                             # Lists all PDF files in a specified OS folder.
    load_XML_toc()                                                      # Loads pickle file 2 (which contains XML_toc)
    set_PDF_toc()

    dload_topics()                                                      # loads the file topics.xml
    dload_authors()                                                     # loads the file authors.xml
    dload_licenses()                                                    # loads the file licenses.xml
    dload_packages()                                                    # loads the file packages.xml
    generate_topicspackages()                                           # Generates dc.topicspackages, ...

    all_packages = set()                                                # initializes set
    for f in dc.packages:
        all_packages.add(f)                                             # constructs a set object (dc.packages has not the right format)

    tmp_tp = all_packages.copy()                                        # initializes tmp_tp (topics)
    tmp_ap = all_packages.copy()                                        # initializes tmp_ap (authors)
    tmp_np = all_packages.copy()                                        # initializes tmp_np (names)
    tmp_lp = all_packages.copy()                                        # initializes tmp_lp (licenses)
    tmp_ly = all_packages.copy()                                        # initializes tmp_ly (years)

    if (dc.name_template != NAME_TEMPLATE_DEFAULT):
        tmp_np = get_package_set()                                      # analyzes 'packages' for name templates
    if (dc.key_template != KEY_TEMPLATE_DEFAULT):
        tmp_tp = get_xyz_lpt()                                          # loads xyz.lpt and analyze it for key templates
    if (dc.author_template != AUTHOR_TEMPLATE_DEFAULT):
        tmp_ap = get_xyz_lap()                                          # loads xyz.lap and analyze it for author templates
    if (dc.license_template != LICENSE_TEMPLATE_DEFAULT):
        tmp_lp = get_xyz_llp()                                          # loads xyz.llp and analyze it for license templates
    if (dc.year_template != YEAR_TEMPLATE_DEFAULT):
        tmp_ly = get_year_set()                                         # looks for packages with the correct year templates

    tmp_pp = tmp_tp & tmp_ap & tmp_np & tmp_lp & tmp_ly                 # builts an set intersection
    if len(tmp_pp) == 0:
        if dc.verbose:
            print("--- Warning: no correct XML file for any specified",
                  "package found")

    tmp_p  = sorted(tmp_pp)                                             # builts an intersection

    dload_XML_files(tmp_p)                                              # loads and processe all required XML files in series

    dc.no_tp = len(tmp_tp)
    dc.no_ap = len(tmp_ap)
    dc.no_np = len(tmp_np)
    dc.no_lp = len(tmp_lp)
    dc.no_ly = len(tmp_ly)

    thr1 = Thread(target=generate_pickle2)                              # dumps dc.XML_toc via pickle file via thread
    thr1.start()
    thr1.join()
    thr2 = Thread(target=generate_pickle1)                              # dumps some lists to pickle file
    thr2.start()
    thr2.join()

    if dc.debugging:
        print("+++ <CTANLoad:call_load")

# ------------------------------------------------------------------
def call_plain(dc=dc_var):                                              # Function call_plain
    """
    Processes all steps for a plain call.

    Rewrtites the variables dc.PDF_toc, dc.authors, dc.licenses,
    dc.packages, dc.topics, dc.topicspackages, dc.packagetopics,
    dc.authorpackages, dc.yearpackages in the data class dc.

    Parameter:
    ---------
    dc   instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.PDF_toc          Python dictionary:
                        for PDF files
    dc.authors          Python dictionary:
                        collection with authors
    dc.licenses         Python dictionary:
                        collection with licenses
    dc.packages         Python dictionary:
                        collection with packages
    dc.topics           Python dictionary:
                        collection with topics
    dc.topicspackages   Python dictionary:
                        collection of topics and their corr. packages
    dc.packagetopics    Python dictionary:
                        list of packages and their corr. topics
    dc.authorpackages   Python dictionary:
                        list of authors and their corr. packages
    dc.yearpackages     Python dictionary:
                        list of years and their corr. packages
    dc.debugging        bool:
                        Flag: debugging 

    Calls:
    -----
    +  get_PDF_files
    +  dload_topics
    +  dload_authors
    +  dload_licenses
    +  dload_packages
    +  generate_topicspackages
       generate_pickle1
    
    Messages:
    --------
    There are no specific messages.
    """

    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:call_plain")

    get_PDF_files(dc.direc)                                             # Lists all PDF files in a specified OS folder.
    dload_topics()                                                      # loads the file topics.xml
    dload_authors()                                                     # loads the file authors.xml
    dload_licenses()                                                    # loads the file licenses.xml
    dload_packages()                                                    # loads the file packages.xml
    generate_topicspackages()                                           # generate dc.topicspackages, ...
    thr3 = Thread(target=generate_pickle1)                              # dumps authors, dc.packages, dc.topics, dc.licenses, dc.topicspackages,
                                                                        # dc.packagetopics, dc.authorpackages, dc.licensepackages, dc.yearpackages (via thread)
    thr3.start()
    thr3.join()

    if dc.debugging:
        print("+++ <CTANLoad:call_plain")

# ------------------------------------------------------------------
def check_integrity(always:bool=False, dc=dc_var):                      # Function check_integrity()
    """
    Checks integrity (tests for inconsistencies).

    Rewrites the variables dc.corrected, dc.PDF_toc, dc.no_error, dc.ok,
    dc.PDF_XML in the data class dc.

    Parameters:
    ---------_
    always (bool) : generation of pickle2 can be controlled
                    default: False   
    dc            : instance of the data class 'dataclass_var'
                    default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.corrected    int:
                    number of corrections
    dc.PDF_toc      Python dictionary:
                    structure: PDF_toc[file] = fkey + "-" + onename
    dc.no_error     bool:
                    Flag: no error
    dc.ok           bool:
                    global flag: status of processing
    dc.PDF_XML      Python set:
                    inconsistencies with PDF file
    dc.debugging    bool:
                    Flag: debugging enabled
    dc.verbose      bool:
                    global flag: output is verbose

    calls:
    -----
    + load_XML_toc
    + generate_pickle2
    + verify_PDF_filespossib
    
    Possible (error) messages:
    -------------------------
    + Warning: entry '{0}'
    + Warning: XML file '{0}' in OS deleted
    + Warning: entry '{0}' in dictionary deleted
    + Warning: entry '{0}' ({1}) in dictionary, but OS file is empty
    + Warning: entry '{0}' in dictionary, but OS file not found
    + Info: no error with integrity check
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.51   2025-09-02 check_integrity (-l): Show inconsistencies +
    #                   list of missing files
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:check_integrity")

    if dc.verbose:
        print("--- Info: integrity check")
    load_XML_toc()                                                      # loads the 2nd pickle file (dc.XML_toc) dc.XML_toc, struct ure: dc.XML_toc[href] = (file, fkey, onename)
    dc.no_error = True

    tmpdict = {}                                                        # for a copy of dc.XML_toc
    for f in dc.XML_toc:                                                # makes a copy of dc.XML_toc
        tmpdict[f] = dc.XML_toc[f]

# ..................................................................
    for f in tmpdict:                                                   # loop: all entries in a copy of XML_toc
        tmp:str    = tmpdict[f]
        f_name:str = (tmp[0].split("."))[0]                             # gets the name of the XML file (without extension)
        xlfn:str   = dc.direc + tmp[0]                                  # local file name for current XML file
        plfn:str   = dc.direc + tmp[1] + "-" + tmp[2]                   # local file name for current PDF file
        xex:str    = os.path.isfile(xlfn)                               # test: XLM file exists?
        pex:str    = os.path.isfile(plfn)                               # test: PDF file exists?

        if xex:                                                         # XLM file exists
            if os.path.getsize(xlfn) == 0:                              # but file is empty
                if dc.verbose:
                    print(f"----- Warning: entry '{xlfn}' ")
                os.remove(xlfn)                                         # OS file removed
                if dc.verbose:
                    print(f"----- Warning: XML file '{xlfn}'",
                          "in OS deleted")
                del dc.XML_toc[f]                                       # entry deleted
                if dc.verbose:
                    print(f"----- Warning: entry '{xlfn}'",
                          "in dictionary deleted")
                dc.no_error = False                                     # flag set
                dc.corrected += 1                                       # number of corrections increasedtuda-ci.xml
            else:                                                       # XML file not empty
                if os.path.isfile(plfn):                                # test: PDF file exists?
                    if os.path.getsize(plfn) != 0:
                        dc.PDF_toc[tmp[1] + "-" + tmp[2]] = tmp[0]      # generate entry in PDF_toc
                    else:
                        if dc.verbose:
                            print(f"----- Warning: entry '{plfn}' (",
                                  f"{tmp[0]}) in",
                                  "dictionary, but OS file is empty")
                        os.remove(plfn)                                 # OS file removed
                        if dc.verbose:
                            print(f"----- Warning: PDF file '{plfn}'",
                                  "in OS deleted")
                        del dc.XML_toc[f]                               # entry deleted
                        if dc.verbose:
                            print(f"----- Warning: entry '{plfn}'",
                                  "in dictionary")
                        dc.PDF_XML.add(f_name)
                        dc.no_error = False                             # flag set
                        dc.corrected += 1                               # number of correct increased
                else:
                    if dc.verbose:
                        print(f"----- Warning: entry '{plfn}'",
                              f"({tmp[0]}) in",
                              "dictionary but PDF file not found")
                    del dc.XML_toc[f]                                   # entry deleted
                    if dc.verbose:
                        print(f"----- Warning: entry '{plfn}' in",
                              "dictionary deleted")
                    dc.PDF_XML.add(f_name)
                    dc.no_error = False                                 # flag set
                    dc.corrected += 1                                   #  number of corr. increased
        else:                                                           # XML file does not exist
            print(f"----- Warning: entry '{xlfn}' in dictionary,",
                  "but OS file not found")
            del dc.XML_toc[f]                                           # entry deleted
            print(f"----- Warning: entry '{xlfn}'",
                  "in dictionary deleted")
            dc.no_error   = False                                       # flag set
            dc.corrected += 1                                           # number of corrections increased

    thr5 = Thread(target=verify_PDF_files)                              # check actualized PDF_toc; delete a PDF file if necessary (via thread)
    thr5.start()
    thr5.join()

# ..................................................................
    if dc.no_error and dc.ok and (not always):                          # there is no error
        if dc.verbose:
            print("----- Info: no error with integrity check")
    else:
        thr2 = Thread(target=generate_pickle2)                          # generate a new version of the 2nd pickle file (via thread)
        thr2.start()
        thr2.join()

    if dc.debugging:
        print("+++ <CTANLoad:check_integrity")

# ------------------------------------------------------------------
def dload_authors(dc=dc_var):                                           # Function dload_authors()
    """
    Downloads XML file 'authors' from CTAN and generates dictionary
    'authors'.

    Rewrites the dictionary dc.authors in the data class dc.

    Parameter:
    ---------
    dc  : instance of the data class 'dataclass_var'
          default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.authors    Python dictionary:
                  collection with authors
    dc.debugging  bool:
                  global flag: debugging enabled
    dc.verbose    bool:
                  global flag: output is verbose

    Possible (error) medssages:
    --------------------------
    + Info: XML file '{0}' downloaded ('{1}.xml' on PC)
    + Info: authors downloaded
    + Error: standard XML file '{0}' not found
    + Error: programm terminated
    + Error: standard XML file '{0}' empty or not well-formed
    + Error: XML file '{0}' not downloaded
    + Error; processor '{0}' not found
    """

    # 2.25   2024-03-04 Function dload_authors revised
    # 2.25.1 2024-03-04 parameters for wget and subprocess reorganized
    # 2.25.2 2024-03-04 parameters for wget now in a list
    # 2.25.3 2024-03-04 subprocess.Popen replaced by subprocess.run
    # 2.25.4 2024-03-04 subprocess.run additionally with check=True,
    #                   timeout=...
    # 2.25.5 2024-03-04 Exception handling extended
    # 2.34   2024-03-13 dload_topics, dload_authors, dload_licenses,
    #                   dload_packages revised
    # 2.34.1 2024-03-13 parameter -O and -P for wget corrected
    # 2.34.2 2024-03-13 exception handling revised
    # 2.45   2025-02-04 new error message
    # 2.45.1 2025-02-04 standard XML file '{0}' not found
    # 2.45.2 2025-02-04 standard XML file '{0}' not not well-formed
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.55   2025-12-12 subprocess.run calls revised 
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.4    2026-06-30 unspecified "except:" replaced by
    #                   "except Exception as err:"
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:dload_authors")

    FILE            = "authors"                                         # file name
    FILE2           = FILE + EXT                                        # file name (with extension)
    parameter_P:str = "-P" + dc.direc                                   # parameter -P for wget
    parameter_O:str = "-O" + FILE2                                      # parameter -O for wget
    CALL1           = "https://ctan.org/xml/2.0/"                       # base URL for authors, packages, ...
    callx:list      = [WGET, parameter_P,  parameter_O, CALL1 + FILE]   # command for subprocess.run

    try:                                                                # downloads file 'authors'
        # wget -P ./ -O authors.xml https://ctan.org/xml/2.0/authors
        process = subprocess.run(callx, check=True,
                                 timeout=TIMEOUT_DEFAULT,
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True)

        if dc.verbose:
            print(f"--- Info: XML file '{FILE}' downloaded",
                  f"('{dc.direc + FILE}.xml' on PC)")
        try:
            authorsTree  = ET.parse(FILE2)                              # parses the XML file 'authors.xml'
            authorsRoot  = authorsTree.getroot()                        # gets the root

            for child in authorsRoot:                                   # all children
                key:str   = EMPTY                                       # defaults
                id:str    = EMPTY
                fname:str = EMPTY
                gname:str = EMPTY
                for attr in child.attrib:                               # three attributes: id, givenname familyname
                    if str(attr) == "id":
                        key = child.attrib['id']                        # gets attribute id
                    if str(attr) == "givenname":
                        gname = child.attrib['givenname']               # gets attribute givenname
                    if str(attr) == "familyname":
                        fname = child.attrib['familyname']              # gets attribute familyname
                dc.authors[key] = (gname, fname)
            if dc.verbose:
                print("----- Info: authors downloaded")
        except FileNotFoundError as err:                                       # file not found
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}'",
                      "not found", err, traceback.print_exc())
            sys.exit("--- Error: programm terminated")                  # program terminated
        except Exception as err1:                                                         # parsing was not successfull
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}' empty",
                      "or not well-formed", err1, traceback.print_exc())
                print("--- Error:", sys.exc_info()[0], "\n   ",
                      sys.exc_info()[1])
            sys.exit("--- Error: programm terminated")                  # program terminated
    except subprocess.CalledProcessError as exc:                        # processor not found
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated
    except FileNotFoundError as exc:                                    # file not found / file not downloaded
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print(f"--- Error; processor '{WGET}' not found", exc,
                  traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated any unspecified error
        if dc.verbose:
            tmp_a = "    any unspecified error"
            print(f"--- Error: XML file '{FILE}' not",
                  f"downloaded\n{tmp_a}")
            print("--- ", sys.exc_info()[0])
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated

    if dc.debugging:
        print("+++ <CTANLoad:dload_authors")

# ------------------------------------------------------------------
def dload_document_file(href:str, key:str, name:str,
                        XML_file:str, dc=dc_var) ->bool:                # Function dload_document_file (href, key, name):
    """
    Downloads one information file (PDF) from CTAN.
    
    Rewrites the variables dc.pdfcounter, dc.pdfctrerr in the data
    class dc.

    Parameters:
    ----------
    href (str)     : URL of a document (PDF file)
                     no default
    key (str)      : key, dc.direc, name build the name of the new document
                     no default
    name (str)     : name of the PDF file
                     no default
    XML_file (str) : name of the XML file with href
                     no default
    dc             : instance of the data class 'dataclass_var'
                     default: dc_var

    Returns:
    -------
    Returns the status (bool) of the PDF download.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.pdfcounter       int:
                        counter for downloaded PDF files
    dc.pdfctrerr        int:
                        counter for not downloaded PDF files
                        (in the actual session)
    dc.PDF_notloaded    Python list:
                        PDF not downloaded
    dc.PDF_XML          Python set:
                        list of XML files: inconsistencies with PDF
                        files for packagessubprocess.run
    dc.debugging        bool:
                        global flag: debugging enabled
    dc.verbose          bool:
                        global flag: output is verbose

    Possible (error) messages:
    -------------------------
    + Info: PDF documentation file '{0}' downloaded
    + Info: unique local file name: '{0}'
    + Warning: PDF documentation file '{0}' not downloaded
    """

    # 2.28   2024-03-04 in dload_document_file: PDF_XML now in global
    #                   list
    # 2.31   2024-03-04 Function dload_document_file revised
    # 2.31.1 2024-03-04 parameters for wget and subprocess reorganized
    # 2.31.2 2024-03-04 parameters for wget now in a list
    # 2.31.3 2024-03-04 subprocess.Popen replaced by subprocess.run
    # 2.31.4 2024-03-04 subprocess.run additionally with check=True,
    #                   timeout=...
    # 2.31.5 2024-03-04 Exception handling extended
    # 2.38   2024-03-15 in dload_document_file: parameter -O and -P for 
    #                   wget corrected
    # 2.39   2024-03-17 in dload_document_file: error in URL building
    #                   corrected
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 2.55   2025-12-12 subprocess.run calls revised 
    # 3.2    2026-05-01 for XML and PDF files: downloads with number
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.4    2026-06-30 unspecified "except:" replaced by
    #                   "except Exception as err:"
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.7    2026-07-05 XML and PDF downloads: number of download
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ -CTANLoad:dload_document_file")

    # to be improved

    name:str        = name.replace("+", "-")
    CALL2           = "https://ctan.org/xml/2.0/pkg/"                   # base wget call for package files
    parameter_P:str = "-P" + dc.direc                                   # parameter -P for wget
    parameter_O:str = "-O" + key + "-" + name                           # parameter -O for wget

    call:list       = [WGET, parameter_P, parameter_O, href]
    noterror:bool   = False                                             # True if there is no error

    try:                                                                # downloads the PDF file and store
        process = subprocess.run(call, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 timeout=TIMEOUT_DEFAULT)
        if dc.verbose:
            print(f"------- Info: PDF documentation file '{name}'",
                  "downloaded")
            tmpxx = dc.direc + key + "-" + name
            print(f"------- (PDF {dc.pdfcounter + 1}) Info:",
                  f"unique local file name: '{tmpxx}'")
        dc.pdfcounter = dc.pdfcounter + 1                               # number of downloaded PDF files incremented
        noterror = True
    except FileNotFoundError as exc:                                    # file not found / file not downloaded
        dc.PDF_notloaded.add(name)                                      # appends name of file to the PDF_notloaded list
        dc.PDF_XML.add(re.sub(".xml", EMPTY, XML_file))
        if dc.verbose:
           print("------- Warning: PDF documentation",
                 f"file '{name}' not downloaded", exc)
    except subprocess.CalledProcessError as exc:                        # processor not found
        dc.PDF_notloaded.add(name)                                      # appends name of file to the PDF_notloaded list
        dc.PDF_XML.add(re.sub(".xml", EMPTY, XML_file))
        if dc.verbose:
            print("------- Warning: PDF documentation",
                  f"file '{name}' not downloaded", exc)
    except subprocess.TimeoutExpired as exc:                            # timeout
        dc.PDF_notloaded.add(name)                                      # append sname of file to the PDF_notloaded list
        dc.PDF_XML.add(re.sub(".xml", EMPTY, XML_file))
        if dc.verbose:
            print("------- Warning: PDF documentation",
                  f"file '{name}' not downloaded", exc)
    except Exception as err:                                                             # any unspecified error
        dc.PDF_notloaded.add(name)                                      # appends name of file to the PDF_notloaded list
        dc.PDF_XML.add(re.sub(".xml", EMPTY, XML_file))
        if dc.verbose:
            print("------- Warning: PDF documentation",
                  f"file '{name}' not downloaded", err)

    return noterror

# ------------------------------------------------------------------
def dload_licenses(dc=dc_var):                                          # Function dload_licenses
    """
    Downloads the'licenses' XML file from CTAN and generates the
    'dc.licenses' dictionary.

    Rewrites the variable dc.licenses in the data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.licenses   Python dictionary:
                  collection with licenses 
    dc.debugging  bool:
                  global flag: debugging enabled
    dc.verbose    bool:
                  global flag: output is verbose

    Possible (error) messages:
    -------------------------
    + Error: programm terminated
    + Error: standard XML file '{0}' empty or not well-formed
    + Error: standard XML file '{0}' not found
    + Error: XML file '{0}' not downloaded
    + Error: XML file '{0}' not downloaded\n{1} any unspecified error
    + Error: processor '{0}' not found
    + Info: XML file '{0}' downloaded ('{1}.xml' on PC)
    """

    # 2.26   2024-03-04 Function dload_licenses revised
    # 2.26.1 2024-03-04 parameters for wget and subprocess reorganized
    # 2.26.2 2024-03-04 parameters for wget now in a list
    # 2.26.3 2024-03-04 subprocess.Popen replaced by subprocess.run
    # 2.26.4 2024-03-04 subprocess.run additionally with check=True,
    #                   timeout=...
    # 2.26.5 2024-03-04 Exception handling extended
    # 2.34   2024-03-13 dload_topics, dload_authors, dload_licenses,
    #                   dload_packages revised
    # 2.34.1 2024-03-13 parameter -O and -P for wget corrected
    # 2.34.2 2024-03-13 exception handling revised
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 2.55   2025-12-12 subprocess.run calls revised 
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.4    2026-06-30 unspecified "except:" replaced by
    #                   "except Exception as err:"
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()
    # 3.9    2026-07-23 correction for not-existing key in licenses.xml

    if dc.debugging:
        print("+++ >CTANLoad:dload_licenses")

    FILE            = "licenses"                                        # file name
    FILE2           = FILE + EXT                                        # file name (with extension)
    parameter_P:str = "-P" + dc.direc                                   # parameter -P for wget
    parameter_O:str = "-O" + FILE2                                      # parameter -O for wget
    CALL1           = "https://ctan.org/xml/2.0/"                       # base URL for authors, packages, ...
    callx:list      = [WGET, parameter_P,  parameter_O, CALL1 + FILE]   # command for subprocess.run

    try:                                                                # Downloads file .../licenses
        process = subprocess.run(callx, check=True,
                                 timeout=TIMEOUT_DEFAULT,
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True)

        if dc.verbose:
            print(f"--- Info: XML file '{FILE}' downloaded",
                  f"('{dc.direc + FILE}.xml' on PC)")
        try:
            licensesTree   = ET.parse(FILE2)                            # parses the XML file 'topics.xml'
            licensesRoot   = licensesTree.getroot()                     # gets the root

            for child in licensesRoot:                                  # all children in 'licenses'
                key:str  = EMPTY                                        # defaults
                name:str = EMPTY
                free:str = EMPTY
                for attr in child.attrib:                               # three attributes: key, name, free
                    if str(attr) == "key":
                        key = child.attrib['key']                       # gets attribute key
                    elif str(attr) == "name":
                        name = child.attrib['name']                     # gets attribute name
                    elif str(attr) == "free":
                        free = child.attrib['free']                     # gets attribute free
                dc.licenses[key] = (name, free)
            dc.licenses["noinfo"]      = ("noinfo", EMPTY)              # correction; not in lincenses.xml
            dc.licenses["collection"]  = ("collection", EMPTY)          # correction; not in lincenses.xml
            dc.licenses["digest"]      = ("digest", EMPTY)              # correction; not in lincenses.xml
            dc.licenses["lppl1.1"]     = ("The LaTeX Project " +\
                                         "Public License 1.1", EMPTY)   # correction; not in lincenses.xml
            # <license key="lppl1.2" name="The LaTeX Project Public License 1.2" free="true" />
            if dc.verbose:
                print("----- Info: licenses downloaded")
        except FileNotFoundError as err:                                       # file not found
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}'",
                      "not found", err, traceback.print_exc())
            sys.exit("--- Error: programm terminated")                  # program terminated
        except Exception as err:                                        # parsing was not successfull
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}' empty",
                      "or not well-formed", err)
                print("--- Error:", sys.exc_info()[0], "\n   ",
                      sys.exc_info()[1])
            sys.exit("--- Error: programm terminated")                  # program terminated
    except subprocess.CalledProcessError as exc:                        # processor not found
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated
    except FileNotFoundError as exc:                                    # file not found / file not downloaded
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print(f"--- Error; processor '{WGET}' not found")
        sys.exit("[CTANLoad] Error: programm terminated", exc,
                 traceback.print_exc())                                 # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated any unspecified error
        if dc.verbose:
            tmp_a = "    any unspecified error"
            print(f"--- Error: XML file '{FILE}'",
                  f"not downloaded\n{tmp_a}")
            print("--- ", sys.exc_info()[0])
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated

    if dc.debugging:
        print("+++ <CTANLoad:dload_licenses")

# ------------------------------------------------------------------
def dload_packages(dc=dc_var):                                          # Function dload_packages
    """
    Downloads XML file 'packages' from CTAN and generates dictionary
    'packages'.

    Rewrites the dictionary dc.packages in the data class dc..

    Parameter:
    ---------
    dc  : instance of the data class 'dataclass_var'
          default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.packages   Python dictionary:
                  collection with packages
    dc.debugging  bool:
                  global flag: debugging enabled
    dc.verbose    bool:
                  global flag: output is verbose

    Possible error messages:
    -----------------------
    + Error: processor '{0}' not found
    + Error: programm terminated
    + Error: standard XML file '{0}' empty or not well-formed
    + Error: standard XML file '{0}' not found
    + Error: XML file '{0}' not downloaded
    + Error: XML file '{0}' not downloaded {1} any unspecified error
    """

    # 2.27   2024-03-04 Function dload_packages revised
    # 2.27.1 2024-03-04 parameters for wget and subprocess reorganized
    # 2.27.2 2024-03-04 parameters for wget now in a list
    # 2.27.3 2024-03-04 subprocess.Popen replaced by subprocess.run
    # 2.27.4 2024-03-04 subprocess.run additionally with check=True,
    #                   timeout=...
    # 2.27.5 2024-03-04 Exception handling extended
    # 2.34   2024-03-13 dload_topics, dload_authors, dload_licenses,
    #                   dload_packages revised
    # 2.34.1 2024-03-13 parameter -O and -P for wget corrected
    # 2.34.2 2024-03-13 exception handling revised
    # 2.45   2025-02-04 new error message
    # 2.45.1 2025-02-04 standard XML file '{0}' not found
    # 2.45.2 2025-02-04 standard XML file '{0}' not not well-formed
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 2.55   2025-12-12 subprocess.run calls revised 
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.4    2026-06-30 unspecified "except:" replaced by
    #                   "except Exception as err:"
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:dload_packages")

    FILE            = "packages"                                        # file name
    FILE2           = FILE + EXT                                        # file name (with extension)
    parameter_P:str = "-P" + dc.direc                                   # parameter -P for wget
    parameter_O:str = "-O" + FILE2                                      # parameter -O for wget
    CALL1           = "https://ctan.org/xml/2.0/"                       # base URL for authors, packages, ...
    callx:list      = [WGET, parameter_P,  parameter_O, CALL1 + FILE]

    try:                                                                # Loads file .../packages
        process = subprocess.run(callx, check=True,
                                 timeout=TIMEOUT_DEFAULT,
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True)

        if dc.verbose:
            print(f"--- Info: XML file '{FILE}' downloaded",
                  f"('{dc.direc + FILE}.xml' on PC)")
        try:                                                            # parses 'packages' tree
            packagesTree = ET.parse(FILE2)                              # parses the XML file 'packages.xml'
            packagesRoot = packagesTree.getroot()                       # gets the root

            for child in packagesRoot:                                  # all children in 'packages'
                key:str     = EMPTY                                     # defaults
                name:str    = EMPTY
                caption:str = EMPTY
                for attr in child.attrib:                               # three attributes: key, name, caption
                    if str(attr) == "key":
                        key = child.attrib['key']                       # gets attribute key
                    if str(attr) == "name":
                        name = child.attrib['name']                     # gets attribute name
                    if str(attr) == "caption":
                        caption = child.attrib['caption']
                                                                        # gets attribute caption
                dc.packages[key] = (name, caption)
            if dc.verbose:
                print("----- Info: packages downloaded")
        except FileNotFoundError as err:                                       # file not found
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}'",
                      "not found", err, traceback.print_exc())
            sys.exit("--- Error: programm terminated")                  # program terminated
        except Exception as err:                                                         # parsing was not successfull
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}' empty",
                      "or not well-formed", err)
                print("--- Error:", sys.exc_info()[0], "\n   ",
                      sys.exc_info()[1])
            sys.exit("--- Error: programm terminated")                  # program terminated
    except subprocess.CalledProcessError as exc:                        # processor not found
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated
    except FileNotFoundError as exc:                                    # file not found / file not downloaded
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print(f"--- Error; processor '{WGET}' not found")
        sys.exit("[CTANLoad] Error: programm terminated", exc,
                 traceback.print_exc())                                 # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated
    except Exception as err1:                                                             # any unspecified error
        if dc.verbose:
            tmp_a = "    any unspecified error"
            print(f"--- Error: XML file '{FILE}' not",
                  f"downloaded\n{tmp_a}", err1, traceback.print_exc())
            print("--- ", sys.exc_info()[0])
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated

    if dc.debugging:
        print("+++ <CTANLoad:dload_packages")

# ------------------------------------------------------------------
def dload_topics(dc=dc_var):                                            # Function dload_topics()
    """
    Downloads XML file 'topics' from CTAN and generates the
    'dc.topics' dictionary.

    Rewrites the dictionary dc.topics in the data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.topics     Python dictionary:
                  collection with topics
    dc.debugging  bool:
                  global flag: debugging enabled
    dc.verbose    bool:
                  global flag: output is verbose

    Possible error messages:
    -----------------------
    + Error: processor '{0}' not found
    + Error: programm terminated
    + Error: standard XML file '{0}' empty or not well-formed
    + Error: standard XML file '{0}' not found
    + Error: XML file '{0}' not downloaded
    + Error: XML file '{0}' not downloaded {1} any unspecified error
    """

    # 2.28   2024-03-04 Function dload_topics revised
    # 2.28.1 2024-03-04 parameters for wget and subprocess reorganized
    # 2.28.2 2024-03-04 parameter for wget now in a list
    # 2.28.3 2024-03-04 subprocess.Popen replaced by subprocess.run
    # 2.28.4 2024-03-04 subprocess.run additionally with check=True,
    #                   timeout=...
    # 2.28.5 2024-03-04 Exception handling extended
    # 2.34   2024-03-13 dload_topics, dload_authors, dload_licenses,
    #                   dload_packages revised
    # 2.34.1 2024-03-13 parameter -O and -P for wget corrected
    # 2.34.2 2024-03-13 exception handling revised
    # 2.45   2025-02-04 new error message
    # 2.45.1 2025-02-04 standard XML file '{0}' not found
    # 2.45.2 2025-02-04 standard XML file '{0}' not not well-formed
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 2.55   2025-12-12 subprocess.run calls revised 
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:dload_topics")

    FILE            = "topics"                                          # file name
    FILE2           = FILE + EXT                                        # file name (with extension)
    parameter_P:str = "-P" + dc.direc                                   # parameter -P for wget
    parameter_O:str = "-O" + FILE2                                      # parameter -O for wget
    CALL1           = "https://ctan.org/xml/2.0/"                       # base URL for authors, packages, ...
    callx:list      = [WGET, parameter_P,  parameter_O, CALL1 + FILE]

    try:                                                                # Loads file .../topics
        process = subprocess.run(callx, check=True,
                                 timeout=TIMEOUT_DEFAULT,
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True)

        if dc.verbose:
            print(f"--- Info: XML file '{FILE}' downloaded",
                  f"('{dc.direc + FILE}.xml' on PC)")
        try:
            topicsTree   = ET.parse(FILE2)                              # parses the XML file 'topics.xml'
            topicsRoot   = topicsTree.getroot()                         # gets the root

            for child in topicsRoot:                                    # all children in 'topics'
                key:str     = EMPTY                                     # defaults
                name:str    = EMPTY
                details:str = EMPTY
                for attr in child.attrib:                               # two attributes: name, details
                    if str(attr) == "name":
                        key = child.attrib['name']                      # gets attribute name
                    if str(attr) == "details":
                        details = child.attrib['details']               # gets attribute details
                dc.topics[key] = details
            if dc.verbose:
                print("----- Info: topics downloaded")
        except FileNotFoundError as err:                                # file not found
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}'",
                      "not found", err, traceback.print_exc())
            sys.exit("--- Error: programm terminated")                  # program terminated
        except Exception as err:                                        # parsing was not successfull
            if dc.verbose:
                print(f"--- Error: standard XML file '{FILE2}' empty",
                      "or not well-formed", err, traceback.print_exc())
                print("--- Error:", sys.exc_info()[0], "\n   ",
                      sys.exc_info()[1])
            sys.exit("--- Error: programm terminated")                  # program terminated
        dc.topics["norsk"] = "Nynorsk"                                  # Emergency entry !!!!
    except subprocess.CalledProcessError as exc:                        # processor not found
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated
    except FileNotFoundError as exc:                                    # file not found / file not downloaded
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print(f"--- Error; processor '{WGET}' not found", exc,
                 traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        if dc.verbose:
            print(f"--- Error: XML file '{FILE}' not downloaded")
            print("--- Error:", exc, traceback.print_exc())
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated any unspecified error
        if dc.verbose:
            tmp_a = "    any unspecified error"
            print(f"--- Error: XML file '{FILE}' not",
                  "downloaded\n{tmp_a}")
            print("--- ", sys.exc_info()[0])
        sys.exit("[CTANLoad] Error: programm terminated")               # program terminated

    if dc.debugging:
        print("+++ <CTANLoad:dload_topics")

# ------------------------------------------------------------------
def dload_XML_files(p:list, dc=dc_var):                                 # Function dload_XML_files
    """
    Downloads XML package files.

    Rewrites the variables dc.topicspackages, dc.number, dc.counter,
    dc.pdfcounter, dc.yearpackages in the data class dc.

    Parameters:
    ---------
    p (list) : names of packages a/o selected_packages
               no default
    dc       : instance of the data class 'dataclass_var'
               default: dc_var

    The function needs access to some var iables in the data class dc:
    -----------------------------------------------------------------
    dc.topicspackages  Python dictionary:
                       collection of topics and their corresponding
                       packages
    dc.number          int::
                       maximum number of files to be loaded
    dc.counter         int:
                       counter for downloadd XML and PDF files
    dc.pdfcounter      int:
                       counter for downloaded PDF files
    dc.yearpackages    Python dictionary:
                       list of years and their corresponding packages
    dc.debugging       bool:
                       global flag: debugging enabled
    dc.verbose         bool:
                       global flag: output is verbose

    Call:
    ----
    + analyze_XML_file

    Possible messages:
    -----------------
    + Info: XML file for package '{0}' downloaded ('{1}.xml' on PC)
    + Warning: maximum number ({0}) of downloaded XML+PDF files
               exceeded
    + Warning: processor '{0}' not found
    + Warning: XML file '{0}' not downloaded
    """

    # 2.30   2024-03-04 Function dload_XML_files revised
    # 2.30.1 2024-03-04 parameters for wget and subprocess reorganized
    # 2.30.2 2024-03-04 parameters for wget now in a list
    # 2.30.3 2024-03-04 subprocess.Popen replaced by subprocess.run
    # 2.30.4 2024-03-04 subprocess.run additionally with check=True,
    #                   timeout=...
    # 2.30.5 2024-03-04 Exception handling extended
    # 2.35   2024-03-15 in dload_XML_files: parameter -O and -P for wget
    #                   corrected
    # 2.37   2024-04-15 in dload_XML_files: exception handling revised
    #                   (downloading a XML file)
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 2.55   2025-12-12 subprocess.run calls revised 
    # 3.1    2026-04-15 in dload_XML_files: better handling with
    #                   processor error (and other exceptions)
    # 3.2    2026-05-01 for XML and PDF files: downloads with number
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.7    2026-07-05 XML and PDF downloads: number of download
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:dload_XML_files")

    CALL2           = "https://ctan.org/xml/2.0/pkg/"                   # base URL for package files
    parameter_P:str = "-P" + dc.direc                                   # parameter -P for wget

    for f in p:                                                         # all packages found in 'packages'
        if p2.match(f) and (dc.counter + dc.pdfcounter < dc.number):    # file name matches name_template
            dc.counter  = dc.counter + 1                                # ioncrement counter
            parameter_O = "-O" + f + EXT                                # parameter -O for wget
            file        = f

            callx = [WGET, parameter_O, parameter_P, CALL2 + f]         # wget  -O xyz.xml -P  .\direc https://ctan.org/xml/2.0/pkg/xyz

            try:                                                        # tries to download a XML file (packages)
                process = subprocess.run(callx, check=True,
                                         timeout=TIMEOUT_DEFAULT,
                                         stderr=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         universal_newlines=True)

                if dc.verbose:
                    print(f"----- Info: (XML {dc.counter})",
                          "XML file for package",
                          f"'{f}' downloaded ('{dc.direc + f}.xml' on PC)")
                analyze_XML_file(f + EXT)                               # if download is set: analyze the associated XML file
            except FileNotFoundError as exc:                            # file not found /  file not downloaded
                if dc.verbose:
                    print(f"--- Warning: XML file '{file}' not",
                          "downloaded")
                    print(f"--- Warning: processor '{WGET}' not found",
                          exc)
            except subprocess.CalledProcessError as exc:                # processor not found
                if dc.verbose:
                    print(f"--- Warning: XML file '{file}' not",
                          "downloaded")
                    print("--- Warning:", exc)
            except subprocess.TimeoutExpired as exc:                    # timeout
                if dc.verbose:
                    print(f"--- Warning: XML file '{file}' not",
                          "downloaded")
                    print("--- Warning:", exc)
            except Exception as exc:                                    # any unspecified error
                if dc.verbose:
                    tmp_a = "    any unspecified error"
                    print(f"--- Warning: XML file '{file}' not",
                          f"downloaded\n{tmp_a}", exc)
                    print("--- ", sys.exc_info()[0])

    if dc.counter + dc.pdfcounter >= dc.number:                         # limit for downloaded files
        if dc.verbose:
            print("--- Warning: maximum number",
                  f"({str(dc.counter + dc.pdfcounter)})",
                  "of downloaded XML+PDF files exceeded")

    if dc.debugging:
        print("+++ <CTANLoad:dload_XML_files")

# ------------------------------------------------------------------
def generate_lists(dc=dc_var):                                          # Function generate_lists
    """
    Generates some special files (with lists).
    
    generates xyz.loa file (list of authors)
    generates xyz.lop file (list of packages)
    generates xyz.lok file (list of topics)
    generates xyz.lol file (list of licenses)
    generates xyz.lpt file (list of topics and associated packages)
    generates xyz.lap file (list of authors and associated packages)
    generates xyz.llp file (list of licenses and associated packages).

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging        bool:
                        global flag: debugging enabled
    dc.verbose          bool:
                        global flag: output is verbose
    dc.authorpackages   Python dictionary:
                        list of authors and their corresponding packages
    dc.authors          Python dictionary:
                        collection with authors
    dc.licensepackages  Python dictionary:
                        list of licenses and their corresponding packages
    dc.licenses         Python dictionary:
                        collection with licenses
    dc.output_name	str:
	                generic file name for output files
    dc.packages         Python dictionary:
                        collection with packages
    dc.topics           Python dictionary:
                        collection with topics
    dc.topicspackages   Python dictionary:
                        collection of topics and their corresponding packages
 
    Possible messages:
    -----------------
    + Info: file '<file>' (list of authors and associated packages)
            generated
    + Info: file '<file>' (list of authors) generated
    + Info: file '<file>' (list of licenses and associated packages)
            generated
    + Info: file '<file>' (list of licenses) generated
    + Info: file '<file>' (list of packages) generated
    + Info: file '<file>' (list of topics and associated packages)
            generated
    + Info: file '<file>' (list of topics) generated
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:generate_lists")

    # .................................................
    # generate xyz.loa file (list of authors)                           xyz.loa

    loa_file = dc.output_name + ".loa"

    loa = open(loa_file, encoding="utf-8", mode="w")                    # opens xyz.loa file
    for f in dc.authors:                                                # loop
        loa.write(str(dc.authors[f]) + "\n")

    if dc.verbose:
        print(f"--- Info: file '{loa_file}'",
              "(list of authors) generated")
    loa.close()                                                         # closes xyz.loa file

    # .................................................
    # generate xyz.lop file (list of packages)                          xyz.lop

    lop_file = dc.output_name + ".lop"

    lop = open(lop_file, encoding="utf-8", mode="w")                    # opens xyz.lop file
    for f in dc.packages:                                               # loop
        lop.write(str(dc.packages[f]) + "\n")

    if dc.verbose:
        print(f"--- Info: file '{lop_file}' (list of packages)",
              "generated")
    lop.close()                                                         # closes xyz.lop file

    # .................................................
    # generate xyz.lok file (list of topics)                            xyz.lok

    # 2.40   2024-03-25 generation of xyz.lok, xyz.lol, xyz.lpt, 
    #                   xyz.lap, xyz.llp corrected a/o improved

    lok_file = dc.output_name + ".lok"

    lok = open(lok_file, encoding="utf-8", mode="w")                    # opens xyz.lok file
    for f in dc.topics:                                                 # loop
        tmp = (f, dc.topics[f])
        lok.write(str(tmp) + "\n")

    if dc.verbose:
        print(f"--- Info: file '{lok_file}' (list of topics) generated")
    lok.close()                                                         # closes xyz.lok file

    # .................................................
    # generate xyz.lol file (list of licenses)                          xyz.lol

    # 2.40   2024-03-25 generation of xyz.lok, xyz.lol, xyz.lpt, 
    #                   xyz.lap, xyz.llp corrected a/o improved

    lol_file = dc.output_name + ".lol"

    lol = open(lol_file, encoding="utf-8", mode="w")                    # opens xyz.lol file
    for f in dc.licenses:                                               # loop
        tmp = (f, dc.licenses[f])
        lol.write(str(tmp) + "\n")

    if dc.verbose:
        print(f"--- Info: file '{lol_file}' (list of licenses)",
              "generated")
    lol.close()                                                         # closes xyz.lol file

    # .................................................
    # generate xyz.lpt file (list of topics and associated packages)    xyz.lpt

    # 2.40   2024-03-25 generation of xyz.lok, xyz.lol, xyz.lpt, 
    #                   xyz.lap, xyz.llp corrected a/o improved

    lpt_file = dc.output_name + ".lpt"

    lpt = open(lpt_file, encoding="utf-8", mode="w")                    # open xyz.lpt file
    for f in dc.topicspackages:                                         # loop
        tmp =(f, dc.topicspackages[f])
        lpt.write(str(tmp) + "\n")

    if dc.verbose:
        print(f"--- Info: file '{lpt_file}' (list of topics and",
              "associated packages) generated")
    lpt.close()                                                         # closes xyz.lpt file

    # .................................................
    # generate xyz.lap file (list of authors and associated packages)   xyz.lap

    # 2.40   2024-03-25 generation of xyz.lok, xyz.lol, xyz.lpt, 
    #                   xyz.lap, xyz.llp corrected a/o improved

    lap_file = dc.output_name + ".lap"

    lap = open(lap_file, encoding="utf-8", mode="w")                    # opens xyz.lap file
    for f in dc.authorpackages:                                         # loop
        tmp = (f, dc.authorpackages[f])
        lap.write(str(tmp) + "\n")

    if dc.verbose:
        print(f"--- Info: file '{lap_file}' (list of authors and",
              "associated packages) generated")
    lap.close()                                                         # closes xyz.lap file

    # .................................................
    # generate xyz.llp file (list of licenses and associated packages)

    # 2.40   2024-03-25 generation of xyz.lok, xyz.lol, xyz.lpt, 
    #                   xyz.lap, xyz.llp corrected a/o improved

    llp_file = dc.output_name + ".llp"

    llp = open(llp_file, encoding="utf-8", mode="w")                    # open xyz.llp file
    for f in dc.licensepackages:                                        # loop
        tmp = (f, dc.licensepackages[f])
        llp.write(str(tmp) + "\n")

    if dc.verbose:
        print(f"--- Info: file '{llp_file}' (list of licenses and",
              "associated packages) generated")
    llp.close()                                                         # closes xyz.llp file

    if dc.debugging:
        print("+++ <CTANLoad:generate_lists")

# ------------------------------------------------------------------
def generate_pickle1(dc=dc_var):                                        # Function generate_pickle1
    """
    Performs a pickle dump.

    Dumps the actual versions of dc.authors, dc.packages, dc.licenses,
    dc.topics, dc.topicspackages, dc.packagetopics, dc.licensepackages,
    dc.yearpackages

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging        bool:
                        global flag: debugging enabled
    dc.verbose          bool:
                        global flag: output is verbose
    dc.authors          Python dictionary:
                        collection with authors
    dc.packages         Python dictionary:
                        collection with packages
    dc.licenses         Python dictionary:
                        collection with licenses
    dc.topics           Python dictionary:
                        collection with topics
    dc.topicspackages   Python dictionary:
                        collection of topics and their corresponding packages
    dc.packagetopics    Python dictionary:
                        list of packages and their topics
    dc.authorpackages   Python dictionary:
                        list of authors and their corresponding packages
    dc.licensepackages  Python dictionary:
                        list of licenses and their corresponding packages
    dc.yearpackages     Python dictionary:
                        list of years and their corresponding packages
    dc.direc      	str:
                  	name of the OS directory

    Possible (error) messages:
    -------------------------
    + Info: pickle file '{0}' written
    + Warning: pickle file '{0}' cannot be loaded a/o written
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:generate_pickle1")

    # dc.authors: Python dictionary (sorted)
    #   each element: [author key]: <tuple with givenname and
    #                 familyname>
    #
    # dc.packages: Python dictionary (sorted)
    #   each element: [package key]: <tuple with package name and
    #                 package title>
    #
    # dc.licenses: Python dictionary (sorted)
    #   each element: [license key]: <license title>
    #
    # dc.topics: Python dictionary (sorted)
    #   each element: [topics name]: <topics title>
    #
    # dc.topicspackages: Python dictionary (unsorted)
    #   each element: [topic key]: <list with package names>
    #
    # dc.packagetopics: Python dictionary (sorted)
    #   each element: [topic key]: <list with package names>
    #
    # dc.authorpackages: Python dictionary (unsorted)
    #   each element: [author key]: <list with package names>
    #
    # dc.licensepackages: Python dictionary (mostly sorted)
    #   each element: [license key]: <list with package names>
    #
    # dc.yearpackages: Python dictionary
    #   each element: [year]: <list with package names>

    pickle_name1  = dc.direc + PKL_FILE                                 # path of the pickle file
    
    try:
        pickle_file1  = open(pickle_name1, "bw")                        # opens the pickle file
        pickle_data1  = (dc.authors, dc.packages, dc.topics,
                         dc.licenses, dc.topicspackages,
                         dc.packagetopics, dc.authorpackages,
                         dc.licensepackages, dc.yearpackages)
        pickle.dump(pickle_data1, pickle_file1)                         # dumps the data
        pickle_file1.close()                                            # closes the file
        if dc.verbose:
            print(f"--- Info: pickle file '{pickle_name1}' written")
    except Exception as exc:
        if dc.verbose:
            print(f"--- Warning: pickle file '{pickle_name1}' cannot",
                  "be loaded a/o written", exc)

    if dc.debugging:
        print("+++ <CTANLoad:generate_pickle1")

# ------------------------------------------------------------------
def generate_pickle2(dc=dc_var):                                        # Function generate_pickle2
    """
    Performs a pickle dump.

    Needs actual variable dc.XML_toc in the data class dc:
    
    dc.XML_toc  list with download information files

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  bool:
                  global flag: debugging enabled
    dc.verbose    bool:
                  global flag: output is verbose

    Possible (error) messages:
    -------------------------
    + Info: pickle file '{0}' written
    + Warning: pickle file '{0}' cannot be loaded a/o written
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:generate_pickle2")

    pickle_name2  = dc.direc + PKL_FILE2
    try:
        pickle_file2  = open(pickle_name2, "bw")                        # opens the 2nd .pkl file
        pickle_data2  = dc.XML_toc                                      # prepares the data
        pickle.dump(pickle_data2, pickle_file2)                         # dumps the data
        pickle_file2.close()                                            # closes the file
        if dc.verbose:
            print(f"--- Info: pickle file '{pickle_name2}' written")
    except Exception as exc:                                                             # not successfull
        if dc.verbose:
            print(f"--- Warning: pickle file '{pickle_name2}' cannot",
                  "be loaded a/o written", exc)

    if dc.debugging:
        print("+++ <CTANLoad:generate_pickle2")

# ------------------------------------------------------------------
def generate_topicspackages(dc=dc_var):                                 # Function generate_topicspackages
    """
    Generates/rewrites dc.topicspackages, dc.packagetopics,
    dc.authorpackages,  dc.licensepackages, and dc.yearpackages.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.topicspackages   Python dictionary
                        collection of topics and their corresponding packages
    dc.packagetopics    Python dictionary
                        ist of packages and their topics
    dc.authorpackages   Python dictionary
                        list of authors and their corresponding packages
    dc.licensepackages  Python dictionary
                        list of licenses and their corresponding packages
    dc.yearpackages     Python dictionary
                        list of years and their corr. packages
    dc.file_not_found   Python set
                        XML file not found
    dc.not_well_formed  Python set
                        XML file not well-formed/empty
    dc.debugging        bool:
                        global flag: debugging enabled
    dc.verbose          bool:
                        global flag: output is verbose

    Possible (error) messages:
    -------------------------
    + Warning: local XML file for package '{0}' empty or not
               well-formed
    + Warning: local XML file for package '<file>' not found
    + Info: dc.packagetopics, dc.topicspackages, authorpackage,
            dc.yearpackages collected
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.4    2026-06-30 unspecified "except:" replaced by
    #                   "except Exception as err:"
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ >CTANLoad:generate_topicspackages")

    dc.yearpackages = {}

    for f in dc.packages:                                               # all package XML files are loaded (+ analyzed) in series
        tmpyears = []                                                   # initialize tmpyears
        maxyears = '1970'                                               # initialize maxyears
        try:                                                            # tries to open and parse file
            fext = f + EXT                                              # file name (with extension)
            ff = open(fext, encoding="utf-8", mode="r")                 # opens file

            try:
                onePackage     = ET.parse(fext)                         # parses one XML file
                onePackageRoot = onePackage.getroot()
                                                                        # gets root
                kk             = list(onePackageRoot.iter("keyval"))    # all keyval elements in the XML file
                aa             = list(onePackageRoot.iter("authorref")) # all authorref elements in the XML file
                ll             = list(onePackageRoot.iter("license"))   # all license elements in the XML file
                mm             = list(onePackageRoot.iter("version"))   # all version elements in the XML file
                nn             = list(onePackageRoot.iter("copyright")) # all copyright elements in the XML file

                for i in kk:                                            # in keyval: one attribute: value
                    key = i.get("value", EMPTY)                         # gets attribute value
                    if key in dc.topicspackages:
                        dc.topicspackages[key].append(f)
                    else:
                        dc.topicspackages[key] = [f]

                    if f in dc.packagetopics:
                        dc.packagetopics[f].append(key)
                    else:
                        dc.packagetopics[f] = [key]

                for j in aa:                                            # in authorref: 4 attributes: givenname, familyname, key, id
                    key1 = j.get("givenname", EMPTY)                    # gets attribute givenname
                    key2 = j.get("familyname", EMPTY)                   # gets attribute familyname
                    key3 = j.get("key", EMPTY)                          # gets attribute key
                    key4 = j.get("id", EMPTY)                           # gets attribute id
                    if key4 != EMPTY:
                        key3 = key4
                    if key3 in dc.authorpackages:
                        dc.authorpackages[key3].append(f)
                    else:
                        dc.authorpackages[key3] = [f]

                for k in ll:                                            # in license: 2 attributes: type, free
                    key5 = k.get("type", EMPTY)                         # get attribute type
                    key6 = k.get("free", EMPTY)                         # get attribute free
                    if key5 in dc.licensepackages:
                        dc.licensepackages[key5].append(f)
                    else:
                        dc.licensepackages[key5] = [f]

                for m in mm:                                            # in version: 2 attributes: date, number
                    key7 = m.get("date", EMPTY)                         # gets attribute date
                    key8 = m.get("number", EMPTY)                       # gets attribute number
                    tmp7 = re.split("[-]", key7)
                for x in tmp7:
                    if p10.match(x):                                    # check: year matches "^[12][09][01289][0-9]$"
                        if x in tmpyears:
                            tmpyears.append(x)
                        else:
                            tmpyears = [x]

                for n in nn:                                            # in copyright: 2 attributes: owner, year
                    key9  = n.get("owner", EMPTY)                       # gets attribute owner
                    key10 = n.get("year", EMPTY)                        # gets attribute year
                    tmp10 = re.split("[, -]", key10)
                for x in tmp10:
                    if p10.match(x):                                    # check: year matches "^[12][09][01289][0-9]$"
                        if x in tmpyears:
                            tmpyears.append(x)
                        else:
                            tmpyears = [x]

                if len(tmpyears) >= 1:
                    maxyears = max(tmpyears)

                if maxyears in dc.yearpackages:
                    dc.yearpackages[maxyears].append(f)
                else:
                    dc.yearpackages[maxyears] = [f]

            except Exception as err:                                    # parsing was not successfull
                if dc.verbose:
                    print(f"----- Warning: local XML file for",
                          f"package '{f}' empty or not well-formed",
                          err)
                ff.close()
                dc.not_well_formed.add(f)                               # appends file name to the not_well_formed list
        except FileNotFoundError as err:                                # file not downloaded
            if dc.verbose and dc.integrity:
                print(f"----- Warning: local XML file for",
                      f"package '{f}' not found")
            dc.file_not_found.add(f)                                    # appends file name to the file_not_found list
    if dc.verbose:
        print("--- Info: packagetopics, topicspackages,"
              "authorpackage, yearpackages collected")

    if dc.debugging:
        print("+++ <CTANLoad:generate_topicspackages")

# ------------------------------------------------------------------
def get_xyz_lpt(dc=dc_var) ->list:                                      # Function get_xyz_lpt
    """
    Loads and analyzes xyz.lpt for topic templates.

    Rewrites the variables dc.number, dc.counter, dc.pdfcounter in the
    data class dc.

    Returns:
    -------
    Returns a list of selected packages.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.number       int:
                    maximum number of files to be loaded
    dc.counter      int:
                    counter for downloadd XML and PDF files
    dc.pdfcounter   int:
                    counter for downloaded PDF files
    dc.debugging    bool:
                    global flag: debugging enabled
    dc.verbose      bool:
                    global flag: output is verbose

    Possible (error) messages:
    -------------------------
    + Error: local file '{0}' cannot be loaded; please call ctanload
             -l  before
    + Warning: no package found which matches the" specified {0}
               template '{1}'
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ -CTANLoad:get_xyz_lpt")

    try:
        f = open(topicpackage_file, encoding="utf-8", mode="r")         # opens file
        for line in f:
            top, pack=eval(line.strip())
            if p5.match(top):                                           # collects packages with
                                                                        # specified key_template
                for g in pack:
                    dc.selected_packages_lpt.add(g)
        f.close()                                                       # closes file
    except IOError as err:
        if dc.verbose:                                                  # there is an error
            print(f"[CTANLoad] Error: local file",
                  "'{topicpackage_file}' cannot",
                  "be loaded; please call ctanload -l ... before", err,
                  traceback.print_exc())
        sys.exit()                                                      # program terminates
    if len(dc.selected_packages_lpt) == 0:                              # no matching packages found
        if dc.verbose:
            tmp_t = "topic"
            print("--- Warning: no package found which matches the",
                  f"specified {tmp_t} template '{dc.key_template}'")
    return dc.selected_packages_lpt

# ------------------------------------------------------------------
def get_xyz_llp(dc=dc_var) ->list:                                      # Function get_xyz_llp
    """
    Loads and analyzes xyz.llp for license templates.

    Rewrites the variables dc.number, dc.counter, dc.pdfcounter in the
    data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    Returns:
    -------
    Returns a list of selected packages.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.number       int:
                    maximum number of files to be loaded
    dc.counter      int:
                    counter for downloadd XML and PDF files
    dc.pdfcounter   int:
                    counter for downloaded PDF files
    dc.debugging    bool:
                    global flag: debugging 
    dc.verbose      bool:
                    global flag: output is verbose

    Possible (error) messages:
    -------------------------
    + Error: local file '{0}' cannot be loaded; please call
             ctanload -l  before
    + Warning: no package found which matches the specified {0}
               template '{1}'
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ -CTANLoad:get_xyz_llp")

    try:
        f = open(licensepackage_file, encoding="utf-8", mode="r")       # opens file
        for line in f:
            lic, pack = eval(line.strip())
            lic2      = dc.licenses[lic][0]
            lic3      = dc.licenses[lic][1]
            if lic3 == "true":
                lic3 = "free"
            else:
                lic3 = "not free"
            if p7.match(lic2) or p7.match(lic) or p7.match(lic3):       # collects packages with specified licenses
                for g in pack:
                    dc.selected_packages_llp.add(g)
        f.close()                                                       # closes file
    except IOError as err:
        if dc.verbose:                                                  # there is an error
            print(f"[CTANLoad] Error: local file",
                  f"'{licensepackage_file}' cannot",
                  "be loaded; please call ctanload -l ... before", err,
                  traceback.print_exc())
        sys.exit()                                                      # program terminates
    if len(dc.selected_packages_llp) == 0:                              # no matching packages found
        if dc.verbose:
            tmp_l = "license"
            print("--- Warning: no package found which matches the",
                  f"specified {tmp_l} template '{dc.license_template}'")
    return dc.selected_packages_llp

# ------------------------------------------------------------------
def get_xyz_lap(dc=dc_var) ->list:                                      # Function get_xyz_lap
    """
    Loads and analyzes xyz.lap for author templates.

    Rewrites the variables dc.number, dc.counter, dc.pdfcounterin the
    data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    Returns:
    -------
    Returns a list of selected packages.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.number       int:
                    maximum number of files to be loaded
    dc.counter      int:
                    counter for downloadd XML and PDF files
    dc.pdfcounter   int:
                    counter for downloaded PDF files
    dc.debugging    bool:
                    global flag: debugging 
    dc.verbose      bool:
                    global flag: output is verbose
 
    Possible (error) messages:
    -------------------------
    + Error: local file '{0}' cannot be loaded; please call ctanload
             -l  before
    + Warning: no package found which matches the" specified {0}
               template '{1}'
    + Warning: no author found with feference '{auth}'; ignored
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 2.56   2025-12-20 Extension of the try...except construct;
    #                   new warning
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.8    2026-07-13 backtracing
    # 3.8.2  2026-07-13 call traceback.print_exc()

    if dc.debugging:
        print("+++ -CTANLoad:get_xyz_lap")

    try:
        f = open(authorpackage_file, encoding="utf-8", mode="r")
                                                                        # opens file
        for line in f:
            auth, pack = eval(line.strip())                             # gets the items author and package
            try:
                if dc.authors[auth][1] != EMPTY:                        # extracts author's familyname
                    auth2 = dc.authors[auth][1]
                else:
                    auth2 = dc.authors[auth][0]
                if p6.match(auth2):                                     # collects packages with specified authors
                    for g in pack:
                        dc.selected_packages_lap.add(g)
            except KeyError as err:
                if dc.verbose:
                    print(f"--- Warning: no author found with",
                          f"reference '{auth}'; ignored", err)
        f.close()                                                       # closes file
    except IOError as err:
        if dc.verbose:                                                  # there is an IO error
            print(f"[CTANLoad] Error: local file",
                  f"'{authorpackage_file}' cannot",
                  "be loaded; please call ctanload -l ... before", err,
                  traceback.print_exc())
        sys.exit()                                                      # program terminates
    if len(dc.selected_packages_lap) == 0:                              # no matching packages found
        if dc.verbose:
            tmp_a = "author"
            print("--- Warning: no package found which matches the",
                  f"specified {tmp_a} template '{dc.author_template}'")
    return dc.selected_packages_lap

# ------------------------------------------------------------------
def get_package_set(dc=dc_var) ->set:                                   # Function get_package_set
    """
    Analyzes dictionary 'dc.packages' for name templates.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    Returns:
    -------
    Returns a list of selected packages.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  bool:
                  global flag: debugging enabled
    dc.verbose    bool:
                  global flag: output is verbose

    Possible message:
    ----------------
    + Warning: no package found which matches the specified {0}
               template '{1}'
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ -CTANLoad:get_package_set")

    tmp = set()
    
    for f in dc.packages:                                               # loop over all the packages
        if p2.match(f):                                                 # check: package name matches template
            tmp.add(f)
    if len(tmp) == 0:                                                   # no matching packages found
        if dc.verbose:
            tmp_n = "name"
            print("--- Warning: no package found which matches the",
                  f"specified {tmp_n} template '{dc.name_template}'")
    return tmp

# ------------------------------------------------------------------
def get_year_set(dc=dc_var) ->set:                                      # Function get_package_set
    """
    Analyzes dictionary 'dc.yearpackages' for year templates.

    Rewrites the variable dc.yearpackages in the data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    Retruns:
    -------
    Returns a list of yselected packages.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.yearpackages   Python dictionary
                      list of years and their corresponding packages
    dc.debugging      bool:
                      global flag: debugging enabled
    dc.verbose        bool:
                      global flag: output is verbose

    Possible message:
    ----------------
    + Warning: no package found which matches the specified {0}
      template '{1}'
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ -CTANLoad:get_year_set")

    tmp = set()
    
    for f in dc.yearpackages:                                           # loop over all the year-package correspondences
        if p9.match(f):                                                 # check: year matches year_template
            tmp2 = set(dc.yearpackages[f])
            tmp = tmp | tmp2
    if len(tmp) == 0:                                                   # no matching packages found
        if dc.verbose:
            tmp_y = "year"
            print("--- Warning: no package found which matches the ",
                  f"specified {tmp_y} template '{dc.year_template}'")
    return tmp

# ------------------------------------------------------------------
def get_PDF_files(d:str, dc=dc_var):                                    # Function get_PDF_files(d)
    """
    Lists all PDF files in the specified OS folder d.

    Parameters:
    ---------_
    d (str) : name of an OS folder
              no dfefault
    dc      : instance of the data class 'dataclass_var'
              default: dc_var

    Rewrites the variable dc.PDF_toc in the data class dc.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.PDF_toc    Python dictionary:
                  collection with PDF files
    dc.debugging  bool:
                  global flag: debugging 

    Messages:
    --------
    There are no specific messages.
    """

    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:get_PDF_files")

    tmp  = os.listdir(d)                                                # gets OS folder list
    tmp2 = {}
    for f in tmp:                                                       # all PDF files in current OS folder
        if p3.match(f):                                                 # check: file name matches "^[0-9]{10}-.+[.]pdf$"
            tmp2[f] = EMPTY                                             # presets with empty string
    dc.PDF_toc = tmp2

    if dc.debugging:
        print("+++ <CTANLoad:get_PDF_files")

# ------------------------------------------------------------------
def get_XML_files(d:str, dc=dc_var) ->list:                             # Function get_XML_files
    """
    Lists all XML files in the current OS folder d.

    Parameters:
    ----------
    d (str) : name of an OS folder
              no default
    dc      : instance of the data class 'dataclass_var'
              default: dc_var

    Returns:
    -------
    Returns a list of XML files.

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.debugging  bool:
                  global flag: debugging 

    Messages:
    --------
    There are no specific messages.
    """

    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ -CTANLoad:get_XML_files")

    tmp  = os.listdir(d)                                                # gets OS folder list
    tmp2 = []

    for f in tmp:
        if p4.match(f) and not f in EXCLUSION:                          # check: file name matches  "^.+[.]xml$"
            tmp2.append(f)
    return tmp2

# ------------------------------------------------------------------
def load_XML_toc(dc=dc_var):                                            # Function load_XML_toc()
    """
    Loads pickle file 2 (which contains dc.XML_toc).

    Rewrites the dc.XML_toc in the data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.XML_toc    Python dictionary
                  collection with XML files
    dc.debugging  bool:
                  global flag: debugging 

    Messages:
    --------
    There are no specific messages.
    """

    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:load_XML_toc")

    try:
        pickleFile2 = open(dc.direc + PKL_FILE2, "br")                  # opens the pickle file
        dc.XML_toc  = pickle.load(pickleFile2)                          # unpickles the data
        pickleFile2.close()
    except IOError:                                                     # not successfull
        pass                                                            # do nothing

    if dc.debugging:
        print("+++ <CTANLoad:load_XML_toc")

# ------------------------------------------------------------------
def main(dc=dc_var):                                                    # Function main()
    """
    Main Function (calls the other functions).

    Rewrites the variables dc.PDF_toc, dc.download, dc.lists,
    dc.integrity, dc.number, template, dc.author_template,
    dc.regenerate in the data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.PDF_toc          Python dictionary:
                        for PDF files
    dc.download         bool:
                        Flag: PDF files are to be downloaded
    dc.lists            bool:
                        Flag: special list are to be generated
    dc.integrity        bool:
                        Flag: integrity is to checked
    dc.number           int:
                        maximum number of files to be loaded
    dc.author_template  str:
                        template for author names
    dc.regenerate       bool:
                        Flag: pickle files are to regenerated
    dc.debugging        bool:
                        global flag: debugging 
    dc.output_name	str:
	                generic file name for output files

    calls:
    -----
    + call_plain
    + call_check
    + call_load
    + make_statistics
    + regenerate_pickle_files
    + check_integrity
    + test_clipboard

    Possible (error) messages:
    -------------------------
    + Info: Program call (with more details)
    + Info: Program call:
    + Info: program successfully completed
    + Info: summary: file not well-formed or empty
    + Info: summary: inconsistencies with PDF files for
    + Info: summary: package not found:
    + Info: summary: PDF could not be loaded
    + process time (CTANLoad)
    + total time (CTANLoad)
    + Warning: '{0}' reset to {1} (due to {2})
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.52   2025-10-05 time specification with unit
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.3    2026-05-08 print statements containing \+ have been
    #                   simplified
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 
    # 3.12   2026-08-15 log output of the options in the call revised

    if dc.debugging:
        print("+++ >CTANLoad:main")

    starttotal  = time.time()                                           # begin of time measure
    startprocess= time.process_time()                                   # begin of time measure

    n_bool    = dc.name_template != NAME_TEMPLATE_DEFAULT               # Flag: -t is set
    k_bool    = dc.key_template != KEY_TEMPLATE_DEFAULT                 # Flag: -k is set
    a_bool    = dc.author_template != AUTHOR_TEMPLATE_DEFAULT           # Flag: -A is set
    l_bool    = dc.license_template != LICENSE_TEMPLATE_DEFAULT         # Flag: -L is set
    y_bool    = dc.year_template != YEAR_TEMPLATE_DEFAULT               # Flag: -y is set
    i_bool    = dc.integrity != INTEGRITY_DEFAULT                       # Flag: -c is set
    r_bool    = dc.regenerate != REGENERATE_DEFAULT                     # Flag: -r is set

    load      = n_bool or k_bool or a_bool or l_bool or y_bool          # load
    check     = (not load) and ((dc.lists != LISTS_DEFAULT) or i_bool)  # check
    newpickle = (not load) and (not check) and r_bool                   # newpickle
    plain     = (not load) and (not check) and (not newpickle)          # plain

    for f in range(1, len(call)):
        if not "-" in call[f]:
            call[f] = '"' + call[f] + '"'
    arguments = BLANK.join(call[1:])                                    # get the parameters of function call

    if dc.verbose:
        print("\n" + "[CTANLoad] Info: Program call:",
              "CTANLoad.py" + BLANK + arguments)

    if load:                                                            # load mode
        if (dc.lists != LISTS_DEFAULT):                                 # -l reset
            dc.lists = False
            if dc.verbose:
                print(RESET_TEXT.format("-l", False,
                                        "'-n' or '-t' or '-f'"))
        if (dc.integrity != INTEGRITY_DEFAULT):                         # -c reset
            dc.integrity = False
            if dc.verbose:
                print(RESET_TEXT.format("-c", False,
                                        "'-n' or '-t' or '-f'"))
        if (dc.regenerate != REGENERATE_DEFAULT):                       # -r reset
            dc.regenerate = False
            if dc.verbose:
                print(RESET_TEXT.format("-r", False,
                                        "'-n' or '-t' or '-f'"))

    if check:                                                           # check mode
        if (dc.regenerate != REGENERATE_DEFAULT):                       # -r reset
            dc.regenerate = False
            if dc.verbose:
                print(RESET_TEXT.format("-r", False, "'-l' or '-c'"))

    if newpickle:                                                       # newpickle mode
        if dc.number <= NUMBER_DEFAULT:
            dc.number  = 3000                                           # -n reset
            if dc.verbose:
                print(RESET_TEXT.format("-n", 3000, "'-r'"))
        if dc.download == DOWNLOAD_DEFAULT:
            dc.download = True                                          # -f reset
            if dc.verbose:
                print(RESET_TEXT.format("-f", True, "'-r'"))

    if dc.verbose:                                                      # output on terminal (options in call)
        print("\n" + "[CTANLoad] Info: Program call (with more",
              "details):  CTANLoad.py")
        if (dc.integrity != INTEGRITY_DEFAULT):                         # parameter -c
            print(f"  {'-c':5} {'(' + INTEGRITY_TEXT + ')':55}")
        if (dc.download != DOWNLOAD_DEFAULT):                           # parameter -f
            print(f"  {'-f':5} {'(' + DOWNLOAD_TEXT + ')':55}")
        if (dc.lists != LISTS_DEFAULT):                                 # parameter -l
            tmpl = '(' + (LISTS_TEXT + ')')[0:50] + ELLIPSE
            print(f"  {'-l':5} {tmpl:55}")
        if (dc.regenerate != REGENERATE_DEFAULT):                       # parameter -r
            print(f"  {'-r':5} {'(' + REGENERATE_TEXT + ')':55}")
        if (dc.statistics != STATISTICS_DEFAULT):                       # parameter -stat
            print(f"  {'-stat':5} {'(' + STATISTICS_TEXT + ')':55}")
        if (dc.verbose != VERBOSE_DEFAULT):                             # parameter -v
            print(f"  {'-v':5} {'(' + VERBOSE_TEXT + ')':55}")

        if (dc.author_template != AUTHOR_TEMPLATE_DEFAULT):             # parameter -A
            tmpA = '(' + AUTHOR_TEMPLATE_TEXT + ')'
            print(f"  {'-A':5} {tmpA:55} {fold(dc.author_template)}")
        if (dc.direc != DIREC_DEFAULT):                                 # parameter -d
            print(f"  {'-d':5} {'(' + DIREC_TEXT + ')':55} {dc.direc}")
        if (dc.key_template != KEY_TEMPLATE_DEFAULT):                   # parameter -k
            tmpk = '(' + KEY_TEMPLATE_TEXT + ')'
            print(f"  {'-k':5} {tmpk:55} {fold(dc.key_template)}")
        if (dc.license_template != LICENSE_TEMPLATE_DEFAULT):           # parameter -L
            tmpL = '(' + LICENSE_TEMPLATE_TEXT + ')'
            print(f"  {'-L':5} {tmpL:55} {fold(dc.license_template)}")
        if (dc.number != NUMBER_DEFAULT):                               # parameter -n
            print(f"  {'-n':5} {'(' + NUMBER_TEXT + ')':55} {dc.number}")
        if (dc.output_name != dc.direc + OUTPUT_NAME_DEFAULT):          # parameter -o
            tmpo = '(' + OUTPUT_TEXT + ')'
            print(f"  {'-o':5} {tmpo:55} {args.output_name}")
        if (dc.name_template != NAME_TEMPLATE_DEFAULT):                 # parameter -t
            tmpt = '(' + NAME_TEMPLATE_TEXT + ')'
            print(f"  {'-t':5} {tmpt:55} {fold(dc.name_template)}")
        if (dc.year_template != YEAR_TEMPLATE_DEFAULT):                 # parameter -y
            tmpy = '(' + YEAR_TEXT + ')'
            print(f"  {'-y':5} {tmpy:55} {fold(dc.year_template)}")
        print("\n")

    if dc.statistics:                                                   # if statistics are to be output
        pp = 5
        endtotal   = time.time()

    if plain:                                                           # Process all steps for a plain call.
        call_plain()
    elif load:                                                          # Process all steps for a complete ctanload call (withoutb integrity check).
        call_load()
    elif check:                                                         # Process all necessary steps for a integrity check.
        call_check()
    elif newpickle:                                                     # Regenerate the two pickle files.
        regenerate_pickle_files()
        check_integrity(always=True)
    else:
        pass                                                            # do nothing

    if dc.verbose:
        if (len(dc.file_not_found) >= 1) and (not load):
            print("--- Info: summary: package not found:",
                  dc.file_not_found)
        if len(dc.not_well_formed) >= 1:
            print("--- Info: summary: file not well-formed or empty:",
                  dc.not_well_formed)
        if len(dc.PDF_notloaded) >= 1:
            print("--- Info: summary: PDF could not be loaded:",
                  dc.PDF_notloaded)
        if len(dc.PDF_XML) >= 1:
            print("--- Info: summary:",
                  "inconsistencies with PDF files for", dc.PDF_XML)
        print("[CTANLoad] Info: program successfully completed")

    if dc.statistics:                                                   # if statistics are to be output
        PP = 5
        make_statistics()                                               # Print statistics on terminal

        endtotal   = time.time()                                        # end of time measure
        endprocess = time.process_time()                                # end of time measure
        print("--")
        print("total time (CTANLoad): ".ljust(LEFT - 1),
              str(round(endtotal-starttotal, RNDG)).rjust(PP), "s")
        print("process time (CTANLoad): ".ljust(LEFT - 1),
              str(round(endprocess-startprocess, RNDG)).rjust(PP), "s")

    test_clipboard()

    if dc.debugging:
        print("+++ <CTANLoad:main")

# ------------------------------------------------------------------
def make_statistics(dc=dc_var):                                         # Function make_statistics()
    """
    Prints statistics on terminal.

    Rewrites the variables dc.counter, dc.pdfcounter in the data
    class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.counter          int:
                        counter for downloaded XML and PDF files
    dc.pdfcounter       int:
                        counter for downloaded PDF files
    dc.debugging        bool:
                        global flag: debugging 
    dc.author_template	str:
			Author template for package XML files
    dc.authors          Python dictionary:
                        collection with authors
    dc.corrected    	int:
                    	number of corrections
    dc.counter          int:
                        counter for downloadd XML and PDF files
    dc.direc      	str:
                  	name of the OS directory
    dc.download         bool:
                        Flag: PDF files are to be downloaded
    dc.integrity        bool:
                        Flag: integrity is to checked
    dc.key_template	str:
			Key template for package XML files
    dc.license_template	str:
			License template for package XML files
    dc.licenses         Python dictionary:
                        collection with licenses
    dc.name_template	str:
			Name template for package XML files
    dc.no_tp            int:
                        number of packages selected per topics
    dc.no_ap            int:
                        number of packages selected per author names
    dc.no_np            int:
                        number of packages selected per n<mes
    dc.no_lp            int:
                        number of packages selected per licenses
    dc.no_ly            int:
                        number of packages selected per years
    dc.packages         Python dictionary:
                        collection with packages
    dc.PDF_toc          Python dictionary:
                        Collection for PDF files
    dc.pdfcounter       int:
                        counter for downloaded PDF files
    dc.pdfctrerr        int:
                        counter for not downloaded PDF files
                        (in the actual session)
    dc.topics           Python dictionary:
                        collection with topics
    dc.year_template	str:
			Template for filtering on the base of years

    Possible messages:
    -----------------
    + no. of packages (based on authors)
    + no. of packages (based on keys)
    + no. of packages (based on licenses)
    + no. of packages (based on names)
    + no. of packages (based on years)
    + number of corrected entries
    + number of downloaded PDF files
    + number of downloaded XML files
    + number of not downloaded PDF files
    + total number of authors on CTAN
    + total number of licenses on CTAN
    + total number of local PDF files
    + total number of local XML files
    + total number of packages on CTAN
    + total number of topics on CTAN
    """

    # 2.43   2024-04-12 smaller changes in make_statistics
    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:make_statistics")

    L             = LEFT + 1                                            # layout parameter
    R             = 5                                                   # layout parameter
    load:bool     = (dc.name_template != EMPTY)
    nrXMLfile:int = 0                                                   # initialze counter

    XMLdir = os.listdir(dc.direc)                                       # files in the current OS folder
    for f in XMLdir:
        if p4.match(f):                                                 # check: XML file name matches "^.+[.]xml$"
            nrXMLfile += 1

    print("\nStatistics:")
    print("date | time:".ljust(L + 1), ACT_DATE, "|", ACT_TIME)
    print("program | version | date:".ljust(L + 1), PRG_NAME, "|",
          PRG_VERSION, "|", PRG_DATE, "\n")

    print("total number of authors on CTAN:".ljust(L),
          str(len(dc.authors)).rjust(R))
    print("total number of topics on CTAN:".ljust(L),
          str(len(dc.topics)).rjust(R))
    print("total number of packages on CTAN:".ljust(L),
          str(len(dc.packages)).rjust(R))
    print("total number of licenses on CTAN:".ljust(L),
          str(len(dc.licenses)).rjust(R))
    if dc.download or (dc.counter > 0):
        print("number of downloaded XML files:".ljust(L),
              str(dc.counter).rjust(R), "(in the actual session)")
        print("number of downloaded PDF files:".ljust(L),
              str(dc.pdfcounter).rjust(R), "(in the actual session)")
        print("number of not downloaded PDF files:".ljust(L),
              str(dc.pdfctrerr).rjust(R), "(in the actual session)")
    print("total number of local PDF files:".ljust(L),
          str(len(dc.PDF_toc)).rjust(R))
    print("total number of local XML files:".ljust(L),
          str(nrXMLfile).rjust(R))
    if dc.integrity:
        print("number of corrected entries:".ljust(L),
              str(dc.corrected).rjust(R), "(in the actual session)")

    print(EMPTY)                                                       
    if dc.name_template != NAME_TEMPLATE_DEFAULT:                       # name filtering
        print("no. of packages (based on names):".ljust(L),
              str(dc.no_np).rjust(R))
    if dc.key_template != KEY_TEMPLATE_DEFAULT:                         # key template
        print("no. of packages (based on keys):".ljust(L),
              str(dc.no_tp).rjust(R))
    if dc.license_template != LICENSE_TEMPLATE_DEFAULT:                 # license template
        print("no. of packages (based on licenses):".ljust(L),
              str(dc.no_lp).rjust(R))
    if dc.author_template != AUTHOR_TEMPLATE_DEFAULT:                   # author template
        print("no. of packages (based on authors):".ljust(L),
              str(dc.no_ap).rjust(R))
    if dc.year_template != YEAR_TEMPLATE_DEFAULT:                       # year template
        print("no. of packages (based on years):".ljust(L),
              str(dc.no_ly).rjust(R))

    if dc.debugging:
        print("+++ <CTANLoad:make_statistics")
 
# ------------------------------------------------------------------
def regenerate_pickle_files(dc=dc_var):                                 # regenerate_pickle_files
    """
    Regenerates corrupted pickle files.

    Rewrites the variables CTAN1.pkl, CTAN2.pkl, a/o the variables
    dc.XML_toc, dc.PDF_toc, dc.authors, dc.packages, dc.topics,
    dc.licenses, dc.topicspackages, dc.packagetopics, dc.authorpackages,
    licensepackages, dc.yearpackages in the data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.XML_toc          Python dictionary:
                        collection with XML files
    dc.PDF_toc          Python dictionary:
                        collection with PDF files
    dc.authors          Python dictionary:
                        collection with authors
    dc.packages         Python dictionary:
                        collection with packages
    dc.topics           Python dictionary:
                        collection with topics
    dc.licenses         Python dictionary:
                        collection with licenses
    dc.topicspackages   Python dictionary:
                        collection of topics and their corresponding packages
    dc.packagetopics    Python dictionary:
                        list of packages and their topics
    dc.authorpackages   Python dictionary:
                        list of authors and their corresponding packages
    dc.licensepackages  Python dictionary:
                        list of licenses and their corresponding packages
    dc.yearpackages     Python dictionary:
                        list of years and their corresponding packages
    dc.debugging        bool:
                        global flag: debugging 

    Calls:
    -----
    +  get_PDF_files
    +  dload_authors
    +  dload_packages
    +  dload_topics
    +  dload_licenses
    +  generate_topicspackages
    +  analyze_XML_file
    +  generate_pickle2
    +  generate_pickle1
    +  get_XML_files

    Possible messages:
    -----------------
    + Info: Regeneration of '{0}'
    + Info: local XML file '{0}'
    + Info: Regeneration of '{0}'
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:regenerate_pickle_files")

# .................................................................
# Regeneration of CTAN2.pkl
# CTAN2.pkl needs dc.XML_toc
# one thread

    if dc.verbose:
        print(f"--- Info: Regeneration of '{dc.direc + PKL_FILE2}'")

    get_PDF_files(dc.direc)                                             # List all PDF files in a specified OS folder.
    dload_authors()                                                     # loads dc.authors
    dload_packages()                                                    # loads packages
    dload_topics()                                                      # loads topics
    dload_licenses()                                                    # loads licenses
    generate_topicspackages()                                           # generates dc.topicspackages, dc.packagetopics, dc.authorpackages, licensepackages, dc.yearpackages

    for f in get_XML_files(dc.direc):
        if dc.verbose:
            print(f"----- Info: local XML file '{dc.direc + f}'")
        analyze_XML_file(f)

    thr1 = Thread(target=generate_pickle2)                              # dumps dc.XML_toc info CTAN2.pkl
    thr1.start()
    thr1.join()

# .................................................................
# Regeneration of CTAN1.pkl
# CTAN1.pkl needs dc.authors, dc.packages, dc.topics, dc.licenses,
# dc.topicspackages, dc.packagetopics, dc.authorpackages,
# dc.yearpackages one thread

    if dc.verbose:
        print(f"--- Info: Regeneration of '{dc.direc + PKL_FILE}'")

    thr2 = Thread(target=generate_pickle1)                              # dumps dc.authors, dc.packages,
                                                                        # dc.topics, dc.licenses, dc.topicspackages, dc.packagetopics,
                                                                        # dc.authorpackages, licensepackages, dc.yearpackages into CTAN1.pkl
    thr2.start()
    thr2.join()

    if dc.debugging:
        print("+++ <CTANLoad:regenerate_pickle_files")

# ------------------------------------------------------------------
def set_PDF_toc(dc=dc_var):                                             # Function set_PDF_toc
    """
    Fills dc.PDF_toc on the basis of dc.XML_toc.

    Rewrites the variables dc.PDF_toc, dc.XML_toc in the data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------
    dc.PDF_toc    Python dictionary:
                  collection with PDF files
    dc.XML_toc    Python dictionary:
                  collection with XML files
    dc.direc      str:
                  name of the OS directory
    dc.debugging  bool:
                  global flag: debugging 

    Messages:
    --------
    There are no specific messages.
    """

    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:set_PDF_toc")

    for f in dc.XML_toc:
        (xlfn, fkey, plfn) = dc.XML_toc[f]
        if os.path.exists(dc.direc + xlfn) and os.path.\
           exists(dc.direc + fkey + "-" + plfn):
            dc.PDF_toc[fkey + "-" + plfn] = xlfn
        else:
            pass

    if dc.debugging:
        print("+++ <CTANLoad:set_PDF_toc")

# ------------------------------------------------------------------
def verify_PDF_files(dc=dc_var):                                        # Function verify_PDF_files
    """
    Checks actualized dc.PDF_toc; deletes a PDF file if necessary.

    Rewrites the variables dc.ok, dc.PDF_toc, and dc.correctedin the
    data class dc.

    Parameter:
    ---------
    dc : instance of the data class 'dataclass_var'
         default: dc_var

    The function needs access to some variables in the data class dc:
    ----------------------------------------------------------------  
    dc.ok         bool:
                  global flag: status of processing
    dc.PDF_toc    Python dictionary:
                  collection collection with PDF files
    dc.corrected  int:
                  number of corrections
    dc.debugging  bool:
                  global flag: debugging 

    Possible (error) messages:
    -------------------------
    + Warning: PDF file '{0}' without associated XML file
    + Warning: PDF file '{0}' in OS deleted
    """

    # 2.46   2025-02-04 messages in functions' __doc__ texts listed
    # 2.49   2025-02-11 more f-strings
    # 2.53   2025-11-01 in __doc__ text: list the respective (error)
    #                   messages
    # 3.5    2026-07-02 data class used
    # 3.5.3  2026-07-02 if necessary: Function definitions supplemented
    #                   by the parameter "dc=dc_var"
    # 3.5.4  2026-07-02 relevant local variables prefixed with "dc."
    #                   and/or non-local with "dc_var"
    # 3.5.6  2026-07-03 "global" statements removed
    # 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the
    #                   data class 

    if dc.debugging:
        print("+++ >CTANLoad:verify_PDF_files")

    dc.ok = True
    
    for g in dc.PDF_toc:                                                # loop: move through dc.PDF_toc
        if dc.PDF_toc[g] == EMPTY:                                      # no entry: no ass. XML file
            dc.ok = False
            if dc.verbose:
                print(f"----- Warning: PDF file '{g}' without",
                      "associated XML file")
            if os.path.isfile(g):                                       # g is file
                os.remove(g)                                            # deletes the PDF file (if it exists)
                dc.corrected += 1                                       # number of corrections increased
                if dc.verbose:
                    print("----- Warning:",
                          f"PDF file '{g}' in OS deleted")
        else:
            pass

    if dc.debugging:
        print("+++ <CTANLoad:verify_PDF_files")


# ==================================================================
# Main part

# 2.50   2025-02-12 no test: __name__ == "__main__; ==>
#                   CTANLoad.py can be imported

# script --> main

##if __name__ == "__main__":                                            # program is called directly
##    main()
##else:
##    if verbose:
##        print("[CTANLoad] Error: tried to use the program indirectly")
main()

# ==================================================================

# History
#
# 2.0    2019-10-01 completely revised
# 2.0.1  2019-10-03 smaller changes: messages + command parsing
# 2.0.2  2019-10-04 smaller changes: messages
# 2.0.3  2019-11-26 smaller changes: error message and parameter -n
# 2.0.4  2020-01-09 -c enhanced
# 2.0.5  2020-01-12 some corrections
# 2.0.6  2020-01-15 time measure
# 2.0.7  2020-01-24 statistics improved
# 2.0.8  2020-01-25 minor corrections
# 2.0.9  2020-06-05 correction in load_documentation_file
# 2.0.10 2020-06-26 enhance verbose output
# 2.0.11 2020-07-22 first lines of file
# 2.0.12 2021-04-05 output for option -c enhanced
# 2.0.13 2021-05-13 output local file name for downladed PDF files in verbose mode
# 2.0.14 2021-05-13 output the call parameters in more details in verbose mode
# 2.0.15 2021-05-14 clean-up for variables
# 2.0.16 2021-05-20 OS folder + separator improved
# 2.0.17 2021-05-21 more details in verbose mode
# 2.0.18 2021-05-23 OS folder name improved
# 2.0.19 2021-05-24 OS folder handling improved (existance, installation)

# 2.1    2021-05-26 load licences, make corr. dictionary and file; expand CTAN.pkl
# 2.1.1  2021-05-26 correction for not-existing keys in licenses.xml
# 2.1.2  2021-06-07 smaller improvements in check_integrity

# 2.2    2021-06-08 new approach in check_integrity

# 2.3    2021-06-09 some funcion calls as threads
# 2.3.1  2021-06-12 auxiliary function fold: shorten long option values for output
# 2.3.2  2021-06-14 messages classified: Warnings, Error, Info
# 2.3.3  2021-06-14 str.format(...) used (if applicable); ellipses used to shorten some texts
# 2.3.4  2021-06-15 main function new structured
# 2.3.5  2021-06-18 output (options in program call) enhanced
# 2.3.6  2021-06-18 new function verify_PDF_files: check actualized PDF_toc; delete a PDF file if necessary
# 2.3.7  2021-06-19 main function more modularized; new functions call_plain, call_load, call_check
# 2.3.8  2021-06-22 error corrections and improvements for the handling von PDF_toc and XML_toc

# 2.4    2021-06-23 regeneration of pickle file enabled: new option -r; new functions regenerate_pickle_files and get_XML_files
# 2.4.1  2021-06-24 error handling in the check_integrity context changed
# 2.4.2  2021-06-26 handling of -r changed

# 2.5    2021-06-30 add. option -k; add. function get_CTAN_lpt (needs CTAN.lpt)
# 2.5.1  2021-07-01 minor corrections
# 2.5.2  2021-07-05 function fold restructured
# 2.5.3  2021-07-06 pickle file 1 is generated, too

# 2.6    2021-07-11 search of packages with author name template; new option -A; new function get_CTAN_lap (needs CTAN.lap)
# 2.6.1  2021-07-12 some corrections in the handling of -t / -k and -A
# 2.6.2  2021-07-15 more corrections in the handling of -t / -k and -A

# 2.7    2021-07-26 combined filtering new organized; new function get_package_set; 2 additional warning messages
# 2.7.1  2022-02-02 attribute free in licenses.xml; changes in dload_licenses
# 2.7.2  2022-02-03 changes in get_CTAN_lap and get_CTAN_lpt; now on the basis of all.(lap, lpt); additional adjustments
# 2.7.3  2022-02-04 functions renamed: get_CTAN_lap --> get_xyz_lap, get_CTAN_lpt --> get_xyz_lpt

# 2.8    2022-02-16 new option -L; new section in argparse; new variables license_template_text, license_template_default, license_template
# 2.8.1  2022-02-16 changes in generate_lists; creates xyz.llp
# 2.8.2  2022-02-16 changes in generate_topicspackages; creates Python dictionary licensepackages
# 2.8.3  2022-02-16 changes in generate_pickle1: CTAN.pkl extended: now with new component licensepackages
# 2.8.4  2022-02-16 new function get_xyz_llp; loads and analyzes xyz.llp; allows license searching with title, shorttitle, and free/not free
# 2.8.5  2022-02-17 changes in call_check, call_load, and main; respects license searching
# 2.8.6  2022-02-18 changes for -stat; changes in make_statistics
# 2.8.7  2022-02-18 messages in get_xyz_lap, get_xyz_lpt, and get_xyz_llp changed

# 2.9    2022-02-23 other messsages improved

# 2.10   2022-06-11 messages revised

# 2.11   2023-06-11 new option -y (filtering on the base of year templates)
# 2.11.1 2023-06-11 some changes in relevant functions (interaction of different filter operations improved)
# 2.11.2 2023-06-11 related changes in the statistics part (option -stat)

# 2.12   2023-06-15 CTANLoad-changes.txt, CTANLoad-examples.txt, CTANLoad-functions.txt changed
# 2.13   2023-06-15 output on terminal changed
# 2.14   2023-06-15 new option -dbg/--debugging: debugging mode enabled
# 2.15   2023-06-26 some minor changes in statistics output
# 2.16   2023-07-05 some messages with the signature [CTANLoad]
# 2.17   2023-07-05 some minor errors in get_year_set and get_package_set corrected
# 2.18   2023-07-11 year_default_template renewed

# 2.19   2023-07-11 file not found, not well formed, PDF notloaded
# 2.19.1 2023-07-11 additionally in statistics: output of the lists file_not_found, not_well_formed, PDF_notloaded
# 2.19.2 2023-07-11 therefore 3 new messages; 3 minor changes in messages
# 2.19.3 2023-07-12 file_not_found, not_well_formed, PDF_notloaded now Python sets
# 2.19.4 2023-07-16 test_clipboard() new: tests if there is file_not_found, not_well_formed or PDF_notloaded + generates a specific program call in clipboard

# 2.20   2023-07-16 now new message, if -l is set: in the case of inconsistencies with PDF files
# 2.21   2023-07-28 output of -stat now with program date
# 2.23   2023-07-28 message "Info: summary: package not found" corrected and adjusted
# 2.24   2024-03-04 wget processor and subprocess timeout now configurable

# 2.25   2024-03-04 Function dload_authors revised
# 2.25.1 2024-03-04 parameters for wget and subprocess reorganized
# 2.25.2 2024-03-04 parameters for wget now in a list
# 2.25.3 2024-03-04 subprocess.Popen replaced by subprocess.run
# 2.25.4 2024-03-04 subprocess.run additionally with check=True, timeout=...
# 2.25.5 2024-03-04 Exception handling extended

# 2.26   2024-03-04 Function dload_licenses revised
# 2.26.1 2024-03-04 parameters for wget and subprocess reorganized
# 2.26.2 2024-03-04 parameters for wget now in a list
# 2.26.3 2024-03-04 subprocess.Popen replaced by subprocess.run
# 2.26.4 2024-03-04 subprocess.run additionally with check=True, timeout=...
# 2.26.5 2024-03-04 Exception handling extended

# 2.27   2024-03-04 Function dload_packages revised
# 2.27.1 2024-03-04 parameters for wget and subprocess reorganized
# 2.27.2 2024-03-04 parameters for wget now in a list
# 2.27.3 2024-03-04 subprocess.Popen replaced by subprocess.run
# 2.27.4 2024-03-04 subprocess.run additionally with check=True, timeout=...
# 2.27.5 2024-03-04 Exception handling extended: all xx-texts of the functions completed (parameters and global variables)

# 2.27   2024-03-04 Function dload_topics revised
# 2.27.1 2024-03-04 parameters for wget and subprocess reorganized
# 2.27.2 2024-03-04 parameters for wget now in a list
# 2.27.3 2024-03-04 subprocess.Popen replaced by subprocess.run
# 2.27.4 2024-03-04 subprocess.run additionally with check=True, timeout=...
# 2.27.5 2024-03-04 Exception handling extended

# 2,28   2024-03-04 in dload_document_file: PDF_XML now in global list
# 2.29   2024-03-04 time specifications with unit s

# 2.30   2024-03-04 Function dload_XML_files revised
# 2.30.1 2024-03-04 parameters for wget and subprocess reorganized
# 2.30.2 2024-03-04 parameters for wget now in a list
# 2.30.3 2024-03-04 subprocess.Popen replaced by subprocess.run
# 2.30.4 2024-03-04 subprocess.run additionally with check=True, timeout=...
# 2.30.5 2024-03-04 Exception handling extended

# 2.31   2024-03-04 Function dload_document_file revised
# 2.31.1 2024-03-04 parameters for wget and subprocess reorganized
# 2.31.2 2024-03-04 parameters for wget now in a list
# 2.31.3 2024-03-04 subprocess.Popen replaced by subprocess.run
# 2.31.4 2024-03-04 subprocess.run additionally with check=True, timeout=...
# 2.31.5 2024-03-04 Exception handling extended

# 2.32   2024-03-05 in analyze_XML_file: additions to the not_well_formed set corrected
# 2.33   2024-03-05 test_clipboard() made more robust

# 2.34   2024-03-13 dload_topics, dload_authors, dload_licenses, dload_packages revised
# 2.34.1 2024-03-13 parameter -O and -P for wget corrected
# 2.34.2 2024-03-13 exception handling revised

# 2.35   2024-03-15 in dload_XML_files: parameter -O and -P for wget corrected
# 2.36   2024-03-15 in analyze_XML_file: exception handling extended (parsing a XML file)
# 2.37   2024-04-15 in dload_XML_files: exception handling revised (downloading a XML file)
# 2.38   2024-03-15 in dload_document_file: parameter -O and -P for wget corrected
# 2.39   2024-03-17 in dload_document_file: error in URL building corrected
# 2.40   2024-03-25 generation of xyz.lok, xyz.lol, xyz.lpt, xyz.lap, xyz.llp corrected a/o improved
# 2.41   2024-03-25 test_clipboard: outputs an explanatory text to clipboard if there is nothing to do
# 2.42   2024-03-28 all __doc__ texts of the functions completed (parameters and global variables)
# 2.43   2024-04-12 smaller changes in make_statistics

# 2.44   2024-07-26 argparse revised
# 2.44.1 2024-07-26 additional parameter in .ArgumentParser: prog, epilog, formatter_class
# 2.44.2 2024-07-26 subdivision-groups by .add_argument_group
# 2.44.3 2024-07-26 additional arguments in .add_argument (if it makes sense): type, metavar, action, dest

# 2.45   2025-02-04 new error message
# 2.45.1 2025-02-04 standard XML file '{0}' not found
# 2.45.2 2025-02-04 standard XML file '{0}' not not well-formed

# 2.46   2025-02-04 messages in functions' __doc__ texts
# 2.47   2025-02-06 everywhere: all source code lines wrapped at a maximum of 80 characters
# 2.48   2025-02-06 wherever appropriate:  string interpolation with f-strings instead of .format
# 2.49   2025-02-11 more f-strings
# 2.50   2025-02-12 no test: __name__ == "__main__; ==> CTANLoad.py can be imported
# 2.51   2025-09-02 check_integrity (-l): Show inconsistencies + list of missing files
# 2.52   2025-10-05 time specification with unit
# 2.53   2025-11-01 in __doc__ text: list the respective (error) messages
# 2.54   2025-11-03 argparse texts revised
# 2.55   2025-12-12 subprocess.run calls revised 
# 2.56   2025-12-20 Extension of a try...except construct in get_xyz_lap; new warning

# 3.0    2026-04-01 Complete revision (too many changes to list in the code)
# 3.0.1  2026-04-01 Functions with type annotations
# 3.0.2  2026-04-01 Variable annotations (where appropriate and possible)
# 3.0.3  2026-04-01 uppercase constants
# 3.0.4  2026-04-01 .format replaced with f-strings (where appropriate)
# 3.0.5  2026-04-01 __doc__ texts supplemented and standardised
# 3.0.6  2026-04-01 Standardised: Code up to a maximum of column 71
# 3.0.7  2026-04-01 Standardised: Comments from column 72 onwards

# 3.1    2026-04-15 in dload_XML_files: better handling with processor error (and other exceptions)
# 3.2    2026-05-01 for XML and PDF files: downloads with number
# 3.3    2026-05-08 print statements containing \+ simplified
# 3.4    2026-06-30 unspecified "except:" replaced by "except Exception as err:"

# 3.5    2026-07-02 data class used
# 3.5.0  2026-07-13 new module dataclasses
# 3.5.1  2026-07-02 new class dataclass-variable (including all globally used variables) derfined
# 3.5.2  2026-07-02 instance "dc_var" of this class created
# 3.5.3  2026-07-02 if necessary: Function definitions supplemented by the parameter "dc=dc_var"
# 3.5.4  2026-07-02 relevant local variables prefixed with "dc." and/or non-local with "dc_var"
# 3.5.5  2026-07-03 original definitions of globally used variables removed
# 3.5.6  2026-07-03 "global" statements removed
# 3.5.7  2026-07-04 __doc__ texts supplemented/adapted to the data class

# 3.6    2026-07-05 ACT_PROGRAMNAME depends on OPERATINGSYS now
# 3.7    2026-07-05 XML and PDF downloads: number of download

# 3.8    2026-07-13 backtracing
# 3.8.1  2026-07-13 new module traceback
# 3.8.2  2026-07-13 call traceback.print_exc()

# 3.9    2026-07-23 correction for not-existing key in licenses.xml
# 3.10   2026-08-05 correction in dataclass_variable: collections with default factory
# 3.11   2026-08-10 Calculation and output of the input string
# 3.12   2026-08-15 log output of the options in the call revised

# + L.3367: arguments: Berechnung und Ausgabe (x)
# - Eintrag an geeigneter Stelle: fehlend topic, license

# - gravierender Fehler: -A xyz führt zum Programmabbruch
# - neue Fehlermeldung registrieren
# - neu machen: Funktionshierarchie, Beispiele, Übersicht über Meldungen
# - laden per ctrl c abbrechbar
# - dictionary.get() wo angebracht
# - doctext im google-stylebzw. numpy-Style; siehe Anleitungen; z.B. https://realpython.com/documenting-python-code/
# - if __name__ == "__main__": main() verwenden
# - finally-clause bei geöffneten Dateien
# - try...except vereinheitlichen + überarbeiten; weniger aggressiv
# - lokale Changes kontrollieren, insb. traceback.print_exc()

# Es fehlen noch  bzw. Probleme:
# - unterschiedliche Verzeichnisse für XML- und PDF-Dateien? (-)
# - GNU-wget ersetzen durch python-Konstrukt; https://pypi.org/project/python3-wget/ (geht eigentlich nicht)(-) (?)
# - Fehler bei -r; es wird jedesmal CTAN.pkl neu gemacht (?)
# - neues feature: alle ungeladenen Pakete laden (?)
# - Auswahl nach Datum (-)
# - später: get_CTAN_lap und get_CTAN_lpt umstellen auf direkte CTAN-Abfrage (?)
# - neu machen: Funktionshierarchie, Beispiele, Übersicht über Meldungen
# - aufgerufene Optionen normieren (?)
# - in ctanload -l -c: nicht nur fehlende Pakete, auch fehlende PDF-Dateien
# - " in OS deleted" wird nicht in Zwischenablage berücksichtigt; bei ctanload -l -c -v -stat
# - problem bei PDF-Dateien mit +:  wahrscheinlich dload_document_file korrigieren (?)
# - reicht nicht; auch verify_PDF_files, analyze_XML_file, check_integrity und PDF_toc?
# - neues Konzept für Programm: CTANLoad <task> <schlüsselwort-parameter>; <task>: load|plain|...
# - fehlerhafte Pakete auflisten; auch wegen fehlendem topics-Eintrag
# + Suche unabhängig von Groß/Kleinschreibung
