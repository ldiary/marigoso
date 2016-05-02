import pytest
import nbformat
import ntpath
import re
from queue import Empty
from jupyter_client import KernelManager
from marigoso import abstract


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


def pytest_collect_file(parent, path):
    if path.ext == ".ipynb":
        return TestScenario(path, parent)


class TestScenario(pytest.File, abstract.Utils):

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
                if '## Test Configurations' in cell.source or '## Environmental Needs' in cell.source:
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


class TestStep(pytest.Item, abstract.Utils):

    def __init__(self, name, parent, cell):
        super(TestStep, self).__init__(name, parent)
        self.cell = cell

    def runtest(self):
        run_id = self.parent.kc.execute(self.cell.source, allow_stdin=False)
        timeout = 1800 #1800seconds == 30minutes
        while True:
            try:
                reply = self.parent.kc.get_shell_msg(block=True, timeout=timeout)
                if reply.get("parent_header", None) and reply["parent_header"].get("msg_id", None) == run_id:
                    break
            except Empty:
                raise TestException("Timeout of %d seconds exceeded executing cell: %s" (timeout, self.cell.source))

        if reply['content']['status'] == 'error':
            _traceback = reply['content']['traceback']
            if self.config.getvalue("color") == 'yes':
                setattr(self, 'traceback', _traceback)
            else:
                ansi_escape = re.compile(r'\x1b[^m]*m')
                setattr(self, 'traceback', ansi_escape.sub('', "\n".join(_traceback)))
            raise TestException(self.cell.source, _traceback)
