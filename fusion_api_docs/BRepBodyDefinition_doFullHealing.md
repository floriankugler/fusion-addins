# BRepBodyDefinition.doFullHealing Property

Parent Object: [BRepBodyDefinition](BRepBodyDefinition.md)  

## Description

Specifies if full healing is done when creating the body. This defaults to true and it's highly recommended that you do full healing because it can find and correct problems with the input. If you're sure that the B-Rep definition that you've constructed is correct then you can set this to false to skip the full healing process.

## Syntax

"bRepBodyDefinition_var" is a variable referencing a BRepBodyDefinition object.  

```python
# Get the value of the property.
propertyValue = bRepBodyDefinition_var.doFullHealing

# Set the value of the property.
bRepBodyDefinition_var.doFullHealing = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

