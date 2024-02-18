#!/usr/bin/env bash
#
# Pin current dependencies versions.
#

uv pip compile requirements.dev.in
uv pip compile requirements.in
