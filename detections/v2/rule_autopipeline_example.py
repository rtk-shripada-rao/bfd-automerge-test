MITRE_MAPPING = {"T1059.001": "Command and Scripting Interpreter: PowerShell"}


def detect(event):
    return "powershell" in event.get("command_line", "").lower()
