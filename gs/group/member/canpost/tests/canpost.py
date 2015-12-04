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
from gs.group.member.canpost.canpost import CanPostToGroup


class SimpleRule(object):

    def __init__(self, canPost=True, statusNum=0, status='', weight=0):
        self.canPost = canPost
        self.statusNum = statusNum
        self.status = status
        self.weight = weight


class TestCanPostToGroup(TestCase):

    def setUp(self):
        self.group = MagicMock()
        self.userInfo = MagicMock()

    @patch.object(CanPostToGroup, 'rules', new_callable=PropertyMock)
    def test_can_post_no_rules(self, mock_rules):
        'Test we can post if there are no rules'
        mock_rules.return_value = []
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.canPost
        self.assertTrue(r)

    @patch.object(CanPostToGroup, 'rules', new_callable=PropertyMock)
    def test_can_post_all_true(self, mock_rules):
        'Test we can post if the rules are all True'
        mock_rules.return_value = [SimpleRule(True), SimpleRule(True)]
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.canPost
        self.assertTrue(r)

    @patch.object(CanPostToGroup, 'rules', new_callable=PropertyMock)
    def test_can_post_one_false(self, mock_rules):
        'Test we are blocked from posting if a rule is False'
        mock_rules.return_value = [SimpleRule(False)]
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.canPost
        self.assertFalse(r)

    @patch.object(CanPostToGroup, 'rules', new_callable=PropertyMock)
    def test_can_post_one_of_many_false(self, mock_rules):
        'Test we are blocked from posting if a rule of many is False'
        mock_rules.return_value = [SimpleRule(True), SimpleRule(False), SimpleRule(True)]
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.canPost
        self.assertFalse(r)

    @patch.object(CanPostToGroup, 'rules', new_callable=PropertyMock)
    def test_status_num_0(self, mock_rules):
        'Test we get status of 0 (ok) if there are no rules'
        mock_rules.return_value = []
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.statusNum
        self.assertEqual(0, r)

    @patch.object(CanPostToGroup, 'rules', new_callable=PropertyMock)
    def test_status_num_min(self, mock_rules):
        'Test we get the minumum status if there are rules'
        mock_rules.return_value = [SimpleRule(True), SimpleRule(False, 9), SimpleRule(False, 7)]
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.statusNum
        self.assertEqual(7, r)

    @patch.object(CanPostToGroup, 'rules', new_callable=PropertyMock)
    def test_status(self, mock_rules):
        'Test we get the right status-message if there are rules'
        mock_rules.return_value = [SimpleRule(True, 0, 'Ethel'), SimpleRule(False, 9, 'the'),
                                   SimpleRule(False, 7, 'frog')]
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.status
        self.assertEqual('frog', r)

    @patch.object(CanPostToGroup, 'adaptors', new_callable=PropertyMock)
    def test_rules(self, mock_adaptors):
        r0 = SimpleRule(True)
        r1 = SimpleRule(True)
        mock_adaptors.return_value = [('Ethel', r0), ('the', r1)]
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.rules
        self.assertEqual([r0, r1], r)

    @patch('gs.group.member.canpost.canpost.getGlobalSiteManager')
    def test_adaptors_sorted(self, mock_get_gsm):
        mock_gsm = mock_get_gsm()
        mock_gsm.getAdapters.return_value = [
            ('Ethel', SimpleRule(weight=10)), ('the', SimpleRule(weight=8))]
        canPost = CanPostToGroup(self.group, self.userInfo)
        r = canPost.adaptors
        self.assertEqual([8, 10], [a.weight for a in [b[1] for b in r]])
