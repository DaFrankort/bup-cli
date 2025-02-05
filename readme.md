# bUp - CLI

A basic CLI tool to back up folders as zip files on your Windows PC.

**Note:** This is a personal project and may not cover all edge cases. Use at your own risk.

## Requirements

- Windows OS (Not tested on other OS)
- Python **3.11.5** (or later)
- `pip` installed

## Installation

1. Clone the repository:
   ```sh
   git clone <repo-url>
   ```
2. Navigate to the repository in your terminal:
   ```sh
   cd bup-cli
   ```
3. Install the package:
   ```sh
   pip install --user .
   ```
4. Verify the installation by running:
   ```sh
   bup
   ```
   This should display a list of available commands.

## Usage

`bUp` provides several commands to manage folder backups. Each command can be invoked using its full name or its first letter.

### ADD / A

**Command:**

```sh
bup add <path>
```

or

```sh
bup a <path>
```

Adds a folder to the backup list. You can provide either an absolute or relative path.

**Default Behavior:** If no path is provided, it defaults to the current directory (`.`).

### DEL / D

**Command:**

```sh
bup del
```

or

```sh
bup d
```

Lists all folders marked for backup. Enter the corresponding number to remove a folder from the list.

### LIST / L

**Command:**

```sh
bup list
```

or

```sh
bup l
```

Displays the list of folders set for backup along with the designated backup location.

### SET / S

**Command:**

```sh
bup set <path>
```

or

```sh
bup s <path>
```

Sets the specified path as the backup storage location.

**Default Behavior:** If no path is provided, it defaults to the current directory (`.`).

### RUN / R

**Command:**

```sh
bup run
```

or

```sh
bup r
```

Starts the backup process. It checks for changes in the marked folders and creates a zip archive for any modified folders, storing them in the designated backup location.

**Backup File Naming:** Backups are stored within a `/Backups` folder in your specified directory, using the folder path as name: e.g., `C_Users_UserName_Pictures.zip`.

### Automating Backups

bUp does not include an automatic scheduling feature. However, you can automate backups by placing a shortcut to the `bup_run.bat` file in the Windows Startup folder:

1. Press `WIN + R`
2. Type `shell:startup` and press `Enter`
3. Place a shortcut to `bup_run.bat` in this folder

This ensures backups run automatically when you start your PC.

---

Enjoy using **bUp**!
