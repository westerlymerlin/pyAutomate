"""
Documentation Generator for Python Projects

This module automatically generates Markdown documentation from Python docstrings
and comments. It's designed to run in a GitHub Action workflow against the main
branch of a repository.

The generator:
1. Scans specified directories for Python modules
2. Extracts docstrings and comments using pydoc-markdown
3. Creates individual Markdown files for each module
4. Generates a consolidated readme.md with links to all module documentation

Dependencies:
- pydoc-markdown: Used to parse Python code and generate documentation

Configuration:
- DOCSPATH: Output directory for generated documentation
- SEARCHPATHS: List of directories to scan for Python modules
- SKIPNAMES: List of module name patterns to exclude from documentation

Usage:
    python document_from_code.py

The output will be a set of Markdown files in the specified DOCSPATH directory.

-----------------------------------------------------------------------------------
Copyright (C) 2025 Gary Twinn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Author: Gary Twinn
--------------------------------------------------------------------------------
"""

import os
import time
from pydoc_markdown.interfaces import Context
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer

CODEBLOCK: str = '\n  \n-------\n#### Copyright (C) YYYY Gary Twinn  \n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.  \n  \nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see <https://www.gnu.org/licenses/>.  \n  \n  #####Author: Gary Twinn  \n  \n ----------------------------'



DOCSPATH = './docs'
SEARCHPATHS = ['../', '../ui/']
SKIPNAMES = ['ui_layout_', 'main_rc', 'RPi', 'test', 'venv', 'document_from_code']

def checkmodule(name):
    """Check if a module is valid for documentation"""
    for item in SKIPNAMES:
        if item in name:
            print('Module %s skipped' % name)
            return False
    print('Module %s processed' % name)
    return True

def create_docs():
    """Create the documents for the project"""
    print('docs path = %s\nsearch paths = %s\nCreating documentation ' % (DOCSPATH, SEARCHPATHS))
    if not os.path.exists(DOCSPATH):
        os.makedirs(DOCSPATH)
    context = Context(directory=DOCSPATH)
    loader = PythonLoader()
    loader.search_path = SEARCHPATHS
    loader.module_level_importable = False
    loader.init(context)
    renderer = MarkdownRenderer()
    renderer.init(context)
    modules = loader.load()
    linedata=[]
    for module in modules:
        if checkmodule(module.name):
            linedata.append([[module.name], [module.docstring]])
            renderer.filename = DOCSPATH + '/' + module.name + '.md'
            renderer.render_toc_title = 'Contents for: ' + module.name
            renderer.render_toc = False
            renderer.render_page_title = True
            renderer.code_headers = False
            renderer.process([module], None)
            renderer.render([module])
    linedata.sort()
    print("\nGenerating readme.md file in docs folder")
    with open( DOCSPATH + '/readme.md', 'w', encoding='utf8') as outfile:
        print('# Module Documentation\n\n', file=outfile)
        print('This document contains the documentation for all the modules in this project.\n\n---\n', file=outfile)
        print('## Contents\n\n', file=outfile)
        for item in linedata:
            module = item[0][0]
            filename = item[0][0] + '.md'
            docstring = item[1][0]
            description = docstring.content
            line_item = '[%s](./%s)  ' % (module, filename)
            print(line_item, file=outfile)
            line_item = '%s\n' % description
            print(line_item, file=outfile)
        print('\n---\n', file=outfile)
        print(CODEBLOCK.replace('YYYY', str(time.localtime().tm_year)), file=outfile)
    outfile.close()
    print('\n\n*** files in Docs path ***\n')
    files = os.listdir(DOCSPATH)
    for item in files:
        print(item)

if __name__ == '__main__':
    create_docs()
