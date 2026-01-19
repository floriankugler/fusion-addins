# ProgressBar.message Property

Parent Object: [ProgressBar](ProgressBar.md)  

## Description

Gets and sets the message to display in the progress bar. The following symbols can be used to display values. "%p" is replaced by the percentage completed. "%v" is replaced by the current value. %m is replaced by the total number of steps. For example, the message "Processing section %v of %m." will result in the message "Processing section 1 of 10." to be displayed if the maximum value is 10 and the current value is 1.  

When a busy bar is displayed, only a simple message is supported and symbols are not supported.  

If your process is running in the main thread of Fusion, you will need to call adsk.doEvents to give control back to Fusion, so it can update the UI.

## Syntax

"progressBar_var" is a variable referencing a ProgressBar object.  

```python
# Get the value of the property.
propertyValue = progressBar_var.message

# Set the value of the property.
progressBar_var.message = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version May 2024  

