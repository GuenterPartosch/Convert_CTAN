#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANLoad.py
# (C) Günter Partosch, 2019/2020

# Es fehlen noch  bzw. Probleme:
# - noch besser unterscheiden zwischen not well-formed und leerer Datei
# - unterschiedliche Verzeichnisse für XML- und PDF-Dateien?
# - GNU-wget ersetzen durch python-Konstrukt
# - Parameter -m BibLaTeX  mit/ohne -l
# - zusätzlicher Aufruf-Parameter -k (Laden nach Topics)?

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
# 2.0.12 2021-03-27 some improvements in check_integrity

# ------------------------------------------------------------------
# Usage (CTANLoad)

# usage: CTANLoad.py [-h] [-a] [-V] [-d DIREC] [-n NUMBER] [-o OUTPUT_NAME]
#                     [-t TEMPLATE] [-c] [-f] [-l] [-stat] [-v]
#
# Loads XLM files and documentation files from CTAN a/o generates some special
# lists, and prepares data for CTANOut [CTANLoad.py; Version: 2.0.12
# (2021-03-27)]
#
# Optional parameters:
#   -h, --help            show this help message and exit
#   -a, --author          author of the program
#   -V, --version         version of the program
#   -d DIREC, --directory DIREC
#                         directory for output files; Default: ./
#   -n NUMBER, --number NUMBER
#                         maximum number of file downloads; Default: 250
#   -o OUTPUT_NAME, --output OUTPUT_NAME
#                         generic file name for output files; Default: all
#   -t TEMPLATE, --template TEMPLATE
#                         name template for package XML files to be loaded;
#                         Default:
#   -c, --check_integrity
#                         Flag: Check the integrity of the 2nd .pkl file;
#                         Default: False
#   -f, --download_files  Flag: Download associated documentation files (PDF);
#                         Default: False
#   -l, --lists           Flag: Generate some special lists and prepare files
#                         for CTAN-Out; Default: False
#   -stat, --statistics   Flag: Print statistics; Default: False
#   -v, --verbose         Flag: output is verbose; Default: False

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
# - XML file for package 'package' empty or not well-formed
# - XML file for package 'package' not downloaded
# - XML file for package 'package' not found
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
# CTANLoad -t "graphicx|pstricks" -v -f -stat
# - load the XML files for 'graphicx' and 'pstricks'           [-t]
# - load the associated information files (PDF)                [-f]
# - verbose output                                             [-v]
# - with statistics                                            [-stat]

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
prg_version     = "2.0.12"
prg_date        = "2021-03-27"
prg_inst        = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"

operatingsys    = platform.system()
call            = sys.argv

# ------------------------------------------------------------------
# Texts for argparse and help

author_text     = "author of the program"
version_text    = "version of the program"
template_text   = "name template for package XML files to be loaded"
output_text     = "generic file name for output files"
number_text     = "maximum number of file downloads"
direc_text      = "directory for output files"
program_text    = "Loads XLM and PDF documentation files from CTAN a/o generates some special lists, and prepares data for CTANOut"
verbose_text    = "Flag: output is verbose"
download_text   = "Flag: Download associated documentation files (PDF)"
lists_text      = "Flag: Generate some special lists and prepare files for CTANOut"
statistics_text = "Flag: Print statistics"
integrity_text  = "Flag: Check the integrity of the 2nd .pkl file"

# ------------------------------------------------------------------
# Defaults/variables for argparse

download        = False          # default for global flag: no download
integrity       = False          # no integrity check
lists           = False          # flag: special lists are generated vs. not generated
number          = 250            # maximum number of files to be loaded
output_name     = "all"          # generic file name
statistics      = False          # default for global flag: statistics output
template        = ""             # name template for file loading
verbose         = False          # flag: output is verbose | not verbose

# ------------------------------------------------------------------
# Dictionaries

authorpackages  = {}             # python dictionary: list of authors and their packages
authors         = {}             # python dictionary: list of authors
packages        = {}             # python dictionary: list of packages
packagetopics   = {}             # python dictionary: list of packages and their topics
topics          = {}             # python dictionary: list of topics
topicspackage   = {}             # python dictionary: list of topics and their packages
XML_toc         = {}             # python dictionary: list of XML and PDF files: XML_toc[CTAN address]=(XML file, key, pure PDF file)
PDF_toc         = {}             # python dictionary: list of local PDF files: PDF_toc[pdf file]=<corr. package XML file>

# ------------------------------------------------------------------
# Settings for wget (authors, packages, topics)

if operatingsys == "Windows":
    direc    = "./"
else:
    direc    = "./"

ctanUrl      = "https://ctan.org"          # head of a CTAN url
ctanUrl2     = ctanUrl + "/tex-archive"    # head of another CTAN url
call1        = "wget https://ctan.org/xml/2.0/"
call2        = "wget https://ctan.org/xml/2.0/pkg/"
parameter    = "?no-dtd=true --no-check-certificate -O "

# ------------------------------------------------------------------
# other settings

pkl_file     = "CTAN.pkl"          # name of 1st pickle file
pkl_file2    = "CTAN2.pkl"         # name of 2nd pickle file
counter      = 0                   # counter for downloaded XML files (in the actual session)
pdfcounter   = 0                   # counter for downloaded PDF files (in the actual session)
pdfctrerr    = 0                   # counter for not downloaded PDF files (in the actual session)
corrected    = 0                   # counter of corrected entries in XML_toc (in the actual session)
ext          = ".xml"              # file name extension for downloaded XML files
rndg         = 2                   # optional rounding of float numbers
left         = 35                  # width of labels in statistics

random.seed(time.time())           # seed for random number generation


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
                    default = direc)

parser.add_argument("-n", "--number",                      # Parameter -n/--number
                    help    = number_text + "; Default: " + "%(default)s",
                    dest    = "number",
                    default = number)

parser.add_argument("-o", "--output",                      # Parameter -o/--output
                    help    = output_text + "; Default: " + "%(default)s",
                    dest    = "output_name",
                    default = output_name)

opgroup.add_argument("-t", "--template",                   # Parameter -t/--template
                    help    = template_text + "; Default: " + "%(default)s",
                    dest    = "template",
                    default = template)

parser.add_argument("-c", "--check_integrity",             # Parameter -c/--check_integrity
                    help    = integrity_text + "; Default: " + "%(default)s",
##                    help    = argparse.SUPPRESS,
                    action  = "store_true",
                    default = integrity)

parser.add_argument("-f", "--download_files",              # Parameter -f/--download_files
                    help    = download_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = download)

opgroup.add_argument("-l", "--lists",                      # Parameter -l/--lists
                    help = lists_text + "; Default: " + "%(default)s",
                    action = "store_true",
                    default = lists)

parser.add_argument("-stat", "--statistics",               # Parameter -stat/--statistics
                    help    = statistics_text + "; Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics)

parser.add_argument("-v", "--verbose",                     # Parameter -v/--verbose
                    help = verbose_text + "; Default: " + "%(default)s",
                    action = "store_true",
                    default = verbose)

# ------------------------------------------------------------------
# Getting parsed values

args         = parser.parse_args()                         # all parameters of programm call
direc        = args.direc                                  # parameter -d
download     = args.download_files                         # parameter -f
integrity    = args.check_integrity                        # parameter -c
lists        = args.lists                                  # parameter -l
number       = int(args.number)                            # parameter -n
output_name  = direc + args.output_name                    # parameter -d
statistics   = args.statistics                             # Parameter -stat
template     = args.template                               # parameter -t
verbose      = args.verbose                                # parameter -v

# ------------------------------------------------------------------
# regular expressions

p2           = re.compile(template)                        # regular expression based on parameter -t
p3           = re.compile("^[0-9]{10}-.+[.]pdf$")          # regular expression for local PDF file names
p4           = re.compile("^.+[.]xml$")                    # regular expression for local XML file names


# ==================================================================
# Functions for main part

# ------------------------------------------------------------------
def load_authors():
    """Downloads XML file 'authors'."""

    global authors                                         # global directory with authors

    file    = "authors"                                    # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # try to load file 'authors'
        # wget https://ctan.org/xml/2.0/authors?no-dtd=true --no-check-certificate -o ./authors
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()                                     # process waits

        if verbose:
            print("--- XML file '" + file + "' downloaded")

        try:                                               # try to parse the XML file 'authors.xml'
            authorsTree  = ET.parse(file2)                 # parse
            authorsRoot  = authorsTree.getroot()           # get the root of tree

            for child in authorsRoot:                      # all children
                key   = ""                                 # defaults
                id    = ""                                 # defaults
                fname = ""                                 # defaults
                gname = ""                                 # defaults
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
            sys.exit("- programm terminated")              # program is terminated
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- XML file '" + file + "' not downloaded")
        sys.exit("- programm terminated")                  # program is terminated

# ------------------------------------------------------------------
def load_packages():
    """Downloads XML file 'packages'."""

    global packages                                        # global directory with packages

    file    = "packages"                                   # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # try to load file .../packages
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()                                     # process waits

        if verbose:
            print("--- XML file '" + file + "' downloaded")

        try:                                               # try to parse 'packages' tree
            packagesTree = ET.parse(file2)                 # parse the XML file 'packages.xml'
            packagesRoot = packagesTree.getroot()          # get the root of tree

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
                packages[key] = (name, caption)            # tuple (name, caption) is stored in 'packages'
            if verbose:
                print("----- packages collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- standard XML file '" + file2 + "' empty or not well-formed")
            sys.exit("--- programm terminated")            # program is terminated
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- XML file '" + file + "' not downloaded")
        sys.exit("- programm terminated")                  # program is terminated

# ------------------------------------------------------------------
def load_topics():
    """Downloads XML file 'topics'."""

    global topics                                          # global directory with topics

    file    = "topics"                                     # file name
    file2   = file + ext                                   # file name (with extension)
    callx   = call1 + file + parameter + direc + file2     # command for Popen

    try:                                                   # try to load file .../topics
        process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
        process.wait()                                     # process waits

        if verbose:
            print("--- XML file '" + file + "' downloaded")

        try:                                               # try to parse the XML file 'topics.xml'
            topicsTree   = ET.parse(file2)                 # parse
            topicsRoot   = topicsTree.getroot()            # get the root of tree

            for child in topicsRoot:                       # all children in 'topics'
                key     = ""                               # defaults
                name    = ""
                details = ""
                for attr in child.attrib:                  # two attributes: name, details
                    if str(attr) == "name":
                        key = child.attrib['name']         # attribute name
                    if str(attr) == "details":
                        details = child.attrib['details']  # attribute details
                topics[key] = details                      # details are stored in 'topics'
            if verbose:
                print("----- topics collected")
        except:                                            # parsing was not successfull
            if verbose:
                print("--- standard XML file '" + file + "' empty or not well-formed")
            sys.exit("--- programm terminated")            # program is terminated
    except FileNotFoundError:                              # file not downloaded
        if verbose:
            print("--- XML file '" + file + "' not downloaded")
        sys.exit("- programm terminated")                  # program is terminated

# ------------------------------------------------------------------
def generate_topicspackage():
    """Generates topicspackage, packagetopics, and authorpackages."""

    global topicspackage, packagetopics, authorpackages

    for f in packages:                                              # all the XML files for packages are loaded in series
        try:                                                        # try to open one file
            fext = f + ext                                          # file name (with extension)
            ff = open(fext, encoding="utf-8", mode="r")             # open file

            try:                                                    # try to parse the XML file
                einPaket     = ET.parse(fext)                       # parse loaded file
                einPaketRoot = einPaket.getroot()                   # get the root of tree
                ll           = list(einPaketRoot.iter("keyval"))    # list with all keyval elements
                aa           = list(einPaketRoot.iter("authorref")) # list with all authorref elements

                for i in ll:                                        # in keyval: 1 attribute: value
                    key = i.get("value", "")                        # attribute value
                    if key in topicspackage:                        # package name is stored in 'topicspackage'
                        topicspackage[key].append(f)                
                    else:
                        topicspackage[key] = [f]

                    if f in packagetopics:                          # key is stored in 'packagetopics'
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
                    if key3 in authorpackages:                      # package name is stored in 'authorpackages'
                        authorpackages[key3].append(f)
                    else:
                        authorpackages[key3] = [f]
            except:                                                 # parsing was not successfull
                if verbose:
                    print("----- XML file for package '" + f + "' empty or not well-formed")
            ff.close()
        except FileNotFoundError:                                   # file not downloaded
            if verbose:
                print("----- XML file for package '" + f + "' not found")
    if verbose:
        print("--- packagetopics, topicspackage, authorpackage collected")

# ------------------------------------------------------------------
def load_XML_files():
    """Downloads XML package files."""

    global packages, topicspackage, number, counter, pdfcounter

    for f in packages:                                              # all packages found in 'packages'
        if p2.match(f) and (counter + pdfcounter < number):         # file name matches template
            counter = counter + 1
            callx   = call2 + f + parameter + direc + f + ext       # wget https://ctan.org/xml/2.0/pkg/xyz --no-check-certificate -O xyz

            try:                                                    # try to download the XML file (packages)
                process = subprocess.Popen(callx, stderr=subprocess.PIPE, universal_newlines=True)
                process.wait()                                      # process waits

                if verbose:
                    print("----- XML file for package '" + f + "' downloaded")
                if download:
                    analyze_XML_file(f + ext)                       # if download is set: analyze the associated XML file
            except FileNotFoundError:                               # download was not successfull
                if verbose:
                    print("----- XML file for package '" + f + "' not downloaded")

    if counter + pdfcounter >= number:
        if verbose:
            print("--- maximum number (" + str(counter + pdfcounter) + ") of downloaded XML+PDF files exceeded")

# ------------------------------------------------------------------
def analyze_XML_file(file):
    """Analyzes a XML package file for documentation (PDF) files."""

    # analyze_XML_file --> load_document_file

    global XML_toc                                                 # global directory
    global PDF_toc

    error = False

    try:                                                           # try to open and parse a XML file
        f            = open(file, encoding="utf-8", mode="r")      # open the XML file
        einPaket     = ET.parse(f)                                 # parse the XML file
        einPaketRoot = einPaket.getroot()                          # get the root of tree
    except:                                                        # parsing not successfull
        if verbose:
            print("------- XML file for package '" + file + "' empty or not well-formed")
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
def load_document_file(href, key, name):
    """Loads one information file (PDF)."""
    
    # to be improved

    global pdfcounter
    global pdfctrerr

    call     = "wget " + href + parameter + direc + key + "-" + name
    noterror = False

    # @wait: 17.5.3 in library
    try:                                                           # tgry to download the PDF file and store
        process = subprocess.Popen(call, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = process.communicate(timeout=50)               # wait?
        if "ERROR" in errs:                                        # "ERROR" found in errs
            if verbose:
                print("------- PDF documentation file '" + name + "' not downloaded")
            pdfctrerr = pdfctrerr + 1                              # number of not downloaded PDF files is incremented
        else:
            if verbose:
                print("------- PDF documentation file '" + name + "' downloaded")
            pdfcounter = pdfcounter + 1                            # number of downloaded PDF files is incremented
            noterror = True
    except:                                                        # download was not successfull
        process.kill()                                             # kill the process
        outs, errs = process.communicate()                         # output and error messages
        if verbose:
            print("------- PDF documentation file '" + name + "' not downloaded")
    return noterror

# ------------------------------------------------------------------
def load_XML_toc():
    """Loads pickle file with XML_toc."""

    global XML_toc                                                 # global directory

    try:                                                           # try to open the pickle file
        pickleFile2 = open(direc + pkl_file2, "br")                # open the pickle file
        XML_toc     = pickle.load(pickleFile2)                     # unpickle the data
        pickleFile2.close()                                        # close the file
    except IOError:                                                # not successfull
        pass                                                       # do nothing

# ------------------------------------------------------------------
def generate_lists():
    """Generates some special files (with lists).:
       xyz.loa (list of authors = 'authors')
       xyz.lop (list of packages = 'packages')
       xyz.lok (list of topics = 'topics')
       xyz.lpt (list of topics and associated packages = 'topicspackage')
       xyz.lap (list of authors and associated packages = 'authorpackages')
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
def generate_pickle1():
    """pickle dump: authors, packages, topics, topicspackage, packagetopics"""

    # authors: directory (sorted)
    #   each element: [author key] <tuple with givenname and familyname>
    #
    # packages: directory (sorted)
    #   each element: [package key] <tuple with package name and package title>
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
    pickle_data1  = (authors, packages, topics, topicspackage, packagetopics, authorpackages)
    pickle.dump(pickle_data1, pickle_file1)                       # dump the data
    pickle_file1.close()                                          # close the file
    if verbose:
        print("--- pickle file '" + pickle_name1 + "' written")

# ------------------------------------------------------------------
def generate_pickle2():
    """pickle dump: XML_toc
    XML_toc       : list with download information files"""

    pickle_name2  = direc + pkl_file2
    try:                                                          # try to open the 2nd .pkl file
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
def check_integrity():
    """Checks integrity."""

    global corrected
    global PDF_toc                                                # list of local PDF files

    print("--- integrity check")
    load_XML_toc()                                                # load the 2nd pickle file

    noerror = True
    tmpdict = {}
    for t in XML_toc:                                             # loop: all members in XML_toc
        tmpdict[t] = XML_toc[t]                                   #    make a copy
        (file, fkey, onename) = XML_toc[t]                        #    get file, fkey, onename
        PDF_toc[fkey + "-" + onename] = file                      #    generate new entry in PDF_toc

    for f in tmpdict:
        tmp  = tmpdict[f]
        dd   = direc + tmp[1] + "-" + tmp[2]
        tmp2 = os.path.isfile(dd)                                 #    does the file exist?
        tmp4 = tmp[0]

        if tmp2:
            tmp2 = os.path.getsize(dd) > 0                        # file is not empty?
        noerror = noerror and tmp2
        tmp3    = dd

        if not tmp2:                                              # there is an error
            if verbose:
                print("----- entry '" + tmp3 + "' (resp. " + tmp4 + ") in directory, but file empty or not found")
            if os.path.isfile(tmp3):                              #    file exists
                os.remove(tmp3)                                   #    delete the associated PDF file
##                if verbose:
##                    print("----- PDF file '" + tmp3 + "' oi")
            del XML_toc[f]
            if verbose:
                print("----- entry '" + tmp3 + "' (resp. " + tmp4 + ") in directory deleted")
            corrected = corrected + 1

    ok = True
    for g in PDF_toc:                                             # move through list of local PDF files
        if PDF_toc[g] == "":                                      #    no entry: no ass. XML file
            ok = False
            if verbose:
                print("----- PDF file '" + g + "' without associated XML file")
            if os.path.isfile(g):
                os.remove(g)                                      #    delete the PDF file
                if verbose:
                    print("----- PDF file '" + g + "' deleted")

    if noerror and ok:                                            # there is no error
        if verbose:
            print("----- no error with integrity check")
    else:                                                         # there is an error
        if not noerror:
            generate_pickle2()                                    #    generate a new version of this pickle file

# ------------------------------------------------------------------
def make_statistics():
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
def get_PDF_files(d):
    """Lists all PDF files in a directory.

    d: directory"""

    global PDF_toc

    tmp  = os.listdir(d)                                          # get OS directory list
    tmp2 = {}
    for f in tmp:                                                 # all PDF files in current OS directory
        if p3.match(f):                                           #    check: file name matches p3
            tmp2[f] = ""                                          #    presets with empty string
    PDF_toc = tmp2

# ------------------------------------------------------------------
def main():
    """Main Function"""

    # main --> get PDF_files
    # main --> load_XML_toc
    # main --> load_topics
    # main --> load_authors
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

    load        = (template != "")                                # package files are to be loaded
    make_lists  = (not load) and lists                            # special list files are to be generated
    make_pickle = (not load) and (not lists)                      # pickle files are to be generated

    arguments   = ""
    tmp         = ""
    tmp_before  = ""
    e_parameter = ["-t","--template"]
     
    for f in range(1,len(call)):                                  # get and prepare the call parameters for output
        tmp = call[f]
        if tmp_before in e_parameter:
            tmp = '"' + tmp + '"'
        arguments = arguments + tmp + " "
        tmp_before = tmp
        
    if verbose:                                                   # output on terminal
        print("\n- program call: CTANLoad.py", arguments)

    if (template == "") and download:                             # test  template <-->  download
        if verbose:
            print("--- '-f'/'--download_files' valid only together with '-t'/'--template'; therefore ignored")
        download = False

    if download:                                                  # load the directory XML_toc
        load_XML_toc()

    load_topics()                                                 # load the file topics.xml
    load_authors()                                                # load the file authors.xml
    load_packages()                                               # load the file packages.xml

    if load:                                                      # if package files are to be loaded
        load_XML_files()                                          #     loads and processey all XML files in series
        if download:
            generate_pickle2()                                    #     dumps XML_toc

    if make_lists:                                                # if lists are to be generated
        generate_topicspackage()                                  #     generates topicspackage, ...
        generate_lists()                                          #     generates x.loa, x.lop, x.lok, x.lpt, x.lap
        generate_pickle1()                                        #     dumps authors, packages, topics, topicspackage, packagetopics

    if make_pickle:                                               # if the main pickle file is to be generated
        generate_topicspackage()                                  #     generates topicspackage, ...
        generate_pickle1()                                        #     dumps authors, packages, topics, topicspackage, packagetopics

    if integrity:                                                 # if the integrity is tobe checked
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

# script --> get_PDF_files
# script --> main

if __name__ == "__main__":
    get_PDF_files(direc)
    main()
else:
    if verbose:
        print("- tried to use the program indirectly")
