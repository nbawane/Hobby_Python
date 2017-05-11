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
    def __init__(self):
        self.a = 'a'
        self.b = 'b'
    def __getattr__(self,name):
        return name
t = Test()
print t.a
print t.b
print t.c