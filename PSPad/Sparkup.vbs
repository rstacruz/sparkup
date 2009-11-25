'****************************
' Author:        Danilo Bargen <gezuru@gmail.com>
' Published:     25.11.2009
' Requirements:  PSPad, sparkup, Windows Script (http://tinyurl.com/376nwk)
' 
' CONFIGURATION
' Please set path to the sparkup python script
  Const SPARKUP_PATH = "c:\sparkup\sparkup"
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
	Dim strCmd
	
	' Create editor-object
	Set editor = newEditor()
	
	' Empty input/output variables
	strInput = ""
	strOutput = ""
	strCmd = ""
	
	' Assign active window
	editor.assignActiveEditor()
	
	' Get selected text
	strInput = editor.selText()
	
	If strInput = "" Then
		Exit Sub
	End If 
	
	' Run sparkup
	strCmd = "cmd /c echo """ & strInput & """ | python " & SPARKUP_PATH & " --no-last-newline"
	with CreateObject("WScript.Shell")
		with .Exec(strCmd)
			with .StdOut
				do until .AtEndofStream
					strOutput = strOutput & Replace(.ReadLine, vbcr, "") & vbNewLine
				Loop
			end with ' StdOut
		end with ' Exec
	end with ' Shell 
	
	' Expand selected shortcuts
	editor.selText(strOutput)
	
	' Destroy unnecessary objects
	Set oExec = Nothing
	Set WshShell = Nothing
	Set objEditor = nothing

End Sub