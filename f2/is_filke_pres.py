#is file present

import os

home_path = r'C:\San_py\f2'
cqfile = 'CQ_bin.txt'
legfile = 'legacy_bin.txt'

fpgafile = os.path.join(home_path,cqfile)
print fpgafile
if os.path.exists(fpgafile):
	fpga_dwn = fpgafile
	
else:
	fpga_dwn = os.path.join(home_path,legfile)

print 'fpga file to download ',fpga_dwn