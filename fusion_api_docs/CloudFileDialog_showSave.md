# CloudFileDialog.showSave Method

Parent Object: [CloudFileDialog](CloudFileDialog.md)  

## Description

Displays a modal save dialog, allowing the user to specify a file. The return value can be used to determine if the dialog was canceled without giving a filename. The filename property can be used to get that file.

## Syntax

"cloudFileDialog_var" is a variable referencing a [CloudFileDialog](CloudFileDialog.md) object.

```python
returnValue = cloudFileDialog_var.showSave()
```

## Return Value

| Type | Description |
|----|----|
| [DialogResults](DialogResults.md) | Returns an enum value indicating which button was clicked on the dialog. |

## Version

Introduced in version October 2022  

