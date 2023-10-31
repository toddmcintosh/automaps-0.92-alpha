AutoMaps Add-On Notes (for version 0.9.2)
***************************************************
Author: Todd McIntosh


Description
---------------------------
The AutoMaps Add-On for Blender allows you to load/manage/refresh groups of related image textures in a structured and organized way. 



Image Texture Setup
---------------------------
In order to load image groups, they must be named in a specific way:

-imagename_DIF.ext
-imagename_NRM.ext
-imagename_BMP.ext
-imagename_SPC.ext

You can mix image groups in a single textures folder or keep separate in subfolders.




Usage
---------------------------
There are essentially three main tasks that AutoMaps can do for you:


Loading
---------------------------
1. Enable the Add-On in Blender (currently only tested against 2.6x-2.70)
2. Switch to Node Editor view, and Material view. you should see the AutoMaps panel on the right side of the window in the Properties column.
3. To add a new AutoMaps group node:

	a. Click the choose Texture Folder button. A file dialogue will come where you need to choose the folder with your textures.
	b. The Groups Found dropdown menu will be loaded with the Group Names the addon has found.
	c. Select a Group in the dropdown menu and click the Create New AutoMap button.


Reloading
---------------------------
1. If you've edited a texture map in an external program, save the texture to the same location with the same name.
2. Select the blue AutoMap group node in Blender. A new Active AutoMap panel will appear on the right.
3. Click Refresh Maps. Blender should now be referencing the updated texture map.


Replacing
---------------------------
To keep your group node in place but replace the set of texture with a different group:
1. Select the blue AutoMap group node.
2. Select a Group in the dropdown menu and click the Create New AutoMap button.
3. Click the Load New Maps button.

Note: If you want to switch to a group of textures already loaded into blender, you can click on the node tree drop down menu on the node itself and switch to a different AutoMap group instance.




Possible Future Features:
---------------------------
- ability to load texture groups from one main texture folder with many different texture group files in it instead of requiring the subfolders to group them
- ability to auto-refresh files based on changed modification date
- convert group node to a custom group node (pynodes) to allow more gui options on the node itself (i.e. Refresh button, etc)
- ability to create Presets of commonly used File Conventions other than the default (ie. support _D, _N instead of just _DIF, _NRM) in order to make working with different texture generators easier (i.e. CrazyBump, Photoshop, Gimp, GameTextures, etc.)












