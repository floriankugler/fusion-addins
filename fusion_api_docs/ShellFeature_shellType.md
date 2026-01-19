# ShellFeature.shellType Property

Parent Object: [ShellFeature](ShellFeature.md)  

## Description

The shell type used when creating a shell. The default value is SharpOffsetShellType.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"shellFeature_var" is a variable referencing a ShellFeature object.  

```python
# Get the value of the property.
propertyValue = shellFeature_var.shellType

# Set the value of the property.
shellFeature_var.shellType = propertyValue
```

## Property Value

This is a read/write property whose value is a [ShellTypes](ShellTypes.md).

## Version

Introduced in version May 2024  

