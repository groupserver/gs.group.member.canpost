# coding=utf-8
from textwrap import TextWrapper
from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.group.privacy.interfaces import IGSGroupVisibility
from gs.group.base.page import GroupPage

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

