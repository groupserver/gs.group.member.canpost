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
        # Sometimes we are passed None as the passedInUserInfo
        piui = getattr(self, 'passedInUserInfo', None) 
        retval = (piui and piui) or self.loggedInUserInfo
        assert retval, 'userInfo is %s:\n  passedInUserInfo is %s\n  '\
            'loggedInUser is %s' %(retval, piui, self.loggedInUserInfo) 
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


