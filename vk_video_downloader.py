#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import vk_api
import sys
import os.path
import getopt
import youtube_dl

def main():
    vk_token = ''
    group_id = ''
    argv = sys.argv[1:]
  
    opts = []
    try:
        opts, args = getopt.getopt(argv, "t:g:")
    except:
        print("Error")
    for opt, arg in opts:
        if opt in ['-t']:
            vk_token = arg
        elif opt in ['-g']:
            group_id = arg

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    videos_dir = str(group_id).lstrip('-')

    albums = vk.video.getAlbums(owner_id=group_id, need_system=1)
    for album in albums['items']:
        videos = vk.video.get(owner_id=group_id, album_id=album['id'], count=100)
        for video in videos['items']:
            if 'player' in video:
                player_url = video['player']
                print(f"Player URL: {player_url}")
                video_file_name = f"{videos_dir}-videos/{video['title']}.mp4"
                if os.path.exists(video_file_name):
                    print(f"Video already downloaded: {video_file_name}")
                    continue
                ydl_opts = {
                    'outtmpl': video_file_name,
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([player_url])
                print(f"Video downloaded: {video['title']}.mp4")

if __name__ == '__main__':
    main()
