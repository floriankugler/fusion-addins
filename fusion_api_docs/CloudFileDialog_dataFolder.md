# CloudFileDialog.dataFolder Property

Parent Object: [CloudFileDialog](CloudFileDialog.md)  

## Description

Gets or sets the initial DataFolder displayed in the dialog. The DataFolder should be in current project. If null, this defaults to the DataFolder that is currently active in the Data Panel.  

When using the showSave method, use this property to get the DataFolder that the user specified.

## Syntax

"cloudFileDialog_var" is a variable referencing a CloudFileDialog object.  

```python
# Get the value of the property.
propertyValue = cloudFileDialog_var.dataFolder

# Set the value of the property.
cloudFileDialog_var.dataFolder = propertyValue
```

## Property Value

This is a read/write property whose value is a [DataFolder](DataFolder.md).

## Version

Introduced in version October 2022  

