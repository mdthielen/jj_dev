"""
    sbtvInfo
    
    Copyright (c) 2015 Robert Showalter
    All Rights Reserved.
    rshowalt@c.ringling.edu
    
    Description:
        This is the core script for working within the storybot, aka "SBTV" project.

        It's purpose is retrieving sequence and shot data based on the project hierarchy.

        Many artist have been involved in this organic, and loosely regulated pipeline.
        This script and others using it attempt to organize and make sense of the
        existing pipeline and, hopefully, iron out some inconsistencies.
    
    Example usage:
        import sbtvInfo
        seqInfo = sbtvInfo.Info('101', '100')
        seqInfo.allShots
        #Returns:
        #['sh_010', 'sh_020', 'sh_030', 'sh_040', 'sh_050', 'sh_060', 'sh_070', 'sh_080', 'sh_090', 'sh_100', 'sh_110', 'sh_120', 'sh_130', 'sh_140', 'sh_150']

"""


import os


def main():
    dev = 1
    if dev:
        seq_info = Info('200', '030')
        anim_latest_files = seq_info.getLastAnim()
        for anim_latest in anim_latest_files:
            print anim_latest


def readContents(keyFile):

        text = open(keyFile, 'r')
        fileContents = text.read().splitlines()
        text.close()
        return fileContents


def getEp(ep, fileContents):
    for line in fileContents:
        if 'EPISODE' in line:
            if ep == line.split(' ')[1]:
                epName = line.split(' ')[2]
                epID = '_'.join([ep, epName])
                return epID, epName
    raise NameError('Episode number not found, check key:\n%s' % fileContents)


def getSeq(ep, seq, fileContents):
    seq_found = False
    for line in fileContents:
        if ep in line:
            seq_found = True
        elif seq_found:
            if 'SEQ' in line:
                if seq == line.split(' ')[1]:
                    seqName = line.split(' ')[2]
                    seqID = '_'.join([seq, seqName])
                    return seqID, seqName
    raise NameError('Seqence number not found, check input or update keyfile:\n    %s' % fileContents)


class Info:
    def __init__(self, ep, seq, shot=''):
        import sys
        self.ep = ep
        self.seq = seq
        self.shot = shot

        if sys.platform == 'darwin':
            keyFile = r'/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/' \
                      r'jj_dev/maya_scripts/python/sbtvKey.txt'
            if not os.path.exists(keyFile):
                keyFile = os.path.expanduser('~/Documents/maya/scripts/JibJab/jj_dev/maya_scripts/python/sbtvKey.txt')
        elif sys.platform == 'win32':
            keyFile = r'~\Documents\maya\scripts\storybots\python\sbtvKey.txt'
        elif sys.platform == 'linux2':
            keyFile = r'~/maya/scripts/storybots/python/sbtvKey.txt'
        else:
            print('couldn\'t recognize operating system')
            import sys
            sys.exit()
        if keyFile and os.path.exists(keyFile):
            print('Using keyfile: ' + keyFile)
        else:
            raise EnvironmentError('Warning: missing keyfile --> sbtvKey.txt')

        fileContents = readContents(keyFile)

        """
        stage in production
        possible selections: 1_pre-preduction, 2_production, 3_distribution
        default = 2_production
        """
        stage = '2_production'

        project_name = 'ask_the_storybots'
        local_darwin_linux_folder = 'maya/projects/JibJab/' + project_name

        if sys.platform == 'darwin':
            public_mount = '/Volumes/public/StoryBots/production/series/' + project_name
            local_mount = os.path.expanduser('~/Documents/' + local_darwin_linux_folder)
            if os.path.exists(public_mount):
                project_folder = public_mount
            elif os.path.exists(local_mount):
                project_folder = local_mount
            else:
                print 'No project exists'
                sys.exit()
        elif sys.platform == 'win32':
            project_folder = os.path.join(os.path.expanduser('~\\Documents'), 'maya', 'projects', project_name)
        elif sys.platform == 'linux2':
            project_folder = os.path.join(os.path.expanduser('~'), local_darwin_linux_folder, project_name)
        # expand this later for mac machines, though many other changes may be needed
        else:
            raise EnvironmentError('This system was not recognised')

        self.epID, self.epName = getEp(self.ep, fileContents)
        self.seqID, self.seqName = getSeq(self.ep + ' ' + self.epName, self.seq, fileContents)
        self.sequence = 'sq' + self.seqID		
        self.seqPath = os.path.join(project_folder, self.epID, stage, self.sequence)
        if not os.path.exists(self.seqPath):
            print('Warning:  Path missing: %s' % self.seqPath)
            sys.exit()
        self.allShots = sorted([x for x in os.listdir(self.seqPath) if 'sh_' in x])
        # added to fix shot folder naming inconsistencies
        if len(self.allShots) == 0:
            self.allShots = sorted([x for x in os.listdir(self.seqPath) if unicode(x).isnumeric()])
        else:
            pass

    def getLastAnim(self):

        lastAnimMAs = []
        animDir = None

        for shot in self.allShots:
            shotDir = os.path.join(self.seqPath, shot)
            for x in sorted(os.listdir(shotDir)):
                if 'maya' in x:
                    shotDirMaya = os.path.join(shotDir, x)
                    # print 'shotDirMaya:\n' + shotDirMaya
                else:
                    NameError('maya directory not found in...%s\n    ' % shotDir)

            for dept in sorted(os.listdir(shotDirMaya)):
                if 'animation' in dept:
                    animDir = os.path.join(shotDirMaya, dept)
                    # print ('animDir:\n{}'.format(animDir))
                    # print ('\n')
                else:
                    NameError('animation directory not found in...%s\n    ' % shotDirMaya)

            maPath = os.path.join(shotDirMaya, animDir)
            maFiles = sorted([f for f in os.listdir(maPath) if '.ma' in f if 'PUBLISH' not in f if not f.startswith('.') if f.startswith('sq')])

            if maFiles:
                lastAnimMAs.append(os.path.join(maPath, maFiles[-1]))

        return lastAnimMAs


if __name__ == '__main__':
    main()

__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.2"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
