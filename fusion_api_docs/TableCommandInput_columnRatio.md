# TableCommandInput.columnRatio Property

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Gets and sets the width ratio of the columns. This is defined using a string such as "1:1:1" where this defines that the first three columns are all the same width. A value of "2:1" defines that the first column is twice the width of the second.  

If the table has more columns than are defined by this property, they will automatically default to a value of 1. If this property defines the width of more columns than are displayed, the extra definitions are ignored.  

You can also specify 0 as a column width and this will have the effect of hiding that column. Setting a column width to 0 does not delete the column or the command inputs but only hides them so they can be turned back on at a later time by resetting the column ratio.

## Syntax

"tableCommandInput_var" is a variable referencing a TableCommandInput object.  

```python
# Get the value of the property.
propertyValue = tableCommandInput_var.columnRatio

# Set the value of the property.
tableCommandInput_var.columnRatio = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2016  

