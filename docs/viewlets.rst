.. _viewlets:

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
they are shown in the :doc:`notifications`. 
