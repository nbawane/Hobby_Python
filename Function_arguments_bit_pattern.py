#this script is used to  for sandisk to calculate the bit value 

def byterange(bit_length):
    while bit_length > 0:
        global byte
        x = bit_length
        bits = [x -i for i in range(8) ]
        bit_length -= 8
        byte += 1
        print "%s   :   %s"%(bits , byte)



byte = 0
byterange(511)