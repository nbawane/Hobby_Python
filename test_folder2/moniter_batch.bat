@echo off
for %%a in (1,2,3,4) do echo %%a

REM getting the arguments from command line
set arg1 = %1

REM executing the programm passed in command line
start cmd.exe @cmd /k %1
echo 'hello'




