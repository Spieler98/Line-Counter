import string
import argparse

#TODO 
# Process replace with regex, maybe faster

class Ansi:
    def __init__(self) -> None:
        self.end = "\33[0m"
        self.bold = "\33[1m"
        self.underline = "\33[4m"
        self.gray = "\33[90m"

def main():
    # Setup argparse and variable
    args = parse_arguments()
    is_verbose = args.verbose
    file_path = args.file
    
    if raw_data:= get_file(file_path):
        if line_dict:= process_data(raw_data, is_verbose):
            print_data(line_dict, is_verbose)

def print_data(line_dict, is_verbose):
    ansi = Ansi()
    separator = " | "
    line = "-"
    length_row_one = max(len(key) for key in line_dict)
    length_row_two = max(len(f"{value:,}") for value in line_dict.values())
    max_length = length_row_one + len(separator) + length_row_two
    print("\nLine Counter")
    print(line*(max_length), sep="")
    for key, i in zip(line_dict, range(len(line_dict))):
        if i == 2 and not is_verbose:
            break
        key_space = " " * (length_row_one - len(key))
        key_str = key + key_space
        list_value = f"{line_dict[f"{key}"]:,}"
        if i % 2 == 0:
            print(key_str.capitalize() + separator + list_value)
        else:
            print(ansi.gray + key_str.capitalize() + separator + list_value + ansi.end)
    print()


def process_data(data, verbose):
    line_dict = {
        "lines": 0,
        "columns": 0,
        "lower-case": 0,
        "upper-case": 0,
        "digits": 0,
        "symbols": 0,
        "whitespace": 0,
        "others": 0,
    }

    for line in data:
        line_dict["lines"] += 1
        for char in line:
            line_dict["columns"] += 1
            if char in string.ascii_lowercase:
                line_dict["lower-case"] += 1
            elif char in string.ascii_uppercase:
                line_dict["upper-case"] += 1
            elif char in string.digits:
                line_dict["digits"] += 1
            elif char in string.punctuation:
                line_dict["symbols"] += 1
            elif char in string.whitespace:
                line_dict["whitespace"] += 1
            else:
                line_dict["others"] += 1

    return line_dict

def get_file(file_path):
    try:
        data = []
        with open(file_path, "r") as f:
            for line in f:
                data.append(line)
        return data
    except FileNotFoundError:
        print_alert("File not found", file_path)
    except PermissionError:
        print_alert("File permission denied", file_path)
    except Exception as e:
        print(e)

def print_alert(msg="", detail="", warn="Error"):
    print(f"[{warn}] {msg}: '{detail}'")

def parse_arguments():
    parser = argparse.ArgumentParser(
                    prog='lines.py',
                    description='Very simple line counter that gives you details about a file. Lines, columns, lowercase, uppercase, digits, symbols, whitespace and other. If you have big file or low-end pc expect low performance.',
                    epilog='-> lines.py example.txt')
    # Add arguments
    parser.add_argument("file", type=str, help="File or full path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    return parser.parse_args()


if __name__ == "__main__":
    main()