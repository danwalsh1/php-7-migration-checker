import re

def rule_list(line):
    # Return True if the rule passes without issue. Else, return False
    if re.search("list\(\s*(?:\$[a-zA-Z0-9_]+\s*,\s*)*\$?[a-zA-Z0-9_]*\s*\[\s*]\s*(?:\s*,\s*(?:\$[a-zA-Z0-9_]*\s*\[\s*]\s*)?)*\s*\)", line) is not None:
        return False

    return True

def rule_empty_list(line):
    # Return True if the rule passes without issue. Else, return False
    if re.search("list\(\s*(?:,?\s*)*\)", line) is not None:
        return False

    return True