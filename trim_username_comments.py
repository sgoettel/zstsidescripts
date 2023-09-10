import argparse
import json
import zstandard as zstd

CHUNK_SIZE = 16384

def filter_comments(zst_file, authors, remove_deleted):
    dctx = zstd.ZstdDecompressor()
    cctx = zstd.ZstdCompressor(level=15) # set compression level here (range 1-22); adjust as needed for optimal size/speed balance

    input_filename = zst_file
    output_filename = f"{zst_file.rsplit('.', 1)[0]}_filtered.zst"
    
    excluded_counts = {author: 0 for author in authors}
    deleted_count = 0
    # create decompression and compression streams

    with open(input_filename, 'rb') as fh, open(output_filename, 'wb') as ofh:
        with dctx.stream_reader(fh) as reader, cctx.stream_writer(ofh) as writer:
            buffer = ""

            deleted_tags = ["[removed]", "[deleted]", "[removed by reddit]"]
            
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

                        if obj["author"].lower() in authors:
                            excluded_counts[obj["author"].lower()] += 1
                            continue

                        if remove_deleted and obj["body"] in deleted_tags:
                            deleted_count += 1
                            continue

                        writer.write(json.dumps(obj).encode() + b"\n") # newline after each JSON

                    except json.JSONDecodeError:
                        continue

    return excluded_counts, deleted_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter Reddit comments based on certain criteria.')
    parser.add_argument('zst_file', help='Path to the zst compressed file containing Reddit comments.')
    parser.add_argument('-a', '--author', action='append', help='Username(s) to be filtered out.', required=True) # used nargs='+' before, still trying to figure out.. 
    parser.add_argument('-rd', '--remove-deleted', action='store_true', help='Remove comments with deleted or removed body.')

    args = parser.parse_args()

    authors_to_remove = [author.lower() for author in args.author]

    excluded_counts, deleted_count = filter_comments(args.zst_file, authors_to_remove, args.remove_deleted)

    # output messages
    for name, count in excluded_counts.items():
        if count > 0:
            print(f"{count} comments from '{name}' excluded.")
        else:
            print(f"No comments from '{name}' found.")
    
    if args.remove_deleted:
        print(f"{deleted_count} 'deleted/removed' comments excluded.")

    print("Script executed successfully.")