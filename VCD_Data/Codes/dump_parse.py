"""
********************************************************************************
* MODULE      : dump_parse.py
* FUNCTION    : Contains all the functions to parse dumps provided
* PROGRAMMER  : Nitesh Bawane
* DATE(ORG)   : 01/03/2017
* REMARKS     : NA
* COPYRIGHT   : Copyright (C) 2015 SanDisk Corporation
*------------------------------------------------------------------------------*
* Revision History : 1.0
********************************************************************************
"""
import os
import re

class dump_parse:
    def __init__(self):
        self.__busy = 0
        self.__time1 = 0
        self.__time2 = 0
        self.__flag = 0
        self.__bytecount = 0
    def find_addr(self,line):
        """
        extracts the address
        counts the address num
        :param line: line at which the addr string occured
        :return:
            1. extracted address
            2. Number of elements in address

        """
        search_phrase = 'addr'
        if search_phrase in line:
            ADDRx = ''
            PBx = ''
            CHx   = ''
            addr_string = ''
            joiner = '-'
            temp = line.split(r'(')[1].split(r')')[0].strip()
            addr_data =  temp.split(' ')
            no_of_elements = len(addr_data)
            ADDRx = 'ADDR'+str(no_of_elements)

            if int(addr_data[-2])%2 == 0:   #to check last second bit to calculate the PB0
                plane = 'PB0'
            else:
                plane = 'PB1'
            CHx = 'CH'+str(int(addr_data[-1]))
            seq = (ADDRx,plane,CHx)
            addr_string = joiner.join(seq)
            return addr_string
    def GetData(self,line,datatofind):

        if line.count(datatofind) == 1:
            self.__bytecount +=1
        else:
            return None

        return str((self.__bytecount)/2)+'KB'

    def cal_tADL(self,line):
        """
        calculates the busy time taken after CMD30
        as of now the busy time is calculated from the 1st BUSY to
        the time stamp after the last busy
        :param line:current line of the file
        :return: tADL (time difference) in float format
        """
        search_string =  'BUSY'
        if search_string in line and self.__busy == 0:
            self.__time1 = self.extract_timestamp(line)
            self.__busy = 1
        elif search_string not in line and self.__busy == 1:
            self.__time2 = self.extract_timestamp(line)
            self.__busy = 0
            #print "self.__time1 : ",self.__time1
            #print "self.__time2 : ", self.__time2
            t_diff = self.__time2 - self.__time1
            return self.ConvertTime(t_diff)



    def extract_timestamp(self,line):
        """
        extracts timestamp
        :param line: current line from dump
        :return: return timestamp in float
        """
        str = line.split(" ")
        for i in str:
            if i != '':
                return float(i)

    def ExtractCommand(self,line):
        """
        get the command and return it in CMD(XX) format
        :param line: current line in file
        :return:
        """
        import re

        m = re.search('cmd[0-9a-zA-Z]*', line)    #regular expression to search for command
        if m is not None:
            num = re.search('(?<=cmd)[0-9a-zA-Z]*',m.group())
            seq = ['cmd','(',num.group(),')']   #logic to convert cmd23->cmd(23)
            printdata = ''.join(seq)
            return printdata

    def ConvertTime(self,time,unit = 'us'):
        """
        converts the time into given units,by default is converts it to us
        :param time: time to convert
        :param unit: s/ms/us/ns
        :return: converted time as a string
        """
        ms = 10**3
        us = 10**6
        ns = 10**9
        if unit == 'ms':
            return str(time*ms)+"ms"

        if unit == 'us':
            return str(time*us)+"us"

        if unit == 'ns':
            return str(time*ns)+"ns"


    def terminate(self,line):
        """
        return true if terminate condition matches
        condition : '    9.012273198 1 BUSY  cmd65'
                    here 1 before BUSY will act as a terminator for a block
        :param line:
        :return: True
        """

        m = re.findall(' 1 ', line)
        if len(m) == 1:
            self.__bytecount = 0
            return True
        else:
            return False











