# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
import re
import sys
if sys.version_info >= (3, ):
    from urllib.parse import quote
else:
    from urllib import quote
from textwrap import TextWrapper
from zope.component import getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from gs.content.email.base import (GroupEmail, TextMixin)
from gs.group.list.base.html2txt import convert_to_txt
from gs.group.privacy.interfaces import IGSGroupVisibility
from .interfaces import IGSPostingUser


class CannotPostMessage(GroupEmail):

    def supportAddress(self, userInfo):
        to = self.siteInfo.get_support_email()
        subject = 'Cannot Post to {0}'.format(self.groupInfo.name)
        body = self.message_body(userInfo)
        retval = self.mailto(to, subject, body)
        return retval

    def message_body(self, userInfo):
        gn = self.groupInfo.name
        sn = self.siteInfo.name
        cp = self.can_post_for_user(userInfo)
        m = 'I had a problem sending an email to %s on %s <%s>. '\
            'The issue was "%s (Reason Number %s)"' % \
            (gn, sn, self.groupInfo.url, cp.status, cp.statusNum)
        retval = 'Hi!\n\n%s\n\nI need your help because...' % \
            TextWrapper().fill(m)
        return retval

    def can_post_for_user(self, userInfo):
        group = self.groupInfo.groupObj
        retval = getMultiAdapter((group, userInfo), IGSPostingUser)
        return retval


class CannotPostMessageText(CannotPostMessage, TextMixin):
    spaceRE = re.compile(r'\s+')

    def __init__(self, context, request):
        CannotPostMessage.__init__(self, context, request)
        filename = 'cannot-post-%s-to-%s.txt' % \
            (self.loggedInUserInfo.id, self.groupInfo.id)
        self.set_header(filename)

    def cp_to_txt(self, cp):
        t = convert_to_txt(cp)
        retval = self.spaceRE.sub(' ', t).strip()
        return retval


# Unknown Email Address
class UnknownEmailMessage(GroupEmail):

    def quote(self, msg):
        retval = quote(to_ascii(msg))
        assert retval
        return retval

    @Lazy
    def groupVisibility(self):
        retval = IGSGroupVisibility(self.groupInfo)
        assert retval
        return retval


class UnknownEmailMessageText(UnknownEmailMessage, TextMixin):
    def __init__(self, context, request):
        super(UnknownEmailMessageText, self).__init__(context, request)
        filename = 'unknown-email-%s.txt' % self.groupInfo.id
        self.set_header(filename)

    def format_message(self, m):
        retval = self.fill(m)
        return retval
