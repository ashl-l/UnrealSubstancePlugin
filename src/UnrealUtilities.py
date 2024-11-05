from unreal import ( #Import classes and fuctions from unreal for maninging tool menus
    AssetToolsHelpers, #class being imported
    EditorAssetLibrary, #class being imported
    AssetTools, #class being imported
    Material, #class being imported
    MaterialFactoryNew, #class being imported
    MaterialEditingLibrary, #class being imported
    MaterialExpressionTextureSampleParameter2D as TexSample2D, #class being imported and adding a nickname
    MaterialProperty, #class being imported
    AssetImportTask, #class being imported
    FbxImportUI #class being imported
)

import os #Import os module to interact with the operating system 

class UnrealUtility:  #creates class
    def __init__(self):  #creates method
        self.substanceRooDir='/game/Substance' #creates folder for substance in content drawer
        self.substanceBaseMatName = 'M_SubstanceBase' #creates folder for base material in content drawer
        self.substanceBaseMatPath = self.substanceRooDir + self.substanceBaseMatName # substance base material is in the root dir
        self.substanceTempFolder='/game/Substance/temp' #creates folder for temp in content drawer
        self.baseColorName = "BaseColor" #names the base color
        self.normalName = "Normal" #names the normal map
        self.occRoughnessMetalic = "OclussionRoughnessMetalic" #names the ao, roughness, and metallic

    def GetAssetTools(self)-> AssetTools:  #creates method
        AssetToolsHelpers.get_asset_tools() #

    def ImportDromDir(self, dir): #creates method
        for file in os.listdir(dir): #for the files in the dir
            if ".fbx" in file: #if the file is and fbx
                self.LoadMeshFromPath(os.path.join(dir, file)) #add the found fbx to the file dir path

    def LoadMeshFromPath(self, meshPath): #creates method
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "") #extracting and giving name to the mesh
        importTask = AssetImportTask() #import will be imported into unreal
        importTask.replace_existing = True #if the import alredy exists it will replace it
        importTask.filename = meshPath #name of the import
        importTask.destination_path = '/game/'+ meshName #dir of where the import will be stored in unreal
        importTask.automated = True #import will run automatically
        importTask.save = True #the import will be saved

        fbxImportOption = FbxImportUI() #import Ui of the fbx when fbx is processed
        fbxImportOption.import_mesh = False #enabling the import of the mesh from the fbx file
        fbxImportOption.import_as_skeletal = False # sets the imported assets as a skeleton as false
        fbxImportOption.static_mesh_import_data.combine_meshes = True #when the meshes are imported, it automatically combines them
        importTask.options = fbxImportOption # the imported task is the impoted fbx file

        self.GetAssetTools().import_asset_tasks([importTask]) #using asset tools create objects using import task
        return importTask.get_objects()[0] #returning objects that original pos

    def FindBuildMaterial(self):  #creates method
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath): # checks if base material exists already
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)  #if base material is made return it since it already exists
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.substanceBaseMatName, self.substanceRooDir, Material, MaterialFactoryNew()) 
        baseColor= MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0) #makes a material expression for the base color
        baseColor.set_editor_properties("parameter_name", self.baseColorName) #finds the base color
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) #connects the base color in the material

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400) #makes a material expression for the normal map
        normal.set_editor_property("parameter_name", self.normalName) #finds the normal map
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterial/DefaultNormal")) #uses the textures in unreal mat for normal
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) #connects the normal map in the material

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800) #makes a material expression for the ao, roughness, metallic
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalic) #finds occRoughnessMetalic
        MaterialEditingLibrary.connect_material_expressions(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) #connects ao in  R channel
        MaterialEditingLibrary.connect_material_expressions(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS) #connects roighness in  G channel
        MaterialEditingLibrary.connect_material_expressions(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC) #connects metallic in  B channel

        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat