Marigoso
========
Marigoso repository is a collection of tools you can use in your automated web application, API tests and
security testing. 

Discover [simplified Selenium functions](https://github.com/ldiary/marigoso/blob/master/notebooks/simplified_selenium_functions.ipynb), or learn how software feature requirements, 
manual test steps and automation code can all be aggregated into one 
[single executable file](https://github.com/ldiary/marigoso/blob/master/notebooks/an_example_of_using_jupyter_for_documenting_and_automating_bdd_style_tests.ipynb) which can help easily identify outdated requirements or outdated test steps documentation.

Installation
============
```
pip install -U marigoso
```

Tutorials
=========
[Handling Select2 Controls in Selenium WebDriver](https://github.com/ldiary/marigoso/blob/master/notebooks/handling_select2_controls_in_selenium_webdriver.ipynb)  
[Using Marigoso to Post a Comment in Blogger](https://github.com/ldiary/marigoso/blob/master/notebooks/using_marigoso_to_post_a_comment_in_blogger_post.ipynb)  
[An example of using Jupyter for Documenting and Automating BDD Style Tests](https://github.com/ldiary/marigoso/blob/master/notebooks/an_example_of_using_jupyter_for_documenting_and_automating_bdd_style_tests.ipynb)  
[Using PyTest to Execute BDD Style Tests Written in Jupyter (IPython) Notebook ](https://github.com/ldiary/marigoso/blob/master/notebooks/using_pytest_to_execute_bdd_style_tests_written_in_jupyter_ipython_notebooks.ipynb)  


2016-03-02 16:54:28,680 INFO: - App: Building service dependencies...
2016-03-02 16:54:28,690 INFO: - App: Copying files and filling templates...
2016-03-02 16:54:28,699 INFO: - App: Building app image without Dockerfile...
2016-03-02 16:54:28,850 INFO: - App: Sending build context to Docker daemon 557.1 kB
Sending build context to Docker daemon 1.114 MB
Sending build context to Docker daemon 1.671 MB
Sending build context to Docker daemon 2.228 MB
Sending build context to Docker daemon 2.785 MB
Sending build context to Docker daemon 3.342 MB
Sending build context to Docker daemon 3.899 MB
Sending build context to Docker daemon 4.456 MB
Sending build context to Docker daemon 5.014 MB
Sending build context to Docker daemon 5.571 MB
Sending build context to Docker daemon 6.128 MB
Sending build context to Docker daemon 6.685 MB
Sending build context to Docker daemon 7.242 MB
Sending build context to Docker daemon 7.799 MB
Sending build context to Docker daemon 8.062 MB
Sending build context to Docker daemon 8.062 MB
2016-03-02 16:54:28,868 INFO: - App: Step 0 : FROM gcr.io/generic-notebooks/binder-base
2016-03-02 16:54:28,891 INFO: - App:  ---> fcd034278706
2016-03-02 16:54:28,909 INFO: - App: Step 1 : ADD repo $HOME/notebooks
2016-03-02 16:54:29,175 INFO: - App:  ---> 18e4436efddb
2016-03-02 16:54:29,188 INFO: - App: Removing intermediate container bf3e4a757e59
2016-03-02 16:54:29,197 INFO: - App: Step 2 : USER root
2016-03-02 16:54:29,280 INFO: - App:  ---> Running in b3ca6d0007eb
2016-03-02 16:54:29,439 INFO: - App:  ---> e37ac188a138
2016-03-02 16:54:29,444 INFO: - App: Removing intermediate container b3ca6d0007eb
2016-03-02 16:54:29,448 INFO: - App: Step 3 : RUN chown -R main:main $HOME/notebooks
2016-03-02 16:54:29,547 INFO: - App:  ---> Running in 5a7cd75a8835
2016-03-02 16:54:30,133 INFO: - App:  ---> 2de81ff4673a
2016-03-02 16:54:30,139 INFO: - App: Removing intermediate container 5a7cd75a8835
2016-03-02 16:54:30,143 INFO: - App: Step 4 : USER main
2016-03-02 16:54:30,232 INFO: - App:  ---> Running in f02a3b8158f2
2016-03-02 16:54:30,376 INFO: - App:  ---> 8d3db418a497
2016-03-02 16:54:30,388 INFO: - App: Removing intermediate container f02a3b8158f2
2016-03-02 16:54:30,395 INFO: - App: Step 5 : RUN find $HOME/notebooks -name '*.ipynb' -exec ipython trust {} \;
2016-03-02 16:54:30,483 INFO: - App:  ---> Running in fc7dba0d517a
2016-03-02 16:54:31,132 INFO: - App: [TrustNotebookApp] Writing notebook-signing key to /home/main/.local/share/jupyter/notebook_secret
2016-03-02 16:54:31,145 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/setting_up_a_local_copy_of_python_selenium_binding.ipynb
2016-03-02 16:54:31,590 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/howto_dynamically_add_functions_to_browser.ipynb
2016-03-02 16:54:32,023 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/simplified_selenium_functions.ipynb
2016-03-02 16:54:32,429 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/library.ipynb
2016-03-02 16:54:32,855 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/howto_obtain_more_detailed_traceback_from_failing_testbooks.ipynb
2016-03-02 16:54:33,355 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/using_marigoso_to_post_a_comment_in_blogger_post.ipynb
2016-03-02 16:54:33,827 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/an_example_of_using_jupyter_for_documenting_and_automating_bdd_style_tests.ipynb
2016-03-02 16:54:34,274 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/testing_the_notebook_import_module.ipynb
2016-03-02 16:54:34,677 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/using_pytest_to_execute_bdd_style_tests_written_in_jupyter_ipython_notebooks.ipynb
2016-03-02 16:54:35,137 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/how_to_enable_firefox_marionette_in_selenium_automated_testing.ipynb
2016-03-02 16:54:35,596 INFO: - App: Signing notebook: /home/main/notebooks/notebooks/handling_select2_controls_in_selenium_webdriver.ipynb
2016-03-02 16:54:35,946 INFO: - App:  ---> 38cea135fcdd
2016-03-02 16:54:35,955 INFO: - App: Removing intermediate container fc7dba0d517a
2016-03-02 16:54:35,966 INFO: - App: Step 6 : WORKDIR $HOME/notebooks
2016-03-02 16:54:36,051 INFO: - App:  ---> Running in 9eff80e051c1
2016-03-02 16:54:36,179 INFO: - App:  ---> b1655a6a6d0e
2016-03-02 16:54:36,191 INFO: - App: Removing intermediate container 9eff80e051c1
2016-03-02 16:54:36,195 INFO: - App: Successfully built b1655a6a6d0e
2016-03-02 16:54:36,201 INFO: - App: Squashing and pushing gcr.io/generic-notebooks/ldiary-marigoso to private registry...
2016-03-02 16:54:49,560 INFO: - App: Preloading app image onto all nodes...
2016-03-02 16:55:44,427 INFO: - App: Successfully built app ldiary-marigoso