# zstsidescripts
This is a place where I've dumped a bunch of side scripts I ended up writing while working with Pushshift's zst [archive files](https://academictorrents.com/details/7c0645c94321311bb05bd879ddee4d0eba08aaee).

You can find my main script that does the "heavy lifting" over [here](https://github.com/sgoettel/rzcf). That's the one you'll want if you're looking to search keywords, filter out content, and other stuff.

This scripts here will let you poke around the zst files to get a feel for the data structure, pull out content based on time, and other simple tasks like that.

Make sure that the `zstandard` library is installed on your machine.

1. archivesampler.py: The script works by extracting one comment from each month of available data in the archive. The purpose of this is to help analyze the structural changes in the JSON format of the comments over time. The output JSON file will be saved in the same directory as your .zst file. Run: `python3 archivesampler.py path/to/your/file.zst`

2. count_comments_per_year.py: This script does a simple job - it counts Reddit comments in a zst file, grouped by year. It extracts the `created_utc` from each JSON object (comment), converts it to year, and tallies up the comments. To use, run: `python3 count_comments_per_year.py path/to/your/file.zst`

I hope these tools will help you in your exploration of the Pushshift archives.
