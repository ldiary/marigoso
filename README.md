Jupyter for BDD Testing in Python
=================================
Marigoso can help you create automated unit tests and functional tests (for end to end testing) 
which can be shared between Manual Testers and Automation Engineers. When you import marigoso in your Jupyter Notebook
you will be able to create a single executable file which contains not only automation code, but manual steps as well.

Tests can be written using BDD (Gherkin) style and the manner of test execution can be step by step or all in one go. 
When test fails during automated execution, the automation engineer can debug the code directly using Jupyter, while the
 manual tester always have the option to easily carry on manually, due to the fact that manual steps are also included in the same file.

Installation
============

```
pip install -U marigoso
```

Usage
============

Create an instance of marigoso Test.
```
from marigoso import Test
test = Test()
```

Use the browser testing tool.
```
test.launch_browser("Firefox")
test.browser.get_url("http://pytestuk.blogspot.co.uk/2015/11/testing.html")
test.browser.press_available("id=cookieChoiceDismiss")
iframe = test.browser.get_element("css=div#bc_0_0T_box iframe")
test.browser.switch_to.frame(iframe)
test.browser.kb_type("id=commentBodyField", "An example of Selenium automation in Python.")
test.browser.select_text("id=identityMenu", "Google Account")
test.browser.submit_btn("Publish")
test.browser.quit()
```
Browser tool offers convenient functions for handling [Selenium](http://seleniumhq.github.io/selenium/docs/api/py/) Python bindings.


Use the API testing tool.
```
test.enable_api()
test.api.host = "https://your.api.host.net"
test.api.session.auth = ('my_username', 'my_password')
response = test.api.get_request("/your/api/route")
test.api.check_fields(['field1', 'field2'], response)
```
API tool offers convenient functions for handling [Requests](http://docs.python-requests.org/en/latest/) Python module.

Tutorials
=========
[Using Marigoso to Post a Comment in Blogger](https://github.com/ldiary/marigoso/blob/master/notes/using_marigoso_to_post_a_comment_in_blogger_post.ipynb)