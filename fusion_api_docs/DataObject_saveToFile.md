# DataObject.saveToFile Method

Parent Object: [DataObject](DataObject.md)  

## Description

Saves the data represented by the DataObject to a file.

## Syntax

"dataObject_var" is a variable referencing a [DataObject](DataObject.md) object.

```python
returnValue = dataObject_var.saveToFile(filename)
```

## Return Value

| Type    | Description                              |
|---------|------------------------------------------|
| boolean | Returns true if the save was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The full filename to save the file to. This includes the full path and the filename. The folder must already exist and you are responsible for specifying the correct extension to match the file type. |

## Version

Introduced in version September 2024  

