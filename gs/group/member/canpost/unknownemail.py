# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals
from email import message_from_string
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEMessage import MIMEMessage
from email.utils import parseaddr
from logging import getLogger
log = getLogger('gs.group.member.canpost.unknownemail')
from zope.cachedescriptors.property import Lazy
from zope.component import createObject, getMultiAdapter
from gs.core import to_ascii
from gs.email import send_email
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
        assert retval, 'Could not create the SiteInfo from %s' % \
            self.context
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        assert retval, 'Could not create the GroupInfo from %s' % \
            self.context
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

    def notify(self, toAddress, origMesg):
        s = '{0}: Problem Posting (Action Required)'.format(
            self.groupInfo.name)
        email = parseaddr(toAddress)[1]
        text = self.textTemplate(email=email)
        html = self.htmlTemplate(email=email)
        fromAddress = self.siteInfo.get_support_email()
        msg = self.create_message(s, text, html, origMesg, fromAddress,
                                  toAddress)
        # TODO: Audit
        # --=mpj17=-- Forward error-correction, to ensure we have everything
        # needed to send the message.
        if fromAddress and email and msg:
            lm = 'Sending "{0}" to <{1}> from <{2}>'
            logMsg = to_ascii(lm.format(s, email, fromAddress))
            log.info(logMsg)
            send_email(fromAddress, email, msg)
        else:
            lm = 'Failed to send "{0}" message of length {1} to <{2}> '\
                 'from <{3}>'
            logMsg = to_ascii(lm.format(s, len(msg), toAddress,
                                        fromAddress))
            log.info(logMsg)

    @staticmethod
    def create_return_message(msg):
        retval = MIMEMessage(msg)
        s = msg.get('Subject', 'No subject').decode('ascii', 'ignore')
        retval['Content-Description'] = 'Returned message: {0}'.format(s)
        retval['Content-Disposition'] = 'inline'
        retval.set_param('name', 'Returned message')
        del retval['MIME-Version']
        return retval

    @staticmethod
    def create_container(subject, fromAddress, toAddresses):
        retval = MIMEMultipart('mixed')
        retval['Subject'] = str(Header(subject, UTF8))
        retval['From'] = fromAddress
        retval['To'] = toAddresses
        return retval

    def create_message(self, subject, txtMessage, htmlMessage, origMesg,
                       fromAddress, toAddresses):
        container = self.create_container(subject, fromAddress, toAddresses)

        messageTextContainer = MIMEMultipart('alternative')
        container.attach(messageTextContainer)

        txt = MIMEText(txtMessage, 'plain', UTF8)
        messageTextContainer.attach(txt)

        html = MIMEText(htmlMessage, 'html', UTF8)
        messageTextContainer.attach(html)

        msg = message_from_string(origMesg)
        m = self.create_return_message(msg)
        container.attach(m)

        retval = container.as_string()
        assert retval
        return retval
