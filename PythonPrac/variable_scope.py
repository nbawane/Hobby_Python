#program to check the variable scope
mat = [1,2,3,4]
var1 = 0

class Check:
    var2 = 2
    def __init__(self):
        print "to check the variable scope"

    def check_scope(self):
        #global var1

        print "before change ",mat,var1,Check.var2
        mat[2] = "change"
        #var1 +=1
        Check.var2 +=2
        print "after change",mat,var1,Check.var2


p = Check()
p.check_scope()