Introduction
============

This is the core code for determining if a group member can post. Both
the mailing list code (``Products.XWFMailingListManager``) and the Topic
interface (``gs.group.messages.topic``) rely on this code for 
determining if a member can post.

In this document I present how the `rules`_ for posting are created for
each different type of group. I then discuss the `viewlets`_ and the
`notification`_ that is sent to those that cannot post.

See the ``gs.group.type.discussion`` group for a real-life 
implementation of some posting rules.

Rules
=====

In this section I present the structure of `a single rule`_, and how the
`Can Post adaptor`_ is used to collect the rules for each group.  I then
provide an example of `chaining rules`_.

A Single Rule
-------------

A rule is an adaptor. It takes a user [#userType]_ and a group
[#groupType]_. It provides four properties.

``weight``
  An integer that has two related functions. First, it is used as the
  sort-key to determine the order that the rules are checked (see
  `can post adaptor`_ below). Second, it uniquely identifies the rule.
  (No two rules should have the same weight as this can lead to 
  ambiguity.)

``canPost``
  A Boolean value that is ``True`` if this rule thinks that the user
  can post the the group.

``status``
  A Unicode value that summaries why the user should be prevented from
  posting to the group.
  
``statusNum``
  An integer that is one of three values.
  
  * ``-1`` if it is unknown whether the user can post to the group
    (``canPost`` will be ``False`` in this case),
  * ``0`` if the user can post to the group (``canPost`` is ``True``), and
  * Set to the ``weight`` value if the user cannot post to the group
    (``canPost`` is ``False``).
  
In practice most rules inherit from the ``BaseRule`` abstract 
base-class. It provides three methods decorated with ``@Lazy`` to 
provide the three properties [#BaseRule]_. To make a concrete rule three
things are needed:

#.  `The check method`_, 
#.  Some `constants`_, and
#.  `The ZCML`_.

The ``check`` Method
~~~~~~~~~~~~~~~~~~~~

The ``check`` method of a rule performs the actual check to see if a
user can post to a group. Based on the result it sets the values in
the dictionary ``self.s``. This dictionary is then used to provide the
return values for the three properties of the rule.

For example, the ``BlockedFromPosting`` rule checks to see if the 
identifier of the user is in the ``blocked_members`` property of the
mailing list. It then sets the ``canPost``, ``status`` and
``statusNum`` values of the ``self.s`` dictionary accordingly. Finally,
it sets ``self.s['checked']`` to ``True``. This prevents the system 
from performing the check more than once.

Constants
~~~~~~~~~

Each rule must provide a ``__doc__`` and a ``weight``. 

The doc-string (``__doc__``) is used to provide documentation on the 
rule, which is shown on the page ``rules.html`` in each group.

The ``weight`` is used for two things. First, the `can post adaptor`_ 
uses it to sort rules, and determine the order that the rules should 
be checked [#Viewlets]_. Each weight should be unique, to prevent
ambiguity. Because of this the weights provide a very useful value for
the ``statusNum`` of each rule.

The ZCML
~~~~~~~~

The ZCML sets up each rule as an adaptor [#WhyZCML]_. It adapts a
``userInfo`` and the *specific* group type and provides an
``IGSCanPostRule``. The adaptor must be a **named adaptor**, as multiple
rules are used for each group. The names are also shown on the
``rules.html`` page in each group.

Can Post Adaptor
----------------

The ``CanPost`` adaptor looks very very very much like the adaptor for
`a single rule`_. However, rather than providing a single rule it
*aggregates* all the rules for a group, giving the final answer as to
weather the user can post. It provides the answer using the same three
properties as the rules: ``canPost``, ``status`` and ``statusNum``.

The core of the ``CanPost`` code are two loops. The first gets all the
rules for the current group::

    retval = [a for a in gsm.getAdapters((self.userInfo, self.group), 
                                          IGSCanPostRule)]

This is later sorted by the ``weight`` of each rule (see `constants`_).

The second loop determines if the user can post::

    reduce(and_, [rule.canPost for rule in self.rules], True)

Only one ``CanPost`` adaptor is needed for *all* group-types. That is
because the first loop will retrieve only the rules that are specific
to the current group-type.

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


This egg (``gs.group.member.canpost``) provides one rule, for the
``IGSGroupMarker`` — which prevents people who have been explicitly 
blocked from posting. All other group types inherit this rule because
their marker-interfaces inherit from the ``IGSGroupMarker``.

The discussion group (``IGSDiscussionGroup``) provides the most rules:
six in all. All these rules are inherited by the announcement group 
because its marker-interface (``IGSAnnouncementGroup``) inherits from
the discussion group. The announcement group also provides its own rule,
to ensure that only posting members can post.

The support group (``IGSSupportGroup``) provides no extra rules, so it
just has the rule that is provided by this package for all the
``IGSGroupMarker`` groups.

Viewlets
========

Each rule will need a viewlet that provides feedback about why a person
cannot post. The code for each viewlet is relatively simple:

* Each viewlet inherits from
  ``gs.group.member.canpost.viewlet.RuleViewlet``,

* The ``weight`` for each viewlet is taken from the weight for the
  respective rule, and

* The ``show`` attribute is set from::

    self.canPost.statusNum == self.weight``

The viewlets appear in two places. First, they are shown at the bottom 
of the Topic page if the person viewing the page cannot post. Second,
they are shown in the `notification`_. 

Notification
============

The Cannot Post notification is sent out to people who post to the 
group, but the can-post check blocks post. The notification contains the
`viewlets`_ [#NotificationViewlets]_. As such care should be taken to
ensure that each viewlet makes sense outside the context of the group,
and all links in each viewlet are **absolute** links that include the
site name.

The Cannot Post notification can be previewed by viewing the pages
``cannot-post.html`` and ``cannot-post.txt`` within each group.

..  [#userType] The user is almost always a 
    ``Products.CustomUserFolder.interfaces.IGSUserInfo`` instance.

..  [#groupType] The group will be a group-folder that has been marked
    with an interface that is *generally* specific to the type of group.

..  [#BaseRule] The ``BaseRule`` also supplies four other useful 
    properties: 

    * A ``userInfo``, 
    * A ``groupInfo``, 
    * A ``siteInfo`` and 
    * A ``mailingListInfo``. 
    
    It also initialises the dictionary ``self.s`` that the ``canPost``, 
    ``status`` and ``statusNum`` properties use.

..  [#Viewlets] The use of a ``weight`` to sort the rules was taken from
    the ``zope.viewlet`` code. Indeed, the entire structure of this 
    system was inspired by that code.

..  [#whyZCML] It easier to use ZCML to set up the adaptor for each rule
    because rules can be mixed and matched by different group-types. By
    using ZCML the mixing-and-matching can be done with very little 
    Python code.

..  [#NotificationViewlets] The Cannot Post notification contains each
    viewlet in two forms: the normal HTML version, and a plain-text
    version, which the notification generates from the HTML.

