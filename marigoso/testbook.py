"""
This is a pytest plugin which will convert bdd-style tests written in Jupyter (IPython Notebook) into a pytest
discoverable and runnable tests. This plugin will auto-generate a python file which pytest will then execute.
"""
import nbformat
from marigoso import abstract
import pprint
import sys
import os
conf = sys.modules[__name__]
called = 0
autogenfiles = []

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
import importlib
import sys
mod = sys.modules[__name__]\n
"""

fixdef = """
import pytest

@pytest.fixture(scope='session')
def configure_test():
    global test
    global data
    global browser
"""

funcdef = """\n\n
def {}(configure_test):
    global test
    global data
    global browser
"""
funcblock = "    {}"


def pytest_collection(session):

    # Note that this is a replacement to the old method of executing the test by running a jupyter kernel.
    # This method auto-generate a test file which can then be discovered and executed by pytest without
    # using the jupyter kernel. The advantage of this approach is that we get a more readable stacktrace
    # when test fails. This might change again in the future once we know how to correctly handle and display
    # stacktrace provided by the jupyter kernel to the pytest terminal writer.
    for note in os.scandir(os.getcwd()):
        if note.name.endswith('.ipynb') and note.is_file():
            contents = []
            nb = nbformat.read(note.path, 4)
            filename = "test_" + note.name.replace('.ipynb', '.py')
            filename = filename.replace("-", "_")
            fileprefix = abstract.BuiltIn().delstring(note.name, [".ipynb", "'", "[", "]", "(", ")", "-"])
            fileprefix = "_" + fileprefix.replace(" ", "_")
            options = session.config.option.__dict__
            contents.append("#This is an auto-generated file. All manual changes to this file will be overwritten.")
            contents.append(modvar)
            contents.append("test = None")
            contents.append("data = None")
            contents.append("browser = None")
            modvars = ["test", "data", "browser"]

            funcname = "Default Name"
            inner_func = []
            setup = False
            for cell in nb.cells:
                if cell.cell_type == 'markdown':
                    if "## Test Results" in cell.source:
                        break
                    if '## Test Configurations' in cell.source:
                        contents.append(fixdef.replace('_test', fileprefix))
                        for key in options:
                            if key not in default_options:
                                option = "    {} = '{}'".format(key, options[key])
                                contents.append(option)
                        setup = True
                        continue
                    for step in ["### Given", "### And", "### When", "### Then", "### But"]:
                        if cell.source.startswith(step):
                            setup = False
                            header = cell.source.split("\n")[0]
                            header = abstract.BuiltIn().delstring(header, ["### ", '(', ')', "'", '"'])
                            latest_funcname = header.strip().replace(" ", "_").replace("-", "_").lower()
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
                            if "import " in source and "from " not in source:
                                _, _, right = source.partition("import ")
                                contents.append("    importlib.reload({})".format(right))
                        contents.append("\n")
                        continue
                    if funcname == "Default Name":
                        continue

                    contents.append(funcdef.replace("_test", fileprefix).format(funcname))
                    inner = False
                    for source in cell.source.split("\n"):
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

                        if " = " in source:
                            left, equals, right = source.partition(" = ")
                            variable = left.strip()
                            if "." in variable:
                                variable, _, _ = variable.partition(".")
                            if variable not in ["test", "data", "browser"]:
                                source = "".join([left.replace(variable, "mod." + variable), equals, right])
                            if variable not in modvars:
                                if type(variable) is list:
                                    contents.insert(2, "".join([str(variable), " = []"]))
                                elif type(variable) is dict:
                                    contents.insert(2, "".join([str(variable), " = {}"]))
                                else:
                                    contents.insert(2, "".join([str(variable), " = None"]))
                                modvars.append(variable)
                        contents.append(funcblock.format(source))

            with open(filename, 'w') as pyfile:
                pyfile.write("\n".join(contents))
            autogenfiles.append(filename)


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 0:
        for pyfile in conf.autogenfiles:
            if os.path.isfile(pyfile):
                os.remove(pyfile)
