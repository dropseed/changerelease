import re


SKIP_VERSIONS = ["Unreleased"]


class Changelog:
    def __init__(self, path, contents):
        self.path = path
        self.contents = contents
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
