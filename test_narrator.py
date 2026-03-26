from app.engine.narrator import Narrator

# 创建叙事者
narrator = Narrator()

# 测试生成开场剧情
print("正在生成开场剧情...\n")
print("=" * 50)

story = narrator.generate(
    world="noir",
    scene_description="我是一个刚从警校毕业的年轻侦探，今天第一次走进这座永远下雨的城市。"
)

print(story)
print("\n" + "=" * 50)
print("✅ 剧情生成完成")