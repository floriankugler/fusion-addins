# Arrange3DEnvelopeInput.originYOffset Property

Parent Object: [Arrange3DEnvelopeInput](Arrange3DEnvelopeInput.md)  

## Description

Gets and sets the Y offset of the envelope from the origin of the construction plane. This value defaults to zero.  

This value will become a parameter when the arrangement is created. If the ValueInput is created using a real number it is in centimeters. If you use a string, it is evaluated the same as a value would be in the command dialog and uses the current document units. For example, if the document units are inch and you specific "0.25" it will result in 1/4 inch clearance. Using a string, you can also specify the units as part of the expression, such as "0.25 in + 2 mm". And you can define equations like "PartSize + 2 mm" where "PartSize" is an existing parameter.

## Syntax

"arrange3DEnvelopeInput_var" is a variable referencing an Arrange3DEnvelopeInput object.  

```python
# Get the value of the property.
propertyValue = arrange3DEnvelopeInput_var.originYOffset

# Set the value of the property.
arrange3DEnvelopeInput_var.originYOffset = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2025  

