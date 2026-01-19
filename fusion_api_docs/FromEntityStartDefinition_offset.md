# FromEntityStartDefinition.offset Property

Parent Object: [FromEntityStartDefinition](FromEntityStartDefinition.md)  

## Description

Gets the currently defined offset value. If the FromEntityStartDefinition object was created statically and is not associated with a feature, this will return a ValueInput object. if the FromEntityStartDefinition is associated with an existing feature, this will return the parameter that was created when the feature was created. To edit the offset, use properties on the parameter to change the value of the parameter.

## Syntax

"fromEntityStartDefinition_var" is a variable referencing a FromEntityStartDefinition object.  

```python
# Get the value of the property.
propertyValue = fromEntityStartDefinition_var.offset
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version November 2016  

