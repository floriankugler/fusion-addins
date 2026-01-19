# VariableRadiusFilletEdgeSet.tangencyWeight Property

Parent Object: [VariableRadiusFilletEdgeSet](VariableRadiusFilletEdgeSet.md)  

## Description

Returns the model parameter that controls the G1 or G2 tangency weight of the fillet. It must be a real value between 0.1 and 2.0 inclusive. You can edit the tangency weight by using the properties on the returned ModelParameter object.

## Syntax

"variableRadiusFilletEdgeSet_var" is a variable referencing a VariableRadiusFilletEdgeSet object.  

```python
# Get the value of the property.
propertyValue = variableRadiusFilletEdgeSet_var.tangencyWeight
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version November 2022  

