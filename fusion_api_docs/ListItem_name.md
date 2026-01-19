# ListItem.name Property

Parent Object: [ListItem](ListItem.md)  

## Description

Gets or sets the name of this item as displayed in the list. If this control is a separator (isSeparator is true) or it's a button row, setting this property is ignored and getting it will return an empty string.

## Syntax

"listItem_var" is a variable referencing a ListItem object.  

```python
# Get the value of the property.
propertyValue = listItem_var.name

# Set the value of the property.
listItem_var.name = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2015  

