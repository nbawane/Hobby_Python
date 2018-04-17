d = {'a':'printing','b':2,'c':3,'d':4,'stat':'done'}

keys = ['a','b','c','d','stat']
# String = [str(d[key]) for key in keys]
# print String
print_sata = '{:<10}{:<10}{:<10}{:<10}{:<10}'.format(d['a'],d['b'],d['c'],d['d'],d['stat'])
print print_sata
#
# def print_table(table):
#     col_width = [max(len(x) for x in col) for col in zip(*table)]
#     for line in table:
#         print "| " + " | ".join("{:{}}".format(x, col_width[i])
#                                 for i, x in enumerate(line)) + " |"
#
# table = [(str(x), str(f(x))) for x in mylist]
# print_table(table)