import os
import json
import pytest
import logging
import allure
from settings import *
from pytest import fixture, hookimpl
from playwright.sync_api import sync_playwright
from page_objects.application import App
from helpers.web_service import WebService
from helpers.db import DataBase


@fixture(autouse=True, scope='session')
def preconditions(request):
    """
    Global fixtures. Run automatically before all tests and executes part before yield statement as test precondition.
    Executes code after yield statement after last test executed as test post conditions

    Reports test results to TCP via API helper in post conditions

    :param request: pytest fixture
    https://docs.pytest.org/en/6.2.x/reference.html#std-fixture-request
    """
    logging.info('preconditions started')
    base_url = request.config.getini('base_url')
    tcm = request.config.getini('tcm_report')
    secure = request.config.getoption('--secure')
    config = load_config(request.session.fspath.strpath, secure)
    yield
    logging.info('postconditions started')

    if tcm == 'True':
        web = WebService(base_url)
        web.login(**config['users']['userRole3'])
        for test in request.node.items:
            if len(test.own_markers) > 0:
                if test.own_markers[0].name == 'test_id':
                    if test.result_call.passed:
                        web.report_test(test.own_markers[0].args[0], 'PASS')
                    if test.result_call.failed:
                        web.report_test(test.own_markers[0].args[0], 'FAIL')


@fixture(scope='session')
def get_web_service(request):
    """
    Fixture returns authenticated WebService object to work with tested app directly via web services

    :param request: pytest fixture
    https://docs.pytest.org/en/6.2.x/reference.html#std-fixture-request

    :return: WebService object
    """
    base_url = request.config.getini('base_url')
    secure = request.config.getoption('--secure')
    config = load_config(request.session.fspath.strpath, secure)
    web = WebService(base_url)
    web.login(**config['users']['userRole1'])
    yield web
    web.close()


@fixture(scope='session')
def get_db(request):
    """
    Fixture returns DataBase object to work with tested app directly via db

    :param request: pytest fixture
    https://docs.pytest.org/en/6.2.x/reference.html#std-fixture-request

    :return: WebService object
    """
    path = request.config.getini('db_path')
    db = DataBase(path)
    yield db
    db.close()


@fixture(scope='session')
def get_playwright():
    """
    returns single instance of playwright itself
    :return:
    """
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session', params=['chromium'])
def get_browser(get_playwright, request):
    browser = request.param
    # save browser type to env variable so fixtures and tests can get current browser
    # Needed to skip unused browser-test combinations
    os.environ['PWBROWSER'] = browser
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'unsupported browser type'

    yield bro
    bro.close()
    del os.environ['PWBROWSER']


@fixture(scope='session')
def desktop_app(get_browser, request):
    """
    Fixture of playwright for non autorised tests
    """
    base_url = request.config.getini('base_url')
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(request.session.fspath.strpath, secure)
    app = desktop_app
    app.goto('/login')
    app.login(**config['users']['userRole1'])
    yield app


@fixture(scope='session')
def desktop_app_bob(get_browser, request):
    base_url = request.config.getini('base_url')
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/login')
    app.login(**config['users']['userRole2'])
    yield app
    app.close()


@fixture(scope='session', params=['iPhone 11', 'Pixel 2'])
def mobile_app(get_playwright, get_browser, request):
    if os.environ.get('PWBROWSER') == 'firefox':
        pytest.skip()
    base_url = request.config.getini('base_url')
    device = request.param
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(BROWSER_OPTIONS)
    else:
        device_config = BROWSER_OPTIONS
    app = App(get_browser, base_url=base_url, **device_config)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    app = mobile_app
    app.goto('/login')
    app.login(**config['users']['userRole1'])
    yield app


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    # result.when == "setup" >> "call" >> "teardown"
    setattr(item, f'result_{result.when}', result)


@fixture(scope='function', autouse=True)
def make_screenshots(request):
    yield
    if request.node.result_call.failed:
        for arg in request.node.funcargs.values():
            if isinstance(arg, App):
                allure.attach(body=arg.page.screenshot(),
                              name='screenshot.png',
                              attachment_type=allure.attachment_type.PNG)


def pytest_addoption(parser):
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addini('base_url', help='base url of site under test', default='http://127.0.0.1:8000')
    parser.addini('db_path', help='path to sqlite db file', default='C:\\DEV\\TestMe-TCM\\db.sqlite3')
    parser.addini('headless', help='run browser in headless mode', default='True')
    parser.addini('tcm_report', help='report test results to tcm', default='False')


# request.session.fspath.strpath - path to project root
def load_config(project_path: str, file: str) -> dict:
    config_file = os.path.join(project_path, file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
