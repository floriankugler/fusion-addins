# ToolbarTabs.add Method

Parent Object: [ToolbarTabs](ToolbarTabs.md)  

## Description

Creates a new ToolbarTab. The tab is initially empty. This method appends the tab to the end of the collection.

## Syntax

"toolbarTabs_var" is a variable referencing a [ToolbarTabs](ToolbarTabs.md) object.

```python
returnValue = toolbarTabs_var.add(id, name)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarTab](ToolbarTab.md) | Returns the newly created tab or null in the case the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique id for this tab. The id must be unique with respect to all of the tabs. |
| name | string | The displayed name of this tab. This is the name visible in the user interface. |

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version October 2019  

