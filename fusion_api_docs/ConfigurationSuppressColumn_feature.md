# ConfigurationSuppressColumn.feature Property

Parent Object: [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md)  

## Description

Returns the feature whose suppression state is being controlled by this column. The term "feature" is used broadly and includes anything displayed in the timeline.  

This property returns null when the table being queried was obtained from a DataFile object.

## Syntax

"configurationSuppressColumn_var" is a variable referencing a ConfigurationSuppressColumn object.  

```python
# Get the value of the property.
propertyValue = configurationSuppressColumn_var.feature
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version January 2024  

