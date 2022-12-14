import time  # for execution time calculation
from pick import pick
import domain_file_scanner
import domain_generator
import easygui

st = time.time()  # start time

title = 'Choose what to do: '
menu_options = ["generate domain list permutations", "scan domain file for whois/availability"]
option, menu_entry_index = pick(menu_options, title)

if menu_entry_index == 0:
    number_of_chars = input("Enter number of chars to generate: ")
    ascii_title = 'Which ascii characters to include when generating? '
    chosen_ascii_chars = pick(["uppercase", "lowercase", "digits"],
                              ascii_title,
                              multiselect=True,
                              min_selection_count=1)
    top_level_domain = input("Enter top level domain (ex: .com): ")
    domain_generator.generate(top_level_domain, number_of_chars, chosen_ascii_chars)
elif menu_entry_index == 1:
    mail_to = input("Enter your email (ex: artur@whoisgen.ga): ")
    out_file_name = input("Enter output filename (ex: scanned_domains_2digit_com): ")
    print("Choose file name to scan (ex: name.csv):")
    src_file_name = easygui.fileopenbox()  # show an "Open" dialog box and return the path to the selected file
    # file_name = input("Enter file name to scan (ex: name.csv): ")
    domain_file_scanner.scanner(src_file_name, out_file_name, mail_to)

# Give some stats after work finishes
et = time.time()  # end time
elapsed_time = et - st  # execution time
print('Execution time:', "%.2f" % elapsed_time, 'seconds')
