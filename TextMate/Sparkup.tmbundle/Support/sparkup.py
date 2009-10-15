#!/usr/bin/env python

import os
import fileinput
import getopt
import sys
import re

# =============================================================================== 

class Parser:
    """The parser.
    """

    # Constructor
    # --------------------------------------------------------------------------- 

    def __init__(self, options=None, str=''):
        """Constructor.
        """

        self.str = str
        self.options = options
        self.root = Element(parser = self)
        self.caret = []
        self.caret.append(self.root)
        self._last = []

    # Methods 
    # --------------------------------------------------------------------------- 

    def load_string(self, str):
        """Loads a string to parse.
        """

        self.str = str
        self._tokenize()
        self._parse()

    def render(self):
        """Renders.
        Called by [[Router]].
        """

        # Get the initial render of the root node
        output = self.root.render()

        # Indent by whatever the input is indented with
        indent = re.findall("^[\r\n]*(\s*)", self.str)[0]
        output = indent + output.replace("\n", "\n" + indent)

        # Strip newline if not needed
        if self.options.has("no-last-newline") \
            or self.prefix or self.suffix:
            output = re.sub(r'\n\s*$', '', output)

        # TextMate mode
        if self.options.has("textmate"):
            output = self._textmatify(output)

        return output

    # Protected methods 
    # --------------------------------------------------------------------------- 

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

        str = self.str.strip()

        # Find prefix/suffix
        while True:
            match = re.match(r"^(\s*<[^>]+>\s*)", str)
            if match is None: break
            if self.prefix is None: self.prefix = ''
            self.prefix += match.group(0)
            str = str[len(match.group(0)):]

        while True:
            match = re.findall(r"(\s*<[^>]+>[\s\n\r]*)$", str)
            if not match: break
            if self.suffix is None: self.suffix = ''
            self.suffix = match[0] + self.suffix
            str = str[:-len(match[0])]

        # Split by the element separators
        for token in re.split('(<|>|\+(?!\\s*\+|$))', str):
            if token.strip() != '':
                self.tokens.append(Token(token))

    def _parse(self):
        """Takes the tokens and does its thing.
        Populates [[self.root]].
        """

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
                    local_count = 0
                    for i in range(token.multiplier):
                        count += 1
                        local_count += 1
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
        return

    # Properties
    # --------------------------------------------------------------------------- 

    # Property: str
    # The string
    str = ''
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

    prefix = ''
    suffix = ''
    pass

# =============================================================================== 

class Element:
    def __init__(self, token=None, parent=None, count=None, local_count=None, parser=None):
        self.children = []
        self.attributes = {}
        self.parser = parser

        if token is not None:
            # Assumption is that token is of type [[Token]] and is
            # a [[Token.ELEMENT]].
            self.name       = token.name
            self.attributes = token.attributes.copy()
            self.text       = token.text
            self.populate   = token.populate
            self.expand     = token.expand

        # `count` can be given. This will substitude & in classname and ID
        if count is not None:
            for key in self.attributes:
                attrib = self.attributes[key]
                attrib = attrib.replace('&', ("%i" % count))
                if local_count is not None:
                    attrib = attrib.replace('$', ("%i" % local_count))
                self.attributes[key] = attrib

        self._fill_attributes()

        self.parent = parent
        if parent is not None:
            self.depth = parent.depth + 1

        if self.populate: self._populate()

    def render(self):
        output = ""
        try:    spaces_count = int(self.parser.options.options['indent-spaces'])
        except: spaces_count = 4
        spaces = ' ' * spaces_count
        indent = self.depth * spaces
        
        prefix, suffix = ('', '')
        if self.prefix: prefix = self.prefix + "\n"
        if self.suffix: suffix = self.suffix

        # Make the guide from the ID (/#header), or the class if there's no ID (/.item)
        # This is for the start-guide, end-guide and post-tag-guides
        guide_str = ''
        if 'id' in self.attributes:
            guide_str += "#%s" % self.attributes['id']
        elif 'class' in self.attributes:
            guide_str += ".%s" % self.attributes['class'].replace(' ', '.')

        # Closing guide (e.g., </div><!-- /#header -->)
        guide = ''
        start_guide = ''
        end_guide = ''
        if ((self.name == 'div') and \
            (('id' in self.attributes) or ('class' in self.attributes))):

            if (self.parser.options.has('post-tag-guides')):
                guide = "<!-- /%s -->" % guide_str

            if (self.parser.options.has('start-guide-format')):
                format = self.parser.options.get('start-guide-format')
                try: start_guide = format % guide_str
                except: start_guide = (format + " " + guide_str).strip()
                start_guide = "%s<!-- %s -->\n" % (indent, start_guide)

            if (self.parser.options.has('end-guide-format')):
                format = self.parser.options.get('end-guide-format')
                try: end_guide = format % guide_str
                except: end_guide = (format + " " + guide_str).strip()
                end_guide = "\n%s<!-- %s -->" % (indent, end_guide)

        # When it should be expanded
        if  len(self.children) > 0 \
            or self.expand \
            or prefix or suffix \
            or (self.parser.options.has('expand-divs') and self.name == 'div'):

            for child in self.children:
                output += child.render()

            # For expand divs
            if (output == ''): output = indent + spaces + "\n"

            # Don't wrap if you're a root node
            if self.name != '':
                output = "%s%s<%s>\n%s%s</%s>%s%s\n" % (
                        start_guide, indent, self.get_tag(), output, indent, self.name, guide, end_guide)

            elif prefix or suffix:
                output = "%s%s%s%s%s\n" % \
                    (indent, prefix, output, suffix, guide)

        # Short, self-closing tags (<br />)
        elif self.name in ('area', 'base', 'basefont', 'br', 'embed', 'hr', 'input', 'img', 'link', 'param', 'meta'):
            output = "%s<%s />\n" % (indent, self.get_tag())

        # Tags with text, possibly
        elif self.name != '':
            output = "%s%s<%s>%s</%s>%s%s\n" % \
                (start_guide, indent, self.get_tag(), self.text, self.name, guide, end_guide)

        # Else, it's an empty-named element (like the root). Pass.
        else: pass


        return output

    def get_tag(self):
        output = '%s' % (self.name)
        for key, value in self.attributes.iteritems():
            output += ' %s="%s"' % (key, value)
        return output

    def append(self, object):
        self.children.append(object)

    def get_last_child(self):
        return self.children[-1]

    def _populate(self):
        """Expands with default items.

        This is called when the [[populate]] flag is turned on.
        """

        if self.name == 'ul':
            elements = [Element(token = Token('li'), parent=self, parser=self.parser)]

        elif self.name == 'dl':
            elements = [
                Element(token = Token('dt'), parent=self, parser=self.parser),
                Element(token = Token('dd'), parent=self, parser=self.parser)]

        elif self.name == 'table':
            tr = Element(token = Token('tr'), parent=self, parser=self.parser)
            td = Element(token = Token('td'), parent=tr, parser=self.parser)
            tr.children.append(td)
            elements = [tr]

        else:
            elements = []

        for el in elements:
            self.children.append(el)

    def _fill_attributes(self):
        """Fills default attributes for certain elements.
        Called by the constructor.
        """

        # Make sure <a>'s have a href, <img>'s have an src, etc.
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

        for element, attribs in required.iteritems():
            if self.name == element:
                for attrib in attribs:
                    if attrib not in self.attributes:
                        self.attributes[attrib] = attribs[attrib]

    last_child = property(get_last_child)
    parent = None
    name = ''
    attributes = None
    children = None
    text = ''
    depth = -1
    expand = False
    populate = False
    parser = None

    prefix = None
    suffix = None

# =============================================================================== 

class Token:
    def __init__(self, str):
        self.str = str.strip()
        self.attributes = {}

        # Set the type
        if self.str == '<':
            self.type = Token.PARENT
        elif self.str == '>':
            self.type = Token.CHILD
        elif self.str == '+':
            self.type = Token.SIBLING
        else:
            self.type = Token.ELEMENT
            self._init_element()
        
    def _init_element(self):
        """Initializes. Only called if the token is an element token.
        [Private]
        """
        # Get the tag name. Default to DIV if none given.
        self.name = re.findall('^(\w*)', self.str)[0]
        if (self.name == ''): self.name = 'div'
        self.name = self.name.lower()

        # Get the class names
        classes = []
        for classname in re.findall('\.([\$a-zA-Z0-9_\-\&]+)', self.str):
            classes.append(classname)
        if len(classes) > 0:
            self.attributes['class'] = ' '.join(classes)

        # Get the ID
        id = None
        for id in re.findall('#([\$a-zA-Z0-9_\-\&]+)', self.str): pass
        if id is not None:
            self.attributes['id'] = id

        # See if there's a multiplier (e.g., "li*3")
        multiplier = None
        for multiplier in re.findall('\*\s*([0-9]+)', self.str): pass
        if multiplier is not None:
            self.multiplier = int(multiplier)

        # Look for attributes
        attribs = []
        for attrib in re.findall('\[([^\]]*)\]', self.str): attribs.append(attrib)
        if len(attribs) > 0:
            for attrib in attribs:
                try:    key, value = attrib.split('=', 1)
                except: key, value = [attrib, '']
            self.attributes[key] = value

        # Try looking for text
        text = None
        for text in re.findall('\{([^\}]*)\}', self.str): pass
        if text is not None:
            self.text = text

        # Populate flag (e.g., ul+)
        flags = None
        for flags in re.findall('[\+\!]+$', self.str): pass
        if flags is not None:
            if '+' in flags: self.populate = True
            if '!' in flags: self.expand = True

    def __str__(self):
        return self.str 

    str = ''

    # For elements
    name = ''
    attributes = None
    multiplier = 1
    expand = False
    populate = False
    text = ''

    # Type
    type = 0
    ELEMENT = 2 
    CHILD = 4
    PARENT = 8
    SIBLING = 16

# =============================================================================== 

class Router:
    """The router.
    """

    # Constructor 
    # --------------------------------------------------------------------------- 

    def __init__(self):
        pass

    # Methods 
    # --------------------------------------------------------------------------- 

    def start(self, options=None):
        if (options):
            self.options = Options(router=self, options=options, argv=None)
        else:
            self.options = Options(router=self, argv=sys.argv[1:], options=None)

        if (self.options.has('help')):
            self.help()

        elif (self.options.has('version')):
            self.version()

        else:
            self.parse()
    
    def help(self):
        print "Usage: %s [OPTIONS]" % sys.argv[0]
        print "Expands input into HTML."
        print ""
        for short, long, info in self.options.cmdline_keys:
            if "Deprecated" in info: continue 
            if not short == '': short = '-%s,' % short
            if not long  == '': long  = '--%s' % long.replace("=", "=XXX")

            print "%6s %-25s %s" % (short, long, info)
        print ""
        print "\n".join(self.help_content)

    def version(self):
        print "Uhm, yeah."

    def parse(self):
        self.parser = Parser(self.options)

        try:
            # Read the files
            lines = []
            # for line in fileinput.input(): lines.append(line.rstrip(os.linesep))
            lines = [sys.stdin.read()]
            lines = " ".join(lines)

        except KeyboardInterrupt:
            pass

        except:
            sys.stderr.write("Reading failed.\n")
            return
            
        try:
            self.parser.load_string(lines)
            output = self.parser.render()
            sys.stdout.write(output)

        except:
            sys.stderr.write("Parse error. Check your input.\n")
            print sys.exc_info()[0]
            print sys.exc_info()[1]

    def exit(self):
        sys.exit()

    help_content = [
        "Please refer to the manual for more information.",
    ]

# =============================================================================== 

class Options:
    def __init__(self, router, argv, options=None):
        # Init self
        self.router = router

        # `options` can be given as a dict of stuff to preload
        if options:
            for k, v in options.iteritems():
                self.options[k] = v
            return

        # Prepare for getopt()
        short_keys, long_keys = "", []
        for short, long, info in self.cmdline_keys: # 'v', 'version'
            short_keys += short
            long_keys.append(long)

        try:
            getoptions, arguments = getopt.getopt(argv, short_keys, long_keys)

        except getopt.GetoptError:
            err = sys.exc_info()[1]
            sys.stderr.write("Options error: %s\n" % err)
            sys.stderr.write("Try --help for a list of arguments.\n")
            return router.exit()

        # Sort them out into options
        options = {}
        i = 0
        for option in getoptions:
            key, value = option # '--version', ''
            if (value == ''): value = True

            # If the key is long, write it
            if key[0:2] == '--':
                clean_key = key[2:]
                options[clean_key] = value

            # If the key is short, look for the long version of it
            elif key[0:1] == '-':
                for short, long, info in self.cmdline_keys:
                    if short == key[1:]:
                        print long
                        options[long] = True

        # Done
        for k, v in options.iteritems():
            self.options[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def get(self, attr):
        try:    return self.options[attr]
        except: return None

    def has(self, attr):
        try:    return self.options.has_key(attr)
        except: return False

    options = {
        'indent-spaces': 4
    }
    cmdline_keys = [
        ('h', 'help', 'Shows help'),
        ('v', 'version', 'Shows the version'),
        ('', 'no-guides', 'Deprecated'),
        ('', 'post-tag-guides', 'Adds comments at the end of DIV tags'),
        ('', 'textmate', 'Adds snippet info (textmate mode)'),
        ('', 'indent-spaces=', 'Indent spaces'),
        ('', 'expand-divs', 'Automatically expand divs'),
        ('', 'no-last-newline', 'Skip the trailing newline'),
        ('', 'start-guide-format=', 'To be documented'),
        ('', 'end-guide-format=', 'To be documented'),
    ]
    
    # Property: router
    # Router
    router = 1

# =============================================================================== 

if __name__ == "__main__":
    z = Router()
    z.start()
