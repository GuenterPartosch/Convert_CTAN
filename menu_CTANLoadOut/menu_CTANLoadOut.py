#!/usr/bin/python3
# -*- coding: utf-8 -*-
# please adjust these two lines if necessary

# menu_CTANLoadOut.py
# (C) Günter Partosch 2024

# --------------------------------------------------------------------
# The program menu_CTANLoadOut.py needs the following Python programs:
# menu_CTANLoadOut.py ==> CTANLoadOut.py
# CTANLoadOut.py      ==> CTANLoad.py
#                     ==> CTANOut.py

# The program essentially uses the tkinter module and its submodules:
# + tkinter as tk
# + tkinter.ttk as ttk
# + tkinter.messagebox as tkm
# + tkinter.scrolledtext

# In particular, the following functions/methods are used:
#
# scrolledtext.ScrolledText
#
# tk.BooleanVar
# tk.Button
# tk.END
# tk.StringVar
# tk.Tk
# tk.Toplevel
# tk.W
#
# tkm.INFO
# tkm.askyesno
# tkm.showinfo
# ttk.Checkbutton
# ttk.Combobox
# ttk.Button
# ttk.Entry
# ttk.Label
#
# xyz.get
# xyz.grid
# xyz.insert
# xyz.mainloop
# xyz.pack
# xyz.set
# xyz.title
# xyz.current


# ====================================================================
# Change history
# --------------
# 0.9   2024-05-09: first working version
# 1.0   2024-05-28: first fully functional version
# 1.1   2024-05-30: in check_value: Errors corrected and inconsistencies eliminated
# 1.2   2024-05-02: default for -b changed to "@online"
# 1.3   2024-06-06: color of the "Log file" button changed
# 1.4   2024-06-11: additional values for -m: tsv, csv
# 1.5   2024-06-11: some texts changed in options
# 1.6   2024-06-17: some texts changed in options
# 1.7   2024-06-18: small error in help2 corrected
# 1.8   2024-06-19: security question added to set_value
# 1.9   2024-06-19: handling of option -m changed for combobox
# 1.9.1 2024-06-19: new in buttons tuple: function help5
# 1.9.2 2024-06-19: new: list CB defined and initialized
# 1.9.3 2024-06-19: option -m in options dictionary: new type combobox, new action
# 1.9.4 2024-06-19: in init_fields: special handling of -m deactivated
# 1.9.5 2024-06-19: in init_fields: new settings for option -m now by set_value_combobox
# 1.9.6 2024-06-19: clear_fields, collect_values, get_default, get_option_line_value, get_value: extended for type combobox
# 1.9.7 2024-06-19: new: function help5 (accumulated combobox defintions)
# 1.9.8 2024-06-19: new: set_value_combobox: set value for comboboxes
# 1.9.9 2024-06-19: former special handling of -m deactivated + resettings of -m now by set_value_combobox
# 1.10  2024-07-08: some texts in buttons changed
# 1.11  2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
# 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
# 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
# 1.12.2 2024-07-08: messagetexts now without any additional top line
# 1.13   2024-07-08: output in help1, help2, help3, help4, help5, and start  improved


# ====================================================================
# some imports

import tkinter as tk                                                  # basis for the most things
import tkinter.ttk as ttk                                             # an alternative
import tkinter.messagebox as tkm                                      # message output
from tkinter import scrolledtext                                      # show scrollable text
import sys                                                            # system calls
import platform                                                       # OS informations
import subprocess                                                     # handling of sub-processes
from tempfile import TemporaryFile                                    # temporary file for subprocess.run

# --------------------------------------------------------------------
# some settings

# 1.11  2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings

mm = tk.Tk()                                                          # start of menu
mm.title("Menu for CTANLoadOut (a combination of CTANLoad + CTANOut)")# title of menu

empty                    = ""
blank                    = " "
values                   = {}                                         # values found in menu; collected by collect_values
option_line              = {}                                         # option <--> line; set by get_option_line
call                     = []                                         # parameters for the call of CTANLoadOut.py
nr                       = 0                                          # number of elements in sequence; will be set later
log                      = empty                                      # to be used for log data

menu_CTANLoadOut_date    = "2024-07-08"                               # menu_CTANLoadOut.py
menu_CTANLoadOut_version = "1.13"
CTANLoadOut_date         = "2024-07-20"                               # CTANLoadOut.py
CTANLoadOut_version      = "1.55.3"
CTANLoad_date            = "2024-07-26"                               # CTANLoad.py
CTANLoad_version         = "2.44.3"
CTANOut_date             = "2024-07-26"                               # CTANOut.py
CTANOut_version          = "2.63.3"

program_name             = "menu_CTANLoadOut.py"                      # name of the program 
author_program           = "Günter Partosch"
author_email             = "Guenter.Partosch@web.de \n(formerly Guenter.Partosch@hrz.uni-giessen.de)"
author_inst              = "formerly Justus-Liebig-Universität, Hochschulrechenzentrum"
operatingsys             = platform.system()                          # operating system on which the program runs
remote_program_name      = "CTANLoadOut.py"                           # program to be processed

warn_text                = "+ '{0}' '{1}' changed to '{2}' (due to given {3})\n"
                                                                      # template for warning texts
timeout10                = 1000                                       # timeout (in sec) for the main subprocess

if operatingsys == "Windows":                                         # the directory separator depends on the OS
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
+ Menu_CTANLoadOut.py ({menu_CTANLoadOut_date}, version {menu_CTANLoadOut_version})
+ CTANLoadOut.py      ({CTANLoadOut_date}, version {CTANLoadOut_version})
+ CTANLoad.py         ({CTANLoad_date}, version {CTANLoad_version})
+ CTANOut.py          ({CTANOut_date}, version {CTANOut_version})

{author_program}; E-Mail: {author_email}
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

# --------------------------------------------------------------------
def check_values():                                                   # check_values: Checks some option values and resets some.
    """Checks some option values and resets some.
    This is to avoid collisions and contradictions between the options.

    no parameters

    global variable: V
    """
    
    # 1.1   2024-05-30: in check_value: Errors corrected and inconsistencies eliminated
    # 1.4   2024-06-11: additional values for -m: tsv, csv
    # 1.9.9 2024-06-19: former special handling of -m deactivated + resettings of -m now by set_value_combobox


    # check_value ==> get_value
    #             ==> get_option_line_value
    #             ==> get_default
    #             ==> set_value_combobox

    # (1)  check -m
    # (2)  ckeck -b 
    # (3)  check -A, -L, -t, -k, -y
    # (3a) check -A 
    # (3b) check -L 
    # (3c) check -t 
    # (3d) check -k
    # (3e) check -y
    # (4)  check -nf
    # (5)  check -b
    # (6)  check -sb
    # (7)  check -p
    # (8)  check -mt
    # (9)  check -mo
    
    global V                                                          # -- list with tk variables

    message_text = empty                                              # -- initialize message text
    changed      = set()                                              # -- collect changed values to prevent collissions

    # (1) check -m (one of LaTeX,latex,tex,RIS,ris,plain,txt,BibLaTeX,biblatex,bib,Excel,excel,csv,tsv)
    
##    value, line, kind, default = get_option_line_value("-m")          
##    if value in ["LaTeX", "RIS", "plain", "BibLaTeX", "Excel"]:       # -- LaTeX, RIS, plain, BibLaTeX, Excel
##        pass
##    elif value in ["latex", "tex"]:                                   # -- latex, tex
##        message_text += warn_text.format("-m", value, "LaTeX", "-m (1)")
##        V[line].set("LaTeX")                                          
##    elif value == "ris":                                              # -- ris
##        message_text += warn_text.format("-m", value, "RIS", "-m (1)")
##        V[line].set("RIS")                                           
##    elif value == "txt":                                              # -- txt
##        message_text += warn_text.format("-m", value, "plain", "-m (1)")
##        V[line].set("plain")
##    elif value in ["biblatex", "bib"]:                                # -- biblatex, bib
##        message_text += warn_text.format("-m", value, "BibLaTeX", "-m (1)")
##        V[line].set("BibLaTeX")
##    elif value in  ["excel", "csv", "tsv"]:                           # -- excel, tsv, csv
##        message_text += warn_text.format("-m", value, "Excel", "-m (1)")
##        V[line].set("Excel")
##    else:
##        message_text += warn_text.format("-m", value, "RIS", "-m (1)")
##        V[line].set("RIS")                                            # -- set default

    # (2) ckeck -b (one of @online,@software,@misc,@ctan,@www         # -- option -b
    
    value, line, kind, default = get_option_line_value("-b")
    if value in ["@online", "@software", "@misc", "@ctan", "@www", empty]:
        pass
    else:                                                             # -- reset -b
        message_text += warn_text.format("-b", value, "@online", "-b (2)")
        V[line].set("@online")

    # (3) check -A, -L, -t, -k, -y
    
    # (3a) check -A                                                   # -- option -A
    # -A ==> -Al ...
    #    ==> -Ao ...
    value, line, kind, default = get_option_line_value("-A")
    if value != default:
        value_Al = get_value("-Al")
        value_Ao = get_value("-Ao")
        if value_Al != value:                                         # -- reset -Al
            message_text += warn_text.format("-Al", value_Al, value, "-A (3a)")
            set_value("-Al", value)
        if value_Ao != value:                                         # -- reset -Ao
            message_text += warn_text.format("-Ao", value_Ao, value, "-A (3a)")
            set_value("-Ao", value)
    
    # (3b) check -L                                                   # -- option -L
    # -L ==> -Ll ...
    #    ==> -Lo ...
    value, line, kind, default = get_option_line_value("-L")
    if value != default:
        value_Ll = get_value("-Ll")
        value_Lo = get_value("-Lo")
        if value_Ll != value:                                         # -- reset -Ll
            message_text += warn_text.format("-Ll", value_Ll, value, "-L (3b)")
            set_value("-Ll", value)
        if value_Lo != value:                                         # -- reset -Lo
            message_text += warn_text.format("-Lo", value_Lo, value, "-L (3b)")
            set_value("-Lo", value)
    
    # (3c) check -t                                                   # -- option -t
    # -t ==> -tl ...
    #    ==> -to ...
    value, line, kind, default = get_option_line_value("-t")
    if value != default:
        value_tl = get_value("-tl")
        value_to = get_value("-to")
        if value_tl != value:                                         # -- reset -tl
            message_text += warn_text.format("-tl", value_tl, value, "-t (3c)")
            set_value("-tl", value)
        if value_to != value:                                         # -- reset -to
            message_text += warn_text.format("-to", value_to, value, "-t (3c)")
            set_value("-to", value)
    
    # (3d) check -k                                                   # -- option -k
    # -k ==> -kl ...
    #    ==> -ko ...
    value, line, kind, default = get_option_line_value("-k")
    if value != default:
        value_kl = get_value("-kl")
        value_ko = get_value("-ko")
        if value_kl != value:                                         # -- reset -kl
            message_text += warn_text.format("-kl", value_kl, value, "-k (3d)")
            set_value("-kl", value)
        if value_ko != value:                                         # -- reset -ko
            message_text += warn_text.format("-ko", value_ko, value, "-k (3d)")
            set_value("-ko", value)

    # (3e) check -y                                                   # -- option -y
    # -y ==> -yl ...
    #    ==> -yo ...
    value, line, kind, default = get_option_line_value("-y")
    if value != default:
        value_yl = get_value("-yl")
        value_yo = get_value("-yo")
        if value_yl != value:                                         # -- reset -yl
            message_text += warn_text.format("-yl", value_yl, value, "-y (3e)")
            set_value("-yo", value)
        if value_yo != value:                                         # -- reset -yo
            message_text += warn_text.format("-yo", value_yo, value, "-y (3e)")
            set_value("-yo", value)

    # To prevent inconsistencies for the following option, there are certain priorities:
    # -nf > -b|-sb > p > mt
    
    # (4) check -nf                                                   # -- option -nf
    # -nf ==> -mt False
    #     ==> -p False
    #     ==> -f False
    value_nf = get_value("-nf")
    value_mt = get_value("-mt")
    value_p  = get_value("-p")
    value_f  = get_value("-f")

    if value_nf and value_mt:                                         # -- reset -mt
        changed.add("-mt")
        message_text += warn_text.format("-mt", value_mt, False, "-nf (4)")
        set_value("-mt", False)
    if value_nf and value_p:                                          # -- reset -p
        changed.add("-p")
        message_text += warn_text.format("-p", value_p, False, "-nf (4)")
        set_value("-p", False)
    if value_nf and value_f:                                          # -- reset -f
        changed.add("-f")
        message_text += warn_text.format("-f", value_f, False, "-nf (4)")
        set_value("-f", False)

    # (5+6) check -b | -sb                                            # -- option -b | -sb
    # -b  ==> -m BibLaTeX 
    #     ==> -mt False
    #     ==> -p False
    # -sb ==> -p False
    #     ==> -mt False
    #     ==> -m BibLateX
    if (not ("-b" in changed)) or (not ("-sb" in changed)):
        value_b  = get_value("-b");  default_b  = get_default("-b")
        value_sb = get_value("-sb"); default_sb = get_default("-sb")
        value_m  = get_value("-m")
        value_mt = get_value("-mt")
        value_p  = get_value("-p")

        a = value_b != default_b
        b = value_sb != default_sb
        c = value_m != "BibLaTeX"
        d = value_mt
        e = value_p

        if (a or b) and c:                                            # -- reset -m
            changed.add("-m")
            message_text += warn_text.format("-m", value_m, "BibLaTeX", "-b|-sb (5+6)")
            set_value_combobox("-m", "BibLaTeX")                      # -- set value for the combobox
            set_value("-m", "BibLaTeX")
        if (a or b) and d:                                            # -- reset -mt
            changed.add("-mt")
            message_text += warn_text.format("-mt", value_mt, False, "-b|-sb (5+6)")
            set_value("-mt", False)
        if (a or b) and e:                                            # -- reset -p
            changed.add("-p")
            message_text += warn_text.format("-p", value_mt, False, "-b-sb (5+6)")
            set_value("-p", False)
            
    # (7) check -p                                                    # -- option -p
    # -p ==> -m LaTeX
    #    ==> -mt True
    if not ("-p" in changed):
        value_m  = get_value("-m")
        value_mt = get_value("-mt")
        value_p  = get_value("-p")
        
        a = value_m == "LaTeX"
        b = value_mt
        c = value_p
        
        if c and not a:                                               # -- reset -m
            changed.add("-m")
            message_text += warn_text.format("-m", value_m, "LaTeX", "-p (7)")
            set_value_combobox("-m", "LaTeX")                         # -- set value for the combobox
            set_value("-m", "LaTeX")
        if not b and c:                                               # -- reset -mt
            changed.add("-mt")
            message_text += warn_text.format("-mt", value_mt, True, "-p (7)")
            set_value("-mt", True)

    # (8) check -mt                                                   # -- option -mt
    # -mt ==> -m LaTeX
    if not ("-mt" in changed):
        value_m  = get_value("-m")
        value_mt = get_value("-mt")
        
        a = value_m == "LaTeX"
        b = value_mt
        
        if b and not a:                                               # -- reset -m
            changed.add("-m")
            message_text += warn_text.format("-m", value_m, "LaTeX", "-p (8)")
            set_value_combobox("-m", "LaTeX")                         # -- set value for the combobox
            set_value("-m", "LaTeX")

    # (9) check -mo                                                   # -- option -mo
    # -mo ==> -f
    value_f  = get_value("-f")
    value_mo = get_value("-mo")

    if value_mo and value_f:                                          # -- reset -f
        message_text += warn_text.format("-f", value_f, False, "-mo (9)")
        set_value("-f", False)

##    # (10) check -m                                                   # -- option -m
##    value_m = get_value("-m")
##    value_b = get_value("-b")
##
##    if (value_m != "BibLaTeX") and (value_b != empty):
##        message_text += warn_text.format("-b", value_b, blank, "-m (10)")
##        set_value("-b", empty)

    # (10) show changes                                               # -- message
    if message_text != empty:                                         
        message_text = "Warnings:\n\n" + message_text
        tkm.showinfo(mm, message_text, icon=tkm.WARNING)
        message_text = empty

    changed = set()
    
# --------------------------------------------------------------------
def clear_fields():                                                   # clear_fields: Clears all entry fields.
    """ The function requires the "sequence" tuple
    and the "options" dictionary.

    no parameters

    global Variable: V, call, values
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default, get_option_line_value, get_value: extended for type combobox

    global V                                                          # -- list with tk variables
    global call                                                       # -- list: parameters for the call of CTANLoadOut.py
    global values                                                     # -- values found in menu; collected by collect_values
    global option_line                                                # -- option <--> line; set by get_option_line
    
    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]
        kind, text1, default, text2, action = options[m]              # -- get the relevant items from options
        if kind in ["number", "listbox", "combobox", "text"]:
##            E[line].delete(0, tk.END)
            V[line].set(empty)                                        # -- initialize with empty string
        elif kind == "checkbox":
            V[line].set(False)                                        # -- initialize with False

    values      = {}                                                  # -- re-initialize the values list
    call        = []                                                  # -- re-initialize the call list
    option_line = {}                                                  # -- option <--> line; set by get_option_line
    
# --------------------------------------------------------------------
def collect_values():                                                 # collect_values: Collects the values in the menu, compares them with the correspoinding defaults and generates a dictionary
    """Collects the values in the menu, compares them with the
    correspoinding defaults and generates a dictionary with
    option <--> value
    THe function requires the "sequence" tuple and the "options" dictionary.

    no parameters

    global variable: values
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default, get_option_line_value, get_value: extended for type combobox

    global values                                                     # -- values found in menu; collected by collect_values
    
    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]
        kind, text1, default, text2, action = options[m]              # -- get the relevant items from options
        if kind in ["text", "listbox"]:
            value = E[line].get()
            if value != str(default):
                values[m] = value                                     # -- get the value of a text or listbox option
        elif kind == "combobox":
            value = CB[line].get()
            if value != str(default):
                values[m] = value                                     # -- get the value of a combobox option 
        elif kind == "number":
            value = E[line].get()
            if value != str(default):
                values[m] = value                                     # -- get the value of a number option 
        elif kind == "list":
            value = E[line].get()
            if value != str(default):
                values[m] = value                                     # -- get the value of a list option
        elif kind == "checkbox":
            value = V[line].get()
            if value != default:
                values[m] = value                                     # -- get the value of a checkbox option

# --------------------------------------------------------------------
def get_default(opt):                                                 # get_default: Returns the default value of a given option.
    """Returns the default value of a given option.
    The function requires the "options" dictionary.

    parameter:
    opt : option to be inspected

    The function returns None:
    + the option is not in ["text", "listbox", "number", "combobox", "list", "checkbox"]
    + the option is not in the sequence disctionary
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default, get_option_line_value, get_value: extended for type combobox

    if opt in sequence:
        kind = options[opt][0]
        if kind in ["text", "listbox", "number", "combobox", "list", "checkbox"]:
                                                                      # -- headers excluded
            return options[opt][2]                                    # -- get the default of opt
        else:
            return None
    else:
        return None

# --------------------------------------------------------------------
def get_option_line():                                                # get_option_line: Generates a dictionary with assignments of options to lines.
    """Generates a dictionary with assignments of options to lines.
    The function requires the "sequence" dictionary.

    no parameters

    global variable: option_line
    """

    global option_line                                                # -- option <--> line; set by get_option_line
    
    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]
        option_line[m] = line

# --------------------------------------------------------------------
def get_option_line_value(option):                                    # get_option_line_value: Generates a dictionary with assignments of options to lines.
    """Returns the tuple (value, line, kind, default) for a given option.
    The function requires the option_line and options dictionary,

    parameter:
    option : option to be inspected
    
    The function returns None:
    + the option is not in ["text", "listbox", "number", "list", "combobox", "checkbox"]
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default, get_option_line_value, get_value: extended for type combobox

    line = option_line[option]
    kind, text1, default, text2, action = options[option]             # -- get the relevant items from options
    if kind in ["text", "listbox", "list", "combobox", "checkbox", "number"]:
                                                                      # -- headers excluded
        value = V[line].get()
        return (value, line, kind, default)
    else:
        return None
   
# --------------------------------------------------------------------
def get_value(option):                                                # get_value: Returns the value of a given option.
    """Returns the value of a given option.
    The function requires the "sequence" tuple, the "option_line" and "options" dictionary.

    parameter:
    option : option to be inspected

    THe function returns None:
    + the option is not in ["text", "listbox", "number", "list", "checkbox", "combobox"]
    + the option is not in the sequence disctionary
    """

    # 1.9.6 2024-06-19: clear_fields, collect_values, get_default, get_option_line_value, get_value: extended for type combobox
    
    if option in sequence:
        tmp  = option_line[option]                                    # get line number of option
        kind = options[option][0]                                     # get type of option
        if kind in ["text", "listbox", "number", "list", "checkbox", "combobox"]:
                                                                      # -- headers excluded
            value = V[tmp].get()                                      # -- read value
            return value
        else:
            return None
    else:
        return None

# --------------------------------------------------------------------
def help1():                                                          # help1 (accumulated entry definitions): Shows an info text (accumulated entry definitions for text, listbox, list, and number).
    """Shows an info text (accumulated entry definitions for text, listbox, list, and number).
    The function requires the "sequence" tuple and the "options" dictionary.

    no parameters
    """

    # 1.11   2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, and start  improved
    
    tmp = empty                                                       # -- title of the info box
    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]                                            # -- get option
        kind, text1, default, text2, action = options[m]              # -- get the relevant items for the option
        if kind in ["text", "listbox", "list"]:
            act_value = V[line].get()                                 # -- get actual value of option
            tmp += f"[E{line}] {text1} ({m}); \n{10*blank}Default: {default}; \n{10*blank}actual value: {act_value}\n"
                                                                      # -- construct one line of the message text
        elif kind == "number":
            tmp += f"[E{line}] {text1} ({m}); \n{10*blank}Default: {default}\n"
                                                                      # -- construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO, title="Description: Entries")
                                                                      # -- show message text

# --------------------------------------------------------------------
def help2():                                                          # help2 (accumulated checkbox definitions): Shows an info text (accumulated checkbox definitions).
    """Shows an info text (accumulated checkbox definitions).
    The function requires the "sequence" tuple and the "options" dictionary.
    """

    # 1.7    2024-06-18: small error in help2 corrected
    # 1.11   2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, and start improved

    tmp = empty                                                       # -- title of the info box
    
    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]                                            # -- get the option
        kind, text1, default, text2, action = options[m]              # -- get the relevant items for the option
        if kind in ["checkbox"]:
            act_value = V[line].get()                                 # -- get actual value of the option
            tmp += f"[C{line}] {text1} ({m}); \n{10*blank}Default: {default}; \n{10*blank}actual value: {default}\n"
                                                                      # -- construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO, title="Description: Checkboxes")
                                                                      # -- show message text

# --------------------------------------------------------------------
def help3():                                                          # help3 (accumulated button definitions): Shows an info text (accumulated button definitions).
    """Shows an info text (accumulated button definitions).
    The function requires the "buttons" tuple.

    no parameters
    """

    # 1.11   2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, and start  improved

    tmp = empty                                                       # -- title of the info box

    for line in range(len(buttons)):                                  # -- loop over all elements of buttons
        text, action, color = buttons[line]                           # -- get the relevant items from buttons
        tmp += f"[B{line}] {text}; color: {color}\n"                  # -- construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO, title="Description: Buttons")
                                                                      # -- show message text

# --------------------------------------------------------------------
def help4():                                                          # help4 (accumulated examples): Shows an info text (accumulated examples).
    """Shows an info text (accumulated examples).
    The function requires the "sequence" tuple, the "examples" and "options" dictionary.

    no parameters
    """

    # 1.11   2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, and start  improved
    
    tmp = empty                                                       # -- title of the info box

    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]
        kind, text1, default, text2, action = options[m]              # -- get the relevant items for the option
        if kind in ["text", "listbox", "list", "number"]:
            example = examples[m]
            tmp += f"[E{line}] {example}\n"                           # -- construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO, title="Examples")
                                                                      # -- show message text

# --------------------------------------------------------------------
def help5():                                                          # help5 (accumulated combobox definitions): Shows an info text (accumulated combobox definitions).
    """Shows an info text (accumulated combobox definitions).
    The function requires the "sequence" tuple and the "options" dictionary.

    no parameters
    """
    
    # 1.9.7  2024-06-19: new: function help5 (accumulated combobox defintions)
    # 1.11   2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top line
    # 1.13   2024-07-08: output in help1, help2, help3, help4, help5, and start  improved
       
    tmp = empty                                                       # -- title of the info box
    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]                                            # -- get the option
        kind, text1, default, text2, action = options[m]              # -- get the relevant items from options
        if kind in ["combobox"]:
            act_value = V[line].get()                                 # -- get actual value of the option
            tmp += f"[CB{line}] {text1} ({m}); \n{10*blank}Default: {default}; \n{10*blank}actual value: {act_value}\n"
                                                                      # -- construct one line of the message text
    tkm.showinfo(master=mm, message=tmp, icon=tkm.INFO, title="Description: omboboxes")
                                                                      # -- show message text

# --------------------------------------------------------------------
def info_version():                                                   # info_version: Shows a version text.
    """Shows a version text.
    """

    # 1.12   2024-07-08: tkm.showinfo in help1, help2, help3, help4, help5, and info_version changed
    # 1.12.1 2024-07-08: showinfo now with the keywords master, message, and title
    # 1.12.2 2024-07-08: messagetexts now without any additional top line
    
    tkm.showinfo(master=mm, message=version, icon=tkm.INFO, title="Version(s)")
                                                                      # -- show message text

# --------------------------------------------------------------------
def init_buttons():                                                   # init_buttons: Defines/initializes on the base of the "buttons" dictionary buttons.
    """Defines/initializes on the base of the "buttons" dictionary
    buttons. The function requires the "buttons" dictionary.

    no parameter

    global variable: B
    """

    # 1.11  2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
    
    global B
    
    for i in range(len(buttons)):                                     # -- loop over all elements of buttons
        text, action, color = buttons[i]                              # -- get the relevant items from buttons
        tmp = f"[B{i}] {text}"                                        # -- construct the text for this button
        B[i] = tk.Button(mm, text=tmp, command=action, bg=color, font=('calibri', 10))
                                                                      # -- define a new button
        B[i].grid(row=3*i, column=2, rowspan=3, sticky=tk.W, padx=7)  # -- position the new button

# --------------------------------------------------------------------
def init_fields():                                                    # init_fields: Defines/initializes on the base of the "options" dictionary headers, labels, entry fields, checkboxes.
    """Defines/initializes on the base of the "options" dictionary
    headers, labels, entry fields, checkboxes.
    The function requires the "sequence" tuple and the "options" dictionary.

    no parameter

    global variables: L, V, E, C, CB
    global variables: values, call, option_line
    """

    # 1.9.4 2024-06-19: in init_fields: special handling of -m deactivated
    # 1.9.5 2024-06-19: in init_fields: new settings for opion -m now by set_value_combobox
    # 1.11  2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings

    # types of fields:
    # + header: only label with text
    # + checkbox: label with text, boolean variable, checkbox
    # + text: label with text, string variable, text field
    # + number: label with text, string variable, text field
    # + list: label with text, string variable, text field
    # + listbox: label with text, string variable, text field
    # + combobox: label with text, string variable, combobox
    
    global L                                                          # -- list for ttk.Label
    global V                                                          # -- list with tk variables
    global E                                                          # -- list for ttk.Entry
    global C                                                          # -- list for ttk.Checkbox
    global CB                                                         # -- list for ttk.Combobox
    global values                                                     # -- values found in menu; collected by collect_values
    global call                                                       # -- list: parameters for the call of CTANLoadOut.py
    global option_line                                                # -- option <--> line; set by get_option_line

    values      = {}                                                  # -- re-initialize values
    call        = []                                                  # -- re-initialize call
    option_line = {}                                                  # -- option <--> line; set by get_option_line

    for line in range(nr):                                            # -- loop over all elements of sequence
        m = sequence[line]
        kind, text1, default, text2, action = options[m]              # -- get the relevant items from options
        if kind == "header":                                          # -- header   
            L[line] = ttk.Label(mm, text=text1, foreground="red") 
            L[line].grid(row=line, column=0, sticky="w", columnspan=3, pady=3)
        elif kind == "checkbox":                                      # -- checkbox
            tmp = f"[C{line}] {text1} ({m})"                          # ---- text of label for checkbox
            L[line] = ttk.Label(mm, text=tmp)                         # ---- label creation 
            L[line].grid(row=line, column=0, sticky="w", padx=5, pady=0)
                                                                      # ---- label position
            V[line] = tk.BooleanVar()                                 # ---- boolean variable 
            C[line] = ttk.Checkbutton(mm, variable=V[line])           # ---- checkbox creation
            C[line].grid(row=line, column=1, sticky="w")              # ---- checkbox position
            V[line].set(str(default))                                 # ---- variable initialization (default)
        elif kind == "text":                                          # -- text
            tmp = f"[E{line}] {text1} ({m})"
            L[line] = ttk.Label(mm, text=tmp)
            L[line].grid(row=line, column=0, sticky="w", padx=5, pady=0)
            V[line] = tk.StringVar()
            E[line] = ttk.Entry(mm, textvariable=V[line])
            E[line].grid(row=line, column=1, sticky="w", ipadx=5)
##            E[line].insert(10, default)
            V[line].set(str(default))
        elif kind == "number":                                        # -- number
            tmp = f"[E{line}] {text1} ({m})"
            L[line] = ttk.Label(mm, text=tmp)
            L[line].grid(row=line, column=0, sticky="w", padx=5, pady=0)
            V[line] = tk.StringVar()
            E[line] = ttk.Entry(mm, textvariable=V[line])
            E[line].grid(row=line, column=1, sticky="w", ipadx=5)
            V[line].set(str(default))
        elif kind == "list":                                          # -- list
            tmp = f"[E{line}] {text1} ({m})"
            L[line] = ttk.Label(mm, text=tmp)
            L[line].grid(row=line, column=0, sticky="w", padx=5, pady=0)
            V[line] = tk.StringVar()
            E[line] = ttk.Entry(mm, textvariable=V[line])
            E[line].grid(row=line, column=1, sticky="w", ipadx=5)
            V[line].set(str(default))
        elif kind == "listbox":                                       # -- listbox       
            tmp = f"[E{line}] {text1} ({m})"
            L[line] = ttk.Label(mm, text=tmp)
            L[line].grid(row=line, column=0, sticky="w", padx=5, pady=0)
            V[line] = tk.StringVar()
            E[line] = ttk.Entry(mm, textvariable=V[line])
            E[line].grid(row=line, column=1, sticky="w", ipadx=5)
            V[line].set(str(default))
        elif kind == "combobox":                                       # -- combobox       
            tmp = f"[CB{line}] {text1} ({m})"
            L[line] = ttk.Label(mm, text=tmp)
            L[line].grid(row=line, column=0, sticky="w", padx=5, pady=0)
            V[line] = tk.StringVar()
            CB[line] = ttk.Combobox(mm, textvariable=V[line], values=action, text=text2, state="readonly")
            if default in list_m:
                ind = list_m.index(default)
            CB[line].current(ind)
            CB[line].grid(row=line, column=1, sticky="w", ipadx=5)
 
# --------------------------------------------------------------------
def listbox_b():                                                      # listbox_b
    # intended for the use with list boxes
    # not yet realized
    pass

# --------------------------------------------------------------------
def listbox_m():                                                      # listbox_m
    # intended for the use with list boxes
    # not yet realized
    pass

# --------------------------------------------------------------------
def make_call():                                                      # make_call: Generates the "call" list.
    """Generates the "call" list. The function requires the "values"
    dictionary.

    no parameters

    global variable: call
    """
    
    global call                                                       # -- list: parameters for the call of CTANLoadOut.py
    
    call = [sys.executable]                                           # -- name of the python processor
    call.append(remote_program_name)                                  # -- the actual program
    for op in values:                                                 # -- loop over all items of values
        val = values[op]                                              # -- fetch one item of values
        if val == False:                                              # -- the checkbox has not been clicked
            pass                                                      # -- do not append nothing
        elif val == True:                                             # -- the checkbox has been clicked
            call.append(op)                                           # -- append option
        else:                                                         # -- another kind of options
            call.append(op)                                           # -- append option
            call.append(val)                                          # -- append cooresponding value

# --------------------------------------------------------------------
def quit():                                                           # quit: Opens a dialogbox, whether the program should be terminated/finished.
    """Opens a dialogbox, whether the program should be terminated/finished.

    no parameters
    """
    
    stat = tkm.askyesno(message="Should the program be terminated??", title="Quit")
                                                                      # -- yes/no message box
    if stat:                                                          # -- if the answer is "yes"
        mm.destroy()                                                  # -- the menu is closed

# --------------------------------------------------------------------
def set_value(option, val):                                           # set_value: Resets the value for a option with a specified value.
    """Resets the value for a option with a specified value.

    parameters:
    option : option to be set
    val    : value

    global variable: V

    The function returns None:
    + the given option is not in sequence
    """

    # 1.8  2024-06-19: security question added to set_value
    
    # set_value ==> get_option_line_value
    
    global V                                                          # -- list with tk variables
    
    if option in sequence:
        value, line, kind, default = get_option_line_value(option)    # -- get the line of the option
        V[line].set(val)                                              # -- set the value
    else:
        return None

# --------------------------------------------------------------------
def set_value_combobox(opt, val):                                     # set_value_combobox: Resets the value for the option (-m" or "-b") with a specified value.
    """Resets the value for the option (-m" or "-b") with a specified value.

    parameters:
    opt : option to be set
    val : value

    global variable: CB

    The function returns None:
    + val ist not in list_m
    + val ist not in list_b
    + opt is not -m or -b
    # opt is not in sequence
    """
    # 1.9.8 2024-06-19: new: set_value_combobox: set value for comboboxes
    
    global CB                                                         # -- list with CB entries
    
    if opt in sequence:
        if opt == "-m":                                               # -- option -m
            if val in list_m:
                opt_ind = list_m.index(val)                           # -- get the number of val in list_m
            else:
                return None
        elif opt == "-b":                                             # -- option -b
            if val in list_b:
                opt_ind = list_b.index(val)                           # -- get the number of val in list_b
            else:
                return None
        else:
            return None
        ind = sequence.index(opt)                                     # -- get the line of the opti
        CB[ind].current(opt_ind)                                      # -- set he value
    else:
        return None

# --------------------------------------------------------------------
def show_log():                                                       # show_log: Shows the log file of the called subprocess.
    """Shows the log file of the called subprocess.
    The function requires the "log" variable (text).

    no parameters
    """

    window = tk.Toplevel(mm)                                          # -- open new window
    window.title("Log file for menu_CTANLoadOut")                     # -- title of the new window

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20)
                                                                      # -- ScrolledText widget
    text_area.pack(expand=True, fill="both")

    message = "Log file of menu_CTANLoadOut\n" + log                  # -- add a title to the log variable
    text_area.insert(tk.END, message)                                 # -- output the message

# --------------------------------------------------------------------
def start():                                                          # start: Prepares the processing.
    """Prepares the processing. The function requires the "options" dictionary.

    no parameters.

    global variable: call
    """

    # 1.11  2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings
    # 1.13  2024-07-08: output in help1, help2, help3, help4, help5, and start improved

    # start ==> get_option_line
    #       ==> check_values
    #       ==> collect_values
    #       ==> make_call
    #       ==> start_call

    global call                                                       # -- list: parameters for the call of CTANLoadOut.py
    
    get_option_line()                                                 # -- preparation: option <--> line
    check_values()                                                    # -- check all possible values 
    collect_values()                                                  # -- collect all Useful options with values
    make_call()                                                       # -- construct the call
    
    msg = "The following options were determined.\nShould the actual processing be started?\n\n"

    tmp = call[2:]
    for f in range(len(tmp)):                                         #  -- construct message text
        tmp_f = tmp[f]
        if tmp_f in ["-c", "-f", "-l", "-mo", "-mt", "-nf", "-p", "-r", "-s", "-stat", "-v"]:
            msg += f"{tmp_f}  --  \n{10*blank}({options[tmp_f][1]})\n"
        elif tmp_f == empty:
            continue
        elif tmp_f[0] == "-":
            msg += f"{tmp_f}  {tmp[f+1]}  --  \n{10*blank}({options[tmp_f][1]})\n"
        else:
            pass
    
    stat = tkm.askyesno(title="Start", message=msg)                   # -- message with question
    if stat:                                                          # -- if OK ==> start_call
        start_call()

# --------------------------------------------------------------------
def start_call():                                                     # start_call: Starts the processing.
    """Starts the processing. The function requires the "call" list.

    no parameters.
    """

    # 1.11  2024-07-08: as far as possible and useful: string interpolation via .format replaced by f-strings

    global log                                                        # -- to be used for log data

    log = empty
    
    try:                                                              # -- start the subprocess in a try/except constrauct
        with TemporaryFile("r+", encoding="utf-8", errors="ignore") as f:
                                                                      # -- temporary file
            process_load = subprocess.run(call, check=True, timeout=timeout10, encoding="utf-8",
                                          stdout=f, stderr=subprocess.PIPE, universal_newlines=True)
            f.seek(0)                                                 # -- rewind file
            for line in f.readlines():                                # -- line by line
                log += line 
            load_errormessage = process_load.stderr                   # -- possible error message
            if len(load_errormessage) > 0:
                print(load_errormessage)
    except subprocess.CalledProcessError as exc:                      # -- process not found
        print(f"[CTANLoadOut] Error: called process '{call[1]}' not found,", sys.exc_info()[0])
        sys.exit("[CTANLoadOut] Error: program terminated")           # -- program terminated    
    except FileNotFoundError as exc:                                  # -- file not found
        print(f"[CTANLoadOut] Error: file '{call[0]}' not found", exc)
        sys.exit("[CTANLoadOut] Error: program terminated")           # -- program terminated
    except subprocess.TimeoutExpired as exc:                          # -- timeout
        print("[CTANLoadOut] Error: timeout error", timeout10)
        sys.exit("[CTANLoadOut] Error: program terminated")           # -- program terminated
    except KeyboardInterrupt as exc:                                  # -- keyboard interrupt
        print("[CTANLoadOut] Error: keyboard interrupt", exc)
        sys.exit("[CTANLoadOut] Error: program terminated")           # -- program terminated
    except UnicodeDecodeError as exc:                                 # -- unicode decode error
        print("[CTANLoadOut] Error: unicode decode error", exc)
        sys.exit("[CTANLoadOut] Error: program terminated")           # -- program terminated
    except:                                                           # -- any unspecified error
        print("[CTANLoadOut] Error: any unspecified error", sys.exc_info())
        sys.exit("[CTANLoadOut] Error: program terminated")           # -- program terminated

    tkm.showinfo(mm, message="Finished!\n\nFor more informations read the log file.", icon=tkm.INFO)    


# ====================================================================
# Lists, tuples, dictionaries
# --------------------------------------------------------------------
# Currently not used; intended for working with list boxes

list_m   = ["LaTeX", "RIS", "plain", "BibLaTeX", "Excel"]             # possible values for -m
list_b   = ["@online", "@software", "@misc", "@ctan", "@www"]         # possible values for -b

# --------------------------------------------------------------------
# tuple "sequence":
# defines the sequence of menu rows (on the base of CTANLoad / CTAMOut options)
# will be used in clear_fields, collect_values, collect_values, get_option_line,
#   get_value, help1, help2, help4, help5, init_fields

# h1, h2, h3, h4, h5 for headers

sequence = ("h1", "-o", "-d", "-tout", "-stat", "-v", "-mo",
            "h2", "-t", "-A", "-k", "-L", "-y",
            "h3", "-tl", "-Al", "-kl", "-Ll", "-yl", "-n", "-f",
            "h4", "-to", "-Ao", "-ko", "-Lo", "-yo", "-m", "-b", "-sb", "-s", "-mt", "-nf",
            "h5", "-p", "-c", "-l", "-r")

# --------------------------------------------------------------------
# dictionary "options":
# defines the look of menu items; on the base of CTANLoad / CTAMOut options
# will be used in clear_fields, collect_values, get_option_line_value, get_value, help1,
#   help2, help4, init_fields, start

# + each element is a tuple with 5 components:
#   (0) type of row in the menu: header, text, number, checkbox, listbox, list
#   (1) text in the label
#   (2) default (found in CTANLoadOut)
#   (3) text of the combobox 
#   (4) action associated with the combobox

# 1.2   2024-05-02: default for -b changed to "@online"
# 1.5   2024-06-11: some texts changed in options
# 1.6   2024-06-17: some texts changed in options
# 1.9.3 2024-06-19: option -m in options dictionary: new type combobox, new action

options = {
    "h1"   : ("header",   "Global options",                                                             None,      None, None),
    "-o"   : ("text",     "[CTANLoad+CTANOut] Generic name for output files [without extensions]",      "all",     None, None),
    "-d"   : ("text",     "[CTANLoad+CTANOut] OS folder (directory) for input and output files",        act_dir,   None, None),
    "-tout": ("number",   "[CTANLoadOut] default timeout (sec) for subprocesses ",                      "60",      None, None),
    "-stat": ("checkbox", "[CTANLoad+CTANOut] Flag: statistics on terminal",                            False,     None, None),
    "-v"   : ("checkbox", "[CTANLoad+CTANOut] Flag: Output is verbose",                                 False,     None, None),
    "-mo"  : ("checkbox", "[CTANLoadOut] Flag: Do not activate CTANLoad",                               False,     None, None),

    "h2"   : ("header",   "Options for CTANLoad and CTANOut",                                           None,      None, None),
    "-A"   : ("text",     "[CTANLoad+CTANOut] Name template for authors",                               "^.+$",    None, None),
    "-L"   : ("text",     "[CTANLoad+CTANOut] Name template for licenses",                              "^.+$",    None, None),
    "-k"   : ("text",     "[CTANLoad+CTANOut] Template for keys",                                       "^.+$",    None, None),
    "-t"   : ("text",     "[CTANLoad+CTANOut] Template for package names",                              "^.+$",    None, None),
    "-y"   : ("text",     "[CTANLoad+CTANOut] Template for years",                                      "^19[89][0-9]|20[012][0-9]$", None, None),

    "h3"   : ("header",   "Options for CTANLoad",                                                       None,      None, None),
    "-Ll"  : ("text",     "[CTANLoad] Name template for licenses",                                      empty,     None, None),
    "-kl"  : ("text",     "[CTANLoad] Template for keys",                                               empty,     None, None),
    "-tl"  : ("text",     "[CTANLoad] Template for package names",                                      empty,     None, None),
    "-yl"  : ("text",     "[CTANLoad] Template for years",                                              empty,     None, None),
    "-Al"  : ("text",     "[CTANLoad} Name template for authors",                                       empty,     None, None),
    "-n"   : ("number",   "[CTANLoad] Maximum number of XML and PDF file downloads",                    "250",     None, None),
    "-f"   : ("checkbox", "[CTANLoad] Flag: Download associated documentation files [PDF]",             False,     None, None),

    "h4"   : ("header",   "Options for CTANOut",                                                        None,      None, None),
    "-Lo"  : ("text",     "[CTANOut] Name template for licenses",                                       "^.+$",    None, None),
    "-ko"  : ("text",     "[CTANOut] Template for keys",                                                "^.+$",    None, None),
    "-to"  : ("text",     "[CTANOut] Template for package names",                                       "^.+$",    None, None),
    "-yo"  : ("text",     "[CTANOut] Template for years",                                               empty,     None, None),
    "-Ao"  : ("text",     "[CTANOut} Name template for authors",                                        "^.+$",    None, None),
    "-m"   : ("combobox", "[CTANOut} Target format",                                                    "RIS",     "…search", list_m),
    "-b"   : ("listbox",  "[CTANOut} Type of BibLaTex entries to be generated",                         "@online", None, None),
    "-sb"  : ("list",     "[CTANOut} Skip specified BibLaTeX fields",                                   "[]",      None, None),
    "-s"   : ("list",     "[CTANOut} Skip specified CTAN fields",                                       "[]",      None, None),
    "-mt"  : ("checkbox", "[CTANOut} Flag: Generate topic lists ",                                      False,     None, None),
    "-nf"  : ("checkbox", "[CTANOut} Flag: Do not generate output files",                               False,     None, None),

    "h5"   : ("header",   "Options for special actions",                                                None,      None, None),
    "-p"   : ("checkbox", "[CTANOut} Flag: Generate PDF output",                                        False,     None, None),
    "-c"   : ("checkbox", "[CTANLoad} Flag: Check the integrity of the 2nd .pkl file",                  False,     None, None),
    "-l"   : ("checkbox", "[CTANLoad} Flag: Generate some special lists and prepare files for CTANOut", False,     None, None),
    "-r"   : ("checkbox", "[CTANLoad} Flag: Regenerate the two pickle files",                           False,     None, None),
}

# --------------------------------------------------------------------
# tuple "buttons" (definitions):
# will be used in help3, init_buttons

# each entry:
# (1) title
# (2) action/command
# (3) color

# 1.3   2024-06-06: color of the "Log file" button changed
# 1.9.1 2024-06-19: new in buttons tuple: function help5
# 1.10  2024-07-08: some texts in buttons changed

buttons = (
    ("Start",                     start,        "#FEE4BE"),
    ("Reset fields",              init_fields,  "#FEE4BE"),
    ("Clear menu",                clear_fields, "#FEE4BE"),
    ("Close menu (Quit)",         quit,         "#FEE4BE"),
    ("Description: Entries",      help1,        "#DAFBC1"),
    ("Description: Checkboxes",   help2,        "#DAFBC1"),
    ("Description: Buttons",      help3,        "#DAFBC1"),
    ("Description: Comboboxes",   help5,        "#DAFBC1"),
    ("Examples: Entries",         help4,        "#DAFBC1"),
    ("Version",                   info_version, "#DAFBC1"),
    ("Log file",                  show_log,     "#B0EEF6"),
    )

# --------------------------------------------------------------------
# dictionary "examples":
# will be used in help4

examples = {
    "-A"   : "author template (according to the rules of a regular expression); see authors.xml\n          for example:  Mittelbach",
    "-Al"  : "author template (according to the rules of a regular expression); see authors.xml\n          for example:  Voß",
    "-Ao"  : "author template (according to the rules of a regular expression); see authors.xml\n          for example:  Mittelbach|Voß",
    "-b"   : "one of @online, @software, @misc, @ctan, @www\n          for example:  @online",
    "-c"   : "flag: without any value",
    "-d"   : "corect directory name\n          for example:  .\\result",
    "-f"   : "flag: without any value",
    "-k"   : "key template (according to the rules of a regular expression); see topics.xml\n          for example:  font",
    "-kl"  : "key template (according to the rules of a regular expression); see topics.xml\n          for example:  graphics",
    "-ko"  : "key template (according to the rules of a regular expression); see topics.xml\n          for example:  german|french",
    "-L"   : "license template (according to the rules of a regular expression); see licenses.xml\n          for example:  gpl",
    "-l"   : "flag: without any value",
    "-Ll"  : "license template (according to the rules of a regular expression); see licenses.xml\n          for example:  cc-by-nd",
    "-Lo"  : "license template (according to the rules of a regular expression); see licenses.xml\n          for example:  lppl|gpl",
    "-m"   : "one of LaTeX, latex, tex, RIS, ris, plain, txt, BibLaTeX, biblatex, bib, Excel, excel\n          for example:  LaTeX",
    "-mo"  : "flag: without any value",
    "-mt"  : "flag: without any value",
    "-n"   : "positive integer number\n          for example:  500",
    "-nf"  : "flag: without any value",
    "-o"   : "correct file name (without extension)\n          for example:  extract",
    "-p"   : "flag: without any value",
    "-r"   : "flag: without any value",
    "-s"   : "list with CTAN fields; correct names can be found in CTAN-elements.txt\n          for example:  [description, documentation]",
    "-sb"  : "list with BibLaTeX fields; correct names can be found in CTANOut_mapping_bib.txt\n          for example:  [abstract, related, note]",
    "-stat": "flag: without any value",
    "-t"   : "package template (according to the rules of a regular expression); see packages.xml\n          for example:  biblatex|bibtex",
    "-tl"  : "package template (according to the rules of a regular expression); see packages.xml\n          for example:  ",
    "-to"  : "package template (according to the rules of a regular expression); see packages.xml\n          for example: ",
    "-tout": "positive integer number\n          for example:  50",
    "-v"   : "flag: without any value",
    "-y"   : "year template (according to the rules of a regular expression)\n          for example:  2024|2023",
    "-yl"  : "year template (according to the rules of a regular expression)\n          for example:  20[0-2][0-9]",
    "-yo"  : "year template (according to the rules of a regular expression)\n          for example:  202[12]",
    }

# --------------------------------------------------------------------
# Initializations of some lists:

# 1.9.2 2024-06-19: new: list CB defined and initialized

# V : tkinter variables
# E : tkinter entry fields
# L : tkinter labels
# C : tkinter checkboxes
# B : tkinter buttons
# CB: tkinter comboboxes

nr = len(sequence)                                                    # number of elements in sequence
E  = [None for f in range(nr)]                                        # list for ttk.Entry
L  = [None for f in range(nr)]                                        # list for ttk.Label
V  = [None for f in range(nr)]                                        # list for tk variables
C  = [None for f in range(nr)]                                        # list for ttk.Checkbox
CB = [None for f in range(nr)]                                        # list for ttk Combobox
B  = [None for f in range(len(buttons))]                              # list for tk.Button


# ====================================================================
# main part

# main part ==> init_fields
#           ==> init buttons
#           ==> mm.mainloop

# the menu will be started by a click on the "start" button

init_fields()                                                         # preparation: initialization of fields
init_buttons()                                                        # preparation: initialization of buttons
mm.mainloop()                                                         # main loop


# ====================================================================
# Wünsche/Fehler
# --------------
# + besseres Konzept für buttons und tk.Buttons
# + vielleic ht mit zusätzlichen Spalten: Typ und Text (ggf. per Funktion)
# + make_call mit return (-) 
# + Protokoll-Ausgabe in scrolledtext-Box (anklickbar?) (x)
# + Mono-Font an manchen Stellen (geht nicht)
# + ZUordnung Option <--> Zeile global festlegen (-)
# + Funktionen entsprechend umbauen (-)
# + -d anpassen an verschiedene OS (x)
# + bessere Farben (x)
# + bei manchen Änderungen durch check_values: Warnungen ausgeben (x)
# + Änderungen an Optionswerten einfacher machen; z.B. set_value("-m") (x)
# + vielleicht deshalb neue Tabelle; option: zeile, wert, default (-)
# + vor der eigentlichen Ausführung noch eine Abfrage (x)
# + Kurzschlüsse in check_values vermeiden (x)
# + askyesno mit englichen Texten (- geht nicht einfach)
# + alte werte werden verwendet bei mehrfachen Aufrufen des Menüs (x)
# + muss log global sein? (ja)
# + start-Box vereinfachen (x)
# + messagebox verbreitern (geht nichtdirekt; vielleicht aber mit Message?)
# + in start_call: print-Anweisungen an log anhängen 
# + Warnings sparsamer einsetzen (x)
# + wie sieht es mit -nf oder -mo aus? (x)
# + check_values bereinigen (x)
# + (5) und (6) zusammenfassen (x)
# + überprüfen: -m != LaTeX (x)
# + Combobox für -m (https://www.tutorialspoint.com/combobox-widget-in-python-tkinter) (x)
# + Combobox für -b (https://www.tutorialspoint.com/combobox-widget-in-python-tkinter) funktioniert nicht
# + Forschrittsanzeige (https://www.tutorialspoint.com/progressbar-widget-in-python-tkinter)?
# + Antwortboxen auf englisch

