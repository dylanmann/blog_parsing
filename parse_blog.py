#!/usr/bin/python3
import requests
import io
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from oauth2client.file import Storage
from os import rename
from sys import argv

blog_id = 4002814717830515080
MAX_RESULTS = 500
POST_API_URL = "https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?fetchBodies=false&maxResults={max_results}&fields=items(id%2Cpublished)&access_token={access_token}"
COMMENT_API_URL = "https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/{post_id}/comments?fetchBodies=true&fields=items(author(displayName%2Cid)%2Ccontent%2CselfLink%2CinReplyTo%2Cpost%2Cpublished)&access_token={access_token}"


def get_token():
    flow = flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/blogger',
        redirect_uri='http://localhost:8080'
    )

    flow.step1_get_authorize_url()
    storage = Storage('creds.data')

    credentials = run_flow(flow, storage)
    print(credentials.access_token)
    return credentials.access_token


def get_500_posts_from_blog(access_token, end_date=None):
    """
    Retreive the maximum number of posts from the blog
    """
    ids = []

    print("GET 500")

    api_url = POST_API_URL.format(
        blog_id=blog_id,
        max_results=MAX_RESULTS,
        access_token=access_token,
    )

    if end_date:
        api_url += "&endDate={end_date}".format(end_date=end_date)

    for result in requests.get(api_url).json().get("items"):
        ids.append(result["id"])
        new_end_date = result["published"]

    return ids, new_end_date


def get_posts_from_blog(access_token):
    """
    Get all the posts ever from the blog and return their ids as a list
    """
    print("GET posts")
    ids = []

    new_ids, end_date = get_500_posts_from_blog(access_token)

    while len(new_ids) == MAX_RESULTS:
        new_ids, end_date = get_500_posts_from_blog(access_token, end_date)
        ids.extend(new_ids)

    return ids


def main():
    argc = len(argv)
    if(argc == 1):
        access_token = get_token()
    else:
        access_token = argv[1]

    if argc == 1 or (argc > 2 and argv[2] == "blog"):
        ids = get_posts_from_blog(access_token)
        with open("post_ids.json", "w") as f:
            json.dump(ids, f)
    else:
        with open("post_ids.json", "r") as f:
            ids = json.load(f)

    count = 0

    comments = []
    for post_id in ids:
        api_url = COMMENT_API_URL.format(
            blog_id=blog_id,
            post_id=post_id,
            access_token=access_token
        )
        try:
            comments.extend(requests.get(api_url).json()['items'])
        except KeyError:
            pass
        count += 1
        if count % 10 == 0:
            print("{}/{} posts | {} comments".format(count, len(ids), len(comments)))

    rename("comments.json", "comments.json.old")

    print("done getting, now writing to file")

    with io.open('comments.json', 'w', encoding='utf-8') as f:
        json.dump(comments, f)


if __name__ == "__main__":
    main()
