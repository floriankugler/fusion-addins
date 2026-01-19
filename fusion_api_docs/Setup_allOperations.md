# Setup.allOperations Property

Parent Object: [Setup](Setup.md)  

## Description

Returns an ObjectCollection containing all of the operations in this setup. This includes all operations nested in folders and patterns.

## Syntax

"setup_var" is a variable referencing a Setup object.  

```python
# Get the value of the property.
propertyValue = setup_var.allOperations
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Samples

| Name | Description |
|----|----|
| [Generate Setup Sheets API Sample](GenerateSetupSheets_Sample_Sample.md) | Demonstrates generating the setup sheets for an existing toolpath.. |
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |

## Version

Introduced in version January 2016  

