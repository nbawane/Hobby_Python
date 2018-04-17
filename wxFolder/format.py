line = ['bronze','Gold','Silver','Platinum']

print "| " + " | ".join("{:{}}".format(x, 12)
                                for i, x in enumerate(line)) + " |"