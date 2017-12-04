# blog_parsing
A git repo for scraping all of the comments off of all of the posts of a blogger blog.

This was a little script I wrote because I wanted to get all of the comments from a blogger site.

You'll need to register a project with google [here](https://console.developers.google.com/iam-admin/iam/project) in order to use their api

You'll need a clientsecret.json file, formatted like specified in [this link](https://developers.google.com/api-client-library/python/guide/aaa_client_secrets)

my client_secrets.json looks like this: 
```
{
  "installed": {
    "client_id":<CLIENT_ID,
    "project_id":<PROJECT_ID>,
    "client_secret":<CLIENT_SECRET>,
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost:8080"]
  }
}
```
