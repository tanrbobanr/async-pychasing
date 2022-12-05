"""An asynchronous version of [pychasing](https://pypi.org/project/pychasing/) 
(a wrapper for the https://ballchasing.com API).

:copyright: (c) 2022 Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__title__ = "async-pychasing"
__author__ = "Tanner B. Corcoran"
__email__ = "tannerbcorcoran@gmail.com"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022 Tanner B. Corcoran"
__version__ = "0.0.1"
__description__ = ("An asynchronous version of [pychasing]("
                   "https://pypi.org/project/pychasing/) (a wrapper for the "
                   "https://ballchasing.com API)")
__url__ = "https://github.com/tanrbobanr/async-pychasing"
__download_url__ = "https://pypi.org/project/async-pychasing/"


from ._client import Client
from ._session import Session
