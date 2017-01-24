import pytest


def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="http://localhost:8080/clowder",
                     help="Host, including protocol and port. ")
    parser.addoption("--username", action="store", default="alice",
                     help="Username: Either from crowd or application.conf depending how fence was setup")
    parser.addoption("--password", action="store", default="fred",
                     help="Password: Either from crowd or application.conf depending how fence was setup")
    parser.addoption("--key", action="store", default="r1ek3rs",
                     help="API Key")

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
