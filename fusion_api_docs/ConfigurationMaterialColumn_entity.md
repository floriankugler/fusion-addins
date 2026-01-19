# ConfigurationMaterialColumn.entity Property

Parent Object: [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md)  

## Description

Returns the Component or BRepBody being modified by this column. This property returns null when the table being queried was obtained from a DataFile object.

## Syntax

"configurationMaterialColumn_var" is a variable referencing a ConfigurationMaterialColumn object.  

```python
# Get the value of the property.
propertyValue = configurationMaterialColumn_var.entity
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version January 2024  

