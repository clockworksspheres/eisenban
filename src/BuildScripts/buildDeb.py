#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path
import argparse
import textwrap


def copy_item(src, dest_dir):
    """Copy a file or directory into the package."""
    src_path = Path(src)
    dest_path = Path(dest_dir) / src_path.name

    if src_path.is_dir():
        shutil.copytree(src_path, dest_path)
    else:
        shutil.copy2(src_path, dest_path)

    # Make files executable if they look like binaries
    if dest_path.is_file():
        os.chmod(dest_path, 0o755)


def create_deb_structure(args):
    root = Path(f"{args.package}_{args.version}")
    debian_dir = root / "DEBIAN"
    bin_dir = root / "usr" / "local" / "bin" / args.package

    # Clean previous build
    if root.exists():
        shutil.rmtree(root)

    # Create directories
    debian_dir.mkdir(parents=True)
    bin_dir.mkdir(parents=True)

    # Write control file
    control_content = f"""Package: {args.package}
Version: {args.version}
Section: utils
Priority: optional
Architecture: {args.arch}
Maintainer: {args.maintainer}
Description: {args.description}
 {args.long_description}
"""
    (debian_dir / "control").write_text(control_content)

    # Copy main PyInstaller executable
    shutil.copy(args.executable, bin_dir / args.package)
    os.chmod(bin_dir / args.package, 0o755)

    # Copy additional files
    for item in args.files:
        copy_item(item, bin_dir)

    return root


def build_deb(root):
    output_file = f"{root}.deb"
    subprocess.run(["dpkg-deb", "--build", str(root)], check=True)
    print(f"Created {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a .deb package from a PyInstaller executable and additional files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Example:
              %(prog)s \\
                  --package myapp \\
                  --version 1.0 \\
                  --executable dist/myapp \\
                  --files config.yaml assets/ helper.sh \\
                  --maintainer "John Doe <john@example.com>" \\
                  --description "My packaged app" \\
                  --long-description "This is a PyInstaller-built application with extra files." \\
                  --arch amd64
        """)
    )

    parser.add_argument("--package", required=True, help="Package name")
    parser.add_argument("--version", required=True, help="Package version")
    parser.add_argument("--executable", required=True, help="Path to PyInstaller output binary")
    parser.add_argument("--files", nargs="*", default=[], help="Additional files or directories to include")
    parser.add_argument("--maintainer", default="Unknown <unknown@example.com>", help="Maintainer info")
    parser.add_argument("--description", default="PyInstaller packaged application", help="Short description")
    parser.add_argument("--long-description", default="A compiled Python application packaged as a .deb file.",
                        help="Long description (second paragraph)")
    parser.add_argument("--arch", default="amd64", help="Architecture (amd64, arm64, all, etc.)")

    args = parser.parse_args()

    root = create_deb_structure(args)
    build_deb(root)


if __name__ == "__main__":
    main()

