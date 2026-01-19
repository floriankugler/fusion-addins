# ConstantRadiusFilletEdgeSetInput.tangencyWeight Property

Parent Object: [ConstantRadiusFilletEdgeSetInput](ConstantRadiusFilletEdgeSetInput.md)  

## Description

Gets and sets the tangency weight for the given edge set. The tangency weight controls the influence of the continuity (G1 or G2) on the fillet. The ValueInput must be a real value between 0.1 and 2.0 inclusive, with no units. The default value is 1.0.

## Syntax

"constantRadiusFilletEdgeSetInput_var" is a variable referencing a ConstantRadiusFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = constantRadiusFilletEdgeSetInput_var.tangencyWeight

# Set the value of the property.
constantRadiusFilletEdgeSetInput_var.tangencyWeight = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2022  

