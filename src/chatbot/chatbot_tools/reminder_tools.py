import datetime
import subprocess
import time

from langchain_core.tools import tool

from src import config


def _set_alarm_with_ps(
    alarm_hour: int, alarm_minute: int, alarm_message: str = "Alarm"
):

    ps_command = f"""
    $Time = (Get-Date).Date.AddHours({alarm_hour}).AddMinutes({alarm_minute})
    $Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-Command \\"Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('{alarm_message}', 'Alarm')\\""
    $Trigger = New-ScheduledTaskTrigger -Once -At $Time
    Register-ScheduledTask -TaskName 'PythonAlarm' -Action $Action -Trigger $Trigger -Force
    """

    subprocess.run(["powershell", "-Command", ps_command], shell=True)


def _set_alarm_with_bash(hour: int, minute: int, message: str):
    """Set an alarm using Bash."""
    now = datetime.datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if target <= now:
        target += datetime.timedelta(days=1)

    wait_seconds = int((target - now).total_seconds())

    bash_cmd = f"sleep {wait_seconds}; echo -e '\\a'; echo 'ALARM: {message} ⏰'"

    subprocess.Popen(["bash", "-c", bash_cmd])
    print(f"Alarm set for {target.strftime('%H:%M')} with message: {message}")


@tool
def set_alarm(hour: int, minute: int, alarm_message: str = "Alarm"):
    """Set an alarm.
    Args:
        alarm_hour (int): Hour for the alarm (0-23).
        alarm_minute (int): Minute for the alarm (0-59).
        alarm_message (str): Message to display when the alarm rings.
    """

    if config.terminal == "PowerShell":
        _set_alarm_with_ps(hour, minute, alarm_message)
    elif config.terminal == "Bash":
        _set_alarm_with_bash(hour, minute, alarm_message)
    else:
        raise ValueError("Unsupported terminal type. Please use PowerShell or Bash.")
