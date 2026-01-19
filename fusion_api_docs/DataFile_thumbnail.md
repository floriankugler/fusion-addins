# DataFile.thumbnail Property

Parent Object: [DataFile](DataFile.md)  

## Description

Starts the process to get the thumbnail image data associated with this DataFile. Because the data exists on the cloud, a DataObjectFuture is returned that you can use to monitor the state of downloading the thumbnail and then getting the image once it is available.  

The data returned is a 256x256 PNG image. For cases where the DataFile does not have an associated thumbnail, the dataObject property of the returned DataObjectFuture will return null and the state property will return 'FailedFutureState'.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.thumbnail
```

## Property Value

This is a read only property whose value is a [DataObjectFuture](DataObjectFuture.md).

## Version

Introduced in version November 2025  

