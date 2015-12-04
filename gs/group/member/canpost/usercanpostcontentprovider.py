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
from __future__ import unicode_literals, absolute_import, print_function
import sys
if sys.version_info >= (3, ):
    from urllib.parse import urlencode
else:
    from urllib import urlencode
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.contentprovider.interfaces import UpdateNotCalled
from Products.GSGroup.joining import GSGroupJoining  # --=mpj17=-- ?
from Products.GSGroupMember.groupmembership import JoinableGroupsForSite, \
    InvitationGroupsForSite
from gs.group.base import GroupContentProvider


class GSUserCanPostContentProvider(GroupContentProvider):

    def __init__(self, context, request, view):
        GroupContentProvider.__init__(self, context, request, view)

    def update(self):
        self.__updated = True
        self.groupsInfo = createObject('groupserver.GroupsInfo', self.context)

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled

        pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(self, view=self)

    #########################################
    # Non standard methods below this point #
    #########################################

    @Lazy
    def ptnCoach(self):
        ptnCoachId = self.groupInfo.get_property('ptn_coach_id')
        retval = createObject('groupserver.UserFromId', self.context, ptnCoachId)
        return retval

    @Lazy
    def canJoin(self):
        joinableGroups = JoinableGroupsForSite(self.loggedInUser.user)
        retval = self.groupInfo.id in joinableGroups
        assert type(retval) == bool
        return retval

    @Lazy
    def canInvite(self):
        invitationGroups = InvitationGroupsForSite(self.loggedInUser.user, self.groupInfo.groupObj)
        retval = (self.groupInfo.id in invitationGroups) and not self.canJoin
        assert type(retval) == bool
        return retval

    @Lazy
    def loginUrl(self):
        assert self.request
        assert self.request.URL
        retval = '/login.html?came_from=%s' % self.request.URL
        assert retval
        return retval

    @Lazy
    def signupUrl(self):
        d = {'form.came_from': self.request.URL,
             'form.groupId': self.groupInfo.id, }
        retval = '/request_registration.html?%s' % urlencode(d)
        return retval

    @Lazy
    def joinability(self):
        return GSGroupJoining(self.groupInfo.groupObj).joinability
