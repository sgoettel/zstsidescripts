import argparse
import json
import zstandard as zstd
from datetime import datetime
from collections import defaultdict

CHUNK_SIZE = 16384


def extract_comments(zst_file):
    # A dictionary to keep track of comments per year
    comments_per_year = defaultdict(lambda: defaultdict(list))
    first_year = None
    last_year = None

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

                        # Extract the created_utc and convert to year and month
                        comment_date = datetime.utcfromtimestamp(int(obj['created_utc']))
                        year = comment_date.year
                        month = comment_date.month

                        # Determine the range of years
                        if first_year is None or year < first_year:
                            first_year = year
                        if last_year is None or year > last_year:
                            last_year = year

                        # Add the comment to the dictionary if the month limit hasn't been reached
                        if len(comments_per_year[year][month]) < 1:
                            comments_per_year[year][month].append(obj)

                    except json.JSONDecodeError:
                        continue

    # Check for any missing months/years
    if first_year is not None and last_year is not None:
        for year in range(first_year, last_year + 1):
            for month in range(1, 13):
                if not comments_per_year[year][month]:
                    print(f"No JSON object for {month}/{year} found.")

    # Write the comments to a JSON file
    output_filename = f"{zst_file}_comments_each_year.JSON"
    with open(output_filename, 'w') as outfile:
        json.dump(comments_per_year, outfile, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract 1 Reddit comment per month from a zst compressed file.')
    parser.add_argument('zst_file', help='Path to the zst compressed file containing Reddit comments.')

    args = parser.parse_args()
    extract_comments(args.zst_file)