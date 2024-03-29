#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import vk_api
import urllib.request
import os.path
import sys, getopt
import time


def main():
    vk_token = ''
    owner_id = ''
    argv = sys.argv[1:]
  
    opts = []
    try:
        opts, args = getopt.getopt(argv, "t:o:")
    except:
        print("Error")
    for opt, arg in opts:
        if opt in ['-t']:
            vk_token = arg
        elif opt in ['-o']:
            owner_id = arg
        
    vk_session = vk_api.VkApi(token = vk_token)
    vk = vk_session.get_api()
    wall = vk.wall.get(owner_id = owner_id)
    wall_items = wall['items']
    image_dir = str(owner_id).lstrip('-')
    isExist = os.path.exists(image_dir)
    if not isExist:
        os.makedirs(image_dir)
    for item in wall_items:
        if 'attachments' in item:
            attachments = item['attachments'][0]
            if 'photo' in attachments:
                photo = attachments['photo']['sizes']
                for size in photo:
                    if size['type'] == 'y':
                        url = size['url']
                        filename = image_dir + "/" + str(attachments['photo']['id']) + ".jpg"
                        if os.path.isfile(filename):
                            print("File exists with name " + filename)
                        else:
                            urllib.request.urlretrieve(url, filename)
                            time.sleep(1)

if __name__ == '__main__':
    main()
