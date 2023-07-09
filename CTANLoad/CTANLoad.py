#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANLoad.py
# (C) Günter Partosch, 2019/2021/2022

# see also: CTANLoad-changes.txt
#           CTANLoad-examples.txt
#           CTANLoad-functions.txt
#           CTANLoad-messages.txt
#           CTANLoad-modules.txt
#           CTANLoad.man
#           CTAN-files.txt


# ==================================================================
# Imports

import argparse                    # parse arguments
import os                          # delete a file on disk, for instance
from os import path                # path informations
import pickle                      # read/write pickle data
import platform                    # get OS informations
import random                      # used for random integers
import re                          # handle regular expressions
import subprocess                  # handling of sub-processes
import sys                         # system calls
import time                        # used for random seed, time measurement
import xml.etree.ElementTree as ET # XML processing
from threading import Thread       # handling of threads


# ==================================================================
# Global settings

# ------------------------------------------------------------------
# The program

prg_name        = "CTANLoad.py"
prg_author      = "Günter Partosch"
prg_email       = "Guenter.Partosch@hrz.uni-giessen,de"
prg_version     = "2.9.0"
prg_date        = "2022-02-23"
prg_inst        = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"

operatingsys    = platform.system()
call            = sys.argv

# ------------------------------------------------------------------
# Texts for argparse and help

author_template_text  = "Author template for package XML files to be loaded"
license_template_text = "License template for package XML files to be loaded"
key_template_text     = "Key template for package XML files to be loaded"
template_text         = "Name template for package XML files to be loaded"

author_text           = "Author of the program"
version_text          = "Version of the program"
output_text           = "Generic file name for output files"
number_text           = "Maximum number of file downloads"
direc_text            = "OS Directory for output files"
program_text          = "Loads XLM and PDF documentation files from CTAN a/o generates some special lists, and prepares data for CTANOut"

verbose_text          = "Flag: Output is verbose."
download_text         = "Flag: Downloads associated documentation files [PDF]."
lists_text            = "Flag: Generates some special lists and prepare files for CTANOut."
statistics_text       = "Flag: Prints statistics."
integrity_text        = "Flag: Checks the integrity of the 2nd .pkl file."
regenerate_text       = "Flag: Regenerates the two pickle files."

# -----------------------------------------------------------------    
# Defaults/variables for argparse

download_default         = False      # default for option -f    (no PDF download)
integrity_default        = False      # default for option -c    (no integrity check)
lists_default            = False      # default for option -n    (special lists are not generated)
number_default           = 250        # default for option -n    (maximum number of files to be loaded)
output_name_default      = "all"      # default for option -o    (generic file name)
statistics_default       = False      # default for option -stat (no statistics output)
template_default         = ""         # default for option -t    (name template for file loading)
author_template_default  = ""         # default for option -A    (author name template)
license_template_default = ""         # default for option -L    (license name template)
key_template_default     = ""         # default for option -k    (key template for file loading)
verbose_default          = False      # default for option -n    (output is not verbose)
regenerate_default       = False      # default for option -r    (no regeneration)

act_direc           = "."        
if operatingsys == "Windows":    
    direc_sep      = "\\"
else:
    direc_sep      = "/"
direc_default       = act_direc + direc_sep # default for -d (output OS directory)

download            = None       # option -f    (no PDF download)
integrity           = None       # option -c    (no integrity check)
lists               = None       # option -n    (special lists are not generated)
number              = 0          # option -n    (maximum number of files to be loaded)
output_name         = ""         # option -o    (generic file name)
statistics          = None       # option -stat (no statistics output)
template            = ""         # option -t    (name template for file loading)
author_template     = ""         # option -A    (author name template)
license_template    = ""         # option -L    (license name template)
key_template        = ""         # option -k    (key template) 
verbose             = None       # option -n    (output is not verbose)

# ------------------------------------------------------------------
# Dictionaries

authorpackages        = {}       # python dictionary: list of authors and their packages
licensepackages       = {}       # python dictionary: list of licenses and their packages
authors               = {}       # python dictionary: list of authors
packages              = {}       # python dictionary: list of packages
licenses              = {}       # python dictionary: list of licenses  
packagetopics         = {}       # python dictionary: list of packages and their topics
topics                = {}       # python dictionary: list of topics
topicspackage         = {}       # python dictionary: list of topics and their packages
XML_toc               = {}       # python dictionary: list of PDF files: XML_toc[href]=...PDF file
PDF_toc               = {}       # python dictionary: list of PDF files: PDF_toc[lfn]=...package file
all_XML_files         = ()       # list with all XML files
selected_packages_lpt = set()    # python dictionary: list of packages with selected topics
selected_packages_lap = set()    # python dictionary: list of packages with selected authors
selected_packages_llp = set()    # python dictionary: list of packages with selected licenses

# XML_toc
#   Structure:                 XML_toc[href] = (XML file, key, onename)
#   generated and changed in:  analyze_XML_file(file), check_integrity()
#   inspected in:              analyze_XML_file(file), check_integrity()
#   stored in pickle file:     generate_pickle2()
#   loaded from pickle file:   load_XML_toc()
#
# PDF_toc
#   Structure:                 PDF_toc[fkey + "-" + onename] = file
#   generated in:              get_PDF_files(d)
#   changed in                 analyze_XML_file(file), check_integrity()
#   inspected in:              check_integrity()

# 1st pickle file:
#   name:      CTAN.pkl
#   contains:  authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licensepackages
#
# 2nd pickle file:
#   name:      CTAN2.pkl
#   contains:  XML_toc

# ------------------------------------------------------------------
# Settings for wget (authors, packages, topics)

ctanUrl             = "https://ctan.org"                        # head of a CTAN url
ctanUrl2            = ctanUrl + "/tex-archive"                  # head of another CTAN url
call1               = "wget https://ctan.org/xml/2.0/"          # base wget call for authors, packages, ...
call2               = "wget https://ctan.org/xml/2.0/pkg/"      # base wget call for package files
parameter           = "?no-dtd=true --no-check-certificate -O " # additional parameter for wget

# ------------------------------------------------------------------ 
# other settings

pkl_file            = "CTAN.pkl" # name of 1st pickle file
pkl_file2           = "CTAN2.pkl"# name of 2nd pickle file

actDate             = time.strftime("%Y-%m-%d")# actual date of program execution
actTime             = time.strftime("%X")      # actual time of program execution

counter             = 0          # counter for downloaded XML files (in the actual session)
pdfcounter          = 0          # counter for downloaded PDF files (in the actual session)
pdfctrerr           = 0          # counter for not downloaded PDF files (in the actual session)
corrected           = 0          # counter of corrected entries in XML_toc (in the actual session)

ext                 = ".xml"     # file name extension for downloaded XML files
rndg                = 2          # optional rounding of float numbers
left                = 35         # width of labels in statistics
ellipse             = " ..."     # abbreviate texts
ok                  = None

reset_text          = "Info: '{0}' reset to {1} (due to {2})"
exclusion           = ["authors.xml", "topics.xml", "packages.xml", "licenses.xml"]

random.seed(time.time())         # seed for random number generation


# ==================================================================
# argparse
# parses options and processes them

parser = argparse.ArgumentParser(description = program_text + " [" + prg_name + "; " +
                                 "Version: " + prg_version + " (" + prg_date + ")]")
parser._positionals.title = 'Positional parameters'
parser._optionals.title   = 'Optional parameters'

parser.add_argument("-a", "--author",                      # Parameter -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = prg_author + " (" + prg_email + ", " + prg_inst + ")")

parser.add_argument("-A", "--author_template",             # Parameter -A/--author_template
                    help    = author_template_text + " - Default: " + "%(default)s",
                    dest    = "author_template",
                    default = author_template_default)

parser.add_argument("-c", "--check_integrity",             # Parameter -c/--check_integrity
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

parser.add_argument("-l", "--lists",                       # Parameter -l/--lists
                    help    = lists_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = lists_default)

parser.add_argument("-L", "--license_template",            # Parameter -L/--license_template
                    help    = license_template_text + " - Default: " + "%(default)s",
                    dest    = "license_template",
                    default = license_template_default)

parser.add_argument("-k", "--key_template",                # Parameter -k/--key_template
                    help    = key_template_text + " - Default: " + "%(default)s",
                    dest    = "key_template",
                    default = key_template_default)

parser.add_argument("-n", "--number",                      # Parameter -n/--number
                    help    = number_text + " - Default: " + "%(default)s",
                    dest    = "number",
                    default = number_default)

parser.add_argument("-o", "--output",                      # Parameter -o/--output
                    help    = output_text + " - Default: " + "%(default)s",
                    dest    = "output_name",
                    default = output_name_default)

parser.add_argument("-r", "--regenerate_pickle_files",     # Parameter -r/--regenerate_pickle_files
                    help    = regenerate_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = regenerate_default)

parser.add_argument("-t", "--template",                    # Parameter -t/--template
                    help    = template_text + " - Default: " + "%(default)s",
                    dest    = "template",
                    default = template_default)

parser.add_argument("-stat", "--statistics",               # Parameter -stat/--statistics
                    help    = statistics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics_default)

parser.add_argument("-v", "--verbose",                     # Parameter -v/--verbose
                    help    = verbose_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = verbose_default)

parser.add_argument("-V", "--version",                     # Parameter -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + prg_version + " (" + prg_date + ")")

# ------------------------------------------------------------------
# Getting parsed values

args            = parser.parse_args()                      # all parameters of programm call

author_template  = args.author_template                    # parameter -A
license_template = args.license_template                   # parameter -L
direc            = args.direc                              # parameter -d
download         = args.download_files                     # parameter -f
integrity        = args.check_integrity                    # parameter -c
key_template     = args.key_template                       # parameter -k
lists            = args.lists                              # parameter -l
number           = int(args.number)                        # parameter -n
regenerate       = args.regenerate_pickle_files            # parameter -r
statistics       = args.statistics                         # Parameter -stat
template         = args.template                           # parameter -k
verbose          = args.verbose                            # parameter -v

# ------------------------------------------------------------------
# Correct OS directory name, test OS directory existence, and install OS directory

direc              = direc.strip()                         # correct OS directory name (-d)
if direc[len(direc) - 1] != direc_sep:
    direc += direc_sep
if not path.exists(direc):
    try:
        os.mkdir(direc)
    except OSError:
        print ("- Warning: Creation of the directory '{0}' failed".format(direc))
    else:
        print ("- Info: Successfully created the directory '{0}' ".format(direc))
        
output_name        = direc + args.output_name              # parameter -d

# ------------------------------------------------------------------
# additional files, if you want to search topics a/a authors and their corr. packages

topicpackage_file   = output_name + ".lpt"                 # name of a the xyz.lpt file
authorpackage_file  = output_name + ".lap"                 # name of a the xyz.lap file
licensepackage_file = output_name + ".llp"                 # name of a the xyz.llp file

# ------------------------------------------------------------------
# special regular expressions

p2           = re.compile(template)                        # regular expression based on parameter -t
p3           = re.compile("^[0-9]{10}-.+[.]pdf$")          # regular expression for local PDF file names
p4           = re.compile("^.+[.]xml$")                    # regular expression for local XML file names
p5           = re.compile(key_template)                    # regular expression for topics
p6           = re.compile(author_template)                 # regular expression for author names
p7           = re.compile(license_template)                # regular expression for licenses


#===================================================================
# Auxiliary function

def fold(s):                                               # Function fold: auxiliary function: shortens long option values for output
    """auxiliary function: shortens long option values for output."""
    
    offset = 64 * " "
    maxlen = 70
    sep    = "|"                                           # separator for split
    parts  = s.split(sep)                                  # split s on sep                   
    line   = ""
    out    = ""
    for f in range(0, len(parts)):
        if f != len(parts) - 1:
            line = line + parts[f] + sep
        else:
            line = line + parts[f]
        if len(line) >= maxlen:
            out = out +line+ "\n" + offset
            line = ""
    out = out + line            
    return out


# ==================================================================
# Functions for main part

# ------------------------------------------------------------------
def analyze_XML_file(file):                                        # Function analyze_XML_file(file): Analyzes a XML package file for documentation (PDF) files
    """Analyzes a XML package file for documentation (PDF) files."""

    # analyze_XML_file --> dload_document_file

    global XML_toc                                                 # global Pythondirectory
    global PDF_toc                                                 # global Pythondirectory for PDF files

    error = False

    try:                                                           # try to open and parse a XML file
        f              = open(file, encoding="utf-8", mode="r")    # open the XML file
        onePackage     = ET.parse(f)                               # parse the XML file
        onePackageRoot = onePackage.getroot()                      # get root
    except:                                                        # parsing not successfull
        if verbose:
            print("------- Warning: local XML file for package '{0}' empty or not well-formed".format(file))
        error = True

    if not error:
        ll           = list(onePackageRoot.iter("documentation"))  # all documentation elements == all documentation childs

        for g in ll:                                               # loop: all documentation childs
            href = g.get("href", "")                               # href attribute
            if ".pdf" in href:                                     # there is ".pdf" in the string
                fnames  = re.split("/", href)                      # split this string at "/"
                href2   = href.replace("ctan:/", ctanUrl2)         # construct the correct URL
                if href in XML_toc:                                # href allready used?
                    (tmp, fkey, onename) = XML_toc[href]           # get the components
                else:                                              # href not allready used?
                    onename       = fnames[len(fnames) - 1]        # get the file name
                    fkey          = str(random.randint(1000000000, 9999999999)) # construct a random file name
                    XML_toc[href] = (file, fkey, onename)          # store this new file name
                if download:
                    if dload_document_file(href2, fkey, onename):  # load the PDF document
                        PDF_toc[fkey + "-" + onename] = file
        f.close()                                                  # close the analyzed XML file

# ------------------------------------------------------------------
def call_check():                                                 # Function call_check: Processes all necessary steps for a integrity check
    """Processes all necessary steps for a integrity check."""

    # call_check --> get_PDF_files
    # call_check --> dload_topics
    # call_check --> dload_authors
    # call_check --> dload_licenses
    # call_check --> dload_packages
    # call_check --> generate_topicspackage
    # call_check --> generate_pickle1
    # call_check --> generate_lists
    # call_check --> check_integrity

    global PDF_toc
    global XML_toc
    global authors
    global licenses
    global packages
    global topics
    global topicspackage, packagetopics, number, counter, pdfcounter

    get_PDF_files(direc)
    dload_topics()                                                # load the file topics.xml
    dload_authors()                                               # load the file authors.xml
    dload_licenses()                                              # load the file licenses.xml
    dload_packages()                                              # load the file packages.xml
    generate_topicspackage()                                      # generates topicspackage, ...
    thr3 = Thread(target=generate_pickle1)                        # dumps authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licensepackages
    thr3.start()
    thr3.join()
    
    if lists:                                                     # if lists are to be generated
        generate_lists()                                          #     generate x.loa, x.lop, x.lok, x.lol, x.lpt, x.lap, x.llp

    if integrity:                                                 # if the integrity is to be checked
        check_integrity()                                         #     when indicated: remove files or entries

# ------------------------------------------------------------------
def call_load():                                                  # Function call_load: Processes all steps for a complete ctanload call (without integrity check)
    """Processes all steps for a complete ctanout call (withoutb integrity check)."""

    # call_load --> get_PDF_files
    # call_load --> dload_topics
    # call_load --> dload_authors
    # call_load --> dload_licenses
    # call_load --> dload_packages
    # call_load --> load_XML_toc
    # call_load --> set_PDF_toc
    # call_load --> dload_XML_files
    # call_load --> generate_pickle1
    # call_load --> generate_pickle2
    # call_load --> get_xyz_lpt
    # call_load --> get_xyz_lap
    # call_load --> get_xyz_llp

    global PDF_toc
    global XML_toc
    global authors
    global licenses
    global packages
    global topics
    global topicspackage, number, counter, pdfcounter
    
    get_PDF_files(direc)
    load_XML_toc()
    set_PDF_toc()

    dload_topics()                                                # load the file topics.xml
    dload_authors()                                               # load the file authors.xml
    dload_licenses()                                              # load the file licenses.xml
    dload_packages()                                              # load the file packages.xml

    all_packages = set()                                          # initialize set
    for f in packages:
        all_packages.add(f)                                       # construct a set object (packages has not the right format)
        
    tmp_tp = all_packages.copy()                                  # initialize tmp_tp (topics)
    tmp_ap = all_packages.copy()                                  # initialize tmp_ap (authors)
    tmp_np = all_packages.copy()                                  # initialize tmp_np (names)
    tmp_lp = all_packages.copy()                                  # initialize tmp_lp (licenses)

    if (template != template_default):
        tmp_np = get_package_set()                                # analyze 'packages' for name templates
    if (key_template != key_template_default):
        tmp_tp = get_xyz_lpt()                                    # load xyz.lpt and analyze it for key templates
    if (author_template != author_template_default):
        tmp_ap = get_xyz_lap()                                    # load xyz.lap and analyze it for author templates
    if (license_template != license_template_default):
        tmp_lp = get_xyz_llp()                                    # load xyz.llp and analyze it for license templates

    tmp_pp = tmp_tp & tmp_ap & tmp_np & tmp_lp                    # built an intersection
    if len(tmp_pp) == 0:
        if verbose:
            print("--- Warning: no correct XML file for any specified package found")

    tmp_p  = sorted(tmp_pp)                                       # built an intersection

    dload_XML_files(tmp_p)                                        # load and processe all required XML files in series
        
    thr1 = Thread(target=generate_pickle2)                        # dump XML_toc via pickle file via thread
    thr1.start()
    thr1.join()
    generate_topicspackage()                                      # generates topicspackage, ...
    thr2 = Thread(target=generate_pickle1)                        # dump some lists to pickle file
    thr2.start()
    thr2.join()
    
# ------------------------------------------------------------------
def call_plain():                                                 # Function call_plain: Processes all steps for a plain call
    """Processes all steps for a plain call."""

    # call_plain --> get_PDF_files
    # call_plain --> dload_topics
    # call_plain --> dload_authors
    # call_plain --> dload_licenses
    # call_plain --> dload_packages
    # call_plain --> generate_topicspackage
    # call_plain --> generate_pickle1
    
    global PDF_toc
    global authors
    global licenses
    global packages
    global topics
    global topicspackage, packagetopics, authorpackages
    
    get_PDF_files(direc)
    dload_topics()                                                # load the file topics.xml
    dload_authors()                                               # load the file authors.xml
    dload_licenses()                                              # load the file licenses.xml
    dload_packages()                                              # load the file packages.xml
    generate_topicspackage()                                      # generate topicspackage, ...
    thr3 = Thread(target=generate_pickle1)                        # dump authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licensepackages (via thread)
    thr3.start()
    thr3.join()

# ------------------------------------------------------------------
def check_integrity(always=False):                                # Function check_integrity(): Checks integrity (tests for inconsistencies)
    """Checks integrity (tests for inconsistencies)."""

    # check_integrity --> load_XML_toc
    # check_integrity --> generate_pickle2
    # check_integrity --> verify_PDF_files

    global corrected                                              # number of corrections
    global PDF_toc                                                # PDF_toc, structure: PDF_toc[file] = fkey + "-" + onename
    global noerror
    global ok

    if verbose:
        print("--- Info: integrity check")
    load_XML_toc()                                                # load the 2nd pickle file (XML_toc)
                                                                  # XML_toc, structure: XML_toc[href] = (file, fkey, onename)
    noerror = True
    
    tmpdict = {}                                                  # for a copy of XML_toc
    for f in XML_toc:                                             # make a copy of XML_toc
        tmpdict[f] = XML_toc[f]

# ..................................................................
    for f in tmpdict:                                             # loop: all entries in a copy of XML_toc
        tmp  = tmpdict[f]
        xlfn = direc + tmp[0]                                     #    local file name for current XML file
        plfn = direc + tmp[1] + "-" + tmp[2]                      #    local file name for current PDF file
        xex  = os.path.isfile(xlfn)                               #    test: XLM file exists     
        pex  = os.path.isfile(plfn)                               #    test: PDF file exists

        if xex:                                                   #    XLM file exists
            if os.path.getsize(xlfn) == 0:                        #        but file is empty
                if verbose:
                    print("----- Warning: entry '{0}' in dictionary, but OS file is empty".format(xlfn))
                os.remove(xlfn)                                   #        OS file removed
                if verbose:
                    print("----- Warning: XML file '{0}' in OS deleted".format(xlfn))
                del XML_toc[f]                                    #        entry deleted
                if verbose:
                    print("----- Warning: entry '{0}' in dictionary deleted".format(xlfn))
                noerror = False                                   #        flag set
                corrected += 1                                    #        number of corrections increasedtuda-ci.xml
            else:                                                 #        XML file not empty
                if os.path.isfile(plfn):                          #            test: PDF file exists
                    if os.path.getsize(plfn) != 0:
                        PDF_toc[tmp[1] + "-" + tmp[2]] = tmp[0]   #            generate entry in PDF_toc
                    else:
                        if verbose:
                            print("----- Warning: entry '{0}' ({1}) in dictionary, but OS file is empty".format(plfn, tmp[0]))
                        os.remove(plfn)                           #            OS file removed
                        if verbose:
                            print("----- Warning: PDF file '{0}' in OS deleted".format(plfn))
                        del XML_toc[f]                            #            entry deleted
                        if verbose:
                            print("----- Warning: entry '{0}' in dictionary deleted".format(plfn))
                        noerror = False                           #            flag set
                        corrected += 1                            #            number of corrections increased
                else:
                    if verbose:
                        print("----- Warning: entry '{0}' ({1}) in dictionary, but PDF file not found".format(plfn, tmp[0]))
                    del XML_toc[f]                                #            entry deleted
                    if verbose:
                        print("----- Warning: entry '{0}' in dictionary deleted".format(plfn))
                    noerror = False                               #            flag set
                    corrected += 1                                #            number of corrections increased
        else:                                                     #     XML file does not exist
            print("----- Warning: entry '{0}' in dictionary, but OS file not found".format(xlfn))
            del XML_toc[f]                                        #         entry deleted
            print("----- Warning: entry '{0}' in dictionary deleted".format(xlfn))
            noerror   = False                                     #         flag set
            corrected += 1                                        #         number of corrections increased
            
    thr5 = Thread(target=verify_PDF_files)                        # check actualized PDF_toc; delete a PDF file if necessary
    thr5.start()
    thr5.join()

# ..................................................................
    if noerror and ok and (not always):                           # there is no error
        if verbose:
            print("----- Info: no error with integrity check")
    else:
        thr2 = Thread(target=generate_pickle2)                    #    generate a new version of the 2nd pickle file (via thread)
        thr2.start()
        thr2.join()

# ------------------------------------------------------------------
def dload_authors():                                       # Function dload_authors(): Downloads XML file 'authors' from CTAN and generates dictionary 'authors'
    """Downloads XML file 'authors' from CTAN and generates dictionary 'authors'."""

    global authors                                         # global Python dictionary with authors

    file    = "authors"                                    # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # load file 'authors'
        # wget https://ctan.org/xml/2.0/authors?no-dtd=true --no-check-certificate -O ./authors.xml
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()                                     # wait?

        if verbose:
            print("--- Info: XML file '{0}' downloaded ('{1}.xml' on PC)".format(file, direc + file))
        try:
            authorsTree  = ET.parse(file2)                 # parse the XML file 'authors.xml'
            authorsRoot  = authorsTree.getroot()           # get the root

            for child in authorsRoot:                      # all children
                key   = ""                                 # defaults
                id    = ""
                fname = ""
                gname = ""
                for attr in child.attrib:                  # three attributes: id, givenname, familyname
                    if str(attr) == "id":
                        key = child.attrib['id']           # attribute id
                    if str(attr) == "givenname":
                        gname = child.attrib['givenname']  # attribute givenname
                    if str(attr) == "familyname":
                        fname = child.attrib['familyname'] # attribute familyname
                authors[key] = (gname, fname)
            if verbose:
                print("----- Info: authors collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- Error: standard XML file '{0}' empty or not well-formed".format(file2))
            sys.exit("- Error: programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- Error: XML file '{0}' not downloaded".format(file))
        sys.exit("- Error: programm terminated")           # program terminated

# ------------------------------------------------------------------
def dload_document_file(href, key, name):                  # Function dload_document_file(href, key, name): Downloads one information file (PDF) from CTAN
    """Downloads one information file (PDF) from CTAN."""
    
    # to be improved

    global pdfcounter
    global pdfctrerr

    call     = "wget " + href + parameter + direc + key + "-" + name
    noterror = False

    # @wait: 17.5.3 in library
    try:                                                   # download the PDF file and store
        process = subprocess.Popen(call, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = process.communicate(timeout=50)       # wait?
        if "ERROR" in errs:                                # "ERROR" found in errs
            if verbose:
                print("------- Warning: PDF documentation file '{0}' not downloaded".format(name))
            pdfctrerr = pdfctrerr + 1
        else:
            if verbose:
                print("------- Info: PDF documentation file '{0}' downloaded".format(name))
                print("------- Info: unique local file name: '{0}'".format(direc + key + "-" + name))
            pdfcounter = pdfcounter + 1                    # number of downloaded PDF files incremented
            noterror = True
    except:                                                # download was not successfull
        process.kill()                                     # kill the process
        outs, errs = process.communicate()                 # output and error messages
        if verbose:
            print("------- Warning: PDF documentation file '{0}' not downloaded".format(name))
    return noterror

# ------------------------------------------------------------------
def dload_licenses():                                      # Function dload_licenses: Downloads XML file 'licenses' from CTAN and generates dictionary 'licemses'
    """Downloads XML file 'licenses' from CTAN and generates dictionary 'licemses'."""

    global licenses                                        # global Python dictionary with licenses

    file    = "licenses"                                   # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # loads file .../licenses
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()                                     # wait?

        if verbose:
            print("--- Info: XML file '{0}' downloaded ('{1}.xml' on PC)".format(file, direc + file))
        try:
            licensesTree   = ET.parse(file2)               # parse the XML file 'topics.xml'
            licensesRoot   = licensesTree.getroot()        # get the root

            for child in licensesRoot:                     # all children in 'licenses'
                key   = ""                                 # defaults
                name  = ""
                free  = ""
                for attr in child.attrib:                  # three attributes: key, name, free
                    if str(attr) == "key":
                        key = child.attrib['key']          # attribute key
                    elif str(attr) == "name":
                        name = child.attrib['name']        # attribute name
                    elif str(attr) == "free":
                        free = child.attrib['free']        # attribute free
                licenses[key] = (name, free)
            licenses["noinfo"]      = ("noinfo", "")       # correction; not in lincenses.xml
            licenses["collection"]  = ("collection", "")   # correction; not in lincenses.xml
            licenses["digest"]      = ("digest", "")       # correction; not in lincenses.xml
            if verbose:
                print("----- Info: licenses collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- Error: standard XML file '{0}' empty or not well-formed".format(file))
            sys.exit("--- Error: programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- Error: XML file '{0}' not downloaded".format(file))
        sys.exit("- Error: programm terminated")           # program terminated

# ------------------------------------------------------------------
def dload_packages():                                      # Function dload_packages: Downloads XML file 'packages' from CTAN and generates dictionary 'packages'
    """Downloads XML file 'packages' from CTAN and generates dictionary 'packages'."""

    global packages                                        # global Python dictionary with packages

    file    = "packages"                                   # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # loads file .../packages
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()                                     # wait?

        if verbose:
            print("--- Info: XML file '{0}' downloaded ('{1}.xml' on PC)".format(file, direc + file))
        try:                                               # parses 'packages' tree
            packagesTree = ET.parse(file2)                 # parse the XML file 'packages.xml'
            packagesRoot = packagesTree.getroot()          # get the root

            for child in packagesRoot:                     # all children in 'packages'
                key     = ""                               # defaults
                name    = ""
                caption = ""
                for attr in child.attrib:                  # three attributes: key, name, caption
                    if str(attr) == "key":
                        key = child.attrib['key']          # attribute key
                    if str(attr) == "name":
                        name = child.attrib['name']        # attribute name
                    if str(attr) == "caption":
                        caption = child.attrib['caption']  # attribute caption
                packages[key] = (name, caption)
            if verbose:
                print("----- Info: packages collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- Error: standard XML file '{0}' empty or not well-formed".format(file2))
            sys.exit("--- Error: programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- Error: XML file '" + file + "' not downloaded".format(file))
        sys.exit("- Error: programm terminated")           # program terminated

# ------------------------------------------------------------------
def dload_topics():                                        # Function dload_topics(): Downloads XML file 'topics' from CTANB and generates dictionary 'topics'
    """Downloads XML file 'topics' from CTAN and generates dictionary 'topics'."""

    global topics                                          # global Python dictionary with topics

    file    = "topics"                                     # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # loads file .../topics
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()                                     # wait?

        if verbose:
            print("--- Info: XML file '{0}' downloaded ('{1}.xml' on PC)".format(file, direc + file))
        try:
            topicsTree   = ET.parse(file2)                 # parse the XML file 'topics.xml'
            topicsRoot   = topicsTree.getroot()            # get the root

            for child in topicsRoot:                       # all children in 'topics'
                key     = ""                               # defaults
                name    = ""
                details = ""
                for attr in child.attrib:                  # two attributes: name, details
                    if str(attr) == "name":
                        key = child.attrib['name']         # attribute name
                    if str(attr) == "details":
                        details = child.attrib['details']  # attribute details
                topics[key] = details
            if verbose:
                print("----- Info: topics collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- Error: standard XML file '{0}' empty or not well-formed".format(file))
            sys.exit("--- Error: programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- Error: '{0}' not downloaded".format(file))
        sys.exit("- Error: programm terminated")           # program terminated

# ------------------------------------------------------------------
def dload_XML_files(p):                                            # Function dload_XML_files: Downloads XML package files
    """Downloads XML package files.

    p: packages/selected_packages"""

    # dload_XML_file --> analyze_XML_file

    global topicspackage, number, counter, pdfcounter

    for f in p:                                                    # all packages found in 'packages'
        if p2.match(f) and (counter + pdfcounter < number):        # file name matches template
            counter = counter + 1
            callx   = call2 + f + parameter + direc + f + ext      # wget https://ctan.org/xml/2.0/pkg/xyz --no-check-certificate -O xyz.xml

            try:                                                   # try to download the XML file (packages)
                process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
                process.wait()                                     # wait ?

                if verbose:
                    print("----- Info: XML file for package '{0}' downloaded ('{1}.xml' on PC)".format(f, direc + f))
                analyze_XML_file(f + ext)                          # if download is set: analyze the associated XML file
            except FileNotFoundError:                              # download was not successfull
                if verbose:
                    print("----- Warning: XML file for package '{0}' not downloaded".format(f))

    if counter + pdfcounter >= number:                             # limit for downloaded files
        if verbose:
            print("--- Warning: maximum number ({0}) of downloaded XML+PDF files exceeded".format(str(counter + pdfcounter)))

# ------------------------------------------------------------------
def generate_lists():                                              # Function generate_lists: Generates some special files (with lists):
                                                                   # xyz.loa (list of authors), xyz.lop (list of packages), xyz.lok (list of topics),
                                                                   # xyz.lpt (list of topics and associated packages), xyz.lol file (list of licenses),
                                                                   # xyz.lap file (list of authors and associated packages)
                                                                   # xyz.llp file (list of licenses and associated packages)
    """Generates some special files (with lists):
    generates xyz.loa file (list of authors)
    generates xyz.lop file (list of packages)
    generates xyz.lok file (list of topics)
    generates xyz.lol file (list of licenses)
    generates xyz.lpt file (list of topics and associated packages)
    generates xyz.lap file (list of authors and associated packages)
    generates xyz.llp file (list of licenses and associated packages)."""

    # .................................................
    # generate xyz.loa file (list of authors)

    loa_file = output_name + ".loa"

    loa = open(loa_file, encoding="utf-8", mode="w")              # open xyz.loa file
    for f in authors:                                             # loop
        loa.write(str(authors[f]) + "\n")

    if verbose:
        print("--- Info: file '" + loa_file + "' (list of authors) generated")
    loa.close()                                                   # close xyz.loa file

    # .................................................
    # generate xyz.lop file (list of packages)

    lop_file = output_name + ".lop"

    lop = open(lop_file, encoding="utf-8", mode="w")              # open xyz.lop file
    for f in packages:                                            # loop
        lop.write(str(packages[f]) + "\n")

    if verbose:
        print("--- Info: file '" + lop_file + "' (list of packages) generated")
    lop.close()                                                   # close xyz.lop file

    # .................................................
    # generate xyz.lok file (list of topics)

    lok_file = output_name + ".lok"

    lok = open(lok_file, encoding="utf-8", mode="w")              # open xyz.lok file
    for f in topics:                                              # loop
        lok.write("('" + f + "', '" + str(topics[f]) + "')\n")

    if verbose:
        print("--- Info: file '" + lok_file + "' (list of topics) generated")
    lok.close()                                                   # close xyz.lok file

    # .................................................
    # generate xyz.lol file (list of licenses)

    lol_file = output_name + ".lol"

    lol = open(lol_file, encoding="utf-8", mode="w")              # open xyz.lol file
    for f in licenses:                                            # loop
        lol.write("('" + f + "', '" + str(licenses[f]) + "')\n")

    if verbose:
        print("--- Info: file '" + lol_file + "' (list of licenses) generated")
    lol.close()                                                   # close xyz.lol file

    # .................................................
    # generate xyz.lpt file (list of topics and associated packages)

    lpt_file = output_name + ".lpt"

    lpt = open(lpt_file, encoding="utf-8", mode="w")              # open xyz.lpt file
    for f in topicspackage:                                       # loop
        lpt.write("('" + f + "', " + str(topicspackage[f]) + ")\n")

    if verbose:
        print("--- Info: file '" + lpt_file + "' (list of topics and associated packages) generated")
    lpt.close()                                                   # close xyz.lpt file

    # .................................................
    # generate xyz.lap file (list of authors and associated packages)

    lap_file = output_name + ".lap"

    lap = open(lap_file, encoding="utf-8", mode="w")              # open xyz.lap file
    for f in authorpackages:                                      # loop
        lap.write("('" + str(f) + "', " + str(authorpackages[f]) + ")\n")

    if verbose:
        print("--- Info: file '" + lap_file + "' (list of authors and associated packages) generated")
    lap.close()                                                   # close xyz.lap file

    # .................................................
    # generate xyz.llp file (list of licenses and associated packages)

    llp_file = output_name + ".llp"

    llp = open(llp_file, encoding="utf-8", mode="w")              # open xyz.llp file
    for f in licensepackages:                                     # loop
        llp.write("('" + f + "', " + str(licensepackages[f]) + ")\n")

    if verbose:
        print("--- Info: file '" + llp_file + "' (list of licenses and associated packages) generated")
    llp.close()                                                   # close xyz.llp file

# ------------------------------------------------------------------
def generate_pickle1():                                           # Function generate_pickle1: pickle dump:
                                                                  # actual authors, packages, licenses, topics, topicspackage, packagetopics, authorpackages, licensepackages
    """pickle dump: 
    actual authors, packages, licenses, topics, topicspackage, packagetopics, licensepackages"""

    # authors: Python dictionary (sorted)
    #   each element: [author key]: <tuple with givenname and familyname>
    #
    # packages: Python dictionary (sorted)
    #   each element: [package key]: <tuple with package name and package title>
    #
    # licenses: Python dictionary (sorted)
    #   each element: [license key]: <license title>
    #
    # topics: Python dictionary (sorted)
    #   each element: [topics name]: <topics title>
    #
    # topicspackage: Python dictionary (unsorted)
    #   each element: [topic key]: <list with package names>
    #
    # packagetopics: Python dictionary (sorted)
    #   each element: [topic key]: <list with package names>
    #
    # authorpackages: Python dictionary (unsorted)
    #   each element: [author key]: <list with package names>
    #
    # licensepackages: Python dictionary (mostly sorted)
    #   each element: [license key]: <list with package names>

    pickle_name1  = direc + pkl_file                              # path of the pickle file
    pickle_file1  = open(pickle_name1, "bw")                      # open the pickle file
    pickle_data1  = (authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licensepackages)
    pickle.dump(pickle_data1, pickle_file1)                       # dump the data
    pickle_file1.close()                                          # close the file
    if verbose:
        print("--- Info: pickle file '{0}' written".format(pickle_name1))

# ------------------------------------------------------------------
def generate_pickle2():                                           # Function generate_pickle2: pickle dump: actual XML_toc (list with download information files
    """pickle dump:
    needs actual XML_toc
    XML_toc       : list with download information files"""

    pickle_name2  = direc + pkl_file2
    try:
        pickle_file2  = open(pickle_name2, "bw")                  # open the 2nd .pkl file
        pickle_data2  = XML_toc                                   # prepare the data
        pickle.dump(pickle_data2, pickle_file2)                   # dump the data
        pickle_file2.close()                                      # close the file
        if verbose:
            print("--- Info: pickle file '{0}' written".format(pickle_name2))
    except:                                                       # not successfull
        if verbose:
            print("--- Warning: pickle file '{0}' cannot be loaded a/o written".format(pickle_name2))

# ------------------------------------------------------------------
def generate_topicspackage():                                       # Function generate_topicspackage:
                                                                    # Generates topicspackage, packagetopics, authorpackages, and licensepackages.
    """Generates topicspackage, packagetopics, authorpackages, and licensepackages."""

    global topicspackage
    global packagetopics
    global authorpackages
    global licensepackages

    for f in packages:                                              # all package XML files are loaded in series
        try:                                                        # try to open and parse file
            fext = f + ext                                          # file name (with extension)
            ff = open(fext, encoding="utf-8", mode="r")

            try:
                onePackage     = ET.parse(fext)                     # parse the XML file
                onePackageRoot = onePackage.getroot()               # get root
                kk             = list(onePackageRoot.iter("keyval"))    # all keyval elements
                aa             = list(onePackageRoot.iter("authorref")) # all authorref elements
                ll             = list(onePackageRoot.iter("license"))   # all license elements
                

                for i in kk:                                        # in keyval: 1 attribute: value
                    key = i.get("value", "")                        # attribute value
                    if key in topicspackage:
                        topicspackage[key].append(f)
                    else:
                        topicspackage[key] = [f]

                    if f in packagetopics:
                        packagetopics[f].append(key)
                    else:
                        packagetopics[f] = [key]

                for j in aa:                                        # in authorref: 4 attributes: givenname, familyname, key, id
                    key1 = j.get("givenname", "")                   # attribute givenname
                    key2 = j.get("familyname", "")                  # attribute familyname
                    key3 = j.get("key", "")                         # attribute key
                    key4 = j.get("id", "")                          # attribute id
                    if key4 != "":
                        key3 = key4
                    if key3 in authorpackages:
                        authorpackages[key3].append(f)
                    else:
                        authorpackages[key3] = [f]

                for k in ll:
                    key5 = k.get("type", "")
                    key6 = k.get("free", "")
                    if key5 in licensepackages:
                        licensepackages[key5].append(f)
                    else:
                        licensepackages[key5] = [f]
            except:                                                 # parsing was not successfull
                if verbose:
                    print("----- Warning: local XML file for package '{0}' empty or not well-formed".format(f))
            ff.close()
        except FileNotFoundError:                                   # file not downloaded
            if verbose and integrity:
                print("----- Warning: local XML file for package '" + f + "' not found".format(f))
    if verbose:
        print("--- Info: packagetopics, topicspackage, authorpackage collected")

# ------------------------------------------------------------------
def get_xyz_lpt():                                                 # Function get_xyz_lpt: Loads and analyzes xyz.lpt for topic templates
    """Loads and analyzes xyz.lpt for topic templates."""

    global number, counter, pdfcounter

    try:
        f = open(topicpackage_file, encoding="utf-8", mode="r")    # open file
        for line in f:
            top, pack=eval(line.strip())
            if p5.match(top):                                      # collect packages with specified topics
                for g in pack:
                    selected_packages_lpt.add(g)
        f.close()                                                  # close file
    except IOError:
        if verbose:                                                # there is an error
            print("- Error: local file '{0}' cannot be loaded; please call ctanload -l ... before".format(topicpackage_file))
        sys.exit()                                                 # program terminates
    if len(selected_packages_lpt) == 0:
        if verbose:
            print("--- Warning: no package found which matches the specified {0} template '{1}'".format("topic", key_template))
    return selected_packages_lpt

# ------------------------------------------------------------------
def get_xyz_llp():                                                 # Function get_xyz_llp: Loads and analyzes xyz.llp for liocense templates
    """Loads and analyzes xyz.llp for liocense templates."""

    global number, counter, pdfcounter

    try:
        f = open(licensepackage_file, encoding="utf-8", mode="r")  # open file
        for line in f:
            lic, pack = eval(line.strip())
            lic2      = licenses[lic][0]
            lic3      = licenses[lic][1]
            if lic3 == "true":
                lic3 = "free"
            else:
                lic3 = "not free"
            if p7.match(lic2) or p7.match(lic) or p7.match(lic3):  # collect packages with specified licenses
                for g in pack:
                    selected_packages_llp.add(g)
        f.close()                                                  # close file
    except IOError:
        if verbose:                                                # there is an error
            print("- Error: local file '{0}' cannot be loaded; please call ctanload -l ... before".format(licensepackage_file))
        sys.exit()                                                 # program terminates
    if len(selected_packages_llp) == 0:
        if verbose:
            print("--- Warning: no package found which matches the specified {0} template '{1}'".format("license", license_template))
    return selected_packages_llp

# ------------------------------------------------------------------
def get_xyz_lap():                                                 # Function get_xyz_lap: Loads and analyzes xyz.lap for author templates
    """Loads and analyzes xyz.lap for author templates."""

    global number, counter, pdfcounter

    try:
        f = open(authorpackage_file, encoding="utf-8", mode="r")   # open file
        for line in f:
            auth, pack=eval(line.strip())                          # get the items author and package
            if authors[auth][1] != "":                             # extract author's familyname
                auth2 = authors[auth][1]
            else:
                auth2 = authors[auth][0]
            if p6.match(auth2):                                    # collect packages with specified authors
                for g in pack:
                    selected_packages_lap.add(g)
        f.close()                                                  # close file
    except IOError:
        if verbose:                                                # there is an error
            print("- Error: local file '{0}' cannot be loaded; please call ctanload -l ... before".format(authorpackage_file))
        sys.exit()                                                 # program terminates
    if len(selected_packages_lap) == 0:
        if verbose:
            print("--- Warning: no package found which matches the specified {0} template '{1}'".format("author", author_template))
    return selected_packages_lap

# ------------------------------------------------------------------
def get_package_set():                                            # Function get_package_set: Analyzes dictionary 'packages' for name templates
    """Analyzes dictionary 'packages' for name templates."""
    
    tmp = set()
    for f in packages:
        if p2.match(f):
            tmp.add(f)
    if len(tmp) == 0:
        if verbose:
            print("--- Warning: no package found which matches the specified {0} template '{1}'".format("name", template))
    return tmp

# ------------------------------------------------------------------
def get_PDF_files(d):                                             # Function get_PDF_files(d): Lists all PDF files in a specified OS directory
    """Lists all PDF files in the specified OS directory d.

    d: directory"""

    global PDF_toc

    tmp  = os.listdir(d)                                          # get OS directory list
    tmp2 = {}
    for f in tmp:                                                 # all PDF files in current OS directory
        if p3.match(f):                                           #    check: file name matches p3
            tmp2[f] = ""                                          #    presets with empty string
    PDF_toc = tmp2

# ------------------------------------------------------------------
def get_XML_files(d):                                             # Function get_XML_files: Lists all XML files in the current OS directory
    """Lists all XML files in the current OS directory d"""

    tmp  = os.listdir(d)                                          # get OS directory list
    tmp2 = []
    
    for f in tmp:
        if p4.match(f) and not f in exclusion:
            tmp2.append(f)
    return tmp2

# ------------------------------------------------------------------
def load_XML_toc():                                                # Function load_XML_toc(): Loads pickle file 2 (which contains XML_toc)
    """Loads pickle file 2 (which contains XML_toc)."""

    global XML_toc                                                 # global Python dictionary

    try:
        pickleFile2 = open(direc + pkl_file2, "br")                # open the pickle file
        XML_toc     = pickle.load(pickleFile2)                     # unpickle the data
        pickleFile2.close()
    except IOError:                                                # not successfull
        pass                                                       # do nothing

# ------------------------------------------------------------------
def main():                                                        # Function main(): Main Function (calls the other functions)
    """Main Function (calls the other functions)"""

    # main --> call_plain
    # main --> call_check
    # main --> call_load
    # main --> make_statistics
    # main --> regenerate_pickle_files
    # main --> check_integrity

    global PDF_toc
    global download
    global lists
    global integrity
    global number
    global template
    global author_template
    global regenerate

    starttotal  = time.time()                                       # begin of time measure
    startprocess= time.process_time()
    reset_text  = "- Warning: '{0}' reset to {1} (due to {2})"
    call[0]     = "CTANLoad.py"

    n_bool    = template != template_default
    k_bool    = key_template != key_template_default
    a_bool    = author_template != author_template_default
    l_bool    = license_template != license_template_default
    i_bool    = integrity != integrity_default
    r_bool    = regenerate != regenerate_default
      
    load      = n_bool or k_bool or a_bool or l_bool                # load 
    check     = (not load) and ((lists != lists_default) or i_bool) # check
    newpickle = (not load) and (not check) and r_bool               # newpickle
    plain     = (not load) and (not check) and (not newpickle)      # plain
    
    if verbose:
        print("- Info: Program call:", call)

    if load:                                                        # load mode
        if (lists != lists_default):                                #     -l reset
            lists = False
            if verbose:
                print(reset_text.format("-l",False,"'-n' or '-t' or '-f'"))                                                      
        if (integrity != integrity_default):                        #     -c reset
            integrity = False
            if verbose:
                 print(reset_text.format("-c",False,"'-n' or '-t' or '-f'"))
        if (regenerate != regenerate_default):                      #     -r reset
            regenerate = False
            if verbose:
                print(reset_text.format("-r", False, "'-n' or '-t' or '-f'"))

    if check:                                                       # check mode
        if (regenerate != regenerate_default):                      #     -r reset
            regenerate = False
            if verbose:
                print(reset_text.format("-r", False, "'-l' or '-c'"))

    if newpickle:                                                   # newpickle mode
        if number == number_default:
            number  = 3000                                          #     -n reset
            if verbose:
                print(reset_text.format("-n", 3000, "'-r'"))
        if download == download_default:
            download = True                                         #     -f reset
            if verbose:
                print(reset_text.format("-f", True, "'-r'"))
        
    if verbose:                                                     # output on terminal (options in call)
        print("\n- Info: Program call (with more details): CTANLoad.py")    
        if (download != download_default):                print("  {0:5} {1:55}".format("-f", "(" + download_text + ")"))
        if (lists != lists_default):                      print("  {0:5} {1:55}".format("-l", "(" + (lists_text + ")")[0:50] + ellipse))
        if (regenerate != regenerate_default):            print("  {0:5} {1:55}".format("-r", "(" + regenerate_text + ")"))
        if (statistics != statistics_default):            print("  {0:5} {1:55}".format("-stat", "(" + statistics_text + ")"))
        if (integrity != integrity_default):              print("  {0:5} {1:55}".format("-c", "(" + integrity_text + ")"))
        if (verbose != verbose_default):                  print("  {0:5} {1:55}".format("-v", "(" + verbose_text + ")"))
        if (direc != direc_default):                      print("  {0:5} {2:55} {1}".format("-d", direc, "(" + direc_text + ")"))
        if (number != number_default):                    print("  {0:5} {2:55} {1}".format("-n", number, "(" + number_text + ")"))
        if (output_name != direc + output_name_default):  print("  {0:5} {2:55} {1}".format("-o", args.output_name, "(" + output_text + ")"))
        if (template != template_default):                print("  {0:5} {2:55} {1}".format("-t", fold(template), "(" + template_text + ")"))
        if (key_template != key_template_default):        print("  {0:5} {2:55} {1}".format("-k", fold(key_template), "(" + key_template_text + ")"))
        if (author_template != author_template_default):  print("  {0:5} {2:55} {1}".format("-A", fold(author_template), "(" + author_template_text + ")"))
        if (license_template != license_template_default):print("  {0:5} {2:55} {1}".format("-L", fold(license_template), "(" + license_template_text + ")"))
        print("\n")

    if plain:                                                       # Process all steps for a plain call.
        call_plain()
    elif load:                                                      # Process all steps for a complete ctanout call (withoutb integrity check).
        call_load()
    elif check:                                                     # Process all necessary steps for a integrity check.
        call_check()
    elif newpickle:                                                 # Regenerate the two pickle files.
        regenerate_pickle_files()
        check_integrity(always=True)
    else:
        pass

    if verbose:
        print("- Info: program successfully completed")

    if statistics:                                                  # if statistics are to be output
        make_statistics()

        endtotal   = time.time()                                    # end of time measure
        endprocess = time.process_time()
        print("--")
        print("total time: ".ljust(left + 1), round(endtotal-starttotal, rndg))
        print("process time: ".ljust(left + 1), round(endprocess-startprocess, rndg))

# ------------------------------------------------------------------
def make_statistics():                                            # Function make_statistics(): Prints statistics on terminal
    """Prints statistics on terminal."""

    global counter, pdfcounter

    l         = left
    r         = 5
    load      = (template != "")
    nrXMLfile = 0

    XMLdir = os.listdir(direc)
    for f in XMLdir:
        if p4.match(f):
            nrXMLfile += 1

    print("\nStatistics:")
    print("date/time:".ljust(l + 1), actDate, actTime)
    print("total number of authors on CTAN:".ljust(l), str(len(authors)).rjust(r))
    print("total number of topics on CTAN:".ljust(l), str(len(topics)).rjust(r))
    print("total number of packages on CTAN:".ljust(l), str(len(packages)).rjust(r))
    print("total number of licenses on CTAN:".ljust(l), str(len(licenses)).rjust(r))
    if download:
        print("number of downloaded XML files:".ljust(l), str(counter).rjust(r), "(in the actual session)")
        print("number of downloaded PDF files:".ljust(l), str(pdfcounter).rjust(r), "(in the actual session)")
        print("number of not downloaded PDF files:".ljust(l), str(pdfctrerr).rjust(r), "(in the actual session)")
    print("total number of local PDF files:".ljust(l), str(len(PDF_toc)).rjust(r))
    print("total number of local XML files:".ljust(l), str(nrXMLfile).rjust(r))
    if integrity:
        print("number of corrected entries:".ljust(l), str(corrected).rjust(r), "(in the actual session)")

# ------------------------------------------------------------------
def regenerate_pickle_files():                                  # Function regenerate_pickle_files: Regenerates corrupted pickle files
    """Regenerates corrupted pickle files."""

    global XML_toc
    global PDF_toc
    global authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licensepackages

    # generate_pickle_files --> get_PDF_files
    # generate_pickle_files --> dload_authors
    # generate_pickle_files --> dload_packages
    # generate_pickle_files --> dload_topics
    # generate_pickle_files --> dload_licenses
    # generate_pickle_files --> generate_topicspackage
    # generate_pickle_files --> analyze_XML_file
    # generate_pickle_files --> generate_pickle2
    # generate_pickle_files --> generate_pickle1
    # generate_pickle_files --> get_XML_files
    
# .................................................................
# Regeneration of CTAN2.pkl
# CTAN2.pkl needs XML_toc
    
    if verbose:
        print("--- Info: Regeneration of '{0}'".format(direc + pkl_file2))
        
    get_PDF_files(direc)
    dload_authors()                                               # load authors
    dload_packages()                                              # load packages
    dload_topics()                                                # load topics
    dload_licenses()                                              # load licenses
    generate_topicspackage()                                      # generate topicspackage, packagetopics, authorpackages, liocensepackages
    
    for f in get_XML_files(direc):
        if verbose:
            print("----- Info: local XML file '{0}'".format(direc + f))
        analyze_XML_file(f)

    thr1 = Thread(target=generate_pickle2)                        # dump XML_toc info CTAN2.pkl
    thr1.start()
    thr1.join()
    
# .................................................................
# Regeneration of CTAN1.pkl
# CTAN2.pkl needs authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages

    if verbose:
        print("--- Info: Regeneration of '{0}'".format(direc + pkl_file))
    
    thr2 = Thread(target=generate_pickle1)                        # dump authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licdensepackages into CTAN1.pkl
    thr2.start()
    thr2.join()
    
# ------------------------------------------------------------------
def set_PDF_toc():                                                # set_PDF_toc: Fills PDF_toc on the basis of XML_Toc
    """Fills PDF_toc on the basis of XML_toc."""
    
    global PDF_toc
    global XML_toc
    
    for f in XML_toc:
        (xlfn, fkey, plfn) = XML_toc[f]
        if os.path.exists(direc + xlfn) and os.path.exists(direc + fkey + "-" + plfn):
            PDF_toc[fkey + "-" + plfn] = xlfn
        else:
            pass

# ------------------------------------------------------------------
def verify_PDF_files():                                           # Function verify_PDF_files: Checks actualized PDF_toc; deletes a PDF file if necessary
    """Checks actualized PDF_toc; deletes a PDF file if necessary."""
    
    global ok
    global PDF_toc
    global corrected
    
    ok = True
    for g in PDF_toc:                                             # loop: move through PDF files
        if PDF_toc[g] == "":                                      #    no entry: no ass. XML file
            ok = False
            if verbose:
                print("----- Warning: PDF file '{0}' without associated XML file".format(g))
            if os.path.isfile(g):                                 #    g is file
                os.remove(g)                                      #         delete the PDF file (if it exists)
                corrected += 1                                    #         number of corrections increased
                if verbose:
                    print("----- Warning: PDF file '{0}' in OS deleted".format(g))
        else:
            pass


# ==================================================================
# Main part

# script --> main

if __name__ == "__main__":
    main()
else:
    if verbose:
        print("- Error: tried to use the program indirectly")


# ==================================================================
# Es fehlen noch  bzw. Probleme:
# - unterschiedliche Verzeichnisse für XML- und PDF-Dateien? (-)
# - GNU-wget ersetzen durch python-Konstrukt; https://pypi.org/project/python3-wget/ (geht eigentlich nicht)(-)
# - Fehler bei -r; es wird jedesmal CTAN.pkl neu gemacht (?)
# - irgenein Fehler: crimsonpro fehlt c:\users\guent\documents\python\ctan
# - neues feature: alle ungladenen Pakete laden (?)
# - Auswahl nach Datum (?)
# - später: get_CTAN_lap und get_CTAN_lpt umstellen auf direkte CTAN-Abfrage
# - neu machen: Funktionshierarchie, Beispiele, Übersicht über Meldungen

# - Auswahl auch nach Autor? CTAN.lap oder authorpackages; for f in authorpackages: print(authors[f][1], authorpackages[f]) (x)
# - Meldungen überarbeitet (x)

# ------------------------------------------------------------------
# History
#
# 2.0.0  2019-10-01 completely revised
# 2.0.1  2019-10-03 smaller changes: messages + command parsing
# 2.0.2  2019-10-04 smaller changes: messages
# 2.0.3  2019-11-26 smaller change: error message and parameter -n
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
# 2.0.16 2021-05-20 OS directory + separator improved
# 2.0.17 2021-05-21 more details in verbose mode
# 2.0.18 2021-05-23 OS directory name improved
# 2.0.19 2021-05-24 OS directory handling improved (existance, installation) 
# 2.1.0  2021-05-26 load licences, make corr. directory and file; expand CTAN.pkl
# 2.1.1  2021-05-26 correction for not-existing keys in licenses.xml
# 2.1.2  2021-06-07 smaller improvements in check_integrity
# 2.2.0  2021-06-08 new approach in check_integrity
# 2.3.0  2021-06-09 some funcion calls as threads
# 2.3.1  2021-06-12 auxiliary function fold: shorten long option values for output
# 2.3.2  2021-06-14 messages classified: Warnings, Error, Info
# 2.3.3  2021-06-14 str.format(...) used (if applicable); ellipses used to shorten some texts
# 2.3.4  2021-06-15 main function new structured
# 2.3.5  2021-06-18 output (options in program call) enhanced
# 2.3.6  2021-06-18 new function verify_PDF_files: check actualized PDF_toc; delete a PDF file if necessary
# 2.3.7  2021-06-19 main function more modularized; new functions call_plain, call_load, call_check
# 2.3.8  2021-06-22 error corrections and improvements for the handling von PDF_toc and XML_toc
# 2.4.0  2021-06-23 regeneration of pickle file enabled: new option -r; new functions regenerate_pickle_files and get_XML_files
# 2.4.1  2021-06-24 error handling in the check_integrity context changed
# 2.4.2  2021-06-26 handling of -r changed
# 2.5.0  2021-06-30 add. option -k; add. function get_CTAN_lpt (needs CTAN.lpt)
# 2.5.1  2021-07-01 minor corrections
# 2.5.2  2021-07-05 function fold restructured
# 2.5.3  2021-07-06 pickle file 1 is generated, too
# 2.6.0  2021-07-11 search of packages with author name template; new option -A; new function get_CTAN_lap (needs CTAN.lap)
# 2.6.1  2021-07-12 some corrections in the handling of -t / -k and -A
# 2.6.2  2021-07-15 more corrections in the handling of -t / -k and -A
# 2.7.0  2021-07-26 combined filtering new organized; new function get_package_set; 2 additional warning messages
# 2.7.1  2022-02-02 attribute free in licenses.xml; changes in dload_licenses
# 2.7.2  2022-02-03 changes in get_CTAN_lap and get_CTAN_lpt; now on the basis of all.(lap, lpt); additional adjustments
# 2.7.3  2022-02-04 functions renamed: get_CTAN_lap --> get_xyz_lap, get_CTAN_lpt --> get_xyz_lpt
# 2.8.0  2022-02-16 new option -L; new section in argparse; new variables license_template_text, license_template_default, license_template
# 2.8.1  2022-02-16 changes in generate_lists; creates xyz.llp
# 2.8.2  2022-02-16 changes in generate_topicspackage; creates Python dictionary licensepackages
# 2.8.3  2022-02-16 changes in generate_pickle1: CTAN.pkl extended: now with new component licensepackages
# 2.8.4  2022-02-16 new function get_xyz_llp; loads and analyzes xyz.llp; allows license searching with title, shorttitle, and free/not free
# 2.8.5  2022-02-17 changes in call_check, call_load, and main; respects license searching
# 2.8.6  2022-02-18 changes for -stat; changes in make_statistics
# 2.8.7  2022-02-18 messages in get_xyz_lap, get_xyz_lpt, and get_xyz_llp changed
# 2.9.0  2022-02-23 other messsages improved
