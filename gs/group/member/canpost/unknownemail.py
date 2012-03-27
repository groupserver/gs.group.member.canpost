# coding=utf-8
from email import message_from_string
from email.Message import Message
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEMessage import MIMEMessage
from email.utils import parseaddr
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, getMultiAdapter

UTF8 = 'utf-8'

class Notifier(object):
    textTemplateName = 'unknown-email.txt'
    htmlTemplateName = 'unknown-email.html'
    
    def __init__(self, context, request):
        self.group = self.context = context
        self.request = request

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        assert retval, 'Could not create the SiteInfo from %s' % self.context
        return retval


    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Could not create the GroupInfo from %s' % self.context
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

    @Lazy
    def mailhost(self):
        sr = self.context.site_root()
        try:
            retval = sr.superValues('Mail Host')[0]
        except:
            raise AttributeError, "Can't find a Mail Host instance"
        return retval

    def notify(self, toAddress, origMesg):
        s = u'%s: Problem Posting (Action Required)' % self.groupInfo.name
        email = parseaddr(toAddress)[1]
        text = self.textTemplate(email=email)
        html = self.htmlTemplate(email=email)
        fromAddress = self.siteInfo.get_support_email()
        msg = self.create_message(s.encode(UTF8), text, html, origMesg,
                             fromAddress, toAddress)
        # TODO: Audit
        self.mailhost._send(mfrom=fromAddress, mto=toAddress,
                            messageText=msg)

    def create_message(self, subject, txtMessage, htmlMessage, origMesg,
        fromAddress, toAddresses):
        container = MIMEMultipart('mixed')
        container['Subject'] = str(Header(subject, UTF8))
        container['From'] = fromAddress
        container['To'] = toAddresses

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

