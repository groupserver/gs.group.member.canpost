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
from operator import and_
from zope.cachedescriptors.property import Lazy
from zope.component import getGlobalSiteManager
from gs.group.member.canpost.interfaces import IGSCanPostRule


class CanPostToGroup(object):
    def __init__(self, group, userInfo):
        self.group = group
        self.userInfo = userInfo

    @Lazy
    def adaptors(self):
        gsm = getGlobalSiteManager()
        retval = [a for a in gsm.getAdapters((self.userInfo, self.group),
                                              IGSCanPostRule)]
        retval.sort(key=lambda r: r[1].weight)
        return retval

    @Lazy
    def rules(self):
        retval = [instance for name, instance in self.adaptors]
        return retval

    @Lazy
    def canPost(self):
        return reduce(and_, [rule.canPost for rule in self.rules], True)

    @Lazy
    def statusNum(self):
        statusNums = [rule.statusNum for rule in self.rules
                        if rule.statusNum != 0]
        retval = (statusNums and min(statusNums)) or 0
        assert retval >= 0
        return retval

    @Lazy
    def status(self):
        retval = [rule.status for rule in self.rules
                    if rule.statusNum == self.statusNum][0]
        return retval
