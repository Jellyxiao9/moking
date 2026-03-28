from app.services.story_service import StoryService

service = StoryService()

print('1. 开始新故事...')
result = service.start_story(
    world='noir',
    opening='我是一个刚从警校毕业的年轻侦探，第一次走进这座永远下雨的城市。'
)
print(f'   故事ID: {result["story_id"]}')
print(f'   剧情: {result["content"][:150]}...')
print(f'   选项: {result["choices"]}')

print('\n2. 继续故事...')
result2 = service.continue_story(
    story_id=result['story_id'],
    user_choice=result['choices'][0]
)
print(f'   新剧情: {result2["content"][:150]}...')
print(f'   新选项: {result2["choices"]}')

print('\n✅ 故事服务测试完成！')