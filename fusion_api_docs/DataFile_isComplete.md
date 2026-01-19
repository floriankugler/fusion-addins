# DataFile.isComplete Property

Parent Object: [DataFile](DataFile.md)  

## Description

Returns if the DataFile is fully processed. This is especially useful when a new file is being saved or uploaded. The initial call to save or upload the file returns when the process has started but processing continues on the cloud. This property will return true when all of the processing has been completed and all information related to the Datafile is now available.

## Syntax

"dataFile_var" is a variable referencing a DataFile object.  

```python
# Get the value of the property.
propertyValue = dataFile_var.isComplete
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2022  

