# WorkingModel.designType Property

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Gets and sets the current design type (DirectDesignType or ParametricDesignType) Changing an existing design from ParametricDesignType to DirectDesignType will result in the timeline and all design history being removed and further operations will not be captured in the timeline.

## Syntax

"workingModel_var" is a variable referencing a WorkingModel object.  

```python
# Get the value of the property.
propertyValue = workingModel_var.designType

# Set the value of the property.
workingModel_var.designType = propertyValue
```

## Property Value

This is a read/write property whose value is a [DesignTypes](DesignTypes.md).

## Version

Introduced in version January 2024  

