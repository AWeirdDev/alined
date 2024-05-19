import asyncio
import time
from typing import Awaitable, Callable, ParamSpec, TypeVar


class RateLimit:
    def __init__(self, *, requests: int, per_seconds: int):
        self.DEFINED_requests = requests
        self.DEFINED_per_secs = per_seconds
        self.r = requests
        self.designated_to_wait = False
        self.last_dispatch = 0

    async def dispatch(self):
        now = time.time()

        if not self.last_dispatch:
            self.last_dispatch = now

        self.r -= 1

        if self.r < 0:
            next_second = self.last_dispatch + self.DEFINED_per_secs
            if now < next_second:
                print("Too many requests!", next_second - now)
                me = False
                if not self.designated_to_wait:
                    self.designated_to_wait = me = True

                await asyncio.sleep(next_second - now)
                if me:
                    self.r = self.DEFINED_requests
                    self.designated_to_wait = False

                return self.dispatch()
            else:
                raise RuntimeError("Uncaught! (timenow >= next_dispatch_available)")

        self.last_dispatch = now


P = ParamSpec("P")
T = TypeVar("T")


def apply_rate_limit(
    *, requests: int, per_seconds: int
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Apply rate limit to an async function.

    Args:
        requests (int): Max requests...
        per_seconds (int): ...per second.
    """

    def wrapper(fn: Callable[P, Awaitable[T]]):
        async def wrapped(*args: P.args, **kwargs: P.kwargs):
            rate_limit = RateLimit(requests=requests, per_seconds=per_seconds)
            await rate_limit.dispatch()
            return await fn(*args, **kwargs)

        return wrapped

    return wrapper
