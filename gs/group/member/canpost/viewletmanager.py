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
from __future__ import absolute_import
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, getMultiAdapter
from gs.viewlet.manager import WeightOrderedViewletManager
from .interfaces import IGSPostingUser


class CanPostViewletManager(WeightOrderedViewletManager):
    @Lazy
    def loggedInUserInfo(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        assert retval, 'Could not create the user-info for the logged '\
            'in user from %s' % self.context
        return retval

    @Lazy
    def userInfo(self):
        # Sometimes we are passed None as the passedInUserInfo
        piui = getattr(self, 'passedInUserInfo', None)
        retval = (piui and piui) or self.loggedInUserInfo
        assert retval, 'userInfo is %s:\n  passedInUserInfo is %s\n  '\
            'loggedInUser is %s' % (retval, piui, self.loggedInUserInfo)
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval

    @Lazy
    def canPost(self):
        group = self.groupInfo.groupObj
        retval = getMultiAdapter((group, self.userInfo),
                    IGSPostingUser)
        return retval
