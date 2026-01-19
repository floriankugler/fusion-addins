# CloudFileDialog.filename Property

Parent Object: [CloudFileDialog](CloudFileDialog.md)  

## Description

Gets and sets the filename when using the showSave method. If you set this value before using the showSave method, this will display the filename as the default in the dialog, but the user can change it. The default is an empty string, which indicates there is not an initial filename.  

After calling the showSave method, use this property to get the filename the user specified. You can use this in combination with the dataFolder property to know where the user has specified to save the file.

## Syntax

"cloudFileDialog_var" is a variable referencing a CloudFileDialog object.  

```python
# Get the value of the property.
propertyValue = cloudFileDialog_var.filename

# Set the value of the property.
cloudFileDialog_var.filename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version October 2022  

