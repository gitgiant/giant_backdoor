# giant_backdoor
### Sticky Keys / Utility Manager Backdoor Diagnostic Tool

Detect and uninstall the sticky keys, utility manager, narrator, on-screen keyboard, magnifier, and display switch backdoors, which allows unauthorized access to a system level command prompt at the login screen.  Checks if setch.exe, utilman.exe, narrator.exe, osk.exe, magnifier.exe, and displayswitch.exe have been replaced by comparing their hashes against cmd.exe, explorer.exe, and powershell.exe.  Checks if there has been any debugger registry keys added for each exe and removes them if necessary. 

Install sticky keys or utility manager backdoor by adding debugger registry keys, use at your own risk!

Disable or Enable Windows Accessibility options through the conifguration menu (currently not working).

To run, open a command prompt in project folder with Administrator Privilege and type in `python backdoor.py`.

## Requirements: 

Windows

Python 3+
