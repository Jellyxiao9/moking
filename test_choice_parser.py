from app.engine.choice_parser import extract_choices

# 测试用剧情文本
test_story = """
雨夜的霓虹灯在湿漉漉的街道上晕开。你站在第七分局的台阶前。

你可以：
1. 推开那扇门，走进警局
2. 在门口多观察一会儿
3. 转身离开，先去码头看看

烟雾缭绕中，几个老警探抬起头。
"""

print("测试1：带显式选项的剧情")
choices = extract_choices(test_story)
for i, choice in enumerate(choices, 1):
    print(f"  {i}. {choice}")

print("\n测试2：不带显式选项的剧情")
test_story2 = """
雨夜的城市寂静无声。你感觉身后有人跟踪，但回头看时什么也没有。
也许你应该加快脚步，或者找个地方躲起来。
"""

choices2 = extract_choices(test_story2)
for i, choice in enumerate(choices2, 1):
    print(f"  {i}. {choice}")

print("\n✅ 测试完成")