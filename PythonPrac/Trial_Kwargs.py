def kwargs_try(**kwargs):
    for key in kwargs:
        print "Key [%s] : value [%s] "%(key,kwargs[key])

#this feature can be used as a dictionary

kwargs_try(var1 = "var_value1",var2 = "param")
