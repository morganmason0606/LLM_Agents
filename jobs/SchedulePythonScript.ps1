# Define the path to the Python script
$pythonScriptPath = Join-Path $(Get-Location) "check.py"

# List of times when the Python script should run (24-hour format, e.g., "HH:mm")
$timesToRun = @("08:00", "12:00", "16:00")

# Function to schedule the Python script
function Schedule-PythonScript {
    param (
        [string]$time
    )

    # Extract hour and minute from the time string
    $hour, $minute = $time -split ":"

    # Create a unique task name using the time
    $taskName = "PythonScriptTask_$hour$minute"

    # Build the argument for the `schtasks` command to create a scheduled task
    $schtasksArguments = "/Create /TN $taskName /TR `"python $pythonScriptPath`" /SC DAILY /ST $time /F"

    # Execute the command to create the task
    schtasks.exe $schtasksArguments
}

# Loop through each time in the list and schedule the script
foreach ($time in $timesToRun) {
    Schedule-PythonScript -time $time
}

Write-Host "Scheduled Python script at the following times:"
$timesToRun | ForEach-Object { Write-Host $_ }
