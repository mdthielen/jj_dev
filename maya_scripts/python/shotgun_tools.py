#!/usr/bin/python
"""General shotgun tools"""

try:
    # noinspection PyUnresolvedReferences
    import shotgun_api3
    sg = shotgun_api3.Shotgun('https://jibjab.shotgunstudio.com',
                              script_name='shotgun_tools',
                              api_key='911d535f8e3d29a1fb6402b67159cef8f6e211aa761791df5adf70735816fb92')
except ImportError, e:
    print e, ' - contact administrator to install'
    exit()


def update():
    data = {
        'description': 'Open on a beautiful field with fuzzy bunnies',
        'sg_status_list': 'ip',
        'code': '090'
        }

    result = sg.update('Shot', 3115, data)
    print result


def batch(shots, execute=False, verbose=True):
    print ('\nShotgun batch name change')
    print ('-------------------------')
    batch_data = []

    for shot in shots:
        if '_' in shot['code']:
            shot_name_change = shot['code'].split('_')[1]
        else:
            shot_name_change = '{}_{}'.format('_'.join(f for f in shot['sg_sequence']['name'].split('_') if f.isdigit()), shot['code'])
        if verbose and not execute:
            print ('Original name: {} --> New name: {}'.format(shot['code'], shot_name_change))
        if execute:
            batch_data.append({"request_type": "update", "entity_type": "Shot", "entity_id": shot['id'], "data": {"code": shot_name_change}})

    if execute:
        batch_log = sg.batch(batch_data)
        i = 0
        for shot_change in batch_log:
            print ('Changed shot {} to: {}'.format(shots[i]['code'], shot_change['code']))
            i += 1
        print ('Total shots: {}'.format(len(shots)))


def find(project_id=153):
    # http://developer.shotgunsoftware.com/python-api/cookbook/usage_tips.html?highlight=big%20buck%20bunny
    # sequence_id = 384  # Sequence "100_FOO"
    # for finding a seq by id
    # shots = sg.find("Sequence", [['id', 'is', sequence_id]], fields)
    # print shots

    # fields = ['shots', 'name']

    sg_project = sg.find("Project", [['id', 'is', project_id]])
    print ('Project found: {}'.format(sg_project))

    # for findings all shots in a project
    shots = sg.find("Shot", [['project.Project.id', 'is', project_id]], ['code', 'sg_sequence'])
    print ('Shots found: {}'.format(shots))

    return shots


if __name__ == '__main__':
    print ('Jib Jab Studios Start')
    print ('---------------------')
    project_shots = find()
    batch(project_shots, execute=True)
    print ('---------------------')
    print ('\nJib Jab Studios End')


__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "4/26/17"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
