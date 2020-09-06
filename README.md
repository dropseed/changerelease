# changerelease

Sync your GitHub Release notes with your `CHANGELOG.md`.

This tool expects that you follow the [Keep a Changelog](https://keepachangelog.com/) format.

Note that, per [SemVer](https://semver.org/spec/v1.0.0.html#tagging-specification-semvertag), this tool also expects that your git tags are prefixed with a "v". As in, "v3.0.0" and not "3.0.0".

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
    - uses: actions/checkout@v2
    - uses: dropseed/changerelease@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Use the Python package

```sh
$ pip install changerelease
$ changerelease sync --repo org/repo --token TOKEN
```
