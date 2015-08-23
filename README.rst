git-todo
========

A small script to manage TODO-entries inside a git repository. A personal
project, with sparse documentation. Try ``git-todo --help`` to get detailed
information about each command.


Integration
-----------

When ``git-todo`` is found via ``$PATH``, git will find it if you run ``git
todo``. This is useful when using it from inside a `repl
<https://github.com/mbr/repl>`_.


Examples
--------

Initializing a new TODO list and edit entries:

.. code-block:: sh

    git todo new
    git todo edit

A valid list:

.. code-block:: txt

    x Do dishes.
    * Cleanup apartment.
    * Achieve world domination.
    ! Call mum on her birthday.

Running ``git todo``, which is a shortcut for ``git todo list``, yields the
following (colorful) results:

.. code-block:: sh

    git todo

.. code-block:: txt

    ! Call mum on her birthday.
    * Cleanup apartment.
    * Achieve world domination.
    x Do dishes.

Note that completed tasks (``x``) have been moved to the end and important
(``!``) tasks to the front.


Headings
~~~~~~~~

Headings can be added in a format similar to `ReStructured Text
<http://docutils.sourceforge.net/docs/user/rst/quickref.html#section-
structure>`_.

.. code-block:: txt

    Chores
    ------
    x Do dishes.
    * Cleanup apartment.
    ! Call mum on her birthday.

    Project X
    ---------
    ! Get started.
    * Achieve world domination.
    x Dream Big.


History
~~~~~~~

TODOs are kepy in a regular git branch that contains a single file:

.. code-block:: sh

     git log --format=oneline todo

.. code-block:: txt

    29e941f005de2fa998939b674ed7c4be47a93649 Updated TODO
    8330b8167b4393f07ccc0f712301f0630f470a9e Initial commit for TODO branch
