# FilletFeatureInput.addConstantRadiusEdgeSet Method

Parent Object: [FilletFeatureInput](FilletFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Adds a set of edges with a constant radius to this input.

## Remarks

This method is obsolete. You should now use the methods on the EdgeSetInputs objects to define new fillets.

## Syntax

"filletFeatureInput_var" is a variable referencing a [FilletFeatureInput](FilletFeatureInput.md) object.

```python
returnValue = filletFeatureInput_var.addConstantRadiusEdgeSet(edges, radius, isTangentChain)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the set of edges was successfully added to the FilletFeatureInput. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edges | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the edges to be filleted. If the isTangentChain argument is true additional edges may also get filleted if they are tangentially connected to any of the input edges. |
| radius | [ValueInput](ValueInput.md) | A ValueInput object that defines the radius of the fillet. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| isTangentChain | boolean | A boolean value for setting whether or not edges that are tangentially connected to the input edges will also be filleted. |

## Version

Introduced in version November 2014  
Retired in version November 2022  

