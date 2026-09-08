
Get ride of the com.apple.quarantine extended attribute:

# macos xattr -dr

macos xattr -dr

The **`-dr`** flags in the macOS `xattr` command are used to **delete** (`-d`) a specific extended attribute from a file and all its contents recursively (`-r`).

This command is most commonly used to remove the **`com.apple.quarantine`** attribute, which prevents downloaded applications from opening due to security warnings.

```bash
sudo xattr -dr com.apple.quarantine /path/to/application.app
```

### Key Distinctions
*   **`-d` (Delete):** Removes a **specific** named attribute (e.g., `com.apple.quarantine`).
*   **`-c` (Clear):** Removes **all** extended attributes from the file(s).
*   **`-r` (Recursive):** Applies the operation to all files within a directory.

### Important Notes
*   **Permissions:** You often need `sudo` to remove attributes from system or protected directories.
*   **Symlinks:** If working with symbolic links, add the `-s` flag (`-drs`) to act on the link itself rather than the target file.
*   **Provenance Attribute:** On newer macOS versions, the `com.apple.provenance` attribute may also block apps. If `-d com.apple.quarantine` fails, try `sudo xattr -cr` to clear all attributes, or ensure your Terminal app has **Full Disk Access** permissions.

