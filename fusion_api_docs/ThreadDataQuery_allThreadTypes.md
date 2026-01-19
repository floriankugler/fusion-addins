# ThreadDataQuery.allThreadTypes Property

Parent Object: [ThreadDataQuery](ThreadDataQuery.md)  

## Description

This method returns an array of all the available thread types (families). The type names are always English. This English name should be used in the other methods that take the type as an input argument. If you need to display the type name to the user, you can use the threadTypeCustomName method To get the localized name.

## Syntax

"threadDataQuery_var" is a variable referencing a ThreadDataQuery object.  

```python
# Get the value of the property.
propertyValue = threadDataQuery_var.allThreadTypes
```

## Property Value

This is a read only property whose value is an array of type string.

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  

