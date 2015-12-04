# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from abc import ABCMeta, abstractproperty
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupViewlet
from .rules import BlockedFromPosting


class RuleViewlet(GroupViewlet):
    __metaclass__ = ABCMeta

    @abstractproperty
    def weight(self):
        'The "weight" of the viewlet. Normally taken from the weight of the rule.'

    @Lazy
    def canPost(self):
        return self.manager.canPost

    @Lazy
    def show(self):
        '``True`` if the viewlet should be shown'
        retval = self.canPost.statusNum == self.weight
        return retval

    @Lazy
    def userInfo(self):
        return self.manager.userInfo


class BlockedRuleViewlet(RuleViewlet):
    weight = BlockedFromPosting.weight
