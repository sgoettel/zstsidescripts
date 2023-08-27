import argparse
import json
import zstandard as zstd

CHUNK_SIZE = 16384


def extract_comments(zst_file, link_id, structured):
    # Create a Zstandard decompression context
    dctx = zstd.ZstdDecompressor()

    comments_mapping = {}
    top_level_comments = []

    # Open the zst file for reading in binary mode
    with open(zst_file, 'rb') as fh:
        
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

                        # Check for link_id
                        if obj.get('link_id', '').replace('t3_', '') == link_id:
                            comments_mapping[obj['id']] = obj
                            if obj['parent_id'].startswith('t3_'):
                                top_level_comments.append(obj['id'])
                            obj['responses'] = []

                    except json.JSONDecodeError:
                        continue

    if not structured:
        comment_list = list(comments_mapping.values())
        output_filename = f"{link_id}_flat.json"
        with open(output_filename, 'w') as outfile:
            json.dump(comment_list, outfile, indent=4)
        return

    for comment_id, comment in comments_mapping.items():
        parent_id = comment['parent_id'].replace('t1_', '')
        if parent_id in comments_mapping:
            comments_mapping[parent_id]['responses'].append(comment)

    comment_tree = {comment_id: comments_mapping[comment_id] for comment_id in top_level_comments}

    # Write the comments to a JSON file
    output_filename = f"{link_id}_tree.json"
    with open(output_filename, 'w') as outfile:
        json.dump(comment_tree, outfile, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Reddit comments from a zst compressed file based on a post link ID.')
    parser.add_argument('zst_file', help='Path to the zst compressed file containing Reddit comments.')
    parser.add_argument('-l', '--link_id', help='link ID of the Reddit post without prefix.', default=None)
    parser.add_argument('-s', '--structured', action='store_true', help='If set, the output will maintain the comment tree structure.')

    args = parser.parse_args()

    if not args.link_id:
        args.link_id = input("Please provide a link ID without prefix: ")

    extract_comments(args.zst_file, args.link_id, args.structured)
