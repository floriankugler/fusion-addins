# ToolbarTabs.itemById Method

Parent Object: [ToolbarTabs](ToolbarTabs.md)  

## Description

Returns the ToolbarTab at the specified ID.

## Syntax

"toolbarTabs_var" is a variable referencing a [ToolbarTabs](ToolbarTabs.md) object.

```python
returnValue = toolbarTabs_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [ToolbarTab](ToolbarTab.md) | Returns the ToolbarTab of the specified id or null if no tab has the specified id. |

## Parameters

| Name | Type   | Description                                        |
|------|--------|----------------------------------------------------|
| id   | string | The Id of the tab within the collection to return. |

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2019  

