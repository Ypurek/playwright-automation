# Playwright automation with python

Test project to show

- features of MS Playwright on Python
- automation project structure using pytest

All tests designed to cover application [Test-Me](https://github.com/Ypurek/TestMe-TCM)

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

1. Create file `secure.json` for logins and passwords. Structure below. For demo purpose my file included to project as credentials already exposed in Test-Me documentaion

```json
{
  "users": {
    "userRole1": {
      "login": "login",
      "password": "password"
    },
    "userRole2": {
      "login": "login",
      "password": "password"
    }
  }
}
```
2. Install software to test [Test-Me](https://github.com/Ypurek/TestMe-TCM)
3. Set correct path to DB in `pytest.ini` file
4. Run Test-Me (check guide in it's repo)
5. Run tests using command `pytest`


