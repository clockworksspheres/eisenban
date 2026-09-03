#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path
import argparse
import textwrap
import tarfile


def create_rpm_structure(args):
    home = Path.home()
    rpmroot = home / "rpmbuild"

    # Standard RPM directory layout
    for d in ["BUILD", "RPMS", "SOURCES", "SPECS", "SRPMS"]:
        (rpmroot / d).mkdir(parents=True, exist_ok=True)

    # Temporary build root for our files
    buildroot = rpmroot / "BUILDROOT" / f"{args.package}-{args.version}-1.{args.arch}"
    if buildroot.exists():
        shutil.rmtree(buildroot)
    buildroot.mkdir(parents=True)

    # Install path inside RPM
    install_dir = buildroot / "usr" / "local" / "bin" / args.package
    install_dir.mkdir(parents=True)

    # Copy main executable
    shutil.copy(args.executable, install_dir / args.package)
    os.chmod(install_dir / args.package, 0o755)

    # Copy additional files
    for item in args.files:
        src = Path(item)
        dest = install_dir / src.name
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
            os.chmod(dest, 0o755)

    # Create tarball for SOURCES
    tar_path = rpmroot / "SOURCES" / f"{args.package}-{args.version}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(buildroot, arcname=f"{args.package}-{args.version}")

    # Create SPEC file
    spec_path = rpmroot / "SPECS" / f"{args.package}.spec"
    spec_content = f"""
Name:           {args.package}
Version:        {args.version}
Release:        1%{{?dist}}
Summary:        {args.description}

License:        Proprietary
URL:            https://example.com
Source0:        {args.package}-{args.version}.tar.gz

BuildArch:      {args.arch}

%description
{args.long_description}

%prep
%setup -q

%build

%install
mkdir -p %{{buildroot}}/usr/local/bin/{args.package}
cp -r * %{{buildroot}}/usr/local/bin/{args.package}/

%files
/usr/local/bin/{args.package}

%changelog
* Thu Jan 01 2026 {args.maintainer} - {args.version}-1
- Initial RPM release
"""
    spec_path.write_text(spec_content)

    return rpmroot, spec_path


def build_rpm(rpmroot, spec_path):
    subprocess.run(["rpmbuild", "-ba", str(spec_path)], check=True)
    print(f"RPM built successfully in: {rpmroot / 'RPMS'}")


def main():
    parser = argparse.ArgumentParser(
        description="Create an RPM package from a PyInstaller executable and additional files",
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
                  --arch x86_64
        """)
    )

    parser.add_argument("--package", required=True, help="Package name")
    parser.add_argument("--version", required=True, help="Package version")
    parser.add_argument("--executable", required=True, help="Path to PyInstaller output binary")
    parser.add_argument("--files", nargs="*", default=[], help="Additional files or directories to include")
    parser.add_argument("--maintainer", default="Unknown <unknown@example.com>", help="Maintainer info")
    parser.add_argument("--description", default="PyInstaller packaged application", help="Short description")
    parser.add_argument("--long-description", default="A compiled Python application packaged as an RPM.",
                        help="Long description")
    parser.add_argument("--arch", default="x86_64", help="Architecture (x86_64, aarch64, noarch, etc.)")

    args = parser.parse_args()

    rpmroot, spec_path = create_rpm_structure(args)
    build_rpm(rpmroot, spec_path)


if __name__ == "__main__":
    main()

