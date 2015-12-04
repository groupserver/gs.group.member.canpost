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
from abc import ABCMeta, abstractmethod, abstractproperty
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo


class BaseRule(object):
    __metaclass__ = ABCMeta

    def __init__(self, userInfo, group):
        self.userInfo = userInfo
        self.group = group
        self.s = {'checked': False,
                  'canPost': False,
                  'status': 'not implemented',
                  'statusNum': -1, }

    @abstractproperty
    def weight(self):
        'The weight for the rule: rules with lighter weights are evaulated first'

    @abstractmethod
    def check(self):
        '''Check that the user can post to the group. Sets ``self.s``.'''

    @Lazy
    def groupInfo(self):
        return IGSGroupInfo(self.group)

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval

    @Lazy
    def mailingList(self):
        site_root = self.group.site_root()
        mailingListManager = site_root.ListManager
        retval = mailingListManager.get_list(self.groupInfo.id)
        return retval

    @Lazy
    def canPost(self):
        self.check()
        retval = self.s['canPost']
        assert type(retval) == bool
        return retval

    @Lazy
    def status(self):
        self.check()
        retval = self.s['status']
        return retval

    @Lazy
    def statusNum(self):
        self.check()
        retval = self.s['statusNum']
        assert retval in (-1, 0, self.weight), \
            'self.statusNum is "%s", not in range: -1, 0, %s' % \
            (retval, self.weight)
        assert ((retval in (-1, self.weight) and (not self.canPost))
                or ((retval == 0) and self.canPost)), 'Mismatch between '\
            'self.statusNum "%s" and self.canPost "%s"' % (retval, self.canPost)
        return retval


class BlockedFromPosting(BaseRule):
    '''A person will be prevented from posting if he or she is
    explicitly blocked by an administrator of the group.'''
    weight = 10

    def check(self):
        if not self.s['checked']:
            ml = self.mailingList
            blockedMemberIds = ml.getProperty('blocked_members', [])
            if (self.userInfo.id in blockedMemberIds):
                self.s['canPost'] = False
                self.s['status'] = 'blocked from posting'
                self.s['statusNum'] = self.weight
            else:
                self.s['canPost'] = True
                self.s['status'] = 'not blocked from posting'
                self.s['statusNum'] = 0
            self.s['checked'] = True
