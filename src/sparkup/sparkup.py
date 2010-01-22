#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from optparse import OptionParser

VERSION = "000" # This line will be replaced in the make process.

# =============================================================================

class Dialect:
    shortcuts = {}
    synonyms = {}
    required = {}
    short_tags = ()

class HtmlDialect(Dialect):
    shortcuts = {
        'cc:ie': {
            'opening_tag': '<!--[if IE]>',
            'closing_tag': '<![endif]-->'},
        'cc:ie6': {
            'opening_tag': '<!--[if lte IE 6]>',
            'closing_tag': '<![endif]-->'},
        'cc:ie7': {
            'opening_tag': '<!--[if lte IE 7]>',
            'closing_tag': '<![endif]-->'},
        'cc:noie': {
            'opening_tag': '<!--[if !IE]><!-->',
            'closing_tag': '<!--<![endif]-->'},
        'html:4t': {
            'expand': True,
            'opening_tag':
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n' +
                '<html lang="en">\n' +
                '<head>\n' +
                '    ' + '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />\n' +
                '    ' + '<title></title>\n' +
                '</head>\n' +
                '<body>',
            'closing_tag':
                '</body>\n' +
                '</html>'},
        'html:4s': {
            'expand': True,
            'opening_tag':
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n' +
                '<html lang="en">\n' +
                '<head>\n' +
                '    ' + '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />\n' +
                '    ' + '<title></title>\n' +
                '</head>\n' +
                '<body>',
            'closing_tag':
                '</body>\n' +
                '</html>'},
        'html:xt': {
            'expand': True,
            'opening_tag':
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n' +
                '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n' +
                '<head>\n' +
                '    ' + '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />\n' +
                '    ' + '<title></title>\n' +
                '</head>\n' +
                '<body>',
            'closing_tag':
                '</body>\n' +
                '</html>'},
        'html:xs': {
            'expand': True,
            'opening_tag':
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n' +
                '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n' +
                '<head>\n' +
                '    ' + '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />\n' +
                '    ' + '<title></title>\n' +
                '</head>\n' +
                '<body>',
            'closing_tag':
                '</body>\n' +
                '</html>'},
        'html:xxs': {
            'expand': True,
            'opening_tag':
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n' +
                '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n' +
                '<head>\n' +
                '    ' + '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />\n' +
                '    ' + '<title></title>\n' +
                '</head>\n' +
                '<body>',
            'closing_tag':
                '</body>\n' +
                '</html>'},
        'html:5': {
            'expand': True,
            'opening_tag':
                '<!DOCTYPE html>\n' +
                '<html lang="en">\n' +
                '<head>\n' +
                '    ' + '<meta charset="UTF-8" />\n' +
                '    ' + '<title></title>\n' +
                '</head>\n' +
                '<body>',
            'closing_tag':
                '</body>\n' +
                '</html>'},
        'input:button': {
            'name': 'input',
            'attributes': { 'class': 'button', 'type': 'button', 'name': '', 'value': '' }
            },
        'input:password': {
            'name': 'input',
            'attributes': { 'class': 'text password', 'type': 'password', 'name': '', 'value': '' }
            },
        'input:radio': {
            'name': 'input',
            'attributes': { 'class': 'radio', 'type': 'radio', 'name': '', 'value': '' }
            },
        'input:checkbox': {
            'name': 'input',
            'attributes': { 'class': 'checkbox', 'type': 'checkbox', 'name': '', 'value': '' }
            },
        'input:file': {
            'name': 'input',
            'attributes': { 'class': 'file', 'type': 'file', 'name': '', 'value': '' }
            },
        'input:text': {
            'name': 'input',
            'attributes': { 'class': 'text', 'type': 'text', 'name': '', 'value': '' }
            },
        'input:submit': {
            'name': 'input',
            'attributes': { 'class': 'submit', 'type': 'submit', 'value': '' }
            },
        'input:hidden': {
            'name': 'input',
            'attributes': { 'type': 'hidden', 'name': '', 'value': '' }
            },
        'script:src': {
            'name': 'script',
            'attributes': { 'src': '' }
            },
        'script:jquery': {
            'name': 'script',
            'attributes': { 'src': 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js' }
            },
        'script:jsapi': {
            'name': 'script',
            'attributes': { 'src': 'http://www.google.com/jsapi' }
            },
        'script:jsapix': {
            'name': 'script',
            'text': '\n    google.load("jquery", "1.3.2");\n    google.setOnLoadCallback(function() {\n        \n    });\n'
            },
        'link:css': {
            'name': 'link',
            'attributes': { 'rel': 'stylesheet', 'type': 'text/css', 'href': '', 'media': 'all' },
            },
        'link:print': {
            'name': 'link',
            'attributes': { 'rel': 'stylesheet', 'type': 'text/css', 'href': '', 'media': 'print' },
            },
        'link:favicon': {
            'name': 'link',
            'attributes': { 'rel': 'shortcut icon', 'type': 'image/x-icon', 'href': '' },
            },
        'link:touch': {
            'name': 'link',
            'attributes': { 'rel': 'apple-touch-icon', 'href': '' },
            },
        'link:rss': {
            'name': 'link',
            'attributes': { 'rel': 'alternate', 'type': 'application/rss+xml', 'title': 'RSS', 'href': '' },
            },
        'link:atom': {
            'name': 'link',
            'attributes': { 'rel': 'alternate', 'type': 'application/atom+xml', 'title': 'Atom', 'href': '' },
            },
        'meta:ie7': {
            'name': 'meta',
            'attributes': { 'http-equiv': 'X-UA-Compatible', 'content': 'IE=7' },
            },
        'meta:ie8': {
            'name': 'meta',
            'attributes': { 'http-equiv': 'X-UA-Compatible', 'content': 'IE=8' },
            },
        'form:get': {
            'name': 'form',
            'attributes': { 'method': 'get' },
            },
        'form:g': {
            'name': 'form',
            'attributes': { 'method': 'get' },
            },
        'form:post': {
            'name': 'form',
            'attributes': { 'method': 'post' },
            },
        'form:p': {
            'name': 'form',
            'attributes': { 'method': 'post' },
            },
        }
    synonyms = {
        'checkbox': 'input:checkbox',
        'check': 'input:checkbox',
        'input:c': 'input:checkbox',
        'button': 'input:button',
        'input:b': 'input:button',
        'input:h': 'input:hidden',
        'hidden': 'input:hidden',
        'submit': 'input:submit',
        'input:s': 'input:submit',
        'radio': 'input:radio',
        'input:r': 'input:radio',
        'text': 'input:text',
        'passwd': 'input:password',
        'password': 'input:password',
        'pw': 'input:password',
        'input:t': 'input:text',
        'linkcss': 'link:css',
        'scriptsrc': 'script:src',
        'jquery': 'script:jquery',
        'jsapi': 'script:jsapi',
        'html5': 'html:5',
        'html4': 'html:4s',
        'html4s': 'html:4s',
        'html4t': 'html:4t',
        'xhtml': 'html:xxs',
        'xhtmlt': 'html:xt',
        'xhtmls': 'html:xs',
        'xhtml11': 'html:xxs',
        'opt': 'option',
        'st': 'strong',
        'css': 'style',
        'csss': 'link:css',
        'css:src': 'link:css',
        'csssrc': 'link:css',
        'js': 'script',
        'jss': 'script:src',
        'js:src': 'script:src',
        'jssrc': 'script:src',
        }
    short_tags = (
        'area', 'base', 'basefont', 'br', 'embed', 'hr',
        'input', 'img', 'link', 'param', 'meta')
    required = {
        'a':      {'href':''},
        'base':   {'href':''},
        'abbr':   {'title': ''},
        'acronym':{'title': ''},
        'bdo':    {'dir': ''},
        'link':   {'rel': 'stylesheet', 'href': ''},
        'style':  {'type': 'text/css'},
        'script': {'type': 'text/javascript'},
        'img':    {'src':'', 'alt':''},
        'iframe': {'src': '', 'frameborder': '0'},
        'embed':  {'src': '', 'type': ''},
        'object': {'data': '', 'type': ''},
        'param':  {'name': '', 'value': ''},
        'form':   {'action': '', 'method': 'post'},
        'table':  {'cellspacing': '0'},
        'input':  {'type': '', 'name': '', 'value': ''},
        'base':   {'href': ''},
        'area':   {'shape': '', 'coords': '', 'href': '', 'alt': ''},
        'select': {'name': ''},
        'option': {'value': ''},
        'textarea':{'name': ''},
        'meta':   {'content': ''},
    }

class Parser:
    """The parser.
    """

    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self, options, string, dialect=HtmlDialect()):
        """Constructor.
        """

        self.tokens = []
        self.string = string
        self.options = options
        self.dialect = dialect
        self.root = Element(parser=self)
        self.caret = []
        self.caret.append(self.root)
        self._last = []

        self._tokenize()
        self._parse()


    # Methods
    # -------------------------------------------------------------------------

    def render(self):
        """Renders.
        Called by [[Router]].
        """

        # Get the initial render of the root node
        output = self.root.render()

        # Indent by whatever the input is indented with
        indent = re.findall(r"^[\r\n]*(\s*)", self.string)[0]
        output = indent + output.replace("\n", "\n" + indent)

        # Strip newline if not needed
        if not self.options.last_newline \
            or self.prefix or self.suffix:
            output = re.sub(r'\n\s*$', '', output)

        # TextMate mode
        if self.options.textmate:
            output = self._textmatify(output)

        return output

    # Protected methods
    # -------------------------------------------------------------------------

    def _textmatify(self, output):
        """Returns a version of the output with TextMate placeholders in it.
        """

        matches = re.findall(r'(></)|("")|(\n\s+)\n|(.|\s)', output)
        output = ''
        n = 1
        for i in matches:
            if i[0]:
                output += '>$%i</' % n
                n += 1
            elif i[1]:
                output += '"$%i"' % n
                n += 1
            elif i[2]:
                output += i[2] + '$%i\n' % n
                n += 1
            elif i[3]:
                output += i[3]
        output += "$0"
        return output

    def _tokenize(self):
        """Tokenizes.
        Initializes [[self.tokens]].
        """

        string = self.string.strip()

        # Find prefix/suffix
        while True:
            match = re.match(r"^(\s*<[^>]+>\s*)", string)
            if match is None: break
            if self.prefix is None: self.prefix = ''
            self.prefix += match.group(0)
            string = string[len(match.group(0)):]

        while True:
            match = re.findall(r"(\s*<[^>]+>[\s\n\r]*)$", string)
            if not match: break
            if self.suffix is None: self.suffix = ''
            self.suffix = match[0] + self.suffix
            string = string[:-len(match[0])]

        # Split by the element separators
        for token in re.split('(<|>|\+(?!\\s*\+|$))', string):
            if token.strip() != '':
                self.tokens.append(Token(token, parser=self))

    def _parse(self):
        """Takes the tokens and does its thing.
        Populates [[self.root]].
        """

        # Carry it over to the root node.
        if self.prefix or self.suffix:
            self.root.prefix = self.prefix
            self.root.suffix = self.suffix
            self.root.depth += 1

        for token in self.tokens:
            if token.type == Token.ELEMENT:
                # Reset the "last elements added" list. We will
                # repopulate this with the new elements added now.
                self._last[:] = []

                # Create [[Element]]s from a [[Token]].
                # They will be created as many as the multiplier specifies,
                # multiplied by how many carets we have
                count = 0
                for caret in self.caret:
                    for local_count in range(1, token.multiplier + 1):
                        count += 1
                        new = Element(token, caret,
                                count = count,
                                local_count = local_count,
                                parser = self)
                        self._last.append(new)
                        caret.append(new)

            # For >
            elif token.type == Token.CHILD:
                # The last children added.
                self.caret[:] = self._last

            # For <
            elif token.type == Token.PARENT:
                # If we're the root node, don't do anything
                parent = self.caret[0].parent
                if parent is not None:
                    self.caret[:] = [parent]

    # Properties
    # -------------------------------------------------------------------------

    # Property: dialect
    # The dialect of XML
    dialect = None

    # Property: string
    # The string
    string = ''

    # Property: tokens
    # The list of tokens
    tokens = []

    # Property: options
    # Reference to the [[Options]] instance
    options = None

    # Property: root
    # The root [[Element]] node.
    root = None

    # Property: caret
    # The current insertion point.
    caret = None

    # Property: _last
    # List of the last appended stuff
    _last = None

    # Property: indent
    # Yeah
    indent = ''

    # Property: prefix
    # (String) The trailing tag in the beginning.
    #
    # Description:
    # For instance, in `<div>ul>li</div>`, the `prefix` is `<div>`.
    prefix = ''

    # Property: suffix
    # (string) The trailing tag at the end.
    suffix = ''

# =============================================================================

class Element:
    """An element.
    """

    def __init__(self, token=None, parent=None, count=None, local_count=None,
                 parser=None, opening_tag=None, closing_tag=None,
                 attributes=None, name=None, text=None):
        """Constructor.

        This is called by ???.

        Description:
        All parameters are optional.

        token       - (Token) The token (required)
        parent      - (Element) Parent element; `None` if root
        count       - (Int) The number to substitute for `&` (e.g., in `li.item-&`)
        local_count - (Int) The number to substitute for `$` (e.g., in `li.item-$`)
        parser      - (Parser) The parser

        attributes  - ...
        name        - ...
        text        - ...
        """

        self.children = []
        self.attributes = {}
        self.parser = parser

        if token is not None:
            # Assumption is that token is of type [[Token]] and is
            # a [[Token.ELEMENT]].
            self.name        = token.name
            self.attributes  = token.attributes.copy()
            self.text        = token.text
            self.populate    = token.populate
            self.expand      = token.expand
            self.opening_tag = token.opening_tag
            self.closing_tag = token.closing_tag

        # `count` can be given. This will substitude & in classname and ID
        if count is not None:
            for key in self.attributes:
                attrib = self.attributes[key]
                attrib = attrib.replace('&', ("%i" % count))
                if local_count is not None:
                    attrib = attrib.replace('$', ("%i" % local_count))
                self.attributes[key] = attrib

        # Copy over from parameters
        if attributes: self.attributes = attributes
        if name:       self.name       = name
        if text:       self.text       = text

        self._fill_attributes()

        self.parent = parent
        if parent is not None:
            self.depth = parent.depth + 1

        if self.populate: self._populate()

    def render(self):
        """Renders the element, along with it's subelements, into HTML code.

        [Grouped under "Rendering methods"]
        """

        options = self.parser.options
        output = ""
        spaces_count = options.indent_spaces
        spaces = ' ' * spaces_count
        indent = self.depth * spaces

        prefix, suffix = ('', '')
        if self.prefix: prefix = self.prefix + "\n"
        if self.suffix: suffix = self.suffix

        # Make the guide from the ID (/#header), or the class if there's no
        # ID (/.item)
        # This is for the start-guide, end-guide and post_tag_guides
        guide_string = ''
        if 'id' in self.attributes:
            guide_string += "#%s" % self.attributes['id']
        elif 'class' in self.attributes:
            guide_string += ".%s" % self.attributes['class'].replace(' ', '.')

        # Build the post-tag guide (e.g., </div><!-- /#header -->),
        # the start guide, and the end guide.
        guide = ''
        start_guide = ''
        end_guide = ''

        if ((self.name == 'div') and \
            (('id' in self.attributes) or ('class' in self.attributes))):

            if (options.post_tag_guides):
                guide = "<!-- /%s -->" % guide_string

            if (options.start_guide_format):
                format = options.start_guide_format
                try: start_guide = format % guide_string
                except: start_guide = (format + " " + guide_string).strip()
                start_guide = "%s<!-- %s -->\n" % (indent, start_guide)

            if (options.end_guide_format):
                format = options.end_guide_format
                try: end_guide = format % guide_string
                except: end_guide = (format + " " + guide_string).strip()

                if options.end_guide_newline:
                    end_guide = "\n%s<!-- %s -->" % (indent, end_guide)
                else:
                    end_guide = "<!-- %s -->" % (end_guide)

        # Short, self-closing tags (<br />)
        short_tags = self.parser.dialect.short_tags

        # When it should be expanded..
        # (That is, <div>\n...\n</div> or similar -- wherein something must go
        # inside the opening/closing tags)
        if  len(self.children) > 0 \
            or self.expand \
            or prefix or suffix \
            or (self.parser.options.expand_divs and self.name == 'div'):

            for child in self.children:
                output += child.render()

            # For expand divs: if there are no children (that is, `output`
            # is still blank despite above), fill it with a blank line.
            if (output == ''): output = indent + spaces + "\n"

            # If we're a root node and we have a prefix or suffix...
            # (Only the root node can have a prefix or suffix.)
            if prefix or suffix:
                output = "%s%s%s%s%s\n" % \
                    (indent, prefix, output, suffix, guide)

            # Uh..
            elif self.name != '' or \
                 self.opening_tag is not None or \
                 self.closing_tag is not None:
                output = start_guide + \
                         indent + self.get_opening_tag() + "\n" + \
                         output + \
                         indent + self.get_closing_tag() + \
                         guide + end_guide + "\n"


        # Short, self-closing tags (<br />)
        elif self.name in short_tags:
            output = "%s<%s />\n" % (indent, self.get_default_tag())

        # Tags with text, possibly
        elif self.name != '' or \
             self.opening_tag is not None or \
             self.closing_tag is not None:
            output = "%s%s%s%s%s%s%s%s" % \
                (start_guide, indent, self.get_opening_tag(), \
                 self.text, \
                 self.get_closing_tag(), \
                 guide, end_guide, "\n")

        return output

    def get_default_tag(self):
        """Returns the opening tag (without brackets).

        Usage:
            element.get_default_tag()

        [Grouped under "Rendering methods"]
        """

        output = '%s' % (self.name)
        for key, value in self.attributes.iteritems():
            output += ' %s="%s"' % (key, value)
        return output

    def get_opening_tag(self):
        if self.opening_tag is None:
            return "<%s>" % self.get_default_tag()
        else:
            return self.opening_tag

    def get_closing_tag(self):
        if self.closing_tag is None:
            return "</%s>" % self.name
        else:
            return self.closing_tag

    def append(self, object):
        """Registers an element as a child of this element.

        Usage:
            element.append(child)

        Description:
        Adds a given element `child` to the children list of this element. It
        will be rendered when [[render()]] is called on the element.

        See also:
        - [[get_last_child()]]

        [Grouped under "Traversion methods"]
        """

        self.children.append(object)

    def get_last_child(self):
        """Returns the last child element which was [[append()]]ed
        to this element.

        Usage:
            element.get_last_child()

        Description:
        This is the same as using `element.children[-1]`.

        [Grouped under "Traversion methods"]
        """

        return self.children[-1]

    def _populate(self):
        """Expands with default items.

        This is called when the [[populate]] flag is turned on.
        """

        if self.name == 'ul':
            elements = [Element(name='li', parent=self, parser=self.parser)]

        elif self.name == 'dl':
            elements = [
                Element(name='dt', parent=self, parser=self.parser),
                Element(name='dd', parent=self, parser=self.parser)]

        elif self.name == 'table':
            tr = Element(name='tr', parent=self, parser=self.parser)
            td = Element(name='td', parent=tr, parser=self.parser)
            tr.children.append(td)
            elements = [tr]

        else:
            elements = []

        for el in elements:
            self.children.append(el)

    def _fill_attributes(self):
        """Fills default attributes for certain elements.

        Description:
        This is called by the constructor.

        [Protected, grouped under "Protected methods"]
        """

        # Make sure <a>'s have a href, <img>'s have an src, etc.
        required = self.parser.dialect.required

        for element, attribs in required.iteritems():
            if self.name == element:
                for attrib in attribs:
                    if attrib not in self.attributes:
                        self.attributes[attrib] = attribs[attrib]

    # -------------------------------------------------------------------------

    # Property: last_child
    # [Read-only]
    last_child = property(get_last_child)

    # -------------------------------------------------------------------------

    # Property: parent
    # (Element) The parent element.
    parent = None

    # Property: name
    # (String) The name of the element (e.g., `div`)
    name = ''

    # Property: attributes
    # (Dict) The dictionary of attributes (e.g., `{'src': 'image.jpg'}`)
    attributes = None

    # Property: children
    # (List of Elements) The children
    children = None

    # Property: opening_tag
    # (String or None) The opening tag. Optional; will use `name` and
    # `attributes` if this is not given.
    opening_tag = None

    # Property: closing_tag
    # (String or None) The closing tag
    closing_tag = None

    text = ''
    depth = -1
    expand = False
    populate = False
    parser = None

    # Property: prefix
    # Only the root note can have this.
    prefix = None
    suffix = None

# =============================================================================

class Token:
    def __init__(self, string, parser=None):
        """Token.

        Description:
        string   - The string to parse

        In the string `div > ul`, there are 3 tokens. (`div`, `>`, and `ul`)

        For `>`, it will be a `Token` with `type` set to `Token.CHILD`
        """

        self.string = string.strip()
        self.attributes = {}
        self.parser = parser

        # Set the type.
        if self.string == '<':
            self.type = Token.PARENT
        elif self.string == '>':
            self.type = Token.CHILD
        elif self.string == '+':
            self.type = Token.SIBLING
        else:
            self.type = Token.ELEMENT
            self._init_element()

    def _init_element(self):
        """Initializes. Only called if the token is an element token.
        [Private]
        """

        # Get the tag name. Default to DIV if none given.
        name = re.findall(r'^([\w\-:]*)', self.string)[0]
        name = name.lower().replace('-', ':')

        # Find synonyms through this thesaurus
        synonyms = self.parser.dialect.synonyms
        if name in synonyms.keys():
            name = synonyms[name]

        if ':' in name:
            shortcuts = self.parser.dialect.shortcuts
            if name in shortcuts.keys():
                for key, value in shortcuts[name].iteritems():
                    setattr(self, key, value)
                if 'html' in name:
                    return
            else:
                self.name = name

        elif (name == ''): self.name = 'div'
        else: self.name = name

        # Look for attributes
        attribs = []
        for attrib in re.findall(r'\[([^\]]*)\]', self.string):
            attribs.append(attrib)
            self.string = self.string.replace("[" + attrib + "]", "")
        if len(attribs) > 0:
            for attrib in attribs:
                try:    key, value = attrib.split('=', 1)
                except: key, value = attrib, ''
                self.attributes[key] = value

        # Try looking for text
        text = None
        for text in re.findall(r'\{([^\}]*)\}', self.string):
            self.string = self.string.replace("{" + text + "}", "")
        if text is not None:
            self.text = text

        # Get the class names
        classes = []
        for classname in re.findall(r'\.([\$a-zA-Z0-9_\-\&]+)', self.string):
            classes.append(classname)
        if len(classes) > 0:
            try:    self.attributes['class']
            except: self.attributes['class'] = ''
            self.attributes['class'] += ' ' + ' '.join(classes)
            self.attributes['class'] = self.attributes['class'].strip()

        # Get the ID
        id_match = re.search(r'#([\$a-zA-Z0-9_\-\&]+)', self.string)
        if id_match is not None:
            self.attributes['id'] = id_match.group(1)

        # See if there's a multiplier (e.g., "li*3")
        multiplier_match = re.search(r'\*\s*([0-9]+)', self.string)
        if multiplier_match is not None:
            self.multiplier = int(multiplier_match.group(1))

        # Populate flag (e.g., ul+)
        flags_match = re.search(r'[\+\!]+$', self.string)
        if flags_match is not None:
            if '+' in flags_match.group(0):
                self.populate = True
            if '!' in flags_match.group(0):
                self.expand = True

    def __str__(self):
        return self.string

    string = ''
    parser = None

    # For elements
    # See the properties of `Element` for description on these.
    name = ''
    attributes = None
    multiplier = 1
    expand = False
    populate = False
    text = ''
    opening_tag = None
    closing_tag = None

    # Type
    type = 0
    ELEMENT = 2
    CHILD = 4
    PARENT = 8
    SIBLING = 16

# =============================================================================

def parse_args():
    optparser = OptionParser(version=VERSION,
            description="Expands input into HTML.",
            epilog="Please refer to the manual for more information.")


    optparser.add_option('--no-guides', action="store_true", help='Deprecated')
    optparser.add_option('--post-tag-guides', action="store_true",
            help='Adds comments at the end of DIV tags')
    optparser.add_option('--textmate', action="store_true",
            help='Adds snippet info (textmate mode)')
    optparser.add_option('--indent-spaces', help='Indent spaces')
    optparser.add_option('--expand-divs', action="store_true",
            help='Automatically expand divs')
    optparser.add_option('--no-last-newline', action="store_false",
            help='Skip the trailing newline')
    optparser.add_option('--start-guide-format', help='To be documented')
    optparser.add_option('--end-guide-format', help='To be documented')
    optparser.add_option('--end-guide-newline', help='To be documented')

    optparser.set_defaults(post_tag_guides=False, textmate=False,
            indent_spaces=4, expand_divs=False, last_newline=True,
            start_guide_format="", end_guide_format="", end_guide_newline=True)

    # Make sure they're the correct types
    opt_args = optparser.parse_args()
    opt_args[0].indent_spaces     = int(opt_args[0].indent_spaces)
    opt_args[0].end_guide_newline = bool(int(opt_args[0].end_guide_newline))
    return opt_args

def main():
    (options, _) = parse_args()

    lines = sys.stdin.read()

    parser = Parser(options, lines)

    output = parser.render()
    sys.stdout.write(output)

if __name__ == "__main__":
    main()
