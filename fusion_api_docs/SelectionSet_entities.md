# SelectionSet.entities Property

Parent Object: [SelectionSet](SelectionSet.md)  

## Description

Gets and sets the entities in the selection set. Setting this property is the equivalent of using the "Update" option for a selection set in the user-interface.  

Setting the entities can fail in the case where you provide an entity that is not valid for selection. All entities must be in the context of the root component. This means if the entity isn't directly owned by the root component, it must be a proxy.

## Syntax

"selectionSet_var" is a variable referencing a SelectionSet object.  

```python
# Get the value of the property.
propertyValue = selectionSet_var.entities

# Set the value of the property.
selectionSet_var.entities = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Version

Introduced in version May 2022  

