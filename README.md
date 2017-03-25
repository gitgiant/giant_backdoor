# giant_backdoor
## Sticky Keys / Utility Manager Backdoor Diagnostic Tool

Detect and uninstall a sticky keys or utility manager backdoor, which allows unauthorized access to a system level command prompt at the login screen.  Checks if setch.exe or utilman.exe have been replaced, compares their hashes against cmd.exe, explorer.exe, and powershell.exe.  Checks if setch.exe or utilman.exe have had any debugger registry keys added and removes them if necessary. 

Install sticky keys or utility manager backdoor by adding debugger registry keys, use at your own risk!

Requirements: 
Windows
Python 3+
