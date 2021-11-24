import base64

import click
import cls_client

from .release import Release
from .changelog import Changelog
from .api import APISession
from . import __version__


cls_client.set_project_key("cls_pk_8zTGqaUxvBdWYEgjJpkEfoM2")
cls_client.set_project_slug("changerelease")
cls_client.set_version(__version__)
cls_client.set_ci_tracking_enabled(True)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--changelog",
    default="CHANGELOG.md",
    show_default=True,
    envvar="CR_CHANGELOG",
)
@click.option("--remote-changelog", is_flag=True, envvar="CR_REMOTE_CHANGELOG")
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
@cls_client.track_command(include_kwargs=["changelog", "remote_changelog", "tag_prefix", "no_tag_prefix", "limit"])
def sync(
    changelog, remote_changelog, tag_prefix, no_tag_prefix, repo, api_url, limit, token
):
    if no_tag_prefix:
        tag_prefix = ""

    requests_session = APISession(base_url=api_url)
    requests_session.headers.update(
        {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token " + token,
        }
    )

    if remote_changelog:
        click.echo(f"Fetching current {changelog} from the {repo} repo")
        response = requests_session.get(f"/repos/{repo}/contents/{changelog}")
        response.raise_for_status()
        changelog_contents = base64.b64decode(response.json()["content"]).decode(
            "utf-8"
        )
    else:
        with open(changelog, "r") as f:
            changelog_contents = f.read()

    cl = Changelog(changelog, changelog_contents)

    outline = "-" * 80

    results = []

    versions = cl.versions
    if limit > -1:
        click.echo(f"Limiting to {limit} of {len(versions)} versions")
        versions = versions[:limit]

    for version in versions:
        release = Release(repo, tag_prefix, version, requests_session)
        suffix = " (pre-release)" if release.prerelease else ""
        click.secho(f"\nSyncing version {release.version}{suffix}", bold=True)

        version_contents = cl.parse_version_content(version)
        click.echo(f"{outline}\n{version_contents or '(empty)'}\n{outline}")
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
