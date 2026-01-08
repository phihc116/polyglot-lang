from abc import ABC, abstractmethod
from typing import Any, List, Iterator, AsyncIterator, Union, Dict
import asyncio

class Runnable(ABC):
    """
    Lớp cơ sở cho tất cả các đối tượng Runnable.
    Định nghĩa giao diện chuẩn cho invoke, batch, stream và các biến thể async.
    """

    def invoke(self, input: Any) -> Any:
        """
        Thực thi đồng bộ (Synchronous execution).
        Phải được triển khai bởi các lớp con.
        """
        raise NotImplementedError("invoke() must be implemented by subclasses")

    async def ainvoke(self, input: Any) -> Any:
        """
        Thực thi bất đồng bộ (Asynchronous execution).
        Mặc định: Chạy invoke() trong một thread pool để tránh chặn event loop.
        """
        return await asyncio.to_thread(self.invoke, input)

    def batch(self, inputs: List[Any]) -> List[Any]:
        """
        Thực thi hàng loạt đồng bộ.
        Mặc định: Gọi invoke() tuần tự cho từng input.
        """
        return [self.invoke(x) for x in inputs]

    async def abatch(self, inputs: List[Any]) -> List[Any]:
        """
        Thực thi hàng loạt bất đồng bộ.
        Mặc định: Gọi ainvoke() song song (concurrently) cho từng input dùng asyncio.gather.
        """
        coros = [self.ainvoke(x) for x in inputs]
        return await asyncio.gather(*coros)

    def stream(self, input: Any) -> Iterator[Any]:
        """
        Stream kết quả đồng bộ.
        Mặc định: Trả về kết quả của invoke() như một phần tử duy nhất.
        """
        yield self.invoke(input)

    async def astream(self, input: Any) -> AsyncIterator[Any]:
        """
        Stream kết quả bất đồng bộ.
        Mặc định: yield kết quả của ainvoke().
        """
        yield await self.ainvoke(input)

    def __or__(self, other: "Runnable") -> "Runnable":
        """
        Toán tử pipe (|) để nối hai Runnable lại với nhau.
        Tạo ra một RunnablePipe.
        """
        from .pipe import RunnablePipe
        return RunnablePipe(self, other)
