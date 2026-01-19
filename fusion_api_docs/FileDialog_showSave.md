# FileDialog.showSave Method

Parent Object: [FileDialog](FileDialog.md)  

## Description

Displays a modal save dialog, allowing the user to specify a file. The return value can be used to determine if the dialog was canceled without selecting a file. The Filename and Filenames properties can be used to get the selected files.

## Syntax

"fileDialog_var" is a variable referencing a [FileDialog](FileDialog.md) object.

```python
returnValue = fileDialog_var.showSave()
```

## Return Value

| Type | Description |
|----|----|
| [DialogResults](DialogResults.md) | Returns an enum value indicating which button was clicked on the dialog. |

## Samples

| Name | Description |
|----|----|
| [File Dialog Sample](FileDialogSample_Sample.md) | Demonstrating how to pop up a file dialog and a folder dialog. |
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2014  

