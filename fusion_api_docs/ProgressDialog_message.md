# ProgressDialog.message Property

Parent Object: [ProgressDialog](ProgressDialog.md)  

## Description

Gets and sets the message to display along with the progress bar. The following symbols can be used to display values. "%p" is replaced by the percentage completed. "%v" is replaced by the current value. %m is replaced by the total number of steps. For example, the message "Processing section %v of %m." will result in the message "Processing section 1 of 10." to be displayed if the maximum value is 10 and the current value is 1. Specify an empty string ("") for no message to appear along with the progress panel.

## Syntax

"progressDialog_var" is a variable referencing a ProgressDialog object.  

```python
# Get the value of the property.
propertyValue = progressDialog_var.message

# Set the value of the property.
progressDialog_var.message = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |

## Version

Introduced in version January 2016  

