# FileDialog.initialFilename Property

Parent Object: [FileDialog](FileDialog.md)  

## Description

Gets or sets the initial filename displayed when the dialog is first displayed. When a new FileDialog object is created this defaults to an empty string so no initial filename is specified.  

If the showOpen option is used, the file must already exist in the directory specified by the initialDirectory property. If it doesn't exist, the initial filename will not be used.

## Syntax

"fileDialog_var" is a variable referencing a FileDialog object.  

```python
# Get the value of the property.
propertyValue = fileDialog_var.initialFilename

# Set the value of the property.
fileDialog_var.initialFilename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version August 2016  

