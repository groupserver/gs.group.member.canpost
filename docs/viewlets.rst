.. _viewlets:

Viewlets
========

Each rule will need a viewlet that provides feedback about why a
person cannot post. The code for each viewlet is relatively
simple:

* Each viewlet inherits from :class:`RuleViewlet`, and

* The ``weight`` for each viewlet is taken from the weight for the
  respective rule.

For example, the viewlet for the *Blocked from posting* rule is
as follows::

    class BlockedRuleViewlet(RuleViewlet):
        weight = BlockedFromPosting.weight

The viewlets appear in two places. First, they are shown at the
bottom of the Topic page if the person viewing the page cannot
post. Second, they are shown in the :doc:`notifications`.


Abstract blase-class
--------------------

The rule-viewlets typically inherit from the :class:`RuleViewlet`
abstract base-class.

.. class:: RuleViewlet(group):

     :param group: The group that the viewlet is for

     :class:`RuleViewlet` is an *abstract base-class* for viewlets
     that display rules.

   .. attribute:: weight

      The *weight* (sort-order) for the viewlet. Sub-classes
      must implement this property.

   .. attribute:: show

      ``True`` if the viewlet should be shown. Read only.

   .. attribute:: canPost
      
      The :class:`CanPost` instance for the current user and the
      group. Read only.


   .. attribute:: userInfo

      The user that the rule is for. Read only.
