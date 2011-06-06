# coding=utf-8
from zope.interface.interface import Interface
from zope.schema import Bool, Choice, Int, Text, TextLine
from zope.contentprovider.interfaces import IContentProvider

class IGSPostingUser(Interface):
    canPost = Bool(title=u'Can Post',
      description=u'Can the user post the the group?',
      required=True)
      
    statusNum = Int(title=u'Status Number',
      description=u'The reason the user cannot post to the group, as '\
        u'a number. 0 if the user can post.',
      required=True)
      
    status = Text(title=u'Status',
      description=u'The reason the user cannot post to the group, as '\
        u'a textual description.',)

class IGSUserCanPostContentProvider(IContentProvider):
    """The content provider for the context menu"""
    
    statusNum = Int(title=u"Status Number",
      description=u"The status number returned by the code that "\
        u"determined if the user could post.",
      required=False,
      default=0)
      
    status = Text(title=u"Posting Status",
      description=u'The posting status of the user.',
      required=False,
      default=u"")
    
    pageTemplateFileName = Text(title=u"Page Template File Name",
      description=u'The name of the ZPT file that is used to render the '\
        u'status message.',
      required=False,
      default=u"browser/templates/canpost.pt") 

