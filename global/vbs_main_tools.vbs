

Function pythonLocation
	' Determines location of python exe file based on computer name
	Set wshShell = CreateObject( "WScript.Shell" )
	strComputerName = wshShell.ExpandEnvironmentStrings( "%COMPUTERNAME%" )
	If strComputerName = "A11963" Then
		pythonLocation = "C:/Users/Barret.OBrock/AppData/Local/Programs/Python/Python35-32/python.exe"
	Else:
		pythonLocation = "C:/Users/Barret.Obrock/Downloads/python.exe"
	End If
End Function
