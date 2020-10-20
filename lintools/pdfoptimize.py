#!/usr/bin/env python
import sys, os

if len(sys.argv) <= 1:
    print('''pdfoptimize inputfile.pdf [-o]
        -o : overwrite input file, otherwise writes inputfile.opt.pdf
    ''')
    sys.exit(1)
    
overwrite = "-o" in sys.argv[1:]
#  TODO add option do choose the optimization mode
optimize_option = ['screen', 'ebook', 'printer', 'prepress', 'default'][1]  # ordered by increasing quality

pdfin = sys.argv[1]
assert os.path.isfile(pdfin) 
assert pdfin.endswith('.pdf')


pdfout = pdfin.replace('.pdf', f'.opt-{optimize_option}.pdf')
assert pdfout != pdfin
if os.path.isfile(pdfout):
    raise IOError(pdfout + ' exists already')
    
assert pdfout.endswith('.pdf')

script = f"""
ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/{optimize_option} -dNOPAUSE -dQUIET -dBATCH -sOutputFile={pdfout} {pdfin}
"""

print(pdfin + ' -> ' + pdfout)
print(script)
os.system(script)

if overwrite:
    if os.path.isfile(pdfout):
        print(pdfout + ' -> ' + pdfin)
        os.system('mv ' + pdfout + " " + pdfin)
    


# =============== TO RASTERIZE THE VECTOR IMAGES WITHOUT LOOSING VECTOR TEXT USE SMTH LIKE :

# script = f"""
# gs -o _tmp_onlytxt.pdf -sDEVICE=pdfwrite -dFILTERVECTOR -dFILTERIMAGE {pdfin} || exit 1
# gs -o _tmp_graphics.pdf -sDEVICE=pdfwrite -dFILTERTEXT {pdfin} || exit 1
# 
# 
# # may require customize imagemagik policy
# DPI=300
# convert -density $DPI -quality 100 _tmp_graphics.pdf _tmp_graphics.png  || exit 1
# convert -density $DPI -quality 100 _tmp_graphics*.png _tmp_graphics.pdf || exit 1
# 
# pdftk _tmp_graphics.pdf multistamp _tmp_onlytxt.pdf output {pdfout} || exit 1
# rm -f _tmp_onlytxt.pdf _tmp_graphics.pdf _tmp_graphics*.png
# """
# 
# print(script)
# os.system(script)
