import re


def rule_eval_parse_error(line):
    # Return True if the rule passes without issue. Else, return False
    if re.search("\w*(?<![A-Za-z0-9\_])eval\(", line) is not None:
        return False

    return True
