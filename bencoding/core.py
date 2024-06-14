from typing import Any, NamedTuple


type BencodedType = str | int | list[BencodedType] | dict[str, BencodedType]


class _ParsedVal[T: BencodedType](NamedTuple):
    val: T
    idx: int


def _parse_str(stream: bytes, idx: int) -> _ParsedVal[str]:
    built_str_len: list[str] = []
    while stream[idx] != ord(":"):
        built_str_len.append(chr(stream[idx]))
        idx += 1

    str_len = int("".join(built_str_len))
    built_str = ""
    idx += 1
    for _ in range(str_len):
        built_str += chr(stream[idx])
        idx += 1

    return _ParsedVal(built_str, idx)


def _parse_int(stream: bytes, idx: int) -> _ParsedVal[int]:
    built_val: list[str] = []
    idx += 1
    while stream[idx] != ord("e"):
        built_val.append(chr(stream[idx]))
        idx += 1
    val = "".join(built_val)
    return _ParsedVal(int(val), idx + 1)


def _parse_list(stream: bytes, idx: int) -> _ParsedVal[list[BencodedType]]:
    built_list: list[BencodedType] = []
    idx += 1
    while stream[idx] != ord("e"):
        val, idx = _parse(stream, idx)
        built_list.append(val)
    return _ParsedVal(built_list, idx + 1)


def _parse_dict(stream: bytes, idx: int) -> _ParsedVal[dict[str, BencodedType]]:
    curr_dict: dict[str, BencodedType] = {}
    idx += 1  # Increment to skip 'd'
    while stream[idx] != ord("e"):
        key, idx = _parse_str(stream, idx)
        value, idx = _parse(stream, idx)
        curr_dict[key] = value
    return _ParsedVal(curr_dict, idx + 1)


def _parse(stream: bytes, idx: int = 0) -> _ParsedVal[Any]:
    byte = stream[idx]
    if byte == ord("i"):
        return _parse_int(stream, idx)
    elif byte == ord("d"):
        return _parse_dict(stream, idx)
    elif byte == ord("l"):
        return _parse_list(stream, idx)
    else:
        return _parse_str(stream, idx)


def decode(stream: bytes) -> BencodedType:
    if not stream:
        return ""
    value, _ = _parse(stream)
    return value
