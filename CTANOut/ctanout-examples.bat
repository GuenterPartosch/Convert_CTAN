:: Examples for CTANLoad.py
:: 2025-02-12
CTANOut.py
CTANOut.py -v
CTANOut.py -v -stat
CTANOut.py -m BibLaTeX
CTANOut.py -m biblatex -b @online -v
CTANOut.py -m bib -b @online -s [texlive,license,miktex] -v -stat
CTANOut.py -m LaTeX -mt -v -stat
CTANOut.py -m latex -k LaTeX -mt
CTANOut.py -m tex -t "l3|latex|ltx" -mt -v
CTANOut.py -m plain -v -stat -o myfile -s "[texlive,license,miktex]"
CTANOut.py -A Knuth -k collection -t knuth -m bib -v -stat
CTANOut.py -m bib -t "akktex|biblatex" -sb "[abstract,note,related]" -v -stat -o example
CTANOut.py -L collection -v
CTANOut.py -L collection -v -A Swift
CTANOut.py -L gpl -v -A Swift -k typesetting
CTANOut.py -L "not free" -v -stat -A Greenwade -k latex209
CTANOut.py -y "2022|2023" -v -stat
CTANOut.py -y "2022|2023" -k "font|class" -v -stat	
CTANOut.py -A "Voß|Oberdieck" -k "font|class" -y "2022|2023" -v -stat
CTANOut.py -k "font|class" -A "Voß|Oberdieck" -y "2022|2023" -v -stat -nf
CTANOut.py -y "2022|2023" -k "font|class"  -A "Voß|Oberdieck" -v -stat -nf
