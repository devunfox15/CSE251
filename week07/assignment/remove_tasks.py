import os
import glob

def delete_task_files(directory: str):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Directory: {directory} does not exist.")
        return

    # Create the file pattern
    file_pattern = os.path.join(directory, '*.task')

    # Find all files that match the pattern
    task_files = glob.glob(file_pattern)

    # Check if there are no .task files
    if not task_files:
        print("No .task files to delete.")
        return

    # Delete each file
    for filename in task_files:
        try:
            os.remove(filename)
            print(f"Deleted {filename}")
        except Exception as e:
            print(f"Could not delete {filename} due to {e}")

    print("Deletion process completed.")

# Usage
if __name__ == "__main__":
    # Set the directory you want to clean up
    current_directory = '.'  # This means the current directory
    delete_task_files(current_directory)
