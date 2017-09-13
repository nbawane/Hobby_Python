#import excelinterface
import global_var

class GetFlags:
    '''
    As of now a row will be passed and to this class
    function of this flag is to provide all the bits
    and data available on that row
    '''
    def __init__(self):
        #self.max_row  = global_var.max_row
        #self.max_column = global_var.max_column
        self.COL_POSITIONS = global_var.COL_POSITION
        self.offset = min(self.COL_POSITIONS.values())
        
    def get_time_unit(self,row):
        return row[self.COL_POSITIONS['units']-self.offset]
    
    def get_ready_busy_state(self,row):
        return int(row[self.COL_POSITIONS['rdy_bsy']-self.offset])
    
    def get_read_enable_flag(self,row):
        return int(row[self.COL_POSITIONS['re0']-self.offset])
    
    def get_ale_flag(self,row):
        return int(row[self.COL_POSITIONS['ale']-self.offset])
    
    def get_cle_flag(self,row):
        return int(row[self.COL_POSITIONS['cle']-self.offset])
    
    def get_write_enable_flag(self,row):
        return int(row[self.COL_POSITIONS['we0']-self.offset])
    
    def get_data_field(self,row):
        return row[self.COL_POSITIONS['fd_bus']-self.offset]
    
    def get_time_stamp(self,row):
        return row[self.COL_POSITIONS['SampleTime']-self.offset]
    
    def get_ce_0_flag(self,row):
        return row[self.COL_POSITIONS['ce_0']-self.offset]
    
    def get_ce_1_flag(self,row):
        try:
            return row[self.COL_POSITIONS['ce1']-self.offset]
        except KeyError:
            return 1    #by defailt return the chip as unselected
    
    def get_ce_2_flag(self,row):
        try:
            return row[self.COL_POSITIONS['ce2']-self.offset]
        except KeyError:
            return 1
    
    def get_ce_3_flag(self,row):
        try:
            return row[self.COL_POSITIONS['ce3']-self.offset]    
        except KeyError:
            return 1
        