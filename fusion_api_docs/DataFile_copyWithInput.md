# DataFile.copyWithInput Method

Parent Object: [DataFile](DataFile.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Executes the copy using the information defined by the provided CopyFileInput.

## Syntax

"dataFile_var" is a variable referencing a [DataFile](DataFile.md) object.

```python
returnValue = dataFile_var.copyWithInput(input)
```

## Return Value

| Type | Description |
|----|----|
| [DataFileFuture](DataFileFuture.md) | The copy process is asynchronous which means that this method will return before the copy process has completed. The returned DataFileFuture object can be used to check on the current state of the copy to determine if it is still copying, is complete, or has failed. If it is complete the new DataFile that was created as a result of the copy can be retrieved through the DataFileFuture object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CopyFileInput](CopyFileInput.md) | The input object is of CopyFileInput object type, based on which our copy behavior will be defined. A CopyDesignFileInput object is created using the DataFile.createCopyDesignFileInput. |

## Version

Introduced in version May 2024  

