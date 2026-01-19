# UserInterface.statusMessage Property

Parent Object: [UserInterface](UserInterface.md)  

## Description

Gets and sets the current message displayed in the lower-right corner of the Fusion window. This is useful when displaying progress information to the user for the current process. Set the value to an empty string to remove the message. The lifetime of your message is indeterminant because Fusion uses the same field to display messages.  

If your process is running in the main thread of Fusion, you will need to call adsk.doEvents to give control back to Fusion, so it can update the UI.  

The ProgressBar can also be used as a way to communicate to the user the current progress of a running process.

## Syntax

"userInterface_var" is a variable referencing a UserInterface object.  

```python
# Get the value of the property.
propertyValue = userInterface_var.statusMessage

# Set the value of the property.
userInterface_var.statusMessage = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version May 2024  

