import sys, os

if len(sys.argv) <= 1:
    print('''pdfreduce inputfile.pdf [-o]
        -o : overwrite input file, otherwise writes inputfile.red.pdf
    ''')
    sys.exit(1)
    
overwrite = "-o" in sys.argv[1:]

pdfin = sys.argv[1]
assert os.path.isfile(pdfin) 
assert pdfin.endswith('.pdf')


pdfout = pdfin.replace('.pdf', '.red.pdf')
assert pdfout != pdfin
if os.path.isfile(pdfout):
    raise IOError(pdfout + ' exists already')
    
assert pdfout.endswith('.pdf')

script = f"""
gs -o {pdfout} -sDEVICE=pdfwrite {pdfin}
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
