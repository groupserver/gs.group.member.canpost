# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from mock import MagicMock, patch, PropertyMock
from unittest import TestCase
from gs.group.member.canpost.rules import BlockedFromPosting


class TestBlockedFromPosting(TestCase):
    def setUp(self):
        self.group = MagicMock()
        self.userInfo = MagicMock()
        # --=mpj17=-- Yes, really
        # <http://www.voidspace.org.uk/python/mock/mock.html#mock.PropertyMock>
        type(self.userInfo).id = PropertyMock(return_value='example')

    @patch.object(BlockedFromPosting, 'mailingList', new_callable=PropertyMock)
    def test_no_block(self, mock_ml):
        'Ensure that no one is blocked if no one is blocked'
        bfp = BlockedFromPosting(self.userInfo, self.group)
        bfp.mailingList.getProperty.return_value = []
        bfp.check()

        self.assertTrue(bfp.s['checked'])
        self.assertTrue(bfp.s['canPost'])
        self.assertEqual(0, bfp.s['statusNum'])

    @patch.object(BlockedFromPosting, 'mailingList', new_callable=PropertyMock)
    def test_block(self, mock_ml):
        'Ensure that someone one is blocked'
        bfp = BlockedFromPosting(self.userInfo, self.group)
        bfp.mailingList.getProperty.return_value = ['example', ]
        bfp.check()

        self.assertTrue(bfp.s['checked'])
        self.assertFalse(bfp.s['canPost'])
        self.assertEqual(bfp.weight, bfp.s['statusNum'])

    @patch.object(BlockedFromPosting, 'mailingList', new_callable=PropertyMock)
    def test_block_non_blocked(self, mock_ml):
        'Ensure that someone one is blocked'
        bfp = BlockedFromPosting(self.userInfo, self.group)
        bfp.mailingList.getProperty.return_value = ['not-example', ]
        bfp.check()

        self.assertTrue(bfp.s['checked'])
        self.assertTrue(bfp.s['canPost'])
        self.assertEqual(0, bfp.s['statusNum'])
