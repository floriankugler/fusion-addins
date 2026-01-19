# FilletEdgeSet.tangencyWeight Property

Parent Object: [FilletEdgeSet](FilletEdgeSet.md)  

## Description

Returns the model parameter that controls the G1 or G2 tangency weight of the fillet. It must be a real value between 0.1 and 2.0 inclusive. You can edit the tangency weight by using the properties on the returned ModelParameter object.

## Syntax

"filletEdgeSet_var" is a variable referencing a FilletEdgeSet object.  

```python
# Get the value of the property.
propertyValue = filletEdgeSet_var.tangencyWeight
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version November 2022  

