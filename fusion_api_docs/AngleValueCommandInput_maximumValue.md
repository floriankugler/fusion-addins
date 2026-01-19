# AngleValueCommandInput.maximumValue Property

Parent Object: [AngleValueCommandInput](AngleValueCommandInput.md)  

## Description

Gets and sets maximum value, if any, that the value can be. The value is in radians. When getting this property you should first check the hasMaximumValue property to see if this property applies. Also, the isMaximumValueInclusive indicates if the minimum includes this value or will be up to this value.  

Setting this value will change the isMaximumValueInclusive to True and the hasMaximumValue property to True if hasMaximumValue is currently False, otherwise it will just update the value.

## Syntax

"angleValueCommandInput_var" is a variable referencing an AngleValueCommandInput object.  

```python
# Get the value of the property.
propertyValue = angleValueCommandInput_var.maximumValue

# Set the value of the property.
angleValueCommandInput_var.maximumValue = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2017  

