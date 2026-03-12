import argparse
from functions.get_files_info import get_files_info

def test_get_files_info_args():
    parser = argparse.ArgumentParser(description="File Info")
    parser.add_argument("working_directory", type=str, help="Working directory")
    parser.add_argument("target_directory", type=str, help="Target Directory")
    args = parser.parse_args()

    print(get_files_info(args.working_directory, args.target_directory))

def test_get_files_info():
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    test_get_files_info()