# ProgressBar.progressValue Property

Parent Object: [ProgressBar](ProgressBar.md)  

## Description

Gets and sets the current progress value. This value determines the progress based on this value relative to the minimum and maximum values specified when the progress bar was created. This will also update the values displayed in the message string.  

If your process is running in the main thread of Fusion, you will need to call adsk.doEvents to give control back to Fusion, so it can update the UI.  

This value is ignored when a busy bar is displayed.

## Syntax

"progressBar_var" is a variable referencing a ProgressBar object.  

```python
# Get the value of the property.
propertyValue = progressBar_var.progressValue

# Set the value of the property.
progressBar_var.progressValue = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version May 2024  

