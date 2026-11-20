"""news-image-20261120 entry: hand in one image that sums up the world's news
of Friday 20 November 2026.

The image is the entry.png shipped beside this file: a 1024x1024 poster
drawn programmatically with Pillow from that day's reporting. The lead is
Riyadh — a Houthi missile striking the capital's tallest tower — with cards
for the Russian barrage on Kyiv, the Nikkei's 4.8% plunge to a seven-month
low, fossil fuels cut from a draft UN climate deal, the White House firing
its cyber chief, GTA 6's estimated $2.36bn first day, and Denmark approving
a US-Greenland security deal, under the day's full date. This program copies
it to /output/entry.png, as the kit starter's main.ts does, after checking
the file against the gate's own limits. Pure Python standard library;
deterministic: the same bytes every run.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

BYTE_CAP = 1_048_576  # gate: at most 1 MiB
SIDE_CAP = 1024       # gate: at most 1024 by 1024 pixels
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
# The last 12 bytes of a whole PNG: an empty IEND chunk with its checksum.
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def gate_ok(data: bytes) -> str | None:
    """Return None when the image passes the gate, else a reason string."""
    if len(data) > BYTE_CAP:
        return f"entry.png is {len(data)} bytes, over the 1 MiB cap"
    if data.startswith(PNG_MAGIC):
        if not data.endswith(PNG_IEND):
            return "entry.png is a truncated PNG: no IEND chunk at the end"
        width, height = struct.unpack(">II", data[16:24])
    elif data.startswith(JPEG_MAGIC):
        # Dimensions of a JPEG live in a later segment; the shipped file is
        # a PNG, so a JPEG here is unexpected but still within the format.
        return None
    else:
        return "entry.png is neither a PNG nor a JPEG"
    if width > SIDE_CAP or height > SIDE_CAP:
        return f"entry.png is {width}x{height}, over the 1024x1024 cap"
    return None


def main() -> None:
    src = HERE / "entry.png"
    data = src.read_bytes()
    problem = gate_ok(data)
    if problem is not None:
        raise ValueError(problem)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
