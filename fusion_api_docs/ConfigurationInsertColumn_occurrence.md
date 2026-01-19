# ConfigurationInsertColumn.occurrence Property

Parent Object: [ConfigurationInsertColumn](ConfigurationInsertColumn.md)  

## Description

Returns the occurrence that is associated with this configuration insertion.  

This property returns null when the table being queried was obtained from a DataFile object.

## Syntax

"configurationInsertColumn_var" is a variable referencing a ConfigurationInsertColumn object.  

```python
# Get the value of the property.
propertyValue = configurationInsertColumn_var.occurrence
```

## Property Value

This is a read only property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version January 2024  

