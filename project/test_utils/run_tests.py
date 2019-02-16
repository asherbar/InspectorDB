#!/usr/bin/env python
import os
import sys
from pathlib import Path

project_root = str(Path(os.path.dirname(os.path.realpath(__file__))).parents[1])

try:
    import manage
except ImportError:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Add project root to path:
    sys.path.append(project_root)
    import manage
import project.test_utils.postgres_container_utils as pcu
from project.test_utils.postgres_container_utils import PostgresContainerManager


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.test_utils.settings'
    sys.argv = [sys.argv[0], 'test'] + sys.argv[1:]
    # Go up two directories to project root:
    os.chdir(project_root)
    with PostgresContainerManager() as global_pcm:
        pcu.global_pcm = global_pcm
        manage.main()


if __name__ == '__main__':
    main()
