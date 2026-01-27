A simple script that allows multiple skins for characters to coexist cleanly in a merged setup.

Unlike previous iterations which are on a per-character/folder basis, this script can be used
inside the main 'characters' folder to automatically merge .ini files of ALL characters within 
the parent directory.

<b>Current features:</b>
1. CLI-based navigation
2. bulk namespace merge & unmerge
3. bulk character update (updates merged namespace with any new mods)
4. disables help.ini files (prevents hotkey issues & unwanted overlays on incompatible skins)
5. config file creation to modify hotkeys
6. .ini file rollback in case of skins bricking

<b>DISCLAIMER:</b>

1. DUE TO THE NATURE OF NAMESPACE MERGING (.ini file modification),
   IT IS IMPERATIVE THAT YOU CREATE A BACKUP OF YOUR CHARACTER FOLDER
   BEFORE USING.

3. IT IS IMPORTANT YOU HAVE A FOLDER SPECIFICALLY FOR CHARACTERS AS 
   THIS WILL MODIFY ANY/ALL EXISTING INI FILES IN THE PARENT DIRECTORY
   INCLUDING NON-CHARACTER MODS (GUI mods, Shaders, Objects, Weapons, etc)

   this script is not intended for use in those directories as they have
   a different organizational hierarchy. Please use this in your character
   directory

   I will not be accountable for incurred losses due to the failure to
   follow these instructions. (not making backups, using it with pre-
   existing merges)

<b>HOW TO USE:</b>

1. UNMERGE YOUR CHARACTER SKINS IF THEY ARE CURRENTLY MERGED
2. Download/place the script in your CHARACTER directory

   <img width="229" height="44" alt="image" src="https://github.com/user-attachments/assets/36272af9-7a39-4b23-a3b4-d0c87476d6dd" />
4. open up a powershell terminal within the folder and run the script using 'python masmergerFINAL.py'
5. press enter and allow the script to run. It will merge all your characters & create a config file
6. TO CHANGE SKIN CYCLE HOTKEYS: open the merger_config file in a text editor and change the
   'cycle forward/back' entries directly after the '=' sign. by default, it's (;) and (')
7. TO UPDATE SKINS: after placing a new skin in a character folder, simply run the script again.
   and enter '1'. This will modify the existing merges and incorporate the mod you add.
8. UNMERGING: Run this script again and hit '2'. this will unmerge any pre-existing merges.
   I also recommend doing this before uninstalling as you'll have a fresh character directory
   when using other namespace merge mods. 

<b>TROUBLESHOOTING:</b>

Q: Some of my characters aren't modded

A: The most likely problem are folders that aren't named after the
   in-game character names so the program skips these. these are names 
   decided by the devs and it's how the game's logic differentiates each 
   character. There are several organizational mods on Gamebanana that 
   automatically inject these folders in your character directly to 
   accurately reflect who's being modded. for example, your "Jean swimsuit"
   character folder may not be recognized by the script since the game's 
   name for her is "JeanSea"

   <img width="108" height="68" alt="image" src="https://github.com/user-attachments/assets/8b374edb-cf7b-48d2-a59d-66f31ffa9a85" />
   

Q: How do i change the hotkeys to cycle between skins?

A. By default, the main keys for swapping back and forth between skins is the
   semicolon (;) and single quote (') key respectively
   
   When the script is used, a "merger_config" file is created which stores hotkey
   settings. you can view these by opening the file in a text editor and making
   changes you deem necessary. I recommend doing this for characters with mounts
   as they may change when you cycle through the affected character's skins. 

   <img width="309" height="263" alt="image" src="https://github.com/user-attachments/assets/4cf3a03d-4bf4-4228-8ee0-81d37858de89" />
   

Q: My Kachina/Furina's skill doesn't have the right skins

A: entities such as Kachina's drill and Fuuina's summons are decoupled from the
   mod/skin it comes with. this is a feature allowing you cycle through different
   skins for them using hotkeys instead of it being relegated to a single skin.
   (ie. multiple mounts for Kachina that can be used in tandem with her other skins). 
   
   hotkey settings can be found in the "merger_config" folder and can be modified
   to your choosing


Please message me on Github for any inquiries.

