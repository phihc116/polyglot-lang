from .base import Runnable
from typing import Any, Callable, Union
import asyncio
import inspect

class RunnableLambda(Runnable):
    """
    RunnableLambda bọc một hàm Python (sync hoặc async) thành một Runnable.
    Giúp tích hợp code tùy chỉnh vào chuỗi xử lý.
    """
    
    def __init__(self, func: Callable):
        self.func = func
    
    def invoke(self, input: Any) -> Any:
        """
        Gọi hàm. Nếu hàm là async, ta không thể gọi trực tiếp trong môi trường sync 
        một cách dễ dàng mà không có event loop.
        Ở đây giả định func là sync function nếu gọi invoke().
        Nếu func là async def, invoke() sẽ trả về coroutine object (không await được ở đây).
        """
        if inspect.iscoroutinefunction(self.func):
             # Cảnh báo hoặc handle việc gọi async func trong sync context
             # Cách đơn giản: chạy event loop mới nếu cần, hoặc báo lỗi.
             # LangChain thường dùng asyncio.run() nếu top-level, nhưng nguy hiểm nếu lồng nhau.
             # Ở đây ta simply return coroutine hoặc lỗi nếu user gọi sai.
             # Nhưng để an toàn với base.ainvoke default, ta cứ gọi.
             pass
        return self.func(input)

    async def ainvoke(self, input: Any) -> Any:
        """
        Hỗ trợ cả sync function và async function.
        """
        if inspect.iscoroutinefunction(self.func):
            return await self.func(input)
        else:
            # Nếu là sync func, chạy trong thread pool (thừa kế từ base) 
            # hoặc chạy trực tiếp nếu func nhẹ.
            # Base.ainvoke đã dùng to_thread cho self.invoke, nên không cần override
            # trừ khi muốn tối ưu không dùng thread.
            # Nhưng ở đây để tường minh:
            return await super().ainvoke(input)
