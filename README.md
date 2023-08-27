# zstsidescripts
This is a place where I've dumped a bunch of side scripts I ended up writing while working with Pushshift's zst [archive files](https://academictorrents.com/details/7c0645c94321311bb05bd879ddee4d0eba08aaee).

You can find my main script that does the "heavy lifting" over [here](https://github.com/sgoettel/rzcf). That's the one you'll want if you're looking to search keywords, filter out content, and other stuff.

This scripts here will let you poke around the zst files to get a feel for the data structure, pull out content based on time, and other simple tasks like that.

Make sure that the `zstandard` library is installed on your machine.

1. archivesampler.py: The script works by extracting one comment from each month of available data in the archive. The purpose of this is to help analyze the structural changes in the JSON format of the comments over time. The output JSON file will be saved in the same directory as your .zst file. Run: `python3 archivesampler.py path/to/your/file.zst`

2. count_comments_per_year.py: This script does a simple job - it counts Reddit comments in a zst file, grouped by year. It extracts the `created_utc` from each JSON object (comment), converts it to year, and tallies up the comments. To use, run: `python3 count_comments_per_year.py path/to/your/file.zst`

3. comment_tree.py: objects_and_tokens.py: This script counts both the JSON objects and tokens (words and numbers) within the 'body' field of each object. You can get individual count reports for each file with `-s` or get the total count from all files with `-a`. Noteworthy, the chunk size in this script is set to 128MB, I just played around with a larger chunk size here to experiment with different performance characteristics.
Run: `python3 count_json_objects_and_tokens.py -s path/to/your/file.zst` for single file stats, or `-a` for total stats.

4. script sifts through a zst file of Reddit comments to extract all comments associated with a particular thread, identified by a `link_id`. What's special about this script is that it doesn't just pull the comments — it structures them in the hierarchical format they're presented in on Reddit. That means responses to top-level comments appear as sub-comments (or children) of the respective top-level comment. This is achieved using the `parent_id` of each comment to determine which comment or post it's replying to. The result is then saved in a JSON file, with the filename being the `link_id`. Run: `python3 extract_comment_tree.py -l linkid path/to/your/comments.zst`

I hope these tools will help you in your exploration of the Pushshift archives.
