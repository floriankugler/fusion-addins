# GroupCommandInput.isFullWidth Property

Parent Object: [GroupCommandInput](GroupCommandInput.md)  

## Description

Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs.

## Syntax

"groupCommandInput_var" is a variable referencing a GroupCommandInput object.  

```python
# Get the value of the property.
propertyValue = groupCommandInput_var.isFullWidth

# Set the value of the property.
groupCommandInput_var.isFullWidth = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2015  

