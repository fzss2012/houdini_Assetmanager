class ReferenceModel:
    _instance = None  # 单例实例存储
    _model_data = {}  # 初始化模型数据存储
    points = []  # 初始化点列表

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReferenceModel, cls).__new__(cls)
        return cls._instance

    def set_model_data(self, key, value):
        """ 设置模型数据 """
        self._model_data[key] = value

    def get_model_data(self, key):
        """ 获取模型数据 """
        return self._model_data.get(key)

    def remove_model_data(self, key):
        """ 移除模型数据 """
        if key in self._model_data:
            del self._model_data[key]

    def clear_model_data(self):
        """ 清空所有模型数据 """
        self._model_data.clear()