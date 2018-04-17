"""
========================================
Create 2D bar graphs in different planes
========================================

Demonstrates making a 3D plot which has 2D bar graphs projected onto
planes y=0, y=1, etc.
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
path = r'C:\LSV3'
log1 = r'LSV3_parsedlog_20180323_153315_2832.log'
log2 = r'LSV3_parsedlog_20180323_165045_3512'
log3 = r'LSV3_parsedlog_20180323_171718_3992'
log4 = r'LSV3_parsedlog_20180323_174319_5848'
log5 = r'LSV3_parsedlog_20180323_175358_2680'
import os
logpath = os.path.join(path,log1)

fd = open(logpath)
for line in fd:
	if '{' in line:
		dict = 


# subcycle = 0
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for c, z in zip([ 'b'], [0,1]):
#     xs = list(hotcount.keys())
#     # xs.sort()
#     ys = list(hotcount.values())
#     # ys.sort()
#
#     # You can provide either a single color or an array. To demonstrate this,
#     # the first bar of each set will be colored cyan.
#     cs = [c] * len(xs)
#     # cs[0] = 'c'
#     ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)
#
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
#
# plt.show()
