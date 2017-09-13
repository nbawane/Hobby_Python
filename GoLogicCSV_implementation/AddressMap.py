
class AdressMap:

    def mem1(self):
        '''2LC by A2h command'''
        addmap = {}
        addmap['col_addr']='0-13'
        addmap['page_addr']='17-24'
        addmap['plane']='25'
        addmap['block_addr']='25-36'
        return addmap
    
    def Bics3_128Gb(self):
        addmap = {}
        addmap['col_addr']='0-14'
        addmap['string'] = '16-17'
        addmap['WL'] = '18-23'
        addmap['plane']='24'
        addmap['block_addr']='25-34'
        addmap['die'] = '35-37'
        return addmap        
    
    def Bics3_256Gb(self):
        addmap = {}
        addmap['col_addr']='0-14'
        addmap['string'] = '16-17'
        addmap['WL'] = '18-23'
        addmap['plane']='24'
        addmap['block_addr']='25-35'
        addmap['die'] = '36-38'
        return addmap        
    
    

class AdressMapOperation:

    def __init__(self,memoryname):
        '''
        memorymap is the memory name 
        accroding to memory name the decoding logic will be selected
        '''
        self.memoryname = memoryname
        self.adressmap = AdressMap()
        mem_type_to_call = getattr(self.adressmap,self.memoryname)   #dictionary with address mapping
        self.addressmapdict = mem_type_to_call()
        self.maskdict,self.offsetdict = self.getmask(self.addressmapdict)               #dictionary with mask has same keys as addressmap
        #self.offsetsdict = 
        self.addresslist_len = 0
    
    def decode_address(self,addresslist):
        '''
        returns a dictionary with field value
        decodes the fields as per the memory address map from class memorymap
        if addresslen is 3 column address is ignored
        '''
        self.addresslist_len = len(addresslist)
        temp_dict = {}
        temp_dict = self.addressmapdict.copy()
        merged_address = self.merge_address(addresslist)
        
        for key in self.addressmapdict.keys():
            if self.addresslist_len == 3 and key == 'col_addr':
                temp_dict[key] = None
                continue
            fielddata = self.maskdict[key] & int(merged_address,16)#converting hexstring to integer
            fielddata = fielddata>>self.offsetdict[key]
            temp_dict[key] = hex(int(fielddata))
        return temp_dict
    
    def decode_die(self,addresslist):
        '''
        To decode die number,whenever a di selection command is called
        '''
        merged_address = self.merge_address(addresslist)
        fielddata = self.maskdict['die'] & int(merged_address,16)#converting hexstring to integer
        fielddata = fielddata>>self.offsetdict['die']   
        return 'Die = %s'%int(fielddata)
        
    def getmask(self,addressmapdict):
        """
        creates mask to extract the fields from address map
        """
        temp_dict = self.addressmapdict.copy()
        offsetsdict = self.addressmapdict.copy()
        for key in temp_dict.keys():
            offsets = temp_dict[key]
            offsets = offsets.split('-')
            temp_data = 0
            if len(offsets) == 2:
                
                lsbbit = int(offsets[0])
                msbbit = int(offsets[1])
            else:
                msbbit=lsbbit=int(offsets[0])
            temp_lsbbit = lsbbit
            offsetsdict[key] = lsbbit
            totalbit = msbbit-lsbbit
            for i in range(totalbit+1):
                temp_data = 1<<(temp_lsbbit)|temp_data
                temp_lsbbit = temp_lsbbit+1
                temp_dict[key] = temp_data                    
        return temp_dict,offsetsdict

    def merge_address(self,addrlist):
        '''
        merge the address in addresslist to form a 5byte address
        if addresslist has 3 bytes then 2bytes of 0s are appended 
        to make it 5bytes
        return : merged address as string
        '''
        #addrlist = addrlist[::-1]
        temp = ''
        for byte in addrlist:
            hexnum = (int(byte, 16))
            if hexnum>0 and hexnum < 10:
                byte = '0' + byte
            temp = byte + temp
            #temp =temp[::-1]
        if len(addrlist)==3:
                temp = temp+'0000'
        return temp