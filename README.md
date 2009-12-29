Sparkup
=======

**Sparkup lets you write HTML code faster.** Don't believe us?
[See it in action!](http://www.youtube.com/watch?v=Jw3jipcenKc)

You can write HTML in a CSS-like syntax, and have Sparkup handle the expansion to full HTML
code. It is meant to help you write long HTML blocks in your text editor by letting you
type less characters than needed.

Sparkup is written in Python, and requires Python 2.5 or newer (2.5 is preinstalled in 
Mac OS X Leopard). Sparkup also offers intregration into common text editors. Support for VIM
and TextMate are currently included.

A short screencast is available here: 
[http://www.youtube.com/watch?v=Jw3jipcenKc](http://www.youtube.com/watch?v=Jw3jipcenKc)

Build instructions
------------------

The files in the source tree are not useable straight away: you need to build the plugins
first. Simple type `make` (assuming you have GNU make installed) in the project's root.

What it will do:

 - Create a directory called `sparkup-<version>/`
 - Put the packaged, ready-to-use plugins there
 - Inject the version number (from the file `VERSION`) to the copies of sparkup.py in that directory
 - Create a redistributable ZIP file (`sparkup-<version>.zip`)
