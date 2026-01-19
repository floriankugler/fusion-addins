# Application.activeDocument Property

Parent Object: [Application](Application.md)  

## Description

Returns the current active document.

## Syntax

"application_var" is a variable referencing an Application object.  

```python
# Get the value of the property.
propertyValue = application_var.activeDocument
```

## Property Value

This is a read only property whose value is a [Document](Document.md).

## Samples

| Name | Description |
|----|----|
| [Generate Setup Sheets API Sample](GenerateSetupSheets_Sample_Sample.md) | Demonstrates generating the setup sheets for an existing toolpath.. |
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |
| [Save and Insert File API Sample](SaveAndInsertSample_Sample.md) | Demonstrates creating save a new file and then inserting it into a design. To use this sample, have a design open that has been saved and run the script. It will create a new design that contains a cylinder, save it to the same folder the active design was saved to, and then insert it into the active design. |

## Version

Introduced in version August 2014  

