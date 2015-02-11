# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from email.parser import Parser
from mock import MagicMock
from unittest import TestCase
from gs.group.member.canpost.unknownemail import Notifier


class TestUnknownEmail(TestCase):
    m = '''From: Me <a.member@example.com>
To: Group <group@groups.example.com>
Subject: Violence

Tonight on Ethel the Frog we look at violence.\n'''

    def setUp(self):
        context = MagicMock()
        request = MagicMock()
        self.notifier = Notifier(context, request)

        parser = Parser()
        self.msg = parser.parsestr(self.m)

    def test_create_return_message(self):
        r = self.notifier.create_return_message(self.msg)
        self.assertIn('Returned message', r['content-description'])
        self.assertIn(self.msg['Subject'], r['content-description'])

    def test_create_return_message_subject_missing(self):
        del(self.msg['Subject'])
        r = self.notifier.create_return_message(self.msg)
        self.assertIn('Returned message', r['content-description'])
        self.assertIn('No subject', r['content-description'])

    def test_create_return_message_subject_latin1(self):
        s = 'Je ne ecrit pas français'
        self.msg.replace_header('Subject', s.encode('latin1'))
        r = self.notifier.create_return_message(self.msg)
        self.assertIn('Returned message', r['content-description'])
        self.assertIn(s.encode('ascii', 'ignore'), r['content-description'])

    def test_create_container(self):
        r = self.notifier.create_container(
            'Returned message', 'group@egroups.example.com',
            'person@example.com')
        self.assertIn('Returned message', r['Subject'])
        self.assertIn('person', r['To'])
        self.assertIn('group', r['From'])

    def test_create_container_unicode(self):
        r = self.notifier.create_container(
            'Je ne ecrit pas français', 'group@egroups.example.com',
            'person@example.com')
        self.assertNotIn('français', r['Subject'])
