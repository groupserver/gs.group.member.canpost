Changelog
=========

3.1.0 (2015-01-14)
------------------

* Following the ``convert_to_txt`` function to ``gs.group.list.base``.
* Naming the ReStructuredText files as such
* Moving the repository to GitHub_

.. _GitHub: https://github.com/groupserver/gs.group.member.canpost/

3.0.2 (2014-03-31)
------------------

* Adding logging to the *Unknown email address* notification

3.0.1 (2014-02-26)
------------------

* Using the ``gs.content.email.base.TextMixin`` class
* Adding ``gs.core`` to the product dependencies

3.0.0 (2013-10-09)
------------------

* Switching the notifications to use the standard code provided
  by ``gs.content.email.base``
* Switching to absolute-imports
* Further PEP-8 compliance cleanups

2.4.0 (2013-05-28)
------------------

* Removing the jQuery UI code from the ``canpost`` info

2.3.1 (2013-01-22)
------------------

* Code cleanup, thanks to `Ninja IDE`_

.. _`Ninja IDE`: http://www.ninja-ide.org

2.3.0 (2012-08-06)
------------------

* Add a delivery-address check

2.2.0 (2012-07-18)
------------------

* Use the new ``gs.email`` product to send the notifications

2.1.0 (2012-06-22)
------------------

* Updating SQLAlchemy

2.0.0 (2012-03-28)
------------------

* New *Cannot post* notification and a *Unknown email address*
  notification that has both HTML and plain-text components
* Allow the *Cannot post* viewlet manager to work from anywhere
* 

1.0.1 (2011-11-22)
------------------

* Updated documentation

1.0.0 (2011-17-11)
------------------

* Initial release, inspired (loosely) on code provided by
  ``Products.XWFMailingListManager``.
