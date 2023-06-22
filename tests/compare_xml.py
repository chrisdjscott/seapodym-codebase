#!/usr/bin/env python3

"""
Compares values between two seapodym xml files where the "use=true" attribute is set.

"""
import sys
import logging
import argparse
import xml.etree.ElementTree as ET

import numpy as np


def read_value(elem, value_label):
    if value_label in elem.attrib:
        value = elem.attrib[value_label]
    elif "value" in elem.attrib:
        value = elem.attrib["value"]
    else:
        KeyError(f"No attrib named '{value_label}' or 'value' for '{elem.tag}': {elem.attrib}")

    return value


def get_used_value(elem, value_label):
    logging.debug(f"Checking for value for '{elem.tag}'")
    # if has a child named variable, check whether that has use=true set, if so the value elem.attrib[ID] is used
    # otherwise check whether it has a use=true set itself (unless called variable(s), skip those)
    value = None
    if elem.tag == "variables" or elem.tag == "variable":
        logging.debug("skipping tag: '{elem.tag}'")

    elif "use" in elem.attrib and elem.attrib["use"] == "true":
        value = read_value(elem, value_label)
        logging.debug(f"Loaded value (use in attrib): {value} ({elem.tag})")

    else:
        children = elem.findall("variable")
        if len(children) > 0:
            if len(children) == 1:
                if "use" in children[0].attrib and children[0].attrib["use"] == "true":
                    value = read_value(elem, value_label)
                    logging.debug(f"Loaded value (use in child): {value} ({elem.tag})")
            else:
                raise ValueError(f"Multiple 'variable' children for '{elem.tag}'")

    return value


def process_root(r, r_label, value_label, results):
    logging.debug(f"Processing root: '{r_label}' (size = {len(r)})")

    for child in r:
        label = f"{r_label}::{child.tag}"
        value = get_used_value(child, value_label)
        if value is not None:
            if label in results:
                raise KeyError(f"label {label} already exists in results")
            else:
                results[label] = value

        # process the child as its own root
        process_root(child, label, value_label, results)


def load_used_values(filename, value_label):
    tree = ET.parse(filename)
    root = tree.getroot()
    logging.info(f"Loading '{filename}': {tree}, {root}, {root.attrib}")

    used_values = {}
    process_root(root, root.tag, value_label, used_values)
    logging.info(f"Loaded {len(used_values)} used values from '{filename}'")

    return used_values


def compare_two_files(file1, file2, value_label, atol, rtol):
    used_values_1 = load_used_values(file1, value_label)
    used_values_2 = load_used_values(file2, value_label)

    match = True
    logging.info("Comparing used values")

    # check same number of values
    if len(used_values_1) != len(used_values_2):
        match = False
        logging.warning(f"Number of used values do not match: {file1} ({len(used_values_1)} vs {file2} (len(used_values_2)))")

    # check labels match
    uv1_keys = set(used_values_1.keys())
    uv2_keys = set(used_values_2.keys())
    shared_keys = uv1_keys.intersection(uv2_keys)
    if len(shared_keys) != len(uv1_keys):
        match = False
        logging.warning("Keys do not match")
    logging.debug(f"Shared keys: {shared_keys}")

    # check values
    for key in used_values_1:
        v1 = used_values_1[key]
        if key not in used_values_2:
            continue
        v2 = used_values_2[key]

        # TODO: try casting to int first and fall back to float if that fails?
        v1 = float(v1)
        v2 = float(v2)
        if not np.isclose(v1, v2, atol=atol, rtol=rtol):
            logging.warning(f"Values do not match for '{key}': {v1} vs {v2}")
            match = False

    # report
    if match:
        logging.info("The files match")
    else:
        logging.error("The files do not match")
        sys.exit(1)


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Compare used=true values in two seapodym xml files")

    parser.add_argument("file1", help="First file to compare")
    parser.add_argument("file2", help="Second file to compare")
    parser.add_argument("-l", "--label", default="skj", help="Value attribute in XML file (default=%(default)s)")
    parser.add_argument("-r", "--rtol", type=float, default=1e-5, help="Relative tolerance for comparison, passed to `numpy.isclose` (default=%(default)s)")
    parser.add_argument("-a", "--atol", type=float, default=1e-8, help="Absolute tolerance for comparison, passed to `numpy.isclose` (default=%(default)s)")
    parser.add_argument("-v", "--verbosity", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO", help="Level of verbosity (default=%(default)s)")

    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        level=args.verbosity,
        format=f'%(asctime)s|%(name)s|%(levelname)s|%(message)s',
    )

    # run the comparison
    compare_two_files(args.file1, args.file2, args.label, args.atol, args.rtol)


if __name__ == "__main__":
    main()
