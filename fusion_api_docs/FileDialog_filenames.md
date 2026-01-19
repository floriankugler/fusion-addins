# FileDialog.filenames Property

Parent Object: [FileDialog](FileDialog.md)  

## Description

Gets the filenames specified by the user in the dialog. This property is used after the ShowOpen or ShowSave methods have been called to retrieve the filenames specified by the user. Each file name includes both the file path and the extension.  

If ShowOpen is used and IsMultiSelectEnabled is true, the user is able to select more than one file. This property returns all of the files that were selected. If ShowSave is used or IsMultiSelectEnabled is false then this array will contain the single file name.

## Syntax

"fileDialog_var" is a variable referencing a FileDialog object.  

```python
# Get the value of the property.
propertyValue = fileDialog_var.filenames
```

## Property Value

This is a read only property whose value is an array of type string.

## Samples

| Name | Description |
|----|----|
| [File Dialog Sample](FileDialogSample_Sample.md) | Demonstrating how to pop up a file dialog and a folder dialog. |

## Version

Introduced in version August 2014  

