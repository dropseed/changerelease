import os
import re

import requests
import click

from .release import Release
from .changelog import Changelog
from .api import APISession


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--changelog",
    default="CHANGELOG.md",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    show_default=True,
)
@click.option("--tag-prefix", default="v", show_default=True, envvar="CR_TAG_PREFIX")
@click.option("--no-tag-prefix", default=False, is_flag=True, envvar="CR_NO_TAG_PREFIX")
@click.option("--repo", envvar="GITHUB_REPOSITORY", required=True)
@click.option(
    "--api-url",
    envvar="GITHUB_API_URL",
    default="https://api.github.com",
)
@click.option("--token", envvar="GITHUB_TOKEN", required=True)
def sync(changelog, tag_prefix, no_tag_prefix, repo, api_url, token):
    if no_tag_prefix:
        tag_prefix = ""

    requests_session = APISession(base_url=api_url)
    requests_session.headers.update(
        {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token " + token,
        }
    )

    cl = Changelog(changelog)

    for version in cl.versions:
        click.secho(f"\nSyncing version {version}", bold=True)
        version_contents = cl.parse_version_content(version)
        if not version_contents:
            click.secho(f"No content found for version {version}", fg="yellow")
            continue

        release = Release(repo, tag_prefix, version, requests_session)
        release.sync(version_contents)

    # TODO fail if tag doesn't exist yet? (continue w/ others though)
    click.secho(f"\nGitHub releases on {repo} synced with {cl.path}", fg="green")


if __name__ == "__main__":
    cli()
