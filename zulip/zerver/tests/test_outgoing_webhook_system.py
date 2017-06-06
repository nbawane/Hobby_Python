# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import mock
import requests
from typing import Any

from zerver.lib.outgoing_webhook import do_rest_call
from zerver.lib.test_classes import ZulipTestCase

rest_operation = {'method': "POST",
                  'relative_url_path': "",
                  'request_kwargs': {},
                  'base_url': ""}

class ResponseMock(object):
    def __init__(self, status_code, data, content):
        # type: (int, Any, str) -> None
        self.status_code = status_code
        self.data = data
        self.content = content

def request_exception_error(http_method, final_url, data, **request_kwargs):
    # type: (Any, Any, Any, Any) -> Any
    raise requests.exceptions.RequestException

def timeout_error(http_method, final_url, data, **request_kwargs):
    # type: (Any, Any, Any, Any) -> Any
    raise requests.exceptions.Timeout

class DoRestCallTests(ZulipTestCase):
    @mock.patch('zerver.lib.outgoing_webhook.succeed_with_message')
    def test_successful_request(self, mock_succeed_with_message):
        # type: (mock.Mock) -> None
        response = ResponseMock(200, {"message": "testing"}, '')
        with mock.patch('requests.request', return_value=response):
            do_rest_call(rest_operation, None, None) # type: ignore
            self.assertTrue(mock_succeed_with_message.called)

    @mock.patch('zerver.lib.outgoing_webhook.request_retry')
    def test_retry_request(self, mock_request_retry):
        # type: (mock.Mock) -> None
        response = ResponseMock(500, {"message": "testing"}, '')
        with mock.patch('requests.request', return_value=response):
            do_rest_call(rest_operation, None, None) # type: ignore
            self.assertTrue(mock_request_retry.called)

    @mock.patch('zerver.lib.outgoing_webhook.fail_with_message')
    def test_fail_request(self, mock_fail_with_message):
        # type: (mock.Mock) -> None
        response = ResponseMock(400, {"message": "testing"}, '')
        with mock.patch('requests.request', return_value=response):
            do_rest_call(rest_operation, None, None) # type: ignore
            self.assertTrue(mock_fail_with_message.called)

    @mock.patch('logging.info')
    @mock.patch('requests.request', side_effect=timeout_error)
    @mock.patch('zerver.lib.outgoing_webhook.request_retry')
    def test_timeout_request(self, mock_request_retry, mock_requests_request, mock_logger):
        # type: (mock.Mock, mock.Mock, mock.Mock) -> None
        do_rest_call(rest_operation, {"command": "", "service_name": ""}, None)
        self.assertTrue(mock_request_retry.called)

    @mock.patch('logging.exception')
    @mock.patch('requests.request', side_effect=request_exception_error)
    @mock.patch('zerver.lib.outgoing_webhook.fail_with_message')
    def test_request_exception(self, mock_fail_with_message, mock_requests_request, mock_logger):
        # type: (mock.Mock, mock.Mock, mock.Mock) -> None
        do_rest_call(rest_operation, {"command": ""}, None)
        self.assertTrue(mock_fail_with_message.called)
