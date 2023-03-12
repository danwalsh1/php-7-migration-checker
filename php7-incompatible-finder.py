import sys

sys.path.append('F:/_PY_Projects/PHP-migration-tools/helpers')

import os
import time
from pathlib import Path

# Import Rules
from rulesExceptionHandler import rule_exception_handler
from rulesEvalParseError import rule_eval_parse_error
from rulesEStrict import rule_e_strict
from rulesIndirectVarPropMethods import rule_indirect_var_prop_methods
from rulesList import rule_list
from rulesList import rule_empty_list

# ================================================================================
# =================================== Settings ===================================
# ================================================================================

# Path to the root directory that holds all files and directories to be checked
root_check_path = "F:/_PY_Projects/PHP-migration-tools/test"

# Path to the directory that should hold the output log files
root_log_path = "F:/_PY_Projects/PHP-migration-tools/logs"

# List of directories not to check (path should start from the root)
# Use back-slashes (\) not forward-slashes
root_directory_blacklist = [
    ".idea"
]

# Log file names (a timestamp prefix will be added)
warning_log_file = "warnings.log"
info_log_file = "info.log"

# Build log files prefix
timestr = time.strftime("%d%m%Y-%H%M%S")
log_directory = "php7-incompatible-finder-" + timestr


# ================================================================================
# ==================================== Rules =====================================
# ================================================================================

def log_warning(file_path, line_number, log_line, failed_rules):
    warning_log_file_open.write(file_path + " [" + str(line_number) + "]: " + log_line)
    for failed_rule in failed_rules:
        warning_log_file_open.write(failed_rule + "\n")
    warning_log_file_open.write("\n")

def log_info(message):
    info_log_file_open.write(message + "\n")

def run_rules(file_path, line_number, rules_line):
    failed_rules = []

    if not rule_exception_handler(rules_line):
        print("Line failed [rule_exception_handler]: " + rules_line.strip())
        failed_rules.append("set_exception_handler() is no longer guaranteed to receive Exception objects")

    if not rule_eval_parse_error(rules_line):
        print("Line failed [rule_eval_parse_error]: " + rules_line.strip())
        failed_rules.append("Parser errors now throw a ParseError. Error handling for eval() should now include a catch block that can handle this error")

    if not rule_e_strict(rules_line):
        print("Line failed [rule_e_strict]: " + rules_line.strip())
        failed_rules.append("E_STRICT notices severity changes")

    if not rule_indirect_var_prop_methods(rules_line):
        print("Line failed [rule_indirect_var_prop_methods]: " + rules_line.strip())
        failed_rules.append("Code that uses right-to-left evaluation must be rewritten to explicitly use that evaluation order with curly braces")

    if not rule_list(rules_line):
        print("Line failed [rule_list]: " + rules_line.strip())
        failed_rules.append("list() no longer assigns variables in reverse order")

    if not rule_empty_list(rules_line):
        print("Line failed [rule_empty_list]: " + rules_line.strip())
        failed_rules.append("Empty list() assignments have been removed")

    # Has the line failed any rules?
    if len(failed_rules) > 0:
        log_warning(file_path, line_number, rules_line, failed_rules)


# ================================================================================
# ==================================== Checks ====================================
# ================================================================================

# Disclaimer for non-checked points
log_info("Please note the following rules haven't been checked for:")
log_info("Internal constructors now always throw exceptions on failure rather than sometimes returning null or an unusable object")
log_info("list() can no longer unpack string variables")
log_info("Array ordering when elements are automatically created during 'by reference' assignments has changed")
log_info("Parentheses around function arguments no longer affect behaviour")
log_info("")
log_info("")

# Create log directory
current_log_directory = os.path.join(root_log_path, log_directory)
os.mkdir(current_log_directory)

# Define absolute log paths
warning_log_file = os.path.join(current_log_directory, warning_log_file)
info_log_file = os.path.join(current_log_directory, info_log_file)

# Open logs
warning_log_file_open = open(warning_log_file, "a+")
info_log_file_open = open(info_log_file, "a+")

# List all root directories
for root_directory in os.walk(root_check_path):
    print("Root Directories:")
    print(root_directory[1])
    print("")
    for current_directory_name in root_directory[1]:
        blacklisted = False

        for blacklist_item in root_directory_blacklist:
            if root_check_path + "\\" + current_directory_name == root_check_path + "\\" + blacklist_item:
                blacklisted = True
                break

        if blacklisted == True:
            print("Skipping blacklisted directory: " + current_directory_name)
            log_info("Skipping blacklisted directory: " + current_directory_name)
            continue

        print("Searching: " + current_directory_name)
        for php_file_path in Path(root_check_path).rglob("*.php"):
            if not os.path.isdir(php_file_path):
                # Check the file
                print("PHP file found: " + php_file_path.name)
                log_info("PHP file found: " + php_file_path.name)

                # Go through the file line-by-line
                current_file_path = php_file_path.absolute()
                line_counter = 1
                with open(current_file_path) as infile:
                    for line in infile:
                        run_rules(str(current_file_path), line_counter, line)
                        line_counter += 1
            else:
                print("Skipping directory with PHP name: " + php_file_path.name)
                log_info("Skipping directory with PHP name: " + php_file_path.name)

    break

print("")
print("")

print("All checks completed!")

print("")
print("")

print("Please note the following rules haven't been checked for:")
print("Internal constructors now always throw exceptions on failure rather than sometimes returning null or an unusable object")
print("list() can no longer unpack string variables")
print("Array ordering when elements are automatically created during 'by reference' assignments has changed")
print("Parentheses around function arguments no longer affect behaviour")

# Close logs
warning_log_file_open.close()
info_log_file_open.close()
