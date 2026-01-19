# ProgressDialog.progressValue Property

Parent Object: [ProgressDialog](ProgressDialog.md)  

## Description

Gets and sets the current progress bar value. Progress is determined based on this value relative to the minimum and maximum values. This will update the values displayed in the message string.

## Syntax

"progressDialog_var" is a variable referencing a ProgressDialog object.  

```python
# Get the value of the property.
propertyValue = progressDialog_var.progressValue

# Set the value of the property.
progressDialog_var.progressValue = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Samples

| Name | Description |
|----|----|
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Progress Dialog API Sample](ProgressDialogSample_Sample.md) | Demonstrates how to use progress dialog |

## Version

Introduced in version January 2016  

