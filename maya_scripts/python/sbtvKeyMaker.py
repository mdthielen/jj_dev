#!/usr/bin/python

"""Generate the sbtvKey.txt from the folders on the server.

Usage:
To create the sbtvKey.txt which is used by sbtvInfo.py
Generates the episode and sequence lists based on the folders in the episode_folder

Format for key_file:

EPISODE <episode_number> <description>
SEQ <seq_number> <description>
"""

import os


def main():
    episode_folder = '/Volumes/public/StoryBots/production/series/ask_the_storybots'
    episodes = [f for f in os.listdir(episode_folder) if f[3] == '_' if f[0] != '.']
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

__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/6/2017"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
