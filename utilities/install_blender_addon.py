import argparse
import os
import shlex
import sys
import platform
from pathlib import Path
import zipfile
import shutil
import tempfile
import psutil
import subprocess

def get_quit_blend_path():
    """Determine the platform-specific path for quit.blend."""
    system = platform.system()
    home = Path.home()

    if system == "Linux":
        return home / ".local" / "share" / "blender" / "quit.blend"
    elif system == "Windows":
        return home / "AppData" / "Roaming" / "Blender Foundation" / "Blender" / "quit.blend"
    elif system == "Darwin":
        return home / "Library" / "Application Support" / "Blender" / "quit.blend"
    else:
        raise RuntimeError("Unsupported operating system.")

def get_blender_addons_path(version=None):
    """Determine the Blender add-ons directory based on the OS and version."""
    system = platform.system()
    home = Path.home()

    if system == "Linux":
        config_dir = home / ".config" / "blender"
    elif system == "Windows":
        config_dir = home / "AppData" / "Roaming" / "Blender Foundation" / "Blender"
    elif system == "Darwin":
        config_dir = home / "Library" / "Application Support" / "Blender"
    else:
        raise RuntimeError("Unsupported operating system.")

    if not config_dir.exists():
        raise FileNotFoundError(f"Blender config directory not found at {config_dir}")

    # List all version folders
    version_dirs = [d.name for d in config_dir.iterdir() if d.is_dir() and d.name[0].isdigit()]
    if not version_dirs:
        raise FileNotFoundError(f"No Blender version directories found in {config_dir}")

    if version:
        if version not in version_dirs:
            raise ValueError(f"Specified version {version} not found in {config_dir}. Available versions: {', '.join(version_dirs)}")
        addons_path = config_dir / version / "scripts" / "addons"
        print(f"Using add-ons path: {addons_path}")
    else:
        if len(version_dirs) > 1:
            raise ValueError(
                f"Multiple Blender versions found: {', '.join(version_dirs)}. "
                "Please specify a version using --version."
            )
        version = version_dirs[0]
        addons_path = config_dir / version / "scripts" / "addons"
        print(f"Version detected from app data: {version}")

    if not addons_path.exists():
        scripts_dir = os.path.dirname(addons_path)
        version_conf_dir = os.path.dirname(scripts_dir)
        if not os.path.isdir(version_conf_dir):
            raise FileNotFoundError(
                f"Configuration dir {version_conf_dir} does not exist.")
        if not os.path.isdir(scripts_dir):
            os.mkdir(scripts_dir)
        os.mkdir(addons_path)

    addons_path.mkdir(parents=True, exist_ok=True)
    return addons_path


def is_valid_addon_folder(folder_path):
    """Check if the folder contains an __init__.py file."""
    return (folder_path / "__init__.py").exists()


def extract_zip_addon(zip_path, temp_dir):
    """Extract ZIP and return the path to the add-on file or folder."""
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    temp_path = Path(temp_dir)
    # Look for a top-level .py file
    py_files = list(temp_path.glob("*.py"))
    if py_files:
        return py_files[0]

    # Look for a folder with __init__.py
    for item in temp_path.iterdir():
        if item.is_dir() and is_valid_addon_folder(item):
            return item

    raise ValueError(
        "ZIP does not contain a valid add-on"
        " (no .py file or folder with __init__.py).")


def install_addon(addon_path, addons_dir):
    """Install the add-on to the Blender add-ons directory."""
    addon_path = Path(addon_path).resolve()
    if not addon_path.exists():
        raise FileNotFoundError(f"Add-on path {addon_path} does not exist.")

    # Handle different add-on types
    if addon_path.suffix == ".py":
        # Single Python file
        shutil.copy(addon_path, addons_dir / addon_path.name)
        print(f"Installed {addon_path.name} to {addons_dir}")

    elif addon_path.suffix == ".zip":
        # ZIP file
        with tempfile.TemporaryDirectory() as temp_dir:
            extracted_path = extract_zip_addon(addon_path, temp_dir)
            if extracted_path.is_file():
                shutil.copy(extracted_path, addons_dir / extracted_path.name)
                print(f"Installed {extracted_path.name} to {addons_dir}")
            else:
                # Folder with __init__.py
                dest_folder = addons_dir / extracted_path.name
                if dest_folder.exists():
                    shutil.rmtree(dest_folder)
                shutil.copytree(extracted_path, dest_folder)
                print(f"Installed folder {extracted_path.name} to {addons_dir}")

    elif addon_path.is_dir():
        # Folder containing __init__.py
        if not is_valid_addon_folder(addon_path):
            raise ValueError(f"Folder {addon_path} is not a valid add-on (no __init__.py found).")
        dest_folder = addons_dir / addon_path.name
        if dest_folder.exists():
            shutil.rmtree(dest_folder)
        shutil.copytree(addon_path, dest_folder)
        print(f"Installed folder {addon_path.name} to {addons_dir}")

    else:
        raise ValueError("Unsupported add-on format. Must be a .py file, .zip file, or folder with __init__.py.")


match_name = "blender.exe" if platform.system() == "Windows" else "blender"


def find_blender_process():
    """Find running Blender processes, excluding those with 'blender_addon'."""
    blender_processes = []
    for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
        try:
            # Check process name and command line for 'blender'
            #   (case-insensitive)
            name = proc.info['name'].lower()
            cmdline = ' '.join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ''
            cmd_parts = shlex.split(cmdline)
            for cmd_part in cmd_parts:
                haystack = cmd_part
                if os.path.sep in haystack:
                    # Split the path for exact (case-insensitive) match,
                    #   since fuzzy match would match too much
                    #   such as blender-meshnav/pack.py etc.
                    path_parts = os.path.split(haystack)
                    haystack = path_parts[1]  # keep only the name
                # if 'blender' in name or 'blender' in cmdline:
                if ((haystack.lower() == match_name)
                        or (name.lower() == match_name)):
                    # Exclude processes with 'blender_addon'
                    if (('blender_addon' not in name)
                        and ('blender_addon' not in cmdline)):
                        blender_processes.append(proc)
                        break
                else:
                    print("Not blender command: {} (from {})"
                          .format(haystack, cmd_part))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if len(blender_processes) > 1:
        process_info = (
            "\n\n".join([f"Name: {p.info['name']},\n"
                         f"command: {p.info['cmdline'] if proc.info['cmdline'] else ''},\n"
                         f"PID: {p.pid}, Exe: "
                         f"{p.info['exe']}" for p in blender_processes]))
        raise RuntimeError(
            "Multiple Blender processes found"
            f" (close Blender first):\n\n{process_info}")

    return blender_processes[0] if blender_processes else None


def get_blender_version(executable_path):
    """Run Blender with --version and extract the version number."""
    try:
        result = subprocess.run(
            [str(executable_path), "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        for line in output.splitlines():
            if line.startswith("Blender"):
                parts = line.split()
                if len(parts) == 2:
                    version_parts = parts[1].split(".")
                    if len(version_parts) >= 2:
                        return ".".join(version_parts[:2])
        raise RuntimeError(f"Running blender executable {executable_path} did not output version in a known format")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to run {executable_path} --version: {e}")

def main():
    parser = argparse.ArgumentParser(description="Install a Blender add-on, managing running Blender process.")
    parser.add_argument("addon_path", help="Path to the add-on (.py, .zip, or folder).")
    parser.add_argument("--version", help="Blender version (e.g., 3.6).")
    parser.add_argument("--restart-blender", action="store_true", help="Allow restarting Blender if running.")
    args = parser.parse_args()

    try:
        # Get platform-specific quit.blend path (used for error message)
        quit_blend_path = get_quit_blend_path()

        # Check if Blender is running
        blender_proc = find_blender_process()
        if blender_proc and not args.restart_blender:
            print(
                f"Error: Blender is running. Specify --restart-blender if configured to save {quit_blend_path} "
                "otherwise close Blender manually first",
                file=sys.stderr
            )
            return 1

        # Initialize variables for version and executable
        found_version = None
        executable_path = None

        # If Blender is running and restart is allowed, get version and executable
        if blender_proc:
            executable_path = Path(blender_proc.exe()).resolve()
            print(f"Found Blender process (PID: {blender_proc.pid}) at {executable_path}")
            found_version = get_blender_version(executable_path)
            print(f"Detected Blender version: {found_version}")

        # Use found_version if no version specified
        version = args.version if args.version else found_version

        # Validate add-ons path
        addons_dir = get_blender_addons_path(version)

        # If Blender is running, terminate it
        if blender_proc:
            blender_proc.terminate()
            blender_proc.wait(timeout=5)  # Wait up to 5 seconds for termination
            print("Blender process terminated.")

        # Install the add-on
        install_addon(args.addon_path, addons_dir)

        # If Blender was running, restart it and instruct user to recover session
        if blender_proc:
            cmd = [str(executable_path)]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Restarted Blender. To recover your last session, click \"File\" > \"Recover Last Session\" in Blender.")
        print("Manual steps are required:")
        print("Blender, Edit, Preferences, Addons, then make sure MeshNav is checked.")
        return 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
