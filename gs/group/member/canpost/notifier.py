# coding=utf-8
from urllib import quote
from textwrap import TextWrapper
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from Products.XWFCore.XWFUtils import get_support_email
from gs.group.base.page import GroupPage
from gs.profile.notify.sender import MessageSender
from interfaces import IGSPostingUser
UTF8 = 'utf-8'

class NotifyNewAdmin(object):
    textTemplateName = 'cannot-post.txt'
    htmlTemplateName = 'cannot-post.html'
    
    def __init__(self, context, request):
        self.group = self.context = context
        self.request = request

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        assert retval, 'Could not create the SiteInfo from %s' % self.context
        return retval

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request), 
                    name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request), 
                    name=self.htmlTemplateName)
        assert retval
        return retval
        
    def notify(self, userInfo, siteInfo, groupInfo):
        subject = (u'%s: Problem Posting' % groupInfo.name).encode(UTF8)
        text = self.textTemplate(userInfo=userInfo, siteInfo=siteInfo, 
                    groupInfo=groupInfo)
        html = self.htmlTemplate(userInfo=userInfo, siteInfo=siteInfo, 
                    groupInfo=groupInfo)
        ms = MessageSender(self.context, userInfo)
        ms.send_message(subject, text, html)

class CannotPostMessage(GroupPage):
    @Lazy
    def supportAddress(self):
        gn = self.groupInfo.name.encode('ascii', 'ignore')
        s = 'Subject=%s' % quote('Cannot Post to %s' % gn)
        b = 'body=%s' % quote(self.messageBody)
        e = get_support_email(self.context, self.siteInfo.id)
        retval = 'mailto:%s?%s&%s' % (e, b, s)
        return retval
    
    @Lazy
    def messageBody(self):
        gn = self.groupInfo.name.encode('ascii', 'ignore')
        sn = self.siteInfo.name.encode('ascii', 'ignore')
        m = 'I had a problem sending an email to %s on %s <%s>. '\
            'The issue was "%s."' % \
            (gn, sn, self.groupInfo.url, self.canPost.status)
        retval = 'Hi!\n\n%s\n\nI need your help because...' % TextWrapper().fill(m)
        return retval
    
    @Lazy
    def canPost(self):
        group = self.groupInfo.groupObj
        retval = getMultiAdapter((group, self.loggedInUserInfo), 
                    IGSPostingUser)
        return retval

class CannotPostMessageText(CannotPostMessage):
    def __init__(self, context, request):
        CannotPostMessage.__init__(self, context, request)
        response = request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = 'cannot-post-%s-to-%s.txt' % \
            (self.loggedInUser.id, self.groupInfo.id)
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)

