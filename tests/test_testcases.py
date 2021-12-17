from pytest import mark, fixture

ddt = {
    'argnames': 'name,description',
    'argvalues': [('hello', 'world'),
                  ('hello', ''),
                  ('123', 'world'), ],
    'ids': ['general test', 'test with no description', 'test with digits in name']
}


@fixture(scope='function')
def clean_up(get_db):
    """
    cleanup should be done separately from test

    :param get_db:
    :return:
    """
    tests_to_delete = list()

    def cleaner(test_name):
        tests_to_delete.append(test_name)

    yield cleaner
    for test in tests_to_delete:
        get_db.delete_test_case(test)


@mark.parametrize(**ddt)
def test_new_testcase(desktop_app_auth, name, description, clean_up, get_db):
    tests = get_db.list_test_cases()
    desktop_app_auth.navigate_to('Create new test')
    desktop_app_auth.create_test(name, description)
    desktop_app_auth.navigate_to('Test Cases')
    test_exists = desktop_app_auth.test_cases.check_test_exists(name)
    clean_up(name)
    tests_new_count = get_db.list_test_cases()
    # desktop_app_auth.test_cases.delete_test_by_name(name)

    assert test_exists
    assert len(tests) + 1 == len(tests_new_count)


def test_testcase_does_not_exist(desktop_app_auth):
    desktop_app_auth.navigate_to('Test Cases')
    assert not desktop_app_auth.test_cases.check_test_exists('fndsfidsnisdfnisdfdsf')
    assert False


@fixture
def delete_precondition(get_web_service):
    test_name = 'test for delete'
    get_web_service.create_test(test_name, 'delete me pls')
    yield


def test_delete_test_case(desktop_app_auth, delete_precondition):
    test_name = 'test for delete'
    desktop_app_auth.navigate_to('Test Cases')
    test_exists = desktop_app_auth.test_cases.check_test_exists(test_name)
    desktop_app_auth.test_cases.delete_test_by_name(test_name)
    assert test_exists
    assert not desktop_app_auth.test_cases.check_test_exists(test_name)
