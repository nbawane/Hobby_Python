wep = ['R','P','S']

import random
me = random.choice(wep)
print('me %s'%me)
cp = random.choice(wep)
print('cp %s'%cp)
mei = wep.index(me)
cpi = wep.index(cp)

maxi = max(mei,cpi)

wini = (maxi+1)%len(wep)
print(wep[wini])
