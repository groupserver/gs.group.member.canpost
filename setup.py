# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014, 2015 OnlineGroups.net and Contributors.
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
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.txt', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.txt"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(name='gs.group.member.canpost',
      version=version,
      description="Determine if a group member can post.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          'License :: OSI Approved :: Zope Public License',
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='groupserver member post group private secret',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://github.com/groupserver/gs.group.member.canpost',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.group', 'gs.group.member'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytz',
          'zope.app.apidoc',
          'zope.app.pagetemplate',
          'zope.browserpage',
          'zope.cachedescriptors',
          'zope.component',
          'zope.contentprovider',
          'zope.interface',
          'zope.tal',
          'zope.tales',
          'zope.schema',
          'zope.viewlet',
          'gs.content.email.base',
          'gs.content.email.layout',
          'gs.core',
          'gs.database',
          'gs.email',
          'gs.group.base',
          'gs.group.list.base',
          'gs.group.member.base',
          'gs.group.privacy',
          'gs.profile.email.base',
          'gs.profile.notify',
          'gs.viewlet',
          'Products.CustomUserFolder',
          'Products.GSGroup',
          'Products.XWFCore',
          'Products.GSProfile',
      ],
      entry_points="""# -*- Entry points: -*-
        """,)
