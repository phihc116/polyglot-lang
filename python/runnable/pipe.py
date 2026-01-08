from .base import Runnable
from typing import Any, Iterator, AsyncIterator

class RunnablePipe(Runnable):
    """
    RunnablePipe thực hiện việc nối tiếp hai Runnable: input -> left -> right -> output.
    Cho phép chuỗi hóa các xử lý (chaining).
    """

    def __init__(self, left: Runnable, right: Runnable):
        self.left = left
        self.right = right

    def invoke(self, input: Any) -> Any:
        """Chạy left rồi lấy kết quả chạy right."""
        return self.right.invoke(self.left.invoke(input))

    async def ainvoke(self, input: Any) -> Any:
        """Chạy bất đồng bộ: await left -> await right."""
        left_result = await self.left.ainvoke(input)
        return await self.right.ainvoke(left_result)

    def stream(self, input: Any) -> Iterator[Any]:
        """
        Stream qua pipe: stream left -> stream right.
        Lưu ý: right phải hỗ trợ xử lý từng chuỗi (chunk) từ left.
        Nếu left stream nhiều chunk, right sẽ được gọi stream với từng chunk đó (flatMap).
        """
        for chunk in self.left.stream(input):
            yield from self.right.stream(chunk)

    async def astream(self, input: Any) -> AsyncIterator[Any]:
        """Async stream qua pipe."""
        async for chunk in self.left.astream(input):
            async for output_chunk in self.right.astream(chunk):
                yield output_chunk

