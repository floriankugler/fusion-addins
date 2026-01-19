# CloudFileDialog.dataFiles Property

Parent Object: [CloudFileDialog](CloudFileDialog.md)  

## Description

Gets the DataFiles specified by the user in the dialog. This property is used after the ShowOpen method has been called to retrieve the DataFiles specified by the user.  

If ShowOpen is used and isMultiSelectEnabled is true, the user is able to select more than one file. This property returns all of the files that were selected.

## Syntax

"cloudFileDialog_var" is a variable referencing a CloudFileDialog object.  

```python
# Get the value of the property.
propertyValue = cloudFileDialog_var.dataFiles
```

## Property Value

This is a read only property whose value is an array of type [DataFile](DataFile.md).

## Version

Introduced in version October 2022  

