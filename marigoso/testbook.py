import pytest
import nbformat
import ntpath
import re
import pprint
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
                        self.header = cell.source.split("\n")[0].replace("### ", "")
                        header = self.delstring(self.header, ["### ", '(', ')', "'", '"'])
                        self.header = ".".join([self.name, self.header])
                        name = header.strip().replace(" ", "_").lower()
            if cell.cell_type == 'code' and nb.metadata.kernelspec.language == 'python':
                if setup:
                    self.test_setup.append(cell.source)
                    continue
                if name == "Default Name":
                    continue
                yield TestStep(self.header, name, self, cell)

    def setup(self):
        self.km.restart_kernel()
        options = self.config.option.__dict__
        for key in options.keys():
            if key not in default_options:
                option = "{} = '{}'".format(key, options[key])
                self.kc.execute(option, allow_stdin=False)
        for setup in self.test_setup:
            send_and_execute(self.kc, setup, allow_stdin=False)

    def teardown(self):
        self.kc.execute("browser.quit()\n", allow_stdin=False)  # Quits any existing browser
        self.kc.stop_channels()
        self.km.shutdown_kernel(now=True)


class TestException(Exception):
    """ custom exception for error reporting. """


def send_and_execute(kernel, source, item=None, allow_stdin=False):
    run_id = kernel.execute(source, allow_stdin=allow_stdin)
    timeout = 1800  # 1800seconds == 30minutes
    while True:
        try:
            reply = kernel.get_shell_msg(block=True, timeout=timeout)
            if reply.get("parent_header", None) and reply["parent_header"].get("msg_id", None) == run_id:
                break
        except Empty:
            raise TestException("Timeout of %d seconds exceeded executing cell: %s"(timeout, source))

    if reply['content']['status'] == 'ok':
        return "Test successfully completed."

    elif reply['content']['status'] == 'error':
        _traceback = reply['content']['traceback']
        if isinstance(item, TestStep):
            item._location = (item._location[0], item._location[1], item.header)
            if item.config.getvalue("color") == 'yes':
                setattr(item, 'traceback', "\n".join(_traceback))
            else:
                ansi_escape = re.compile(r'\x1b[^m]*m')
                setattr(item, 'traceback', ansi_escape.sub('', "\n".join(_traceback)))
        raise TestException(source, _traceback)

    elif reply['content']['status'] == 'aborted':
        raise TestException(source, "Test was aborted")
    else:
        pprint.pprint(reply)
        pprint.pprint(reply['content'])
        raise TestException(source, "Unknown Status Code")


class TestStep(pytest.Item, abstract.Utils):

    def __init__(self, header, name, parent, cell):
        super(TestStep, self).__init__(name, parent)
        self.header = header
        self.cell = cell

    def runtest(self):
        send_and_execute(self.parent.kc, self.cell.source, item=self, allow_stdin = False)

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, TestException):
            try:
                return ("\n\n".join([self.cell.source, self.traceback]))
            except AttributeError:
                return ("\n\n".join([self.cell.source, "\n".join(excinfo.value.args)]))
        else:
            return super(TestStep, self).repr_failure(excinfo)