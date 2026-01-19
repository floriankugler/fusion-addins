# ToEntityExtentDefinition.offset Property

Parent Object: [ToEntityExtentDefinition](ToEntityExtentDefinition.md)  

## Description

Returns the current offset. If the EntityExtentDefinition object has been created statically and isn't associated with a feature this will return a ValueInput object. If the EntityExtentDefinition object is obtained from a feature this will return a ModelParameter object. You can use properties of the parameter to edit its value which will result in the feature updating.

## Syntax

"toEntityExtentDefinition_var" is a variable referencing a ToEntityExtentDefinition object.  

```python
# Get the value of the property.
propertyValue = toEntityExtentDefinition_var.offset
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version November 2016  

