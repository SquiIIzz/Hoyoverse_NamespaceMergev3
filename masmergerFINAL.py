#MasterMerger

import os
import re
import difflib
import argparse
import configparser
import hashlib
import chardet
import sys

def main():
    parser = argparse.ArgumentParser(description="Generates merged mods for multiple characters")
    parser.add_argument("-r", "--root", type=str, default=".", help="Location of the mods folder")
    parser.add_argument("-d", "--delete", action="store_true", help="Run the script in delete mode")
    parser.add_argument("-v", "--vanilla", action="store_true", help="Exclude vanilla outfit as a part of the mod")
    parser.add_argument("-e", "--enable", action="store_true", help="Delete disabled .ini files that were created")
    parser.add_argument("-f", "--renable", action="store_true", help="Re-enable disabled .ini files")
    parser.add_argument("-x", "--delete and renmerge", action="store_true", help="deletes and remerges .ini files")
    parser.add_argument("-dh", "--disable-help", action="store_true", help="Disable all help.ini files")
    parser.add_argument("-eh", "--enable-help", action="store_true", help="Enable all disabled help.ini files")
    args = parser.parse_args()

    # Check for existing merges if no arguments are provided
    if len(sys.argv) == 1:
        existing_merges = check_existing_merges(args.root)
        if existing_merges:
            print("\nPre-existing merge files detected in subdirectories.\n")
            choice = input("Enter [1] to delete then remerge (when updating skins)\nEnter [2] to delete \nEnter [any other key] to exit\n>  ")
            if choice == '1':
                print("deleting and remerging")
                delete_main(args.root)
            elif choice == '2':
                print("deleting old .ini files")
                delete_main(args.root)
                print("enabling help .ini files")
                enable_help(args.root)
                return
            else:
                print("Exiting program.")
                return
            
    if args.delete:
        delete_main(args.root)
        return
    
    if args.disable_help:
        print("disabling help .ini files")
        disable_help(args.root)
        print("help .ini files disabled")
        return

    if args.enable_help:
        print("enabling help .ini files")
        enable_help(args.root)
        print("help .ini files enabled")
        return

    print("\nGenshin and Star Rail Mod Merger/Toggle Creator Script Utilizing Namespaces\n")
    choice = input("Press Enter to continue or any other key to exit...")
    
    if choice != "":
        print("Exiting program.")
        sys.exit()

    character_folders = [f for f in os.listdir(args.root) if os.path.isdir(os.path.join(args.root, f)) and "disabled" not in f.lower()]
    
    # Manage config file
    config = manage_config(args, character_folders)

    for character_folder in character_folders:
        character_path = os.path.join(args.root, character_folder)
        print(f"\nProcessing {character_folder}...")

        # Get key bindings from config
        key = config[character_folder].get('Cycle forward', 'ctrl \'')
        back = config[character_folder].get('Cycle backward', 'ctrl ;')

        if args.enable:
            print("Re-enabling all.ini files")
            enable_ini(character_path, delete_disabled=args.enable)
            print()
        if args.renable:
            print("Re-enabling old.ini files")
            renable_ini(character_path)
            print()

        # Search for .ini files in the character folder
        ini_files = collect_ini(character_path)
        if not ini_files:
            print(f"Found no .ini files in {character_folder} - skipping.")
            continue

        # Place holder for the vanilla outfit
        ini_files.insert(0, None)

        # List all found files
        print("\nFound:")
        print("\t0: Vanilla Outfit")
        for i, ini_file in enumerate(ini_files):
            if i != 0:
                print(f"\t{i}: {ini_file}")

        print("\nThis script will merge using the order listed above.")
        if args.vanilla:
            print("The vanilla outfit will be removed at the end")
            ini_files.pop(0)

        # Generate backups
        print("Generating backups")
        generate_backup(ini_files)

        # Generate the master.ini file
        create_master_ini(ini_files, character_folder, key, back, character_path)
             
    print("disabling help inis")
    disable_help(args.root)
    
    print("All operations completed")
    
###
### New in V3
###

def check_existing_merges(root):
    master_files = []
    # go through directories in the root folder
    for dir_name in os.listdir(root):
        dir_path = os.path.join(root, dir_name)
        if os.path.isdir(dir_path):
            # Check for Master*.ini file in each directory
            master_file = os.path.join(dir_path, f"Master{dir_name}.ini")
            if os.path.exists(master_file):
                master_files.append(master_file)

    # Print detected master files
    if master_files:
        print("\nMaster .ini files detected:")
        for i, file in enumerate(master_files, 1):
            print(f"{i}. {file}")

    return master_files  # Return list of found master files

def delete_main(root):
    print("\nNamespace Merged Mod Unmerger\n")
    print("\nTHIS SCRIPT WILL DELETE FILES FROM YOUR DEVICE USE WITH CAUTION AND MAKE BACKUPS")
    print("Press enter to proceed or enter anything else to exit")
    userin = input()
    if userin != "":
        print("Exiting")
        return

    # Searches for .ini files in the main directory subdirectories
    print("\nSearching for .ini files with backups in subdirectories")
    ini_paths = []
    master_files = []
    
    # Iterate over each folder in the main directory
    for character_folder in os.listdir(root):
        character_path = os.path.join(root, character_folder)
        if os.path.isdir(character_path):
            # Collect master.ini files
            master_file = os.path.join(character_path, f"Master{character_folder}.ini")
            if os.path.exists(master_file):
                master_files.append(master_file)

            # Search for .ini files in the immediate subdirectories of each character folder
            for subfolder in os.listdir(character_path):
                subfolder_path = os.path.join(character_path, subfolder)
                if os.path.isdir(subfolder_path):
                    for file in os.listdir(subfolder_path):
                        if file.lower().endswith('.ini') and 'disabled' not in file.lower():
                            disabled_file = os.path.join(subfolder_path, 'DISABLED' + file)
                            if os.path.exists(disabled_file):
                                ini_paths.append(os.path.join(subfolder_path, file))
                            else:
                                print(f"No backup for {file}, {file}.ini will be preserved")

    if not ini_paths and not master_files:
        print("Found no .ini files with backups or master files - make sure the mod folders are in the correct structure.")
        return

    # Lists all found files
    print("\nFound:")
    for i, ini_file in enumerate(ini_paths):
        print(f"\t{i}: {ini_file}")

    print("\nMaster merge files:")
    for i, master_file in enumerate(master_files):
        print(f"\t{i}: {master_file}")

    print("\nAll .ini files and master files displayed above will be deleted and their backups will be restored")
    print("Press enter to proceed with the delete or enter a number to remove a file from the deletion list.")
    print("ONLY ENTER ONE NUMBER! you will be able to remove other paths from deletion list")

    while True:
        userin = input()
        if userin == "":
            break
        try:
            index = int(userin)
            if 0 <= index < len(ini_paths):
                removed_file = ini_paths.pop(index)
                print(f"\nRemoved path number {index}: {removed_file}")
            else:
                print(f"\nInvalid index: {index}")
        except ValueError:
            print(f"\nInvalid input: {userin}")
        
        print("Current Deletion List:")
        for i, ini_file in enumerate(ini_paths):
            print(f"\t{i}: {ini_file}")
        print("Press enter to proceed with the delete or enter a number to remove a file from the deletion list.")
        print("ONLY ENTER ONE NUMBER! you will be able to remove other paths from deletion list")

    try:
        # Delete master files
        for master_file in master_files:
            os.remove(master_file)
            print(f"Deleted master file: {master_file}")

        # Delete and restore backup for other .ini files
        for file in ini_paths:
            # Deletes the file
            os.remove(str(file))
            # Renames the backup file
            try:
                disabled_file = os.path.join(os.path.dirname(file), 'DISABLED' + os.path.basename(file))
                os.rename(disabled_file, file)
                print(f"Restored backup for {file}")
            except Exception as e:
                print(f"Error restoring backup for {file}: {str(e)}")
        
        print("All operations completed")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

### Modified ini aggregator

# Collects all .ini files from current folder (ignores subfolders)
def collect_ini(path):
    ini_files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            selected_ini = find_best_ini(item_path, item)
            if selected_ini:
                ini_files.append(selected_ini)
                
    return ini_files

# Selects the best .ini file from a folder based on specific criteria
def find_best_ini(folder_path, folder_name):
    # First, look for 'merged.ini'
    merged_ini = os.path.join(folder_path, 'merged.ini')
    if os.path.exists(merged_ini):
        return merged_ini

    # Get the parent folder name
    parent_folder_name = os.path.basename(os.path.dirname(folder_path))

    # If 'merged.ini' doesn't exist, find the .ini file with the closest name match to the parent folder
    closest_ini = None
    highest_ratio = 0
    for file in os.listdir(folder_path):
        if file.lower().endswith('.ini') and 'disabled' not in file.lower():
            # Calculate the similarity ratio between the parent folder name and the file name
            ratio = difflib.SequenceMatcher(None, parent_folder_name.lower(), file.lower()).ratio()
            if ratio > highest_ratio:
                highest_ratio = ratio
                closest_ini = os.path.join(folder_path, file)

    return closest_ini

def enable_ini(path, delete_disabled=False):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            for file in os.listdir(item_path):
                if file.lower().endswith('.ini') and 'disabled' in file.lower():
                    regular_file = file.lower().replace("disabled", "")
                    regular_path = os.path.join(item_path, regular_file)
                    disabled_path = os.path.join(item_path, file)
                    if os.path.exists(regular_path):
                        print(f"\tDeleting {regular_path}")
                        os.remove(regular_path)
                    print(f"\tRe-enabling {disabled_path}")
                    os.rename(disabled_path, regular_path)
    print("Disabled .ini files re-enabled.")

def renable_ini(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            for file in os.listdir(item_path):
                if file.lower().endswith('.ini') and 'disabled' in file.lower():
                    disabled_path = os.path.join(item_path, file)
                    new_path = re.compile("disabled", re.IGNORECASE).sub("", disabled_path)
                    print(f"\tRe-enabling {disabled_path}")
                    os.rename(disabled_path, new_path)
    print("Old Merge Script Disabled .ini files re-enabled.")

def get_key_bindings(character):
    print(f"\nNew character added")
    print(f"\nSet up cycle keys for {character}")
    print("Please enter the key that will be used to cycle mods forward. (default: ctrl ')")
    key = input().strip() or "ctrl '"
   
    print("Please enter the key that will be used to cycle mods backwards. (default: ctrl ;)")
    back = input().strip() or "ctrl ;"
   
    return key.lower(), back.lower()

def disable_help(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower() == "help.ini":
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, "DISABLEDhelp.ini")
                try:
                    os.rename(old_path, new_path)
                    print(f"Disabled: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error disabling {old_path}: {str(e)}")

def enable_help(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower() == "disabledhelp.ini":
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, "help.ini")
                try:
                    os.rename(old_path, new_path)
                    print(f"Enabled: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error enabling {old_path}: {str(e)}")

def create_master_ini(ini_files, name, key, back, character_path):
    
    # Generates the namespace for the master file
    constants =     f"namespace = {name}\\Master\n; Constants---------------------------\n\n"
    overrides =    "; Overrides ---------------------------\n\n"
    swapvar = "swapvar"
    
    # adds the [Constants] section
    constants += f"[Constants] \nglobal persist ${swapvar} = 0\n"
    constants += f"global $active\n"
    constants += "global $creditinfo = 0\n"
    
    # adds the [KeySwap] section
    constants += f"\n[KeySwap]\n"
    constants += f"condition = $active == 1\n"
    constants += f"key = {key}\nback = {back}\ntype = cycle\n"
    constants += f"${swapvar}= {','.join([str(x) for x in range(len(ini_files))])}\n$creditinfo = 0 \n\n"
    
    # adds the [Present] section to not swap when character is not active
    constants += f"[Present] \n"
    constants += f"post $active = 0\n"
    
    # this gets the position override and may cause problems if mods for multiple charters are added as that character will not be detected
    overrides = f"[TextureOverride{name}Position]\n"
    for file in ini_files:
        if file is not None:
            temp = get_position_hash(str(file))
            if temp != ";None found\n":
                overrides += temp
                break
    overrides += "$active = 1\n"
    
    print("Modifying inis...")
    for i, ini_file in enumerate(ini_files):
        if ini_file is not None:
            edit_ini(str(ini_file), name, i)
    ini_files = [x for x in ini_files if x is not None]
    result = f"; Merged Mod: {', '.join([x for x in ini_files])}\n\n"
    result += constants
    result += overrides
    result += "\n\n;.ini generated by GIMI (Genshin-Impact-Model-Importer) mod merger script utilizing namespaces\n"
    result += "; If you have any issues or find any bugs dm qwerty3yuiop on discord or leave a comment on game banana"
    with open(os.path.join(character_path, f"Master{name}.ini"), "w", encoding="utf-8") as f:
        f.write(result)
        
# Gets the user's preferred order to merge mod files

def get_user_order(ini_files):

    choice = input()
    # User entered data before pressing enter
    while choice:
        choice = choice.strip().split(" ")

        if len(choice) > len(ini_files):
            print("\nERROR: please only enter up to the number of the original mods\n")
            choice = input()
        else:
            try:
                result = []
                choice = [int(x) for x in choice]
                if len(set(choice)) != len(choice):
                    print("\nERROR: please enter each mod number at most once\n")
                    choice = input()
                elif max(choice) >= len(ini_files):
                    print("\nERROR: selected index is greater than the largest available\n")
                    choice = input()
                elif min(choice) < 0:
                    print("\nERROR: selected index is less than 0\n")
                    choice = input()
                    print()
                else:
                    for x in choice:
                        result.append(ini_files[x])
                    return result
            except ValueError:
                print("\nERROR: please only enter the index of the mods you want to merge separated by spaces (example: 3 0 1 2)\n")
                choice = input()

    # User didn't enter anything and just pressed enter
    return ini_files

###
###     INI FILE MODIFICATION
###

# Editing existing inis and adding needed text at the end for shader and texture overrides.
def edit_ini(path, name, num):
    with open(path, 'r') as file:
        lines = file.readlines()
    found = False
    count = 0
    max = len(lines)-1
    block = []
    with open(path, 'w') as file:
        for line in lines:
            # Ends the if when a line with [ or when end of file is reached
            # meant to end on next overide
            if found and line.startswith('[') or count == max:
                block.append(line)
                line = comment_fix(block)
                block = []
                found = False
            # if there is already a match priority remove it
            elif found and line.lower().startswith('match_priority'):
                block.append("")
            # adds a tab to every line in the if
            elif found:
                line = "\t" + line
                block.append(line)
            # looks for lines that start with a hash and starts an if statement.
            elif line.strip().lower().startswith('hash = ') or line.strip().lower().startswith('hash='):
                # adds namespace also this line is by ricochet_7
                line = line + f'match_priority = {num}\n' + f"if $\{name}\Master\swapvar=={num}\n"
                found = True
                block.append(line)
            if not found:
                file.write(line)
            count += 1

# makes sure to place the endif immediatly after code to be enclosed
def comment_fix(block):
    index = len(block) - 1
    # cycle from the bottom
    for line in reversed(block):
        # If text that is not ; "" [ are found, end if is placed there
        if not line.strip().startswith(';') and not line.strip().startswith('[') and not line.strip() == "":
            block[index] = block[index].rstrip()+"\nendif\n\n"
            break
        # removes any indentation given to comments as a result of the previous function
        elif line.strip().startswith(';'):
            block[index] = block[index].lstrip()
        index -= 1
    line = ""
    for x in block:
        line = line + x
    block = []
    return line

# makes a copy of a file that is DISABLED
def generate_backup(file_list):
    for file_path in file_list:
        try:
            if file_path != None:
                dir_name = os.path.dirname(file_path)
                base_name = os.path.basename(file_path)
                new_file_path = os.path.join(dir_name, 'DISABLED' + base_name)
                with open(file_path, 'r') as original_file, open(new_file_path, 'w') as new_file:
                    new_file.write(original_file.read())
        except:
            print("!!! NON-LATIN/ASCII FILNEAME ENCOUNTERED !!!")
            print("Please rename to process properly")
        continue

# finds the position override of a a character and returns it
def get_position_hash(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        found = False
        for line in lines:
            # Ends the if when a line with [] or ; is found
            if line.startswith('[TextureOverride') and line.endswith('Position]\n'):
                found = True
            if found and (line.strip().lower().startswith('hash = ') or line.strip().lower().startswith('hash=')):
                return line
        return ";None found\n"

# renames file
def rename_file(file_path):
    if file_path != None:
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        os.rename(dir_name + '\\DISABLED' + base_name, dir_name + '\\' + base_name)
        
        
# config file creation
def manage_config(args, character_folders):
    config = configparser.ConfigParser()
    config_file = os.path.join(args.root, 'merger_config.ini')
    
    if not os.path.exists(config_file):
        # Create new config file if one doesn't exist already
        # uses default keybindings of ' and ;
        for character in character_folders:
            config[character] = {
                'Master file': f'Master{character}.ini',
                'Cycle forward': 'ctrl \'',
                'Cycle backward': 'ctrl ;'
            }
        
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        print(f"Created new config file: {config_file}")
    else:
        # Read existing config file
        config.read(config_file)
    
        # removes character configs when applicable
        # i.e. their folder name changes or it's deleted
        for character in list(config.sections()):
            if character not in character_folders:
                config.remove_section(character)
                print(f"Removed configuration for non-existent character folder: {character}")
    
        # Add new characters if any
        # i.e. new char added or existing char gets a diff folder name
        for character in character_folders:
            if character not in config:
                config[character] = {
                    'Master file': f'Master{character}.ini',
                    'Cycle forward': 'ctrl \'',
                    'Cycle backward': 'ctrl ;'
                }
        
        # Update config file with new characters
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    
    return config

if __name__ == "__main__":
    main()