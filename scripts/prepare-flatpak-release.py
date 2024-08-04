
import os
import sys

import hashlib
import argparse

FLATID = "io.github.zen_browser.zen"

def get_sha256sum(filename):  
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256.update(byte_block)
    return sha256.hexdigest()

def build_template(template, linux_sha256, flatpak_sha256, version):
    return template.format(linux_sha256=linux_sha256, 
                          flatpak_sha256=flatpak_sha256,
                          version=version)

def get_template(template_root):
    with open(f"{template_root}/{FLATID}.yml.template", "r") as f:
        return f.read()
    print(f"Template {template_root}/flatpak.yml not found")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Prepare flatpak release')
    parser.add_argument('--version', help='Version of the release', required=True)
    parser.add_argument('--linux-archive', help='Linux archive', required=True)
    parser.add_argument('--flatpak-archive', help='Flatpak archive', required=True)
    parser.add_argument('--output', help='Output file', default=f"{FLATID}.yml")
    parser.add_argument('--template-root', help='Template root', default="flatpak")
    args = parser.parse_args()

    version = args.version
    linux_archive = args.linux_archive
    flatpak_archive = args.flatpak_archive
    output = args.output
    template_root = args.template_root

    linux_sha256 = get_sha256sum(linux_archive)
    flatpak_sha256 = get_sha256sum(flatpak_archive)

    template = build_template(get_template(template_root), linux_sha256, flatpak_sha256, version)

    with open(output, "w") as f:
        f.write(template)

if __name__ == "__main__":
    main()
