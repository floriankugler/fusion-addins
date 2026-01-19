# Workspaces.itemById Method

Parent Object: [Workspaces](Workspaces.md)  

## Description

Returns the Workspace of the specified ID.

## Syntax

"workspaces_var" is a variable referencing a [Workspaces](Workspaces.md) object.

```python
returnValue = workspaces_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [Workspace](Workspace.md) | Returns the specified workspace or null in the case where there isn't a workspace with the specified ID. |

## Parameters

| Name | Type   | Description                     |
|------|--------|---------------------------------|
| id   | string | The ID of the workspace to get. |

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

