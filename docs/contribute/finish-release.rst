.. _finish-release:

Finish the Release
==================

.. meta::
   :description lang=en:
      Finish the semver release by creating tags

1. Create a tag:

   $ git tag -a x.x.x

   It’s recommended to use the generated Tox output from the Changelog.

2. Push the tag:

   $ git push –tags

3. In `GitHub Release
   page <https://github.com/python-semver/python-semver/release>`_
   document the new release. Select the tag from the last step and copy
   the content of the tag description into the release description.

4. Announce it in
   https://github.com/python-semver/python-semver/discussions/categories/announcements.

You’re done! Celebrate!
