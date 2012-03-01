# coding=utf-8
from zope.cachedescriptors.property import Lazy
from Products.GSGroup.interfaces import IGSGroupInfo

class BaseRule(object):
    def __init__(self, userInfo, group):
        self.userInfo = userInfo
        self.group = group

    @Lazy
    def groupInfo(self):
        return IGSGroupInfo(self.group)
            
    @Lazy
    def mailingList(self):
        mailingListManager = self.site_root.ListManager
        retval = mailingListManager.get_list(self.groupInfo.id)
        return retval
    
    canPost = False
    statusNum = -1
    status = u'Not Implemented'

class BlockedFromPosting(BaseRule):
    u'''A person will be prevented from posting if he or she is 
    explicitly blocked by an administrator of the group.'''
    weight = 10

    def __init__(self, user, group):
        BaseRule.__init__(self, user, group)
        self.__checked = False
            
    def check(self):
        if not self.__checked:
            ml = self.mailingList
            blockedMemberIds = ml.getProperty('blocked_members', [])
            if (self.userInfo.id in blockedMemberIds):
                self.__canPost = False
                self.__status = u'blocked from posting'
                self.__statusNum = self.weight
            else:
                self.__canPost = True
                self.__status = u'not blocked from posting'
                self.__statusNum = 0
        assert type(self.__canPost) == bool
        assert type(self.__status) == unicode
        assert type(self.__statusNum) == int

    @Lazy
    def canPost(self):
        self.check()
        return self.__canPost
    
    @Lazy
    def statusNum(self):
        self.check()
        return self.__statusNum

    @Lazy
    def status(self):
        self.check()
        return self.__status

