from .base import Runnable
from typing import Any, Dict
import asyncio

class RunnableParallel(Runnable):
    """
    RunnableParallel (hoặc RunnableMap) cho phép chạy nhiều Runnable song song 
    trên cùng một input và trả về kết quả dưới dạng dictionary.
    """

    def __init__(self, steps: Dict[str, Runnable]):
        self.steps = steps

    def invoke(self, input: Any) -> Dict[str, Any]:
        """
        Chạy các bước một cách đồng bộ.
        Mặc dù tên là 'Parallel', phiên bản đồng bộ này chạy tuần tự để đơn giản hóa 
        hoặc có thể dùng ThreadPoolExecutor nếu cần tối ưu hóa IO-bound.
        Ở đây cài đặt chạy tuần tự cho đơn giản.
        """
        results = {}
        for key, runnable in self.steps.items():
            results[key] = runnable.invoke(input)
        return results

    async def ainvoke(self, input: Any) -> Dict[str, Any]:
        """
        Chạy song song thực sự dùng asyncio.gather.
        """
        keys = list(self.steps.keys())
        # Tạo danh sách các coroutine
        coros = [self.steps[key].ainvoke(input) for key in keys]
        
        # Chạy đồng thời
        results_list = await asyncio.gather(*coros)
        
        # Ghép kết quả vào dict
        return dict(zip(keys, results_list))
