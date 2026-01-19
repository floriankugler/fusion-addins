# ToolbarControl Object

Derived from: [Base](Base.md) Object  

## Description

The base class for all toolbar controls.

## Methods

| Name | Description |
|----|----|
| [classType](ToolbarControl_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](ToolbarControl_deleteMe.md) | Deletes the ToolbarControl |

## Properties

| Name | Description |
| --- | --- |
| [id](ToolbarControl_id.md) | Gets the unique ID of this control. The ID is unique with respect to the other controls within the same panel, toolbar, or drop-down control. |
| [index](ToolbarControl_index.md) | Gets the position of this control within the list of controls within the panel, toolbar, or drop-down control. |
| [isValid](ToolbarControl_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](ToolbarControl_isVisible.md) | Gets or sets if this control is currently visible. |
| [objectType](ToolbarControl_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](ToolbarControl_parent.md) | Gets the Parent object. When associated with a toolbar (right or left QAT or the NavBar) this returns the parent Toolbar object. When associated with a panel it returns the parent ToolbarPanel object. When associated with a control (DropDownControl) it returns the parent control. |

## Accessed From

[ToolbarControlList.item](ToolbarControlList_item.md), [ToolbarControlList.itemById](ToolbarControlList_itemById.md), [ToolbarControls.item](ToolbarControls_item.md), [ToolbarControls.itemById](ToolbarControls_itemById.md)

## Derived Classes

[CommandControl](CommandControl.md), [DropDownControl](DropDownControl.md), [SeparatorControl](SeparatorControl.md), [SplitButtonControl](SplitButtonControl.md)

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

