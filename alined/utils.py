import asyncio
import functools
from typing import Awaitable, Callable, ParamSpec, TypeVar


P = ParamSpec("P")
T = TypeVar("T")


def asyncify(f: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    """Async-ify a synchronous function.

    Usage:
        .. code-block :: python

            def foo(*, money: int):
                return f"I have {money} dollars"

            afoo = asyncify(foo)
            await afoo(money=10)
            # "I have 10 dollars"

    Args:
        f (f: (**P) -> T): The synchronous function.

    Returns:
        ((**P) -> Awaitable[T]): An async function.
    """

    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return await asyncio.to_thread(functools.partial(f, *args, **kwargs))

    return wrapper
