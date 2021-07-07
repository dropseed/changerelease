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
    assert (
        cl.parse_version_content("5.1.0b1")
        == """release-date

:   2021-04-02 10.25 P.M UTC+6:00

release-by

:   Asif Saif Uddin

-   Add sentinel_kwargs to Redis Sentinel docs.
-   Depend on the maintained python-consul2 library. (#6544).
-   Use result_chord_join_timeout instead of hardcoded default value.
-   Upgrade AzureBlockBlob storage backend to use Azure blob storage
    library v12 (#6580).
-   Improved integration tests.
-   pass_context for handle_preload_options decorator (#6583).
-   Makes regen less greedy (#6589).
-   Pytest worker shutdown timeout (#6588).
-   Exit celery with non zero exit value if failing (#6602).
-   Raise BackendStoreError when set value is too large for Redis.
-   Trace task optimizations are now set via Celery app instance.
-   Make trace_task_ret and fast_trace_task public.
-   reset_worker_optimizations and create_request_cls has now app as
    optional parameter.
-   Small refactor in exception handling of on_failure (#6633).
-   Fix for issue #5030 \\"Celery Result backend on Windows OS\\".
-   Add store_eager_result setting so eager tasks can store result on
    the result backend (#6614).
-   Allow heartbeats to be sent in tests (#6632).
-   Fixed default visibility timeout note in sqs documentation.
-   Support Redis Sentinel with SSL.
-   Simulate more exhaustive delivery info in apply().
-   Start chord header tasks as soon as possible (#6576).
-   Forward shadow option for retried tasks (#6655).
-   \--quiet flag now actually makes celery avoid producing logs
    (#6599).
-   Update platforms.py \\"superuser privileges\\" check (#6600).
-   Remove unused property [autoregister]{.title-ref} from the Task
    class (#6624).
-   fnmatch.translate() already translates globs for us. (#6668).
-   Upgrade some syntax to Python 3.6+.
-   Add [azureblockblob_base_path]{.title-ref} config (#6669).
-   Fix checking expiration of X.509 certificates (#6678).
-   Drop the lzma extra.
-   Fix JSON decoding errors when using MongoDB as backend (#6675).
-   Allow configuration of RedisBackend\\'s health_check_interval
    (#6666).
-   Safeguard against schedule entry without kwargs (#6619).
-   Docs only - SQS broker - add STS support (#6693) through kombu.
-   Drop fun_accepts_kwargs backport.
-   Tasks can now have required kwargs at any order (#6699).
-   Min py-amqp 5.0.6.
-   min billiard is now 3.6.4.0.
-   Minimum kombu now is5.1.0b1.
-   Numerous docs fixes.
-   Moved CI to github action.
-   Updated deployment scripts.
-   Updated docker.
-   Initial support of python 3.9 added."""
    )
