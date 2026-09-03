#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys

def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)

def prepare_payload(files):
    payload_root = "payload/usr/local/bin"
    os.makedirs(payload_root, exist_ok=True)

    for f in files:
        if not os.path.isfile(f):
            raise FileNotFoundError(f"File not found: {f}")
        shutil.copy(f, payload_root)

    return "payload"

def build_pkg(payload_dir, identifier, version, output):
    component_pkg = f"{output}.component.pkg"

    run([
        "pkgbuild",
        "--root", payload_dir,
        "--identifier", identifier,
        "--version", version,
        component_pkg
    ])

    run([
        "productbuild",
        "--package", component_pkg,
        f"{output}.pkg"
    ])

    print(f"\nCreated installer: {output}.pkg")

def main():
    parser = argparse.ArgumentParser(
        description="Create a macOS .pkg installer for 1–3 files installed into /usr/local/bin.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  Install one file:
    %(prog)s --identifier com.example.tool --version 1.0 tool

  Install two files:
    %(prog)s --identifier com.example.tools --version 2.0 tool1 tool2

  Install three files with custom output name:
    %(prog)s --identifier com.example.pkg --version 1.2 --output myinstaller file1 file2 file3
"""
    )

    parser.add_argument("files", nargs="+", help="1–3 files to install into /usr/local/bin")
    parser.add_argument("--identifier", required=True, help="Package identifier (e.g., com.example.mytool)")
    parser.add_argument("--version", default="1.0.0", help="Package version")
    parser.add_argument("--output", default="installer", help="Base name for output .pkg file")

    args = parser.parse_args()

    if not (1 <= len(args.files) <= 5):
        print("Error: You must specify between 1 and 3 files.")
        sys.exit(1)

    payload = prepare_payload(args.files)
    build_pkg(payload, args.identifier, args.version, args.output)

if __name__ == "__main__":
    main()


