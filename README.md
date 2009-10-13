Sparkup
=======

Install this by putting `sparkup` in your `$PATH` somewhere. Requires Python 2.5+ (comes
preinstalled with Mac OS X).

Usage
-----

You can write HTML in a CSS-like syntax, and have `sparkup` handle the expansion to full code.
To use `sparkup` in the command line, simply do `echo "<your code here>" | sparkup`.

Sparkup also offers intregration into common text editors. Support for VIM and TextMate are
currently included.

Usage for text editors
----------------------

 - **TextMate**: Simply double-click on the `Sparkup.tmbundle` package in Finder. This
   will install it automatically. In TextMate, open an HTML file (orset the document type to
   HTML) type in something (e.g., `#header > h1`), then press `Ctrl` + `E`. Pressing `Tab`
   will cycle through empty elements.

 - **VIM**: See the `sparkup.vim` file's contents for details.

Examples
--------

**div**
    <div></div>

**div#header**
    <div id="header"></div>

**div.align-left#header**
    <div id="header" class="align-left"></div>

**div#header + div#footer**
    <div id="header"></div>
    <div id="footer"></div>

**#menu > ul**
    <div id="menu">
        <ul></ul>
    </div>

**#menu > h3 + ul**
    <div id="menu">
        <h3></h3>
        <ul></ul>
    </div>

**#header > h1{Welcome to our site}**
    <div id="header">
        <h1>Welcome to our site</h1>
    </div>

**a[href=index.html]{Home}**
    <a href="index.html">Home</a>

**ul > li*3**
    <ul>
        <li></li>
        <li></li>
        <li></li>
    </ul>

**ul > li.item-$*3**
    <ul>
        <li class="item-1"></li>
        <li class="item-2"></li>
        <li class="item-3"></li>
    </ul>

**ul > li.item-$*3 > strong**
    <ul>
        <li class="item-1"><strong></strong></li>
        <li class="item-2"><strong></strong></li>
        <li class="item-3"><strong></strong></li>
    </ul>

**table > tr*2 > td.name + td*3**
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

**#header > ul > li < p{Footer}**
    <!-- The < symbol goes back up the parent; i.e., the opposite of >. -->
    <div id="header">
        <ul>
            <li></li>
        </ul>
        <p>Footer</p>
    </div>


