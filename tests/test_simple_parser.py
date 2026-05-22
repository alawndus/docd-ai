from src.parsers.simple_parser import parse_key_values


def test_parse_key_values_basic():
    text = """
Title: Example Document
Author: Alice

Summary: This is a test.
"""
    parsed = parse_key_values(text)
    assert parsed["Title"] == "Example Document"
    assert parsed["Author"] == "Alice"
    assert parsed["Summary"] == "This is a test."


def test_parse_ignores_invalid_lines():
    text = """
NoColonHere
Key: Value
Some other line
Another:  123
"""
    parsed = parse_key_values(text)
    assert parsed == {"Key": "Value", "Another": "123"}
