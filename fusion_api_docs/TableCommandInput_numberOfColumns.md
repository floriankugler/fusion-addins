# TableCommandInput.numberOfColumns Property

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Returns the current number of visible columns displayed. Setting this property has no effect because the number of columns is automatically inferred by the command inputs that have been added to the table. The table automatically adjusts the number of rows displayed so all inputs can be seen.

## Syntax

"tableCommandInput_var" is a variable referencing a TableCommandInput object.  

```python
# Get the value of the property.
propertyValue = tableCommandInput_var.numberOfColumns

# Set the value of the property.
tableCommandInput_var.numberOfColumns = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version September 2016  

