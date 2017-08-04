# class tetcall:
#     def __init__(self):
#         print "tasting __call__"
#
#     def __call__(self, *args):
#         for i in args:
#             print i
#
#
# a = tetcall()
# a("1","e","pp")

class Test:

    def __new__(cls):
        print "creating new instance"
    def __init__(self):
        print "intanciting the the class"

a = Test()