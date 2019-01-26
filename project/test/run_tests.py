#!/usr/bin/env python
import os
import sys
from pathlib import Path

import manage
import project.test.postgres_container_utils as pcu
from project.test.postgres_container_utils import PostgresContainerManager


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.test.settings'
    sys.argv = [sys.argv[0], 'test'] + sys.argv[2:]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Go up two directories to project root:
    os.chdir(str(Path(dir_path).parents[1]))
    with PostgresContainerManager() as global_pcm:
        pcu.global_pcm = global_pcm
        manage.main()


if __name__ == '__main__':
    main()
