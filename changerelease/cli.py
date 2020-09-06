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
)
@click.option("--repo", default=lambda: os.environ.get("GITHUB_REPOSITORY", ""))
@click.option(
    "--api-url",
    default=lambda: os.environ.get("GITHUB_API_URL", "https://api.github.com"),
)
@click.option("--token", default=lambda: os.environ.get("GITHUB_TOKEN", ""))
def sync(changelog, repo, api_url, token):
    requests_session = APISession(base_url=api_url)
    requests_session.headers.update(
        {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token " + token,
        }
    )

    response = requests_session.get("/user")
    if not response.ok:
        click.secho(f"Failed to authenticate using token '{token}'", fg="red")
        exit(1)
    click.echo(f"Acting on behalf of {response.json()['login']}")

    cl = Changelog(changelog)

    for version in cl.versions:
        click.secho(f"\nSyncing version {version}", bold=True)
        version_contents = cl.parse_version_content(version)
        if not version_contents:
            click.secho(f"No content found for version {version}", fg="yellow")
            continue

        release = Release(repo, version, requests_session)
        release.sync(version_contents)

    click.secho(f"\nGitHub releases on {repo} synced with {cl.path}", fg="green")


if __name__ == "__main__":
    cli()
