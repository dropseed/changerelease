# changerelease

Sync your GitHub Release notes with your `CHANGELOG.md`.

This tool expects that you follow the [Keep a Changelog](https://keepachangelog.com/) format.

## Use the GitHub Action

```yml
name: changerelease
on:
  workflow_dispatch: {}
  push:
    paths: [CHANGELOG.md]
    branches: [master]
    tags: ["*"]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
    - uses: dropseed/changerelease@v1
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        # optional
        tag_prefix: v
        changelog: CHANGELOG.md
```

## Use the Python package

```sh
$ pip install changerelease
$ changerelease sync --repo org/repo --token TOKEN
```
