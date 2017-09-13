'''
Should contain all global variables which must be initialized once in main 
file and used across all the file without reinitialization
'''
COL_POSITION = {}
GUI_COL = {}
max_row = None
max_column = None
globalcsvsheet=None
GUI_Row = 0
GUI_Column = 0
class GetColNums:
    '''
    This class is responsible to give column number of the fields
    Return : Dictionary with column name and current column number. 
             Number starts from 1.
    '''
    
    def __init__(self):
        '''
        csvsheet : is a sheet instance , must be passed from main file
        '''
        global COL_POSITION
        global max_row
        global max_column
        global globalcsvsheet
        global GUI_COL
        global GUI_Row
        global GUI_Column
        
        COL_POSITION = {'Sample#':None,
                        'SampleTime':None,
                        'units':None,
                        'fd_bus':None,
                        'rdy_bsy':None,
                        're0':None,
                        'ale':None,
                        'cle':None,
                        'we0':None
                        }
        #max_column = self.csvsheet.max_column
        #max_row = sum(1 for row in self.csvsheet)
        GUI_COL = {'Timestamp(ns)':0,
                   'Chip':1,
                   'Event':2,
                   'AddrMap':3,
                   'Ready/Busy(ns)':4,
                   'CMD':5,
                   'Address':6,
                   'Data':7,
                   'DataSize(Bytes)':8}
        
        GUI_Column = len(GUI_COL)
        GUI_Row = 200000 #fixed as of now
        
    def getposition(self,row):
        ##
        #purpose is to extract column numbers of the field name
        global COL_POSITION
        keys = COL_POSITION.keys()
        for index,element in enumerate(row):
            print 'index %s: row  %s'%(index,element)
            COL_POSITION[element] = index
        return
        
        
        
    def col_position_dict(self,row):
        global COL_POSITION
        if len(set(COL_POSITION.values())) == len(COL_POSITION.keys()):
            return COL_POSITION
        else:
            return self.getposition(row)
        
   