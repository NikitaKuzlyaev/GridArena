def make_string_clear(
        string: str,
) -> str:
    return ''.join(string.lower().strip().split())
