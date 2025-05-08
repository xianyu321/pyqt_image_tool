class EventManager:
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.listeners = {}  # 存储事件类型与监听器的映射

    def on(self, event_type, callback):
        """
        注册事件监听器
        :param event_type: 事件类型
        :param callback: 回调函数
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def off(self, event_type, callback = None):
        """
        注销事件监听器
        :param event_type: 事件类型
        :param callback: 回调函数
        """

        if event_type in self.listeners:
            if callback is not None:
                if callback in self.listeners[event_type]:
                    self.listeners[event_type].remove(callback)
            else:
                del self.listeners[event_type]

    # def emit(self, event_type, data=None):
    #     """
    #     触发事件
    #     :param event_type: 事件类型
    #     :param data: 传递给监听器的数据（可选）
    #     """
    #     print(f"触发事件：{event_type}, 数据：{data}")
    #     if event_type in self.listeners:
    #         for callback in self.listeners[event_type]:
    #             callback(data)
    def emit(self, event_type, *args, **kwargs):
        """
        触发事件
        :param event_type: 事件类型
        :param args: 位置参数
        :param kwargs: 关键字参数
        """
        print(f"触发事件：{event_type}, 参数：args={args}, kwargs={kwargs}")
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(*args, **kwargs)  # 将参数传递给回调函数

    @staticmethod
    def get_instance():
        """
        获取单例实例
        """
        if EventManager._instance is None:
            EventManager()
        return EventManager._instance