
CMS VPN logger-inner
======================


.. image:: https://img.shields.io/badge/license-Apache%202.0-informational
   :target: https://www.apache.org/licenses/LICENSE-2.0.txt
   :alt: LICENSE


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: STYLE


.. image:: https://img.shields.io/circleci/build/gh/trussworks/cmslogin
   :target: https://circleci.com/gh/trussworks/cmslogin/tree/master
   :alt: CIRCLECI


Helps logging in to the CMS VPN via openconnect-tinyproxy: https://github.com/trussworks/openconnect-tinyproxy

Usage
-----

You need the openconnect-tinyproxy on disk. In 1Password, right click on the
record that has your EUA password and TOTP. In the context menu choose "Copy
UUID".

Now, you can run the script by passing the path to the tinyproxy followed by the UUID:


.. code-block:: console

   $ python3 -m cmslogin ~/src/truss/works/openconnect-tinyproxy/ rsfq7iycufda7m5acghwyodapq
   Spawning child process
   waiting for username prompt...
   sending username
   waiting for password prompt...
   sending password
   waiting for totp prompt...
   fetching totp
   sending totp
   finished, switching to interactive

   POST https://cloudvpn.cms.gov/
   Got CONNECT response: HTTP/1.1 200 OK
   CSTP connected. DPD 30, Keepalive 20
   Connected as 10.232.43.156, using SSL, with DTLS in progress
   Established DTLS connection (using OpenSSL). Ciphersuite ECDHE-ECDSA-AES256-GCM-SHA384.
   Connect Banner:
   | *        You are accessing a U.S. Government information system.          *
   | *      UNAUTHORIZED ACCESS OR USE OF THIS COMPUTER        *
   | *                        SYSTEM IS PROHIBITED BY LAW                            *
   | By clicking Accept, you authorize the U.S. Government to monitor, intercept, and search and seize any communication or data transiting or stored on this information system. Any communication or data transiting or stored on this information system may be disclosed or used for any lawful U.S. Government purpose.
   | ********************************    WARNING    ********************************
   |



Development
-----------

You need pre-commit and poetry:

.. code-block:: console

   brew install poetry ; brew install pre-commit

Inside the project directory you can enter a virtual environment like so:

.. code-block:: console

   poetry shell