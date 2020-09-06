import click


class Release:
    def __init__(self, repo, version, requests_session):
        self.repo = repo
        self.version = version

        self.requests_session = requests_session

        self.github_data = self.get()

    def exists(self):
        return bool(self.github_data)

    def tag_exists(self):
        response = self.requests_session.get(
            f"/repos/{self.repo}/git/refs/tags/v{self.version}"
        )
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    def body_matches(self, contents):
        return self.github_data["body"] == contents

    def get(self):
        response = self.requests_session.get(
            f"/repos/{self.repo}/releases/tags/v{self.version}"
        )
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()

    def create(self, name, contents):
        response = self.requests_session.post(
            f"/repos/{self.repo}/releases",
            json={
                "tag_name": "v" + name,
                "name": name,
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
                click.echo(
                    f"Release for {self.version} does not exist. Creating it...", fg="green"
                )
                release_data = self.create(self.version, contents)
                click.echo(release_data["html_url"])
            else:
                click.secho(
                    f"Git tag not found for {self.version}. A tag needs to be pushed before we can create a release for it.",
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
