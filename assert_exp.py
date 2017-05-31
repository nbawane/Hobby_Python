stat = {'PDMS':"sup",'PSUS':'nsup','POFS':'nsup'}
assert ((stat['PDMS']=='sup' or stat['PSUS']=='sup') and (stat['POFS']=='nsup'))
print " abc \n%s"%stat