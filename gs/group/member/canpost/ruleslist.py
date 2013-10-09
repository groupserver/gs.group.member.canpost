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
from __future__ import absolute_path
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter
from gs.group.base.page import GroupPage
from .interfaces import IGSPostingUser


class PostingRules(GroupPage):

    @Lazy
    def canPost(self):
        retval = getMultiAdapter((self.context, self.loggedInUserInfo),
                    IGSPostingUser)
        return retval
