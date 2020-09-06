import click


class Release:
    def __init__(self, repo, tag_prefix, version, requests_session):
        self.repo = repo
        self.tag_prefix = tag_prefix
        self.version = version
        self.version_tag = tag_prefix + version

        self.requests_session = requests_session

        self.github_data = self.get()

    def exists(self):
        return bool(self.github_data)

    def tag_exists(self):
        response = self.requests_session.get(
            f"/repos/{self.repo}/git/refs/tags/{self.version_tag}"
        )
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    def body_matches(self, contents):
        return self.github_data["body"] == contents

    def get(self):
        response = self.requests_session.get(
            f"/repos/{self.repo}/releases/tags/{self.version_tag}"
        )
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()

    def create(self, contents):
        response = self.requests_session.post(
            f"/repos/{self.repo}/releases",
            json={
                "tag_name": self.version_tag,
                "name": self.version,
                "body": contents,
                # TODO prerelease if semver prerelease
            },
        )
        response.raise_for_status()
        return response.json()

    def update_body(self, contents):
        response = self.requests_session.patch(
            self.github_data["url"], json={"body": contents}
        )
        response.raise_for_status()
        return response.json()

    def sync(self, contents):
        if not self.exists():
            if self.tag_exists():
                click.secho(
                    f"Release for {self.version} does not exist. Creating it...",
                    fg="green",
                )
                release_data = self.create(contents)
                click.echo(release_data["html_url"])
            else:
                click.secho(
                    f'Git tag "{self.version_tag}" not found. A tag needs to be pushed before we can create a release for it.',
                    fg="red",
                )
        elif not self.body_matches(contents):
            click.secho(
                f"Release for {self.version} exists but the changelog doesn't match. Updating the release...",
                fg="green",
            )
            self.update_body(contents)
        else:
            click.echo("No change")
