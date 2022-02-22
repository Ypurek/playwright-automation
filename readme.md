# Playwright automation with python

Test project to show

- features of MS Playwright on Python
- automation project structure using pytest

All tests designed to cover application [Test-Me](https://github.com/Ypurek/TestMe-TCM)

Guide in Ukrainian about python playwright: [Our youtube channel](https://www.youtube.com/watch?v=024tZHVFiLA&list=PLGE9K4YL_ywj4F7cSA4oDptnqTmyS7hZp)


Tools:

- [Playwright](https://github.com/microsoft/playwright-python)
- [Pytest](https://pytest.org/)
- [PyCharm](https://www.jetbrains.com/ru-ru/pycharm/)

## Install guide

1. Install python
2. Install PyCharm
3. Install python dependencies
   `pip install -r requirements.txt`
4. Make sure playwright version 1.8+ installed

## Project structure

- [conftest.py](conftest.py) file contains main fixtures to work
- Page objects stored in page_object folder
- Tests stored in tests folder
- Settings are spread between:
    - pytest.ini
    - settings.py

## Run guide
1. Install software to test [Test-Me](https://github.com/Ypurek/TestMe-TCM)
2. Set correct path to DB in `pytest.ini` file
3. Run Test-Me (check guide in it's repo)
4. Run tests using command `pytest`


