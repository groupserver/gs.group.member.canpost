==============================
:mod:`gs.group.member.canpost`
==============================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Determining if a group member can post
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-12-02
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Contents:

.. toctree::
   :maxdepth: 2

   rules
   viewlets
   notifications
   HISTORY

This is the core code for determining if a group member can
post. The mailing list code, the *Topic* page and *Start a topic*
page rely on this code for determining if a member can post.

In this document I present how the :doc:`rules <rules>` for
posting are created for each different type of group. I then
discuss the :doc:`viewlets <viewlets>` and the
:doc:`notifications <notifications>` that are sent to those that
cannot post.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.group.member.canpost
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
