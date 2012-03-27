# coding=utf-8
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.profile.notify.sender import MessageSender
from gs.profile.notify.notifyuser import NotifyUser
UTF8 = 'utf-8'

class Notifier(object):
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
        
    def notify(self, userInfo, origMesg):
        subject = (u'%s: Problem Posting' % groupInfo.name).encode(UTF8)
        text = self.textTemplate(userInfo=userInfo, siteInfo=siteInfo, 
                    groupInfo=groupInfo)
        html = self.htmlTemplate(userInfo=userInfo, siteInfo=siteInfo, 
                    groupInfo=groupInfo)
        
        #ms = MessageSender(self.context, userInfo)
        #ms.send_message(subject, text, html)

