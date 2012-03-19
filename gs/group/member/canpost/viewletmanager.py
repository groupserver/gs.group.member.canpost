# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, getMultiAdapter
from gs.viewlet.manager import WeightOrderedViewletManager
from interfaces import IGSPostingUser

class CanPostViewletManager(WeightOrderedViewletManager):
    @Lazy
    def loggedInUserInfo(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        assert retval, 'Could not create the user-info for the logged '\
            'in user from %s' % self.context
        return retval
        
    @Lazy
    def userInfo(self):
        retval = getattr(self, 'passedInUserInfo', self.loggedInUserInfo)
        assert retval
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


