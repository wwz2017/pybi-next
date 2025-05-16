import re


def extract_special_tags(sql):
    pattern = r"@_(\d+)_@"
    matches = re.findall(pattern, sql)

    result = [f"'@_{match}_@'" for match in matches]

    return result
