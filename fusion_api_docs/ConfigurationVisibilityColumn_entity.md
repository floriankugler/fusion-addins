# ConfigurationVisibilityColumn.entity Property

Parent Object: [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md)  

## Description

Returns the entity whose visibility is being controlled by this column.  

This property returns null when the table being queried was obtained from a DataFile object.

## Syntax

"configurationVisibilityColumn_var" is a variable referencing a ConfigurationVisibilityColumn object.  

```python
# Get the value of the property.
propertyValue = configurationVisibilityColumn_var.entity
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version January 2024  

