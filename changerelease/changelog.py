import re


SKIP_VERSIONS = ["Unreleased"]


class Changelog:
    def __init__(self, path):
        self.path = path
        with open(self.path, "r") as f:
            self.contents = f.read()

        self.versions = self.parse_versions()

    def parse_versions(self):
        version_names = re.findall("^## \[(.+)\].*$", self.contents, re.MULTILINE)
        version_names = [x for x in version_names if x not in SKIP_VERSIONS]
        return version_names

    def parse_version_content(self, version):
        matches = re.findall(
            f"^## \[{version}\].*$([\s\S]+?)^(## |\[.+\]: )",
            self.contents,
            re.MULTILINE,
        )

        if not matches:
            return ""

        return matches[0][0].strip()
