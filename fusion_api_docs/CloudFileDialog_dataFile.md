# CloudFileDialog.dataFile Property

Parent Object: [CloudFileDialog](CloudFileDialog.md)  

## Description

Gets the DataFile selected by the user in the dialog. This property is used after the ShowOpen method has been called to retrieve the filename specified by the user.  

If ShowOpen was used and isMultiSelectEnabled is true, then this property will only display the first DataFile selected and the dataFiles property should be used instead to retrieved the full list. If ShowSave was used, then only a single DataFile is ever returned.

## Syntax

"cloudFileDialog_var" is a variable referencing a CloudFileDialog object.  

```python
# Get the value of the property.
propertyValue = cloudFileDialog_var.dataFile
```

## Property Value

This is a read only property whose value is a [DataFile](DataFile.md).

## Version

Introduced in version October 2022  

