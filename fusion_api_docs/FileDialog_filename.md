# FileDialog.filename Property

Parent Object: [FileDialog](FileDialog.md)  

## Description

Gets the filename specified by the user in the dialog. This property is used after the ShowOpen or ShowSave methods have been called to retrieve the filename specified by the user. The file name includes both the file path and the extension.  

If ShowOpen was used and IsMultiSelectEnabled is true, then this property will only display the first filename selected and the Filenames property should be used instead to retrieved the full list. Is ShowSave was used, then only a single file name is ever returned.

## Syntax

"fileDialog_var" is a variable referencing a FileDialog object.  

```python
# Get the value of the property.
propertyValue = fileDialog_var.filename
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [File Dialog Sample](FileDialogSample_Sample.md) | Demonstrating how to pop up a file dialog and a folder dialog. |
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2014  

