
#!/bin/bash

# Function to get the latest modified file based on stat mtime
get_latest_modified_file() {
  local dir="$1"
  local latest_file=""
  local latest_mtime=0

  # Loop through directory entries (excluding "." and "..")
  for entry in $(find "$dir" ! -name "." ! -name ".."); do
    # Get file stats
    file_stat=$(stat -t %Y "$entry")

    # Check if mtime is greater than current latest
    if [[ $file_stat -gt $latest_mtime ]]; then
      latest_mtime=$file_stat
      latest_file="$entry"
    fi
  done

  # Print the latest file (or empty string if no files)
  echo "$latest_file"
}

# Get the directory path (replace with your actual directory)
dir="."

# Get the latest modified file
latest_file=$(get_latest_modified_file "$dir")

if [ -z "$latest_file" ]; then
  echo "No files found in the directory."
else
  echo "Latest modified file: $latest_file"
fi
