# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.contentprovider.interfaces import  UpdateNotCalled
from Products.GSGroup.joining import GSGroupJoining # --=mpj17=-- ?
from Products.GSGroupMember.groupmembership import JoinableGroupsForSite, InvitationGroupsForSite
from gs.group.base.contentprovider import GroupContentProvider

class GSUserCanPostContentProvider(GroupContentProvider):

    def __init__(self, context, request, view):
        GroupContentProvider.__init__(self, context, request, view)
        
    def update(self):
        self.__updated = True
        self.groupsInfo = createObject('groupserver.GroupsInfo',
          self.context)

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled

        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(view=self)
        
    #########################################
    # Non standard methods below this point #
    #########################################
    
    @Lazy
    def ptnCoach(self):
        ptnCoachId = self.groupInfo.get_property('ptn_coach_id')
        retval = createObject('groupserver.UserFromId',
          self.context, ptnCoachId)
        return retval 

    @Lazy
    def canJoin(self):
        joinableGroups = JoinableGroupsForSite(self.loggedInUserInfo.user)
        retval = self.groupInfo.id in joinableGroups
        assert type(retval) == bool
        return retval
    
    @Lazy
    def canInvite(self):
        invitationGroups = InvitationGroupsForSite(self.loggedInUserInfo.user,
                                               self.groupInfo.groupObj)
        retval = (self.groupInfo.id in invitationGroups) and \
          not self.canJoin
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
    def joinability(self):
        return GSGroupJoining(self.groupInfo.groupObj).joinability

