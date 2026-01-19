# CustomGraphicsEntity.transform Property

Parent Object: [CustomGraphicsEntity](CustomGraphicsEntity.md)  

## Description

Gets and sets the transform associated with the graphics entity. When a new graphics entity is created its default transform is an identity matrix which results in the graphics entity being displayed in model space using the original coordinate data used to define the entity.

## Syntax

"customGraphicsEntity_var" is a variable referencing a CustomGraphicsEntity object.  

```python
# Get the value of the property.
propertyValue = customGraphicsEntity_var.transform

# Set the value of the property.
customGraphicsEntity_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Samples

| Name | Description |
| --- | --- |
| [Custom Graphics Sample](CustomGraphicsSample_Sample.md) | A sample demonstrating how to create custom graphics entities. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/GraphicsSampleResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2017  

