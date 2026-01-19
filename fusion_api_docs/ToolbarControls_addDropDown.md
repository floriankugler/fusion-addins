# ToolbarControls.addDropDown Method

Parent Object: [ToolbarControls](ToolbarControls.md)  

## Description

Adds a drop-down to the controls in the toolbar, panel, or drop-down. When the drop-down is initially created it will be empty. you can get the associated ToolbarControls object from the DropDownControl to add additional controls to the drop-down.

## Syntax

"toolbarControls_var" is a variable referencing a [ToolbarControls](ToolbarControls.md) object.

```python
# Uses no optional arguments.
returnValue = toolbarControls_var.addDropDown(text, resourceFolder)

# Uses optional arguments.
returnValue = toolbarControls_var.addDropDown(text, resourceFolder, id, positionID, isBefore)
```

## Return Value

| Type | Description |
|----|----|
| [DropDownControl](DropDownControl.md) | Returns the newly created DropDownControl object or null if the creation fails. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| text | string | The text displayed for the drop-down in a menu. For a drop-down in a toolbar this argument is ignored because an icon is used. |
| resourceFolder | string | This argument defines the resource folder that contains the images used for the icon when the drop-down is in a toolbar. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). |
| id | string | Optional unique ID for the control. It must be unique with respect to other controls in this collection. If the default empty string is provided, Fusion will create a unique ID. This is an optional argument whose default value is "". |
| positionID | string | Specifies the reference id of the control to position this control relative to. Not setting this value indicates that the control will be created at the end of all other controls in toolbar. The isBefore parameter specifies whether to place the control before or after the reference control. This is an optional argument whose default value is "". |
| isBefore | boolean | Specifies whether to place the control before or after the reference control specified by the positionID parameter. This argument is ignored is positionID is not specified. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

