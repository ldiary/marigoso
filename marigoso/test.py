# External Package dependencies
#import requests
from selenium.webdriver import Firefox, Ie, PhantomJS, Chrome, Safari, DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# Python built-in Packages
import types
import os
import sys
import inspect
import importlib
import configparser
import pprint

from pathlib import Path, PurePath
#TODO: convert os.path to pathlib.Path/PurePath
#TODO: convert request['django']['path'] to request.django.path

# Internal Modules
from . import abstract, browser, interface


class TestException(Exception):
    """Test exceptions."""


class Test(object):
    """
    A Test instance should have the following attributes that are often necessary to execute a test:
         DEFAULT Attributes
         1. data - a mutant dictionary which you can use both key referencing and dot notation to retrieve values
         2. request - a copy of parameters passed to Test instance initialization

         OPTIONAL Attributes
         1. configparser - by calling self.setup_config_parser()
         2. browser - by calling self.launch_browser()
    """

    def __init__(self, request=None):
        self.data = abstract.MutantDictionary()
        self.request = request
        self.pp = pprint.PrettyPrinter(indent=4)

    def setup_notebooks(self, parent, subfolder=None):
        return abstract.Utils().import_parent_folders(parent, subfolder)

    def setup_django_models(self, request=None):
        request = request or self.request
        if 'django' in request:
            self.models = abstract.MutantDictionary()
            self.get_django_models(request)

    def setup_config_parser(self, request=None):
        """Creates a ConfigParser, attach a reference of it to the Test instance
        and returns the ConfigParser instance."""

        def data(self, key, section=None):
            section = section or self.sections()[0]
            return self.get(section, key)

        request = request or self.request
        if isinstance(request, str):
            # convert it into a dictionary
            request = {
                'configparser': request
            }
            # then replace self.request if it's not defined yet
            try:
                self.request.update(request)
            except AttributeError:
                self.request = request

        if 'configparser' in request:
            self.configparser = configparser.ConfigParser()
            self.configparser.read(request['configparser'])
            setattr(self.configparser, 'data', types.MethodType(data, self.configparser))
            return self.configparser
        raise TestException("A configuration file was not specified.")

    def setup_proxy(self, request=None):
        request = request or self.request
        if 'proxy' in request:
            pass
            """uncomment this to enable browsermobproxy
            from browsermobproxy import Server
            self.server = Server(request['proxy'])
            self.server.start()
            self.proxy = self.server.create_proxy()
            selenium_proxy = self.proxy.selenium_proxy()"""
        else:
            selenium_proxy = None
        return selenium_proxy

    # def enable_api(self, request=None):
    #     self.api = abstract.MutantDictionary()
    #     self.api.session = requests.Session()
    #     requests.packages.urllib3.disable_warnings()
    #     self.api.session.headers = {'content-type': 'application/json'}
    #     self.api.session.verify = False
    #     self.api.codes = requests.codes
    #     self.api._requests = requests
    #     self.api.pp = self.pp
    #     self.register_modules("api", [abstract, interface])
    #     return self.api

    def launch_browser(self, request=None):
        request = request or self.request
        if isinstance(request, str):
            request = {
                'browser': request
            }
            try:
                self.request.update(request)
                request = self.request
            except AttributeError:
                self.request = request
        if 'browser' in request:
            capabilities_map = {
                "Firefox":      DesiredCapabilities.FIREFOX,
                "IExplorer":    DesiredCapabilities.INTERNETEXPLORER,
                "Chrome":       DesiredCapabilities.CHROME,
                "PhantomJS":    DesiredCapabilities.PHANTOMJS,
                "Safari":       DesiredCapabilities.SAFARI,
            }
            caps = capabilities_map[request['browser']]

            ############################################
            ### Firefox
            ############################################
            if request['browser'] == 'Firefox':
                firefox_profile = FirefoxProfile()
                if 'firefox' in request:
                    if 'preferences' in request['firefox']:
                        for preference in request['firefox']['preferences']:
                            firefox_profile.set_preference(*preference)
                    if 'extensions' in request['firefox']:
                        for extension in request['firefox']['extensions']:
                            extension = PurePath(request['firefox']['extensions_path'], extension)
                            firefox_profile.add_extension(str(extension))
                    if 'mime' in request['firefox']:
                        import shutil
                        shutil.copy2(request['firefox']['mime'], firefox_profile.profile_dir)
                    if 'capabilities' in request['firefox']:
                        caps.update(request['firefox']['capabilities'])
                selenium_proxy = self.setup_proxy()
                class Mixin(Firefox, browser.BrowsingActions): pass
                self.browser = Mixin(firefox_profile, proxy=selenium_proxy, capabilities=caps)

            ############################################
            ### Internet Explorer
            ############################################
            elif request['browser'] == 'IExplorer':
                # Not a good idea => caps['nativeEvents'] = False
                iedriver_server = os.path.join(request['iexplorer']['server_path'],
                                               request['iexplorer']['server_file'])
                class Mixin(Ie, browser.BrowsingActions): pass
                self.browser = Mixin(iedriver_server, capabilities=caps)

            ############################################
            ### GhostDriver, PhantomJS
            ############################################
            elif request['browser'] == 'PhantomJS':
                service_args = ["--ignore-ssl-errors=yes"]
                caps['phantomjs.page.settings.userAgent'] = (
                    'Mozilla/5.0 (Windows NT'
                    ' 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
                )

                class Mixin(PhantomJS, browser.BrowsingActions): pass
                self.browser = Mixin(service_args=service_args,
                                         desired_capabilities=caps)
                # If you don't do this, you'll get the pain:
                # https://github.com/angular/protractor/issues/585
                self.browser.set_window_size(1024, 768)

            ############################################
            ### Chrome
            ############################################
            elif request['browser'] == 'Chrome':
                chromedriver_server = os.path.join(request['chrome']['server_path'],
                                                   request['chrome']['server_file'])
                os.environ["webdriver.chrome.driver"] = chromedriver_server
                class Mixin(Chrome, browser.BrowsingActions): pass
                self.browser = Mixin(chromedriver_server)

            ############################################
            ### Safari
            ############################################
            elif request['browser'] == 'Safari':
                selenium_server = os.path.join(request['safari']['server_path'],
                                               request['safari']['server_file'])
                class Mixin(Safari, browser.BrowsingActions): pass
                self.browser = Mixin(selenium_server)
            return self.browser

        print("Please specify which browser to launch.")
        assert 'browser' in request

    def register_functions(self, attr_name, *functions):
        """
        :param attr_name: The name of the attribute that will be attached to the test object.
        :param functions: A sequence of functions that will be attached
                           to the test object using the attribute mentioned above.
        :return: None
        """
        for func in functions:
            _attribute = getattr(self, attr_name)
            setattr(_attribute, func.__name__, types.MethodType(func, _attribute))

    def register_modules(self, attr_name, *modules):
        """Register module defined functions to an attribute of the test object."""
        for mod in modules:
            for func_name, func in inspect.getmembers(mod, inspect.isfunction):
                _attribute = getattr(self, attr_name)
                setattr(_attribute, func_name, types.MethodType(func, _attribute))

    def register_classes(self, *args):
        """This generates high level classes which inherits all the capabilities of the humble browser.
        For example, if you have class 'Angora' inside the module you passed into this method,
        you can then use it like 'test.Angora.get_element(locator)' because the 'Angora' attribute of 'test'
        is a mutated 'browser' object."""
        class SubBrowser(self.browser.__class__):

            def __init__(self, browser):
                self.__dict__.update(browser.__dict__)

        for mod in args:
            for cls_name, cls in inspect.getmembers(mod, inspect.isclass):
                if not hasattr(self, cls_name):
                    setattr(self, cls_name, SubBrowser(self.browser))
                _attribute = getattr(self, cls_name)
                for func_name, func in inspect.getmembers(cls, inspect.isfunction):
                    setattr(_attribute, func_name, types.MethodType(func, _attribute))

    def reload_modules(self, *modules):
        """This is useful when you have edited a module and you want this edited version to be updated in your
        currently running jupyter notebook."""
        for module in modules:
            importlib.reload(module)

    def get_django_models(self, request):
        # Setup Django
        if str(request['django']['path']) not in sys.path:
            sys.path.append(request['django']['path'])
        if not 'DJANGO_SETTINGS_MODULE' in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = "{}.settings".format(request['django']['name'])
        import django
        django.setup()

        for app in request['django']['apps'].keys():
            app_models = importlib.import_module("{}.models".format(app))
            for model in request['django']['apps'][app]:
                self.models[model] = getattr(app_models, model)
