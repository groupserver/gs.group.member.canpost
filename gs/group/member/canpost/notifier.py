# coding=utf-8
from email import message_from_string
from email.Message import Message
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEMessage import MIMEMessage
from email.utils import parseaddr
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
        
    def notify(self, userInfo, siteInfo, groupInfo, origMesg):
        subject = (u'%s: Problem Posting' % groupInfo.name).encode(UTF8)
        text = self.textTemplate(userInfo=userInfo, siteInfo=siteInfo, 
                    groupInfo=groupInfo)
        html = self.htmlTemplate(userInfo=userInfo, siteInfo=siteInfo, 
                    groupInfo=groupInfo)
        ms = CannotPostMessageSender(self.context, userInfo)
        ms.send_message(subject, text, html, origMesg)

class CannotPostMessageSender(MessageSender):
    def send_message(self, subject, txtMessage, htmlMessage, origMesg):
        toAddresses = self.emailUser.get_delivery_addresses()
        if toAddresses:
            msg = self.create_message(subject, txtMessage, htmlMessage, 
                                      origMesg)
            notifyUser = NotifyUser(self.toUserInfo.user)
            fromAddr = self.from_address(None)
            for addr in toAddresses:
                notifyUser.send_message(msg, addr, fromAddr)
        else:
            log.warn("Cannot notify user %s, no delivery addresses" %
                     self.toUserInfo.id)
    
    def create_message(self, subject, txtMessage, htmlMessage, origMesg):
        container = MIMEMultipart('mixed')
        container['Subject'] = str(Header(subject, UTF8))
        # --=mpj17=-- Similar to the call in MessageSender, but we
        #   always want the default.
        container['From'] = self.from_header_from_address(None)
        container['To'] = self.to_header_from_addresses(None)

        messageTextContainer = MIMEMultipart('alternative')
        container.attach(messageTextContainer)
        
        txt = MIMEText(txtMessage.encode(UTF8), 'plain', UTF8)
        messageTextContainer.attach(txt)
        
        html = MIMEText(htmlMessage.encode(UTF8), 'html', UTF8)
        messageTextContainer.attach(html)
        
        msg = message_from_string(origMesg)
        m = MIMEMessage(msg)
        m['Content-Description'] = 'Returned Message: %s' % \
            msg['Subject']
        m['Content-Disposition'] = 'inline'
        m.set_param('name', 'Returned message')
        del m['MIME-Version']
        container.attach(m)
        
        retval = container.as_string()
        assert retval
        return retval

