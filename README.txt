Introduction
============

This is the code for determining if a group member can post. Both
the mailing list code (``Products.XWFMailingListManager``) and the web
interface (``gs.group.messages.topic``) rely on this code for determining
if a member can post.

Rule
====

A person can post if one of two rules are met. One rule is for 'unclosed'
groups, the other is for closed groups.

Unclosed
--------

The first rule is that the someone can post if he or he is not blocked
from posting and the group is 'unclosed'.

*Not* blocked from posting
  A member can be added to the ``blocked_members`` list. If this occurs 
  then the member is blocked from posting.
  
The group is unclosed
  Support groups allow anyone who is not blocked to post, even if the
  person posting does not have a profile. Due to the Teutonic heritage
  of GroupServer, such groups are known as ``unclosed``.

Closed
------

The second rule is that a person can post if all of the following
conditions are met. This is the most common check, because most groups
are closed.

The group is closed
  Most groups are closed: only members can post. 

*Not* anonymous
  Only people with profiles can post to closed groups.
  
Group member
  The person posting must be a member of the group in order to post.
  
Has preferred email addresses
  To post to a group the member must have at least one verified email
  address. This rule exists to prevent people from partially creating
  a profile and then posting to a group.

The maximum posting rate has *not* been hit
  GroupServer can limit the rate that members can post. This prevents
  trite and trivial messages ("me too!") from being posted. The
  posting rate only applies to normal members: participation coaches
  and administrators are not subject to the posting rate.

Member has the required properties
  All required profile properties must be provided before a member can
  post. There are two types of required properties: those that are 
  required by the site, and those that are required for the group.

Testing
=======

The table below summarises the correct results from the most basic test
that should be carried out if the can post code is changed.

============= ====== ========== ======== ========
Group Privacy Member Non Member Admin    Anon
============= ====== ========== ======== ========
Public        Post   Not Post   Not Post Not post
Private       Post   NA         Not Post NA
Secret        Post   NA         Not Post NA
============= ====== ========== ======== ========

Post
  The person viewing the page sees the interfaces that allows him or
  her to post
  
Not Post
  The member sees messages saying that he or she cannot post.

NA
  The person should not even get so far as seeing the can post 
  information. Therefore this test is not applicable.

