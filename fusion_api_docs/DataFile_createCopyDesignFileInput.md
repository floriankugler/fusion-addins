# DataFile.createCopyDesignFileInput Method

Parent Object: [DataFile](DataFile.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new CopyDesignFileInput object that is used to create a copy of a DataFile that represents a Fusion design. You set options on the CopyDesignFileInput object to define the behavior of the copy and call the copyWithInput method passing in the input object to create the copy.

## Syntax

"dataFile_var" is a variable referencing a [DataFile](DataFile.md) object.

```python
returnValue = dataFile_var.createCopyDesignFileInput(folder)
```

## Return Value

| Type | Description |
|----|----|
| [CopyDesignFileInput](CopyDesignFileInput.md) | Returns the created CopyDesignFileInput object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| folder | [DataFolder](DataFolder.md) | The folder where the copied files will be created. |

## Version

Introduced in version May 2024  

