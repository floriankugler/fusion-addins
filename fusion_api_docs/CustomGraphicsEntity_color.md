# CustomGraphicsEntity.color Property

Parent Object: [CustomGraphicsEntity](CustomGraphicsEntity.md)  

## Description

Gets and sets the current color definition for this entity. The color of custom graphics can be defined in many ways; solid color, simple material, and appearance.

## Syntax

"customGraphicsEntity_var" is a variable referencing a CustomGraphicsEntity object.  

```python
# Get the value of the property.
propertyValue = customGraphicsEntity_var.color

# Set the value of the property.
customGraphicsEntity_var.color = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsColorEffect](CustomGraphicsColorEffect.md).

## Samples

| Name | Description |
| --- | --- |
| [Custom Graphics Sample](CustomGraphicsSample_Sample.md) | A sample demonstrating how to create custom graphics entities. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/GraphicsSampleResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2017  

