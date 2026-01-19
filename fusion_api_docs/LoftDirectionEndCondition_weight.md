# LoftDirectionEndCondition.weight Property

Parent Object: [LoftDirectionEndCondition](LoftDirectionEndCondition.md)  

## Description

Gets the valueInput or Parameter that defines the weight of the loft. If this object was obtained from a LoftFeatureInput object then this will return a valueInput object with the initial value provided. If this object was obtained from an exiting LoftFeature then it returns a Parameter. In the case of a parameter, to change the weight, edit the value of the associated parameter.

## Syntax

"loftDirectionEndCondition_var" is a variable referencing a LoftDirectionEndCondition object.  

```python
# Get the value of the property.
propertyValue = loftDirectionEndCondition_var.weight
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2016  

