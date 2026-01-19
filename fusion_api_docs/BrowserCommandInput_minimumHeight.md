# BrowserCommandInput.minimumHeight Property

Parent Object: [BrowserCommandInput](BrowserCommandInput.md)  

## Description

Gets and sets the minimum height of the browser within the command dialog in pixels. As the user resizes the dialog, the area taken up by the browser will shrink and grow to fit within the defined space. It will never shrink to be less than the minimum height or expand to be larger than the maximum height. If the dialog can't fit the browser at the minimum size a scroll bar will appear for the dialog to allow the user to scroll to access all the inputs in the dialog.

## Syntax

"browserCommandInput_var" is a variable referencing a BrowserCommandInput object.  

```python
# Get the value of the property.
propertyValue = browserCommandInput_var.minimumHeight

# Set the value of the property.
browserCommandInput_var.minimumHeight = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version July 2021  

