.. _rules:

Posting rules
=============

In this section I present the `Rule abstract base-class`_, and
how the `Can Post adaptor`_ is used to collect the rules for each
group.  I then provide an example of `chaining rules`_.

Rule abstract base-class
------------------------

A rule is an adaptor. It takes a user [#userType]_ and a group
[#groupType]_.  The :class:`BaseRule` abstract base-class
provides most of what is required to create a rule.

.. class:: BaseRule(userInfo, group)

   :param IGSUserInfo userInfo: The user that is being tested by
                                the rule.
   :param group: The group the user is being tested for.

   .. attribute:: __doc__

      (Abstract property: sub-classes must provide a weight.) The
      documentation on the rule, which is shown on the page
      ``rules.html`` in each group.

   .. attribute:: weight

      (Abstract property: sub-classes must provide a weight.) An
      integer that has two related functions. First, it is used
      as the sort-key to determine the order that the rules are
      checked (see `can post adaptor`_ below). Second, the
      :attr:`statusNum` is set to this value to uniquely
      identifies the rule. (No two rules should have the same
      weight as this can lead to ambiguity.)

   .. method:: check()

      (Abstract method: sub-classes must supply :meth:`check`.)
      Perform the actual check to see if a user can post to a
      group. Based on the result it sets the values in the
      dictionary ``self.s``:

      ``checked``:
        ``True`` after the check, ``False`` initially.

      ``canPost``:
         ``True`` if the user can post (see :attr:`canPost`).

      ``status``:
          A string that summarises the status (see
          :attr:`status`).

      ``statusNum``:
          A number representing the status. Normally this is set
          to :attr:`weight` (see :attr:`statusNum`).

   .. attribute:: canPost

      (Read only.) A Boolean value that is ``True`` if this rule
      thinks that the user can post the the group.

   .. attribute:: status

      (Read only.) A Unicode value that summaries why the user
      should be prevented from posting to the group.

   .. attribute:: statusNum

      (Read only.) An integer that is one of three values:

      * ``-1`` if it is unknown whether the user can post to the
        group (``canPost`` will be ``False`` in this case),
      * ``0`` if the user can post to the group (``canPost`` is
        ``True``), and
      * Set to the ``weight`` value if the user cannot post to
        the group (``canPost`` is ``False``).

Example
~~~~~~~

Most rules only provide a doc-string, the :attr:`BaseRule.weight`
attribute, and :meth:`BaseRule.check` method. For example, the
:class:`BlockedFromPosting` rule checks to see if the identifier
of the user is in the ``blocked_members`` property of the mailing
list. It then sets the ``canPost``, ``status`` and ``statusNum``
values of the ``self.s`` dictionary accordingly. Finally, it sets
``self.s['checked']`` to ``True`` to prevent the system from
performing the check more than once.

.. code-block:: python

  class BlockedFromPosting(BaseRule):
    '''A person will be prevented from posting if he or she is
    explicitly blocked by an administrator of the group.'''
    weight = 10

    def check(self):
        if not self.s['checked']:
            ml = self.mailingList
            blockedMemberIds = ml.getProperty('blocked_members', [])
            if (self.userInfo.id in blockedMemberIds):
                self.s['canPost'] = False
                self.s['status'] = 'blocked from posting'
                self.s['statusNum'] = self.weight
            else:
                self.s['canPost'] = True
                self.s['status'] = 'not blocked from posting'
                self.s['statusNum'] = 0
            self.s['checked'] = True

The **ZCML** sets up each rule as an adaptor [#WhyZCML]_. It
adapts a ``userInfo`` and the *specific* group type and provides
an ``IGSCanPostRule``. The adaptor must be a **named adaptor**,
as multiple rules are used for each group. The names are also
shown on the ``rules.html`` page in each group.

.. code-block:: xml

  <adapter
    name="Blocked from Posting"
    for="Products.CustomUserFolder.interfaces.IGSUserInfo
         gs.group.base.interfaces.IGSGroupMarker"
    provides=".interfaces.IGSCanPostRule"
    factory=".rules.BlockedFromPosting" />

Can post adaptor
----------------

The ``CanPost`` adaptor looks very very very much like the
adaptor for the `rule abstract base-class`_. However, rather than
providing a single rule it *aggregates* all the rules for a
group, giving the final answer as to weather the user can
post. It provides the answer using the same three properties as
the rules: :attr:`CanPost.canPost`, :attr:`CanPost.status` and
:attr:`CanPost.statusNum`.

.. class:: CanPost(userInfo, group)

   :param IGSUserInfo userInfo: The user that is being tested.
   :param group: The group the user is being tested for.

   .. attribute:: canPost

      ``True`` if the user can post to the group.

   .. attribute:: status

      A description of the reason the user cannot post, for the
      most important reason (the rule with lowest weight; see
      :attr:`BaseRule.weight`). Undefined if :attr:`canPost` is
      ``True``.

   .. attribute:: statusNum

      A numeric description of the reason the user cannot post,
      for the most important reason (the rule with lowest weight;
      see :attr:`BaseRule.weight`). Undefined if :attr:`canPost`
      is ``True``.

Only one ``CanPost`` adaptor is needed for *all*
group-types. That is because the it implements the **strategy**
pattern to determine the applicable rules.

Chaining Rules
--------------

The core GroupServer group types use the following inheritance
hierarchy for their interfaces::

  gs.group.base.interfaces.IGSGroupMarker
     △        △
     │        │
     │       gs.group.type.discussion.interfaces.IGSDiscussionGroup
     │        △
     │        │
     │       gs.group.type.announcement.interfaces.IGSAnnouncementGroup
     │
    gs.group.type.support.interfaces.IGSSupportGroup


This product (:mod:`gs.group.member.canpost`) provides one rule
for the ``IGSGroupMarker`` — which prevents people who have been
explicitly blocked from posting (see the `example`_ above). All
other group types inherit this rule because their
marker-interfaces inherit from the ``IGSGroupMarker``.

The discussion group (``IGSDiscussionGroup``) provides the most
rules: six in all. All these rules are inherited by the
announcement group because its marker-interface
(``IGSAnnouncementGroup``) inherits from the discussion
group. The announcement group also provides its own rule, to
ensure that only posting members can post.

The support group (``IGSSupportGroup``) provides no extra rules,
so it just has the rule that is provided by this package for all
the ``IGSGroupMarker`` groups.

..  [#userType] The user is almost always a
    ``Products.CustomUserFolder.interfaces.IGSUserInfo`` instance.

..  [#groupType] The group will be a group-folder that has been marked
    with an interface that is *generally* specific to the type of group.

..  [#whyZCML] It easier to use ZCML to set up the adaptor for
    each rule because rules can be mixed and matched by different
    group-types. By using ZCML the mixing-and-matching can be
    done with very little Python code.
