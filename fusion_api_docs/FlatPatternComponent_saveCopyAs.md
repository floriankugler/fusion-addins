# FlatPatternComponent.saveCopyAs Method

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Performs a Save Copy As on this component. This saves the specified component as a new document in the specified location.

## Syntax

"flatPatternComponent_var" is a variable referencing a [FlatPatternComponent](FlatPatternComponent.md) object.

```python
returnValue = flatPatternComponent_var.saveCopyAs(name, dataFolder, description, tag)
```

## Return Value

| Type | Description |
|----|----|
| [DataFileFuture](DataFileFuture.md) | Returns a DataFileFuture object that can be used to track the progress of the upload and get the resulting DataFile once it's available on A360. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name to use for the new document. If this is an empty string, Fusion will use the name of the component being saved. |
| dataFolder | [DataFolder](DataFolder.md) | The data folder to save the new document to. |
| description | string | The description string of the document. This can be an empty string. |
| tag | string | The tag string of the document. This can be an empty string. |

## Version

Introduced in version October 2022  

