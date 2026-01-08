import asyncio
from typing import Any, Coroutine, List

"""
Module này cung cấp các tiện ích xử lý bất đồng bộ (async). 
"""

async def gather_with_concurrency(n: int, *coros: Coroutine) -> List[Any]:
    """
    Chạy song song một danh sách coroutines nhưng giới hạn số lượng chạy đồng thời (concurrency limit).
    
    Args:
        n: Số lượng coroutine tối đa chạy cùng lúc.
        *coros: Các coroutine cần chạy.
        
    Returns:
        List kết quả theo thứ tự.
    """
    semaphore = asyncio.Semaphore(n)

    async def sem_task(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_task(c) for c in coros))
