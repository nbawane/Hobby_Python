maxlba = 33456743 #blocks

total_regions = 7

k4allignment = maxlba/8

print k4allignment

k4perregion = k4allignment/total_regions
print k4perregion
print k4allignment%total_regions
startadd = 0

while currentblockcount < k4perregion:
	print startadd
	startadd = startadd + k4perregion

