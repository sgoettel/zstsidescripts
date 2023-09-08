import argparse
import json
import zstandard as zstd

CHUNK_SIZE = 16384

def filter_comments_by_author(zst_file, author_names):
    dctx = zstd.ZstdDecompressor()
    cctx = zstd.ZstdCompressor(level=15) # set compression level here (range 1-22); adjust as needed for optimal size/speed balance

    input_filename = zst_file
    output_filename = f"{zst_file.rsplit('.', 1)[0]}_filtered.zst"
    
    excluded_counts = {name: 0 for name in author_names}

    with open(input_filename, 'rb') as fh, open(output_filename, 'wb') as ofh:
        # create decompression and compression streams
        with dctx.stream_reader(fh) as reader, cctx.stream_writer(ofh) as writer:
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
                        author_lower = obj["author"].lower()

                        if author_lower in [name.lower() for name in author_names]:
                            excluded_counts[obj["author"]] += 1
                            continue
                        else:
                            writer.write(json.dumps(obj).encode() + b"\n") # newline after each JSON

                    except json.JSONDecodeError:
                        continue
    # output messages
    for name, count in excluded_counts.items():
        if count > 0:
            print(f"{count} comments from '{name}' excluded.")
        else:
            print(f"No comments from '{name}' found.")
    print("Script executed successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter Reddit comments from specific usernames in a zst compressed file.')
    parser.add_argument('zst_file', help='Path to the zst compressed file containing Reddit comments.')
    parser.add_argument('-a', '--author', nargs='+', help='Usernames to be filtered out.', required=True)

    args = parser.parse_args()
    filter_comments_by_author(args.zst_file, args.author)