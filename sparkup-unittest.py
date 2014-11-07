#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import sparkup


class SparkupTest:
    options = {
        'textmate': True,
        'no-last-newline': True,
        'post-tag-guides': True,
        }
    options = {
        'default': {'textmate': True, 'no-last-newline': True, 'post-tag-guides': True},
        'guides':  {'textmate': True, 'no-last-newline': True, 'post-tag-guides': True, 'start-guide-format': 'Begin %s'},
        'namespaced-elements': {'textmate': True, 'no-last-newline': True, 'post-tag-guides': True, 'namespaced-elements': True }
        }
    cases = {
        'Simple test': {
            'options': 'default',
            'input': 'div',
            'output': '<div>$1</div>$0'
            },
        'Class test': {
            'input': 'div.lol',
            'output': '<div class="lol">$1</div><!-- /.lol -->$0'
            },
        'ID and class test': {
            'input': 'div.class#id',
            'output': '<div class="class" id="id">$1</div><!-- /#id -->$0'
            },
        'ID and class test 2': {
            'input': 'div#id.class',
            'output': '<div class="class" id="id">$1</div><!-- /#id -->$0'
            },
        'Attributes test': {
            'input': 'div#id.class[style=color:blue]',
            'output': '<div style="color:blue" class="class" id="id">$1</div><!-- /#id -->$0'
            },
        'Multiple attributes test': {
            'input': 'div[align=center][style=color:blue][rel=none]',
            'output': '<div align="center" style="color:blue" rel="none">$1</div>$0'
            },
        'Multiple class test': {
            'input': 'div.c1.c2.c3',
            'output': '<div class="c1 c2 c3">$1</div><!-- /.c1.c2.c3 -->$0'
            },
        'Shortcut test': {
            'input': 'input:button',
            'output': '<input type="button" class="button" value="$1" name="$2">$0'
            },
        'Shortcut synonym test': {
            'input': 'button',
            'output': '<button>$1</button>$0',
            },
        'Child test': {
            'input': 'div>ul>li',
            'output': "<div>\n    <ul>\n        <li>$1</li>\n    </ul>\n</div>$0"
            },
        'Sibling test': {
            'input': 'div#x + ul+   h3.class',
            'output': '<div id="x">$1</div><!-- /#x -->\n<ul>$2</ul>\n<h3 class="class">$3</h3>$0'
            },
        'Child + sibling test': {
            'input': 'div > ul > li + span',
            'output': '<div>\n    <ul>\n        <li>$1</li>\n        <span>$2</span>\n    </ul>\n</div>$0'
            },
        'Multiplier test 1': {
            'input': 'ul > li*3',
            'output': '<ul>\n    <li>$1</li>\n    <li>$2</li>\n    <li>$3</li>\n</ul>$0'
            },
        'Multiplier test 2': {
            'input': 'ul > li.item-$*3',
            'output': '<ul>\n    <li class="item-1">$1</li>\n    <li class="item-2">$2</li>\n    <li class="item-3">$3</li>\n</ul>$0'
            },
        'Multiplier test 3': {
            'input': 'ul > li.item-$*3 > a',
            'output': '<ul>\n    <li class="item-1">\n        <a href="$1">$2</a>\n    </li>\n    <li class="item-2">\n        <a href="$3">$4</a>\n    </li>\n    <li class="item-3">\n        <a href="$5">$6</a>\n    </li>\n</ul>$0'
            },
        'Ampersand test': {
            'input': 'td > tr.row-$*3 > td.cell-&*2',
            'output': '<td>\n    <tr class="row-1">\n        <td class="cell-1">$1</td>\n        <td class="cell-2">$2</td>\n    </tr>\n    <tr class="row-2">\n        <td class="cell-3">$3</td>\n        <td class="cell-4">$4</td>\n    </tr>\n    <tr class="row-3">\n        <td class="cell-5">$5</td>\n        <td class="cell-6">$6</td>\n    </tr>\n</td>$0'
            },
        'Menu test': {
            'input': 'ul#menu > li*3 > a > span',
            'output': '<ul id="menu">\n    <li>\n        <a href="$1">\n            <span>$2</span>\n        </a>\n    </li>\n    <li>\n        <a href="$3">\n            <span>$4</span>\n        </a>\n    </li>\n    <li>\n        <a href="$5">\n            <span>$6</span>\n        </a>\n    </li>\n</ul>$0'
            },
        'Back test': {
            'input': 'ul#menu > li*3 > a <   < div',
            'output': '<ul id="menu">\n    <li>\n        <a href="$1">$2</a>\n    </li>\n    <li>\n        <a href="$3">$4</a>\n    </li>\n    <li>\n        <a href="$5">$6</a>\n    </li>\n</ul>\n<div>$7</div>$0'
            },
        'Expand test': {
            'input': 'p#menu > table+ + ul',
            'output': '<p id="menu">\n    <table>\n        <tr>\n            <td>$1</td>\n        </tr>\n    </table>\n    <ul>$2</ul>\n</p>$0'
            },
        'Text with dot test': {
            'input': 'p { text.com }',
            'output': '<p> text.com </p>$0'
            },
        'Attribute with dot test': {
            'input': 'p [attrib=text.com]',
            'output': '<p attrib="text.com">$1</p>$0'
            },
        'PHP tag test': {
            'input': 'php',
            'output': '<?php\n    $1\n?>$0',
            },
        'Eruby tag test': {
            'input': 'erb:p',
            'output': '<%=  %>$0',
            },
        'ERB block test': {
            'input': 'erb:b',
            'output': '<% $2 %>\n    $1\n<% end %>$0'
            },
        'Nested curly braces test': {
            'input': 'p{{{ title }}}',
            'output': '<p>{{ title }}</p>$0'
            },
        'Nested curly braces test (#54)': {
            'input': 'html>head>title{${title}}',
            'output': '<html>\n    <head>\n        <title>${title}</title>\n    </head>\n</html>$0'
            },
        'HTML component element with dash test': {
            'input': 'my-html-component',
            'output': '<my-html-component>$1</my-html-component>$0' 
            },
        'XML namespaced element': {
            'options': 'namespaced-elements',
            'input': 'namespaced-ul',
            'output': '<namespaced:ul>$1</namespaced:ul>$0'
            },
        # Add: text test, broken test, multi-attribute tests, indentation test, start and end comments test
        }

    def run(self):
        """Run Forrest run!"""
        failures = 0

        print("Test results:")
        for name, case in self.cases.iteritems():
            try:
                options_key = case['options']
            except:
                options_key = 'default'

            try:
                options = self.options[options_key]
            except:
                options = self.options['default']

            # Output buffer
            r = sparkup.Router()
            input = case['input']
            output = r.start(options=options, str=input, ret=True)
            del r

            # Did it work?
            result = output == case['output']
            if result:
                result_str = " OK "
            else:
                result_str = "FAIL"

            print(" - %-30s [%s]" % (name, result_str))
            if not result:
                failures += 1
                print("= %s" % input.replace("\n", "\n= "))
                print("Actual output (condensed):")
                print(" | '%s'" % output.replace("\n", r"\n").replace('"', '\"'))
                print("Actual output:")
                print(" | %s" % output.replace("\n", "\n | "))
                print("Expected:")
                print(" | %s" % case['output'].replace("\n", "\ n| "))

        return failures

if __name__ == '__main__':
    s = SparkupTest()
    sys.exit(s.run())
