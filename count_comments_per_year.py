import argparse
import json
import zstandard as zstd
from datetime import datetime
from collections import defaultdict

CHUNK_SIZE = 16384


def extract_comments(zst_file):
    # A dictionary to keep track of comments per year
    comments_per_year = defaultdict(int)

    # Create a Zstandard decompression context
    dctx = zstd.ZstdDecompressor()

    # Open the zst file for reading in binary mode
    with open(zst_file, 'rb') as fh:
        # Create a decompression stream
        with dctx.stream_reader(fh) as reader:
            buffer = ""

            while True:
                chunk = reader.read(CHUNK_SIZE)
                if not chunk:
                    break

                buffer += chunk.decode(errors='ignore')

                while True:
                    position = buffer.find('\n')

                    if position == -1:
                        break

                    line = buffer[:position]
                    buffer = buffer[position + 1:]

                    try:
                        obj = json.loads(line)

                        # Extract the created_utc and convert to year
                        comment_date = datetime.utcfromtimestamp(int(obj['created_utc']))
                        comments_per_year[comment_date.year] += 1

                    except json.JSONDecodeError:
                        continue

            for year, count in sorted(comments_per_year.items()):
                print(f"{year}: {count} comments")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count Reddit comments per year from a zst compressed file.')
    parser.add_argument('zst_file', help='Path to the zst compressed file containing Reddit comments.')

    args = parser.parse_args()
    extract_comments(args.zst_file)