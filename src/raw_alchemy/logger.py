"""
统一的日志处理模块
提供一致的日志接口，支持多种输出方式（控制台、队列、文件等）
"""
from typing import Optional, Callable, Any


class Logger:
    """统一的日志处理器"""
    
    def __init__(self, log_target: Optional[Any] = None, file_id: Optional[str] = None):
        """
        初始化日志处理器
        
        Args:
            log_target: 日志输出目标，可以是：
                       - None: 使用 print
                       - Queue 对象: 使用 queue.put()
                       - Callable: 直接调用该函数
            file_id: 文件标识符，用于多文件处理时区分日志来源
        """
        self.log_target = log_target
        self.file_id = file_id
    
    def log(self, message: str, level: str = "INFO"):
        """
        发送日志消息
        
        Args:
            message: 日志消息内容
            level: 日志级别 (INFO, ERROR, SUCCESS, WARNING)
        """
        formatted_msg = self._format_message(message)
        
        if self.log_target is None:
            # 默认使用 print
            print(formatted_msg)
        elif hasattr(self.log_target, 'put'):
            # 队列模式（多进程/GUI）
            self.log_target.put({
                'id': self.file_id,
                'msg': message,
                'level': level
            })
        elif callable(self.log_target):
            # 函数模式（CLI）
            self.log_target(formatted_msg)
        else:
            # 兜底
            print(formatted_msg)
    
    def _format_message(self, message: str) -> str:
        """格式化消息，添加文件 ID 前缀"""
        if self.file_id:
            return f"[{self.file_id}] {message}"
        return message
    
    def info(self, message: str):
        """信息级别日志"""
        self.log(message, "INFO")
    
    def error(self, message: str):
        """错误级别日志"""
        self.log(message, "ERROR")
    
    def success(self, message: str):
        """成功级别日志"""
        self.log(message, "SUCCESS")
    
    def warning(self, message: str):
        """警告级别日志"""
        self.log(message, "WARNING")


def create_logger(log_target: Optional[Any] = None, file_id: Optional[str] = None) -> Logger:
    """
    工厂函数：创建日志处理器实例
    
    Args:
        log_target: 日志输出目标
        file_id: 文件标识符
    
    Returns:
        Logger 实例
    """
    return Logger(log_target, file_id)
