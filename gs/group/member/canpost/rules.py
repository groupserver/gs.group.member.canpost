# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo

class BaseRule(object):
    weight = None
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
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval
            
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
        retval = self.s['canPost']
        assert type(retval) == bool
        return retval
    
    @Lazy
    def status(self):
        self.check()
        retval = self.s['status']
        assert type(retval) == unicode
        return retval

    @Lazy
    def statusNum(self):
        self.check()
        retval = self.s['statusNum']
        assert retval in (-1, 0, self.weight), \
            'self.statusNum is "%s", not in range: -1, 0, %s' % \
            (retval, self.weight)
        assert (retval in (-1, self.weight) and (not self.canPost)) \
                or ((retval == 0) and self.canPost), 'Mismatch between '\
                'self.statusNum "%s" and self.canPost "%s"' %\
                (retval, self.canPost)
        return retval

class BlockedFromPosting(BaseRule):
    u'''A person will be prevented from posting if he or she is 
    explicitly blocked by an administrator of the group.'''
    weight = 10
            
    def check(self):
        if not self.s['checked']:
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
            self.s['checked'] = True

        assert self.s['checked']
        assert type(self.s['canPost']) == bool
        assert type(self.s['status']) == unicode
        assert type(self.s['statusNum']) == int

