# DataFileFuture.dataFile Property

Parent Object: [DataFileFuture](DataFileFuture.md)  

## Description

Returns the DataFile when the upload is complete (uplodeState returns UploadFinished). Returns null if the upload is still running or has failed.

## Syntax

"dataFileFuture_var" is a variable referencing a DataFileFuture object.  

```python
# Get the value of the property.
propertyValue = dataFileFuture_var.dataFile
```

## Property Value

This is a read only property whose value is a [DataFile](DataFile.md).

## Version

Introduced in version March 2015  

