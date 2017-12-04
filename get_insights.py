#!/usr/bin/python3

import json
from pprint import pprint
import operator


def dedup(x):
    return {
        'Julian': 'Julian Mazaira',
        'Steven': 'Steven Jacobson',
        'JLiu'  : 'Jasper Liu',
        'Alan'  : 'Alan Delaney',
        'alan delaney': 'Alan Delaney',
        'Roman' : 'Roman Schuster',
        'BrianK': 'Brian Kraus',
        'Dylan mann': 'Dylan Mann',
        'Jasper': 'Jasper Liu',
        'ben'   : 'Ben Stollman'
    }.get(x, x)


def main():
    comments = json.load(open("comments.json", "r"))
    comments_by_name = {}

    for comment in comments:
        name = comment["author"]["displayName"]

        name = dedup(name)

        if name in comments_by_name:
            comments_by_name[name].append(comment)
        else:
            comments_by_name[name] = [comment]

    sorted_comments = sorted(comments_by_name, key=lambda k: len(comments_by_name[k]))

    for person in sorted_comments:
        print("{}: {}".format(person, len(comments_by_name[person])))

    name_to_check = "Dylan Mann"

    # pprint(list(map(lambda x: x["content"] + (" " * 90), comments_by_name[name_to_check])))


if __name__ == "__main__":
    main()
