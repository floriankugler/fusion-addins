# CAM.allOperations Property

Parent Object: [CAM](CAM.md)  

## Description

Gets a collection containing all of the operations in the document. This includes all operations nested in folders and patterns.

## Syntax

"cAM_var" is a variable referencing a CAM object.  

```python
# Get the value of the property.
propertyValue = cAM_var.allOperations
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Samples

| Name | Description |
|----|----|
| [Generate Setup Sheets API Sample](GenerateSetupSheets_Sample_Sample.md) | Demonstrates generating the setup sheets for an existing toolpath.. |
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Create CAM Operation From Template API Sample](New_Operation_Sample_Sample.md) | Demonstrates adding a new toolpath into the document using an existing CAM template. You can view the template [here](../ExtraFiles/face.f3dhsm-template), although it will be loaded automatically. Run the sample script within any Fusion project containing at least one setup. A new facing operation will be created at the end of each setup discovered. |

## Version

Introduced in version January 2016  

