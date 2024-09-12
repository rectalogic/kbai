# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: AGPL-3.0-or-later
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--skip-mocks",
        choices=["image", "detect", "encode"],
        action="append",
        default=[],
        help="Mocks to skip when encoding test videos.",
    )


@pytest.fixture
def skip_mocks(request):
    return request.config.getoption("--skip-mocks")
