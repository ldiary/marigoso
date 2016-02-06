import pytest
import nbformat
import ntpath
from queue import Empty
from jupyter_client import KernelManager
from marigoso import abstract
import pprint
import sys
import os
conf = sys.modules[__name__]
called = 0

default_options = ['assertmode',
                  'basetemp',
                  'cacheclear',
                  'cacheshow',
                  'capture',
                  'collectonly',
                  'color',
                  'confcutdir',
                  'debug',
                  'doctest_ignore_import_errors',
                  'doctestglob',
                  'doctestmodules',
                  'durations',
                  'exitfirst',
                  'failedfirst',
                  'file_or_dir',
                  'fulltrace',
                  'genscript',
                  'help',
                  'ignore',
                  'importmode',
                  'inifilename',
                  'junitprefix',
                  'keyword',
                  'lf',
                  'markers',
                  'markexpr',
                  'maxfail',
                  'noassert',
                  'noconftest',
                  'nomagic',
                  'pastebin',
                  'plugins',
                  'pyargs',
                  'quiet',
                  'report',
                  'reportchars',
                  'resultlog',
                  'runxfail',
                  'showfixtures',
                  'showlocals',
                  'strict',
                  'tbstyle',
                  'traceconfig',
                  'usepdb',
                  'verbose',
                  'version',
                  'xmlpath']

modvar = """
import sys
mod = sys.modules[__name__]\n
"""

fixdef = """
import pytest

@pytest.fixture(scope='session')
def configure_test():\n"""

funcdef = """\n\n
def {}(configure_test):
    test, data, browser = configure_test
"""
funcblock = "    {}"


def pytest_collection(session):

    for note in os.scandir(os.getcwd()):
        if note.name.endswith('.ipynb') and note.is_file():
            contents = []
            nb = nbformat.read(note.path, 4)
            filename = "test_" + note.name.replace('.ipynb', '.py')
            options = session.config.option.__dict__
            contents.append("#This is an automatically generated file. All manual changes to this file will be overwritten.\n")
            contents.append(modvar)
            for key in options:
                if key not in default_options:
                    option = "{} = '{}'\n".format(key, options[key])
                    contents.append(option)

            funcname = "Default Name"
            inner_func = []
            modvars = []
            setup = False
            for cell in nb.cells:
                if cell.cell_type == 'markdown':
                    if "## Test Results" in cell.source:
                        break
                    if '## Test Configurations' in cell.source:
                        contents.append(fixdef)
                        setup = True
                        continue
                    for step in ["### Given", "### And", "### When", "### Then", "### But"]:
                        if cell.source.startswith(step):
                            if setup:
                                contents.append(funcblock.format("return test, data, browser"))
                            setup = False
                            header = cell.source.split("\n")[0]
                            header = abstract.BuiltIn().delstring(header, ["### ", '(', ')', "'", '"'])
                            latest_funcname = header.strip().replace(" ", "_").lower()
                            if latest_funcname != funcname:
                                if inner_func:
                                    contents.append("\n\n\n")
                                    contents.extend(inner_func)
                                    inner_func = []
                                funcname = latest_funcname
                if cell.cell_type == 'code' and nb.metadata.kernelspec.language == 'python':
                    if setup:
                        for source in cell.source.split("\n"):
                            contents.append(funcblock.format(source))
                        contents.append("\n")
                        continue
                    if funcname == "Default Name":
                        continue

                    contents.append(funcdef.format(funcname))
                    inner = False
                    for source in cell.source.split("\n"):
                        if " = " in source:
                            variable, _, _ = source.partition(" = ")
                            modvars.append(variable)
                        if source.startswith("def"):
                            inner_func.append(source)
                            inner = True
                            continue
                        if inner:
                            if source.startswith("    "):
                                inner_func.append(source)
                                continue
                            else:
                                inner = False
                        contents.append(funcblock.format(source))
        with open(filename, 'w') as pyfile:
            pyfile.write("\n".join(contents))
        pprint.pprint(modvars)
