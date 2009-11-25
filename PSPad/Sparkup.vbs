'****************************
' Author:        Danilo Bargen <gezuru@gmail.com>
' Requirements:  PSPad, sparkup, Windows Script (http://tinyurl.com/376nwk)
' 
' CONFIGURATION
' Please set path to the sparkup python script
  Const SPARKUP_PATH = "c:\sparkup\sparkup"
' In case python isn't in the PATH variable, set the path here
  Const PYTHON_PATH = "python"
'****************************


Const MODULE_NAME  = "Sparkup"
Const MODULE_VER   = "1.00"

Sub Init()
	addMenuItem "Sparkup Expand", "", MODULE_NAME, "CTRL+,"
End Sub

Sub Sparkup()
	' Define variables
	Dim strInput
	Dim strOutput
	Dim strError
	Dim strCmd
	
	' Create editor-object
	Set editor = newEditor()
	
	' Empty input/output variables
	strInput = ""
	strOutput = ""
	strError = ""
	strCmd = ""
	
	' Assign active window
	editor.assignActiveEditor()
	
	' Get selected text
	strInput = editor.selText()
	
	' If no text selected, do nothing
	If strInput = "" Then
		Exit Sub
	End If 
	
	' Run sparkup
	strCmd = "cmd /c echo """ & strInput & """ | " & PYTHON_PATH & " " & SPARKUP_PATH & " --no-last-newline"
	with CreateObject("WScript.Shell")
		with .Exec(strCmd)
			with .StdOut
				do until .AtEndofStream
					strOutput = strOutput & Replace(.ReadLine, vbcr, "") & vbNewLine
				Loop
			end with ' StdOut
			with .StdErr
				do until .AtEndofStream
					strError = strError & Replace(.ReadLine, vbcr, "") & vbNewLine
				Loop
			end with ' StdErr
		end with ' Exec
	end with ' Shell
	
	' If error occured
	If strError <> "" Then
		MsgBox strError, 16, "Sparkup Error"
		' Destroy unnecessary objects
		Set oExec = Nothing
		Set WshShell = Nothing
		Set objEditor = nothing
		' Quit script
		Exit Sub
	End If
	
	' Expand selected shortcuts
	editor.selText(strOutput)
	
	' Destroy unnecessary objects
	Set oExec = Nothing
	Set WshShell = Nothing
	Set objEditor = nothing

End Sub