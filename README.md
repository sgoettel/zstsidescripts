# zstsidescripts
This is a place where I've dumped a bunch of side scripts I ended up writing while working with Pushshift's zst [archive files](https://academictorrents.com/details/7c0645c94321311bb05bd879ddee4d0eba08aaee).

You can find my main script that does the "heavy lifting" over [here](https://github.com/sgoettel/rzcf). That's the one you'll want if you're looking to search keywords, filter out content, and other stuff.

This scripts here will let you poke around the zst files to get a feel for the data structure, pull out content based on time, and other simple tasks like that.

Make sure that the `zstandard` library is installed on your machine.

- [archivesampler.py](#archivesamplerpy)
- [count_comments_per_year.py](#count_comments_per_yearpy)
- [objects_and_tokens.py](#objects_and_tokenspy)
- [trim_username_comments.py](#trim_username_commentspy)
- [comment_tree.py](#comment_treepy)

---

## archivesampler.py

The script works by extracting one comment from each month of available data in the archive. The purpose of this is to help analyze the structural changes in the JSON format of the comments over time. The output JSON file will be saved in the same directory as your .zst file. Run: `python3 archivesampler.py path/to/your/file.zst`


## count_comments_per_year.py

This script does a simple job - it counts Reddit comments in a zst file, grouped by year. It extracts the `created_utc` from each JSON object (comment), converts it to year, and tallies up the comments. To use, run: `python3 count_comments_per_year.py path/to/your/file.zst`

## objects_and_tokens.py

This script counts both the JSON objects and tokens (words and numbers) within the 'body' field of each object. You can get individual count reports for each file with `-s` or get the total count from all files with `-a`. Noteworthy, the chunk size in this script is set to 128MB, I just played around with a larger chunk size here to experiment with different performance characteristics.
Run: `python3 count_json_objects_and_tokens.py -s path/to/your/file.zst` for single file stats, or `-a` for total stats.

## trim_username_comments.py

This script is designed to filter out Reddit comments from specific users (or mainly bots). Common use-cases include excluding comments from users such as "[deleted]", "AutoModerator", or any other usernames you might want to omit. Script is also capable of removing "empty" body keys, like `"[removed]"` or `"[deleted]"` via `-rd` or `--removed-deleted`. Run: `trim_username_comments.py -a "AutoModerator" -rd path/to/your/file.zst` (filters out all comments from u/AutoModerator as well as all deleted/removed comments). The script supports filtering multiple authors at once, e.g. `python3 trim_comments.py -a "bot2" -a "bot1 path/to/zst.zst` (filters out all comments from u/bot1 and u/bot2).

## comment_tree.py

Script with some couple more functions to explain, it processes the zst-compressed file of Reddit comments to extract comments associated with specific threads or all threads. You can specify a particular thread using the `link_id` of a post or use `-a` for all excisting threads within a zst file/subreddit.

The script allows two ways to display comments:

-   **structured Format**: Comments are structured in the hierarchical format, similar to how they appear on Reddit. In this format, responses to top-level comments are displayed as sub-comments (or children) of the respective top-level comment. This structure uses the `parent_id` of each comment to determine its placement within the hierarchy.
-   **flat Format**: Comments are simply listed in a flat manner without preserving any hierarchy.

Using the `-a` option, the script can extract comments from all threads in the zst file. The output comments are saved in JSON files, named after their respective `link_id` with a suffix `_tree` for structred output or `_flat` for flat output.


`python3 comment_tree.py [-l] [-a] [-s|-f] path/toyourfiles.zst` 

Where:

-   `-l` is the link_id and targets a specific Reddit thread.
-   `-a` extracts comments from all threads.
-   `-s` or `-f` determine the format, structured or flat, respectively.


I hope these tools will help you in your exploration of the Pushshift archives and Reddit data.
