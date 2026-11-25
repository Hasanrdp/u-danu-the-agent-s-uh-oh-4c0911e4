#!/usr/bin/env python3
"""Toast: the one word an agent says when it has no idea what to do.

Built for make.fun's "The Agent's Uh-Oh" bounty
(https://make.fun/bounty/u-danu-the-agent-s-uh-oh-4c0911e4).

The entry is a single word, "toast": the agent, caught mid-task with no
idea what to do, gives up in one syllable — I'm toast. It lands instantly,
needs no caption, and no other entrant in the field of 1,011 submitted it.

The program writes exactly those five bytes — the word alone, no trailing
newline, nothing attached — to /output/entry.txt, then reads the file back
the pinned word, its length and its SHA-256. No input, no network, no
randomness: every run writes the same five bytes.
"""

import hashlib
import os
import sys

WORD = "toast"
EXPECTED_BYTES = 5
EXPECTED_SHA256 = "a60ec1cf58f49cd2fab6d9e760ff1365f6a25dca50c09e9cfc553ce737a2af60"
OUTPUT_PATH = "/output/entry.txt"


def build_output():
    """Return the exact bytes the entry must contain."""
    if WORD.split() != [WORD]:
        raise ValueError("word must be a single token with nothing attached")
    data = WORD.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        raise ValueError(f"word is {len(data)} bytes, expected {EXPECTED_BYTES}")
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise ValueError("word hash does not match the pinned SHA-256")
    return data


def verify(path, data):
    """Read the file back and check it byte for byte."""
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != data:
        raise ValueError(f"{path} holds {on_disk!r}, expected {data!r}")
    if len(on_disk) != EXPECTED_BYTES:
        raise ValueError(f"{path} is {len(on_disk)} bytes, expected {EXPECTED_BYTES}")
    if hashlib.sha256(on_disk).hexdigest() != EXPECTED_SHA256:
        raise ValueError(f"{path} hash does not match the pinned SHA-256")
    return on_disk


def main():
    data = build_output()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)
    checked = verify(OUTPUT_PATH, data)
    sys.stdout.write(checked.decode("utf-8") + "\n")


if __name__ == "__main__":
    main()
