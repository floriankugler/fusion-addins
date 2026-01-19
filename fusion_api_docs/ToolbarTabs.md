# ToolbarTabs Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to a set of toolbar tabs.

## Methods

| Name | Description |
|----|----|
| [add](ToolbarTabs_add.md) | Creates a new ToolbarTab. The tab is initially empty. This method appends the tab to the end of the collection. |
| [classType](ToolbarTabs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ToolbarTabs_item.md) | Returns the specified toolbar tab using an index into the collection. When iterating by index, the tabs are returned in the same order as they are shown in the user interface. |
| [itemById](ToolbarTabs_itemById.md) | Returns the ToolbarTab at the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](ToolbarTabs_count.md) | Gets the number of ToolbarTabs. |
| [isValid](ToolbarTabs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ToolbarTabs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Workspace.toolbarTabs](Workspace_toolbarTabs.md)

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2019  

