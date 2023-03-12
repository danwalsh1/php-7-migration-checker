def rule_indirect_var_prop_methods(line):
    # Return True if the rule passes without issue. Else, return False
    if "$$" in line:
        return False

    if "->$" in line:
        return False

    if "::$" in line:
        return False

    return True
