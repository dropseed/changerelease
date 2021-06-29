import os

from changerelease.changelog import Changelog


def load_changelog(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        contents = f.read()
    return Changelog(path, contents)


def test_parse_example():
    cl = load_changelog("keepachangelog_example.md")
    assert cl.parse_versions() == [
        "1.0.0",
        "0.3.0",
        "0.2.0",
        "0.1.0",
        "0.0.8",
        "0.0.7",
        "0.0.6",
        "0.0.5",
        "0.0.4",
        "0.0.3",
        "0.0.2",
        "0.0.1",
    ]
    assert (
        cl.parse_version_content("0.3.0")
        == """### Added
- RU translation from [@aishek](https://github.com/aishek).
- pt-BR translation from [@tallesl](https://github.com/tallesl).
- es-ES translation from [@ZeliosAriex](https://github.com/ZeliosAriex)."""
    )


def test_parse_pandoc():
    """
    rst converted to md using pandoc
    CHANGELOG.rst -f rst -t markdown -o CR_CHANGELOG.md
    """
    cl = load_changelog("celery_pandoc_changelog.md")
    assert cl.parse_versions() == [
        "5.1.2",
        "5.1.1",
        "5.1.0",
        "5.1.0rc1",
        "5.1.0b2",
        "5.1.0b1",
    ]
    assert (
        cl.parse_version_content("5.1.0rc1")
        == """release-date

:   2021-05-02 16.06 P.M UTC+3:00

release-by

:   Omer Katz

-   Celery Mailbox accept and serializer parameters are initialized from
    configuration. (#6757)
-   Error propagation and errback calling for group-like signatures now
    works as expected. (#6746)
-   Fix sanitization of passwords in sentinel URIs. (#6765)
-   Add LOG_RECEIVED to customize logging. (#6758)"""
    )
