# ConfigurationInsertCell.row Property

Parent Object: [ConfigurationInsertCell](ConfigurationInsertCell.md)  

## Description

Gets and sets which row of the configured design is used for this cell. When setting this property, the row must come from the configured design used by the occurrence associated with the parent column of this cell.

## Syntax

"configurationInsertCell_var" is a variable referencing a ConfigurationInsertCell object.  

```python
# Get the value of the property.
propertyValue = configurationInsertCell_var.row

# Set the value of the property.
configurationInsertCell_var.row = propertyValue
```

## Property Value

This is a read/write property whose value is a [ConfigurationRow](ConfigurationRow.md).

## Version

Introduced in version January 2024  

