"""
模板模块 - 提供世界观角色模板的抽象接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class TemplateProvider(ABC):
    """模板提供者抽象类"""
    
    @abstractmethod
    def get_templates(self, world_id: str) -> List[Dict]:
        """获取指定世界观的模板列表"""
        pass
    
    @abstractmethod
    def get_template_by_name(self, world_id: str, name: str) -> Optional[Dict]:
        """根据名称获取模板"""
        pass


class AITemplateGenerator(ABC):
    """AI模板生成器抽象类"""
    
    @abstractmethod
    async def generate_template(self, world_id: str, user_history: Optional[List] = None) -> Dict:
        """AI生成角色模板"""
        pass
    
    @abstractmethod
    async def recommend_template(self, user_id: str, world_id: str) -> Optional[Dict]:
        """根据用户历史推荐模板"""
        pass