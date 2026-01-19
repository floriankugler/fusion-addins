# Arrange2DPlaneEnvelopeInput.quantity Property

Parent Object: [Arrange2DPlaneEnvelopeInput](Arrange2DPlaneEnvelopeInput.md)  

## Description

Specifies the number of envelopes that can be used. The default value is -1 which means there is no limit.  

This value will become a parameter when the arrangement is created. When created with a real value it must be a whole number. You can also use a string where it is interpreted the same as when entered in the command dialog. The expression must result in a unitless whole number. It's also possible to use an equation like "Total / 4" where "Total" is an existing parameter and be evenly divided by four.

## Syntax

"arrange2DPlaneEnvelopeInput_var" is a variable referencing an Arrange2DPlaneEnvelopeInput object.  

```python
# Get the value of the property.
propertyValue = arrange2DPlaneEnvelopeInput_var.quantity

# Set the value of the property.
arrange2DPlaneEnvelopeInput_var.quantity = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2025  

