# DataFolder.uploadAssembly Method

Parent Object: [DataFolder](DataFolder.md)  

## Description

Uploads a set of files that represent an assembly There should only be a single top-level assembly file but there can be any number of other files that represent sub-assemblies.

## Remarks

Uploading an assembly is not supported within any of the Command related events. When a command is running, a transaction is open, and uploading files cannot be transacted and, as a result, cannot be contained within a command transaction.

## Syntax

"dataFolder_var" is a variable referencing a [DataFolder](DataFolder.md) object.

```python
returnValue = dataFolder_var.uploadAssembly(filenames)
```

## Return Value

| Type | Description |
|----|----|
| [DataFileFuture](DataFileFuture.md) | The upload process is asynchronous which means that this method will return before the upload process had completed. The returned DataFileFuture object can be used to check on the current state of the upload to determine if it is still uploading, is complete, or has failed. If it is complete the final DataFinal can be retrieved through the DataFileFuture object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filenames | string\[\] | An array of strings that contains the list of all of the files that are part of the assembly. The name of the top-level assembly file must be the first file in the array. |

## Version

Introduced in version March 2015  

