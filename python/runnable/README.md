# Runnable Module (Python)

Module này mô phỏng core `Runnable` của LangChain bằng Python thuần, giúp xây dựng các pipeline xử lý dữ liệu dễ dàng thông qua cơ chế chaining (chuỗi hóa).

## Cấu trúc thư mục

```
runnable/
├── base.py            # Lớp cơ sở Runnable, định nghĩa interface invoke/batch/stream/async
├── pipe.py            # Xử lý toán tử | (pipe) để nối các Runnable
├── lambda_runnable.py # Wrapper cho các hàm (function) thường hoặc async function
├── runnable_async.py  # Các tiện ích xử lý bất đồng bộ (thay cho async.py)
├── retry.py           # Logic thử lại (Retry) khi gặp lỗi
├── parallel.py        # Chạy song song nhiều nhánh (RunnableParallel / RunnableMap)
└── errors.py          # Các định nghĩa lỗi tùy chỉnh
```

## Tính năng chính

1.  **Chaining (`|`)**: Nối các step xử lý lại với nhau.
    ```python
    chain = step1 | step2 | step3
    chain.invoke(input)
    ```

2.  **Async Support**: Hỗ trợ đầy đủ `ainvoke`, `abatch`, `astream`.
    ```python
    await chain.ainvoke(input)
    ```

3.  **Batch Processing**: Xử lý hàng loạt input.
    ```python
    chain.batch([1, 2, 3])
    ```

4.  **Parallel Execution**: Chạy nhiều Runnable song song và trả về dict kết quả.
    ```python
    map_chain = RunnableParallel({"a": step1, "b": step2})
    ```

5.  **Retry Mechanism**: Tự động thử lại khi lỗi.
    ```python
    safe_step = RunnableRetry(step_risky, max_retries=3)
    ```

6.  **Streaming**: Hỗ trợ yield dữ liệu từng phần.

## Ví dụ sử dụng

Xem file `examples.py` (cần cập nhật để test các tính năng mới).

```python
from runnable.lambda_runnable import RunnableLambda
from runnable.parallel import RunnableParallel
from runnable.retry import RunnableRetry
import asyncio

# Định nghĩa các hàm xử lý
def add_one(x): 
    return x + 1

def mul_two(x): 
    return x * 2

# Tạo Runnable từ hàm
r_add = RunnableLambda(add_one)
r_mul = RunnableLambda(mul_two)

# Tạo chain đơn giản
chain = r_add | r_mul 
print(chain.invoke(3)) # (3 + 1) * 2 = 8

# Chạy song song
parallel = RunnableParallel({
    "original": RunnableLambda(lambda x: x),
    "plus_one": r_add,
    "times_two": r_mul
})

print(parallel.invoke(5))
# Output: {'original': 5, 'plus_one': 6, 'times_two': 10}
```
