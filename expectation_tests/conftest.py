import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="store",
        help="Host on which the tests should be executed. Should conform to the format: http(s)://<hostname> "
             "(without trailing slash)",
        default="http://localhost:8080",
    )


@pytest.fixture
def host(request):
    host_from_parameter = request.config.getoption("--host")
    assert host_from_parameter is not None
    host_from_parameter.startswith('http')
    if host_from_parameter.endswith('/'):
        host_from_parameter = host_from_parameter[:-1]
    return host_from_parameter
