# CustomGraphicsGroup.isChildrenSelectable Property

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Defines if the child custom graphic entities are selectable or if the entire group is selected in the UI. By default this is true. If false, the isSelectable property defines if this group is selectable. If true, the isSelectable property of each child entity defines if it is selectable.

## Syntax

"customGraphicsGroup_var" is a variable referencing a CustomGraphicsGroup object.  

```python
# Get the value of the property.
propertyValue = customGraphicsGroup_var.isChildrenSelectable

# Set the value of the property.
customGraphicsGroup_var.isChildrenSelectable = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2025  

