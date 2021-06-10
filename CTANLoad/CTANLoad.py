#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANLoad.py
# (C) Günter Partosch, 2019/2021

# Es fehlen noch  bzw. Probleme:
# - noch besser unterscheiden zwischen not well-formed und leerer Datei
# - unterschiedliche Verzeichnisse für XML- und PDF-Dateien?
# - GNU-wget ersetzen durch python-Konstrukt; https://pypi.org/project/python3-wget/
# - Parameter -m BibLaTeX  mit/ohne -l
# - zusätzlicher Aufruf-Parameter -k (Laden nach Topics)?
# - https://ctan.org/xml/2.0/licenses auswerten und für <license .../> nutzen (x)
# - bei -d: ggf. Verzeichnis anlegen (X)
# - bei -d: Verzeichnistrenner besser/explizit behandeln (x)
# - Ausgabe von Zeichenketten verbessern
# - Generierung von CTAN.pkl auch ohne Parameter -l ? ggf. verschieben? (x)
# - neuer Parameter für die Generierung von CTAN.pkl und CTAN2.pkl ?
# - gründliche Überarbeitung von -c; Zusammenspiel von PDF_toc and XML_toc
# - ggf. try: ... except KeyboardInterrupt ?

# ------------------------------------------------------------------
# History

# 2.0.0  2019-10-01 completely revised
# 2.0.1  2019-10-03 smaller changes: messages + command parsing
# 2.0.2  2019-10-04 smaller changes: messages
# 2.0.3  2019-11-26 smaller change: error message and parameter -n
# 2.0.4  2020-01-09 -c enhanced
# 2.0.5  2020-01-12 some corrections
# 2.0.6  2020-01-15 time measure
# 2.0.7  2020-01-24 statistics improved
# 2.0.8  2020-01-25 minor corrections
# 2.0.9  2020-06-05 correction in load_documentation file
# 2.0.10 2020-06-26 enhance verbose output
# 2.0.11 2020-07-22 first lines of file
# 2.0.12 2021-04-05 output for option -c enhanced
# 2.0.13 2021-05-13 output local file name for downladed PDF files in verbose mode
# 2.0.14 2021-05-13 output the call parameters in more details in verbose mode
# 2.0.15 2021-05-14 clean-up for variables
# 2.0.16 2021-05-20 directory + separator improved
# 2.0.17 2021-05-21 more details in verbose mode
# 2.0.18 2021-05-23 directiry name improved
# 2.0.19 2021-05-24 directory handling improved (existance, installation) 
# 2.1.0  2021-05-26 load licences, make corr. directory and file; expand CTAN.pkl
# 2.1.1  2021-05-26 correction for not-existing keys in licenses.xml
# 2.1.2  2021-06-01 smaller improvements in check_integrity

# ------------------------------------------------------------------
# Usage (CTANLoad)

# usage: CTANLoad.py [-h] [-a] [-V] [-d DIREC] [-n NUMBER] [-o OUTPUT_NAME] [-t TEMPLATE] [-c] [-f] [-l] [-stat] [-v]
# 
# Loads XLM and PDF documentation files from CTAN a/o generates some special lists, and prepares data for CTANOut [CTANLoad.py; Version: 2.1.2
# (2021-06-01)]
# 
# Optional parameters:
#   -h, --help            show this help message and exit
#   -a, --author          Author of the program
#   -V, --version         Version of the program
#   -d DIREC, --directory DIREC
#                         Directory for output files; Default: ./
#   -n NUMBER, --number NUMBER
#                         Maximum number of file downloads; Default: 250
#   -o OUTPUT_NAME, --output OUTPUT_NAME
#                         Generic file name for output files; Default: all
#   -t TEMPLATE, --template TEMPLATE
#                         Name template for package XML files to be loaded; Default:
#   -c, --check_integrity
#                         Flag: Check the integrity of the 2nd .pkl file; Default: False
#   -f, --download_files  Flag: Download associated documentation files (PDF); Default: False
#   -l, --lists           Flag: Generate some special lists and prepare files for CTANOut; Default: False
#   -stat, --statistics   Flag: Print statistics; Default: False
#   -v, --verbose         Flag: Output is verbose; Default: False

# ------------------------------------------------------------------
# Messages (CTANLoad)

# Informative messages:
# - authors collected
# - entry 'file' in directory deleted
# - file 'file' (list of authors and associated packages) generated
# - file 'file' (list of authors) generated
# - file 'file' (list of packages) generated
# - file 'file' (list of topics and associated packages) generated
# - file 'file' (list of topics) generated
# - integrity check
# - no error with integrity check
# - packages collected
# - packagetopics, topicspackage, authorpackage collected
# - PDF documentation file 'file' downloaded
# - pickle file 'CTAN.pkl' written
# - pickle file 'CTAN2.pkl' cannot be loaded a/o written
# - pickle file 'CTAN2.pkl' written
# - program successfully completed
# - topics collected
# - XML file 'file' downloaded
# - XML file for package 'package' downloaded
#
# Warnings:
# - entry 'file' in directory, but file empty or not found
# - maximum number (n) of downloaded XML+PDF files exceeded
# - PDF documentation file 'file' not downloaded
# - PDF file 'file' deleted
# - XML file 'file' empty or not well-formed
# - XML file 'file' not downloaded
# - local XML file for package 'package' empty or not well-formed
# - XML file for package 'package' not downloaded
# - local XML file for package 'package' not found
# - PDF file 'file' without associated XML file
# - '-f'/'--download_files' valid only together with '-t'/'--template'; therefore ignored
#
# Errors:
# - programm terminated
# - tried to use the program indirectly
# - standard XML file 'file' empty or not well-formed 
# - XML file 'file' not downloaded 

# ------------------------------------------------------------------
# Examples (CTANLoad)

# CTANLoad -h
# - help, show the options
#
# CTANLoad -t "^a.+$" -v
# - load all CTAN XML files with name template "^a.+$"         [-t]
# - verbose output                                             [-v]
#
# CTANLoad -f -n 300 -t "^l3" -v
# - verbose output [-v]
# - load all CTAN XML files with the name template "^l3$"      [-t]
# - load the associated information files (PDF)                [-f]
# - maximum number of download files                           [-n]
#
# CTANLoad -v -l
# - generate some special lists, and prepare files for CTANOut [-l]
# - verbose output                                             [-v]
#
# CTANLoad -v -l -c -stat
# - generate some special lists, and prepare files for CTANOut [-l]
# - verbose output                                             [-v]
# - with integrity check                                       [-c]
# - with statistics                                            [-stat]

# ------------------------------------------------------------------
# Imports

import argparse                    # parse arguments
import os                          # delete a file on disk, for instance
import os.path                     # operating system relevant routines
from os import path                # path informations
import pickle                      # read/write pickle data
import platform                    # get OS informations
import random                      # used for random integers
import re                          # handle regular expressions
import subprocess                  # handling of sub-processes
import sys                         # system calls
import time                        # used for random seed, time measurement
import xml.etree.ElementTree as ET # XML processing


# ==================================================================
# Global settings

# ------------------------------------------------------------------
# The program

prg_name        = "CTANLoad.py"
prg_author      = "Günter Partosch"
prg_email       = "Guenter.Partosch@hrz.uni-giessen,de"
prg_version     = "2.1.2"
prg_date        = "2021-06-01"
prg_inst        = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"

operatingsys    = platform.system()
call            = sys.argv

# ------------------------------------------------------------------
# Texts for argparse and help

author_text         = "Author of the program"
version_text        = "Version of the program"
template_text       = "Name template for package XML files to be loaded"
output_text         = "Generic file name for output files"
number_text         = "Maximum number of file downloads"
direc_text          = "OS Directory for output files"
program_text        = "Loads XLM and PDF documentation files from CTAN a/o generates some special lists, and prepares data for CTANOut"

verbose_text        = "Flag: Output is verbose."
download_text       = "Flag: Download associated documentation files [PDF]."
lists_text          = "Flag: Generate some special lists and prepare files for CTANOut."
statistics_text     = "Flag: Print statistics."
integrity_text      = "Flag: Check the integrity of the 2nd .pkl file."

# ------------------------------------------------------------------
# Defaults/variables for argparse

download_default    = False      # default for option -f    (no PDF download)
integrity_default   = False      # default for option -c    (no integrity check)
lists_default       = False      # default for option -n    (special lists are not generated)
number_default      = 250        # default for option -n    (maximum number of files to be loaded)
output_name_default = "all"      # default for option -o    (generic file name)
statistics_default  = False      # default for option -stat (no statistics output)
template_default    = ""         # default for option -t    (name template for file loading)
verbose_default     = False      # default for option -n    (output is not verbose)

act_direc           = "."        
if operatingsys == "Windows":    
    direc_sep      = "\\"
else:
    direc_sep      = "/"
direc_default       = act_direc + direc_sep # default for -d (output directory)

download            = None       # default for option -f    (no PDF download)
integrity           = None       # default for option -c    (no integrity check)
lists               = None       # default for option -n    (special lists are not generated)
number              = 0          # default for option -n    (maximum number of files to be loaded)
output_name         = ""         # default for option -o    (generic file name)
statistics          = None       # default for option -stat (no statistics output)
template            = ""         # default for option -t    (name template for file loading)
verbose             = None       # default for option -n    (output is not verbose)

# ------------------------------------------------------------------
# Dictionaries

authorpackages      = {}         # python dictionary: list of authors and their packages
authors             = {}         # python dictionary: list of authors
packages            = {}         # python dictionary: list of packages
licenses            = {}         # python dictionary: list of licenses
packagetopics       = {}         # python dictionary: list of packages and their topics
topics              = {}         # python dictionary: list of topics
topicspackage       = {}         # python dictionary: list of topics and their packages
XML_toc             = {}         # python dictionary: list of PDF files: XML_toc[href]=...PDF file
PDF_toc             = {}         # python dictionary: list of PDF files: PDF_toc[lfn]=...package file

# XML_toc
#   Structure:                 XML_toc[href] = (file, fkey, onename)
#   generated and changed in:  analyze_XML_file(file), check_integrity()
#   inspected in:              analyze_XML_file(file), check_integrity()
#   stored in pickle file:     generate_pickle2()
#   loaded from pickle file:   load_XML_toc()
#
# PDF_toc
#   Structure:                 PDF_toc[file] = fkey + "-" + onename
#   generated in:              get_PDF_files(d)
#   changed in                 analyze_XML_file(file), check_integrity()
#   inspected in:              check_integrity()

# ------------------------------------------------------------------
# Settings for wget (authors, packages, topics)

ctanUrl             = "https://ctan.org"          # head of a CTAN url
ctanUrl2            = ctanUrl + "/tex-archive"    # head of another CTAN url
call1               = "wget https://ctan.org/xml/2.0/"
call2               = "wget https://ctan.org/xml/2.0/pkg/"
parameter           = "?no-dtd=true --no-check-certificate -O "

# ------------------------------------------------------------------
# other settings

pkl_file            = "CTAN.pkl" # name of 1st pickle file
pkl_file2           = "CTAN2.pkl"# name of 2nd pickle file

counter             = 0          # counter for downloaded XML files (in the actual session)
pdfcounter          = 0          # counter for downloaded PDF files (in the actual session)
pdfctrerr           = 0          # counter for not downloaded PDF files (in the actual session)
corrected           = 0          # counter of corrected entries in XML_toc (in the actual session)

ext                 = ".xml"     # file name extension for downloaded XML files
rndg                = 2          # optional rounding of float numbers
left                = 35         # width of labels in statistics

random.seed(time.time())         # seed for random number generation


# ==================================================================
# argparse
# parses options and processes them

parser = argparse.ArgumentParser(description = program_text + " [" + prg_name + "; " +
                                 "Version: " + prg_version + " (" + prg_date + ")]")
parser._positionals.title = 'Positional parameters'
parser._optionals.title   = 'Optional parameters'
opgroup = parser.add_mutually_exclusive_group()

parser.add_argument("-a", "--author",                      # Parameter -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = prg_author + " (" + prg_email + ", " + prg_inst + ")")

parser.add_argument("-V", "--version",                     # Parameter -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + prg_version + " (" + prg_date + ")")

parser.add_argument("-d", "--directory",                   # Parameter -d/--directory
                    help    = direc_text + "; Default: " + "%(default)s",
                    dest    = "direc",
                    default = direc_default)

parser.add_argument("-n", "--number",                      # Parameter -n/--number
                    help    = number_text + "; Default: " + "%(default)s",
                    dest    = "number",
                    default = number_default)

parser.add_argument("-o", "--output",                      # Parameter -o/--output
                    help    = output_text + "; Default: " + "%(default)s",
                    dest    = "output_name",
                    default = output_name_default)

opgroup.add_argument("-t", "--template",                   # Parameter -t/--template
                    help    = template_text + "; Default: " + "%(default)s",
                    dest    = "template",
                    default = template_default)

parser.add_argument("-c", "--check_integrity",             # Parameter -c/--check_integrity
                    help    = integrity_text + "; Default: " + "%(default)s",
##                    help    = argparse.SUPPRESS,
                    action  = "store_true",
                    default = integrity_default)

parser.add_argument("-f", "--download_files",              # Parameter -f/--download_files
                    help    = download_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = download_default)

opgroup.add_argument("-l", "--lists",                      # Parameter -l/--lists
                    help = lists_text + "; Default: " + "%(default)s",
                    action = "store_true",
                    default = lists_default)

parser.add_argument("-stat", "--statistics",               # Parameter -stat/--statistics
                    help    = statistics_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics_default)

parser.add_argument("-v", "--verbose",                     # Parameter -v/--verbose
                    help = verbose_text + "; Default: " + "%(default)s",
                    action = "store_true",
                    default = verbose_default)

# ------------------------------------------------------------------
# Getting parsed values

args         = parser.parse_args()                         # all parameters of programm call
direc        = args.direc                                  # parameter -d
download     = args.download_files                         # parameter -f
integrity    = args.check_integrity                        # parameter -c
lists        = args.lists                                  # parameter -l
number       = int(args.number)                            # parameter -n
statistics   = args.statistics                             # Parameter -stat
template     = args.template                               # parameter -t
verbose      = args.verbose                                # parameter -v

# ------------------------------------------------------------------
# Correct directory name, test directory existence, and install directory

direc = direc.strip()                                      # correct directory name (-d)
if direc[len(direc) - 1] != direc_sep:
    direc += direc_sep
if not path.exists(direc):
    try:
        os.mkdir(direc)
    except OSError:
        print ("- Creation of the directory '%s' failed" % direc)
    else:
        print ("- Successfully created the directory '%s' " % direc)
output_name  = direc + args.output_name                    # parameter -d

# ------------------------------------------------------------------
# regular expressions

p2           = re.compile(template)                        # regular expression based on parameter -t
p3           = re.compile("^[0-9]{10}-.+[.]pdf$")          # regular expression for local PDF file names
p4           = re.compile("^.+[.]xml$")                    # regular expression for local XML file names


# ==================================================================
# Functions for main part

# ------------------------------------------------------------------
def load_authors():                                        # Function load_authors()
    """Downloads XML file 'authors'."""

    global authors                                         # global directory with authors

    file    = "authors"                                    # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # loads file 'authors'
        # wget https://ctan.org/xml/2.0/authors?no-dtd=true --no-check-certificate -O ./authors.xml
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()

        if verbose:
            print("--- XML file '" + file + "' downloaded", "('" + direc + file + ".xml' on PC)")

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
                print("----- authors collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- standard XML file '" + file2 + "' empty or not well-formed")
            sys.exit("- programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- XML file '" + file + "' not downloaded")
        sys.exit("- programm terminated")                  # program terminated

# ------------------------------------------------------------------
def load_packages():                                       # Function load_packages()
    """Downloads XML file 'packages'."""

    global packages                                        # global directory with packages

    file    = "packages"                                   # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # loads file .../packages
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()

        if verbose:
            print("--- XML file '" + file + "' downloaded", "('" + direc + file + ".xml' on PC)")

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
                print("----- packages collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- standard XML file '" + file2 + "' empty or not well-formed")
            sys.exit("--- programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- XML file '" + file + "' not downloaded")
        sys.exit("- programm terminated")                  # program terminated

# ------------------------------------------------------------------
def load_topics():                                         # Function load_topics()
    """Downloads XML file 'topics'."""

    global topics                                          # global directory with topics

    file    = "topics"                                     # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # loads file .../topics
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()

        if verbose:
            print("--- XML file '" + file + "' downloaded", "('" + direc + file + ".xml' on PC)")

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
                print("----- topics collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- standard XML file '" + file + "' empty or not well-formed")
            sys.exit("--- programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- XML file '" + file + "' not downloaded")
        sys.exit("- programm terminated")                  # program terminated

# ------------------------------------------------------------------
def load_licenses():                                       # Function load_licenses()
    """Downloads XML file 'licenses'."""

    global licenses                                        # global directory with licenses

    file    = "licenses"                                   # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # loads file .../licenses
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()

        if verbose:
            print("--- XML file '" + file + "' downloaded", "('" + direc + file + ".xml' on PC)")

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
                    if str(attr) == "name":
                        name = child.attrib['name']        # attribute name
                    if str(attr) == "free":
                        free = child.attrib['free']        # attribute free
                licenses[key] = name
            licenses["noinfo"]      = "No Information"     # correction; not in lincenses.xml
            licenses["collection"]  = "Collection"         # correction; not in lincenses.xml
            licenses["digest"]      = "Digest"             # correction; not in lincenses.xml
            if verbose:
                print("----- licenses collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- standard XML file '" + file + "' empty or not well-formed")
            sys.exit("--- programm terminated")
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- XML file '" + file + "' not downloaded")
        sys.exit("- programm terminated")                  # program terminated

# ------------------------------------------------------------------
def generate_topicspackage():                                       # Function generate_topicspackage()
    """Generates topicspackage, packagetopics, and authorpackages."""

    global topicspackage, packagetopics, authorpackages

    for f in packages:                                              # all package XML files are loaded in series
        try:                                                        # try to open and parse file
            fext = f + ext                                          # file name (with extension)
            ff = open(fext, encoding="utf-8", mode="r")

            try:
                einPaket     = ET.parse(fext)                       # parse the XML file
                einPaketRoot = einPaket.getroot()
                ll           = list(einPaketRoot.iter("keyval"))    # all keyval elements
                aa           = list(einPaketRoot.iter("authorref")) # all authorref elements

                for i in ll:                                        # in keyval: 1 attribute: value
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
            except:                                                 # parsing was not successfull
                if verbose:
                    print("----- local XML file for package '" + f + "' empty or not well-formed")
            ff.close()
        except FileNotFoundError:                                   # file not downloaded
            if verbose:
                print("----- local XML file for package '" + f + "' not found")
    if verbose:
        print("--- packagetopics, topicspackage, authorpackage collected")

# ------------------------------------------------------------------
def load_XML_files():                                               # Function load_XML_files()
    """Downloads XML package files."""

    global packages, topicspackage, number, counter, pdfcounter

    for f in packages:                                              # all packages found in 'packages'
        if p2.match(f) and (counter + pdfcounter < number):         # file name matches template
            counter = counter + 1
            callx   = call2 + f + parameter + direc + f + ext       # wget https://ctan.org/xml/2.0/pkg/xyz --no-check-certificate -O xyz

            try:                                                    # try to download the XML file (packages)
                process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
                process.wait()

                if verbose:
                    print("----- XML file for package '" + f + "' downloaded", "('" + direc + f + ".xml' on PC)")
                if download:
                    analyze_XML_file(f + ext)                       # if download is set: analyze the associated XML file
            except FileNotFoundError:                               # download was not successfull
                if verbose:
                    print("----- XML file for package '" + f + "' not downloaded")

    if counter + pdfcounter >= number:
        if verbose:
            print("--- maximum number (" + str(counter + pdfcounter) + ") of downloaded XML+PDF files exceeded")

# ------------------------------------------------------------------
def analyze_XML_file(file):                                        # Function analyze_XML_file(file)
    """Analyzes a XML package file for documentation (PDF) files."""

    # analyze_XML_file --> load_document_file

    global XML_toc                                                 # global directory
    global PDF_toc

    error = False

    try:                                                           # try to open and parse a XML file
        f            = open(file, encoding="utf-8", mode="r")      # open the XML file
        einPaket     = ET.parse(f)                                 # parse the XML file
        einPaketRoot = einPaket.getroot()                          # get root
    except:                                                        # parsing not successfull
        if verbose:
            print("------- local XML file for package '" + file + "' empty or not well-formed")
        error = True

    if not error:
        ll           = list(einPaketRoot.iter("documentation"))    # all documentation elements = all documentation childs

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
                if load_document_file(href2, fkey, onename):       # load the PDF document
                    PDF_toc[file] = fkey + "-" + onename
        f.close()                                                  # close the analyzed XML file

# ------------------------------------------------------------------
def load_document_file(href, key, name):                           # Function load_document_file(href, key, name)
    """Loads one information file (PDF)."""
    
    # to be improved

    global pdfcounter
    global pdfctrerr

    call     = "wget " + href + parameter + direc + key + "-" + name
    noterror = False

    # @wait: 17.5.3 in library
    try:                                                           # download the PDF file and store
        process = subprocess.Popen(call, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = process.communicate(timeout=50)               # wait?
        if "ERROR" in errs:                                        # "ERROR" found in errs
            if verbose:
                print("------- PDF documentation file '" + name + "' not downloaded")
            pdfctrerr = pdfctrerr + 1
        else:
            if verbose:
                print("------- PDF documentation file '" + name + "' downloaded")
                print("------- unique local file name:", "'" + direc + key + "-" + name + "'")
            pdfcounter = pdfcounter + 1                            # number of downloaded PDF files incremented
            noterror = True
    except:                                                        # download was not successfull
        process.kill()                                             # kill the process
        outs, errs = process.communicate()                         # output and error messages
        if verbose:
            print("------- PDF documentation file '" + name + "' not downloaded")
    return noterror

# ------------------------------------------------------------------
def load_XML_toc():                                                # Function load_XML_toc()
    """Loads pickle file with XML_toc."""

    global XML_toc                                                 # global directory

    try:
        pickleFile2 = open(direc + pkl_file2, "br")                # open the pickle file
        XML_toc     = pickle.load(pickleFile2)                     # unpickle the data
        pickleFile2.close()
    except IOError:                                                # not successfull
        pass                                                       # do nothing

# ------------------------------------------------------------------
def generate_lists():                                              # Function generate_lists()
    """Generates some special files (with lists).:
       xyz.loa (list of authors)
       xyz.lop (list of packages)
       xyz.lok (list of topics)
       xyz.lpt (list of topics and associated packages)
       xyz.lap (list of authors and associated packages)
       xyz is the specified generic output file name."""

    # .................................................
    # generates xyz.loa file (list of authors)

    loa_file = output_name + ".loa"

    loa = open(loa_file, encoding="utf-8", mode="w")              # open xyz.loa file
    for f in authors:                                             # loop
        loa.write(str(authors[f]) + "\n")

    if verbose:
        print("--- file '" + loa_file + "' (list of authors) generated")
    loa.close()                                                   # close xyz.loa file

    # .................................................
    # generates xyz.lop file (list of packages)

    lop_file = output_name + ".lop"

    lop = open(lop_file, encoding="utf-8", mode="w")              # open xyz.lop file
    for f in packages:                                            # loop
        lop.write(str(packages[f]) + "\n")

    if verbose:
        print("--- file '" + lop_file + "' (list of packages) generated")
    lop.close()                                                   # close xyz.lop file

    # .................................................
    # generates xyz.lok file (list of topics)

    lok_file = output_name + ".lok"

    lok = open(lok_file, encoding="utf-8", mode="w")              # open xyz.lok file
    for f in topics:                                              # loop
        lok.write("('" + f + "', '" + str(topics[f]) + "')\n")

    if verbose:
        print("--- file '" + lok_file + "' (list of topics) generated")
    lok.close()                                                   # close xyz.lok file

    # .................................................
    # generates xyz.lol file (list of licenses)

    lol_file = output_name + ".lol"

    lol = open(lol_file, encoding="utf-8", mode="w")              # open xyz.lol file
    for f in licenses:                                            # loop
        lol.write("('" + f + "', '" + str(licenses[f]) + "')\n")

    if verbose:
        print("--- file '" + lol_file + "' (list of licenses) generated")
    lol.close()                                                   # close xyz.lol file

    # .................................................
    # generates xyz.lpt file (list of topics and associated packages)

    lpt_file = output_name + ".lpt"

    lpt = open(lpt_file, encoding="utf-8", mode="w")              # open xyz.lpt file
    for f in topicspackage:                                       # loop
        lpt.write("('" + f + "', " + str(topicspackage[f]) + ")\n")

    if verbose:
        print("--- file '" + lpt_file + "' (list of topics and associated packages) generated")
    lpt.close()                                                   # close xyz.lpt file

    # .................................................
    # generates xyz.lap file (list of authors and associated packages)

    lap_file = output_name + ".lap"

    lap = open(lap_file, encoding="utf-8", mode="w")              # open xyz.lap file
    for f in authorpackages:                                      # loop
        lap.write("('" + str(f) + "', " + str(authorpackages[f]) + ")\n")

    if verbose:
        print("--- file '" + lap_file + "' (list of authors and associated packages) generated")
    lap.close()                                                   # close xyz.lap file

# ------------------------------------------------------------------
def generate_pickle1():                                           # Function generate_pickle1()
    """pickle dump:
    needs actual authors, packages, licenses, topics, topicspackage, packagetopics"""

    # authors: directory (sorted)
    #   each element: [author key] <tuple with givenname and familyname>
    #
    # packages: directory (sorted)
    #   each element: [package key] <tuple with package name and package title>
    #
    # licenses: directory (sorted)
    #   each element: [license key] <license title>
    #
    # topics: directory (sorted)
    #   each element: [topics name] <topics title>
    #
    # topicspackage: directory (unsorted)
    #   each element: [topic key] <list with package names>
    #
    # packagetopics: directory (sorted)
    #   each element: [topic key] <list with package names>
    #
    # authorpackages: directory (unsorted)
    #   each element: [author key] <list with package names>

    pickle_name1  = direc + pkl_file                              # path of the pickle file
    pickle_file1  = open(pickle_name1, "bw")                      # open the pickle file
    pickle_data1  = (authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages)
    pickle.dump(pickle_data1, pickle_file1)                       # dump the data
    pickle_file1.close()                                          # close the file
    if verbose:
        print("--- pickle file '" + pickle_name1 + "' written")

# ------------------------------------------------------------------
def generate_pickle2():                                           # Function generate_pickle2()
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
            print("--- pickle file '" + pickle_name2 + "' written")
    except:                                                       # not successfull
        if verbose:
            print("--- pickle file '" + pickle_name2 + "' cannot be loaded a/o written")

# ------------------------------------------------------------------
def check_integrity():                                            # Function check_integrity()
    """Checks integrity."""

    # check_integrity --> generate_pickle2

    global corrected
    global PDF_toc

    if verbose:
        print("--- integrity check")
    load_XML_toc()                                                # load the 2nd pickle file (XML_toc)

    noerror = True
    tmpdict = XML_toc                                             # make a copy

# ..................................................................
    for f in tmpdict:                                             # loop: all entries in a copy of XML_toc
        tmp  = tmpdict[f]
        dd   = direc + tmp[1] + "-" + tmp[2]
        tmp2 = os.path.isfile(dd)                                 #    does the file exist?

        if tmp2:
            tmp2 = os.path.getsize(dd) > 0                        #    file exists and is not empty?
        else:
            noerror = False
        tmp3 = dd

        if not tmp2:                                              #    there is an error (file is empty)
            if verbose:
                print("----- entry '" + tmp3 + "' (" + tmp[0] + ") in directory, but file empty or not found")
            if os.path.isfile(tmp3):                              #    file exists
                os.remove(tmp3)                                   #    delete the associated PDF file
                if verbose:
                    print("----- PDF file '" + tmp3 + "' deleted")
            del XML_toc[f]
            if verbose:
                print("----- entry '" + tmp3 + "' in directory deleted")
            corrected = corrected + 1
    
# ..................................................................
# specify values in PDF_toc (via XML_toc)
    for t in XML_toc:                                             # loop: all members in XML_toc (all XML files)
        (file, fkey, onename)         = XML_toc[t]                #    get file, fkey, onename
        PDF_toc[fkey + "-" + onename] = file                      #    generate entry in PDF_toc

# ..................................................................
# check actualized PDF_toc; delete a PDF file if necessary
    ok = True
    for g in PDF_toc:                                             # move through PDF files
        if PDF_toc[g] == "":                                      #    no entry: no ass. XML file
            ok = False
            if verbose:
                print("----- PDF file '" + g + "' without associated XML file")
            if os.path.isfile(g):                                 #    g is file
                os.remove(g)                                      #    delete the PDF file (if it exists)
                if verbose:
                    print("----- PDF file '" + g + "' deleted")

# ..................................................................
    if noerror and ok:                                            # there is no error
        if verbose:
            print("----- no error with integrity check")
    else:                                                         # there is an error
        if not noerror:
            generate_pickle2()                                    #    generate a new version of this pickle file

# ------------------------------------------------------------------
def make_statistics():                                            # Function make_statistics()
    """Prints statistics on terminal."""

    l         = left
    r         = 5
    load      = (template != "")
    nrXMLfile = 0

    XMLdir = os.listdir(direc)
    for f in XMLdir:
        if p4.match(f):
            nrXMLfile += 1

    print("\nStatistics\n")
    print("total number of authors on CTAN:".ljust(l), str(len(authors)).rjust(r))
    print("total number of topics on CTAN:".ljust(l), str(len(topics)).rjust(r))
    print("total number of packages on CTAN:".ljust(l), str(len(packages)).rjust(r))
    if load:
        print("number of downloaded XML files:".ljust(l), str(counter).rjust(r), "(in the actual session)")
        print("number of downloaded PDF files:".ljust(l), str(pdfcounter).rjust(r), "(in the actual session)")
        print("number of not downloaded PDF files:".ljust(l), str(pdfctrerr).rjust(r), "(in the actual session)")
    print("total number of local PDF files:".ljust(l), str(len(PDF_toc)).rjust(r))
    print("total number of local XML files:".ljust(l), str(nrXMLfile).rjust(r))
    if integrity:
        print("number of corrected entries:".ljust(l), str(corrected).rjust(r), "(in the actual session)")

# ------------------------------------------------------------------
def get_PDF_files(d):                                             # Function get_PDF_files(d)
    """Lists all PDF files in a OS directory.

    d: directory"""

    global PDF_toc

    tmp  = os.listdir(d)                                          # get OS directory list
    tmp2 = {}
    for f in tmp:                                                 # all PDF files in current OS directory
        if p3.match(f):                                           #    check: file name matches p3
            tmp2[f] = ""                                          #    presets with empty string
    PDF_toc = tmp2

# ------------------------------------------------------------------
def main():                                                       # Function main()
    """Main Function"""

    # main --> get PDF_files
    # main --> load_XML_toc
    # main --> load_topics
    # main --> load_authors
    # main --> load_licenses
    # main --> load_packages
    # main --> load_XML_files
    # main --> generate_pickle2
    # main --> generate_topicspackage
    # main --> generate_lists
    # main --> generate_pickle1
    # main --> check_integrity
    # main --> make_statistics

    global PDF_toc
    global download

    starttotal  = time.time()                                     # begin of time measure
    startprocess= time.process_time()
     
    if verbose:                                                   # output on terminal
        print("\n- program call: CTANLoad.py")
        if ("-d" in call) or ("--directory" in call):       print("  {0:5} {2:55} {1}".format("-d", direc, "(" + direc_text + ")"))
        if ("-n" in call) or ("--number" in call):          print("  {0:5} {2:55} {1}".format("-n", number, "(" + number_text + ")"))
        if ("-o" in call) or ("--output" in call):          print("  {0:5} {2:55} {1}".format("-o", args.output_name, "(" + output_text + ")"))
        if ("-t" in call) or ("--template" in call):        print("  {0:5} {2:55} {1}".format("-t", template, "(" + template_text + ")"))
        if ("-c" in call) or ("--check_integrity" in call): print("  {0:5} {1:55}".format("-c", "(" + integrity_text + ")"))
        if ("-f" in call) or ("--download_files" in call):  print("  {0:5} {1:55}".format("-f", "(" + download_text + ")"))
        if ("-l" in call) or ("--lists" in call):           print("  {0:5} {1:55}".format("-l", "(" + lists_text + ")"))
        if ("-stat" in call) or ("--statistics" in call):   print("  {0:5} {1:55}".format("-stat", "(" + statistics_text + ")"))
        if ("-v" in call) or ("--verbose" in call):         print("  {0:5} {1:55}".format("-v", "(" + verbose_text + ")"))
        print("\n")

    get_PDF_files(direc)

    load        = (template != "")                                # package files are to be loaded
    make_lists  = (not load) and lists                            # special list files are to be generated

    tmp         = ""

    if (template == template_default) and download:               # test  template <-->  download
        if verbose:
            print("--- '-f'/'--download_files' valid only together with '-t'/'--template'; therefore ignored")
        download = False

    if download:                                                  # load the directory XML_toc
        load_XML_toc()

    load_topics()                                                 # load the file topics.xml
    load_authors()                                                # load the file authors.xml
    load_licenses()                                               # load the file licenses.xml
    load_packages()                                               # load the file packages.xml

    if load:                                                      # if package files are to be loaded
        load_XML_files()                                          #     load and processe all XML files in series
        generate_pickle2()                                        #     dump XML_toc

    generate_topicspackage()                                      # generates topicspackage, ...
    generate_pickle1()                                            # dumps authors, packages, topics, licenses, topicspackage, packagetopics

    if make_lists:                                                # if lists are to be generated
        generate_lists()                                          #     generates x.loa, x.lop, x.lok, x.lol, x.lpt, x.lap

    if integrity:                                                 # if the integrity is to be checked
        check_integrity()                                         #     when indicated: remove files or entries

    if verbose:
        print("- program successfully completed")

    if statistics:                                                # if statistics are to be output
        make_statistics()

        endtotal   = time.time()                                  # end of time measure
        endprocess = time.process_time()
        print("--")
        print("total time: ".ljust(left + 1), round(endtotal-starttotal, rndg))
        print("process time: ".ljust(left + 1), round(endprocess-startprocess, rndg))


# ==================================================================
# Main part

# script --> main

if __name__ == "__main__":
    main()
else:
    if verbose:
        print("- tried to use the program indirectly")
