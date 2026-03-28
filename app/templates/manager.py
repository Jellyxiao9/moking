"""
模板管理器 - 统一管理所有世界观的角色模板
高内聚：模板相关的所有逻辑都在这里
低耦合：其他模块只通过这个管理器访问模板
"""

import importlib
from typing import List, Dict, Optional
from app.templates import TemplateProvider


class TemplateManager:
    """模板管理器"""
    
    # 世界观与模板模块的映射
    _WORLD_MODULES = {
        "noir": "app.templates.noir_templates",
        "cyberpunk": "app.templates.cyberpunk_templates",
        "fantasy": "app.templates.fantasy_templates",
        "xianxia": "app.templates.xianxia_templates",
        "strategy": "app.templates.strategy_templates",
        "urban": "app.templates.urban_templates",
        "cthulhu": "app.templates.cthulhu_templates",
        "wasteland": "app.templates.wasteland_templates",
    }
    
    def __init__(self):
        self._cache = {}  # 缓存已加载的模板
    
    def _load_templates(self, world_id: str) -> List[Dict]:
        """懒加载指定世界观的模板"""
        if world_id in self._cache:
            return self._cache[world_id]
        
        module_name = self._WORLD_MODULES.get(world_id)
        if not module_name:
            return []
        
        try:
            module = importlib.import_module(module_name)
            templates = module.get_templates()
            self._cache[world_id] = templates
            return templates
        except ImportError:
            # 模板文件不存在，返回空列表
            return []
    
    def get_templates(self, world_id: str) -> List[Dict]:
        """获取指定世界观的模板列表"""
        return self._load_templates(world_id)
    
    def get_template_by_id(self, world_id: str, template_id: str) -> Optional[Dict]:
        """根据ID获取模板"""
        templates = self._load_templates(world_id)
        for t in templates:
            if t.get("id") == template_id:
                return t
        return None
    
    def get_template_by_index(self, world_id: str, index: int) -> Optional[Dict]:
        """根据索引获取模板（用于随机）"""
        templates = self._load_templates(world_id)
        if 0 <= index < len(templates):
            return templates[index]
        return None

    def get_all_tags(self) -> List[str]:
        """获取所有标签（去重）"""
        all_tags = set()
        for world_id in self._WORLD_MODULES.keys():
            templates = self.get_templates(world_id)
            for t in templates:
                tags = t.get("tags", [])
                all_tags.update(tags)
        return sorted(list(all_tags))
    
    def get_templates_by_tag(self, tag: str, world_id: str = None) -> List[Dict]:
        """根据标签获取模板
        - 如果指定 world_id，只返回该世界观的模板
        - 如果不指定，返回所有世界观的模板
        """
        results = []
        worlds = [world_id] if world_id else self._WORLD_MODULES.keys()
        
        for w in worlds:
            templates = self.get_templates(w)
            for t in templates:
                if tag in t.get("tags", []):
                    results.append({
                        "world": w,
                        "template": t
                    })
        return results
    
    def recommend_by_tags(self, preferred_tags: List[str], world_id: str = None, limit: int = 3) -> List[Dict]:
        """根据偏好标签推荐模板
        - preferred_tags: 用户偏好的标签列表
        - world_id: 可选，限定世界观
        - limit: 返回数量
        """
        # 计算每个模板的匹配分数
        scores = []
        worlds = [world_id] if world_id else self._WORLD_MODULES.keys()
        
        for w in worlds:
            templates = self.get_templates(w)
            for t in templates:
                tags = t.get("tags", [])
                score = sum(1 for tag in preferred_tags if tag in tags)
                if score > 0:
                    scores.append({
                        "world": w,
                        "template": t,
                        "score": score,
                        "matched_tags": [tag for tag in preferred_tags if tag in tags]
                    })
        
        # 按分数排序，取前 limit 个
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:limit]

# 全局单例
template_manager = TemplateManager()