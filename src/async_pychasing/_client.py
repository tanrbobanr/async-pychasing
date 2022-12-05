"""Code for the ``Client`` object.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"

from ._session import Session
import pychasing
import aiohttp
import prepr
import rlim


class Client:
    """Used to store rate limiters and the API token, with the ability to create
    new ``Session`` instances.
    
    """
    def __init__(self, token: str, auto_rate_limit: bool,
                 patreon_tier: pychasing.PatreonTier,
                 rate_limit_safe_start: bool = False, concurrent: bool = False,
                 ca_deviation: float = 0) -> None:
        """
        Arguments
        ---------
        token : str
            A ballchasing API key (acquirable
            from https://ballchasing.com/upload).
        auto_rate_limit : bool
            If `True`, the client will automatically limit API calls according
            to the given Patreon tier.
        patreon_tier : pychasing.PatreonTier
            The token-holder's Ballchasing Patreon tier.
        rate_limit_safe_start : bool, optional, default=False
            If `True`, the rate limiter will start out as fully maxed out on API
            calls.

        """
        self._token = token
        if auto_rate_limit:
            self._rate_limiters = {k:rlim.RateLimiter(*v,
                                   safestart=rate_limit_safe_start,
                                   concurrent_async=concurrent,
                                   ca_deviation=ca_deviation) for k, v
                                   in patreon_tier.value.items()}
        else:
            self._rate_limiters = None

    def __call__(self, session: aiohttp.ClientSession) -> "Session":
        """Create a new pychasing session with the given aiohttp session.
        
        """
        return Session(session, self._token, self._rate_limiters)
    
    def session(self, session: aiohttp.ClientSession) -> "Session":
        """Create a new pychasing session with the given aiohttp session.
        
        """
        return Session(session, self._token, self._rate_limiters)
    
    def __repr__(self, *args, **kwargs) -> prepr.pstr:
        return prepr.prepr(self).args(self._token, self._rate_limiters).build(
            *args, **kwargs)
