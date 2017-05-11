import os
import subprocess
import time

class RunScript:
    '''
    here the default operation should come

    execute setenv.bat file
    open test_list and make list
    '''
    env_file = r"C:\CQ_implementation\SDDVT_CQ_Python_Package_Nitesh_workspace\SDDVT\Tools\Environment\setenv.bat"
    cwd = r'C:\CQ_implementation\SDDVT_CQ_Python_Package_Nitesh_workspace\SDDVT'
    os.system(env_file)
    os.chdir(cwd)
    def Execute(self):
        path = r'C:\San_py\test_folder2'
        proc = []
        t_list = []
        test_file = r'test_file.txt'
        #batch_file = "moniter_batch.bat "
        batch_file = "start cmd.exe @cmd /k "
        file = open(test_file,'r')      #open the test_file which contains list of tests to be performed
        for line in file:
            test_id = line.split('_')[0]
            #print test_id                   #test ids to be used in final stages
            execute =  script = r'python Testrunner.py --protocol=sd --sdtestid='+test_id+' --dbconnection=none --adapter=0 --sdConfiguration=DDR50 --projectconfig="C:\Program Files (x86)\SanDisk\SDDVT_Python_Package\SDDVT_Python_Package\SDDVT\Projects_configuration\Phnx2_SD_HC_I041_SDR50_Perf_C4_U0_064G" --paramsfile="C:\Program Files (x86)\SanDisk\SDDVT_Python_Package\SDDVT_Python_Package\SDDVT\Projects_configuration\Phnx2_SD_HC_I041_SDR50_Perf_C4_U0_064G\Phnx2_SD_HC_I041_SDR50_Perf_C4_U0.txt" --logfilename=C:\New_package_result\\'+test_id+'.txt'
            os.system(execute)
            t_list.append(line)
            #print line
            '''
            need to launch in different command.exe and give the title  and use TASKLIST /V /FO "CSV" | FINDSTR abra
            '''
        time.sleep(10)
        print t_list
        self.kill(t_list)

    def kill(self,kill_list):
        self.kill_list = kill_list
        find = "TASKLIST /V /fo csv"
        #output = subprocess.Popen(find, stdout=subprocess.PIPE).stdout
        for task in self.kill_list:
            output = subprocess.Popen(find, stdout=subprocess.PIPE).stdout
            for cm_line in output:
                if task.strip('\n') in cm_line:
                    pid = cm_line.split(',')[1]
                    print pid
                    end = 'Taskkill /pid '+str(pid)
                    #time.sleep(20)
                    os.system(end)
                    print  'killed ',pid



runobj = RunScript()
runobj.Execute()