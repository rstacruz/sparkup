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

Usage and installation
----------------------
You may download Sparkup from Github. [Download the latest version here](http://github.com/rstacruz/sparkup/downloads).

 - **TextMate**: Simply double-click on the `Sparkup.tmbundle` package in Finder. This
   will install it automatically. In TextMate, open an HTML file (orset the document type to
   HTML) type in something (e.g., `#header > h1`), then press `Ctrl` + `E`. Pressing `Tab`
   will cycle through empty elements.

 - **VIM**: See the `vim/README.txt` file for details.

 - **Others/command line use**: You may put `sparkup` in your `$PATH` somewhere. You may then
   invoke it by typing `echo "(input here)" | sparkup`, or `sparkup --help` for a list of commands.

Credits
-------

Sparkup is written by Rico Sta. Cruz and is released under the MIT license.

This project is inspired by [Zen Coding](http://code.google.com/p/zen-coding/) of
[Vadim Makeev](http://pepelsbey.net). The Zen HTML syntax is forward-compatible with Sparkup
(anything that Zen HTML can parse, Sparkup can too).

The following people have contributed code to the project:

 - Guillermo O. Freschi (Tordek @ github)
   Bugfixes to the parsing system

 - Eric Van Dewoestine (ervandew @ github)
   Improvements to the VIM plugin

Examples
--------

**`div`** expands to:
    <div></div>

**`div#header`** expands to:
    <div id="header"></div>

**`div.align-left#header`** expands to:
    <div id="header" class="align-left"></div>

**`div#header + div#footer`** expands to:
    <div id="header"></div>
    <div id="footer"></div>

**`#menu > ul`** expands to:
    <div id="menu">
        <ul></ul>
    </div>

**`#menu > h3 + ul`** expands to:
    <div id="menu">
        <h3></h3>
        <ul></ul>
    </div>

**`#header > h1{Welcome to our site}`** expands to:
    <div id="header">
        <h1>Welcome to our site</h1>
    </div>

**`a[href=index.html]{Home}`** expands to:
    <a href="index.html">Home</a>

**`ul > li*3`** expands to:
    <ul>
        <li></li>
        <li></li>
        <li></li>
    </ul>

**`ul > li.item-$*3`** expands to:
    <ul>
        <li class="item-1"></li>
        <li class="item-2"></li>
        <li class="item-3"></li>
    </ul>

**`ul > li.item-$*3 > strong`** expands to:
    <ul>
        <li class="item-1"><strong></strong></li>
        <li class="item-2"><strong></strong></li>
        <li class="item-3"><strong></strong></li>
    </ul>

**`table > tr*2 > td.name + td*3`** expands to:
    <table>
        <tr>
            <td class="name"></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td class="name"></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </table>

**`#header > ul > li < p{Footer}`** expands to:
    <!-- The < symbol goes back up the parent; i.e., the opposite of >. -->
    <div id="header">
        <ul>
            <li></li>
        </ul>
        <p>Footer</p>
    </div>


