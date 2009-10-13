Sparkup
=======

Install this by putting `sparkup` in your `$PATH` somewhere. Requires Python 2.5+.

Examples
--------

echo "div" | sparkup
    <div></div>

echo "div#header" | sparkup
    <div id="header"></div>

echo "div.align-left#header" | sparkup
    <div id="header" class="align-left"></div>

echo "#menu \> ul" | sparkup
    # This should be >, but bash needs it escaped.
    <div id="menu">
        <ul></ul>
    </div>
