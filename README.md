Simpler Selenium
================
You can use Selenium functions to automatically interact with the web elements being rendered in a browser.
However, some of these Selenium functions have too long names and are pretty much confusing. 

Therefore, instead of using Selenium directly, you can use Marigoso as a layer on top of Selenium. Marigoso gives you
more convenient functions so you don't need to remember long Selenium function names.

Instead of coding like this:
```
from selenium import webdriver
browser = webdriver.Firefox()
browser.get('https://python.org.')
download = browser.find_element_by_link_text('Downloads')
download.click()
download = browser.find_element_by_id('downloads')
ul = download.find_element_by_tag_name('ul')
lis = ul.find_elements_by_tag_name('li')
for index, li in enumerate(lis):
    print("{}: {}".format(index, li.text))
```

You can make your code look a little better like this:
```
from marigoso import Test
browser = Test().launch_browser('Firefox')
browser.get_url('https://python.org')
browser.press('Downloads')
download = browser.get_element('id=downloads')
ul = download.get_child('tag=ul')
lis = ul.get_children('tag=li')
for index, li in enumerate(lis):
    print("{}: {}".format(index, li.text))
```

Getting a Single Web Element from a Web Page

|Marigoso | Selenium|
|:-------|------------------------------------------------------------------------|
|get_element("css=xxx")  | *find_element_by_css_selector("xxx")*|
|get_element("xpath=xxx")| *find_element_by_xpath("xxx")*|
|get_element("xxx")      | *find_element_by_link_text("xxx")*|
|get_element("class=xxx")| *find_element_by_class_name("xxx")*|
|get_element("id=xxx")   | *find_element_by_id("xxx")*|
|get_element("name=xxx") | *find_element_by_name("xxx")* |
|get_element("plink=xxx")| *find_element_by_partial_link_text("xxx")*|
|get_element("tag=xxx")  | *find_element_by_tag_name("xxx")*|


Getting Multiple Web Elements from a Web Page

|Marigoso | Selenium|
|:-------|------------------------------------------------------------------------|
|get_all("css=xxx")   | *find_elements_by_css_selector("xxx")*|
|get_all("xpath=xxx") | *find_elements_by_xpath("xxx")*|
|get_all("xxx")       | *find_elements_by_link_text("xxx")*|
|get_all("class=xxx") | *find_elements_by_class_name("xxx")*|
|get_all("id=xxx")    | *find_elements_by_id("xxx")*|
|get_all("name=xxx")  | *find_elements_by_name("xxx")* |
|get_all("plink=xxx") | *find_elements_by_partial_link_text("xxx")*|
|get_all("tag=xxx")   | *find_elements_by_tag_name("xxx")*|


Getting a Single Web Element from a given Web Element

|Marigoso | Selenium|
|:-------|------------------------------------------------------------------------|
|element.get_child("css=xxx")  | *element.find_element_by_css_selector("xxx")*|
|element.get_child("xpath=xxx")| *element.find_element_by_xpath("xxx")*|
|element.get_child("xxx")      | *element.find_element_by_link_text("xxx")*|
|element.get_child("class=xxx")| *element.find_element_by_class_name("xxx")*|
|element.get_child("id=xxx")   | *element.find_element_by_id("xxx")*|
|element.get_child("name=xxx") | *element.find_element_by_name("xxx")* |
|element.get_child("plink=xxx")| *element.find_element_by_partial_link_text("xxx")*|
|element.get_child("tag=xxx")  | *element.find_element_by_tag_name("xxx")*|


Getting Multiple Web Elements from a given Web Element

|Marigoso | Selenium|
|:-------|------------------------------------------------------------------------|
|element.get_children("css=xxx")   | *element.find_elements_by_css_selector("xxx")*|
|element.get_children("xpath=xxx") | *element.find_elements_by_xpath("xxx")*|
|element.get_children("xxx")       | *element.find_elements_by_link_text("xxx")*|
|element.get_children("class=xxx") | *element.find_elements_by_class_name("xxx")*|
|element.get_children("id=xxx")    | *element.find_elements_by_id("xxx")*|
|element.get_children("name=xxx")  | *element.find_elements_by_name("xxx")* |
|element.get_children("plink=xxx") | *element.find_elements_by_partial_link_text("xxx")*|
|element.get_children("tag=xxx")   | *element.find_elements_by_tag_name("xxx")*|


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


Jupyter for BDD Testing in Python
=================================
Marigoso can help you create automated unit tests and functional tests (for end to end testing)
which can be shared between Manual Testers and Automation Engineers. When you import marigoso in your Jupyter Notebook
you will be able to create a single executable file which contains not only automation code, but manual steps as well.

Tests can be written using BDD (Gherkin) style and the manner of test execution can be step by step or all in one go.
When test fails during automated execution, the automation engineer can debug the code directly using Jupyter, while the
 manual tester always have the option to easily carry on manually, due to the fact that manual steps are also included in the same file.


Tutorials
=========
[Using Marigoso to Post a Comment in Blogger](https://github.com/ldiary/marigoso/blob/master/notes/using_marigoso_to_post_a_comment_in_blogger_post.ipynb)