# coding=utf-8
from zope.contentprovider.interfaces import IContentProvider
from zope.interface.interface import Interface
from zope.schema import Bool, Int, Text, Field
from zope.viewlet.interfaces import IViewletManager

class ICanPost(Interface):
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

class IGSCanPostRule(ICanPost):
    weight = Int(   title=u'Weight',
                    description=u'The weight of this rule, used for '\
                        u'sorting the rules.',
                    default = 0)

class IGSPostingUser(ICanPost):
    pass

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

class ICanPostInfo(IViewletManager):
    u'''The viewlet manager for the Can Post information'''

    passedInUserInfo = Field(title=u'Passed-In User Information',
        description=u'User information for the person to be checked.',
        required=False)

