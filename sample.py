# coding: utf-8
from auto_liker import AutoLiker
 
# Set parameter
max_like_num = 100
config_path = './config.ini'

hashtag = '東京カメラ部'

# Generate instance
auto_liker = AutoLiker()

auto_liker.load_user_info(config_path)
auto_liker.login()
auto_liker.prepare(hashtag, avoid_popular_post=True)

print('Start to like photos on {}'.format(hashtag))
exists_next_pic = True
while auto_liker.liked_num < max_like_num and exists_next_pic is True:
    exists_next_pic = auto_liker.press_like_and_next()
    print(' - like {}/{}'.format(auto_liker.liked_num, max_like_num))

print('You Pressed {} Likes at #{}'.format(auto_liker.liked_num, hashtag))