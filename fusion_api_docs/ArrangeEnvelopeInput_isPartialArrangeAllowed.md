# ArrangeEnvelopeInput.isPartialArrangeAllowed Property

Parent Object: [ArrangeEnvelopeInput](ArrangeEnvelopeInput.md)  

## Description

Gets and sets if a partial arrange is allowed. If true, it will still create a result when there is not enough space on the envelope to fit all of the components. Components are arranged until all the available space is used up. The components that were not included in the partial arrangement are highlighted in the components list. If the envelope size increases, the arrangement recalculates to include the components that did not previously fit in the arrangement.

## Syntax

"arrangeEnvelopeInput_var" is a variable referencing an ArrangeEnvelopeInput object.  

```python
# Get the value of the property.
propertyValue = arrangeEnvelopeInput_var.isPartialArrangeAllowed

# Set the value of the property.
arrangeEnvelopeInput_var.isPartialArrangeAllowed = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

