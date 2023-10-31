### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "AutoMaps Alpha",
    "author": "Todd McIntosh",
    "version": (0, 9, 2),
    "blender": (2, 7, 0),
    "location": "Node Editor > Sidebar",
    "description": "Allows easy import, setup, and reloading of related image maps.",
    "warning": "",
    "category": "Material",
    "tracker_url": "http://cgcookiemarkets.com/blender/all-products/automaps-texture-group-manager-addon/",
    "wiki_url": "http://cgcookiemarkets.com/blender/all-products/automaps-texture-group-manager-addon/"
    }





import bpy
from mathutils import Vector
import os, datetime
from bpy.props import BoolProperty
from bpy.props import *
import time
from collections import OrderedDict




scn = bpy.types.Scene

scn.filePath =  StringProperty(name="Maps Folder", description="Image Folder Path", subtype="DIR_PATH", update=None)
scn.updateFilePath =  StringProperty(name="New Folder", description="Image Folder Path", subtype="DIR_PATH", update=None)

mapSuf = {}
mapSuf["DIF"] = ["DIF", "D", "DIFFUSE", "COLOR", "COLOUR", "COL", "C","CO"]
mapSuf["NRM"] = ["NRM","NM","NORMAL","N","NO"]
mapSuf["NRMY+"] = ["nY+","NMY+","NORMALY+", "NOY+"]
mapSuf["REF"] =  ["REF", "RF","REFLECTION","G","GLOSSY","GLS"]
mapSuf["BMP"] = ["BMP","BUMP","B","BP","H","HT","HEIGHT"]
mapSuf["TRN"] = ["TRN","ALPHA","A","ALP","TRANSPARENCY"]
mapSuf["AO"] = ["AO","O","OCCLUSION","AMBOCC"]
mapSuf["TRL"] = ["TRL","TRANS","TRANSLUCENCY"]
mapSuf["EMS"] = ["EMS","E","ES","GLOW","LIGHT","L","GL"]
mapSuf["DSP"] = ["DSP","D","DISPLACEMENT","DISP"]
mapSuf["SSS"] = ["SSS","SUBSURFACESCATTERING","SCT","SUB","SB"]
mapSuf["SPC"] = ["SPC","S","SP","SPEC","SPECULAR"]


scn.drpFileList = EnumProperty(items = [('None', 'None', 'None')], name = "")
scn.TextureGroupNames = ""


imgNodes = []

startYpos = 600
startXpos = -800
ySpacing = 80
xSpacing = 180

imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapDiffuse', 'Diffuse/Color','COLOR','DIF'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapNormal', 'Normal','NONE','NRM'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapNormalY+', 'Normal Y+','NONE','NRMY+'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapBump','Bump/Height','NONE','BMP'])     

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapSpecular','Specular','NONE','SPC'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapDisplacement', 'Displacement','NONE','DSP']) 

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapTransparency', 'Transparency/Alpha','NONE','TRN'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapReflection', 'Reflection/Glossy','NONE','REF'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapAO','AO','COLOR','AO'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapEmission', 'Emission/Glow','NONE','EMS'])

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapTranslucency', 'Translucency','NONE','TRL']) 

startYpos -= ySpacing
startXpos += xSpacing
imgNodes.append(['ShaderNodeTexImage', (startXpos, startYpos), 'MapSSS', 'SSS','NONE','SSS']) 







class AutoMapsPanel(bpy.types.Panel):
    
    bl_label = "AutoMaps"
    bl_idname = "Automaps"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = "object"


    


    @classmethod
    def poll(cls,context):
       
        showPanel = True
        if context.space_data.tree_type != 'ShaderNodeTree':
            showPanel = False 
        if context.scene.render.engine != 'CYCLES':
            showPanel = False 

        return showPanel

   


    newAutoMapUserMsg = ""
    updateAutoMapUserMsg = ""
    progressBar = ""


    def draw_header(self, context):
      
        layout = self.layout
        layout.label(icon='ASSET_MANAGER') 



            
    def draw(self, context):

        currentMat = bpy.context.active_object.active_material

        layout = self.layout
        obj = context.object
        sce = bpy.context.scene
    
        layout.separator()

        boxTextFolder = layout.box()
        boxTextFolder.scale_y = 1.0
        boxTextFolder.label("Source Texture Folder", icon='IMASEL') 

        row = boxTextFolder.row()
        row.label(text="Choose your texture group folder:")


        row = boxTextFolder.row()
        row.scale_y = 1.5
        row.operator("object.choose_texture_folder", icon="ZOOMIN", text="Choose Texture Folder        ")
        # boxNew.separator()

        row = boxTextFolder.row()
        row.label(text="Groups found:")

        row = boxTextFolder.row()
        row.prop(sce, 'drpFileList')
    
        boxTextFolder.separator()

        layout.separator()


        boxNew = layout.box()
        boxNew.scale_y = 1.0
        boxNew.label("Create New AutoMap:", icon='IMASEL') 

        if self.newAutoMapUserMsg != "":
            boxNew.label(text=self.newAutoMapUserMsg,icon='ERROR')

        row = boxNew.row()
        row.scale_y = 1.5
        row.operator("object.genimgnodes", icon="ZOOMIN", text="Create New AutoMap        ")

        boxNew.separator()


        layout.separator()
        layout.separator()


        activeNode = currentMat.node_tree.nodes.active

        if activeNode != None and activeNode.type=='GROUP':

            groupDataBlock = activeNode.node_tree

            if groupDataBlock['AutoMaps.isAutoMap']:

                getAutoMapsIsAutoMapForNode = groupDataBlock['AutoMaps.isAutoMap']
           
                if(getAutoMapsIsAutoMapForNode==1):
                
                    box = layout.box()
                    box.scale_y = 1.0

                    box.label("Active AutoMap:", icon='IMASEL') 
                    box3 = box.box()
                    box3.prop(groupDataBlock, 'name', emboss=False)
                    box3.prop(groupDataBlock, '["AutoMaps.FolderPath"]', text="Current Folder", emboss=False)
                    box3.operator("am.refresh", text = "Refresh Maps", icon='FILE_REFRESH')
                    box.separator() 
                   
                    box3 = box.box()
                    box3.label("Replace Images with New Map Group")   
                    # box3.prop(sce, 'updateFilePath')
                    
                    if self.updateAutoMapUserMsg != "":
                        box3.label(text=self.updateAutoMapUserMsg,icon='ERROR')

                    box3.operator("object.update", text = "Load New Maps", icon='FILE_REFRESH')
         
                    layout.separator()
        
        row = layout.row()
        row.scale_y = 0.5
   
        attrString = str(bl_info['name']) + " " + str(bl_info['version']) + ". Author: " + str(bl_info['author'])

        row.label(text=attrString)










class SelectTextureFolder_OT(bpy.types.Operator):
    bl_idname = "object.choose_texture_folder"
    bl_label = "Select Texture Folder"
 
    directory = StringProperty(maxlen=1024, subtype='DIR_PATH', options={'HIDDEN', 'SKIP_SAVE'})

    def execute(self, context):
        path = self.properties.directory
        groupNameList = {}

        for file in os.listdir(bpy.path.abspath(path)):
       
            splitFile = os.path.splitext(file)
            ext = splitFile[1]
           
            if ext in bpy.path.extensions_image:
                nameNoExt = splitFile[0]
                lastHyphenIndex = nameNoExt.rfind('_')
                groupName = nameNoExt[0:lastHyphenIndex]
                groupNameList[groupName] = path 

        OrderedDict.fromkeys(groupNameList).keys()


       

        nameTupleList = []
        for g in groupNameList.items():
           

            nameTuple = (g[0], g[0], g[1])
            nameTupleList.append(nameTuple)
            
        scn.TextureGroupNames = nameTupleList
            
        scn.drpFileList = EnumProperty(items = nameTupleList, name = "")



       


        return {'FINISHED'}


 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)


        return {'RUNNING_MODAL'}
 
    


class GetMapFolder(bpy.types.Operator):
    bl_idname = "object.getfolder"
    bl_label = "Get map Folder" 
    
 
    def execute(self, context):

        layout = self.layout
        layout.prop(sce, 'filePath')
       
        return{'FINISHED'}  



class OBJECT_OT_LoadMaps(bpy.types.Operator):
    bl_idname = "object.loadmaps"
    bl_label = "Load Image Maps" 
 
    def execute(self, context):

        LoadMaps(sce.filePath)
       
        return{'FINISHED'}  




def LoadMaps(folderPath, autoMapNodeTree, getSelecteGroupName):

 
    checkNodes(autoMapNodeTree, folderPath, getSelecteGroupName)

           
  

def UpdateMapsInAutoMap(folderPath, autoMapNodeTree, getSelecteGroupName):

    checkNodes(autoMapNodeTree, folderPath, getSelecteGroupName)
        


def FindMapType(dir, mapSuf, getSelecteGroupName):

    for file in os.listdir(bpy.path.abspath(dir)):
       
        splitFile = os.path.splitext(file)
        ext = splitFile[1]
        fileNameNoExt = splitFile[0]

        if fileNameNoExt.startswith(getSelecteGroupName):
            if ext in bpy.path.extensions_image:
                for suffix in mapSuf:
                    if fileNameNoExt.upper().endswith('_' + suffix.upper()):
                        return(file)

    return('NOFILEFOUND')




class OBJECT_OT_UpdateImgNodes(bpy.types.Operator):

    bl_idname = "object.update"
    bl_label = "Update Image Texture Nodes in AutoMap" 


    def execute(self, context):
        
        sce = bpy.context.scene
        
        if sce.drpFileList == 'None':

            bpy.types.Automaps.updateAutoMapUserMsg = "Please choose a Texture Folder"

        else:

            currentMAT = bpy.context.object.active_material  
            getSelecteGroupName = sce.drpFileList

            print(str(sce.TextureGroupNames))


            for t in sce.TextureGroupNames:
                if t[0] == getSelecteGroupName:
                    getSelectedGroupNamePath = t[2]
          
            folderPath = sce.filePath
            newPath = folderPath


            activeNode = currentMAT.node_tree.nodes.active
            autoMap = activeNode.node_tree

            print(str(autoMap['AutoMaps.FolderPath']))
            print(str(autoMap['AutoMaps.FileGroupName']))

            print("getSelecteGroupName: " + getSelecteGroupName)
            print("getSelectedGroupNamePath: " + getSelectedGroupNamePath)
            

            if(autoMap['AutoMaps.isAutoMap']==1):

                UpdateMapsInAutoMap(getSelectedGroupNamePath, autoMap, getSelecteGroupName)

                autoMap['AutoMaps.FolderPath'] = getSelectedGroupNamePath
                autoMap['AutoMaps.FileGroupName'] = getSelecteGroupName


                if(folderPath[-1:] in ['\\','/']):
                    newPath = folderPath[:-1]
                    newGroupName = "AM-" + bpy.path.display_name_from_filepath(getSelecteGroupName.upper())
                    autoMap.name = newGroupName
                    activeNode.name = newGroupName
                    activeNode.label = newGroupName

        
        return{'FINISHED'}  




class OBJECT_OT_RefreshImgNodes(bpy.types.Operator):
    bl_idname = "am.refresh"
    bl_label = "Refresh Image Texture Nodes in AutoMap" 
  

    def execute(self, context):

        sce = bpy.context.scene
        currentMat = bpy.context.active_object.active_material

        activeNode = currentMat.node_tree.nodes.active
        autoMap = activeNode.node_tree

    
        if(autoMap['AutoMaps.isAutoMap']==1):
            getAutoMapsPathForNode = autoMap['AutoMaps.FolderPath']
            getSelecteGroupName = autoMap['AutoMaps.FileGroupName']
            UpdateMapsInAutoMap(getAutoMapsPathForNode, autoMap, getSelecteGroupName)
        
        return{'FINISHED'}  






class OBJECT_OT_GenImgNodes(bpy.types.Operator):
    bl_idname = "object.genimgnodes"
    bl_label = "Generate AutoMap" 


    def execute(self, context):
        
        sce = bpy.context.scene
    

        if sce.drpFileList == 'None':

            bpy.types.Automaps.newAutoMapUserMsg = "Please choose a Texture Folder"

        else:

            currentMAT = bpy.context.object.active_material  
            currentMAT.use_nodes = True
            
            getSelecteGroupName = sce.drpFileList

            for t in sce.TextureGroupNames:
                if t[0] == getSelecteGroupName:
                    getSelectedGroupNamePath = t[2]

          
            sce.filePath = getSelectedGroupNamePath
            folderPath = sce.filePath
            newPath = folderPath

            if(folderPath[-1:] in ['\\','/']):
                newPath = folderPath[:-1]

            newGroupName = "AM-" + bpy.path.display_name_from_filepath(getSelecteGroupName.upper())
            
            autoMapGroup = bpy.data.node_groups.new(newGroupName, 'ShaderNodeTree')   
            
            autoMapGroup['AutoMaps.FolderPath'] = folderPath
            autoMapGroup['AutoMaps.isAutoMap'] = True
            autoMapGroup['AutoMaps.FileGroupName'] = getSelecteGroupName

            workNodeTree = autoMapGroup 


            gOutput = workNodeTree.nodes.new('NodeGroupOutput')
            gOutput.label = 'Group Output'
            gOutput.name = 'Group Output'
            gOutput.location = Vector((1700, 600))
            
            gInput = workNodeTree.nodes.new('NodeGroupInput')
            gInput.label = 'Group Input'
            gInput.name = 'Group Input'
            gInput.location = Vector((-1500, -400))

            gInput.outputs.new(name='Vector', type='Vector')


            for v in imgNodes:
                
                location = Vector(v[1])
                cur_node = workNodeTree.nodes.new(v[0])
                cur_node.location = location
                cur_node.label = v[2]
                cur_node.name = v[2]
                cur_node.show_preview = True
                cur_node.projection = 'FLAT'
                cur_node.color_space = v[4]
                

                #test conditional output socket creation
                findImageFile = FindMapType(sce.filePath, mapSuf[v[5]],getSelecteGroupName)

                if findImageFile != 'NOFILEFOUND':
                    #connect image node output to group output socket
                    workNodeTree.outputs.new('NodeSocketColor', v[3])
                    output_socket = workNodeTree.nodes[v[2]].outputs['Color']
                    inpNum = workNodeTree.nodes['Group Output'].inputs.find(v[3])
                    input_socket = workNodeTree.nodes['Group Output'].inputs[inpNum]
                    workNodeTree.links.new(output_socket, input_socket)
                    to_node = workNodeTree.nodes[v[2]]
                    input_socket = to_node.inputs['Vector']
                    workNodeTree.links.new(gInput.outputs[0], input_socket)

               
            insAutoGroup = currentMAT.node_tree.nodes.new(type='ShaderNodeGroup')
            insAutoGroup.node_tree = workNodeTree  
            insAutoGroup.label =  newGroupName
            insAutoGroup.name = newGroupName
            insAutoGroup.use_custom_color = True
            insAutoGroup.color =(0.0,0.15,0.32)
            insAutoGroup.width = 300

          
            autoMapNodeTree = workNodeTree

            LoadMaps(sce.filePath, autoMapNodeTree, getSelecteGroupName)

            sce.filePath = ''
        
        return{'FINISHED'}  
        
        





def checkNodes(autoMapNodeTree, folderPath, getSelecteGroupName):
    
 
    inputNodes = autoMapNodeTree.nodes

    srcPath = folderPath 
  
    if srcPath != None:
    
        for n in inputNodes:

            if n.type == 'TEX_IMAGE':


                parseMapPath(n, 'MapDiffuse', mapSuf["DIF"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapNormal', mapSuf["NRM"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapNormalY+', mapSuf["NRMY+"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapReflection', mapSuf["REF"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapBump', mapSuf["BMP"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapTransparency', mapSuf["TRN"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapAO', mapSuf["AO"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapTranslucency', mapSuf["TRL"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapEmission', mapSuf["EMS"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapDisplacement', mapSuf["DSP"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapSSS', mapSuf["SSS"], srcPath, autoMapNodeTree, getSelecteGroupName)
                parseMapPath(n, 'MapSpecular', mapSuf["SPC"], srcPath, autoMapNodeTree, getSelecteGroupName)

               



def parseMapPath(n, mapName, mapSuf, srcPath, autoMapNodeTree, getSelecteGroupName):
    if n.label == mapName:
        imgName = FindMapType(srcPath, mapSuf, getSelecteGroupName)
        
        if(imgName!='NOFILEFOUND'):
            imgPath = srcPath + imgName 
            checkImage(n,imgName,imgPath, autoMapNodeTree, True)
        else: 
            checkImage(n,"", "", autoMapNodeTree, False)




def checkImage(n,imgName,imgPath, autoMapNodeTree, imageExists):
  

    if imageExists == True:
      
        # try:
        realpath = os.path.expanduser(imgPath)
        img = bpy.data.images.load(realpath)
        n.image = img


        for v in imgNodes:
            
            if v[2] == n.label:

                inpNum = autoMapNodeTree.nodes['Group Output'].inputs.find(v[3])
  
                if inpNum == -1:

                    autoMapNodeTree.outputs.new('NodeSocketColor', v[3])
                    output_socket = autoMapNodeTree.nodes[v[2]].outputs['Color']
                    inpNum = autoMapNodeTree.nodes['Group Output'].inputs.find(v[3])
                    input_socket = autoMapNodeTree.nodes['Group Output'].inputs[inpNum]
                    autoMapNodeTree.links.new(output_socket, input_socket)
                     
        # except:
        #     raise NameError("Cannot load image %s" % realpath)

   
    else:

         for v in imgNodes:
            
            if v[2] == n.label:

                inpNum = autoMapNodeTree.nodes['Group Output'].inputs.find(v[3])
                outpNum = autoMapNodeTree.nodes['Group Output'].outputs.find(v[3])
              
            
                if inpNum > -1:
                    input_socket = autoMapNodeTree.nodes['Group Output'].inputs[inpNum]
                    
                    autoMapNodeTree.outputs.remove(autoMapNodeTree.outputs[v[3]])


    
            
    



    
def register():

    bpy.utils.register_class(OBJECT_OT_LoadMaps) 
    bpy.utils.register_class(OBJECT_OT_GenImgNodes) 
    bpy.utils.register_class(AutoMapsPanel)
    bpy.utils.register_class(OBJECT_OT_UpdateImgNodes)
    bpy.utils.register_class(OBJECT_OT_RefreshImgNodes)
    bpy.utils.register_class(SelectTextureFolder_OT)
   

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_LoadMaps)
    bpy.utils.unregister_class(OBJECT_OT_GenImgNodes)
    bpy.utils.unregister_class(AutoMapsPanel)
    bpy.utils.unregister_class(OBJECT_OT_UpdateImgNodes)
    bpy.utils.unregister_class(OBJECT_OT_RefreshImgNodes)
    bpy.utils.unregister_class(SelectTextureFolder_OT)
    

if __name__ == "__main__":
    register()



