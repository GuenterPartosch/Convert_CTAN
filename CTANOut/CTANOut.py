#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# CTANOut.py (CTANout2b.py)
# (C) Günter Partosch, 2019/2021/2022

# see also CTANOut-changes.txt
#          CTANOut-messages.txt
#          CTANOut.man
#          CTANOut-examples.txt
#          CTANOut-mappings.txt
#          CTANOut-modules.txt
#          CTAN-files.txt


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
import codecs                                # needed for full UTF-8 output on stdout


#===================================================================
# Settings

programname             = "CTANOut.py"
programversion          = "2.24"
programdate             = "2022-03-01"
programauthor           = "Günter Partosch"
documentauthor          = "Developers and contributors for {\\TeX}, {\\LaTeX}, \\& Co"
documentauthor_txt      = "Developers and contributors for TeX, LaTeX, & Co"
authorinstitution       = "Justus-Liebig-Universität Gießen, Hochschulrechenzentrum"
authoremail             = "Guenter.Partosch@hrz.uni-giessen.de"
documenttitle           = "The CTAN book -- Packages on CTAN"
documentsubtitle        = "Collected, prepared and selected with the aid of the program "

operatingsys            = platform.system()        # operating system
call                    = sys.argv                 # actual program call
calledprogram           = sys.argv[0]              # name of called program

# ------------------------------------------------------------------
# Global settings

ctanUrl                 = "https://ctan.org"       # head of a CTAN url
ctanUrl2                = ctanUrl + "/tex-archive" # head of another CTAN url
ctanUrl3                = ctanUrl2 + "/install"    # head of another CTAN url
ctanUrl4                = ctanUrl + "/pkg/"        # head of another CTAN url
actDate                 = time.strftime("%Y-%m-%d")# actual date of program execution
actTime                 = time.strftime("%X")      # actual time of program execution

pickle_name1            = "CTAN.pkl"               # default name of the 1st pickle file
pickle_name2            = "CTAN2.pkl"              # default name of the 2nd pickle file
empty                   = ""                       # default text in some cases
blank                   = " "                      # default text in some other cases
file_encoding           = "UTF-8"                  # encoding of output file
ext                     = ".xml"                   # file name extension for info files to be downloaded

# ------------------------------------------------------------------
# Collect infos for elements which cannot be output in another way

list_info_files         = True                     # switch for RIS/BibLaTeX: XML_toc is to be proceeded
no_package_processed    = False                    # Flag: if no package is processed

year_default            = "1970"                   # default text for year
year_default2           = "without year"
max_year                = "2050"                   # maximum value for year
default_text            = "no text"                # default text for elements without embedded text
authorunknown           = "N. N."                  # default text for author
date_default            = year_default + "-01-01"  # default text for date
ellipsis                = " ..."                   # ellipsis
package_id              = empty                    # ID of a package
authorexists            = False                    # default for a global flag

notice                  = empty                    # collecting infos /RIS/BibLaTeX)
author_str              = empty                    # collecting authors of a package
date_str                = empty                    # collects date information
contact_str             = empty                    # collects contact information
version_str             = date_default             # collects all version items for a package
license_str             = empty                    # collects all license items for a package
also_str                = empty                    # collects all also items for a package
copyright_str           = empty                    # collects all copyright items for a package 
info_files              = []                       # default for each package: collection of local info files
language_set            = {'en'}                   # default for each package: collection of language items
year_str                = year_default             # default for each package: concatenation of year items
description_str         = empty                    # collects description content
level                   = empty                    # level of itemize/enumerate (<ol>, <ul>)

err_mode_text           = "- Warning: '{0} \"{1}\" ' changed to '{2}' (due to '{3}')"
exclusion               = ["authors.xml", "topics.xml", "packages.xml", "licenses.xml"]

maxcaptionlength        = 60                       # for LaTeX: max length for header lines
fieldwidth              = 10                       # for BibLaTeX: width of the field labels
ris_fieldwidth          = 5                        # for RIS: width of the field labels
txt_fieldwidth          = 18                       # for plain: width of the field labels
tex_fieldwidth          = 10                       # for LaTeX: width of the field labels
counter                 = 1                        # count for  packages
left                    = 35                       # width of labels in verbose output
labelwidth              = len("Web page on CTAN: ")# width of the longest label for LaTeX
cases                   = {"BibLaTeX":fieldwidth + 2, "LaTeX":tex_fieldwidth, "RIS":ris_fieldwidth + 1,
                           "plain":txt_fieldwidth, "Excel":0 } # length of left indentations

# ------------------------------------------------------------------
# Texts for argument parsing

author_text             = "Shows author of the program and exit."
author_template_text    = "Template for output filtering on the base of author names"
license_template_text   = "Template for output filtering on the base of license names"
version_text            = "Shows version of the program and exit."
verbose_text            = "Flag: Output is verbose."
statistics_text         = "Flag: Prints statistics on terminal."   
topics_text             = "Flag: Generates topic lists [meaning of topics/licenses + cross-reference (topics/packages, authors/packages, licenses/packages); only for -m LaTeX])."
btype_text              = "Type of BibLaTex entries to be generated [only for -m BibLateX]"
direc_text              = "Directory for input and output files"
key_text                = "Template for output filtering on the base of keys"
mode_text               = "Target format"
out_text                = "Generic name [without extensions] for output files"
program_text            = "Converts CTAN XLM package files to LaTeX, RIS, plain, BibLaTeX, Excel [tab separated]."
skip_text               = "Skips specified CTAN fields."
skip_biblatex_text      = "Skips specified BibLaTeX fields."
template_text           = "Template for output filtering on the base of package names"

# ------------------------------------------------------------------
# Defaults for argument parsing and further processing

make_topics_default      = False                    # default for topics output (-mt)
verbose_default          = False                    # default for global flag: verbose output (-v)
statistics_default       = False                    # default for global flag: statistics output (-stat)
license_template_default = """^.+$"""               # default for option -L (license name template)
name_template_default    = """^.+$"""               # default for file name template (-t) [at least one character]
filter_key_default       = """^.+$"""               # default for topic filter (-k) [at least one character]
author_template_default  = """^.+$"""               # default for author name template (-A) [at least one character]
btype_default            = "@online"                # default for BibLaTeX entry type (-b)
skip_default             = "[]"                     # default for option -s
skip_biblatex_default    = "[]"                     # default for option -sb
mode_default             = "RIS"                    # default for option -m
out_default              = "all"                    # default for generic output file name (-o)

act_direc               = "."                      # actual OS directory
if operatingsys == "Windows":    
    direc_sep      = "\\"                          #   directory separator
else:
    direc_sep      = "/"
direc_default           = act_direc + direc_sep    # default for -d (output directory)

make_topics             = None                     # variable for -mt
verbose                 = None                     # variable for -v
statistics              = None                     # variable for -stat
btype                   = empty                    # variable for -b
skip                    = empty                    # variable for -s
skip_biblatex           = empty                    # variable for -sb
mode                    = empty                    # variable for -m
name_template           = empty                    # variable for -t
author_template         = empty                    # variable for -A
out_file                = empty                    # variable for -o
filter_key              = empty                    # variable for -k
direc                   = empty                    # variable for -d

name_default            = name_template_default    # copy of name_template_default
filter_default          = filter_key               # copy of filter_key
    
# ------------------------------------------------------------------
# python dictionaries and lists

languagecodes   = {"ar":"Arabic",  "ar-dz":"Arabic (Algeria)",  "bg":"Bulgarian",  "bn":"Bengali", "ca":"Catalan",
                   "cs":"Czech",  "da":"Danish",  "de":"German",  "de,en":"German + English",  "de-de":"German (Germany)",
                   "el":"Greek",  "en":"English",  "en,ja":"English + Japanese",  "en-gb":"English (Great britain)",
                   "eo":"Esperanto",  "es":"Spanish",  "es-mx":"Spanish (Mexico)", "es-ve":"Spanish (Venezuela)",
                   "et":"Estonian",  "eu":"Basque",  "fa":"Farsi", "fa-ir":"Farsi (Iran)",  "fi":"Finnish",  "fr":"French",
                   "hi":"Hindi",  "hr":"Croatian", "hu":"Hungarian",  "hy":"Armenian",  "it":"Italian",  "ja":"Japanese",
                   "ka":"Georgian",  "ko":"Korean",  "lv":"Latvian",  "mn":"Mongolian",  "mr":"Marathi", "mr,hi":"Marathi + Hindi",
                   "nl":"Dutch", "nn-no":"Nynorsk",  "pl":"Polish",  "pt":"Portuguese", "pt-br":"Portuguese (Brazilia)",
                   "ru":"Russian",  "sk":"Slovak",  "sl":"Slovenian",  "sr":"Serbian", "sr-sp":"Serbian (Serbia)",  "th":"Thai",
                   "tr":"Turkish",  "uk":"Ukrainian",  "vi":"Vietnamese", "zh":"Chinese",  "zh,en":"Chinese + English",
                   "zh,ja":"Chinese + Japanese",  "zh-cn":"Chinese (China)"}

usedTopics               = {}                      # Python dictionary:  collect used topics for all packages
usedPackages             = []                      # python list:        collect used packages
usedAuthors              = {}                      # Python dictionary:  collect used authors for all packages
usedLicenses             = {}                      # Python dictionary:  collect used licenses for all packages

allauthoryears           = {}                      # Python dictionary:  each element: allauthoryears[(<author>,<year>] = <appendix>
citation_keys            = {}                      # Python dictionary:  each element: citation_keys[package] = (<author>, <year>, <appendix>)

XML_toc                  = {}                      # python dictionary:  list of XML and PDF files: XML_toc[CTAN address]=(XML file, key, plain PDF file name)
packages                 = {}                      # python dictionary:  each element: <package key>:<tuple with package name and package title>
topics                   = {}                      # python dictionary:  each element: <topics name>:<topics title>
licenses                 = {}                      # python dictionary:  each element: <license key>:<license title>
topicspackage            = {}                      # python dictionary:  each element: <topic key>:<list with package names>
packagetopics            = {}                      # python dictionary:  each element: <topic key>:<list with package names>
authorpackages           = {}                      # python dictionary:  each element: <author key>:<list with package names>
authors                  = {}                      # python dictionary:  each element: <author key>:<tuple with givenname and familyname>

# ------------------------------------------------------------------
# Strings for Excel output

s_id                     = empty                   # id attribute in entry element
s_id_text                = "id"                    # id attribute in entry element
s_author                 = empty                   # authoref elements (collected)
s_author_text            = "author"                # authoref elements (collected)
s_name                   = empty                   # name element
s_name_text              = "name"                  # name element
s_caption                = empty                   # caption element
s_caption_text           = "caption"               # caption element
s_year                   = empty                   # extracted from copyright and version
s_year_text              = "year"                  # extracted from copyright and version
s_lastchanges            = empty                   # extracted from version element
s_lastchanges_text       = "lastchanges"           # extracted from version element
s_language               = empty                   # extracted from documentation and description (collected)
s_language_text          = "language"              # extracted from documentation and description (collected)
s_lastaccess             = empty                   # day of last download
s_lastaccess_text        = "lastaccess"            # day of last download
s_version                = empty                   # version element
s_version_text           = "version"               # version element
s_keyval                 = empty                   # keyval elements (collected)
s_keyval_text            = "keyval"                # keyval elements (collected)
s_alias                  = empty                   # alias element
s_alias_text             = "alias"                 # alias element
s_also                   = empty                   # alias element
s_also_text              = "also"                  # alias element
s_contact                = empty                   # contact element
s_contact_text           = "contact"               # contact element
s_copyright              = empty                   # copyright elements (collected)
s_copyright_text         = "copyright"             # copyright elements (collected)
s_ctan                   = empty                   # ctan element
s_ctan_text              = "CTAN"                  # ctan element
s_documentation          = empty                   # documentation elements (collected)
s_documentation_text     = "documentation"         # documentation elements (collected)
s_home                   = empty                   # home element
s_home_text              = "home"                  # home element
s_install                = empty                   # install element
s_install_text           = "install"               # install element
s_license                = empty                   # license elements (collected)
s_license_text           = "license"               # license elements (collected)
s_miktex                 = empty                   # miktex element
s_miktex_text            = "MikTeX"                # miktex element
s_texlive                = empty                   # texlive element
s_texlive_text           = "TeXLive"               # texlive element


#===================================================================
# Parsing the arguments

parser = argparse.ArgumentParser(description = "[" + programname + "; " + "Version: " + programversion + " (" + programdate + ")] " + program_text)
parser._positionals.title = 'Positional parameters'# there are none
parser._optionals.title   = 'Options'

parser.add_argument("-a", "--author",              # Parameter -a/--author
                    help    = author_text,
                    action  = 'version',
                    version = programauthor + " (" + authoremail + ", " + authorinstitution + ")")

parser.add_argument("-A", "--author_template",     # Parameter -A/--author_template
                    help    = author_template_text + " - Default: " + "%(default)s",
                    dest    = "author_template",
                    default = author_template_default)

parser.add_argument("-b", "--btype",               # Parameter -b/--btype
                    help    = btype_text + " - Default: " + "%(default)s",
                    choices = ["@online", "@software", "@misc", "@ctan", "@www", "@electronic"],
                    dest    = "btype",
                    default = btype_default)

parser.add_argument("-d", "--directory",           # Parameter -d/--directory
                    help    = direc_text + " - Default: " + "%(default)s",
                    dest    = "direc",
                    default = direc_default)

parser.add_argument("-k", "--key",                 # Parameter -k/--key
                    help    = key_text + " - Default: " + "%(default)s",
                    dest    = "filter_key",
                    default = filter_key_default)

parser.add_argument("-L", "--license_template",    # Parameter -L/--license_template
                    help    = license_template_text + " - Default: " + "%(default)s",
                    dest    = "license_template",
                    default = license_template_default)

parser.add_argument("-m", "--mode",                # Parameter -m/--mode
                    help    = mode_text + " - Default: " + "%(default)s",
                    choices = ["LaTeX", "latex", "tex", "RIS", "plain", "txt", "BibLaTeX", "biblatex", "bib", "ris", "Excel", "excel", "tsv", "csv"],
                    dest    = "mode",
                    default = mode_default)

parser.add_argument("-mt", "--make_topics",        # Parameter -mt/--make_topics
                    help    = topics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = make_topics_default)

parser.add_argument("-o", "--output",              # Parameter -o/--output
                    help    = out_text + " - Default: " + "%(default)s",
                    dest    = "out_file",
                    default = out_default)

parser.add_argument("-s", "--skip",                # Parameter -s/--skip
                    help    = skip_text + " - Default: " + "%(default)s",
                    dest    = "skip",
                    default = skip_default)

parser.add_argument("-sb", "--skip_biblatex",      # Parameter -sb/--skip_biblatex
                    help    = skip_biblatex_text + " - Default: " + "%(default)s",
                    dest    = "skip_biblatex",
                    default = skip_biblatex_default)

parser.add_argument("-t", "--template",            # Parameter -t/--template
                    help    = template_text + " - Default: " + "%(default)s",
                    dest    = "name_template",
                    default = name_template_default)

parser.add_argument("-stat", "--statistics",       # Parameter -stat/--statistics
                    help    = statistics_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = statistics_default)

parser.add_argument("-v", "--verbose",             # Parameter -v/--verbose
                    help    = verbose_text + " - Default: " + "%(default)s",
                    action  = "store_true",
                    default = verbose_default)

parser.add_argument("-V", "--version",             # Parameter -V/--version
                    help    = version_text,
                    action  = 'version',
                    version = '%(prog)s ' + programversion + " (" + programdate + ")")

# ------------------------------------------------------------------
# Getting parsed values

args             = parser.parse_args()
author_template  = args.author_template      # parameter -A
btype            = args.btype                # Parameter -b
direc            = args.direc                # Parameter -d
license_template = args.license_template     # parameter -L
make_topics      = args.make_topics          # Parameter -mt
mode             = args.mode                 # Parameter -m
name_template    = args.name_template        # Parameter -t
out_file         = args.out_file             # Parameter -o
filter_key       = args.filter_key           # Parameter -k
skip             = args.skip                 # Parameter -s
skip_biblatex    = args.skip_biblatex        # Parameter -sb
verbose          = args.verbose              # Parameter -v
statistics       = args.statistics           # Parameter -stat

# ------------------------------------------------------------------
# Resettings and settings

if mode in ["latex", "LaTeX", "tex"]:       # -m latex in call
    mode = "LaTeX"                          #   mode is reset
if mode in ["ris", "RIS"]:                  # -m ris in call
    mode = "RIS"                            #   mode is reset 
if mode in ["biblatex", "BibLaTeX", "bib"]: # -m biblatex in call
    mode = "BibLaTeX"                       #   mode is reset
if mode in ["excel", "Excel", "tsv", "csv"]:# -m excel in call
    mode = "Excel"                          #   mode is reset
if mode in ["plain", "txt"]:                # -m plain in call
    mode = "plain"                          #   mode is reset

if (skip_biblatex != skip_biblatex_default) and (mode != "BibLaTeX"): 
    if verbose:                             # "- Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
        print(err_mode_text.format('-m', mode, '-m BibLaTeX', '-sb'))
    mode  = "BibLaTeX"                      #   mode is set to BibLaTeX if -sb is given
    if verbose:                             # "- Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
        print(err_mode_text.format('-b', btype, '-b @online', '-sb')) 
    btype = "@online"                       #   btype is reset

if (btype != btype_default) and (mode != "BibLaTeX"): 
    if verbose:                             # "- Warning: '{0} {1}' changed to '{2}' (due to '{3}')"
        print(err_mode_text.format('-m', mode, '-m BibLaTeX', '-b')) 
    mode = "BibLaTeX"                       # mode is set to BibLaTeX if -b is given

if (make_topics != make_topics_default) and (mode != "LaTeX"):
    if verbose:
        print(err_mode_text.format('-m', mode, '-m LaTeX', '-mt'))
    mode = "LaTeX"                          # mode is set to LaTeX if -mt is given

# ------------------------------------------------------------------
# Correct directory name, test directory existence, and/or install directory

direc = direc.strip()                       # strip directory name (-d)
if direc[len(direc) - 1] != direc_sep:      #   append a separator, if necessary
    direc += direc_sep
    
if not path.exists(direc):                  
    try:
        os.mkdir(direc)                     # create OS directory, if necessary 
    except OSError:
        print ("- Warning: Creation of the OS directory '{0}' failed".format(direc))
    else:
        print ("- Info: Successfully created OS the directory '{0}' ".format(direc))

# ------------------------------------------------------------------
# pre-compiled regular expressions (based on specified options)

p2 = re.compile(name_template)              # regular expression based on -t
p3 = re.compile(filter_key)                 # regular expression based on -k
p4 = re.compile("[- |.,a-z]")               # split a string to find year data
p5 = re.compile(author_template)            # regular expression based on -A
p6 = re.compile("^.+[.]xml$")               # regular expression for local XML file names
p7 = re.compile("[\s]+")                    # regular expression: test of "white space"
p8 = re.compile("§§=([1-2][0-9]|[1-9])")    # regular expression: processing of "§§=xx"
p9 = re.compile(license_template)           # regular expression based on -L


#===================================================================
# Other settings

# ------------------------------------------------------------------
# Full name for the output file (with file name extensions)

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

out = open(direc + out_file, encoding=file_encoding, mode="w") # open output file

# ------------------------------------------------------------------
# Preambel for LaTeX output

if mode in ["LaTeX"]:                       # only for LaTeX: package loading + font declaration
    usepkg  = """
\\usepackage[bidi=basic]{babel}          % language support
\\usepackage{fontspec}                   % font specification
\\babelprovide[import, onchar=ids fonts]{hindi}

\\defaultfontfeatures{Scale=MatchUppercase,
                      Ligatures=TeX,
                      Renderer=HarfBuzz}
\\babelfont[hindi]{rm}{Shobhika}
\\babelfont{rm}[Ligatures=Common, Scale=1.0]{Libertinus Serif}
\\babelfont{sf}[Ligatures=Common]{Libertinus Sans}
\\babelfont{tt}[Scale=0.9]{Libertinus Mono}

\\usepackage{makeidx}                    % index generation
\\usepackage[colorlinks=true]{hyperref}  % hypertext structures

\\newcommand{\inp}[1]{\\IfFileExists{#1}{\\input{#1}}{}}

\\makeindex"""

# ------------------------------------------------------------------
# Only for LaTeX (header of the LaTeX file)

if mode in ["LaTeX"]:                       # only for LaTeX: class options and trailer
    classoptions = """                      
paper    = a4,       % paper A4
fontsize = 11pt,     % font size
parskip  = half,     % half parskip
numbers  = noenddot, % no dot after section number
index    = totoc,    % index in TOC
headings = small,    % small headers
DIV      = 12,       % 12-strip page layout
english"""
    
    title        = """
\\title{""" + documenttitle + """}
\\subtitle{""" + documentsubtitle + "\\texttt{" + programname + """}}
\\author{""" + documentauthor + """}
\\date{\\today}\n"""
    
    header       = "\n\\begin{{document}}\n \\pagestyle{{headings}}\n \\maketitle\n \\inp{{{0}.stat}}\n \\newpage\n".format(args.out_file)
    trailer      = empty
    if make_topics:                         # option -mt is specified
        trailer = trailer + "\n\\newpage\n\\appendix"   
        trailer = trailer + "\n\\inp{" + args.out_file + ".top}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".xref}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".tap}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".lic}"
        trailer = trailer + "\n\\inp{" + args.out_file + ".tlp}"
        trailer = trailer + "\n\\printindex\n\\end{document}\n"


# ======================================================================
# auxiliary functions

# ------------------------------------------------------------------
def bibfield_test(s, f):                                   # auxiliary function bibfield_test: output text is not empty and field is not be skipped
    """auxiliary function: tests a BibLaTeX field: output text is not empty and field is not be skipped.

    s: string for output
    f: BibLaTeX field

    returns True/False"""
    
    return (s != empty) and (not f in skip_biblatex)

# ------------------------------------------------------------------
def biblatex_citationkey():                                # auxiliary function: Generates a dictionary with citations keys for all packages
    """auxiliary function: Generates a dictionary with citations keys for all packages.

    citation_keys[package] = (name, year, appendix)

    inspects the authorref, version, copyright elements."""

    global citation_keys                                   # set: citation keys

    # biblatex_citationkeys --> get_year()
    # biblatex_citationkeys --> get_authoryear()
        
    author_id_default = authorunknown
    citation_key      = {}
    
    tmp = get_local_packages(direc)                        # get a directory list
    
    for f in tmp:                                          # some dafaults for the actual pacKAGE
        auth         = []                                  
        vers         = empty
        copyr        = empty
        author       = empty
        givenname    = empty
        familyname   = empty
        version_date = empty
        ff           = direc + f + ext
        
        try:
            op = ET.parse(ff)                              # parse XML file
            OK = True
        except:                                            # not successfull
            if verbose:
                print("- Warning: XML file for package '{0}' not well-formed".format(ff))
            OK = False
            
        if OK:
            opRoot = op.getroot()                          # analyze package file
            for child in opRoot:
                if child.tag == "authorref":               # element <authorref ...>
                    author_id = child.get("id", author_id_default)
                    auth.append(author_id)
                elif child.tag == "version":               # element <version ...>
                    version_date = child.get("date", "")
                elif child.tag == "copyright":             # element <copyright ...>
                    copyright_year = child.get("year", year_default)
                    copyr          = copyr + blank + copyright_year
                    
            if len(auth) == 0:                             # if no author is specified
                familyname = author_id_default
                givenname  = author_id_default
            else:
                id                    = auth[0]
                givenname, familyname = authors[id]        # get the author's name
                
            year = version_date + blank + copyr            # string to be analyzed
            if (year == blank) or (year == empty):         # if any year is not specified
                year = year_default
            year             = get_year(year)              # get the year
            tmp              = get_authoryear(familyname, year)
            citation_keys[f] = tmp
    if verbose:
        print("- Info: all package files analyzed and dictionary citation_keys created.")

# ------------------------------------------------------------------
def comment_fold(s):                                       # auxiliary function: shortens/folds long option values in LaTeX comment output
    """auxiliary function: Shortens/folds long option values in LaTeX comment output

    s: string

    Returns a string."""
     
    offset = 28 * blank
    maxlen = 120
    sep    = "|"
    parts  = s.split(sep)
    line   = empty
    out    = empty
    
    for f in range(0, len(parts)):
        if f != len(parts) - 1:
            line = line + parts[f] + sep
        else:
            line = line + parts[f]
        if len(line) >= maxlen:
            out  = out + line + "\n%" + offset + ": "
            line = empty
    out = out + line            
    return out

# ------------------------------------------------------------------
def fold(s):                                               # auxiliary function fold: shortens long option values for output
    """auxiliary function: Shortens/folds long option values for normal output

    s: string

    Returns a string."""
    
    offset = 64 * blank                                    # left indentation
    maxlen = 70                                            # maximal lined length
    sep    = "|"                                           # split on sep
    parts  = s.split(sep)
    line   = empty
    out    = empty
    
    for f in range(0, len(parts)):
        if f != len(parts) - 1:
            line = line + parts[f] + sep
        else:
            line = line + parts[f]
        if len(line) >= maxlen:
            out  = out + line + "\n" + offset
            line = empty
    out = out + line            
    return out

# ------------------------------------------------------------------
def gen_fold(s, o):                                         # auxiliary function gen_fold: folds content of <p>, <li>, <dd> (mode dependant)
    """auxiliary function: folds content of <p>, <li>, <dd> (mode dependant)

    s: string
    o: offset

    Returns a string."""
    
    offset = "§§=" + str(o)
    maxlen = 100                                            # maximal line length
    sep    = blank                                          # seperation character for output
    parts  = p7.split(s)                                    # split on p7
    line   = empty
    out    = empty

    if len(s) >= maxlen:
        for f in range(0, len(parts)):
            if f != len(parts) - 1:
                line = line + parts[f] + sep
            else:
                line = line + parts[f]
            if len(line) > maxlen:
                out  = out + line + "§§-" + offset
                line = empty
        out = out + line
    else:
        out = s
    return out

# ------------------------------------------------------------------
def get_authoryear(a, y):                                  # auxiliary function get_authoryear: constructs a unique authoryear string (for BibLaTeX only)
    """auxiliary function: Constructs a unique authoryear string (for BibLaTeX)
    performs some changes according to the BibLaTeX rules

    a: familyname (string)
    y: year (int)

    returns a tuple (name, year, appendix)"""

    global allauthoryears

    name = a
    if name == "":                                         # if name is not specified
        name = authorunknown
    
    name = re.sub("Jr", "", name)                          # some changes
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
    
    tmp  = (name, str(y))                                        # construct an author year tuple
    if not (tmp in allauthoryears):                              # store it in a dictionary
        allauthoryears[tmp] = ord("a") - 1
    else:
        tmp2  = allauthoryears[tmp]                              # append a small letter 
        tmp2 += 1                                                # (the next in the alphabet)
        allauthoryears[tmp] = tmp2
        if tmp2 <= 122: 
            tmp = (name, str(y), "." + chr(tmp2))
        else:                                                    # add a second letter
            remain = (tmp2 - 97) % 26 + 1
            times  = (tmp2 - 97) // 26
            tmp    = (name, str(y), "." + chr(times + 96) + chr(remain + 96))
    return tmp

# ------------------------------------------------------------------
def get_local_packages(d):                                 # auxiliary function get_local_packages(d): Lists all local packages in the current OS directory 
    """auxiliary function: Lists all local packages in the current OS directory d

    d: OS directory to be analyzed

    returns a set"""

    tmp  = os.listdir(d)                                   # get local OS directory list
    tmp2 = []
    
    for f in tmp:                                          # check all the files
        if p6.match(f) and not (f in exclusion):           #   name matches
            tmp3 = f[0:len(f) - 4]
            tmp2.append(tmp3)
    return set(tmp2)

# ------------------------------------------------------------------
def get_year(s):                                           # auxiliary function: gets the most recent year in string s (only for BibLaTeX)
    """auxiliary function: Gets the most recent year in string s (only for BibLaTeX)
    includes decimal numbers in the intervall [year_default, max_year]

    s: string

    returns the maximum year in s."""
    
    nn    = p4.split(s)                                    # split the given string according p4: re.compile("[- |.,a-z]")
    years = []
    yd    = int(year_default)
    for i in nn:                                           # loop over all elements
        if i.isdecimal():                                  #   element is decimal
            if (yd <= int(i)) and (int(i) <= int(max_year)):#     element is in the intervall [year_default, max_year]?
                years.append(int(i))                       #     element is collected
    if len(years) >= 1:                                    # there is at least one year
        return max(years)                                  # maximum is calculated
    else:                                                  # there is no year
        return year_default

# ------------------------------------------------------------------
def TeX_fold(s):                                           # auxiliary function TeX_fold: shortens/folds long option values in LaTeX tabular output
    """auxiliary function: Shortens/folds long option values in LaTeX tabular output

    s: string

    Returns a string."""
     
    offset = 64 * blank                                    # left indendation
    maxlen = 65                                            # maximal line length
    sep    = "|"                                           # separaor in input and output
    parts  = s.split(sep)
    line   = empty
    out    = empty
    
    for f in range(0,len(parts) ):
        if f != len(parts) - 1:
            line = line + "\\verb§" + parts[f] + sep + "§"
        else:
            line = line + "\\verb§" + parts[f] + "§"
        if len(line) >= maxlen:
            out  = out + line + "\\\\\n" + offset + "&"
            line = empty
    out = out + line            
    return out

# ------------------------------------------------------------------
def TeXchars(s):                                          # auxiliary function: prepares characters for LaTeX/BibLaTeX
    """auxiliary function: Prepares characters for LaTeX/BibLaTeX (with the exception of desc ription).

    s: string

    returns a changed string s."""
    
    tmp = s
    tmp = re.sub(r"\\", r"{\\textbackslash}", tmp)
    tmp = re.sub("_", r"\\_", tmp)
    tmp = re.sub("&", r"{\\&}", tmp)
    tmp = re.sub(r"[\^]", r"{\\textasciicircum}", tmp)
    tmp = re.sub("[$]", r"\\$", tmp)
    return tmp


# ==================================================================
# main functions

# ------------------------------------------------------------------
def alias(k):                                     # function: processes element <alias .../>
    """Processes the alias element.

    k: current knot

    inspects embedded text and the ambedded attribute id. """

    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global s_alias                                # string for Excel: alias
    global package_id                             # string: package id

    id  = k.get("id", empty)                      # get attribute id
    
    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                             
    else:
        tmp = default_text                        # if k.text is empty

    if mode in ["LaTeX"]:                         # LaTeX
        out.write(r"\item[Alias] " + r"\texttt{" + tmp + "}\n")
        out.write("\\index{{Package!{0} (alias for {1})}}\n".format(tmp, package_id))
        out.write("\\index{{Alias!{0} (for {1})}}\n".format(tmp, package_id))
    elif mode in ["plain"]:                       # plain
        if tmp != empty:
            out.write("\n" + "alias: ".ljust(labelwidth) + tmp)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if notice != empty:                       # accumulate notice string
            notice += ";\n" + blank * (fieldwidth + 2) + "Alias: " + tmp
        else:
            notice = "Alias: " + tmp 
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:                       # accumulate notice string
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Alias: " + tmp
        else:
            notice = "Alias: " + tmp 
    elif mode in ["Excel"]:                       # Excel
        if s_alias != empty:
            s_alias += "; " + tmp                 #   accumulate s_alias string
        else:
            s_alias = tmp

# ------------------------------------------------------------------
def also(k):                                      # function: processes element <also .../>
    """Processes the also elements.

    k: current knot

    fetches the local attribute refid."""

    # also --> TeXchars
    
    global s_also                                 # string for Eccel: also
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global also_str                               # string: collect also

    refid = k.get("refid",empty)                  # get attribute refid

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
        if notice != empty:                       #   accumulate notice string
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Also: " + refid
        else:
            notice += "Also: " + refid
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if refid in packages:
            tmp = empty.join(citation_keys[refid])
            if also_str != empty:
                also_str += "; " + tmp            #   accumulate also_str string
            else:
                also_str = tmp
    elif mode in ["Excel"]:                       # Excel
        if refid in packages:
            if s_also != empty:
                s_also += "; " + refid            #   accumulate s_also string 
            else:
                s_also = refid

# ------------------------------------------------------------------
def authorref(k):                                 # function: processes element <authorref .../>
    """Processes the authorref elements, constructs the complete name and usedAuthors entry.

    k: current knot

    fetches the local attributes key, id, givenname, familyname, active."""
    
    global authorexists                           # flag
    global s_author                               # string for Excel: authorref
    global usedAuthors                            # dictionary: collects used authors

    key        = k.get("key", empty)              # get attribute key
    xid        = k.get("id", empty)               # get attribute id
    givenname  = k.get("givenname", empty)        # get attribute givenname
    familyname = k.get("familyname", empty)       # get attribute familyname
    active     = k.get("active", empty)           # get attribute active
    tmp        = givenname

    if (xid != empty) and (xid in authors):       # attribute xid is used
        key = xid
        givenname, familyname = authors[xid]      #   find givenname, familyname in authors 
        tmp = givenname
    else:
        key = xid
        givenname, familyname = empty, authorunknown#   givenname, familyname not found
        tmp = givenname

    if familyname != empty:                       # constructs the complete name + usedAuthors entry
        tmp  += blank + familyname
        tmp2 = familyname + ", " + givenname
        usedAuthors[key] = (givenname, familyname)#   store actual author in usedAuthors
    else:
        tmp2             = tmp
        usedAuthors[key] = (givenname)            #   store actual author in usedAuthors

    if active == "false":
        tmp = tmp + " (not active)"

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[author] {0}\n".format(tmp))
        out.write("\\index{{Author!{0}}}\n".format(tmp2)) 
    elif mode in ["RIS"]:                         # RIS
        out.write("AU  - " + tmp2 + "\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "author: ".ljust(labelwidth) + tmp)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        pass                                      #   for BibLaTeX do nothing 
    elif mode in ["Excel"]:                       # Excel
        pass                                      #   for Excel do nothing 

    authorexists = True

# ------------------------------------------------------------------
def caption(k):                                   # function: processes element <caption>...</caption>
    """Processes the caption element (sub title).

    k: current knot

    Fetches any embedded text."""

    # caption --> TeXchars
    # caption --> bibfield_test
    
    global s_caption                              # string for Excel: caption

    if len(k.text) > 0:                           # get embedded text
        tmp = k.text.strip()
    else:
        tmp = default_text                        #   if k.text is empty

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        tmp = re.sub("#", "\\#", tmp)
        out.write("\\item[caption] {0}\n".format(tmp))
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "caption: ".ljust(labelwidth) + tmp)
    elif mode in ["RIS"]:                         # RIS
        out.write("T2  - {0}\n".format(tmp))      #   subtitle
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = TeXchars(tmp)
        tmp = re.sub("#", "\\#", tmp)
        
        if bibfield_test(tmp, "subtitle"):        #   subtitle
            out.write("subtitle".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_caption = tmp

# ------------------------------------------------------------------
def contact(k):                                   # function: processes element <contact .../>
    """Processes the contact elements.

    k: current knot

    Fetches the local attributes type, href."""
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note  
    global contact_str                            # string: collect contact
    global s_contact                              # string for Excel

    typeT = k.get("type", empty)                  # get attribute type (announce, bugs, development, repository, support)
    href  = k.get("href", empty)                  # get attribute href

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[contact] \\textit{{{0}}}: \\url{{{1}}}\n".format(typeT, href))
        out.write("\\index{{Contact!{0}}}\n".format(typeT))
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:                       #   accumulate notice string
            notice += "\\\\\n" + blank * (ris_fieldwidth + 1) + "Contact: " + typeT + ": " + href
        else:
            notice = "Contact: " + typeT + ": " + href 
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if contact_str != empty:                  #   accumulate contact_str string
            contact_str += "; " + typeT + ": " + href
        else:
            contact_str = typeT + ": " + href
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "contact: ".ljust(labelwidth) + typeT + ": " + href)
    elif mode in ["Excel"]:                       # Excel
        if s_contact != empty:                    #   accumulate s_contact string
            s_contact += "; " + typeT + ": " + href
        else:
            s_contact = typeT + ": " + href

# ------------------------------------------------------------------
def copyrightT(k, p):                             # function: processes element <copyright .../>
    """Processes the copyright element.

    k: current knot
    p: current package

    Fetches the emebedded attributes owner, year."""

    # copyrighT --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global copyright_str                          # string: collect copyright
    global s_copyright                            # string for Excel: copyright
    global year_str                               # string: collect all year items for a package

    owner    = k.get("owner", empty)              # get attribute owner
    year     = k.get("year", "--")                # get attribute year

    year_str = year_str + "|" + year              # append year to year_str

    tmp   = owner                                 
    if year != "--":                              # construct "owner (year)"
        tmp = tmp + " (" + year + ")"
    tmp = re.sub("[ \t]+", " ", tmp)

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        out.write("\\item[copyright] {0}\n".format(tmp))
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Copyright: " + tmp
        else:
            notice = "Copyright: " + tmp
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = re.sub("_", r"\\_", tmp)
        tmp = TeXchars(tmp)
        if copyright_str != empty:
            copyright_str += "; " + tmp
        else:
            copyright_str = tmp
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "copyright: ".ljust(labelwidth) + tmp)
    elif mode in ["Excel"]:                       # Excel
        if s_copyright != empty:
            s_copyright += "; " + tmp             # accumulate s_copyright string
        else:
            s_copyright = tmp

# ------------------------------------------------------------------
def ctan(k, t):                                   # function: processes element <ctan .../>
    """Processes the ctan element.

    k: current knot
    t: current package date

    Fetches the local attributes path and file."""

    # ctan --> bibfield_test
    
    global s_ctan                                 # string for Excel: ctan
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note

    xpath = k.get("path", empty)                  # get attribute path
    file  = k.get("file", empty)                  # get attribute file

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[on CTAN] \\url{{{0}}}\n".format(ctanUrl2 + xpath))
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "on CTAN: " + ctanUrl2 + xpath
        else:
            notice = "on CTAN: " + ctanUrl2 + xpath
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "on CTAN: ".ljust(labelwidth) + ctanUrl2 + xpath)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if bibfield_test(ctanUrl2 + xpath, "userc"):
            out.write("userc".ljust(fieldwidth) + "= {" + ctanUrl2 + xpath + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_ctan = ctanUrl2 + xpath

# ------------------------------------------------------------------
def documentation(k):                             # function: processes element <documentation .../>
    """Processes the documentation elements.

    k: current knot

    Fetches the local attributes details, href, language."""

    # documentation --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global language_set                           # set: collect language
    global info_files                             # list of local PDF files
    global XML_toc                                # python dictionary:  list of XML and PDF files: XML_toc[CTAN address]=(XML file, key, plain PDF file name)
    global s_documentation                        # string for Excel: documentation

    details  = k.get("details", empty)            # get attribute details
    href     = k.get("href", empty)               # get attribute href
    language = k.get("language", empty)           # get attribute language

    href2    = href.replace("ctan:/", ctanUrl2)
    p        = None

    if language in languagecodes:                 # convert language keys
        languagex = " (" + languagecodes[language] + ")"
    else:
        languagex = empty
    language_set.add(language)

    if languagex != empty:
        p = re.search(languagecodes[language], details)

    if mode in ["LaTeX"]:                         # LaTeX
        details = TeXchars(details)
        if languagex != empty:
            out.write("\\index{{Language in description/documentation!{0}}}\n".format(languagecodes[language]))
        if p == None:                             #   no language found in details
            out.write("\\item[documentation] {0} \\textit{{{1}}}: \\url{{{2}}}\n".format(languagex, details, href2))
        else:
            out.write("\\index{{Language in description/documentation!{0}}}\n".format(p.group()))
            out.write("\\item[documentation] \\textit{{{0}}}: \\url{{{1}}}\n".format(details, href2))
        if href in XML_toc:
            tmp    = XML_toc[href]
            one_if = tmp[1] + "-" + tmp[2]        #   one info file
            fx2    = "./" + one_if
            out.write("\\item[--local file]".ljust(labelwidth + 1) + " \\verb|" + fx2 + "|\n")
    elif mode in ["RIS"]:                         # RIS
        if list_info_files:
            out.write("UR  - {0}\n".format(href2))
            if href in XML_toc:
                tmp    = XML_toc[href]
                one_if = tmp[1] + "-" + tmp[2]    #   one info file
                fx     = os.path.abspath(one_if)
                out.write("L1  - {0}\n".format(fx))
        if p == None:                             #   no language found in details
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Documentation" + languagex + ": " + details + ": " + href2
        else:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Documentation" + ": " + details + ": " + href2
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        details = TeXchars(details)
        if list_info_files:
            if href in XML_toc:
                tmp        = XML_toc[href]
                one_if     = tmp[1] + "-" + tmp[2]#   one info file
                info_files += [one_if]
        if p == None:                             #   no language found in details
            tmp = "Documentation{0}: {1}: {2}".format(languagex, details, href2)
        else:
            tmp = "Documentation: {0}: {1}".format(details, href2)
            
        if notice != empty:                       #   accumulate notice string
            notice += ";\n" + blank * (fieldwidth + 2) + tmp
        else:
            notice = tmp
    elif mode in ["plain"]:                       # plain
        if p == None:                             #   no language found in details
            out.write("\ndocumentation: ".ljust(labelwidth + 1) + details + languagex + ": " + href2)
        else:
            out.write("\ndocumentation: ".ljust(labelwidth + 1) + details + ": " + href2)
        if href in XML_toc:
            tmp    = XML_toc[href]
            one_if = tmp[1] + "-" + tmp[2]        #   one info file
            dx     = "./" + one_if
            out.write("\n--local file: ".ljust(labelwidth + 1) + dx)
    elif mode in ["Excel"]:                       # Excel
        if s_documentation != empty:              #   accumulate s_documentation string
            s_documentation += "; " + details + ": " + href2
        else:
            s_documentation = details + ": " + href2

# -----------------------------------------------------------------
def entry(k, t, p):                               # function: processes element <entry ...>...</entry>
    """Processes the main element entry.

    k: current knot
    t: date
    p: current package

    Fetches the local attribute id.
    Fetches the embedded text."""

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
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global package_id                             # string: package id
    global s_id, s_alias, s_also, s_author, s_caption, s_contact, s_copyright, s_ctan, s_date
    global s_documentation, s_home, s_install, s_keyval, s_language, s_license, s_miktex
    global s_name, s_texlive, s_version, s_year, s_lastchanges, s_lastaccess

    if mode in ["Excel"]:                         # initialize strings for Excel; id attribute in entry element
        s_id                    = k.get("id", empty) # get attribute id
        s_alias                  = empty          # alias element
        s_also                   = empty          # also element
        s_author                 = empty          # authoref elements (collected)
        s_caption                = empty          # caption element
        s_contact                = empty          # contact element
        s_copyright              = empty          # copyright elements (collected)
        s_ctan                   = empty          # ctan element
        s_date                   = empty          # xx element
        s_documentation          = empty          # documentation elements (collected)
        s_home                   = empty          # home element
        s_install                = empty          # install element
        s_keyval                 = empty          # keyval elements (collected)
        s_language               = empty          # extracted from documentation and description (collected)
        s_license                = empty          # license elements (collected)
        s_miktex                 = empty          # miktex element
        s_name                   = empty          # name element
        s_texlive                = empty          # texlive element
        s_version                = empty          # version element
        s_year                   = empty          # extracted from copyright and version
        s_lastchanges            = empty          # extracted from version element
        s_lastaccess             = empty          # day of last download

    leading(k, p, t)
    package_id = k.get("id", empty)               # get attribute id

    for child in k:                               # call the sub-elements
        if child.tag == "description":            # description
            if mode != "Excel":                   #   not for Excel
                if not child.tag in skip:
                    description(child, p)
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
                copyrightT(child, p)
        elif child.tag == "license":              # license
            if not child.tag in skip:
                licenseT(child)
        elif child.tag == "version":              # version
            if not child.tag in skip:
                version(child, p)
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
    trailing(k, t, p)

# ------------------------------------------------------------------
def first_lines():                                # function: creates the first lines of output.
    """Creates the first lines of output"""
    
    arguments   = empty
    tmp         = empty
    tmp_before  = empty
    e_parameter = ["-t","-k","--template","--key", "-s", "--skip"]
     
    for f in range(1,len(call)):                  # getting the parameters of function call
        tmp = call[f]
        if tmp_before in e_parameter:
            tmp = '"' + tmp + '"'
        arguments = arguments + tmp + blank
        tmp_before = tmp

    if verbose:
        print("- Info: Program call:", programname, arguments)
        
    if verbose:                                   # header for terminal output
        print("\n- Info: program call (with details): CTANOut.py")
        if ("-mt" in call) or ("--make_topics" in call):    print("  {0:5} {1:60}".format("-mt", "(" + (topics_text + ")")[0:50] + ellipsis))
        if ("-stat" in call) or ("--statistics" in call):   print("  {0:5} {1:60}".format("-stat", "(" + statistics_text + ")"))
        if ("-v" in call) or ("--verbose" in call):         print("  {0:5} {1:60}".format("-v", "(" + verbose_text + ")"))
        if ("-d" in call) or ("--directory" in call):       print("  {0:5} {2:60} {1}".format("-d", direc, "(" + direc_text + ")"))
        if ("-m" in call) or ("--mode" in call):            print("  {0:5} {2:60} {1}".format("-m", mode, "(" + mode_text + ")"))
        if ("-o" in call) or ("--output" in call):          print("  {0:5} {2:60} {1}".format("-o", args.out_file, "(" + out_text + ")"))
        if ("-b" in call) or ("--btype" in call):           print("  {0:5} {2:60} {1}".format("-b", btype, "(" + (btype_text + ")")[0:50] + ellipsis))
        if ("-s" in call) or ("--skip" in call):            print("  {0:5} {2:60} {1}".format("-s", skip, "(" + skip_text + ")"))
        if ("-sb" in call) or ("--skip_biblatex" in call):  print("  {0:5} {2:60} {1}".format("-sb", skip_biblatex, "(" + skip_biblatex_text + ")"))
        if ("-k" in call) or ("--key" in call):             print("  {0:5} {2:60} {1}".format("-k", fold(filter_key), "(" + key_text + ")"))
        if ("-A" in call) or ("--author_template" in call): print("  {0:5} {2:60} {1}".format("-A", fold(author_template), "(" + author_template_text + ")"))
        if ("-t" in call) or ("--template" in call):        print("  {0:5} {2:60} {1}".format("-t", fold(name_template), "(" + template_text + ")"))
        if ("-L" in call) or ("--license_template" in call):print("  {0:5} {2:60} {1}".format("-L", fold(license_template), "(" + license_template_text + ")"))
        print("\n")

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("% File                        : {0}\n".format(out_file))
        out.write("% Encoding                    : {0}\n".format(file_encoding))
        out.write("% Date                        : {0}\n".format(actDate))
        out.write("% Time                        : {0}\n\n".format(actTime))
        
        out.write("% generated by                : {0}\n".format(programname))
        out.write("% Program author              : {0}\n".format(programauthor))
        out.write("% Program version             : {0}\n".format(programversion))
        out.write("% Program date                : {0}\n\n".format(programdate))
        
        out.write("% Program call                : {0} {1}\n".format(programname, arguments))
        out.write("% mode                        : {0}\n".format(mode))
        out.write("% skipped CTAN fields         : {0}\n".format(skip))
        if name_template != empty:
            out.write("% filtered by name template   : '{0}'\n".format(comment_fold(name_template)))
        if filter_key != empty:
            out.write("% filtered by key template    : '{0}'\n".format(comment_fold(filter_key)))
        if author_template != empty:
            out.write("% filtered by author template : '{0}'\n".format(comment_fold(author_template)))
        if license_template != empty:
            out.write("% filtered by license template: '{0}'\n".format(comment_fold(license_template)))
        out.write("\n% --------------------------")
        out.write("\n% to be compiled by LuaLaTeX")
        out.write("\n% --------------------------\n")
        out.write("\n\\documentclass[{0}\n]{{scrartcl}}\n".format(classoptions))
        out.write(usepkg)
        out.write(title)
        out.write(header)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        out.write("% File                        : {0}\n".format(out_file))
        out.write("% Encoding                    : {0}\n".format(file_encoding))
        out.write("% Date                        : {0}\n".format(actDate))
        out.write("% Time                        : {0}\n\n".format(actTime))
        
        out.write("% generated by                : {0}\n".format(programname))
        out.write("% Program author              : {0}\n".format(programauthor))
        out.write("% Program version             : {0}\n".format(programversion))
        out.write("% Program date                : {0}\n\n".format(programdate))
        
        out.write("% Program Call                : {0} {1}\n".format(programname, arguments))
        out.write("% Mode                        : {0}\n".format(mode))
        out.write("% skipped CTAN fields         : {0}\n".format(skip))
        out.write("% skipped BibLaTeX fields     : {0}\n".format(skip_biblatex))
        out.write("% Type of BibLaTeX entries    : {0}\n".format(btype))
        if name_template != empty:
            out.write("% filtered by name template   : '{0}'\n".format(comment_fold(name_template)))
        if filter_key != empty:
            out.write("% filtered by key template    : '{0}'\n".format(comment_fold(filter_key)))
        if author_template != empty:
            out.write("% filtered by author template : '{0}'\n".format(comment_fold(author_template)))
        if license_template != empty:
            out.write("% filtered by license template: '{0}'\n".format(comment_fold(license_template)))
        out.write("\n% actual mapping CTAN --> BibLaTeX fields\n")
        out.write("% alias         --> embedded in 'note'\n")
        out.write("% also          --> 'related'\n")
        out.write("% authorref     --> collected in 'author'\n")
        out.write("% caption       --> 'subtitle'\n")
        out.write("% contact       --> collected in 'userd'\n")
        out.write("% copyright     --> 'usera'; 'year' (if applicable)\n")
        out.write("% ctan          --> 'userc'\n")
        out.write("% description   --> 'abstract'; collected in 'language' (if appliocable)\n")
        out.write("% documentation --> embedded in 'note'; local download in 'file' (if applicable); collected in 'language' (if appliocable)\n")
        out.write("% home          --> 'usere'\n")
        out.write("% install       --> 'userf'\n")
        out.write("% keyval        --> collected in 'keywords'\n")
        out.write("% license       --> 'userb'\n")
        out.write("% miktex        --> embedded in 'note'\n")
        out.write("% name          --> 'title'\n")
        out.write("% texlive       --> embedded in 'note'\n")
        out.write("% version       --> 'version'; 'year' (if applicable)\n\n")
        out.write("% a) If available, the program outputs the following BibLaTex fields:\n")
        out.write("%    abstract,author,date,file,keywords,language,note,related,subtitle,title,url,\n")
        out.write("%    urldate,usera,userb,userc,userd,usere,userf,version,year\n")
        out.write("% b) The BibLaTeX field 'note' is used for collecting the following CTAN items:\n")
        out.write("%    alias, contact, documentation, home, install, license, miktex, texlive\n")
        out.write("% c) The program uses the optional BibLaTeX fields usera, userb, userc, userd, usere, userf\n")
        out.write("\n% -----------------------")
        out.write("\n% to be compiled by biber")
        out.write("\n% -----------------------\n")
    elif mode in ["plain"]:                       # plain
        out.write(documenttitle.center(80) + "\n" + (documentsubtitle + programname).center(80) + "\n\n")
        out.write(documentauthor_txt.center(80) + "\n\n")
        
        out.write("% File                        : {0}\n".format(out_file))
        out.write("% Encoding                    : {0}\n".format(file_encoding))
        out.write("% Date                        : {0}\n".format(actDate))
        out.write("% Time                        : {0}\n\n".format(actTime))

        out.write("% generated by                : {0}\n".format(programname))
        out.write("% Program author              : {0}\n".format(programauthor))
        out.write("% Program version             : {0}\n".format(programversion))
        out.write("% Program date                : {0}\n\n".format(programdate))
        out.write("% Program call                : {0} {1}\n".format(programname, arguments))
        out.write("% Mode                        : {0}\n".format(mode))
        out.write("% skipped CTAN fields         : {0}\n".format(skip))
        if name_template != empty:
            out.write("% filtered by name template   : '{0}'\n".format(comment_fold(name_template)))
        if filter_key != empty:
            out.write("% filtered by key template    : '{0}'\n".format(comment_fold(filter_key)))
        if author_template != empty:
            out.write("% filtered by author template : '{0}'\n".format(comment_fold(author_template)))
        if license_template != empty:
            out.write("% filtered by license template: '{0}'\n".format(comment_fold(license_template)))
    elif mode in ["RIS"]:                         # RIS
        pass                                      #   for RIS do nothing
    elif mode in ["Excel"]:                       # Excel: write head of table
        out.write(s_id_text)
        for f in [s_author_text, s_name_text, s_caption_text, s_year_text, s_lastchanges_text, s_language_text,
                  s_lastaccess_text, s_version_text, s_keyval_text, s_alias_text, s_also_text, s_contact_text,
                  s_copyright_text, s_ctan_text, s_documentation_text, s_home_text, s_install_text, s_license_text,
                  s_miktex_text, s_texlive_text]:
            out.write("\t" + f)
        out.write("\n")

# ------------------------------------------------------------------
def get_author_packages():                        # Function get_author_packages: Gets package names by specified author name template
    """Gets package names by specified author name template.

    Returns a set (authors and associated packages)."""
    
    author_pack = set()                           # initialize set
    tmp_set     = set()                           # initialize auxiliary set
    
    for f in authors:                             # loop over authors
        (gn, fn) = authors[f]
        if fn != empty:                           # get familyname
            tmp_a = authors[f][1]
        else:
            tmp_a = authors[f][0]                 # if an incorrect entry is in authorsset
        if p5.match(tmp_a):                       # member matches template
            tmp_set.add(f)                        # built-up a new auxiliary set
            
    for f in tmp_set:                             # loop over auxiliary set
        if f in authorpackages:                   # prevent a wrong entry                         
            for g in authorpackages[f]:
                author_pack.add(g)                # built-up the resulting set
    if len(author_pack) == 0:
        if verbose:
            print("----- Warning: no package found which matches the specified {0} template '{1}'".format("author", author_template))
    return author_pack

# ------------------------------------------------------------------
def get_name_packages():                          # Function get_name_packages: Gets package names by specified package name template.
    """Gets package names by specified package name template.

    Reurns a set."""
    
    name_pack = set()                             # initialize set
    
    for f in packages:                            # loop over packages
        if p2.match(f):                           # member matches template
            name_pack.add(f)                      # built-up the resulting set
    if len(name_pack) == 0:
        if verbose:
            print("----- Warning: no package found which matches the specified {0} template '{1}'".format("name", name_template))
    return name_pack

# ------------------------------------------------------------------
def get_topic_packages():                         # Function get_topic_packages: Gets package names by specified topic template.
    """Gets package names by specified topic template.

    Returns a set (used topics and related packages)."""
    
    topic_pack = set()                            # initialize set
    
    for f in topicspackage:                       # loop over topicspackage
        if p3.match(f):                           # member matches template
            for g in topicspackage[f]:            # all packagexs for this entry
                topic_pack.add(g)                 # built-up the resulting set
    if len(topic_pack) == 0:
        if verbose:
            print("----- Warning: no package found which matches the specified {0} template '{1}'".format("topic", filter_key))
    return topic_pack

# ------------------------------------------------------------------
def get_license_packages():                       # Function get_license_packages: Gets package names by specified license template.
    """Gets package names by specified license template.

    Returns a set (used licenses and related packages)."""
    
    license_pack = set()                          # initialize set
    
    for lic in licensepackages:                   # loop over licensepackages
        lic2 = licenses[lic][0]
        lic3 = licenses[lic][1]
        if lic3 == "true":
            lic3 = "free"
        else:
            lic3 = "not free"
        if p9.match(lic2) or p9.match(lic) or p9.match(lic3):  # collect packages with specified licenses
            for g in licensepackages[lic]:
                license_pack.add(g)
    if len(license_pack) == 0:
        if verbose:
            print("----- Warning: no package found which matches the specified {0} template '{1}'".format("license", license_template))
    return license_pack

# ------------------------------------------------------------------
def home(k):                                      # function: processes element <home .../>
    """Processes the home element.

    k: current knot

    Fetches the local attribute href."""

    # home --> bibfield_test
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global s_home                                 # string for Excel: home

    href = k.get("href", empty)                   # get attribute href

    if mode in ["LaTeX"]:                         # LaTeX 
        out.write("\\item[home page] \\url{{{0}}}\n".format(href))
    elif mode in ["RIS"]:                         # RIS"usere
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Home page: " + href
        else:
            notice = "Home page: " + href
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if bibfield_test(href, "usere"):
            out.write("usere".ljust(fieldwidth) + "= {" + href + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "home page: ".ljust(labelwidth) + href)
    elif mode in ["Excel"]:                       # Excel
        s_home = href

# ------------------------------------------------------------------
def install(k):                                   # function: processes element <install .../>
    """Processes the install element.

    k: current knot

    Fetches the local attribute path."""

    # install --> bibfield_test
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global s_install                              # string for Excel: install

    xpath = k.get("path", empty)                  # get attribute path

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[installation] \\url{{{0}}}\n".format(ctanUrl3 + xpath))
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Installation: " + ctanUrl3 + xpath
        else:
            notice = "Installation: " + ctanUrl3 + xpath
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        
        if bibfield_test(ctanUrl3 + xpath, "userf"):
            out.write("userf".ljust(fieldwidth) + "= {" + ctanUrl3 + xpath + "},\n")
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "installation: ".ljust(labelwidth) + ctanUrl3 + xpath)
    elif mode in ["Excel"]:                       # Excel
        s_install = ctanUrl3 + xpath

# ------------------------------------------------------------------
def keyval(k):                                    # function: processes element <keyval .../>
    """Processes the keyval elements.

    k: current knot

    fetches the local attributes key, value."""

    # keyval --> TeXchars
    
    global s_keyval                               # string for Excel: keyval
    global usedTopics                             # dictionary for collecting topics

    key   = k.get("key", empty)                   # get attribute key
    value = k.get("value", empty)                 # get attribute value

    tmp   = topics[value]
    if not value in usedTopics:                   # collects topics in usedTopics
        usedTopics[value] = 1
    else:
        usedTopics[value] = usedTopics[value] + 1

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)
        out.write("\\item[keyword] \\texttt{{{0}}} ({1})\n".format(value, tmp))
        out.write("\\index{{Topic!{0}}}\n".format(value))
    elif mode in ["RIS"]:                         # RIS
        out.write("KW  - {0}\n".format(value))
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "keyword: ".ljust(labelwidth) + value + " (" + topics[value] + ")")
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        pass                                      #   for BibLaTeX do nothing
    elif mode in ["Excel"]:                       # Excel
        pass

# ------------------------------------------------------------------
def leading(k, p, t):                                         # function: first lines for package output
    """Analyzes the first lines of each XML package file and print out some lines.

    k: current knot (here entry)
    p: current package
    t: date of package

    Fetches the local attribute id.
    Inspects the elements caption, authorref."""

    # leading --> TeXchars
    # leading --> get_year
    # leading --> get_authoryear
    # leading --> bibfield_test
    
    global authorexists                                       # flag
    global s_lastaccess                                       # string for Excel: Last access
    global s_author                                           # string for Excel: authorref

    xname = k.get("id", empty)                                # get attribute id
    xpath = ctanUrl4 + p

    allauthors  = []                                          # initialize some variables
    year        = empty
    authorexists= False
    date        = empty
    year        = empty
    xcaption    = empty
    
    usedPackages.append(xname)                                # collect used packages 

    for child in k:                                           # find some supp. infos
        if child.tag == "caption":
            xcaption  = child.text                            # embedded text xcaption
            xcaption2 = xcaption
            if len(xcaption2) >= maxcaptionlength:
                xcaption2 = xcaption2[0 : maxcaptionlength] + "xyz"
            xcaption2 = TeXchars(xcaption2)
            xcaption2 = re.sub("#", "\\#", xcaption2)
            
        if child.tag == "authorref":                          # author(s) for mode=="BibLaTeX"
            onefamilyname = child.get("familyname", empty)    #   get attribute familyname
            onegivenname  = child.get("givenname", empty)     #   get attribute givenname
            active        = child.get("active", "true")       #   get attribute active
            oneauthor     = (onefamilyname, onegivenname)     #   new variable
            xid           = child.get("id", empty)            #   get attribute id
            
            if (xid != empty) and (xid in authors):
                onegivenname, onefamilyname = authors[xid]
                oneauthor = (onefamilyname, onegivenname)
            else:
                onegivenname, onefamilyname = empty, authorunknown
                oneauthor = (onefamilyname, onegivenname)
                
            if active:
                allauthors.append(oneauthor)
                
    if mode in ["BibLaTeX", "Excel"]:                         # BibLaTeX
        allauthors2 = []                                      #    generate author string for the current package
        for f in allauthors:
            f = list(f)
            
            if (blank in f[0]) and (mode in ["BibLaTeX"]):
                f[0] = "{" + f[0] + "}"
            if (blank in f[1]) and (mode in ["BibLaTeX"]):
                f[1] = "{" + f[1] + "}"
                
            if (f[0] != empty) and (f[1] != empty):
                 oneauthor = f[0] + ", " + f[1]
            elif (f[0] != empty) and (f[1] == empty):
                oneauthor = f[0]
            else:
                oneauthor = f[1]

            allauthors2.append(oneauthor)
            
        if len(allauthors2) > 0:
            author_string = allauthors2[0]
        else:
            author_string = authorunknown

        if mode in ["Excel"]:
            for f in range(1, len(allauthors2)):
                author_string = author_string + "; " + allauthors2[f]
        else:
            for f in range(1, len(allauthors2)):
                author_string = author_string + " and " + allauthors2[f]

    if mode in ["LaTeX"]:                                     # LaTeX
        xcaption  = TeXchars(xcaption)
        xcaption  = re.sub("#", "\\#", xcaption)
        xcaption2 = xcaption2.replace("xyz", "\\ldots")
        xname1    = TeXchars(xname)
        xname2    = re.sub("_", "-", xname)
        out.write("\n%" + 80*"-")
        tmp = r"\texttt{" + xname1 + "} -- "
        out.write("\n\\section[{0}{1}]{{{2}{3}}}\\label{{pkg:{4}}}\n".format(tmp, xcaption2, tmp, xcaption, xname2))
        out.write("\\index{{Package!{0}}}\n\n".format(xname1))
        out.write("\\begin{labeling}{Web page on CTAN}\n")
        out.write("\\item[Web page on CTAN] \\url{" + xpath + "}\n")
    elif mode in ["RIS"]:                                     # RIS
        out.write("TY  - ICOMM" + "\n")                       #   header with type
        out.write("UR  - {0}\n".format(xpath))                #   main URL
        out.write("Y3  - {0}\n".format(t))                    #   date of last access
    elif mode in ["plain"]:                                   # plain
        tmp = xname + " -- " + xcaption
        out.write("\n\n\n" + tmp)
        out.write("\n" + len(tmp) * "-")
        out.write("\n" + "Web page on CTAN: ".ljust(labelwidth) + xpath)
    elif mode in ["BibLaTeX"]:                                # BibLaTeX
        tmp7 = empty.join(citation_keys[p])                   #   find citation key
        out.write("\n{0}{{{1},\n".format(btype, tmp7))        #   1st line of citation
        
        if bibfield_test(author_string, "author"):
            out.write("author".ljust(fieldwidth) + "= {" + author_string + "},\n") # author(s)
            
        if bibfield_test(xpath, "url"):
            out.write("url".ljust(fieldwidth) + "= {" + xpath + "},\n")            # URL of web page
            
        if bibfield_test(t, "urldate"):
            out.write("urldate".ljust(fieldwidth) + "= {" + t + "},\n")            # date of last access
    elif mode in ["Excel"]:                                   # Excel
        s_author     = author_string                          #
        s_lastaccess = t                                      #
    authorexists = False

# ------------------------------------------------------------------
def licenseT(k):                                  # function: processes element <license .../>
    """Processes the license elements.

    k: current knot

    Fetches the embedded attibutes type, date."""
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global license_str                            # string: collect license
    global s_license                              # string for Excel: license
    global usedLicenses

    typeT     = k.get("type", empty)              # get attribute type; get a language key
    tmp       = typeT
    tmpname   = licenses[tmp][0]                  # name of license
    tmpstatus = licenses[tmp][1]                  # status of license: free/not free
    if tmpstatus == "true":
        tmpstatus = "(free)"
    elif tmpstatus =="false":
        tmpstatus = "(not free)"
    else:
        pass

    if tmp in licenses:                           # look in dictionary
        tmp2   = "{0} = {1} {2}".format(tmp, tmpname, tmpstatus)

    if not typeT in usedLicenses:                 # collects licenses in usedLicenses
        usedLicenses[typeT] = 1
    else:
        usedLicenses[typeT] = usedLicenses[typeT] + 1
    
    if license_str != empty:                      # for BibLaTeX
        license_str += "; " + tmp + blank + tmpstatus
    else:
        license_str = tmp + blank + tmpstatus

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[license] {0}\n".format(tmp2))
        out.write("\\index{{License!{0}}}\n".format(tmp))
        out.write("\\index{{License!{0}}}\n".format(tmpname))
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "License: " + tmp2
        else:
            notice = "License: " + tmp2
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        pass
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "license: ".ljust(labelwidth) + tmp2)
    elif mode in ["Excel"]:                       # Excel
        if s_license != empty:
            s_license += "; " + tmp2
        else:
            s_license = tmp2

# ------------------------------------------------------------------
def load_pickle1():                               # Function load_pickle1: loads/unpacks pickle file 1
    """Gets the structures authors, packages, topics, topicspackage, authorpackages, licensepackages (generated by CTANLoad.py)"""

    global authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licensepackages
    
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
    # licensepackages: Python dictionary (mostly sorted)
    #   each element: [license key] <list with package names>

    try:                                          # try to open 1st pickle file 
        pickleFile1 = open(direc + pickle_name1, "br")
        (authors, packages, topics, licenses, topicspackage, packagetopics, authorpackages, licensepackages) = pickle.load(pickleFile1)
        pickleFile1.close()                       #   close file
    except FileNotFoundError:                     # unable to open pickle file
        print("--- Error: pickle file '{0}' not found".format(pickle_name1))
        sys.exit("- Error: program is terminated")

# ------------------------------------------------------------------
def load_pickle2():                               # Function load_pickle2: loads/unpacks pickle file 2
    """gets XML_toc (generated by CTANLoad.py)"""

    global XML_toc                                # python dictionary:  list of XML and PDF files: XML_toc[CTAN address]=(XML file, key, plain PDF file name)
    
    try:                                          # try to open second pickle file
        pickleFile2 = open(direc + pickle_name2, "br")
        XML_toc     = pickle.load(pickleFile2)
        pickleFile2.close()                       #   close file
    except FileNotFoundError:                     # unable to open pickle file
        list_info_files = False
        print("--- Warning: pickle file '{0}' not found; local information files ignored".format(pickle_name2))

# ------------------------------------------------------------------
def main():                                       # function: Main function (calls the other functions)
    """Main function (calls the other functions)"""

    # main --> biblatex_citationkey
    # main --> load_pickle1
    # main --> load_pickle2
    # main --> first_lines
    # main --> process_packages
    # main --> make_tops
    # main --> make_xref
    # main --> make_lic
    # main --> make_tlp
    # main --> make_tap
    # main --> make_stat
    # main --> make_statistics

    starttotal   = time.time()                    # set begin of total time
    startprocess = time.process_time()            # set begin of process time

    load_pickle1()                                # load pickle file 1
    load_pickle2()                                # load pickle file 21
    if mode == "BibLaTeX":
        biblatex_citationkey()                    # generate BibLaTeX citation keys
    
    first_lines()                                 # first lines of output
    process_packages()                            # process all packages

    # ------------------------------------------------------------------
    # Generate topic list, topics and their packages (cross-reference), finish
    #
    if mode in ["LaTeX"] and make_topics: 
        if not no_package_processed:
            make_tops()                           # Topic list
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".top"))
            
        if not no_package_processed:
            make_xref()                           # Topics/Packages cross-reference
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".xref"))
            
        if not no_package_processed:
            make_tap()                            # Authors/Packages cross-reference
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".tap"))

        if not no_package_processed:
            make_lics()                            # License list cross-reference
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".lic"))
            
        if not no_package_processed:
            make_tlp()                            # Licenses/Packages cross-reference
        else:
            if verbose:
                print("--- Warning: no file '{0}' created".format(direc + args.out_file + ".tlp"))
        make_stat()                               # Statistics file (xyz.stat)

    # ------------------------------------------------------------------
    # The end
    #
    if mode in ["LaTeX"]:                         # LaTeX
        out.write(trailer)                        # output trailer
        out.close()                               # close output file
    if verbose:
        print("- Info: CTANOut program successfully completed")

    # ------------------------------------------------------------------
    # Statistics on terminal
    #
    if statistics:                                # flag -stat is set
        make_statistics()                         # output statistics on terminal
        
        endtotal   = time.time()
        endprocess = time.process_time()
        print("--")
        print("total time: ".ljust(left + 2), round(endtotal-starttotal, 2))
        print("process time: ".ljust(left + 2), round(endprocess-startprocess, 2))

# ------------------------------------------------------------------
def make_stat():                                  # function: generates statistics in the stat file (xyz.stat)
    """generates statistics in the stat file (xyz.stat)."""
    
    # write statistics in the stat (.stat) file

    text1 = empty
    text2 = empty
    text3 = empty
    text4 = empty
    text5 = empty
    
    stat = open(direc + args.out_file + ".stat", encoding=file_encoding, mode="w")
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
    stat.write("skipped CTAN fields "            + r"& \verb§" + skip + r"§  " + text3 + r"\\" + "\n\n")
    
    if name_template == name_default:
        text1 = "(all packages = default)"
##    print("***call_output", call_output)            
    stat.write("template for package names "     + r"& " + TeX_fold(name_template) + blank + text1 + r"\\" + "\n")
    
    if filter_key == filter_key_default:
        text2 = "(all topics = default)"
    stat.write("template for topics "            + r"& " + TeX_fold(filter_key) + r"  " + text2 + r"\\" + "\n")

    if author_template == author_template_default:
        text4 = "(all authors = default)"
    stat.write("template for author names "     + r"& " + TeX_fold(author_template) + r"  " + text4 + r"\\" + "\n")

    if license_template == license_template_default:
        text5 = "(all licenses = default)"
    stat.write("template for licenses "     + r"& " + TeX_fold(license_template) + r"  " + text5 + r"\\\\" + "\n\n")

    stat.write("number of authors, total on CTAN "    + r"&" + str(len(authors)).rjust(6) + r"\\" + "\n")
    stat.write("number of authors, cited here "       + r"&" + str(len(usedAuthors)).rjust(6)  + r"\\" + "\n")
    stat.write("number of packages, total on CTAN "   + r"&" + str(len(packages)).rjust(6)  + r"\\" + "\n")
    stat.write("number of packages, described here "  + r"&" + str(len(usedPackages)).rjust(6)  + r"\\" + "\n")

    stat.write("number of topics, total on CTAN "   + r"&" + str(len(topics)).rjust(6)  + r"\\" + "\n")
    stat.write("number of topics, used here "       + r"&" + str(len(usedTopics)).rjust(6)  + r"\\" + "\n")
    
    stat.write("number of licenses, total on CTAN "   + r"&" + str(len(licenses)).rjust(6)  + r"\\" + "\n")
    stat.write("number of licenses, used here "       + r"&" + str(len(usedLicenses)).rjust(6)  + r"\\" + "\n")
    stat.write(r"\end{tabular}" + "\n")
    stat.write(	"\\footnotetext{special lists: topics/licinses and their explanation + topics/authors/licenses and related packages(cross-reference lists)}\n")
    stat.close()                                  # close statistics file 
    if verbose:
        print("--- Info: file '{0}' written: [statistics]".format(direc + args.out_file + ".stat"))

# ------------------------------------------------------------------
def make_statistics():                            # function: Generates statistics on terminal.
    """Generates statistics on terminal."""

    l = left + 1
    r = 5
    
    # Statistics on terminal
    print("\nStatistics:")
    print("date/time:".ljust(l + 1), actDate, actTime)
    print("target format:".ljust(l + 1), mode)
    print("output file:".ljust(l + 1), direc + out_file, "\n")
    print("number of authors, total on CTAN:".ljust(l),  str(len(authors)).rjust(r))
    print("number of authors, cited here:".ljust(l),   str(len(usedAuthors)).rjust(r))
    print("number of packages, total on CTAN:".ljust(l), str(len(packages)).rjust(r))
    print("number of packages, collected here:".ljust(l),  str(len(usedPackages)).rjust(r))
    print("number of topics, total on CTAN:".ljust(l),   str(len(topics)).rjust(r))
    print("number of topics, used here:".ljust(l),    str(len(usedTopics)).rjust(r))
    print("number of licenses, total on CTAN:".ljust(l),   str(len(licenses)).rjust(r))
    print("number of licenses, used here:".ljust(l),    str(len(usedLicenses)).rjust(r))

# ------------------------------------------------------------------
def make_tap():                                   # function: Generates the tap (xyz.tap) file.
    """Generates the tap (xyz.tap) file."""
    
    # Authors/Packages cross-reference
        
    tap = open(direc + args.out_file + ".tap", encoding=file_encoding, mode="w")
    tap.write("% file: '{0}.tap'\n".format(args.out_file))
    tap.write("% date: {0}\n".format(actDate))
    tap.write("% time: {0}\n".format(actTime))
    tap.write("% is called by '{0}.tex'\n\n".format(args.out_file))
    tap.write(r"\section{Authors and associated packages}" + "\n\n")
    tap.write("\\textit{Note: The numbers do not refer to page numbers, but to section numbers. A click on this number leads to the corresponding package description.}\n\n")
    tap.write(r"\raggedright" + "\n")
    tap.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")

    tap.write("\n")
    for f in authors:                             # all authors
        if f in usedAuthors:                      #  all used authors
            if authors[f][1] != empty:
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
def make_tlp():                                   # function: Generates the tlp (xyz.tlp) file
    """Generates the tlp (xyz.tlp) file."""
    
    # Authors/Packages cross-reference
        
    tlp = open(direc + args.out_file + ".tlp", encoding=file_encoding, mode="w")
    tlp.write("% file: '{0}.tlp'\n".format(args.out_file))
    tlp.write("% date: {0}\n".format(actDate))
    tlp.write("% time: {0}\n".format(actTime))
    tlp.write("% is called by '{0}.tex'\n\n".format(args.out_file))
    tlp.write(r"\section{Licenses and associated packages}" + "\n\n")
    tlp.write("\\textit{Note: The numbers do not refer to page numbers, but to section numbers. A click on this number leads to the corresponding package description.}\n\n")
    tlp.write(r"\raggedright" + "\n")

    tlp.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")
    for f in licenses:                            # loop: all topics
        if f in usedLicenses:                     # topic is used?
            tlp.write("\\item[\\texttt{" + f + "}] \\index{{License!" + f + "}}")
            tmp1 = licensepackages[f]             # get the packages for this topic
            package_no = 0	
			
            for ff in tmp1:
                if ff in usedPackages:
                    package_no += 1
            if package_no == 1:
                text1 = " package: "
            else:
                text1 = " packages: "
            tlp.write(str(package_no) + text1)

            for ff in tmp1:                       # loop: all packages with this license name
                if ff in usedPackages:
                    ff = re.sub("_", "-", ff)
                    tlp.write("\\texttt{{{0}}}~(\\ref{{pkg:{1}}}); ".format(ff, ff))
            tlp.write("\n")
    tlp.write(r"\end{labeling}" + "\n")
    
    tlp.close()                                   # close file
    if verbose:
        print("--- Info: file '{0}.tlp' created: [list with licenses and related packages (cross-reference list)]".format(direc + args.out_file))

# ------------------------------------------------------------------
def make_tops():                                  # function: Generates the tops (xyz.top) file.
    """Generates the tops (xyz.top) file."""
    
    # Topic list
    tops = open(direc + args.out_file + ".top", encoding=file_encoding, mode="w")
    
    tops.write("% file: {0}.top\n".format(args.out_file))
    tops.write("% date: {0}\n".format(actDate))
    tops.write("% time: {0}\n".format(actTime))
    tops.write("% is called by {0}.tex\n\n".format(args.out_file))
    
    tops.write(r"\section{Used topics, short explainations}" + "\n\n")
    tops.write(r"\raggedright" + "\n")
    tops.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")
  
    for f in topics:                              # all topics
        if f in usedTopics:                       #  all used topics
            tmp = topics[f]
            tmp = re.sub(r"\\", r"\\textbackslash ", tmp)
            tops.write("\\item[\\texttt{{{0}}}] {1}".format(f, tmp))
            tops.write("\\index{{Topic!{0}}}\n".format(f))
    tops.write(r"\end{labeling}" + "\n")
    tops.close()                                  # close file
    if verbose:
        print("--- Info: file '{0}.top' created: [topics and their explainations]".format(direc + args.out_file))

# ------------------------------------------------------------------
def make_lics():                                  # function: Generates the lics (xyz.lic) file.
    """Generates the tops (xyz.lic) file."""
    
    # License list
    lics = open(direc + args.out_file + ".lic", encoding=file_encoding, mode="w")
    
    lics.write("% file: {0}.lic\n".format(args.out_file))
    lics.write("% date: {0}\n".format(actDate))
    lics.write("% time: {0}\n".format(actTime))
    lics.write("% is called by {0}.tex\n\n".format(args.out_file))
    
    lics.write(r"\section{Used licenses, short explainations}" + "\n\n")
##    lics.write("\\textit{Note: The numbers do not refer to page numbers, but to section numbers. A click on this number leads to the corresponding package description.}\n\n")
    lics.write(r"\raggedright" + "\n")
    lics.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")
  
    for f in licenses:                              # all topics
        if f in usedLicenses:                       #  all used topics
            tmp  = licenses[f][0]
            tmp2 = licenses[f][1]
            if tmp2 == "true":
                tmp3 = "free"
            else:
                tmp3 = "not free"
##            tmp = re.sub(r"\\", r"\\textbackslash ", tmp)
            lics.write("\\item[\\texttt{{{0}}}] {1} ({2})".format(f, tmp, tmp3))
            lics.write("\\index{{License!{0}}}\n".format(f))
    lics.write(r"\end{labeling}" + "\n")
    lics.close()                                  # close file
    if verbose:
        print("--- Info: file '{0}.lic' created: [licenses and their explainations]".format(direc + args.out_file))

# ------------------------------------------------------------------
def make_xref():                                  # function: Generates the xref (xyz.xref) file.
    """Generates the xref (xyz.xref) file."""
    
    # Topics/Packages cross-reference
    xref = open(direc + args.out_file + ".xref", encoding=file_encoding, mode="w")
    
    xref.write("% file: {0}.xref\n".format(args.out_file))
    xref.write("% date: {0}\n".format(actDate))
    xref.write("% time: {0}\n".format(actTime))
    xref.write("% is called by '{0}.tex'\n\n".format(args.out_file))
    xref.write(r"\section{Used topics and related packages}" + "\n\n")
    xref.write("\\textit{Note: The numbers do not refer to page numbers, but to section numbers. A click on this number leads to the corresponding package description.}\n\n")
    xref.write(r"\raggedright" + "\n")
    xref.write(r"\begin{labeling}{xxxxxxxxxxxxxxxxxxxxxx}" + "\n")
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
def miktex(k):                                    # function: processes element <miktex .../>
    """Processes the miktex element.

    k: current knot

    Fetches the local attribute location."""

    # miktex --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global s_miktex                               # string for Excel: miktex

    location = k.get("location", empty)           # get attribute location

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(location)
        out.write("\\item[on Mik\TeX] \\texttt{{{0}}}\n".format(tmp))
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "on MikTeX: " + location
        else:
            notice = "on MikTeX: " + location
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp    = TeXchars(location)
        if notice != empty:
            notice += ";\n" + blank * (fieldwidth + 2) + "on MikTeX: " + tmp
        else:
            notice = "on MikTeX: " + tmp
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "on MikTeX: ".ljust(labelwidth) + location)
    elif mode in ["Excel"]:                       # Excel
        s_miktex = location

# ------------------------------------------------------------------
def name(k):                                      # function: processes element <name>...</name>
    """Processes the name element.

    k: current knot

    Fetches embedded text."""

    # name --> TeXchars
    # name --> bibfield_test
    
    global s_name                                 # string for Excel: name

    if len(k.text) > 0:                           # get embedded text
        tmp = k.text                              
    else:                                         #   k.text is empty
        tmp = default_text                        #   default text

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(tmp)                       #   clean-up embedded text
        out.write("\\item[name] \\texttt{{{0}}}\n".format(tmp))
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "name: ".ljust(labelwidth) + tmp)
    elif mode in ["RIS"]:                         # RIS
        out.write("T1  - {0}\n".format(tmp))      #   main title
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = TeXchars(tmp)                       #   clean-up embedded text
        if bibfield_test(tmp, "title"):
            out.write("title".ljust(fieldwidth) + "= {" + tmp + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_name = k.text                           #   embedded text

# ------------------------------------------------------------------
def onepackage(s, t):                             # function: loads a package XML file and start parsing
    """Loads a package XML file and start parsing.

    s: package name
    t: current package date"""

    # onepackage --> entry
    
    global counter                                # counter for packages

    left = 33

    try:
        onePackage     = ET.parse(direc + s + ext)# parse XML file
    except:                                       # not successfull
        if verbose:
            print("----- Warning: XML file for package '{0}' not well-formed".format(s))
        return
    if verbose:
        print("    " + str(counter).ljust(5), "package:", s.ljust(left), "mode:", mode.ljust(7), "file:", direc + out_file.ljust(15))

    counter        = counter + 1                  # increment counter
    onePackageRoot = onePackage.getroot()         # get XML root 
    entry(onePackageRoot, t, s)                   # begin with entry element

# ------------------------------------------------------------------
def process_packages():                           # function: Global loop (over alll selected packaged)
    """Global loop (over alll selected packages)"""

    global no_package_processed                   # if there is no correct XML file

    # process_packages --> onepackage
    # process_packages --> get_topic_packages
    # process_packages --> get_author_packages
    # process_packages --> get_name_packages
    # process_packages --> get_local_packages
    
    all_packages = set()                          # initialize set
    for f in packages:
        all_packages.add(f)                       # construct a set object (packages has not the right format)
        
    tmp_tp = all_packages.copy()                  # initialize tmp_tp
    tmp_ap = all_packages.copy()                  # initialize tmp_ap
    tmp_np = all_packages.copy()                  # initialize tmp_np
    tmp_lp = all_packages.copy()                  # initialize tmp_np

    if filter_key != filter_key_default:
        tmp_tp = get_topic_packages()             # get packages by topic
    if author_template != author_template_default:
        tmp_ap = get_author_packages()            # get packages by author name
    if name_template != name_template_default:
        tmp_np = get_name_packages()              # get packages by package name
    if license_template != license_template_default:
        tmp_lp = get_license_packages()           # get packages by package name

    tmp_pp = tmp_tp & tmp_ap & tmp_np & tmp_lp & get_local_packages(direc)
    tmp_p  = sorted(tmp_pp)                       # built an intersection 
                                                 
    for f in tmp_p:                               # all XML files in loop
        fext = f + ext                            # XML file name (with extension)
 
        try:                                      # try to open file
            ff       = open(direc + fext, encoding=file_encoding, mode="r")
            mod_time = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(fext)))
            onepackage(f, mod_time)               # process loaded XML file 
            ff.close()                            # loaded XML file closed
        except FileNotFoundError:                 # specified XML file not found
            if verbose:
                print("----- Warning: XML file for package '{0}' not found".format(f))

    if counter <= 1:                              # no specified package found <=== error1
        if verbose:
            print("----- Warning: no correct local XML file for any specified package found")
        no_package_processed = True

    if verbose:
        print("--- Info: packages processed")

# ------------------------------------------------------------------
def texlive(k):                                   # function: processes element <texlive .../>
    """Processes the texlive element.

    k: current knot

    Fetches the local attribute loacation."""

    # texlive --> TeXchars
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global s_texlive                              # string for Excel: texlive

    location = k.get("location", empty)           # get attribute location

    if mode in ["LaTeX"]:                         # LaTeX
        tmp = TeXchars(location)
        out.write("\\item[on \\TeX Live] \\texttt{{{0}}}\n".format(tmp))
    elif mode in ["RIS"]:                         # RIS
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "on TeXLive: " + location
        else:
            notice = "on TeXLive: " + location 
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        tmp = TeXchars(location)
        if notice != empty:
            notice += ";\n" + blank * (fieldwidth + 2) + "on TeXLive: " + tmp
        else:
            notice = "on TeXLive: " + tmp
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "on TeXLive: ".ljust(labelwidth) + location)
    elif mode in ["Excel"]:                       # Excel
        s_texlive = location

# ------------------------------------------------------------------
def trailing(k, t, p):                            # function: last lines for the actual package
    """Completes the actual package.

    k: current knot (here entry)
    t: current date
    p: current package

    Inspects the element keyval."""

    # trailing --> bibfield_test
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global info_files                             # list of local PDF files
    global language_set                           # set: collect language
    global year_str                               # string: collect all year items for a package
    global version_str                            # string: collect all version items for a package
    global date_str                               # string: collect date
    global also_str                               # string: collect also
    global license_str                            # string: collect license
    global copyright_str                          # string: collect copyright
    global description_str                        # string: collect description
    global authorexists                           # flag
    global contact_str                            # string: collect contact

    kw = []                                       # keywords
     
    language_set.discard(empty)         
    lang      = sorted(list(language_set))
    lang_str  = empty                                # construct lang_str; used for Excel
    lang_str2 = empty                                # used for RIS, BibLaTeX
    lang_str3 = empty                                # used for LaTeX, plain
    for f in lang:
        if lang_str != empty:
            lang_str = lang_str + "; " + f
        else:
            lang_str = f
        if lang_str2 != empty:
            lang_str2 = lang_str2 + "; " + languagecodes[f]
        else:
            lang_str2 = languagecodes[f]
        if lang_str3 != empty:
            lang_str3 = lang_str3 + "; " + "{0}={1}".format(f, languagecodes[f])
        else:
            lang_str3 = "{0}={1}".format(f, languagecodes[f])

    act_year = get_year(year_str)                 # calculate actual year (on the base of year_str and version_str)
    
    for child in k:                               # fetch and collect the package's keywords
        if child.tag == "keyval":                 #   element keyval
            value = child.get("value", empty)     #   get attribute value
            if kw == []:
                kw.append(value)
            else:
                kw.append("; " + value)
    kw2 = empty.join(kw)                          # collect all keywords in one string

    if str(act_year) == year_default:
        if mode in ["RIS", "BibLaTeX"]:
            act_year = empty
        else:
            act_year = year_default2

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[language(s)] {0}\n".format(lang_str3))
        if (str(act_year) != empty) and (date_str == empty):  #   year
            out.write("\\item[year] {0}\n".format(act_year))
            out.write("\\index{Year!" + str(act_year) + "}\n")
        out.write("\\item[last access] {0}\n".format(t))      #   date of last access
        out.write(r"\end{labeling}" + "\n")
    elif mode in ["RIS"]:                         # RIS
        if not authorexists:
            out.write("AU  - {0}\n".format(authorunknown))
        out.write("N1  - " + notice.strip() + "\n")       # 
        out.write("LA  - {0}\n".format(lang_str2))
        if (str(act_year) != empty) and (date_str == empty):
            out.write("PY  - {0}\n".format(act_year))
        out.write("ER  -\n\n")
    elif mode in ["plain"]:                       # plain
        if (str(act_year) != empty) and (date_str == empty):
            out.write("\n" + "year: ".ljust(labelwidth) + str(act_year))
        out.write("\n" + "language(s): ".ljust(labelwidth) + lang_str3)
        out.write("\n" + "last access: ".ljust(labelwidth) + t)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if bibfield_test(description_str, "abstract"):
            out.write(description_str)
            out.write("},\n")
            
        if bibfield_test(str(act_year), "year") and (date_str == empty):
            out.write("year".ljust(fieldwidth) + "= {" + str(act_year) + "},\n")
            
        if bibfield_test(lang_str2, "language"):
            out.write("language".ljust(fieldwidth) + "= {" + lang_str2 + "},\n")
            
        if bibfield_test(kw2, "keywords"):
            out.write("keywords".ljust(fieldwidth) + "= {" + kw2 + "},\n")
            
        if bibfield_test(copyright_str, "usera"): 
            copyright_str = re.sub("@", "'at'", copyright_str)
            out.write("usera".ljust(fieldwidth) + "= {" + copyright_str + "},\n")
            
        if bibfield_test(license_str, "userb"): 
            out.write("userb".ljust(fieldwidth) + "= {" + license_str + "},\n")
            
        if bibfield_test(contact_str, "userd"): 
            out.write("userd".ljust(fieldwidth) + "= {" + contact_str + "},\n")
            
        if bibfield_test(also_str, "related"):
            out.write("related".ljust(fieldwidth) + "= {" + also_str + "},\n")
            
        if bibfield_test(notice.strip(), "note"):
            notice = re.sub("@", "'at'", notice.strip())
            out.write("note".ljust(fieldwidth)     + "= {" + notice.strip() + "},\n")
            
        if len(info_files) > 0:
            tmp = empty
            for f in info_files:
                fx = os.path.abspath(f)
                fx = re.sub(r"\\", "/", fx)
                fx = re.sub(":", "\\:", fx)
                fx = ":" + fx + ":PDF"
                if tmp != empty:
                    tmp += "; " + fx
                else:
                    tmp = fx
            if bibfield_test(tmp, "file"):
                out.write("file".ljust(fieldwidth) + "= {" + tmp + "},\n")
        out.write("}\n")
    elif mode in ["Excel"]:                       # Excel
        s_language = lang_str
        s_keyval   = kw2
        s_year     = str(act_year)
        out.write(s_id)
        for f in [s_author, s_name, s_caption, s_year, s_lastchanges, s_language, s_lastaccess, s_version, s_keyval,
                  s_alias, s_also, s_contact, s_copyright, s_ctan, s_documentation, s_home, s_install, s_license,
                  s_miktex, s_texlive]:
            out.write("\t" + f)
        out.write("\n")

    notice          = empty                         # re-initialize notice
    info_files      = []                            # re-initialize info_files
    language_set    = {'en'}                        # re-initialize language_set
    year            = empty                         # re-initialize year
    authorexists    = False                         # re-initialize authorexists
    year_str        = year_default                  # re-initialize year_str
    date_str        = empty                         # re-initialize date_str
    also_str        = empty                         # re-initialize also_str
    version_str     = date_default                  # re-initialize version_str
    license_str     = empty                         # re-initialize license_str
    copyright_str   = empty                         # re-initialize copyright_str
    description_str = empty
    contact_str     = empty

# ------------------------------------------------------------------
def version(k, p):                                # function: processes <version .../> element 
    """Processes the version element.

    k: current knot
    p: current package

    Fetches the embedded attribues number, date."""

    # version --> bibfield_test
    
    global notice                                 # string for RIS/BibLaTeX: collection for N1 a/o note
    global date_str                               # string: collect date
    global version_str                            # string: collect all version items for a package
    global s_version                              # string for Excel: version
    global s_lastchanges                          # string for Excel: last changes
    global s_year                                 # string for Eccel: year

    number = k.get("number", empty)               # get attribute number
    date   = k.get("date", empty)                 # get attribute date
    tmp    = number

    if mode in ["LaTeX", "BibLaTeX"]:             # for LaTeX/BibLaTeX
        tmp    = re.sub("_", r"\\_", tmp)         #   correction

    if date != empty:
        tmp = tmp + " (" + date + ")"             # version with date

    version_str = version_str + "|" + date        # append date to version_str
    date_str    = date
    year        = str(get_year(date_str))

    if mode in ["LaTeX"]:                         # LaTeX
        out.write("\\item[version] {0}\n".format(tmp))
        if date != empty:
            out.write("\\item[last changes] {0}\n".format(date))
            if year != year_default:
                out.write("\\item[year] {0}\n".format(year))
                out.write("\\index{Year!" + year + "}\n")
    elif mode =="RIS":                            # RIS
        if notice != empty:
            notice += ";\n" + blank * (ris_fieldwidth + 1) + "Version: " + tmp
        else:
            notice = "Version: " + tmp
        if date != empty:
            out.write("Y2  - {0}\n".format(date))
            if year != year_default:
                out.write("PY  - {0}\n".format(year))
    elif mode in ["plain"]:                       # plain
        out.write("\n" + "version: ".ljust(labelwidth) + tmp.strip())
        if date != empty:
            out.write("\n" + "last changes: ".ljust(labelwidth) + date)
            if year != year_default: 
                out.write("\n" + "year:".ljust(labelwidth) + year)
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if bibfield_test(tmp.strip(), "version"):
            out.write("version".ljust(fieldwidth) + "= {" + tmp.strip() + "},\n")
        if bibfield_test(date, "date"):
            out.write("date".ljust(fieldwidth) + "= {" + date + "},\n")
        if bibfield_test(year, "year") and (year != year_default):
            out.write("year".ljust(fieldwidth) + "= {" + year + "},\n")
    elif mode in ["Excel"]:                       # Excel
        s_version = tmp.strip()
        if date != empty:
            s_lastchanges = date
            if year != year_default:
                s_year = year


# ======================================================================
#  functions in the context of description
        
# ------------------------------------------------------------------
def description(k, pp):                           # function: processes element <description ...> ... </description>
    """Processes the description elements.

    k: current knot
    pp: current package

    Fetches embedded text and the embbeded attribute language."""
    
    # description --> innertext
    # description --> TeXchars_restore

    global language_set                           # set: collect language
    global description_str                        # string: collect description
    global level
    
##    for child in k:
##        print("***", pp.ljust(33), "description".ljust(11), child.tag)
    
    language = k.get("language", empty)           # get attribute language

    if language in languagecodes:                 # convert language keys
        languagex = languagecodes[language]
    else:
        languagex = empty
    language_set.add(language)                    # collect languages uniqly
    
    level = empty                                 # initialize variable

    tmptext = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    tmptext = re.sub("[ \t]+\n", "\n", tmptext)
    tmptext = TeXchars_restore(tmptext)           # restore changed characters
    tmptext = re.sub("[\n]+[ ]*[\n]+", "\n\n", tmptext)

    if mode in ["LaTeX"]:                         # LaTeX
        if languagex != empty:
            out.write("\\item[description] ({0})".format(languagex))
            out.write("\\index{{Language in description/documentation! {0}}}\n".format(languagex))
        else:
            out.write("\\item[description] ")
    elif mode in ["RIS"]:                         # RIS
        if languagex != empty:
            out.write("AB  - ({0}) ".format(languagex))
        else:
            out.write("AB  - ")
    elif mode in ["plain"]:                       # plain
        if languagex != empty:
            out.write("\ndescription:".ljust(labelwidth + 1) + "(" + languagex + ")")
        else:
            out.write("\ndescription:".ljust(labelwidth + 1))
    elif mode in ["BibLaTeX"]:                    # BibLaTeX
        if languagex != empty:
            tmptext2 = "(" + languagex + ")"
        else:
            tmptext2 = empty
        if not "abstract" in skip_biblatex:
            if description_str != empty:
                description_str += "\n\n" + blank * (fieldwidth + 2) + tmptext2 + tmptext.strip()
            else:
                description_str = "abstract".ljust(fieldwidth)+ "= {" + tmptext2 + tmptext.strip()
    elif mode in ["Excel"]:                       # Excel
        pass                                      #   for Excel do nothing

    if mode in ["LaTeX", "RIS", "plain"]:
        if tmptext != empty:
            out.write(tmptext.strip() +"\n")
    
# ------------------------------------------------------------------
def innertext(k, start, pp):                      # function innertext: looks for embedded text and elements and returns an evaluated string
    """Acts as an interface during the processing of <description>...</description>.
    It scans the body of description and calls recursively other functions.
    It returns an evualated string.

    k:     current knot
    pp:    current package
    start: start of scanning"""
    
    global level
    
    tmp = start
    
    if tmp == None:
        tmp = empty
        
    for child in k:
        if child.tag == "em":                     # sub-element em
            mod_em(child, pp)
        elif child.tag == "a":                    # sub-element a
            mod_a(child, pp)
        elif child.tag == "i":                    # sub-element i
            mod_i(child, pp)
        elif child.tag == "tt":                   # sub-element tt
            mod_tt(child, pp)
        elif child.tag == "xref":                 # sub-element xref
            mod_xref(child, pp)
        elif child.tag == "pre":                  # sub-element pre
            mod_pre(child, pp)
        elif child.tag == "code":                 # sub-element code
            mod_code(child, pp)
        elif child.tag == "b":                    # sub-element b
            mod_b(child, pp)
        elif child.tag == "br":                   # sub-element br
            mod_br(child, pp)
        elif child.tag == "small":                # sub-element small
            mod_small(child, pp)
        elif child.tag == "p":                    # sub-element p
            level = empty
            mod_p(child, pp)
        elif child.tag == "ul":                   # sub-element ul
            oldlevel = level
            if oldlevel == empty:
                level = "ul"
            elif oldlevel == "ul-li":
                level = "li-ul"
            else:
                level = None
            mod_ul(child, pp)
            level = oldlevel
        elif child.tag == "ol":                   # sub-element ol
            oldlevel = level
            if oldlevel == empty:
                level = "ol"
            elif oldlevel == "ol-li":
                level = "li-ol"
            else:
                level = None
            mod_ol(child, pp)
            level = oldlevel
        elif child.tag == "li":                   # sub-element li
            oldlevel = level
            if oldlevel == "ul":
                level = "ul-li"
            elif oldlevel == "ol":
                level = "ol-li"
            elif oldlevel == "li-ul":
                level = "ul-li2"
            elif oldlevel == "li-ol":
                level = "ol-li2"
            else:
                level = None
            mod_li(child, pp)
            level = oldlevel
        elif child.tag == "dl":                   # sub-element dl
            level = empty
            mod_dl(child, pp)
        elif child.tag == "dt":                   # sub-element dt
            mod_dt(child, pp)
        elif child.tag == "dd":                   # sub-element dd
            mod_dd(child, pp)
            
        if child.text != None:
            tmp = tmp + child.text.strip()
        if child.tail != None:
            tmp += child.tail.strip()
    return tmp

# ------------------------------------------------------------------
def mod_a(k, pp):                             # function: processes element <a ...> ... </a>
    """Processes the a elements.

    k:  current knot
    pp: current package

    Fetches any embedded text and the local attribute href."""

    # mod_b --> innertext
    
    tmp = k.get("href", empty)                # get attribute href
    p   = re.search("http", tmp)              # searches "http" in string
    
    if p == None:                             # build complete URL
        tmp2 = ctanUrl + tmp
    else:
        tmp2 = tmp

    if k.text == None:                        # no embedded text
        k.text = tmp                          #   get embedded text

    tmp3 = innertext(k, k.text, pp).strip()   # get embedded text and sub-elements
        
    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        tmp3   = re.sub("_", "-", tmp3)       #   change embedded text
        k.text = "§§=1§§3href§§1{0}§§2§§1{1}§§2§§=1".format(tmp2, tmp3)
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§=1{0} ({1})§§=1".format(tmp3, tmp2) #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excek do nothing

# ------------------------------------------------------------------
def mod_b(k, pp):                             # function: processes element <b>...</b>
    """Processes the b elements.

    k:  current knot
    pp: current package

    Fetches any embedded text."""
    
    # mod_b --> innertext
##    for child in k:
##        print("***", pp.ljust(33), "b".ljust(11), child.tag)
    
    tmp = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    
    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        k.text = "§§=1§§3textbf§§1{0}§§2§§=1".format(tmp) #   change embedded text
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§=1'{0}'§§=1".format(tmp)  #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_br(k, pp):                            # function: processes element <br/>
    """Processes the br elements."""
    
    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        k.text = "§§3§§3"                     #   change embedded text
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§-"                        #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_code(k, pp):                          # function: processes element <code>...</code>
    """Processes the code elements.

    k:  current knot
    pp: current package

    Fetches any embedded text."""

    # mod_code --> innertext
    # mod_code --> mod_TeXchars2
    
    tmp = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    tmp = mod_TeXchars2(tmp)

    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        if "\n" in tmp.strip():
            tmp = re.sub("\n", "§§-", tmp)
            k.text = "§§3begin§§1verbatim§§2§§-{0}§§-§§3end§§1verbatim§§2".format(tmp)
        else:
            k.text = "§§=1§§3verb|{0}|§§=1".format(tmp.strip())
    elif mode in ["RIS", "plain"]:            # RIS / plain
        if "\n" in tmp.strip():
            k.text = "§§-{0}§§-".format(tmp.strip()) #   change embedded text
        else:
            k.text = "§§=1|{0}|§§=1".format(tmp.strip())
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing
  
# ------------------------------------------------------------------
def mod_dd(k, pp):                                # function: processes element <dd>...</dd>
    """Processes the dd sub-elements.

    k:  current knot
    pp: current package

    Fetches embedded text."""

    # mod_dd --> innertext
    # mod_dd --> mod_TeXchars1
    # mod_dd --> gen_fold

    tmp   = innertext(k, k.text, pp).strip()      # get embedded text and sub-elements
    tmp   = mod_TeXchars1(tmp)
    tmp   = re.sub("[\n]+", blank, tmp)
    tmp   = re.sub("[ \t]+", blank, tmp)         
    width = cases[mode]
    tmpbl = "§§=" + str(width)

    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX/BibLaTeX
        k.text = tmp
    if mode in ["RIS", "plain"]:                  # BibLaTeX / RIS / plain
        tmp = gen_fold(tmp, width)
        k.text = tmp                       
    if mode in ["Excel"]:                         # Excel
        pass                                      #   for Excel do nothing

# ------------------------------------------------------------------
def mod_dl(k, pp):                                # function: processes element <dl>...</dl>
    """Processes the ol elements.

    k: current knot

    Fetches embedded text."""

    # mod_dl --> innertext

    tmp   = innertext(k, k.text, pp).strip()      # get embedded text and sub-elements
    tmp   = re.sub("[\n]+", blank, tmp)
    tmp   = re.sub("[ \t]+", blank, tmp)         
    width = cases[mode]
    tmpbl = "§§=" + str(width)
    
    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX/BibLaTeX
        tmp = "§§-" + tmpbl + "§§3begin§§1description§§2{0}§§-".format(tmp) + tmpbl + "§§3end§§1description§§2§§-§§-"
        k.text = tmp
    if mode in ["RIS", "plain"]:                  # BibLaTeX / RIS / plain##    print("***mod_dt, k.text: |{0}|".format(k.text))
        k.text = "§§-" + tmpbl + tmp                       
    if mode in ["Excel"]:                         # Excel
        pass                                      #   for Excel do nothing

# ------------------------------------------------------------------
def mod_dt(k, pp):                                # function: processes element <dt>...</dt>
    """Processes the dt sub-elements.

    k: current knot
    pp: current package

    Fetches embedded text."""

    # mod_dt --> innertext

    tmp   = innertext(k, k.text, pp).strip()      # get embedded text and sub-elements
    width = cases[mode]
    tmpbl = "§§=" + str(width)

    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX/BibLaTeX
        k.text = "§§-" + tmpbl + "§§3item[{0}] ".format(tmp)
    if mode in ["RIS", "plain"]:                  # BibLaTeX / RIS / plain
        k.text = "§§-" + tmpbl + "+ " + tmp + ": "                
    if mode in ["Excel"]:                         # Excel
        pass                                      #   for Excel do nothing
    
# ------------------------------------------------------------------
def mod_em(k, pp):                            # function: processes element <em>...</em>
    """Processes the em elements.

    k:  current knot
    pp: current package

    Fetches any embedded text."""
    
    # mod_em --> innertext
    
    tmp = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    
    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        k.text = "§§=1§§3emph§§1{0}§§2§§=1".format(tmp) #   change embedded text
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§=1'{0}'§§=1".format(tmp)          #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing
    
# ------------------------------------------------------------------
def mod_i(k, pp):                             # function: processes element <i>...</i>
    """Processes the i elements.

    k:  current knot
    pp: current package

    Fetches any embedded text."""

    # mod_xref --> innertext

    tmp = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements

    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        k.text = "§§=1§§3emph§§1{0}§§2§§=1".format(tmp) #   change embedded text
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§=1'{0}'§§=1".format(tmp)          #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_li(k, pp):                                # function: processes element <li>...</li>
    """Processes the li elements.

    k: current knot
    pp: current package

    Fetches embedded text."""

    global level

    # mod_li --> innertext
    # mod_li --> mod_TeXchars1
    # mod_li --> test_embedded
    # mod_li --> gen_fold

    tmptext = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    tmppref = empty

    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX / BibLaTeX
        tmptext = mod_TeXchars1(tmptext)
    tmptext = re.sub("\n", blank, tmptext)
    tmptext = re.sub("[ \t]+", blank, tmptext)

    width = cases[mode]
    tmpbl = "§§=" + str(width)

    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX/BibLaTeX
        tmptext = "§§-" + tmpbl + "§§3item {0}".format(tmptext)
        k.text  = tmptext
    elif mode in ["RIS", "plain"]:                # RIS/plain
        if level == "ul-li2":
            tmppref ="++"
            tmptext = gen_fold(tmptext, width + 3)
        elif level == "ul-li":
            tmppref ="+"
            if not test_embedded(k, pp):
                tmptext = gen_fold(tmptext, width + 2)
        elif level == "ol-li2":
            tmppref ="**"
            tmptext = gen_fold(tmptext, width + 2)
        elif level == "ol-li":
            tmppref ="*"
            if not test_embedded(k, pp):
                tmptext = gen_fold(tmptext, width + 3)
        tmptext = "§§-" + tmpbl + tmppref + blank * 2 + tmptext
        k.text  = tmptext
    elif mode in ["Excel"]:                       # Excel
        pass

# ------------------------------------------------------------------
def mod_pre(k, pp):                           # function: processes element <pre>...</pre>
    """Processes the pre elements.

    k:  current knot
    pp: current package

    Fetches any embedded text."""

    # mod_pre --> innertext
    # mod_pre --> mod_TeXchars2
    
    tmp = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    tmp = mod_TeXchars2(tmp)

    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        if "\n" in tmp.strip():
            k.text = "§§3begin§§1verbatim§§2§§-{0}§§-§§3end§§1verbatim§§2".format(tmp)
        else:
            k.text = "§§=1§§3verb|{0}|§§=1".format(tmp.strip())
    elif mode in ["RIS", "plain"]:            # RIS / plain
        if "\n" in tmp.strip():
            k.text = "§§-{0}§§-".format(tmp.strip()) #   change embedded text
        else:
            k.text = "§§=1|{0}|§§=1".format(tmp.strip())
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_small(k, pp):                         # function: processes element <small>...</small>
    """Processes the small elements.

    k:  current knot
    pp: current package

    Fetches any embedded text."""

    # mod_small --> innertext
    
    tmp = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements

    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        k.text = "§§=1§§1§§3small {0}§§2§§=1".format(tmp) # change embedded text
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§=1'{0}'§§=1".format(tmp)          #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing

# ------------------------------------------------------------------
def mod_TeXchars1(s):                                       # auxiliary function: prepares characters for LaTeX/BibLaTeX in a paragraph
    """auxilary function: Prepares characters for LaTeX/BibLaTeX (only for description - intended for to be printed).

    s: string

    returns a changed string s."""

    # $ ---> \$   ---> 
    # { ---> \{   ---> \textbraceleft
    # } ---> \}   ---> \textbraceright
    # # ---> \#   ---> 
    # \ ---> ...  ---> \textbackslash
    # & ---> \&   ---> 
    # _ ---> \_   ---> 
    # ^ ---> \^{} ---> \textasciicircum
    # % ---> \%   ---> 
    # ~ ---> \~{} ---> \textasciitilde
	
    # \ ---> §§3
    # { ---> §§1
    # } ---> §§2

    tmp = s
    tmp = re.sub("[\[]", "[", tmp)                         # change [
    tmp = re.sub("≥", "§§4>=§§4", tmp)                     # change ≥
    tmp = re.sub("≤", "§§4<=§§4", tmp)                     # change ≤
    tmp = re.sub("#", "§§3§§6", tmp)                       # change #
    tmp = re.sub("_", "§§3§§7", tmp)                       # change _
    tmp = re.sub("~", "§§1§§3textasciitilde§§2", tmp)      # change ~
    tmp = re.sub("&", "§§3§§5", tmp)                       # change &
    tmp = re.sub("%", "§§3§§9", tmp)                       # change %
    tmp = re.sub("{", "§§1§§3textbraceleft§§2", tmp)       # change {
    tmp = re.sub("}", "§§1§§3textbraceright§§2", tmp)      # change }
    tmp = re.sub("\^", "§§1§§3textasciicircum§§2", tmp)    # change ^
    tmp = re.sub("[$]", "§§3§§4", tmp)                     # change $
    tmp = re.sub(r"\\", "§§1§§3textbackslash§§2", tmp)     # change \
    tmp = re.sub("“", "``", tmp)                           # change	“
    tmp = re.sub("”", "''", tmp)                           # change	”
    tmp = re.sub("`", "'", tmp)                            # change	`
    tmp = re.sub("´", "'", tmp)                            # change	´
    return tmp

# ------------------------------------------------------------------
def mod_TeXchars2(s):                                      # auxiliary function: prepares characters for LaTeX/BibLaTeX
    """auxiliary function: Prepares characters for LaTeX/BibLaTeX (only for description - intended for to be used by LaTeX).

    s: string

    returns a changed string s."""
    
    tmp = s
    tmp = re.sub("{", "§§1", tmp)                          # change	{
    tmp = re.sub("}", "§§2", tmp)                          # change	}
    tmp = re.sub(r"\\", "§§3", tmp)                        # change	\
    tmp = re.sub("[$]", "§§4", tmp)                        # change	$
    tmp = re.sub("&", "§§5", tmp)                          # change	&
    tmp = re.sub("#", "§§6", tmp)                          # change	#
    tmp = re.sub("_", "§§7", tmp)                          # change	_
    tmp = re.sub("\^", "§§8", tmp)                         # change	^
    tmp = re.sub("%", "§§9", tmp)                          # change	%
    tmp = re.sub("~", "§§0", tmp)                          # change	~
    tmp = re.sub("“", "``", tmp)                           # change	“
    tmp = re.sub("”", "''", tmp)                           # change	”
    tmp = re.sub("`", "'", tmp)                            # change	`
    tmp = re.sub("´", "'", tmp)                            # change	´
    return tmp

# ------------------------------------------------------------------
def mod_tt(k, pp):                            # function: processes element <tt>...</tt>
    """Processes the tt elements.

    k: current knot
    pp: current package

    Fetches embedded text."""
    
    # mod_tt --> innertext
    # mod_tt --> mod_TeXchars1

    tmp = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    
    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        tmp    = mod_TeXchars1(tmp)           #   change embedded text
        k.text = "§§=1§§3texttt§§1{0}§§2§§=1".format(tmp) 
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§=1{0}§§=1".format(tmp)    #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excel do nothing


# ------------------------------------------------------------------
def mod_xref(k, pp):                          # function: processes element <xref ...> ... </xref>
    """Processes the xref elements.

    k: current knot
    pp: current package

    Fetches any embedded text and the attribute refid."""

    # mod_xref --> innertext
        
    tmp  = k.get("refid", empty)              # get attribute refid
    tmp2 = ctanUrl4 + tmp                     # build the complete URL
    
    if k.text == None:                        # no embedded text
        k.text = tmp                          #   get embedded text
        
    tmp3 = innertext(k, k.text, pp).strip()   # get embedded text and sub-elements
        
    if mode in ["LaTeX", "BibLaTeX"]:         # LaTeX / BibLaTeX
        tmp3   = re.sub("_", "-", tmp3)       #   change embedded text
        k.text = "§§=1§§3href§§1{0}§§2§§1{1}§§2§§=1".format(tmp2, tmp3)
    elif mode in ["RIS", "plain"]:            # RIS / plain
        k.text = "§§=1{0} ({1})§§=1".format(tmp3, tmp2) #   change embedded text
    elif mode in ["Excel"]:                   # Excel
        pass                                  #   for Excek do nothing

# ------------------------------------------------------------------
def mod_ol(k, pp):                                # function: processes element <ol>...</ol>
    """Processes the ol elements.

    k: current knot
    pp: current package

    Fetches embedded text."""

    # mod_ol --> innertext

    tmp = innertext(k, k.text, pp).strip()        # get embedded text and sub-elements
    
    tmp   = re.sub("[\n]+", blank, tmp)
    tmp   = re.sub("[ \t]+", blank, tmp)         
    width = cases[mode]
    tmpbl = "§§=" + str(width)

    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX/BibLaTeX
        k.text = "§§-" + tmpbl + "§§3begin§§1enumerate§§2{0}§§-".format(tmp) + tmpbl + "§§3end§§1enumerate§§2§§-"
    if mode in ["RIS", "plain"]:                  # RIS / plain
        k.text = tmp + "§§-"                       
    if mode in ["Excel"]:                         # Excel
        pass                                      #   for Excel do nothing

# ------------------------------------------------------------------
def mod_p(k, pp):                                 # function: processes element <p> ... </p>
    """Processes the p elements.

    k:  current knot
    pp: current package

    Fetches embedded text."""

    # mod_p --> innertext
    # mod_p --> mod_TeXchars1
    # mod_p --> test_embedded
    # mod_p --> gen_fold

    tmptext = innertext(k, k.text, pp).strip()    # get embedded text and sub-elements
    width   = cases[mode]

    tmptext = re.sub("[\n]+", blank, tmptext)
    tmptext = re.sub("[ ]+", blank, tmptext)
    
    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX
        tmptext  = mod_TeXchars1(tmptext)
        if not test_embedded(k, pp):
            tmptext = gen_fold(tmptext, width)
        tmptext += "§§-§§-§§=" + str(width)
        k.text   = tmptext
    elif mode in ["plain", "RIS"]:                # plain/RIS
        if not test_embedded(k, pp):
            tmptext = gen_fold(tmptext, width)
        tmptext += "§§-§§-§§=" + str(width)
        k.text   = tmptext
    elif mode in ["Excel"]:                       # Excel
        pass                                      #  do nothing

# ------------------------------------------------------------------
def mod_ul(k, pp):                                # function: processes element <ul>...</ul>
    """Processes the ul elements.

    k:  current knot
    pp: current package

    Fetches any embedded text."""

    # mod_ul --> innertext

    tmp = innertext(k, k.text, pp).strip()        # get embedded text and sub-elements
    
    tmp   = re.sub("[\n]+", blank, tmp)
    tmp   = re.sub("[ \t]+", blank, tmp)
    width = cases[mode]
    tmpbl = "§§=" + str(width)

    if mode in ["LaTeX", "BibLaTeX"]:             # LaTeX/BibLaTeX
        k.text = "§§-" + tmpbl + "§§3begin§§1itemize§§2{0}§§-".format(tmp) + tmpbl + "§§3end§§1itemize§§2§§-"
    if mode in ["RIS", "plain"]:                  # RIS / plain
        k.text = tmp + "§§-"
    if mode in ["Excel"]:                         # Excel
        pass                                      #   for Excel do nothing

# ------------------------------------------------------------------
def test_embedded(k, pp):                         # auxiliary function test_embedded: tests current knot for embedded material
    """auxiliary function: tests current knot for embedded material

    k :  current knot
    pp : current package

    Resturns TRUE, if there are embedded elements in k."""
    
    tmp = False
    for child in k:
        tmp = tmp or (child.tag in ["ol", "ul", "li", "pre", "code"])
    return tmp

# ------------------------------------------------------------------
def TeXchars_restore(s):                                   # auxiliary function: restores characters for LaTeX/BibLaTeX
    """auxiliary function: Restores characters for LaTeX/BibLaTeX.

    s: string

    returns a changed string s."""
	
    tmp  = s
    tmp = re.sub("§§=12(§§=1)?", blank * 12, tmp)
    tmp = re.sub("§§=10(§§=1)?", blank * 10, tmp)
    tmp = re.sub("§§=18(§§=1)?", blank * 18, tmp)
    tmp2 = p8.findall(tmp)                                 # find "§§=xx"
    for i in tmp2:
        tmp = re.sub("§§=" + str(i), blank * int(i), tmp)  # change "§§=xx" to blanks
    tmp = re.sub("§§1", "{", tmp)                          # restore {
    tmp = re.sub("§§2", "}", tmp)                          # restore }
    tmp = re.sub("§§3", r"\\", tmp)                        # restore \
    tmp = re.sub("§§4", "$", tmp)                          # restore $
    tmp = re.sub("§§5", "&", tmp)                          # restore &
    tmp = re.sub("§§6", "#", tmp)                          # restore #
    tmp = re.sub("§§7", "_", tmp)                          # restore _
    tmp = re.sub("§§8", "^", tmp)                          # restore ^
    tmp = re.sub("§§9", "%", tmp)                          # restore %
    tmp = re.sub("§§0", "~", tmp)                          # restore ~
    tmp = re.sub("§§-", "\n", tmp)                         # restore \n
    return tmp

  
#===================================================================
# Main Part

if __name__ == "__main__":
    try:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    except:
        pass
    main()
else:
    if verbose:
        print("- Error: tried to use the program indirectly")


#===================================================================

# ------------------------------------------------------------------
# python dictionaries and lists

# usedTopics: Python dictionary (unsorted)
#   each element: <key for topic>:<number>
# usedPackages: Python list
#   each element: <package name>
# usedAuthors: Python dictionary (unsorted)
#   each element: <key for author>:<tuple with givenname and familyname>

# allauthoryears: Python dictionary
#   each element: allauthoryears[(<author>,<year>] = <appendix>
# citation_keys: Python dictionary
#   each element: itation_keys[package] = (<author>, <year>, <appendix>)

# authors: Python dictionary (sorted)
#   each element: <author key> <tuple with givenname and familyname> 
# packages: Python dictionary (sorted)
#   each element: <package key> <tuple with package name and package title>
# topics: Python dictionary (sorted)
#   each element: <topics name> <topics title>
# licenses: Python dictionary (sorted)
#   each element: <license key> (<license title>, <free>)
# topicspackage: Python dictionary (unsorted)
#   each element: <topic key> <list with package names>
# packagetopics: Python dictionary (sorted)
#   each element: <topic key> <list with package names>
# authorpackages: Python dictionary (unsorted)
#   each element: <author key> <list with package names>
# licensepackages: Python dictionary (mostly sorted)
#   each element: [license key] <list with package names>


#===================================================================
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
# 1.129 2021-10-22 RIS: better values for 'PY' and 'LA'; mapping von <also .../>; better values for 'Y2' and 'Y3'
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
# 2.0   2022-01-02 new concept for the processing of <description> ... </description>; content recursively processed
# 2.1   2022-01-02 functions mod_backslash and mod_TeXchars removed
# 2.2   2022-01-02 new functions: mod_TeXchars1, mod_TeXchars2, TeXchars_restore (change and restore the content of elements)
# 2.3   2022-01-03 functions renamed: p --> mod_p; ol --> mod_ol; ul --> mod_ul; dl --> mod_dl; li --> mod_li; dd --> mod_dd; dt --> mod_dt
# 2.4   2022-01-03 new function: innertext (scans the body of description and calls recursively other functions for the sub-elements)
# 2.5   2022-01-04 new function: mod_small (processing of <small> ...</small>)
# 2.6   2022-01-04 new functions: mod_dl, mod_dt, mod_dd (processing of <dl>, <dt>, and <dd>)
# 2.7   2022-01-06 nested <ol>/<ul> can be processed
# 2.8   2022-01-07 left indentation of <li> (mode dependant)
# 2.9   2022-01-09 new function gen_fold (folds content of <li>)
# 2.10  2022-01-10 new function test_embedded (controls the call of gen_fold in <p>, <li>, <dd>)
# 2.11  2022-01-11 new language code "zn,ja"
# 2.12  2022-01-26 texts for the -h option changed
# 2.13  2022-01-28 left indentation for all modes tuned
# 2.14  2022-01-28 additionally: output of date and time in statistics on output (-stat)
# 2.15  2022-02-02 additional license information: now with free a/o not free
# 2.16  2022-02-05 additional texts at the top of output files
# 2.17  2022-02-07 messages in get_topic_packages, get_name_packages, and get_author_packages changed
# 2.18    2022-02-15 new option -L (selection of packages by licenses)
# 2.18.1  2022-02-15 new variables: license_template_text, license_template_default, license_template (used by argparse); licensepackages
# 2.18.2  2022-02-15 new section for specifying -L by argparse
# 2.18.3  2022-02-15 new function get_license_packages (collecting packages for specified licenses)
# 2.18.4  2022-02-15 changes in load_pickle1: new CTAN.pkl component licensepackages
# 2.18.5  2022-02-15 new variable p9 [re.compile(license_template)]; allows filtering by license template
# 2.18.6  2022-02-15 changes in first_lines, licenseT, process_packages, make_stat, make_statistics, and process_packages
# 2.18.7  2022-02-16 shorttitlde and status can be used for -L, too
# 2.19    2022-02-19 error in make_stat corrected
# 2.20    2022-02-21 some corrections in make_stat
# 2.21    2022-02-23 in LaTeX mode: output of licenses and related packages (tlp) + output of licenses and explainations (lic)
# 2.21.1  2022-02-03 new function make_tlp; changes in main(); new file xyz.tlp; called in LaTeX document (option -mt)
# 2.21.2  2022-02-23 new function make_lics; changes in main(); new file xyz.lic; called in LaTeX document (option -mt)
# 2.21.3  2022-02-23 additions and corrections in make_tlp, make_tap, make_lics, make_xref
# 2.22    2022-03-01 additions and corrections in make_stat
# 2.23    2022-03-01 texts for argparse and terminal log changed
# 2.24    2022-03-01 correc tions in first_lines (plain, BibLaTeX)


# ------------------------------------------------------------------
# Probleme/Ideen:

# - Idee: Klassenkonzept für die Ausgabe: für jeden Ausgabetyp eine eigene Klasse?
# - kann Zeitstempel bei XML/PDF-Dateien genutzt werden? wahrscheinlich nicht (?)
# - <ol>/<ul> gescchachtelt; Stack verwenden (?)
# - <ol> sollte bei RIS und plain Nummern erzeugen
# - BibLaTeX: language: volle Namen der Sprache (- bringt nichts)
# - Prozessor über Parameter wählbar (--)
# - verschiedene Präambel-Sätze für XeLaTeX und LuaLaTeX; automatisch ausgewählt (--)
# - lualatex-Ausgabe: missing character
# - Fehler bei BibLateX: author nicht normgerecht?
# - noch Fehler: (fehlende) Einrückung in description an manchen Stellen (x)
# - RIS: relativ bei L1 (-)
# - skip_biblatex auch für andere Modus?
# - BibLaTeX: Probleme noch bei Mehrfach-related (laut jab[]ref)
# - besseres Zusammenspiel von §§= und TeXchars_restore

# - Element-Hierarchie und function-Hierarchie neu machen

# - Strategien stimmt nicht mehr


