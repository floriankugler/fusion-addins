# Design.designType Property

Parent Object: [Design](Design.md)  

## Description

Gets and sets the current design type (DirectDesignType or ParametricDesignType) Changing an existing design from ParametricDesignType to DirectDesignType will result in the timeline and all design history being removed and further operations will not be captured in the timeline.

## Syntax

"design_var" is a variable referencing a Design object.  

```python
# Get the value of the property.
propertyValue = design_var.designType

# Set the value of the property.
design_var.designType = propertyValue
```

## Property Value

This is a read/write property whose value is a [DesignTypes](DesignTypes.md).

## Version

Introduced in version August 2014  

