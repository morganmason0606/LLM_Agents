# Define the path to the Python executable and the script
$pythonPath = "C:\Python39\python.exe"
$scriptPath = "C:\path\to\my_script.py"

# Define the task name and the time to run the task
$taskName = "RunPythonScript"
$timeToRun = "2024-08-08T10:00:00"  # Set your desired time here

# Create the scheduled task
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptPath
$trigger = New-ScheduledTaskTrigger -Once -At $timeToRun
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -Settings $settings -TaskName $taskName
```

3. **Run the PowerShell Script**:
   Save the PowerShell script as `schedule_task.ps1` and run it in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File C:\path\to\schedule_task.ps1
```

This script will create a scheduled task that runs your Python script at the specified time. The task will run only once, as specified by the `-Once` parameter in the `New-ScheduledTaskTrigger` cmdlet.

Would you like more details or assistance with any specific part of this process?

Source: Conversation with Copilot, 8/8/2024
(1) Executing Python Scripts through PowerShell: A Step-by-Step Guide. https://www.advancedinstaller.com/execute-python-script-through-powershell.html.
(2) Running a python script via Powershell script - Stack Overflow. https://stackoverflow.com/questions/54350820/running-a-python-script-via-powershell-script.
(3) What's the best way to execute PowerShell scripts from Python. https://stackoverflow.com/questions/47094207/whats-the-best-way-to-execute-powershell-scripts-from-python.
(4) How to run a python program from powershell based on python hashbang .... https://stackoverflow.com/questions/55601446/how-to-run-a-python-program-from-powershell-based-on-python-hashbang.