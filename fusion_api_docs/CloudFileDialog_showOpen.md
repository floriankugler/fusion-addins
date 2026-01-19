# CloudFileDialog.showOpen Method

Parent Object: [CloudFileDialog](CloudFileDialog.md)  

## Description

Displays a modal open dialog, allowing the user to select one or more files. The return value can be used to determine if the dialog was canceled without selecting a file. The dataFile and dataFiles properties can be used to get the selected files.

## Syntax

"cloudFileDialog_var" is a variable referencing a [CloudFileDialog](CloudFileDialog.md) object.

```python
returnValue = cloudFileDialog_var.showOpen()
```

## Return Value

| Type | Description |
|----|----|
| [DialogResults](DialogResults.md) | Returns an enum value indicating which button was clicked on the dialog. |

## Version

Introduced in version October 2022  

