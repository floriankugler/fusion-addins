# VariableRadiusFilletEdgeSetInput.entities Property

Parent Object: [VariableRadiusFilletEdgeSetInput](VariableRadiusFilletEdgeSetInput.md)  

## Description

Gets and sets the entities associated with this fillet edge set. For constant radius and chord length edge sets, this can be edges, faces, and features. For variable radius edges sets, this must be edges.

## Syntax

"variableRadiusFilletEdgeSetInput_var" is a variable referencing a VariableRadiusFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = variableRadiusFilletEdgeSetInput_var.entities

# Set the value of the property.
variableRadiusFilletEdgeSetInput_var.entities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2022  

