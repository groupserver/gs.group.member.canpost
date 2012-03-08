# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, getMultiAdapter
from gs.group.base.page import GroupPage
from interfaces import IGSPostingUser

class PostingRules(GroupPage):
    
    @Lazy
    def canPost(self):
        retval = getMultiAdapter((self.context, self.loggedInUserInfo), 
                    IGSPostingUser)
        return retval

