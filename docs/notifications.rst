Notifications
=============

There are two notifications: the `cannot post`_ notification is
sent to people with a profile who cannot post, while `unknown
email address`_ is sent when the email address is not recognised.

Cannot post
-----------

The Cannot Post notification is sent out to people who post to
the group, but the :doc:`rules <rules>` block the post. The
notification contains the :doc:`viewlets <viewlets>`
[#NotificationViewlets]_. As such care should be taken to ensure
that each viewlet makes sense outside the context of the group,
and all links in each viewlet are **absolute** links that include
the site name.

The Cannot Post notification can be previewed by viewing the
pages ``cannot-post.html`` and ``cannot-post.txt`` within each
group.

The notification email is sent using a variant of the class
``gs.profile.notify.sender.MessageSender``. The main difference
is the notification is constructed differently, so it can include
the original email message that was blocked. The notification
email is made up of five parts::

    ┌──────────────────────────┐
    │multipart/mixed           │
    │┌────────────────────────┐│
    ││ multipart/alternative  ││
    ││┌──────────────────────┐││
    │││┌────────────────────┐│││
    ││││text/plain          ││││
    │││└────────────────────┘│││
    │││┌────────────────────┐│││
    ││││text/html           ││││
    │││└────────────────────┘│││
    ││└──────────────────────┘││
    │└────────────────────────┘│
    │┌────────────────────────┐│
    ││ message/rfc822         ││
    │└────────────────────────┘│
    └──────────────────────────┘

* The text of the Cannot Post notification is contained within
  two components:
  
  + ``text/plain`` contains the ``cannot-post.txt`` message, and
  + ``text/html`` components contains the ``cannot-post.html``.

* The two text block are wrapped in a ``multipart/alternative``
  block.

* The message that could not be posted is placed in a
  ``message/rfc822`` block at the end of the email.

* Finally, everything is wrapped in a ``multipart/mixed`` block,
  which carries the subject line, addresses, and the rest of the
  headers.

Unknown Email Address
---------------------

The unknown email address notification can be thought of as a
highly specialised form of Cannot Post. It is sent when the
mailing list (``Products.XWFMailingListManager.XWFMailingList``)
fails to recognise the email address of the sender of a message.

The notification is constructed the same way as the `cannot
post`_ notification, with the same five parts. The text
encourages the recipient to add the email address to his or her
profile: we speculate that existing members posting from an
unknown email address is the most common reason for receiving the
notification. The rest of the message is similar to the "Not a
Member" message that is sent by the standard Cannot Post
notification. The text can be previewed by looking at the
``unknown-email.html`` and ``unknown-email.txt`` within each
group.

The unknown-email notifier (``unknownemail.Notifier`` within this
egg) avoids all use of the ``gs.profile.notify`` system — because
there is not profile to sent the notification to! To send the
notification the code assembles the email message, and sends the
post using ``gs.email.send_email``.

TODO
~~~~

The unknown email address notification should *probably* appear
in the code that handles the mailing list. However, that product
[#list]_ is due for a **huge** refactor, so the unknown email
address notification was placed here for safe-keeping.  In the
future this notification should be moved closer to the mailing
list.

..  [#NotificationViewlets] The Cannot Post notification contains each
    viewlet in two forms: the normal HTML version, and a plain-text
    version, which the notification generates from the HTML.

..  [#list] See
            <https://github.com/groupserver/Products.XWFMailingListManager>
