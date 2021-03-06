# -*- coding: utf-8 -*-

# Copyright (c) 2013-2014, Camptocamp SA
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.


from unittest import TestCase
from c2cgeoportal.tests import create_dummy_request


class TestGetURL(TestCase):

    def test_get_url(self):
        from c2cgeoportal.lib import get_url

        request = create_dummy_request({
            "package": "my_project",
            "servers": {
                "srv": "https://example.com/test",
            },
        })

        def static_url(path, **kwargs):
            return "http://server.org/" + path
        request.static_url = static_url

        self.assertEquals(get_url("static://pr:st/icon.png", request), "http://server.org/pr:st/icon.png")
        self.assertEquals(get_url("static:///icon.png", request), "http://server.org/c2cgeoportal:project/icon.png")
        self.assertEquals(get_url("config://srv/icon.png", request), "https://example.com/test/icon.png?")
        self.assertEquals(get_url("config://srv2/icon.png", request, "/icon2.png"), "/icon2.png")
        self.assertEquals(get_url("http://example.com/icon.png", request), "http://example.com/icon.png")
        self.assertEquals(get_url("https://example.com/icon.png", request), "https://example.com/icon.png")
        errors = []
        self.assertEquals(get_url("config://srv2/icon.png", request, errors=errors), None)
        self.assertEquals(errors, ["The server 'srv2' isn't found in the config"])
