# SelectionCommandInput.isFullWidth Property

Parent Object: [SelectionCommandInput](SelectionCommandInput.md)  

## Description

Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs.

## Syntax

"selectionCommandInput_var" is a variable referencing a SelectionCommandInput object.  

```python
# Get the value of the property.
propertyValue = selectionCommandInput_var.isFullWidth

# Set the value of the property.
selectionCommandInput_var.isFullWidth = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2015  

