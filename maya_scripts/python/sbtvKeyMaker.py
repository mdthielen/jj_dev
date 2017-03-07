#!/usr/local/python

# Jib Jab Studios
# Author: Mark Thielen
# email:  mdthielen@gmail.com
# Start date: 3/6/2017
# Version: 1.0.0

# Usage:
# To create the sbtvKey.txt which is used by sbtvInfo.py
# Generates the episode and sequence lists based on the folders in the episode_folder

import os

'''
Format for key_file:

EPISODE <episode_number> <description>
SEQ <seq_number> <description>

'''

def main():
    episode_folder = '/Volumes/public/StoryBots/production/series/ask_the_storybots'
    episodes = [f for f in os.listdir(episode_folder) if f[3] =='_' if f[0] != '.']
    key_file = r'/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/' \
                      r'jj_dev/maya_scripts/python/sbtvKey.txt'
    stage = '2_production'

    lines = []
    for episode in sorted(episodes):
        lines.append('EPISODE ' + episode.split('_')[0] + ' ' + episode.split('_')[1])
        lines.append('\n')
        for seq in sorted(os.listdir(os.path.join(episode_folder, episode, stage))):
            if seq.startswith('sq'):
                lines.append('SEQ ' + seq.split('_')[0][2:] + ' ' + seq.split('_', 1)[1] + '\n')
        lines.append('\n\n')

    f = open(key_file, 'w')
    f.writelines(lines)
    f.close()

if __name__ == '__main__':
    main()