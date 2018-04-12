#

from bs4 import BeautifulSoup
from slugify import slugify

import requests
import shutil
import os
url = '...'
domain = ''
output_folder = './output'
username = '...'
password = '...'

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')

lessons = soup.find_all('li', class_='toc-level-1')
print(len(lessons))

parallel = 0
# shutil.rmtree(output_folder, ignore_errors=True)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# module_name = "Module 0"
module_name = slugify(soup.find('h1').text)
for  lindex, lesson in enumerate(lessons):
    lesson_name = str(lindex) + "_-_" + slugify(lesson.a.text)
    if lesson_name.startswith('Module') and not 'Summary' in lesson_name:
        module_name =  lesson_name
        if not os.path.exists(output_folder + '/' + module_name):
            os.makedirs(output_folder + '/' + module_name)
        print(module_name)
        for index, video in enumerate(lesson.find_all('a')):
            video_name = slugify(str(index) + '_-_' + video.text)
            video_url = domain + video.get('href')
            video_out = output_folder + '/' + module_name + '/' + video_name + '.mp4'
            # print('        ', domain + video_url)
            # print('        ', video_out)
            if not os.path.exists(video_out):
                if parallel < 2:
                    background = "&"
                    parallel = parallel + 1
                    os.system ("youtube-dl -u {} -p {} --output '{}' {} {}".format(username, password, video_out, video_url, background))
    else:
        if not os.path.exists(
                output_folder + '/' + module_name + '/' + lesson_name):
            os.makedirs(output_folder + '/' + module_name + '/' + lesson_name)
        print('   ', lesson_name)
        for index, video in enumerate(lesson.find_all('a')):
            video_name = slugify(str(index) + '_-_' + video.text)
            video_url = domain + video.get('href')
            video_out = output_folder + '/'  + module_name + '/' + lesson_name + '/' + video_name + '.mp4'
            # print('        ', domain + video_url)
            # print('        ', video_out)
            if not os.path.exists(video_out):
                if parallel < 30:
                    background = "&"
                    parallel = parallel + 1
                else:
                    background = ""
                os.system ("youtube-dl -u {} -p {} --output '{}' {} {}".format(username, password, video_out, video_url, background))