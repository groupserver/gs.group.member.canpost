# coding=utf-8
import re
from urllib import quote
from textwrap import TextWrapper
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from Products.XWFMailingListManager.html2txt import convert_to_txt
from Products.XWFCore.XWFUtils import get_support_email
from gs.group.base.page import GroupPage
from gs.group.privacy.interfaces import IGSGroupVisibility
from interfaces import IGSPostingUser
        
class CannotPostMessage(GroupPage):
    def supportAddress(self, userInfo):
        gn = self.groupInfo.name.encode('ascii', 'ignore')
        s = 'Subject=%s' % quote('Cannot Post to %s' % gn)
        b = 'body=%s' % quote(self.message_body(userInfo))
        e = get_support_email(self.context, self.siteInfo.id)
        retval = 'mailto:%s?%s&%s' % (e, b, s)
        return retval
    
    def message_body(self, userInfo):
        gn = self.groupInfo.name.encode('ascii', 'ignore')
        sn = self.siteInfo.name.encode('ascii', 'ignore')
        cp  = self.can_post_for_user(userInfo)
        m = 'I had a problem sending an email to %s on %s <%s>. '\
            'The issue was "%s (Reason Number %s)"' % \
            (gn, sn, self.groupInfo.url, cp.status, cp.statusNum)
        retval = 'Hi!\n\n%s\n\nI need your help because...' % \
            TextWrapper().fill(m)
        return retval
    
    def can_post_for_user(self, userInfo):
        group = self.groupInfo.groupObj
        retval = getMultiAdapter((group, userInfo),
                    IGSPostingUser)
        return retval

class CannotPostMessageText(CannotPostMessage):
    spaceRE = re.compile(r'\s+')
    def __init__(self, context, request):
        CannotPostMessage.__init__(self, context, request)
        response = request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = 'cannot-post-%s-to-%s.txt' % \
            (self.loggedInUserInfo.id, self.groupInfo.id)
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)
        self.textWrapper = TextWrapper()

    def format_message(self, m):
        retval = self.textWrapper.fill(m)
        return retval

    def cp_to_txt(self, cp):
        t = convert_to_txt(cp)
        retval = self.spaceRE.sub(' ', t).strip()
        return retval

# Unknown Email Address      
class UnknownEmailMessage(GroupPage):
    def quote(self, msg):
        assert msg
        retval = quote(msg)
        assert retval
        return retval

    @Lazy
    def groupVisibility(self):
        retval = IGSGroupVisibility(self.groupInfo)
        assert retval
        return retval

class UnknownEmailMessageText(UnknownEmailMessage):
    def __init__(self, context, request):
        UnknownEmailMessage.__init__(self, context, request)
        response = request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = 'unknown-email-%s.txt' % self.groupInfo.id
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)
        self.textWrapper = TextWrapper()
        
    def format_message(self, m):
        retval = self.textWrapper.fill(m)
        return retval

