# ToolbarControls.addSeparator Method

Parent Object: [ToolbarControls](ToolbarControls.md)  

## Description

Adds a separator to the controls in the toolbar, panel, or drop-down.

## Syntax

"toolbarControls_var" is a variable referencing a [ToolbarControls](ToolbarControls.md) object.

```python
# Uses no optional arguments.
returnValue = toolbarControls_var.addSeparator()

# Uses optional arguments.
returnValue = toolbarControls_var.addSeparator(id, positionID, isBefore)
```

## Return Value

| Type | Description |
|----|----|
| [SeparatorControl](SeparatorControl.md) | Returns the newly created separator controls or null if the creation fails. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | Optional unique ID for the control. It must be unique with respect to other controls in this collection. If the default empty string is provided, Fusion will create a unique ID. This is an optional argument whose default value is "". |
| positionID | string | Specifies the reference id of the control to position this separator control relative to. Not setting this value indicates that the separator control will be created at the end of all other controls in toolbar. The isBefore parameter specifies whether to place the control before or after the reference control. This is an optional argument whose default value is "". |
| isBefore | boolean | Specifies whether to place the separator control before or after the reference control specified by the positionID parameter. This argument is ignored is positionID is not specified. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

