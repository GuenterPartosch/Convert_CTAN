#!/usr/bin/python3
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

"""
menu_CTANLoadOut.py
(C) Günter Partosch 2024|2025/2026

CTANLoadOut.py is part of the CTAN bundle (CTANLoad.py, CTANOut.py,
CTANLoadOut.py, menu_CTANLoadOut.py).

The menu_CTANLoadOut.py program is used to call up and control the
CTANLoadOut.py program via a menu.

 ---------------------------------------------------------------
 Requirements:
 + operating system windows 10/11 or Linux (like Linux Mint or Ubuntu or
   Debian)
 + wget a/o wget2 is installed
 + Python installation 3.10 or newer
 + a series of Python modules (see the import instructions below)

--------------------------------------------------------------------
The program menu_CTANLoadOut.py needs the following Python programs:

menu_CTANLoadOut.py ==> CTANLoadOut.py
CTANLoadOut.py      ==> CTANLoad.py
                    ==> CTANOut.py

CTANLoadOut.py:  It combines the tasks of CTANLoayd.py and CTANOut.py:

CTANLoad.py:     Loads XLM and PDF documentation files from CTAN a/o
                 generates some special lists, and prepares data for
                 CTANOut.
CTANOut.py:      Converts CTAN XLM package files to LaTeX, RIS, plain,
                 BibLaTeX, Excel [tab separated].

menu_CTANLoadOut.py must be located in the same OS directory as
CTANLoad.py, CTANOut.py, and CTANLoadOut.py.

--------------------------------------------------------------------
The program essentially uses the tkinter module and its submodules:
+ tkinter as tk
+ tkinter.ttk as ttk
+ tkinter.messagebox as tkm
+ tkinter.scrolledtext

In particular, the following functions|methods are used:

scrolledtext.ScrolledText

tk.BooleanVar
tk.Button
tk.END
tk.StringVar
tk.Tk
tk.Toplevel
tk.W

tkm.INFO
tkm.askyesno
tkm.showinfo
ttk.Checkbutton
ttk.Combobox
ttk.Button
ttk.Entry
ttk.Label

xyz.get
xyz.grid
xyz.insert
xyz.mainloop
xyz.pack
xyz.set
xyz.title
xyz.current

 ---------------------------------------------------------------
menu_CTANLoadOut.py needs the programs CTANLoad.py, CTANOut.py, and CTANLoadOut.py.

see also menu_CTANLoadOut-changes.txt
         menu_CTANLoadOut-messages.txt
         menu_CTANLoadOut-modules.txt
         CTAN-files.txt
         call.txt
         installation.txt
"""


# ====================================================================
# some imports

# 2.2.1  2026-04-13 import textwrap

import tkinter as tk                                                    # basis for the most things
import tkinter.ttk as ttk                                               # an alternative
import tkinter.messagebox as tkm                                        # message output
from tkinter import scrolledtext                                        # show scrollable text
import sys                                                              # system calls
import platform                                                         # OS informations
import subprocess                                                       # handling of sub-processes
from tempfile import TemporaryFile                                      # subprocess.run
import textwrap                                                         # wrapping of texts

# 2.1    2026-04-10 date and version of CTANLoad, CTANOut und CTANLoadOut via Import

from CTANLoad import PRG_VERSION as CTANLOAD_VERSION                    # version of CTANLoad.py
from CTANLoad import PRG_DATE as CTANLOAD_DATE                          # date of CTANLoad.py
from CTANOut import PROGRAM_VERSION as CTANOUT_VERSION                  # version of CTANOut.py
from CTANOut import PROGRAM_DATE as CTANOUT_DATE                        # date of CTANOut.py
from CTANLoadOut import PROGRAM_VERSION as CTANLOADOUT_VERSION          # version of CTANLoadOut.py
from CTANLoadOut import PROGRAM_DATE  as CTANLOADOUT_DATE               # date of CTANLoadOut.py
from CTANLoadOut import ALL_DEF1, ALL_DEF2, ALL_DEF3                    # import some values of CTANLoadOut

# --------------------------------------------------------------------
# unbundle the imported ALL_DEF1, All_DEF2, and ALL_DEf3

# 2.1    2026-04-10 date and version of CTANLoad, CTANOut und CTANLoadOut via Import

(AUTHOR_TEMPLATE_DEFAULT, AUTHOR_LOAD_TEMPLATE_DEFAULT,
AUTHOR_OUT_TEMPLATE_DEFAULT, LICENSE_TEMPLATE_DEFAULT,
LICENSE_LOAD_TEMPLATE_DEFAULT, LICENSE_OUT_TEMPLATE_DEFAULT,
KEY_TEMPLATE_DEFAULT, KEY_LOAD_TEMPLATE_DEFAULT,
KEY_OUT_TEMPLATE_DEFAULT, NAME_TEMPLATE_DEFAULT,
NAME_LOAD_TEMPLATE_DEFAULT, NAME_OUT_TEMPLATE_DEFAULT,
YEAR_TEMPLATE_DEFAULT, YEAR_LOAD_TEMPLATE_DEFAULT,
YEAR_OUT_TEMPLATE_DEFAULT)                                  = ALL_DEF1  # unbundle ALL_DEf1

(BTYPE_DEFAULT, MODE_DEFAULT, NUMBER_DEFAULT,
OUTPUT_NAME_DEFAULT, SKIP_DEFAULT, SKIP_BIBLATEX_DEFAULT,
TIMEOUT_DEFAULT)                                            = ALL_DEF2  # unbundle ALL_DEf2

(DOWNLOAD_DEFAULT, INTEGRITY_DEFAULT, LISTS_DEFAULT,
MAKE_OUTPUT_DEFAULT, MAKE_TOPICS_DEFAULT, NO_FILES_DEFAULT,
PDF_OUTPUT_DEFAULT, REGENERATE_DEFAULT, STATISTICS_DEFAULT,
VERBOSE_DEFAULT, DEBUGGING_DEFAULT)                         = ALL_DEF3  # unbundle ALL_DEf3

# --------------------------------------------------------------------
# some settings

# 1.11  2024-07-08: as far as possible and useful: string interpolation
#                   via .format replaced by f-strings

mm = tk.Tk()                                                            # start of menu
mm.title("Menu for CTANLoadOut (a combination of CTANLoad + CTANOut)")  # title of menu

# --------------------------------------------------------------------
MENU_CTANLOADOUT_DATE    = "2026-04-13"                                 # menu_CTANLoadOut.py
MENU_CTANLOADOUT_VERSION = "2.2.3"

PROGRAM_NAME             = "menu_CTANLoadOut.py"                        # name of the program 
AUTHOR_PROGRAM           = "Günter Partosch"
AUTHOR_EMAIL             = "Guenter.Partosch@web.de\n(formerly " +\
                           "Guenter.Partosch@hrz.uni-giessen.de)"
AUTHOR_INST              = "formerly Justus-Liebig-Universität, " +\
                           "Hochschulrechenzentrum"
OPERATINGSYS             = platform.system()                            # operating system on which the program runs
REMOTE_PROGRAM_NAME      = "CTANLoadOut.py"                             # program to be processed

# --------------------------------------------------------------------
EMPTY                    = ""
BLANK                    = " "
values:dict              = {}                                           # values found in menu; collected by collect_values
option_line:dict         = {}                                           # option <--> line; set by get_option_line
call:list                = []                                           # parameters for the call of CTANLoadOut.py
nr:int                   = 0                                            # number of elements in SEQUENCE; will be se:t later
log:str                  = EMPTY                                        # to be used for log data
changes:str              = EMPTY                                        # corrections made

# 1.20   2025-12-05: better colors

COLOR1                   = "#FEE4BE"                                    # [B0]: Start; [B1]: Reset fields; [B2]: Clear menu; [B3]: Close menu (Quit)
COLOR2                   = "#DAFBC1"                                    # [B4]: Entries; [B5]: Checkboxe; [B6]: Buttons; [B7]: Comboboxes; [B8]: Entries; [B9]: Version
COLOR3                   = "#B0EEF6"                                    # [B10]: Log File
COLOR4                   = "red"                                        # header

# --------------------------------------------------------------------
WARN_TEXT                = "+ '{0}' '{1}' changed to '{2}' " +\
                           "(due to {3})\n"                             # template for warning texts
TIMEOUT                  = 1000                                         # timeout (in sec) for the main subprocess

# --------------------------------------------------------------------
# 1.15   2025-10-02: -d adapted to different operating systems

if OPERATINGSYS == "Windows":                                           # the directory separator depends on the OS
    dir_sep = "\\"
    act_dir = ".\\"
else:
    dir_sep = "/"
    act_dir = "./"
    
version = f"""
Call sequence:
=============
menu_CTANLoadOut.py ==> calls ==> CTANLoadOut.py

CTANLoadOut.py      ==> calls ==> CTANLoad.py
                    ==> calls ==> CTANOut.py

Versions:
========
+ Menu_CTANLoadOut.py ({MENU_CTANLOADOUT_DATE},
                      version {MENU_CTANLOADOUT_VERSION})
+ CTANLoadOut.py      ({CTANLOADOUT_DATE}, version {
                      CTANLOADOUT_VERSION})
+ CTANLoad.py         ({CTANLOAD_DATE}, version {CTANLOAD_VERSION})
+ CTANOut.py          ({CTANOUT_DATE}, version {CTANOUT_VERSION})

{AUTHOR_PROGRAM}; _E-Mail: {AUTHOR_EMAIL}
"""


# ====================================================================
# Functions:
#
# check_values()
# collect_values()
# get_default(option)
# get_option_line()
# get_option_line_value(option)
# get_value(option)
# help1()
# help2()
# help3()
# help4()
# help5()
# info_version()
# init_buttons()
# init_fields()
# make_call()
# set_value(option, value)
# set_value_combobox(option, value)
# quit()
# start()
# start_call()
# text_wrap(text, ident, length)

# --------------------------------------------------------------------
def check_values():                                                     # function check_values
    """
    Checks some option values and resets some.
    This is to avoid collisions and contradictions between the options.

    no parameters

    global variable:
    + _V
    + changes

    no messages
    """
    
    # 1.1   2024-05-30: in check_value: Errors corrected and 
    #                   inconsistencies eliminated
    # 1.4   2024-06-11: additional values for -m: tsv, csv
    # 1.9.9 2024-06-19: former special handling of -m deactivated + 
    #                   resettings of -m now by set_value_combobox
    # 1.16.1 2025-10-14: a prompt before the actual execution
    # 1.17   2025-11-18: changes in check_values
    # 1.17.1 2025-11-18: for certain changes made by check_values:
    #                    warnings are issued
    # 1.17.2 2025-11-18: check_values cleaned up 
    # 1.17.3 2025-11-18: "Short circuits" removed

    # check_value ==> get_value
    #             ==> get_option_line_value
    #             ==> get_default
    #             ==> set_value_combobox

    # (1)  check -m
    # (2)  ckeck -b 
    # (3)  check -A, -_L, -t, -k, -y
    # (3a) check -A 
    # (3b) check -_L 
    # (3c) check -t 
    # (3d) check -k
    # (3e) check -y
    # (4)  check -nf
    # (5)  check -b
    # (6)  check -sb
    # (7)  check -p
    # (8)  check -mt
    # (9)  check -mo
    
    global _V                                                           # list with tk variables
    global changes                                                      # changes made

    message_text:str = EMPTY                                            # initialize message text
    changed:set      = set()                                            # collect changed values to prevent collissions
    changes          = "changes made:\n"

# ....................................................................
# (1) check -m (one of LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,
    #               biblatex, bib,Excel,excel,csv,tsv)
    
    value, line, kind, default = get_option_line_value("-m")          
    if value in ["LaTeX", "RIS", "plain", "BibLaTeX", "Excel"]:         # LaTeX, RIS, plain, BibLaTeX, Excel
        pass
    elif value in ["latex", "tex"]:                                     # latex, tex
        message_text += WARN_TEXT.format("-m", value, "LaTeX", "-m (1)")
        _V[line].set("LaTeX")                                          
    elif value == "ris":                                                # ris
        message_text += WARN_TEXT.format("-m", value, "RIS", "-m (1)")
        _V[line].set("RIS")                                           
    elif value == "txt":                                                # txt
        message_text += WARN_TEXT.format("-m", value, "plain", "-m (1)")
        _V[line].set("plain")
    elif value in ["biblatex", "bib"]:                                  # biblatex, bib
        message_text += WARN_TEXT.format("-m", value, "BibLaTeX",
                                         "-m (1)")
        _V[line].set("BibLaTeX")
    elif value in  ["excel", "csv", "tsv"]:                             # excel, tsv, csv
        message_text += WARN_TEXT.format("-m", value, "Excel", "-m (1)")
        _V[line].set("Excel")
    else:
        message_text += WARN_TEXT.format("-m", value, "RIS", "-m (1)")
        _V[line].set("RIS")                                             # set default

# ....................................................................
    # (2) ckeck -b (one of @online,@software,@misc,@ctan,@www           # option -b
    
    value, line, kind, default = get_option_line_value("-b")
    if value in ["@online", "@software", "@misc", "@ctan", "@www",
                 EMPTY]:
        pass
    else:                                                               # reset -b
        message_text += WARN_TEXT.format("-b", value, "@online",
                                         "-b (2)")
        _V[line].set("@online")

# ....................................................................
    # (3) check -A, -L, -t, -k, -y
    
    # (3a) check -A                                                     # option -A
    # -A ==> -Al ...
    #    ==> -Ao ...
    value, line, kind, default = get_option_line_value("-A")
    if value != default:
        value_Al = get_value("-Al")
        value_Ao = get_value("-Ao")
        if value_Al != value:                                           # reset -Al
            message_text += WARN_TEXT.format("-Al", value_Al, value,
                                             "-A (3a)")
            set_value("-Al", value)
        if value_Ao != value:                                           # reset -Ao
            message_text += WARN_TEXT.format("-Ao", value_Ao, value,
                                             "-A (3a)")
            set_value("-Ao", value)
    
    # (3b) check -L                                                     # option -L
    # -L ==> -Ll ...
    #    ==> -Lo ...
    value, line, kind, default = get_option_line_value("-L")
    if value != default:
        value_Ll = get_value("-Ll")
        value_Lo = get_value("-Lo")
        if value_Ll != value:                                           # reset -Ll
            message_text += WARN_TEXT.format("-Ll", value_Ll, value,
                                             "-L (3b)")
            set_value("-Ll", value)
        if value_Lo != value:                                           # reset -Lo
            message_text += WARN_TEXT.format("-Lo", value_Lo, value,
                                             "-L (3b)")
            set_value("-Lo", value)
    
    # (3c) check -t                                                     # option -t
    # -t ==> -tl ...
    #    ==> -to ...
    value, line, kind, default = get_option_line_value("-t")
    if value != default:
        value_tl = get_value("-tl")
        value_to = get_value("-to")
        if value_tl != value:                                           # reset -tl
            message_text += WARN_TEXT.format("-tl", value_tl, value,
                                             "-t (3c)")
            set_value("-tl", value)
        if value_to != value:                                           # reset -to
            message_text += WARN_TEXT.format("-to", value_to, value,
                                             "-t (3c)")
            set_value("-to", value)
    
    # (3d) check -k                                                     # option -k
    # -k ==> -kl ...
    #    ==> -ko ...
    value, line, kind, default = get_option_line_value("-k")
    if value != default:
        value_kl = get_value("-kl")
        value_ko = get_value("-ko")
        if value_kl != value:                                           # reset -kl
            message_text += WARN_TEXT.format("-kl", value_kl, value,
                                             "-k (3d)")
            set_value("-kl", value)
        if value_ko != value:                                           # reset -ko
            message_text += WARN_TEXT.format("-ko", value_ko, value,
                                             "-k (3d)")
            set_value("-ko", value)

    # (3e) check -y                                                     # option -y
    # -y ==> -yl ...
    #    ==> -yo ...
    value, line, kind, default = get_option_line_value("-y")
    if value != default:
        value_yl = get_value("-yl")
        value_yo = get_value("-yo")
        if value_yl != value:                                           # reset -yl
            message_text += WARN_TEXT.format("-yl", value_yl, value,
                                             "-y (3e)")
            set_value("-yo", value)
        if value_yo != value:                                           # reset -yo
            message_text += WARN_TEXT.format("-yo", value_yo, value,
                                             "-y (3e)")
            set_value("-yo", value)

    # To prevent inconsistencies for the following option, there are
    # certain priorities:
    # -nf > -b|-sb > p > mt
    
# ....................................................................
    # (4) check -nf                                                     # option -nf
    # -nf ==> -mt False
    #     ==> -p False
    #     ==> -f False
    value_nf = get_value("-nf")
    value_mt = get_value("-mt")
    value_p  = get_value("-p")
    value_f  = get_value("-f")

    if value_nf and value_mt:                                           # reset -mt
        changed.add("-mt")
        message_text += WARN_TEXT.format("-mt", value_mt, False,
                                         "-nf (4)")
        set_value("-mt", False)
    if value_nf and value_p:                                            # reset -p
        changed.add("-p")
        message_text += WARN_TEXT.format("-p", value_p, False,
                                         "-nf (4)")
        set_value("-p", False)
    if value_nf and value_f:                                            # reset -f
        changed.add("-f")
        message_text += WARN_TEXT.format("-f", value_f, False,
                                         "-nf (4)")
        set_value("-f", False)

# ....................................................................
    # (5+6) check -b | -sb                                              # option -b | -sb
    # -b  ==> -m BibLaTeX 
    #     ==> -mt False
    #     ==> -p False
    # -sb ==> -p False
    #     ==> -mt False
    #     ==> -m BibLateX
    # (5) check -b                                                      # option -b
    if not ("-b" in changed):
        value, line, kind, default = get_option_line_value("-b")
        if value != default:
            set_value("-m", "BibLaTeX")
            set_value("-mt", False)
            set_value("-p", False)
            changed.add("-m"); changed.add("-mt"); changed.add("-p")
            message_text += WARN_TEXT.format("-m", get_value("-m"),
                                             "BibLaTeX", "-b")
            message_text += WARN_TEXT.format("-mt", get_value("-mt"),
                                             False, "-b")
            message_text += WARN_TEXT.format("-p", get_value("-p"),
                                             False, "-b")

# ....................................................................
    # (6) check -sb                                                     # option -sb                                           
    if not("-sb" in changed):
        value, line, kind, default = get_option_line_value("-sb")
        if value != default:
            set_value("-m", "BibLaTeX")
            set_value("-mt", False)
            set_value("-p", False)
            changed.add("-m"); changed.add("-mt"); changed.add("-p")
            message_text += WARN_TEXT.format("-m", get_value("-m"),
                                             "BibLaTeX", "-sb")
            message_text += WARN_TEXT.format("-mt", get_value("-mt"),
                                             False, "-sb")
            message_text += WARN_TEXT.format("-p", get_value("-p"),
                                             False, "-sb")
            
# ....................................................................
    # (7) check -p                                                      # option -p
    # -p ==> -m LaTeX
    #    ==> -mt True
    if not ("-p" in changed):
        value_m  = get_value("-m")
        value_mt = get_value("-mt")
        value_p  = get_value("-p")
        
        a = value_m == "LaTeX"
        b = value_mt
        c = value_p
        
        if c and not a:                                                 # reset -m
            changed.add("-m")
            message_text += WARN_TEXT.format("-m", value_m, "LaTeX",
                                             "-p (7)")
            set_value_combobox("-m", "LaTeX")                           # set value for the combobox
            set_value("-m", "LaTeX")
        if not b and c:                                                 # reset -mt
            changed.add("-mt")
            message_text += WARN_TEXT.format("-mt", value_mt, True,
                                             "-p (7)")
            set_value("-mt", True)

# ....................................................................
    # (8) check -mt                                                     # option -mt
    # -mt ==> -m LaTeX
    if not ("-mt" in changed):
        value_m  = get_value("-m")
        value_mt = get_value("-mt")
        
        a = value_m == "LaTeX"
        b = value_mt
        
        if b and not a:                                                 # reset -m
            changed.add("-m")
            message_text += WARN_TEXT.format("-m", value_m, "LaTeX",
                                             "-p (8)")
            set_value_combobox("-m", "LaTeX")                           # set value for the combobox
            set_value("-m", "LaTeX")

# ....................................................................
    # (9) check -mo                                                     # option -mo
    # -mo ==> -f
    value_f  = get_value("-f")
    value_mo = get_value("-mo")

    if value_mo and value_f:                                            # reset -f
        message_text += WARN_TEXT.format("-f", value_f, False,
                                         "-mo (9)")
        set_value("-f", False)

    # (10) show changes                                                 # message
    if message_text != EMPTY:
        changes += message_text
        message_text = "Warnings:\n\n" + message_text
        tkm.showinfo(mm, message_text, icon=tkm.WARNING)
        message_text = EMPTY

    changed = set()
    
# --------------------------------------------------------------------
def clear_fields():                                                     # function clear_fields
    """
    The function requires the "SEQUENCE" tuple
    and the "options" dictionary.

    no parameters

    global Variables:
    + _V
    + call
    + values

    no merssages
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default,
    #                   get_option_line_value, get_value: extended for
    #                   type combobox

    global _V                                                           # list with tk variables
    global call                                                         # list: parameters for the call of CTANLoadOut.py
    global values                                                       # values found in menu; collected by collect_values
    global option_line                                                  # option <--> line; set by get_option_line
    
    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]
        kind, text1, default, text2, action = options[m]                # get the relevant items from options
        if kind in ["number", "listbox", "combobox", "text"]:
##            _E[line].delete(0, tk.END)
            _V[line].set(EMPTY)                                         # initialize with EMPTYstring
        elif kind == "checkbox":
            _V[line].set(False)                                         # initialize with False

    values      = {}                                                    # re-initialize the values list
    call        = []                                                    # re-initialize the call list
    option_line = {}                                                    # option <--> line; set by get_option_line
    
# --------------------------------------------------------------------
def collect_values():                                                   # function collect_values
    """
    Collects the values in the menu, compares them with the
    correspoinding defaults and generates a dictionary with
    option <--> value
    THe function requires the "SEQUENCE" tuple and the "options"
    dictionary.

    no parameters

    global variable:
    + values

    no messages
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default,
    #                   get_option_line_value, get_value: extended for
    #                   type combobox

    global values                                                       # values found in menu; collected by collect_values
    
    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]
        kind, text1, default, text2, action = OPTIONS[m]                # get the relevant items from OPTIONS
        if kind in ["text", "listbox"]:
            value = _E[line].get()
            if value != str(default):
                values[m] = value                                       # get the value of a text or# listbox option
        elif kind == "combobox":
            value = _CB[line].get()
            if value != str(default):
                values[m] = value                                       # get the value of a combobox option 
        elif kind == "number":
            value = _E[line].get()
            if value != str(default):
                values[m] = value                                       # get the value of a number option 
        elif kind == "list":
            value = _E[line].get()
            if value != str(default):
                values[m] = value                                       # get the value of a list option
        elif kind == "checkbox":
            value = _V[line].get()
            if value != default:
                values[m] = value                                       # get the value of a checkbox option

# --------------------------------------------------------------------
def get_default(opt:str) ->str:                                         # function get_default
    """
    Returns the default value (str) of a given option.
    
    The function requires the "OPTIONS" dictionary.

    parameter:
    opt : option to be inspected

    The function returns None:
    + the option is not in ["text", "listbox", "number", "combobox",
      "list", "checkbox"]
    + the option is not in the SEQUENCE disctionary

    no messages
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default,
    #                   get_option_line_value, get_value: extended for
    #                   type combobox

    if opt in SEQUENCE:
        kind = OPTIONS[opt][0]
        if kind in ["text", "listbox", "number", "combobox", "list",
                    "checkbox"]:                                        # headers excluded
            return OPTIONS[opt][2]                                      # get the default of opt
        else:
            return None
    else:
        return None

# --------------------------------------------------------------------
def get_option_line():                                                  # function get_option_line
    """
    Generates a dictionary with assignments of OPTIONS to lines.
    The function requires the "SEQUENCE" dictionary.

    no parameters

    global variable:
    + option_line

    no messages
    """

    global option_line                                                  # option <--> line; set by get_option_line
    
    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]
        option_line[m] = line

# --------------------------------------------------------------------
def get_option_line_value(option:str) ->tuple:                          # function get_option_line_value
    """
    Returns the tuple (value, line, kind, default) for a given option.
    
    The function requires the option_line and OPTIONS dictionary.

    parameter:
    option : option to be inspected
    
    The function returns None:
    + the option is not in ["text", "listbox", "number", "list",
      "combobox", "checkbox"]

    no messages
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default,
    #                   get_option_line_value, get_value: extended for
    #                   type combobox

    line = option_line[option]
    kind, text1, default, text2, action = OPTIONS[option]               # get the relevant items from# OPTIONS
    if kind in ["text", "listbox", "list", "combobox", "checkbox",
                "number"]:                                              # headers excluded
        value = _V[line].get()
        return (value, line, kind, default)
    else:
        return None
   
# --------------------------------------------------------------------
def get_value(option:str) ->str|bool|int:                               # function get_value
    """
    Returns the value (str|bool|int) of a given option.
    
    The function requires the "SEQUENCE" tuple, the "option_line" and
    "OPTIONS" dictionary.

    parameter:
    option : option to be inspected

    THe function returns None:
    + the option is not in ["text", "listbox", "number", "list",
      "checkbox", "combobox"]
    + the option is not in the SEQUENCE disctionary

    no messages
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default,
    #                   get_option_line_value, get_value: extended for
    #                   type combobox
    
    if option in SEQUENCE:
        tmp  = option_line[option]                                      # get line number of option
        kind = OPTIONS[option][0]                                       # get type of option
        if kind in ["text", "listbox", "number", "list", "checkbox",
                    "combobox"]:                                        # headers excluded
            value = _V[tmp].get()                                       # read value
            return value
        else:
            return None
    else:
        return None

# --------------------------------------------------------------------
def help1():                                                            # function help1 
    """
    Shows an info text (accumulated entry definitions for text, listbox,
    list, and number).
    
    The function requires the "SEQUENCE" tuple and the "OPTIONS"
    dictionary.

    no parameters

    no messages
    """

    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, 
    #                    help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message,
    #                    and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top
    #                    line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, 
    #                    and start improved
    
    tmp:str = EMPTY
    INDENT  = 8                                                         # indentation of wrapped texts
    LENGTH  = 55                                                        # max. length of wrapped texts
    
    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]                                              # get option
        kind, text1, default, text2, action = OPTIONS[m]                # get the relevant items for the option
        if kind in ["text", "listbox", "list"]:
            act_value = _V[line].get()                                  # get actual value of option
            tmp0 = f"[E{line}] {text1} ({m}); Default: {default}; " +\
                   f"actual value: {act_value}\n"
            tmp2 = text_wrap(tmp0, INDENT, LENGTH)                      # construct one line of the message text
            tmp += tmp2 + "\n"                                          # collect
##            tmp += f"[E{line}] {text1} ({m}); \n{10*BLANK}Default: " +\
##                   f"{default};\n{10*BLANK}actual value: {act_value}\n" 
        elif kind == "number":
            tmp0 = f"[E{line}] {text1} ({m}); Default: {default}\n"
            tmp2 = text_wrap(tmp0, INDENT, LENGTH)                      # construct one line of the message text
            tmp += tmp2 + "\n"                                          # collect
##            tmp += f"[E{line}] {text1} ({m}); \n{10*BLANK}Default: " +\
##                   f"{default}\n"                                       # construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO,
                 title="Description: Entries")                          # show message text

# --------------------------------------------------------------------
def help2():                                                            # function help2
    """
    Shows an info text (accumulated checkbox definitions).
    
    The function requires the "SEQUENCE" tuple and the "OPTIONS"
    dictionary.

    no parameters

    no messages
    """

    # 1.7    2024-06-18: small error in help2 corrected
    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, 
    #                    help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message,
    #                    and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top
    #                    line
    
    tmp:str = EMPTY
    INDENT  = 8                                                         # indentation of wrapped texts
    LENGTH  = 55                                                        # max. length of wrapped texts
    
    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]                                              # get the option
        kind, text1, default, text2, action = OPTIONS[m]                # get the relevant items for the option
        if kind in ["checkbox"]:
            act_value = _V[line].get()                                  # get actual value of the option
            tmp0 = f"[C{line}] {text1} ({m}); Default: {default}; " +\
                   f"actual value: {default}\n"
            tmp2 = text_wrap(tmp0, INDENT, LENGTH)                      # construct one line of the message text
            tmp += tmp2 + "\n"                                          # collect
           
##            tmp += f"[C{line}] {text1} ({m}); \n{10*BLANK}Default:" +\
##                   f"{default}; \n{10*BLANK}actual value: {default}\n"  
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO,
                 title="Description: Checkboxes")                       # show message text

# --------------------------------------------------------------------
def help3():                                                            # function help3
    """
    Shows an info text (accumulated button definitions).
    
    The function requires the "BUTTONS" tuple.

    no parameters

    no messages
    """

    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, 
    #                    help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message,
    #                    and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top
    #                    line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, 
    #                    and start improved

    tmp:str = EMPTY                                                     

    for line in range(len(BUTTONS)):                                    # loop over all elements of BUTTONS
        text, action, color = BUTTONS[line]                             # get the relevant items from BUTTONS
        tmp += f"[B{line}] {text}; color: {color}\n"                    # construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO,
                 title="Description: Buttons")                          # show message text

# --------------------------------------------------------------------
def help4():                                                            # function help4
    """
    Shows an info text (accumulated examples).
    
    The function requires the "SEQUENCE" tuple, the "EXAMPLES" and
    "OPTIONS" dictionary.

    no parameters

    no messages
    """

    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, 
    #                    help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message,
    #                    and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top
    #                    line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, 
    #                    and start improved
    
    tmp:str = EMPTY                                                     

    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]
        kind, text1, default, text2, action = OPTIONS[m]                # get the relevant items for the option
        if kind in ["text", "listbox", "list", "number"]:
            example = EXAMPLES[m]
            tmp    += f"[E{line}] {example}\n"                          # construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO,
                 title="Examples")                                      # show message text

# --------------------------------------------------------------------
def help5():                                                            # function help5 
    """
    Shows an info text (accumulated combobox definitions).
    
    The function requires the "SEQUENCE" tuple and the "OPTIONS"
    dictionary.

    no parameters

    no messages
    """
    
    # 1.9.7  2024-06-19: new: function help5 (accumulated combobox
    #                    defintions)
    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, 
    #                    help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message,
    #                    and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top
    #                    line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, 
    #                    and start improved
       
    tmp:str = EMPTY                                                    
    
    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]                                              # get the option
        kind, text1, default, text2, action = OPTIONS[m]                # get the relevant items from OPTIONS
        if kind in ["combobox"]:
            act_value = _V[line].get()                                  # get actual value of the option
            tmp += f"[CB{line}] {text1} ({m}); \n{10*BLANK}Default:" +\
                   f" {default}; \n{10*BLANK}actual value: " +\
                   f"{act_value}\n"                                     # construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO,
                 title="Description: comboboxes")                       # show message text

# --------------------------------------------------------------------
def info_version():                                                     # function info_version
    """
    Shows a version text.

    no parameters

    no messages
    """

    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, 
    #                    help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message,
    #                    and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top
    #                    line
    
    tkm.showinfo(master=mm, message=version, icon=tkm.INFO,
                 title="Version(s)")                                    # show message text

# --------------------------------------------------------------------
def init_buttons():                                                     # function init_buttons
    """
    Defines/initializes on the base of the "BUTTONS" tuple  buttons.

    The function requires the "BUTTONS" dictionary.

    no parameter

    global variable:
    + _B

    no messages
    """

    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings
    
    global _B
    
    for i in range(len(BUTTONS)):                                       # loop over all elements of BUTTONS
        text, action, color = BUTTONS[i]                                # get the relevant items from BUTTONS
        tmp = f"[B{i}] {text}"                                          # construct the text for this button
        _B[i] = tk.Button(mm, text=tmp, command=action, bg=color,
                         font=('calibri', 10))                          # define a new button
        _B[i].grid(row=3*i, column=2, rowspan=3, sticky=tk.W, padx=7)   # position the new button

# --------------------------------------------------------------------
def init_fields():                                                      # function init_fields
    """
    Defines/initializes on the base of the "OPTIONS" dictionary
    headers, labels, entry fields, checkboxes.
    The function requires the "SEQUENCE" tuple and the "OPTIONS"
    dictionary.

    no parameters

    global variables: _L, _V, _E, _C, _CB
    global variables: values, call, option_line

    no messages
    """

    # 1.9.4 2024-06-19: in init_fields: special handling of
    #                   -m deactivated
    # 1.9.5 2024-06-19: in init_fields: new settings for opion -m now by
    #                   set_value_combobox
    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings
    # 1.20   2025-12-05: better colors

    # types of fields:
    # + header:   only label with text
    # + checkbox: label with text, boolean variable, checkbox
    # + text:     label with text, string variable, text field
    # + number:   label with text, string variable, text field
    # + list:     label with text, string variable, text field
    # + listbox:  label with text, string variable, text field
    # + combobox: label with text, string variable, combobox
    
    global _L                                                           # list for ttk.Label
    global _V                                                           # list with tk variables
    global _E                                                           # list for ttk.Entry
    global _C                                                           # list for ttk.Checkbox
    global _CB                                                          # list for ttk.Combobox
    global values                                                       # dictionary: values found in menu; collected by collect_values
    global call                                                         # list: parameters for the call of CTANLoadOut.py
    global option_line                                                  # dictionary: option <--> line; set by get_option_line

    values      = {}                                                    # re-initialize values
    call        = []                                                    # re-initialize call
    option_line = {}                                                    # option <--> line; set by get_option_line

    for line in range(nr):                                              # loop over all elements of SEQUENCE
        m = SEQUENCE[line]
        kind, text1, default, text2, action = OPTIONS[m]                # get the relevant items from OPTIONS
        if kind == "header":                                            # type is header   
            _L[line] = ttk.Label(mm, text=text1, foreground=COLOR4) 
            _L[line].grid(row=line, column=0, sticky="w", columnspan=3,
                         pady=3)
        elif kind == "checkbox":                                        # type is checkbox
            tmp = f"[C{line}] {text1} ({m})"                            # text of label for checkbo
            _L[line] = ttk.Label(mm, text=tmp)                          # label creation 
            _L[line].grid(row=line, column=0, sticky="w", padx=5,
                         pady=0)                                        # label position
            _V[line] = tk.BooleanVar()                                  # boolean variable 
            _C[line] = ttk.Checkbutton(mm, variable=_V[line])           # checkbox creation
            _C[line].grid(row=line, column=1, sticky="w")               # checkbox position
            _V[line].set(str(default))                                  # variable initialization (default)
        elif kind == "text":                                            # type is text
            tmp = f"[E{line}] {text1} ({m})"
            _L[line] = ttk.Label(mm, text=tmp)
            _L[line].grid(row=line, column=0, sticky="w", padx=5,
                          pady=0)
            _V[line] = tk.StringVar()
            _E[line] = ttk.Entry(mm, textvariable=_V[line])
            _E[line].grid(row=line, column=1, sticky="w", ipadx=5)
##            _E[line].insert(10, default)
            _V[line].set(str(default))
        elif kind == "number":                                          # type is number
            tmp = f"[E{line}] {text1} ({m})"
            _L[line] = ttk.Label(mm, text=tmp)
            _L[line].grid(row=line, column=0, sticky="w", padx=5,
                          pady=0)
            _V[line] = tk.StringVar()
            _E[line] = ttk.Entry(mm, textvariable=_V[line])
            _E[line].grid(row=line, column=1, sticky="w", ipadx=5)
            _V[line].set(str(default))
        elif kind == "list":                                            # type is list
            tmp = f"[E{line}] {text1} ({m})"
            _L[line] = ttk.Label(mm, text=tmp)
            _L[line].grid(row=line, column=0, sticky="w", padx=5,
                          pady=0)
            _V[line] = tk.StringVar()
            _E[line] = ttk.Entry(mm, textvariable=_V[line])
            _E[line].grid(row=line, column=1, sticky="w", ipadx=5)
            _V[line].set(str(default))
        elif kind == "listbox":                                         # type is listbox       
            tmp = f"[E{line}] {text1} ({m})"
            _L[line] = ttk.Label(mm, text=tmp)
            _L[line].grid(row=line, column=0, sticky="w", padx=5,
                          pady=0)
            _V[line] = tk.StringVar()
            _E[line] = ttk.Entry(mm, textvariable=_V[line])
            _E[line].grid(row=line, column=1, sticky="w", ipadx=5)
            _V[line].set(str(default))
        elif kind == "combobox":                                        # type is combobox       
            tmp = f"[CB{line}] {text1} ({m})"
            _L[line] = ttk.Label(mm, text=tmp)
            _L[line].grid(row=line, column=0, sticky="w", padx=5,
                          pady=0)
            _V[line] = tk.StringVar()
            _CB[line] = ttk.Combobox(mm, textvariable=_V[line],
                         values=action, text=text2, state="readonly")
            if default in list_m:
                ind = list_m.index(default)
            _CB[line].current(ind)
            _CB[line].grid(row=line, column=1, sticky="w", ipadx=5)
 
# --------------------------------------------------------------------
def listbox_b():                                                        # function listbox_b
    # intended for the use with list boxes
    # not yet realized
    pass

# --------------------------------------------------------------------
def listbox_m():                                                        # function listbox_m
    # intended for the use with list boxes
    # not yet realized
    pass

# --------------------------------------------------------------------
def make_call():                                                        # function make_call
    """
    Generates the "call" list. The function requires the "values"
    dictionary.

    no parameters

    global variable:
    + call

    no messages
    """
    
    global call                                                         # list: parameters for the call of CTANLoadOut.py
    
    call = [sys.executable]                                             # name of the python processor
    call.append(REMOTE_PROGRAM_NAME)                                    # the actual program
    for op in values:                                                   # loop over all items of values
        val = values[op]                                                # fetch one item of values
        if val == False:                                                # the checkbox has not been clicked
            pass                                                        # do not append nothing
        elif val == True:                                               # the checkbox has been clicked
            call.append(op)                                             # append option
        else:                                                           # another kind of OPTIONS
            call.append(op)                                             # append option
            call.append(val)                                            # append cooresponding value

# --------------------------------------------------------------------
def quit():                                                             # function quit
    """
    Opens a dialogbox, whether the program should be
    terminated/finished.

    no parameters

    no messages
    """
    
    stat = tkm.askyesno(message="Should the program be terminated??",
                        title="Quit")                                   # yes/no message box
    if stat:                                                            # if the answer is "yes"
        mm.destroy()                                                    # the menu is closed

# --------------------------------------------------------------------
def set_value(option:str, val:str):                                     # function set_value
    """
    Resets the value for a option with a specified value.

    parameters:
    option : option to be set
    val    : value

    global variable:
    + _V

    The function returns None:
    + the given option is not in SEQUENCE

    no messages
    """

    # 1.8  2024-06-19: security question added to set_value
    
    # set_value ==> get_option_line_value
    
    global _V                                                           # list with tk variables
    
    if option in SEQUENCE:
        value, line, kind, default = get_option_line_value(option)      # get the line of the option
        _V[line].set(val)                                               # set the value
    else:
        return None

# --------------------------------------------------------------------
def set_value_combobox(opt:str, val:str):                               # function set_value_combobox
    """
    Resets the value for the option (-m" or "-b") with a
    specified value.

    parameters:
    opt : option to be set
    val : value

    global variable:
    + _CB

    The function returns None:
    + val ist not in list_m
    + val ist not in list_b
    + opt is not -m or -b
    + opt is not in SEQUENCE

    no messages
    """
    
    # 1.9.8 2024-06-19: new: set_value_combobox: set value for
    #                   comboboxes
    # 1.19  2025-11-30: Combobox for the handling of -m
    #                   (https://www.tutorialspoint.com/
    #                   combobox-widget-in-python-tkinter)
    
    global _CB                                                          # list with _CB entries
    
    if opt in SEQUENCE:
        if opt == "-m":                                                 # option -m
            if val in list_m:
                opt_ind = list_m.index(val)                             # get the number of val in list_m
            else:
                return None
        elif opt == "-b":                                               # option -b
            if val in list_b:
                opt_ind = list_b.index(val)                             # get the number of val in list_b
            else:
                return None
        else:
            return None
        ind = SEQUENCE.index(opt)                                       # get the line of the opti
        _CB[ind].current(opt_ind)                                       # set he value
    else:
        return None

# --------------------------------------------------------------------
def show_log():                                                         # function show_log
    """
    Shows the log file of the called subprocess.
    
    The function requires the "log" variable (text).

    no parameters

    no messages
    """

    # 1.18   2025-11-29: log output in a clickable scrolledtext-Box

    window = tk.Toplevel(mm)                                            # open new window
    window.title("Log file for menu_CTANLoadOut")                       # title of the new window

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD,
                                          width=50, height=20)          # ScrolledText widget
    text_area.pack(expand=True, fill="both")

    message = "Log file of the menu_CTANLoadOut program:\n\n"           # add a title to the log variable
    message += changes + log
    text_area.insert(tk.END, message)                                   # output the message

# --------------------------------------------------------------------
def start():                                                            # function start
    """
    Prepares the processing. The function requires the "OPTIONS"
    dictionary.

    no parameters.

    global variable:
    + call

    no messages
    """

    # 1.11  2024-07-08: as far as possible and useful: string 
    #                   interpolation via .format replaced by f-strings
    # 1.13  2024-07-08: output in help1, help2, help3, help4, help5, and
    #                   start improved
    # 1.16   2025-10-14: changes in Start-Box
    # 1.16.1 2025-10-14: a prompt before the actual execution
    # 1.16.1 2025-10-14: Start-Box simplified 
    # 2.2    2026-04-13 formatting of collected texts
    # 2.2.3  2026-04-13 text_wraöp used in start, help1 und help2

    # start ==> get_option_line
    #       ==> check_values
    #       ==> collect_values
    #       ==> make_call
    #       ==> start_call

    global call                                                         # list: parameters for the call of CTANLoadOut.py
    
    get_option_line()                                                   # preparation: option <--> line
    check_values()                                                      # check all possible values 
    collect_values()                                                    # collect all Useful OPTIONS with values
    make_call()                                                         # construct the call
    
    msg = "The following OPTIONS were determined.\nShould " +\
          "processing be started using the current values?\n\n"

    tmp = call[2:]
    INDENT  = 2                                                         # indentation of wrapped texts
    LENGTH  = 55                                                        # max. length of wrapped texts

    for f in range(len(tmp)):                                           # construct message text
        tmp_f = tmp[f]
        if tmp_f in ["-c", "-f", "-l", "-mo", "-mt", "-nf", "-p", "-r",
                     "-s", "-stat", "-v"]:
            tmp0 = f"{tmp_f} -- {OPTIONS[tmp_f][1]})"
##            msg += f"{tmp_f}  --  \n{10*BLANK}({OPTIONS[tmp_f][1]})\n"
            tmp2 = text_wrap(tmp0, INDENT, LENGTH)                      # construct one line of the message text
            msg += tmp2 + "\n"                                          # collect
        elif tmp_f == EMPTY:
            continue
        elif tmp_f[0] == "-":
            tmp0 = f"{tmp_f} {tmp[f+1]} -- ({OPTIONS[tmp_f][1]})"
            tmp2 = text_wrap(tmp0, INDENT, LENGTH)                      # construct one line of the message text
            msg += tmp2 + "\n"                                          # collect
##            msg += f"{tmp_f}  {tmp[f+1]}  --  " +\
##                   f" \n{10*BLANK}({OPTIONS[tmp_f][1]})\n"
        else:
            pass
    
    stat = tkm.askyesno(title="Start", message=msg)                     # message with question
    if stat:                                                            # if OK ==> start_call
        start_call()

# --------------------------------------------------------------------
def start_call():                                                       # function start_call
    """
    Starts the processing.

    The function requires the "call" list.

    no parameters

    no messages
    """

    # 1.11   2024-07-08: as far as possible and useful: string 
    #                    interpolation via .format replaced by f-strings

    global log                                                          # to be used for log data

    log = EMPTY
    
    try:                                                                # start the subprocess in a try/except constrauct
        with TemporaryFile("r+", encoding="utf-8",
                           errors="ignore") as f:                       # temporary file
            process_load = subprocess.run(call, check=True,
                              timeout=TIMEOUT, encoding="utf-8",
                              stdout=f, stderr=subprocess.PIPE,
                              universal_newlines=True)
            f.seek(0)                                                   # rewind file
            for line in f.readlines():                                  # line by line
                log += line 
            load_errormessage = process_load.stderr                     # possible error message
            if len(load_errormessage) > 0:
                print(load_errormessage)
    except subprocess.CalledProcessError as exc:                        # process error
        print(f"[CTANLoadOut] Error: called process '{call[1]}' " +\
              "not found,", sys.exc_info()[0])
        sys.exit("[CTANLoadOut] Error: program terminated")             # program terminated    
    except FileNotFoundError as exc:                                    # file not found
        print(f"[CTANLoadOut] Error: file '{call[0]}' not found", exc)
        sys.exit("[CTANLoadOut] Error: program terminated")             # program terminated
    except subprocess.TimeoutExpired as exc:                            # timeout
        print("[CTANLoadOut] Error: timeout error", TIMEOUT)
        sys.exit("[CTANLoadOut] Error: program terminated")             # program terminated
    except KeyboardInterrupt as exc:                                    # keyboard interrupt
        print("[CTANLoadOut] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut] Error: program terminated")             # program terminated
    except UnicodeDecodeError as exc:                                   # unicode decode error
        print("[CTANLoadOut] Error: unicode decode error", exc)
        sys.exit("[CTANLoadOut] Error: program terminated")             # program terminated
    except:                                                             # any unspecified error
        print("[CTANLoadOut] Error: any unspecified error",
              sys.exc_info())
        sys.exit("[CTANLoadOut] Error: program terminated")             # program terminated

    tkm.showinfo(mm,
                 message="Finished!\n\nFor more informations read " +\
                 "the log file.", icon=tkm.INFO)

# --------------------------------------------------------------------
def text_wrap(text:str, ident:int=5, length:int=30) ->str:              # function text_wrap
    """
    auxiliary function: Wrapes a given text.

    parameters:
    text   : text to be wrapped (str)
    indent : indentation of the 2nd and all following lines (int); default: 5
    length : maximal length of lines (int); default: 30

    It returns a wrapped text.

    no messages
    """
    
    # 2.2    2026-04-13 formatting of collected texts
    # 2.2.2  2026-04-13 new function text_wrap

    tmp = BLANK * ident
    return ('\n' + tmp).join(textwrap.wrap(text, length))


# ====================================================================
# Lists, tuples, dictionaries
# --------------------------------------------------------------------
# Currently not used; intended for working with list boxes

list_m   = ["LaTeX", "RIS", "plain", "BibLaTeX", "Excel"]               # possible values for -m
list_b   = ["@online", "@software", "@misc", "@ctan", "@www"]           # possible values for -b

# --------------------------------------------------------------------
# tuple "SEQUENCE":
# defines the sequence of menu rows (on the base of CTANLoad /
# CTAMOut options) will be used in clear_fields, collect_values,
# collect_values, get_option_line, get_value, help1, help2, help4,
# help5, init_fields

# h1, h2, h3, h4, h5 for headers

SEQUENCE = ("h1", "-o", "-d", "-tout", "-stat", "-v", "-mo",
            "h2", "-t", "-A", "-k", "-L", "-y",
            "h3", "-tl", "-Al", "-kl", "-Ll", "-yl", "-n", "-f",
            "h4", "-to", "-Ao", "-ko", "-Lo", "-yo", "-m", "-b", "-sb",
            "-s", "-mt", "-nf", "h5", "-p", "-c", "-l", "-r")

# --------------------------------------------------------------------
# dictionary "OPTIONS":
# defines the look of menu items; on the base of CTANLoad /
# CTAMOut options will be used in clear_fields, collect_values,
# get_option_line_value, get_value, help1, help2, help4, init_fields,
# start

# + each element is a tuple with 5 components:
#   (0) type of row in the menu: header, text, number, checkbox,
#       listbox, list
#   (1) text in the label
#   (2) default (found in CTANLoadOut)
#   (3) text of the combobox 
#   (4) action associated with the combobox


# 1.2   2024-05-02: default for -b changed to "@online"
# 1.5   2024-06-11: some texts changed in OPTIONS
# 1.6   2024-06-17: some texts changed in OPTIONS
# 1.9.3 2024-06-19: option -m in OPTIONS dictionary: new type combobox,
#                   new action
# 1.15  2025-10-02: -d adapt to different operating systems
# 1.19  2025-11-30: Combobox for the handling of -m
#                   (https://www.tutorialspoint.com/
#                   combobox-widget-in-python-tkinter)

OPTIONS = {
    "h1"   : ("header",                                                 # header                      
              "Global options",
              None,
              None,
              None),
    "-o"   : ("text",                                                   # -o
              "[CTANLoad+CTANOut] Generic name for output files" +\
              "[without extensions]",
              OUTPUT_NAME_DEFAULT,
              None,
              None),
    "-d"   : ("text",                                                   # -d
              "[CTANLoad+CTANOut] OS folder (directory) for input" +\
              " and output files",
              act_dir,
              None,
              None),
    "-tout": ("number",                                                 # -tout
              "[CTANLoadOut] default timeout (sec) for subprocesses ",
              TIMEOUT_DEFAULT,
              None,
              None),
    "-stat": ("checkbox",                                               # -stat
              "[CTANLoad+CTANOut] Flag: statistics on terminal",
              STATISTICS_DEFAULT,
              None,
              None),
    "-v"   : ("checkbox",                                               # -v
              "[CTANLoad+CTANOut] Flag: Output is verbose",
              VERBOSE_DEFAULT,
              None,
              None),
    "-mo"  : ("checkbox",                                               # -mo
              "[CTANLoadOut] Flag: Do not activate CTANLoad",
              False,
              None,
              None),

    "h2"   : ("header",                                                 # header
              "Options for CTANLoad and CTANOut",
              None,
              None,
              None),
    "-A"   : ("text",                                                   # -A
              "[CTANLoad+CTANOut] Name template for authors",
              AUTHOR_TEMPLATE_DEFAULT,
              None,
              None),
    "-L"   : ("text",                                                   # -L
              "[CTANLoad+CTANOut] Name template for licenses",
              LICENSE_TEMPLATE_DEFAULT,
              None,
              None),
    "-k"   : ("text",                                                   # -k
              "[CTANLoad+CTANOut] Template for keys",
              KEY_TEMPLATE_DEFAULT,
              None,
              None),
    "-t"   : ("text",                                                   # -t
              "[CTANLoad+CTANOut] Template for package names",
              NAME_TEMPLATE_DEFAULT,
              None,
              None),
    "-y"   : ("text",                                                   # -y
              "[CTANLoad+CTANOut] Template for years",
              YEAR_TEMPLATE_DEFAULT,
              None,
              None),

    "h3"   : ("header",                                                 # header
              "Options for CTANLoad",
              None,
              None,
              None),
    "-Ll"  : ("text",                                                   # -Ll
              "[CTANLoad] Name template for licenses",
              LICENSE_LOAD_TEMPLATE_DEFAULT,
              None,
              None),
    "-kl"  : ("text",                                                   # -kl
              "[CTANLoad] Template for keys",
              KEY_LOAD_TEMPLATE_DEFAULT,
              None,
              None),
    "-tl"  : ("text",                                                   # -tl
              "[CTANLoad] Template for package names",
              NAME_LOAD_TEMPLATE_DEFAULT,
              None,
              None),
    "-yl"  : ("text",                                                   # -yl
              "[CTANLoad] Template for years",
              YEAR_LOAD_TEMPLATE_DEFAULT,
              None,
              None),
    "-Al"  : ("text",                                                   # -Al
              "[CTANLoad} Name template for authors",
              AUTHOR_LOAD_TEMPLATE_DEFAULT,
              None,
              None),
    "-n"   : ("number",                                                 # -n
              "[CTANLoad] Maximum number of XML and PDF file downloads",
              NUMBER_DEFAULT,
              None,
              None),
    "-f"   : ("checkbox",                                               # -f
              "[CTANLoad] Flag: Download associated documentation " +\
              "files [PDF]",
              DOWNLOAD_DEFAULT,
              None,
              None),

    "h4"   : ("header",                                                 # header
              "Options for CTANOut",
              None,
              None,
              None),
    "-Lo"  : ("text",                                                   # -Lo
              "[CTANOut] Name template for licenses",
              LICENSE_OUT_TEMPLATE_DEFAULT,
              None,
              None),
    "-ko"  : ("text",                                                   # -ko
              "[CTANOut] Template for keys",
              KEY_OUT_TEMPLATE_DEFAULT,
              None,
              None),
    "-to"  : ("text",                                                   # -to
              "[CTANOut] Template for package names",
              NAME_OUT_TEMPLATE_DEFAULT,
              None,
              None),
    "-yo"  : ("text",                                                   # -yo
              "[CTANOut] Template for years",
              YEAR_OUT_TEMPLATE_DEFAULT,
              None,
              None),
    "-Ao"  : ("text",                                                   # -Ao
              "[CTANOut} Name template for authors",
              AUTHOR_OUT_TEMPLATE_DEFAULT,
              None,
              None),
    "-m"   : ("combobox",                                               # -m
              "[CTANOut} Target format",
              MODE_DEFAULT,
              "…search",
              list_m),
    "-b"   : ("listbox",                                                # -b
              "[CTANOut} Type of BibLaTex entries to be generated",
              BTYPE_DEFAULT,
              None,
              None),
    "-sb"  : ("list",                                                   # -sb
              "[CTANOut} Skip specified BibLaTeX fields",
              SKIP_BIBLATEX_DEFAULT,
              None,
              None),
    "-s"   : ("list",                                                   # -s
              "[CTANOut} Skip specified CTAN fields",
              SKIP_DEFAULT,
              None,
              None),
    "-mt"  : ("checkbox",                                               # -mt
              "[CTANOut} Flag: Generate topic lists ",
              MAKE_OUTPUT_DEFAULT,
              None,
              None),
    "-nf"  : ("checkbox",                                               # -nf
              "[CTANOut} Flag: Do not generate output files",
              NO_FILES_DEFAULT,
              None,
              None),

    "h5"   : ("header",                                                 # header
              "Options for special actions",
              None,
              None,
              None),
    "-p"   : ("checkbox",                                               # -p
              "[CTANOut} Flag: Generate PDF output",
              PDF_OUTPUT_DEFAULT,
              None,
              None),
    "-c"   : ("checkbox",                                               # -c 
              "[CTANLoad} Flag: Check the integrity of the " + \
              "2nd .pkl file",
              INTEGRITY_DEFAULT,
              None,
              None),
    "-l"   : ("checkbox",                                               # -l
              "[CTANLoad} Flag: Generate some special lists and" +\
              " prepare files for CTANOut",
              LISTS_DEFAULT,
              None,
              None),
    "-r"   : ("checkbox",                                               # -r
              "[CTANLoad} Flag: Regenerate the two pickle files",
              REGENERATE_DEFAULT,
              None,
              None),
}

# --------------------------------------------------------------------
# tuple "BUTTONS" (definitions):
# will be used in help3, init_buttons

# each entry:
# (1) title
# (2) action/command
# (3) color

# 1.3   2024-06-06: color of the "Log file" button changed
# 1.9.1 2024-06-19: new in BUTTONS tuple: function help5
# 1.10  2024-07-08: some texts in BUTTONS changed
# 1.20  2025-12-05: better colors

BUTTONS = (
    ("Start",                     start,        COLOR1),
    ("Reset fields",              init_fields,  COLOR1),
    ("Clear menu",                clear_fields, COLOR1),
    ("Close menu (Quit)",         quit,         COLOR1),
    ("Description: Entries",      help1,        COLOR2),
    ("Description: Checkboxes",   help2,        COLOR2),
    ("Description: Buttons",      help3,        COLOR2),
    ("Description: Comboboxes",   help5,        COLOR2),
    ("Examples: Entries",         help4,        COLOR2),
    ("Version",                   info_version, COLOR2),
    ("Log file",                  show_log,     COLOR3),
    )

# --------------------------------------------------------------------
# dictionary "EXAMPLES":
# will be used in help4

EXAMPLES = {
    "-A"   : "author template (according to the rules of a regular" +\
             " expression); see authors.xml\n          for example: " +\
             "Mittelbach",
    "-Al"  : "author template (according to the rules of a regular" +\
             " expression); see authors.xml\n          for " +\
             "example:  Voß",
    "-Ao"  : "author template (according to the rules of a regular" +\
             " expression); see authors.xml\n          for example:" +\
             " Mittelbach|Voß",
    "-b"   : "one of @online, @software, @misc, @ctan, @www" +\
             " \n          for example:  @online",
    "-c"   : "flag: without any value",
    "-d"   : "corect directory name\n          for example:  .\\result",
    "-f"   : "flag: without any value",
    "-k"   : "key template (according to the rules of a regular " +\
             "expression); see topics.xml\n          for example:  font",
    "-kl"  : "key template (according to the rules of a regular " +\
             "expression); see topics.xml\n          for " +\
             "example:  graphics",
    "-ko"  : "key template (according to the rules of a regular " +\
             "expression); see topics.xml\n          for example:  " +\
             "german|french",
    "-L"   : "license template (according to the rules of a regular" +\
             " expression); see licenses.xml\n          for " +\
             "example:  gpl",
    "-l"   : "flag: without any value",
    "-Ll"  : "license template (according to the rules of a regular" +\
             " expression); see licenses.xml\n          for " +\
             "example:  cc-by-nd",
    "-Lo"  : "license template (according to the rules of a regular" +\
             " expression); see licenses.xml" +\
             "\n          for example:  lppl|gpl",
    "-m"   : "one of LaTeX, latex, tex, RIS, ris, plain, txt, " +\
             "BibLaTeX, biblatex, bib, Excel, excel\n          for " +\
             "example:  LaTeX",
    "-mo"  : "flag: without any value",
    "-mt"  : "flag: without any value",
    "-n"   : "positive integer number\n          for example:  500",
    "-nf"  : "flag: without any value",
    "-o"   : "correct file name (without extension)" +\
             "\n          for example:  extract",
    "-p"   : "flag: without any value",
    "-r"   : "flag: without any value",
    "-s"   : "list with CTAN fields; correct names can be found in" +\
             " CTAN-elements.txt" +\
             "\n          for example:  [description, documentation]",
    "-sb"  : "list with BibLaTeX fields; correct names can " +\
             "be found in CTANOut_mapping_bib.txt" +\
             "\n          for example:  [abstract, related, note]",
    "-stat": "flag: without any value",
    "-t"   : "package template (according to the rules of a regular" +\
             " expression); see packages.xml" +\
             "\n          for example:  biblatex|bibtex",
    "-tl"  : "package template (according to the rules of a regular" +\
             " expression); see packages.xml\n          for example:  ",
    "-to"  : "package template (according to the rules of a regular" + \
             " expression); see packages.xml\n          for example: ",
    "-tout": "positive integer number\n          for example:  50",
    "-v"   : "flag: without any value",
    "-y"   : "year template (according to the rules of a regular" +\
             " expression)\n for example:  2024|2023",
    "-yl"  : "year template (according to the rules of a regular " +\
             "expression)\n          for example:  20[0-2][0-9]",
    "-yo"  : "year template (according to the rules of a regular " +\
             "expression)\n          for example:  20[0-2][0-9]",
    }

# --------------------------------------------------------------------
# Initializations of some lists:

# 1.9.2 2024-06-19: new: list _CB defined and initialized

# _V : tkinter variables
# _E : tkinter entry fields
# _L : tkinter labels
# _C : tkinter checkboxes
# _B : tkinter buttons
# _CB: tkinter comboboxes

nr = len(SEQUENCE)                                                      # number of elements in SEQUENCE
_E  = [None for f in range(nr)]                                         # list for ttk.Entry
_L  = [None for f in range(nr)]                                         # list for ttk.Label
_V  = [None for f in range(nr)]                                         # list for tk variables
_C  = [None for f in range(nr)]                                         # list for ttk.Checkbox
_CB = [None for f in range(nr)]                                         # list for ttk Combobox
_B  = [None for f in range(len(BUTTONS))]                               # list for tk.Button


# ====================================================================
# main part

# main part ==> init_fields
#           ==> init buttons
#           ==> mm.mainloop

# the menu will be started by a click on the "start" button

init_fields()                                                           # preparation: initialization of fields
init_buttons()                                                          # preparation: initialization of BUTTONS
mm.mainloop()                                                           # main loop


# ====================================================================
# Change history
# --------------
# 0.9    2024-05-09: first working version
# 1.0    2024-05-28: first fully functional version
# 1.1    2024-05-30: in check_value: Errors corrected and inconsistencies eliminated
# 1.2    2024-05-02: default for -b changed to "@online"
# 1.3    2024-06-06: color of the "Log file" button changed
# 1.4    2024-06-11: additional values for -m: tsv, csv
# 1.5    2024-06-11: some texts changed in options
# 1.6    2024-06-17: some texts changed in options
# 1.7    2024-06-18: small error in help2 corrected
# 1.8    2024-06-19: security question added to set_value

# 1.9    2024-06-19: handling of option -m changed for combobox
# 1.9.1  2024-06-19: new in BUTTONS tuple: function help5
# 1.9.2  2024-06-19: new: list _CB defined and initialized
# 1.9.3  2024-06-19: option -m in options dictionary: new type combobox, new action
# 1.9.4  2024-06-19: in init_fields: special handling of -m deactivated
# 1.9.5  2024-06-19: in init_fields: new settings for option -m now by set_value_combobox
# 1.9.6  2024-06-19: clear_fields, collect_values, get_default, get_option_line_value, get_value: extended for type combobox
# 1.9.7  2024-06-19: new: function help5 (accumulated combobox defintions)
# 1.9.8  2024-06-19: new: set_value_combobox: set value for comboboxes
# 1.9.9  2024-06-19: former special handling of -m deactivated + resettings of -m now by set_value_combobox

# 1.10   2024-07-08: some texts in BUTTONS changed
# 1.11   2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings

# 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
# 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
# 1.12.2 2024-07-08: messagetexts now without any additional top line

# 1.13   2024-07-08: output in help1, help2, help3, help4, help5, and start improved
# 1.14   2025-02-06: everywhere: all source code lines wrapped at a maximum of 80 characters
# 1.15   2025-10-02: -d adapted to different operating systems

# 1.16   2025-10-14: changes in Start-Box
# 1.16.1 2025-10-14: a prompt before the actual execution
# 1.16.1 2025-10-14: Start-Box simplified 

# 1.17   2025-11-18: changes in check_values
# 1.17.1 2025-11-18: for certain changes made by check_values: warnings are issued
# 1.17.2 2025-11-18: check_values cleaned up 
# 1.17.3 2025-11-18: "Short circuits" removed

# 1.18   2025-11-29: log output in a clickable scrolledtext-Box
# 1.19   2025-11-30: Combobox for the handling of -m (https://www.tutorialspoint.com/combobox-widget-in-python-tkinter)
# 1.20   2025-12-05: better colors

# 2.0    2026-04-01 Complete revision (too many changes to list in the code)
# 2.0.1  2026-04-01 Functions with type annotations
# 2.0.2  2026-04-01 Variable annotations (where appropriate and possible)
# 2.0.3  2026-04-01 Constants in uppercase
# 2.0.4  2026-04-01 .format replaced with f-strings (where appropriate)
# 2.0.5  2026-04-01 __doc__ texts supplemented and standardised
# 2.0.6  2026-04-01 Standardised: Code up to a maximum of column 71
# 2.0.7  2026-04-01 Standardised: Comments from column 72 onwards

# 2.1    2026-04-10 date and version of CTANLoad, CTANOut und CTANLoadOut via Import

# 2.2    2026-04-13 formatting of collected texts
# 2.2.1  2026-04-13 import textwrap
# 2.2.2  2026-04-13 new function text_wrap
# 2.2.3  2026-04-13 text_wrap used in start, help1 und help2


# ====================================================================
# + Änderungen an Optionswerten einfacher machen; z.B. set_value("-m") (x)
# + alte werte werden verwendet bei mehrfachen Aufrufen des Menüs (x)
# + Warnings sparsamer einsetzen (x)
# + wie sieht es mit -nf oder -mo aus? (x)
# + überprüfen: -m != LaTeX (x)

# Wünsche/Fehler
# --------------
# + besseres Konzept für BUTTONS und tk.Buttons
# + vielleicht mit zusätzlichen Spalten: Typ und Text (ggf. per Funktion)
# + make_call mit return (-) 
# + Mono-Font an manchen Stellen (geht nicht)
# + Zuordnung Option <--> Zeile global festlegen (-)
# + Funktionen entsprechend umbauen (-)
# + vielleicht deshalb neue Tabelle; option: zeile, wert, default (-)
# + askyesno mit englichen Texten (- geht nicht einfach)
# + muss log global sein? (ja)
# + messagebox verbreitern (geht nichtdirekt; vielleicht aber mit Message?)
# + in start_call: print-Anweisungen an log anhängen 
# + Combobox für -b (https://www.tutorialspoint.com/combobox-widget-in-python-tkinter) funktioniert nicht
# + Forschrittsanzeige (https://www.tutorialspoint.com/progressbar-widget-in-python-tkinter)?
# + Antwortboxen auf englisch
# + Parameter an SupProzess mittels Bytes?
