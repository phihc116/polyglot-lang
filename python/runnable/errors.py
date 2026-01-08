class RunnableError(Exception):
    """
    Lớp lỗi cơ sở cho tất cả các lỗi trong hệ thống Runnable.
    Base exception class for all errors in the Runnable system.
    """
    pass

class RunnableExecutionError(RunnableError):
    """
    Lỗi xảy ra trong quá trình thực thi Runnable.
    Error occurred during Runnable execution.
    """
    pass

class RunnableConfigError(RunnableError):
    """
    Lỗi cấu hình (ví dụ: tham số không hợp lệ).
    Configuration error (e.g., invalid parameters).
    """
    pass
