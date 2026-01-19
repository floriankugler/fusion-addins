# TableCommandInput.maximumVisibleRows Property

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Gets and sets the maximum number of rows that can be displayed. As rows are added the visible size of the table will grow to show all rows until this maximum number of rows is reached and then a scroll bar will be displayed to allow the user to access all rows. For a new created table, this property defaults to 4.

## Syntax

"tableCommandInput_var" is a variable referencing a TableCommandInput object.  

```python
# Get the value of the property.
propertyValue = tableCommandInput_var.maximumVisibleRows

# Set the value of the property.
tableCommandInput_var.maximumVisibleRows = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version September 2016  

