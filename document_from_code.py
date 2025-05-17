"""Gerates documentation from comments in the code
Coded to run in a github action against the master branch
uses:
pydoc-markdown to generate the documentation
"""

import os
from pydoc_markdown.interfaces import Context
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer


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
            renderer.render_toc = True
            renderer.render_page_title = False
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
    outfile.close()
    print('\n\n*** files in Docs path ***\n')
    files = os.listdir(DOCSPATH)
    for item in files:
        print(item)

if __name__ == '__main__':
    create_docs()
