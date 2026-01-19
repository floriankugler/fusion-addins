# FileDialog.showOpen Method

Parent Object: [FileDialog](FileDialog.md)  

## Description

Displays a modal open dialog, allowing the user to select one or more files. The return value can be used to determine if the dialog was canceled without selecting a file. The Filename and Filenames properties can be used to get the selected files.

## Syntax

"fileDialog_var" is a variable referencing a [FileDialog](FileDialog.md) object.

```python
returnValue = fileDialog_var.showOpen()
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

Introduced in version August 2014  

