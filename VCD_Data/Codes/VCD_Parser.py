"""
********************************************************************************
* MODULE      : VCD_Parser.py
* FUNCTION    : Parse VCD dumps in provide the extracted output in predefined .xlsx format
* PROGRAMMER  : Nitesh Bawane
* DATE(ORG)   : 01/03/2017
* REMARKS     : NA
* COPYRIGHT   : Copyright (C) 2015 SanDisk Corporation
*------------------------------------------------------------------------------*
* Revision History : 1.0
********************************************************************************
"""
import dump_parse
import xlsxwt
import os
import DirOperation as DirOpp
import time
# file_path = 'C:\VCD_Parsing\Input_File'
Output_Files = r"C:\VCD_Data\Output_Files"
# file_name = "FOLD01_F0B0_Fail_VCD.txt"
Input_Files = r"C:\VCD_Data\Input_Files"

class VCD_Parser:

    def __init__(self,dump,filename):

        self.dump_file = dump
        self.file_name = filename
        self.dump_file_operation    = dump_parse.dump_parse()
        self.DirOps                  = DirOpp.DirOperation()
        self.string_to_excel        = ''
        self.excel_operation        = xlsxwt.write_to_excel()
        self.Row                    = 1
        self.Column                 = 1

    def __del__(self):
        self.dump_file.close()

    def Run(self):

        self.Row = 1
        joiner = '-'
        seq = []
        for line in self.dump_file:

            if not self.dump_file_operation.terminate(line):
                '''
                check for the termination condition, if termination condition satisfied then
                new line would be created
                '''

                addr_data = self.dump_file_operation.find_addr(line)
                tADL = self.dump_file_operation.cal_tADL(line)
                command = self.dump_file_operation.ExtractCommand(line)
                data = self.dump_file_operation.GetData(line,"_512_bytes")
                if data is not None:
                    seq[-1] = data

                if addr_data is not None:
                    seq.append(addr_data)
                if tADL > 0:
                    seq.append(str(tADL))

                if command is not None:
                    seq.append(command)
            else:
                printstr = joiner.join(seq)+'\n'    #added to achieve the newline logging of string in cell
                print printstr
                self.Row += 1
                self.excel_operation.write_at_location(self.Row,self.Column,printstr)
                seq = []
        self.file_name = self.file_name.split(".")[0]
        #self.excel_operation.Concat("B2",self.Row,self.Column)
        #self.excel_operation.EraseCells(self.Row,self.Column)#after concatenation the data is copied in specified space hence need to rease the cell previously
        self.excel_operation.file_save(self.file_name+time.strftime('_%Y%m%d_%H%M%S'))

        self.dump_file.close()


if __name__ == "__main__":
    DirOp =  DirOpp.DirOperation()
    files = DirOp.GetInputFiles()
    for file in files:
        filepath = os.path.join(Input_Files,file)
        fd = open(filepath,'r')
        parser = VCD_Parser(fd,file)
        parser.Run()
    DirOp.MoveInputFilesToFolder()
    DirOp.MoveOutputFiles()



