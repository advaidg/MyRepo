import os
import subprocess

def compare_folders(folder1, folder2):
    for subdir1, dirs1, files1 in os.walk(folder1):
        corresponding_subdir2 = get_corresponding_subdir(subdir1, folder2)
        if corresponding_subdir2:
            for file1 in files1:
                if file1.endswith('.txt'):
                    corresponding_file2 = os.path.join(corresponding_subdir2, file1)
                    if os.path.exists(corresponding_file2):
                        call_java_application(os.path.join(subdir1, file1), corresponding_file2)

def get_corresponding_subdir(subdir1, folder2):
    folder1_name = os.path.basename(subdir1)
    for subdir2, dirs2, files2 in os.walk(folder2):
        if folder1_name in subdir2:
            return subdir2
    return None

def call_java_application(file1, file2):
    # Replace 'java_application.jar' with the actual name of your Java application JAR file
    subprocess.call(['java', '-jar', 'java_application.jar', file1, file2])

if __name__ == "__main__":
    folder1 = input("Enter the path to folder 1: ")
    folder2 = input("Enter the path to folder 2: ")
    compare_folders(folder1, folder2)
