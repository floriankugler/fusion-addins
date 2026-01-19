# FolderDialog.showDialog Method

Parent Object: [FolderDialog](FolderDialog.md)  

## Description

Displays a modal dialog allowing the user to select a folder. The return value can be used to determine if the dialog was canceled without selecting a folder. the folder property can be used to get the selected folder.

## Syntax

"folderDialog_var" is a variable referencing a [FolderDialog](FolderDialog.md) object.

```python
returnValue = folderDialog_var.showDialog()
```

## Return Value

| Type | Description |
|----|----|
| [DialogResults](DialogResults.md) | Returns an enum value indicating which button was clicked on the dialog. |

## Samples

| Name | Description |
|----|----|
| [File Dialog Sample](FileDialogSample_Sample.md) | Demonstrating how to pop up a file dialog and a folder dialog. |

## Version

Introduced in version September 2017  

