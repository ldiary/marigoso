import types
import datetime
from .abstract import Utils
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from contextlib import contextmanager


ONE, ALL, TIMEOUT = 0, 1, 5


def get_element(self, coordinate, child=None, _all=None, timeout=TIMEOUT, stealth=None):
    find = {
        'css=':   ("find_element_by_css_selector", "find_elements_by_css_selector"),
        'xpath=': ("find_element_by_xpath", "find_elements_by_xpath"),
        'link=':  ("find_element_by_link_text", "find_elements_by_link_text"),
        'class=': ("find_element_by_class_name", "find_elements_by_class_name"),
        'id=':    ("find_element_by_id", "find_elements_by_id"),
        'name=':  ("find_element_by_name", "find_elements_by_name"),
        'plink=': ("find_element_by_partial_link_text", "find_elements_by_partial_link_text"),
        'tag=':   ("find_element_by_tag_name", "find_elements_by_tag_name")
    }

    def wait_for(_self, method, locator, timeout=TIMEOUT, stealth=None):
        """Wait until the element specified by the given locator (i.e. string selector) is displayed to the user."""
        status = "Unknown"
        for index in range(timeout):
            try:
                _element = method(locator)
                if stealth:
                    # When we want to interact with the element even when it's not displayed.
                    return _element
                try:
                    if _element.is_displayed():
                        return _element
                # When we get a list of element instead of a single element, we check if any of them is visible
                except AttributeError:
                    for _lmn in _element:
                        if _lmn.is_displayed():
                            return _element
                status = "Not Displayed"
            except (NoSuchElementException, StaleElementReferenceException) as e:
                status = "Not Found" if isinstance(e, NoSuchElementException) else "Stale Element"
            _self.wait(1)
        raise BrowserException("wait_for({}, {}, {}), timeout reached; Status: {}".format(
            method.__name__, locator, timeout, status), status=status)

    def get_children(_self, coordinate, timeout=TIMEOUT, stealth=None):
        return _self.get_child(coordinate, _all=True, timeout=timeout, stealth=stealth)

    if isinstance(coordinate, str):
        if "=" not in coordinate:
            if _all is None:
                return wait_for(self, getattr(self, find['link='][ONE]), coordinate, timeout, stealth)
            return wait_for(self, getattr(self, find['link='][ALL]), coordinate, timeout, stealth)
        reference, locator = self, coordinate
    else:
        reference, locator = coordinate, child

    # Try the most commonly used selectors
    for by in ['css=', 'xpath=', 'id=', 'name=', 'tag=', 'class=', 'plink', 'link']:
        if locator.startswith(by):
            locator = locator.replace(by, '')
            if _all is None:
                # Get the element returned by wait_for
                element = wait_for(self, getattr(reference, find[by][ONE]), locator, timeout, stealth)
                # Give the element the ability to grab displayed element
                element.wait_for = types.MethodType(wait_for, element)
                # Give the element the ability to get a child or all children
                element.get_child = types.MethodType(get_element, element)
                element.get_children = types.MethodType(get_children, element)
                # Return the groomed element
                return element
            else:
                # Get the elements returned by wait_for
                elements = wait_for(self, getattr(reference, find[by][ALL]), locator, timeout, stealth)
                for element in elements:
                    element.wait_for = types.MethodType(wait_for, element)
                    element.wait = types.MethodType(Utils().wait, element)
                    element.get_child = types.MethodType(get_element, element)
                    element.get_children = types.MethodType(get_children, element)
                return elements
    raise BrowserException("Locator: {} does not start with known by method.".format(coordinate), "Invalid Locator")


class BrowserException(Exception):

    def __init__(self, message, status=None):
        super(BrowserException, self).__init__(message)
        self.status = status


class DOM(Utils):

    @property
    def url(self):
        return self.current_url

    def get_all(self, coordinate, timeout=TIMEOUT):
        return self.get_element(coordinate, _all=True, timeout=timeout)

    def get_stealth(self, coordinate, timeout=TIMEOUT):
        return self.get_element(coordinate, timeout=timeout, stealth=True)

    def get_element(self, coordinate, child=None, _all=None, timeout=TIMEOUT, stealth=None):
        # We're using '_all' instead of the Python keyword 'all'
        return get_element(self, coordinate, child, _all, timeout=timeout, stealth=stealth)

    def is_available(self, coordinate, timeout=TIMEOUT):
        if isinstance(coordinate, str):
            try:
                return self.get_element(coordinate, timeout)
            except BrowserException as e:
                if e.status in ['Not Displayed', 'Not Found']:
                    return False
                raise e
        return coordinate.is_displayed()

    def switch_frame(self, coordinate):
        if isinstance(coordinate, str):
            element = self.get_element(coordinate)
        else:
            element = coordinate
        self.switch_to.frame(element)


class KeyBoard(DOM):

    def kb_type(self, coordinate, text, clear=None):
        if isinstance(coordinate, str):
            element = self.get_element(coordinate)
        else:
            element = coordinate
        element.click()
        element.clear()
        if clear is not None:
            for _ in range(clear):
                element.send_keys(Keys.ARROW_RIGHT)
                element.send_keys(Keys.BACKSPACE)
        element.send_keys(text)


class Mouse(DOM):

    def press(self, coordinate, success=None):
        """Success must be given as a tuple of a (coordinate, timeout).
        Use (coordinate,) if you want to use the default timeout."""
        if isinstance(coordinate, WebElement):
            coordinate.click()
        else:
            self.get_element(coordinate).click()
        if success is not None:
            assert self.is_available(*success)

    def press_available(self, coordinate, timeout=2):
        if self.is_available(coordinate, timeout):
            self.press(coordinate)

    def select_text(self, coordinate, text, select2drop=None):
        '''
        :param an element or a locator of the select element
        :param a selection text or selection index to be selected
        :param the select2 dropdown locator
        :return: True
        '''
        if not isinstance(coordinate, Select):
            if isinstance(coordinate, str):
                element = self.get_element(coordinate)
            else:
                element = coordinate
            if element.tag_name.lower() != "select":
                # Selenium's Select does not support non-select tags
                return self.select2(element, select2drop, text)
            selection = Select(element)
        else:
            selection = coordinate
            # TODO: Can't understand why Select made it private, replace Select in the future(?)
            element = coordinate._el
        if isinstance(text, int):
            if select2drop is not None:
                return self.select2(element, select2drop, text)
            return selection.select_by_index(text)
        try:
            selection.select_by_visible_text(text)
            return True
        except NoSuchElementException:
            available_selections = []
            for option in selection.options:
                if text in option.text:
                    selection.select_by_visible_text(option.text)
                    return True
                available_selections.append(option.text)
            print("[Error!] Selection not found: {}".format(text))
            print("Available Selections\n {}".format(available_selections))
        except ValueError:
            if select2drop is None:
                print("[Hint] You might be dealing with a select2 element. Try specifying select2drop locator.")
                raise
            # We are assuming we encountered a select2 selection box
            self.select2(element, select2drop, text)

    def select2(self, box, drop, text):
        '''
        :param box: the locator for Selection Box
        :param drop: the locator for Selection Dropdown
        :param text: the text value to select or the index of the option to select
        :return: True
        :example: https://github.com/ldiary/marigoso/blob/master/notebooks/handling_select2_controls_in_selenium_webdriver.ipynb
        '''
        if not self.is_available(drop):
            if isinstance(box, str):
                self.get_element(box).click()
            else:
                box.click()
        ul_dropdown = self.get_element(drop)
        options = ul_dropdown.get_children('tag=li')
        if isinstance(text, int):
            options[text].click()
            return True

        for option in options:
            if option.text == text:
                option.click()
                return True
        print("[Error!] Selection not found: {}".format(text))
        print("Available Selections\n {}".format([option.text for option in options]))

    def submit_btn(self, value, success=None):
        """This presses an input button with type=submit.
        Success must be given as a tuple of a (coordinate, timeout).
        Use (coordinate,) if you want to use the default timeout."""
        self.press("css=input[value='{}']".format(value))
        if success is not None:
            assert self.is_available(*success)


class BrowsingActions(Mouse, KeyBoard):

    def accept_alert(self):
        if self.name == 'phantomjs':
            # http://stackoverflow.com/questions/15708518/how-can-i-handle-an-alert-with-ghostdriver-via-python
            self.execute_script("window.confirm = function(){return true;}")
        else:
            self.switch_to.alert.accept()

    def get_url(self, url):
        if not url:
            print("URL can not be empty or None. Given: {}".format(url))
            assert url
        self.get(url)
        if self.name == 'internet explorer':
            self.press_available("css=a#overridelink")

    def iexplorer_wait(self, seconds):
        # TODO: This is a temporary workaround until we figure out
        # how to make iexplorer wait for page to load completely before performing operations
        if self.name == 'internet explorer':
            self.wait(seconds)

    def scroll(self, coordinate):
        if isinstance(coordinate, str):
            element = self.get_element(coordinate)
        else:
            element = coordinate
        self.execute_script("arguments[0].scrollIntoView(true);", element)

    def screenshot(self, name):
        name = self.time_unique(name) + ".png"
        self.get_screenshot_as_file(name)
        self.log(name)
        self.log(self.url)
        return name

    @contextmanager
    def page_will_reload(self, coordinate, timeout=30):
        if isinstance(coordinate, str):
            element = self.get_element(coordinate)
        else:
            element = coordinate
        yield
        start = datetime.datetime.utcnow()
        while True:
            try:
                element.is_enabled()
                seconds = self.timelapse(start, unit='seconds')
            except StaleElementReferenceException:
                break
            if seconds > timeout:
                status = "{} is enabled = {}".format(coordinate, element.is_enabled())
                raise BrowserException("Timed out waiting for an expected page reload.", status=status)

    @contextmanager
    def alert_will_popup(self, text, timeout=30):
        try:
            self.switch_to.alert.text
        except NoAlertPresentException:
            pass
        yield
        start = datetime.datetime.utcnow()
        while True:
            try:
                return self.switch_to.alert.text == text
            except NoAlertPresentException:
                pass
            seconds = self.timelapse(start, unit='seconds')
            if seconds > timeout:
                raise BrowserException("Timed out waiting for an expected alert\n{}.".format(text))