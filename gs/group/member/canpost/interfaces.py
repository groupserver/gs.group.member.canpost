# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED 'AS IS' AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals, absolute_import, print_function
from zope.contentprovider.interfaces import IContentProvider
from zope.interface.interface import Interface
from zope.schema import Bool, Int, Text, Field
from zope.viewlet.interfaces import IViewletManager


class ICanPost(Interface):
    canPost = Bool(
        title='Can post',
        description='Can the user post the the group?',
        required=True)

    statusNum = Int(
        title='Status Number',
        description='The reason the user cannot post to the group, as a number. 0 if the user can '
                    'post.',
        required=True)

    status = Text(
        title='Status',
        description='The reason the user cannot post to the group, as a textual description.',
        required=True)


class IGSCanPostRule(ICanPost):
    weight = Int(
        title='Weight',
        description='The weight of this rule, used for sorting the rules.',
        default=0)


class IGSPostingUser(ICanPost):
    pass


class IGSUserCanPostContentProvider(IContentProvider):
    'The content provider for the context menu'

    statusNum = Int(
        title='Status Number',
        description='The status number returned by the code that determined if the user could '
                    'post.',
        required=False,
        default=0)

    status = Text(
        title='Posting Status',
        description='The posting status of the user.',
        required=False,
        default='')

    pageTemplateFileName = Text(
        title='Page Template File Name',
        description='The name of the ZPT file that is used to render the status message.',
        required=False,
        default='browser/templates/canpost.pt')


class ICanPostInfo(IViewletManager):
    'The viewlet manager for the Can Post information'

    passedInUserInfo = Field(
        title='Passed-In User Information',
        description='User information for the person to be checked.',
        required=False)
