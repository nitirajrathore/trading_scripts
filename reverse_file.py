import argparse


weekdays_array = ["Monday", "Tuesday", "Wednessday", "Thursday", "Friday", "Saturday", "Sunday"]


def main(file_path, output_file, no_headers):
    with open(file_path, "r") as input_file:
        lines = input_file.readlines()
        if not no_headers:
            header = lines[0]
        output_file.write(header)
        for line in reversed(lines[1:]):
            output_file.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''reverse a file with headers'''
    )

    parser.add_argument('-if', '--file-path', help='file-path', default=None, required=True)
    parser.add_argument('-of', '--output-file', help='output-file', required=False)
    parser.add_argument('-nh', '--no-headers', help='always assumes headers, set this to say no headers',
                        action='store_true', required=False)

    args = parser.parse_args()

    if args.output_file is None:
        main(args.file_path, None, args.no_headers)
    else:
        with open(args.output_file, 'w+') as out_file:
            main(args.file_path, out_file, args.no_headers)

