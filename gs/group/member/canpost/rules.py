# coding=utf-8
from zope.cachedescriptors.property import Lazy
from Products.GSGroup.interfaces import IGSGroupInfo

class BaseRule(object):
    def __init__(self, userInfo, group):
        self.userInfo = userInfo
        self.group = group
        self.s =  { 'checked':    False,
                    'canPost':    False,
                    'status':     u'not implemented', 
                    'statusNum':  -1,}

    @Lazy
    def groupInfo(self):
        return IGSGroupInfo(self.group)
            
    @Lazy
    def mailingList(self):
        mailingListManager = self.site_root.ListManager
        retval = mailingListManager.get_list(self.groupInfo.id)
        return retval

    def check(self):
        m = 'Sub-classes must implement the check method.'
        raise NotImplementedError(m)
        
    @Lazy
    def canPost(self):
        self.check()
        return self.s['canPost']
    
    @Lazy
    def status(self):
        self.check()
        return self.s['status']

    @Lazy
    def statusNum(self):
        self.check()
        return self.s['statusNum']

class BlockedFromPosting(BaseRule):
    u'''A person will be prevented from posting if he or she is 
    explicitly blocked by an administrator of the group.'''
    weight = 10
            
    def check(self):
        if not self.__checked:
            ml = self.mailingList
            blockedMemberIds = ml.getProperty('blocked_members', [])
            if (self.userInfo.id in blockedMemberIds):
                self.s['canPost'] = False
                self.s['status'] = u'blocked from posting'
                self.s['statusNum'] = self.weight
            else:
                self.s['canPost'] = True
                self.s['status'] = u'not blocked from posting'
                self.s['statusNum'] = 0
        assert type(self.s['canPost']) == bool
        assert type(self.s['status']) == unicode
        assert type(self.s['statusNum']) == int

