import pytest


@pytest.fixture
def simple_yield_fixture():
    print('setUp part')
    yield 3
    print('tearDown part')
