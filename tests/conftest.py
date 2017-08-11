import pytest


def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="http://localhost:9000/clowder",
                     help="Host, including protocol and port. ")
    parser.addoption("--username", action="store",
                     help="Clowder username")
    parser.addoption("--password", action="store",
                     help="Clowder user password")
    parser.addoption("--key", action="store", default="r1ek3rs",
                     help="Clowder API Key, use this or username/password combo")


@pytest.fixture(scope="module")
def host(request):
    return request.config.getoption("--host")


@pytest.fixture(scope="module")
def username(request):
    return request.config.getoption("--username")


@pytest.fixture(scope="module")
def password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope="module")
def key(request):
    return request.config.getoption("--key")
