# SelectionCommandInput.hasFocus Property

Parent Object: [SelectionCommandInput](SelectionCommandInput.md)  

## Description

Gets and sets if this selection input has focus with respect to other selection inputs on the command dialog. Only one selection input on a dialog can have focus at a time, so setting hasFocus to true will remove the focus from the selection input that previously had focus. When a selection input has focus; any user selections will be added to that selection input, and the selection rules associated with that selection input will apply.  

Setting hasFocus to True for a selection input whose isVisible property is false will fail.

## Syntax

"selectionCommandInput_var" is a variable referencing a SelectionCommandInput object.  

```python
# Get the value of the property.
propertyValue = selectionCommandInput_var.hasFocus

# Set the value of the property.
selectionCommandInput_var.hasFocus = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2016  

