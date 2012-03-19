# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.base.viewlet import GroupViewlet
from rules import BlockedFromPosting

class RuleViewlet(GroupViewlet):
    @Lazy
    def canPost(self):
        return self.manager.canPost
        
    @Lazy
    def show(self):
        m = 'Sub-classes must implement the "show" method.'
        raise NotImplementedError(m)
    
    @Lazy
    def userInfo(self):
        return self.manager.userInfo

class BlockedRuleViewlet(RuleViewlet):
    weight = BlockedFromPosting.weight
    @Lazy
    def show(self):
        retval = self.canPost.statusNum == self.weight
        assert type(retval) == bool
        return retval

