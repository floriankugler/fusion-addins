# SymmetricExtentDefinition.distance Property

Parent Object: [SymmetricExtentDefinition](SymmetricExtentDefinition.md)  

## Description

Returns the current extent distance. If the SymmetricExtentDefinition object has been created statically and isn't associated with a feature this will return a ValueInput object. If the SymmetricExtentDefinition object is obtained from a feature this will return a ModelParameter object. You can use properties of the parameter to edit its value which will result in the feature updating.

## Syntax

"symmetricExtentDefinition_var" is a variable referencing a SymmetricExtentDefinition object.  

```python
# Get the value of the property.
propertyValue = symmetricExtentDefinition_var.distance
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version November 2016  

