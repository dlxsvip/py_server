# -*- coding:UTF-8 -*-
import json
from utils import http_util

rsp = http_util.http('127.0.0.1', '8012', 'action/test_action', 'POST', 5)

code = rsp.status_code
body = rsp.text
print code, body
# print json.loads(body)
# print json.dumps(json.loads(body), indent=4)
