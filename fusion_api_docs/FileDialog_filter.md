# FileDialog.filter Property

Parent Object: [FileDialog](FileDialog.md)  

## Description

Gets or sets the current file name filter string, which determines the choices that appear in the "Save as file type" or "Files of type" box in the dialog box.  

For each filtering option, the filter string contains a description of the filter and the filter pattern as specified in parentheses and separated by semi-colons. Multiple filters are separated by a double semi-colon. These are illustrated below.  

The following is an example of a filter string:  

Text files (\*.txt);;All files (\*.\*)  

You can add several filter patterns to a filter by separating the file types with semicolons, for example:  

Image Files (\*.BMP;\*.JPG;\*.GIF);;All files (\*.\*)

## Syntax

"fileDialog_var" is a variable referencing a FileDialog object.  

```python
# Get the value of the property.
propertyValue = fileDialog_var.filter

# Set the value of the property.
fileDialog_var.filter = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [File Dialog Sample](FileDialogSample_Sample.md) | Demonstrating how to pop up a file dialog and a folder dialog. |
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2014  

