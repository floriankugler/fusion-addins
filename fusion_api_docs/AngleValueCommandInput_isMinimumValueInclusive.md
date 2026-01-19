# AngleValueCommandInput.isMinimumValueInclusive Property

Parent Object: [AngleValueCommandInput](AngleValueCommandInput.md)  

## Description

Gets and sets if the value of the input includes the minimum value or is up to the minimum value. For example, if the minimum value is zero and this property is True, the minimum value can be zero. If this is False, the minimum value must be greater than zero. When the minimum value is first defined using the minimumValue property, this property is set to True. The value returned by this property is only meaningful when the hasMinimumValue property returns True.

## Syntax

"angleValueCommandInput_var" is a variable referencing an AngleValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = angleValueCommandInput_var.isMinimumValueInclusive

# Set the value of the property.
angleValueCommandInput_var.isMinimumValueInclusive = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2017  

