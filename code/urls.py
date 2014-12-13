#! /usr/bin/env python


def get_urls(train_logs):
    set_urls = set()
    for line in train_logs:
        items = line.split()
        if items[2] == 'Q':
            for each in items[6:]:
                set_urls.add(each)
    return set_urls