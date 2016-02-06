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

funcdef = """\n\n
def {}():
"""
funcblock = "    {}"


def pytest_collection(session):
    print("************** SESSION *************")
    pprint.pprint(session.__dict__)
    for note in os.scandir(os.getcwd()):
        if note.name.endswith('.ipynb') and note.is_file():
            nb = nbformat.read(note.path, 4)
            filename = "test_" + note.name.replace('.ipynb', '.py')

            funcname = "Default Name"
            text = ''
            setup = False
            test_setup = []
            for cell in nb.cells:
                if cell.cell_type == 'markdown':
                    if "## Test Results" in cell.source:
                        break
                    if '## Test Configurations' in cell.source:
                        setup = True
                        continue
                    for step in ["### Given", "### And", "### When", "### Then", "### But"]:
                        if cell.source.startswith(step):
                            setup = False
                            header = cell.source.split("\n")[0]
                            header = abstract.BuiltIn().delstring(header, ["### ", '(', ')', "'", '"'])
                            funcname = header.strip().replace(" ", "_").lower()
                if cell.cell_type == 'code' and nb.metadata.kernelspec.language == 'python':
                    if setup:
                        with open(filename, "a") as pyfile:
                            pyfile.write("\n\n" + cell.source)
                        continue
                    if funcname == "Default Name":
                        continue

                    with open(filename, "a") as pyfile:
                        text = funcdef.format(funcname)
                        pyfile.write(text)
                        text = []
                        for source in cell.source.split("\n"):
                            text.append(funcblock.format(source))
                        pyfile.write("\n".join(text))


def pytest_collect_file(path, parent):
    # print("************** PATH *************")
    # print("Call No: {}".format(conf.called))
    # conf.called += 1
    # pprint.pprint(path.__dict__)
    # print("\n")
    # print("************** PARENT *************")
    # pprint.pprint(parent.__dict__)
    pass

def old_collect_file(path, parent):
    if path.ext == ".ipynb":
        return TestScenario(path, parent)


class TestScenario(pytest.File, abstract.BuiltIn):

    def collect(self):
        nb = nbformat.read(self.fspath.open(), 4)
        self.km = KernelManager()
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()
        self.name = ntpath.basename(self.name).replace(".ipynb", "")

        name = "Default Name"
        setup = False
        self.test_setup = []
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                if "## Test Results" in cell.source:
                    return
                if '## Test Configurations' in cell.source:
                    setup = True
                    continue
                for step in ["### Given", "### And", "### When", "### Then", "### But"]:
                    if cell.source.startswith(step):
                        setup = False
                        header = cell.source.split("\n")[0]
                        header = self.delstring(header, ["### ", '(', ')', "'", '"'])
                        name = header.strip().replace(" ", "_").lower()
            if cell.cell_type == 'code' and nb.metadata.kernelspec.language == 'python':
                if setup:
                    self.test_setup.append(cell.source)
                    continue
                if name == "Default Name":
                    continue
                yield TestStep(name, self, cell)

    def setup(self):
        self.km.restart_kernel()
        options = self.config.option.__dict__
        for key in options.keys():
            if key not in default_options:
                option = "{} = '{}'".format(key, options[key])
                self.kc.execute(option, allow_stdin=False)
        for setup in self.test_setup:
            self.kc.execute(setup, allow_stdin=False)

    def teardown(self):
        self.kc.execute("browser.quit()\n", allow_stdin=False)  # Quits any existing browser
        self.kc.stop_channels()
        self.km.shutdown_kernel(now=True)

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, TestException):
            return "\n".join([
                "TestItem execution failed",
                "Source:\n%s\n\n"
                "Traceback:\n%s\n" % excinfo.value.args,
            ])
        else:
            return "pytest plugin exception: %s" % str(excinfo.value)


class TestException(Exception):
    """ custom exception for error reporting. """


class TestStep(pytest.Item):

    def __init__(self, name, parent, cell):
        super(TestStep, self).__init__(name, parent)
        self.cell = cell

    def runtest(self):
        run_id = self.parent.kc.execute(self.cell.source, allow_stdin=False)
        timeout = 540 #540seconds == 9minutes
        while True:
            try:
                reply = self.parent.kc.get_shell_msg(block=True, timeout=timeout)
                if reply.get("parent_header", None) and reply["parent_header"].get("msg_id", None) == run_id:
                    break
            except Empty:
                raise TestException("Timeout of %d seconds exceeded executing cell: %s" (timeout, self.cell.source))

        if reply['content']['status'] == 'error':
            raise TestException(self.cell.source, '\n'.join(reply['content']['traceback']))
