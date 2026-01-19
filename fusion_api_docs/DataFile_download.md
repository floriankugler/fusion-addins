# DataFile.download Method

Parent Object: [DataFile](DataFile.md)  

## Description

Performs a synchronous or asynchronous download of this DataFile. Only DataFiles that represent non-Fusion data can be downloaded. For example, this will work for TXT or XLS files but will fail for F3D files.  

When using this in its synchronous mode, Fusion is frozen during the download and the call will not return until the download is complete or has failed. When using this in its asynchronous mode, calling this method will start the download process and the call return before the download is complete. The event on the provided handler will be called notifying you when the download is complete.

## Syntax

"dataFile_var" is a variable referencing a [DataFile](DataFile.md) object.

```python
returnValue = dataFile_var.download(path, handler)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns True in synchronous mode if successful. Returns True in asynchronous mode if the download was successfully started. |

## Parameters

| Name | Type | Description |
|----|----|----|
| path | string | The full path and optionally the filename used on the local file system for the file. If the path doesn't exist it will be created. If only a path is specified, the name and file extension associated with the DataFile is used for the filename. You can also specify the full path, including the filename. |
| handler | [DataEventHandler](DataEventHandler.md) | If you want to do an asynchronous download, provide the handler object to be called when this operation is complete. To call the method synchronously, set this argument to null/None. |

## Version

Introduced in version January 2022  

