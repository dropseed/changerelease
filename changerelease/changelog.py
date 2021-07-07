import re


SKIP_VERSIONS = ["Unreleased"]
RE_VERSION_HEADING = r"## "
RE_VERSION_NAME = r"\[?([^\[\]\s]+)\]?"
RE_VERSION_CONTENTS = r"([\s\S]+?)"
RE_LINK_DEFINITIONS = r"\[.+\]: "
RE_END_STRING = r"\Z"
RE_VERSION_HEADING_LINE = f"^{RE_VERSION_HEADING}{RE_VERSION_NAME}.*$"


class Changelog:
    def __init__(self, path, contents):
        self.path = path
        self.contents = contents
        self.versions = self.parse_versions()

    def parse_versions(self):
        version_names = re.findall(RE_VERSION_HEADING_LINE, self.contents, re.MULTILINE)
        version_names = [x for x in version_names if x not in SKIP_VERSIONS]
        return version_names

    def parse_version_content(self, version):
        matches = re.findall(
            f"^{RE_VERSION_HEADING}\[?{version}\]?.*${RE_VERSION_CONTENTS}^({RE_VERSION_HEADING}|{RE_LINK_DEFINITIONS}|{RE_END_STRING})",
            self.contents,
            re.MULTILINE,
        )

        if not matches:
            return ""

        return matches[0][0].strip()
