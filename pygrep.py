# The program is a Python implementation of the grep command line tool. 
# It uses the argparse module to parse the command line arguments and the re module to perform the regular expression search. 
# The program supports most of the grep command options such as case-insensitive search, count-only mode, excluding and including files based on patterns, recursive search, context printing, inverting the match, matching whole words only, color highlighting, printing line numbers, and printing the file name for each match. 
# The program also handles errors and exceptions gracefully.


import re # Here, we are importing the regular expression module to use the regular expression functions in the program.
import argparse # Here, we are importing the argparse module to use the command line arguments so that this program can work like a Grep commmand line.
import glob # Here, we are importing the glob module to use the wildcard expansion so that it allows users to select filenames based on patterns of characters in the program.
import fnmatch # Here, we are importing the fnmatch module to use the filename pattern matching in the program.
import os # Here, we are importing the os module to use the operating system dependent functionality in the program.
from collections import deque # Here, we are importing the deque class from the collections module to use the double-ended queue and keep track of the previous.


# 10th line defines the main function grep2_O with several parameters. Each parameter corresponds to a feature of the grep command Line.
def grep2_O(pattern, files, ignore_case, count_only, exclude_pattern, include_pattern, recursive, context, invert_match, word_match, color_match, line_number, file_name):
    try:
        if word_match:                          # line 12 and 13 checks if the word_match option is enabled and it modifies the pattern to match whole words only.
            pattern = r'\b' + pattern + r'\b' 
        compiled_pattern = re.compile(pattern, re.IGNORECASE if ignore_case else 0) # This line compiles the regular expression pattern. If the ignore_case option is enabled, it uses the re.IGNORECASE flag to make the search case-insensitive.
        count = 0 # Here, it is initializing the count to 0.
        for file_name in files: # Here, it is iterating through the files.
            if exclude_pattern and fnmatch.fnmatch(file_name, exclude_pattern): # If the exclude_pattern option is enabled and the filename matches the exclude pattern, it skips the current file and continues with the next one.
                continue
            if include_pattern and not fnmatch.fnmatch(file_name, include_pattern): # If the include_pattern option is enabled and the filename does not match the include pattern, it skips the current file and continues with the next one.
                continue


            # Lines 24, 25, 26 and 27 checks if the recursive option is enabled and the current file is actually a directory, it recursively calls the grep function on each file in the directory and its subdirectories.
            if os.path.isdir(file_name) and recursive: 
                for root, dirs, files in os.walk(file_name):   # it is iterating through the files in the directory.
                    for file in files:
                        grep2_O(pattern, [os.path.join(root, file)], ignore_case, count_only, exclude_pattern, include_pattern, False, context, invert_match, word_match, color_match, line_number, file_name) # it is calling the grep function with the pattern, file, ignore_case, count_only, exclude_pattern, include_pattern, False, context, invert_match, word_match, color_match, line_number, and file_name.
            elif os.path.isfile(file_name):
                try:
                    # lines 31 to 34 checks if the current file is a regular file and it opens the file and reads it line by line. For each line, it checks if the line matches the pattern.
                    with open(file_name, 'r') as f:
                        prev_lines = deque(maxlen=context)  
                        for line_no, line in enumerate(f, start=1):
                            match = compiled_pattern.search(line) # It is searching for the pattern in the line.

                           #lines 37 to 41 checks if the invert_match option is enabled and it inverts the match result. If the line matches the pattern (or does not match, if invert_match is enabled), it increments the count and, unless the count_only option is enabled, prints the line along with the line number and filename, if those options are enabled.
                            if invert_match == (not match): # It is checking if the invert_match is True and the match is False.
                                count += 1
                                if not count_only: # It is checking if the count_only is False.
                                    for ln, pline in prev_lines: 
                                        print(f'{file_name if file_name else ""}:{ln if line_number else ""}:{pline.rstrip()}') # It is printing the file_name, line_number, and the previous line.
                                    
                                    #lines 43 to 47 checks if the color_match option is enabled and it highlights the matching part of the line in red. 
                                    if color_match and match: 
                                        start = match.start() 
                                        end = match.end() 
                                        line = line[:start] + '\033[91m' + line[start:end] + '\033[0m' + line[end:] # It is adding the color to the matching line.
                                    print(f'{file_name if file_name else ""}:{line_no if line_number else ""}:{line.rstrip()}') # It is printing the file_name, line_number, and the line.
                                    
                                    #lines 50 to 56 checks if the context option is enabled and it also prints the specified number of lines before and after the matching line.
                                    for _ in range(context): 
                                        line = next(f, None) # It is getting the next line from the file.
                                        if line is None: 
                                            break
                                        line_no += 1 
                                        print(f'{file_name if file_name else ""}:{line_no if line_number else ""}:{line.rstrip()}') # It is printing the file_name, line_number, and the line.
                            prev_lines.append((line_no, line)) 
                except IOError as e:
                    print(f'Error opening file {file_name}: {e}') # It prints a error message if there is a error in opening a file.

        # lines 62 and 63 checks if the count_only option is enabled and it prints the total number of matches.
        if count_only:
            print(f'Match count: {count}') #
    except Exception as e:
        print(f'An error occurred: {e}')

def main():
    try:
        parser = argparse.ArgumentParser(description='Python grep command.') # Here, it is creating a parser object with the description.
        parser.add_argument('pattern', type=str, help='Pattern to search for') # Here, it is adding the pattern argument to the parser.
        parser.add_argument('files', type=str, nargs='+', help='Files to search') # Here, it is adding the files argument to the parser.
        parser.add_argument('-i', '--ignore-case', action='store_true', help='Ignore case') # Here, it is adding the ignore-case argument to the parser.
        parser.add_argument('-c', '--count', action='store_true', help='Count matches only') # Here, it is adding the count argument to the parser.
        parser.add_argument('-excl', '--exclude', type=str, help='Exclude files matching this pattern')# Here, it is adding the exclude argument to the parser.
        parser.add_argument('-incl', '--include', type=str, help='Include files matching this pattern')# Here, it is adding the include argument to the parser.
        parser.add_argument('-r', '--recursive', action='store_true', help='Recursive search')# Here, it is adding the recursive argument to the parser.
        parser.add_argument('-con', '--context', type=int, default=0, help='Print num lines of leading and trailing context')# Here, it is adding the context argument to the parser.
        parser.add_argument('-v', '--invert-match', action='store_true', help='Invert match')# Here, it is adding the invert-match argument to the parser.
        parser.add_argument('-w', '--word-match', action='store_true', help='Match whole words only')# Here, it is adding the word-match argument to the parser.
        parser.add_argument('-col','--color', action='store_true', help='Color match')# Here, it is adding the color argument to the parser.
        parser.add_argument('-n', '--line-number', action='store_true', help='Print line number with output lines')# Here, it is adding the line-number argument to the parser.
        parser.add_argument('-H', '--with-filename', action='store_true', help='Print the file name for each match')# Here, it is adding the with-filename argument to the parser.

        args = parser.parse_args()# Here, it is parsing the arguments.

        # Expand wildcards
        files = [file for wildcard in args.files for file in glob.glob(wildcard)] # Here, it is expanding the wildcards in the files.

        grep2_O(args.pattern, files, args.ignore_case, args.count, args.exclude, args.include, args.recursive, args.context, args.invert_match, args.word_match, args.color, args.line_number, args.with_filename)
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__": # Here, it is checking if the __name__ is equal to __main__.
    main() # and here the main function is called.


'''To run the program, you can save it to a file (e.g., pygrep.py) and run it from the command line with the desired options and arguments.
   That is use the cd command to navigate to the directory where you saved the python script. For example, if you saved it in a directory called pygrep on your desktop, you would type cd Desktop in the terminal.
   Type python grep.py followed by the arguments you want to use.
   For example, to search for the word "python" in all .txt files in the current directory, you would type "python grep.py python *.txt."

   Some more examples are: 
   1. python grep.py -i 'hello' *.txt( it will search for the word "hello" in all .txt files in the current directory and its subdirectories. It will ignore the case of the word "hello".)
   2. python grep.py -c 'hello' *.txt( it will search for the word "hello" in all .txt files in the current directory and print the total number of matches.)
   3. python grep.py -e '*test*' 'hello' *.txt (it will search for the word "hello" in all .txt files in the current directory and its subdirectories. It will exclude files with "test" in their names.)
   4. python grep.py -excl '*.txt' -incl '*.txt' -r 'hello' *.txt (it will search for the word "hello" in all .txt files in the current directory and its subdirectories.)
   5. python grep.py -con 2 'hello' *.txt (it will search for the word "hello" in all .txt files in the current directory and print 2 lines of context before and after each match.)
   6. python grep.py -v 'hello' *.txt (it will search for lines that do not contain the word "hello" in all .txt files in the current directory.)
   7. python grep.py -w 'hello' *.txt (it will search for whole words only in all .txt files in the current directory.)
   8. python grep.py -col 'hello' *.txt (it will search for the word "hello" in all .txt files in the current directory and highlight the matching part of the line in red.)
   9. python grep.py -n 'hello' *.txt (it will search for the word "hello" in all .txt files in the current directory and print the line number with each match.)
   10. python grep.py -H 'hello' *.txt (it will search for the word "hello" in all .txt files in the current directory and print the file name for each match.)
   11. python grep.py -i -c -excl '*.txt' -incl '*.txt' -r -con 2 -v -w -col -n -H 'hello' *.txt 
   (it will search for the word "hello" in all .txt files in the current directory and its subdirectories. It will exclude files with "test" in their names. It will print 2 lines of context before and after each match. It will search for lines that do not contain the word "hello" and match whole words only. It will highlight the matching part of the line in red and print the line number and the file name for each match.)
   and so on.

   The above program was done with the guidance of google and other resources.
   By doing this program, I have learned how to use the regular expression module, primarily argparse module, glob module, fnmatch module, os module, and collections module in Python.
   Thank you, for providing me this opportunity to learn new things and improve my skills. :)
   '''