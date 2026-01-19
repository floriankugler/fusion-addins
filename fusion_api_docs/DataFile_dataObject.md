# DataFile.dataObject Property

Parent Object: [DataFile](DataFile.md)  

## Description

Starts the process to get the raw binary data associated with this DataFile. Because the data exists on the cloud, a DataObjectFuture is returned that you can use to monitor the state of downloading the data and then getting the raw data once it is available.  

Only DataFiles that represent non-Fusion data can accessed. For example, this will work for TXT or XLS files but will fail for F3D files.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.dataObject
```

## Property Value

This is a read only property whose value is a [DataObjectFuture](DataObjectFuture.md).

## Version

Introduced in version September 2024  

