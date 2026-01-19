# CAM.documentToolLibrary Property

Parent Object: [CAM](CAM.md)  

## Description

Gets the document ToolLibrary. The ToolLibrary contains all tools used by any operation inside the document. Changes to the original ToolLibrary will not affect any operation because the document ToolLibrary is an independent copy.

## Syntax

"cAM_var" is a variable referencing a CAM object.  

```python
# Get the value of the property.
propertyValue = cAM_var.documentToolLibrary
```

## Property Value

This is a read only property whose value is a [DocumentToolLibrary](DocumentToolLibrary.md).

## Version

Introduced in version April 2023  

