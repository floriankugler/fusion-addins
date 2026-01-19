# FileDialog.filterIndex Property

Parent Object: [FileDialog](FileDialog.md)  

## Description

Gets or sets the index of the filter currently selected in the file dialog box. Use the FilterIndex property to set which filtering option is shown first to the user. You can also use the value of FilterIndex after showing the file dialog to perform special file operations depending upon the filter chosen. The first item in the filter list is index 0.

## Syntax

"fileDialog_var" is a variable referencing a FileDialog object.  

```python
# Get the value of the property.
propertyValue = fileDialog_var.filterIndex

# Set the value of the property.
fileDialog_var.filterIndex = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Samples

| Name | Description |
|----|----|
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2014  

