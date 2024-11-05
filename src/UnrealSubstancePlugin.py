import tkinter.filedialog  #imports the filedialog module from tkinder to create file dialogs in GUI
from unreal import (ToolMenus,   #Import classes and fuctions from unreal for maninging tool menus
                    ToolMenuContext, #class being imported
                    uclass, #function being imported
                    ufunction, #function being imported
                    ToolMenuEntryScript) #class being imported

import os #Import os module to interact with the operating system 
import sys #Import sys to acces specifc parameters and functions
import importlib #import module to import modules
import tkinter  #imports tkinder aka GUI toolkit for Python

srcPath = os.path.dirname(os.path.abspath(__file__))  #determine the dir of the script and assigns it scrPath
if srcPath not in sys.path:  #if srcPath not included previously
    sys.path.append(srcPath) #adds scrPath to the system path

import UnrealUtilities #imports UnrealUtilities
importlib.reload(UnrealUtilities) #reloads to ensure it's updated

@uclass() #defining class to be used as a class in unreal engine
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):  #creates class
    @ufunction(override=True) #overrides over the exiting class
    def execute(self, context: ToolMenuEntryScript) -> None:  #overrides the execute method
        UnrealUtilities.UnrealUtility().FindBuildMaterial() #execute unreal utility in find or create base material in tool menu


@uclass() #defining class to be used as a class in unreal engine
class LoadMeshEntryScript(ToolMenuEntryScript): #creates class
    @ufunction(override=True) #overrides over the exiting class
    def execute(self, context) -> None: #run class with these parameters
        window = tkinter.Tk() #create a tkinter window
        window.withdraw() #hides tkinter window
        importDir = tkinter.filedialog.askdirectory()  #chose folder using file dialog
        window.destroy() #destroys tkinter window
        UnrealUtilities.UnrealUtility().ImportDromDir(importDir) #using function LoadFromDir from UnrealUtilities

class UnrealSubstancePlugin: #creates class
    def __init__(self): #creates method
        self.submenuName= "UnrealSubstancePlugin" #creates a submenu
        self.submenuLabel= "Unreal Substance Plugin" #names the submenu
        self.CreateMenu() #calls the method during object creation

    def CreateMenu(self): #creates method
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu") #opens level editor in main menu

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}") #checks if there's an existing one
        if existing: #if there is an existing one
            ToolMenus.get().remove_menu(existing.menu_name) #removes the existing menu

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", self.submenuName, self.submenuLabel) #creates a submenu
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript()) #what the button will be called, do, and the function the button has from the script
        self.AddEntryScript("LoadFromDirectory", "Load from Directory", LoadMeshEntryScript()) #adding identifier and explaination to object from load directory entry script
        ToolMenus.get().refresh_all_widgets() #update the UI

    def AddEntryScript(self, name, Label, script: ToolMenuEntryScript):  #creates method
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, Label) #starting menu entry with the name and label of each object within the menu
        script.register_menu_entry() #creates menu entry

UnrealSubstancePlugin() #creates instance nad initialize the menu creation