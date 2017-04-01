import os
import hashlib

def calculate_sha256(targetFile):
    sha256 = hashlib.sha256()

    with open(targetFile, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            sha256.update(block)
    return sha256.hexdigest()

header = """
  ,ad8888ba,  88
 d8"'    `"8b ""                         ,d
d8'                                      88
88            88 ,adPPYYba, 8b,dPPYba, MM88MMM
88      88888 88 ""     `Y8 88P'   `"8a  88
Y8,        88 88 ,adPPPPP88 88       88  88
 Y8a.    .a88 88 88,    ,88 88       88  88,
  `"Y88888P"  88 `"8bbdP"Y8 88       88  "Y888
______________________________________________\n
Version 1.0     http://www.github.com/gitgiant
        Login Backdoor Diagnostic Tool
Will not work without Administrator privileges
        WARNING: USE AT YOUR OWN RISK!        """

bar = "______________________________________________\n"

drive = os.getenv('SystemDrive')
sethcPath = (drive + '\windows\system32\sethc.exe ')
sethcRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe')
utilmanPath = (drive + '\windows\system32\\utilman.exe ')
utilmanRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\utilman.exe')
narratorPath = (drive + '\windows\system32\\narrator.exe ')
narratorRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\\narrator.exe')
oskPath = (drive + '\windows\system32\osk.exe ')
oskRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\osk.exe')
magnifierPath = (drive + '\windows\system32\magnify.exe ')
magnifierRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\magnify.exe')
displaySwitcherPath = (drive + '\windows\system32\displayswitch.exe ')
displaySwitcherRegistryPath = ('SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\displayswitch.exe')
cwd = os.getcwd()
cmdPath = (drive + '\windows\system32\cmd.exe ')
explorerPath = (drive + '\windows\explorer.exe ')
powershellPath = (drive + '\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe')
cmdSha = calculate_sha256(cmdPath)
explorerSha = calculate_sha256(explorerPath)
powershellSha = calculate_sha256(powershellPath)