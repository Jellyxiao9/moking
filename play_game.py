"""
完整游戏测试 - 命令行版互动叙事
"""

from app.services.story_service import StoryService
import time

def print_with_delay(text, delay=0.02):
    """逐字打印，模拟打字机效果"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print("\n")

def play_game():
    print("\n" + "="*50)
    print("        墨境 · 互动叙事引擎")
    print("="*50 + "\n")

    # 选择世界观
    print("请选择世界观：")
    print("1. 赛博朋克 (cyberpunk)")
    print("2. 奇幻 (fantasy)")
    print("3. 黑色电影 (noir)")

    world_map = {"1": "cyberpunk", "2": "fantasy", "3": "noir"}
    choice = input("\n请输入数字 (1-3): ").strip()
    world = world_map.get(choice, "noir")

    # 开场描述
    print("\n请描述你的角色或开场场景（例如：我是一个寻找真相的记者）")
    opening = input("> ").strip()
    if not opening:
        opening = "一个陌生人走进了这座城市最阴暗的酒吧"

    print("\n" + "="*50)
    print("故事开始...")
    print("="*50 + "\n")

    # 开始故事
    service = StoryService()
    result = service.start_story(world=world, opening=opening)

    print_with_delay(result["content"])
    print("\n" + "-"*30)

    # 游戏循环
    story_id = result["story_id"]
    turn_count = 1

    while True:
        # 显示选项
        print("\n【你的选择】")
        for i, choice_text in enumerate(result["choices"], 1):
            print(f"{i}. {choice_text}")

        print("\n0. 结束游戏")

        # 获取用户输入
        user_input = input("\n请输入数字选择: ").strip()

        if user_input == "0":
            print("\n游戏结束，感谢游玩！")
            break

        # 处理选项
        try:
            idx = int(user_input) - 1
            if 0 <= idx < len(result["choices"]):
                selected = result["choices"][idx]
                print(f"\n你选择了: {selected}\n")
                print("-"*30 + "\n")

                # 继续故事
                result = service.continue_story(story_id, selected)
                print_with_delay(result["content"])
                turn_count += 1
                print("\n" + "-"*30)
            else:
                print("无效选择，请重新输入")
        except ValueError:
            print("请输入数字")

if __name__ == "__main__":
    play_game()