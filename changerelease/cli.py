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
    envvar="CR_CHANGELOG",
)
@click.option("--tag-prefix", default="v", show_default=True, envvar="CR_TAG_PREFIX")
@click.option("--no-tag-prefix", default=False, is_flag=True, envvar="CR_NO_TAG_PREFIX")
@click.option("--repo", envvar="GITHUB_REPOSITORY", required=True)
@click.option(
    "--api-url",
    envvar="GITHUB_API_URL",
    default="https://api.github.com",
)
@click.option("--limit", default=-1, envvar="CR_LIMIT")
@click.option("--token", envvar="GITHUB_TOKEN", required=True)
def sync(changelog, tag_prefix, no_tag_prefix, repo, api_url, limit, token):
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

    outline = "-" * 80

    results = []

    versions = cl.versions
    if limit > -1:
        click.echo(f"Limiting to {limit} of {len(versions)} versions")
        versions = versions[:limit]

    for version in versions:
        click.secho(f"\nSyncing version {version}", bold=True)
        version_contents = cl.parse_version_content(version)

        click.echo(f"{outline}\n{version_contents or '(empty)'}\n{outline}")

        release = Release(repo, tag_prefix, version, requests_session)
        message, synced = release.sync(version_contents)

        click.secho(message, fg="green" if synced else "red")

        results.append(synced)

    if all(results):
        click.secho(
            f"\nSynced {len(results)} GitHub Releases on {repo} with {cl.path}",
            fg="green",
        )
    else:
        failed = [x for x in results if not x]
        click.secho(f"Failed to sync {len(failed)} versions", fg="red")
        exit(1)


if __name__ == "__main__":
    cli()
