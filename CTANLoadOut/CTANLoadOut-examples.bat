:: Examples for CTANLoadOut.py
:: 2025-02-12

:: CTANLoadOut.py -r
:: CTANLoadOut.py -r -v -stat
:: CTANLoadOut.py -l
:: CTANLoadOut.py -l -v -stat
:: CTANLoadOut.py -mt -p
CTANLoadOut.py -mt -m latex -p -v -stat
CTANLoadOut.py -to latex -m bib -v -stat
CTANLoadOut.py -t "latex|ltx|l3|lt3" -f -m tex -mt -v -stat
CTANLoadOut.py -t pgf -l -c -mt -p -v -stat
CTANLoadOut.py -k latex -m txt -v 
CTANLoadOut.py -k latex -f -v -stat -mt -p
CTANLoadOut.py -k chinese -t "^zh" -f -v -stat
CTANLoadOut.py -ko "latex" -m bib -v
CTANLoadOut.py -A "Knuth" -f -v -stat -m latex -mt -p -k "collection" -t "knuth"
CTANLoadOut.py -k class -v -m latex -mt  -L lppl  -p  -f -A Mittelbach
CTANLoadOut.py -k class -v -m latex -mt  -L lppl -A Kohm -t scr -p  -f
CTANLoadOut.py -L lppl -A Fairbairns -k footnote -v 
CTANLoadOut.py -k class -L lppl -A Kohm -t scr

