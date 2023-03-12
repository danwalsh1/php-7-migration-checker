def rule_exception_handler(line):
    # Return True if the rule passes without issue. Else, return False
    if "set_exception_handler" in line:
        return False

    return True
