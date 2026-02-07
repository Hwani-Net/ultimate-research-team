$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = "C:\Users\AIcreator\OneDrive\바탕 화면"
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\AI_연구팀_실행.lnk")
$Shortcut.TargetPath = "D:\AI 자동화 연구\AI 에이전트 협업\ultimate_research_team\Run_Research_Team.bat"
$Shortcut.WorkingDirectory = "D:\AI 자동화 연구\AI 에이전트 협업\ultimate_research_team"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,263"
$Shortcut.Save()
