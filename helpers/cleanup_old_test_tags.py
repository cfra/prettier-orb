#!/usr/bin/env python

from subprocess import check_call, check_output, CalledProcessError
from time import time


def is_tag_old(tag):
    tag_info = (
        check_output(
            [
                "git",
                "for-each-ref",
                "--format=%(taggerdate:unix)",
                "refs/tags/{}".format(tag),
            ]
        )
        .decode("utf8")
        .strip()
    )
    if not tag_info:
        # Happens if the tag is not an annotated tag
        tag_info = (
            check_output(["git", "show", "--no-patch", "--pretty=format:%at", tag])
            .decode("utf8")
            .strip()
        )
    tag_timestamp = int(tag_info)
    return time() - tag_timestamp >= 86400


def find_old_test_tags():
    old_test_tags = []
    for tag in check_output(["git", "tag"]).decode("utf8").splitlines():
        if not tag.startswith("test-"):
            continue
        if not is_tag_old(tag):
            continue
        old_test_tags.append(tag)
    return old_test_tags


def cleanup_old_test_tags():
    check_call(["git", "fetch"])
    tags_to_clean = find_old_test_tags()
    try:
        check_call(["git", "push", "origin", "--delete"] + tags_to_clean)
    except CalledProcessError:
        # Ignore failures here, multiple instances might try to delete
        # tags at the same time.
        pass
    check_call(["git", "tag", "--delete"] + tags_to_clean)


if __name__ == "__main__":
    cleanup_old_test_tags()
