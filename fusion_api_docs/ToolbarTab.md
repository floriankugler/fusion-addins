# ToolbarTab Object

Derived from: [Base](Base.md) Object  

## Description

Toolbar tabs are the tabs shown in the command toolbar.

## Methods

| Name | Description |
|----|----|
| [activate](ToolbarTab_activate.md) | Activate this toolbar tab. |
| [classType](ToolbarTab_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ToolbarTab_deleteMe.md) | Deletes this tab. Fusion native tabs cannot be deleted. Use the isNative property to determine if this is a native or API created tab. |
| [move](ToolbarTab_move.md) | Move this tab to a different position in the Toolbar in the user interface. |

## Properties

| Name | Description |
| --- | --- |
| [id](ToolbarTab_id.md) | Gets The unique, language independent, ID of this tab. |
| [index](ToolbarTab_index.md) | Gets the position this tab is in within the toolbar. The first tab is at position 0. This value is with respect to the complete list of tabs so this value could be outside of the expected range if you have a collection of tabs associated with a workspace, which is a subset of the entire list of tabs. |
| [isActive](ToolbarTab_isActive.md) | Gets if this toolbar tab is currently active - i.e. displayed. |
| [isNative](ToolbarTab_isNative.md) | Gets if this tab is native to Fusion or was created via the API. |
| [isValid](ToolbarTab_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](ToolbarTab_isVisible.md) | Gets or sets whether this tab is currently being displayed in the user interface. By default, a tab is made visible if it is associated with the active workspace and hidden otherwise. Setting it here will override that default behavior. |
| [name](ToolbarTab_name.md) | Gets or sets the name of the tab as seen in the user interface. |
| [objectType](ToolbarTab_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentUserInterface](ToolbarTab_parentUserInterface.md) | Gets the parent UserInterface object. |
| [productType](ToolbarTab_productType.md) | Returns the name of the product this toolbar tab is associated with. |
| [toolbarPanels](ToolbarTab_toolbarPanels.md) | Gets the collection containing the panels associated with this tab. It's through this collection that you can add new toolbar panels. |

## Accessed From

[ToolbarTabList.item](ToolbarTabList_item.md), [ToolbarTabList.itemById](ToolbarTabList_itemById.md), [ToolbarTabs.add](ToolbarTabs_add.md), [ToolbarTabs.item](ToolbarTabs_item.md), [ToolbarTabs.itemById](ToolbarTabs_itemById.md), [UserInterface.activeToolbarTab](UserInterface_activeToolbarTab.md)

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2019  

