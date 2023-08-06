import zstandard
import re
import argparse

def count_json_objects_and_tokens_in_zst(file_name):
    object_count = 0
    token_count = 0
    token_pattern = re.compile(r'\b\w+\b')  # Regex to match words (including numbers)
    buffer_size = 2**27  # 128MB

    with open(file_name, 'rb') as file_handle:
        dctx = zstandard.ZstdDecompressor()
        with dctx.stream_reader(file_handle) as reader:
            while True:
                chunk = reader.read(buffer_size)
                if not chunk:
                    break

                lines = chunk.split(b"\n")
                for line in lines:
                    if line.startswith(b"{") and line.endswith(b"}"):
                        object_count += 1
                        comment = line.decode(errors='ignore')
                        try:
                            body = comment.split('"body":', 1)[1].split(',', 1)[0].strip('"')
                            tokens = token_pattern.findall(body)
                            token_count += len(tokens)
                        except IndexError:
                            continue

    return object_count, token_count



parser = argparse.ArgumentParser(description="Counts JSON objects and tokens from zst file.")
parser.add_argument('files', metavar='file', type=str, nargs='+', help="The zst files for processing.")
parser.add_argument('-s', '--single', action='store_true', help="Output results for each zst archive individually.")
parser.add_argument('-a', '--all', action='store_true', help="Output the total sum of the counts from all zst files.")

args = parser.parse_args()

# check for options
if args.single and args.all:
    print("Please choose -s/--single or -a/--all, not both.")
    exit(1)


total_objects_all = 0
total_tokens_all = 0

for zst_file in args.files:
    number_of_objects, total_tokens = count_json_objects_and_tokens_in_zst(zst_file)
    
    if args.all:
        total_objects_all += number_of_objects
        total_tokens_all += total_tokens
    elif args.single:
        print(f"Number of JSON objects in {zst_file}: {number_of_objects}")
        print(f"Total number of tokens in 'body' fields in {zst_file}: {total_tokens}")


if args.all:
    print(f"Total number of JSON objects in all files: {total_objects_all}")
    print(f"Total number of tokens in 'body' fields in all files: {total_tokens_all}")