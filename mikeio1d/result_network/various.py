from __future__ import annotations
import re
from typing import List, Tuple, Dict
from html import escape


def make_proper_variable_name(string, extra_string_before_digit="_"):
    """
    Makes a more proper variable name.

    It is assumed that the input string never is or after manipulations
    becomes an '_' or an empty string.
    """
    # Replace all non alpha numeric characters by an underscore.
    string = re.sub(r"[^a-zA-Z0-9]", "_", string)
    # Replace more than two underscores with a single underscore.
    string = re.sub(r"_{2,}", "_", string)
    # Add an extra string is the string starts with a number.
    string = extra_string_before_digit + string if string and string[0].isdigit() else string
    # Remove a starting underscore
    string = string[1:] if string[0] == "_" else string
    # Remove a trailing underscore
    string = string[:-1] if string[-1] == "_" else string
    return string


def build_html_repr_from_sections(header: str, sections: List[Tuple[str, List | Dict]]):
    """
    Builds an html representation from a list of sections.

    Parameters
    ----------
    header : str
        Header string (e.g. <ResultNode>).
    sections : list of tuples
        List of tuples with section name and section content.
        The section content can be either a list of values or
        a dictionary of key value pairs.
    """
    repr = escape(header)
    repr += _build_html_repr_section_style()  # TODO: A better way to inject css?
    for section_name, section_content in sections:
        if isinstance(section_content, list):
            section = _build_html_repr_section_from_list(section_name, section_content)
        elif isinstance(section_content, dict):
            section = _build_html_repr_section_from_dict(section_name, section_content)
        else:
            raise ValueError(f"Unknown section content type: {section_content}")
        repr += section
    return repr


def _build_html_repr_section_style():
    """
    Builds a style string for html representation."""
    style = """
    <style>
        ul {
            margin: 0px;
            padding: 0px;
            padding-left: 2em;
        }
    </style>
    """
    return style


def _build_html_repr_section_from_dict(name, keyvalues):
    """
    Builds a section from a dictionary."""
    section = "<details>"
    section += f"<summary>{name}</summary>"
    section += "<ul>"
    for key, value in keyvalues.items():
        section += f"<li>{key}: {value}</li>"
    section += "</ul>"
    section += "</details>"
    return section


def _build_html_repr_section_from_list(name, values):
    """
    Builds a section from a list."""
    section = "<details>"
    section += f"<summary>{name}</summary>"
    section += "<ul>"
    for value in values:
        section += f"<li>{value}</li>"
    section += "</ul>"
    section += "</details>"
    return section
