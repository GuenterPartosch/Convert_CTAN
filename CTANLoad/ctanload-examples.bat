:: Examples for CTANLoad.py
:: 2025-02-12
CTANLoad.py
CTANLoad.py -v -stat                                            
CTANLoad.py -t "^a.+$" -v
CTANLoad.py -f -n 300 -t "^l3" -v
CTANLoad.py -v -l
CTANLoad.py -v -l -c -stat
CTANLoad.py -vlc -stat
CTANLoad.py -v -stat -r
CTANLoad.py -k latex -f -v -stat
CTANLoad.py -k chinese -t "^zh" -f -v -stat
CTANLoad.py -A Knuth -v -stat
CTANLoad.py -A Knuth -k collection -stat
CTANLoad.py -A Knuth -k collection -f -v -stat -t knuth
CTANLoad.py -L collection -v
CTANLoad.py -L collection -v -A Swift
CTANLoad.py -L gpl -v -A Swift -k typesetting
CTANLoad.py -L "not free" -v -stat -A Greenwade -k latex209
CTANLoad.py -y "2022|2023" -v -stat
CTANLoad.py -y "2022|2023" -k "font|class" -v -stat..py	
CTANLoad.py -A "Voß|Oberdieck" -k "font|class" -y "2022|2023" -v -stat
CTANLoad.py -k "font|class" -A "Voß|Oberdieck" -y "2022|2023" -v -stat 
CTANLoad.py -y "2022|2023" -k "font|class"  -A "Voß|Oberdieck" -v -stat 
