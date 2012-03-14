# coding=utf-8
from urllib import urlencode
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from Products.XWFCore.XWFUtils import get_support_email
from gs.group.base.page import GroupPage
from gs.profile.notify.sender import MessageSender
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
        print 'Here 1'
        gn = self.groupInfo.name.encode('ascii', 'ignore')
        print 'Here 2'
        sn = self.siteInfo.name.encode('ascii', 'ignore')
        print 'Here 3'
        d = {'Subject': 'Cannot Post to %s' % gn,
            'body': 'Hi!\n\nThere I had a problem sending a post to'\
                    '%s on %s.' % (gn, sn)}
        print 'Here 4'
        e = get_support_email(self.context, self.siteInfo.id)
        print 'Here 5'
        retval = 'mailto:%s?%s' % (e, urlencode(d))
        print 'Here 6'
        return retval
    # CanPost adaptor

class CannotPostMessageText(CannotPostMessage):
    def __init__(self, context, request):
        CannotPostMessage.__init__(self, context, request)
        response = request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = 'cannot-post-%s-to-%s.txt' % \
            (self.loggedInUser.id, self.groupInfo.id)
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)

