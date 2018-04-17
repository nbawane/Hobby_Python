
const = [0x55 for i in range(511)]
print const

allzeros = [0 for i in range(511)]
print allzeros

allones = [0xff for i in range(511)]
print allones

x=0
incremental = [hex(i) for i in range(511) ]
print incremental

x = 90
neg_const = [hex(0-x) for i in range(511)]
print neg_const

