#!/usr/bin/env python

import os
import sys
import time

import requests


def get_project_build_jobs():
    response = requests.get('https://circleci.com/api/v1.1/project/github/{}/{}'.format(
                            os.environ['CIRCLE_PROJECT_USERNAME'].lower(),
                            os.environ['CIRCLE_PROJECT_REPONAME']
                        ),
                        auth=(os.environ['CIRCLE_TOKEN'], ''))
    if response.status_code != 200:
        raise RuntimeError("Request failed: {}".format(response.text))
    return response.json()


def get_tag_build_jobs(tag):
    builds_for_tag = []
    for build in get_project_build_jobs():
        if build.get('vcs_tag', None) != tag:
            continue
        builds_for_tag.append(build)
    return builds_for_tag


STATUS_FAILED = 0
STATUS_SUCCESS = 1
STATUS_WAIT = 2

def get_tag_build_status(tag):
    tag_build_jobs = get_tag_build_jobs(tag)
    if not tag_build_jobs:
        return STATUS_WAIT

    builds_running = False
    for build in tag_build_jobs:
        if build['lifecycle'] == 'finished':
            if build['status'] != 'success':
                return STATUS_FAILED
        else:
            build_running = True

    if builds_running:
        return STATUS_WAIT
    else:
        return STATUS_SUCCESS


def await_builds_for_tag(tag):
    success_count = 0
    sys.stderr.write('Waiting for jobs for tag {}\n'.format(tag))
    while True:
        build_status = get_tag_build_status(tag)
        if build_status == STATUS_FAILED:
            sys.stderr.write('Jobs for tag failed!\n')
            return 1
        elif build_status == STATUS_SUCCESS:
            success_count += 1
            if success_count == 2:
                sys.stderr.write('Jobs for tag succeeded.\n')
                return 0
        else:
            success_count = 0
        time.sleep(5)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(await_builds_for_tag(sys.argv[1]))
    else:
        sys.stderr.write('Usage: {} <tag>\n'.format(sys.argv[0]))
        sys.exit(1)
