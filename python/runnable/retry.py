from .base import Runnable
from typing import Any
import time
import asyncio

class RunnableRetry(Runnable):
    """
    RunnableRetry bọc một Runnable khác và tự động thử lại (retry) nếu gặp lỗi.
    """

    def __init__(self, runnable: Runnable, max_retries: int = 3, delay: float = 1.0):
        self.runnable = runnable
        self.max_retries = max_retries
        self.delay = delay

    def invoke(self, input: Any) -> Any:
        """"Thực thi với cơ chế thử lại đồng bộ."""
        last_exception = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.runnable.invoke(input)
            except Exception as e:
                last_exception = e
                # Nếu chưa phải lần cuối thì chờ rồi thử lại
                if attempt < self.max_retries:
                    time.sleep(self.delay)
        
        # Nếu hết số lần thử mà vẫn lỗi thì ném lỗi cuối cùng
        raise last_exception

    async def ainvoke(self, input: Any) -> Any:
        """Thực thi với cơ chế thử lại bất đồng bộ."""
        last_exception = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return await self.runnable.ainvoke(input)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    await asyncio.sleep(self.delay)
        
        raise last_exception
