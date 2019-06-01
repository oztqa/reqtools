# -*- coding: utf-8 -*-
import pickle

import pytest
from requests import Session as RequestsSession
from hamcrest import assert_that, equal_to, instance_of, is_

from reqtools import RemoteApiSession


def test_remote_api_create_instance():
    session = RemoteApiSession('http://test.ru')
    assert_that(session, instance_of(RequestsSession))


def test_remote_api_base_url():
    url = 'http://test.ru'
    session = RemoteApiSession(url)
    assert_that(session.base_url, is_(equal_to(url)))


def test_remote_api_prefix():
    url = 'http://test.ru'
    prefix = 'prefix'
    session = RemoteApiSession(url, prefix=prefix)
    assert_that(session.prefix, is_(equal_to(prefix)))


def test_remote_api_url():
    url = 'http://test.ru'
    session = RemoteApiSession(url)
    assert_that(session.url, is_(equal_to(url)))


@pytest.mark.parametrize(
    'url, prefix, expected',
    [
        ('http://test.ru', 'prefix', 'http://test.ru/prefix'),
        ('http://test.ru', '/prefix', 'http://test.ru/prefix'),
        ('http://test.ru', 'prefix/', 'http://test.ru/prefix/'),
    ],
)
def test_remote_api_url_with_prefix(url, prefix, expected):
    session = RemoteApiSession(url, prefix=prefix)
    assert_that(session.url, is_(equal_to(expected)))


def test_remote_api_build_url():
    session = RemoteApiSession('http://test.ru')
    assert_that(session._build_url(session.url, '/test'), is_(equal_to('http://test.ru/test')))


@pytest.mark.parametrize(
    'prefix, url_path, expected',
    [
        ('prefix', 'test', 'http://test.ru/prefix/test'),
        ('prefix', '/test', 'http://test.ru/prefix/test'),
        ('/prefix', 'test/', 'http://test.ru/prefix/test/'),
        ('/prefix', '/test', 'http://test.ru/prefix/test'),
        ('prefix/', 'test', 'http://test.ru/prefix/test'),
        ('prefix/', 'test/', 'http://test.ru/prefix/test/'),
    ],
)
def test_remote_api_build_url_with_prefix(prefix, url_path, expected):
    session = RemoteApiSession('http://test.ru', prefix=prefix)
    assert_that(session._build_url(session.url, url_path), is_(equal_to(expected)))


@pytest.mark.parametrize(
    'base, prefix, url_path, expected',
    [
        ('http://localhost:5000/api', 'prefix', 'test/', 'http://localhost:5000/api/prefix/test/'),
        ('http://localhost:5000/api', 'prefix/', 'test', 'http://localhost:5000/api/prefix/test'),
        ('http://localhost:5000/api', '/prefix', 'test/', 'http://localhost:5000/api/prefix/test/'),
        ('http://localhost:5000/api', '/prefix/', 'test', 'http://localhost:5000/api/prefix/test'),
        ('http://localhost:5000/api/', 'prefix', 'test/', 'http://localhost:5000/api/prefix/test/'),
        ('http://localhost:5000/api/', 'prefix/', 'test', 'http://localhost:5000/api/prefix/test'),
        ('http://localhost:5000/api/', '/prefix', 'test/', 'http://localhost:5000/api/prefix/test/'),
        ('http://localhost:5000/api/', '/prefix/', 'test', 'http://localhost:5000/api/prefix/test'),
    ],
)
def test_remote_api_build_url_with_prefix_and_nonorigin_base(base, prefix, url_path, expected):
    session = RemoteApiSession(base, prefix=prefix)
    assert_that(session._build_url(session.url, url_path), is_(equal_to(expected)))


def test_serializable():
    base_url = 'http://test.ru'
    prefix = '/prefix'
    session_original = RemoteApiSession(base_url, prefix=prefix)
    serialization = pickle.dumps(session_original)
    del session_original
    session_loaded = pickle.loads(serialization)
    assert_that(session_loaded.base_url, is_(base_url))
    assert_that(session_loaded.prefix, is_(prefix))
