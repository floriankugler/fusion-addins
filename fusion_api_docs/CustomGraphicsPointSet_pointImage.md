# CustomGraphicsPointSet.pointImage Property

Parent Object: [CustomGraphicsPointSet](CustomGraphicsPointSet.md)  

## Description

Gets and sets the image that will be used to display the point if the point type is a custom image. The image will always be billboarded. The file should be a PNG image and can use transparency. The filename can be a full path or a relative path that is relative to your runtime file. Setting this will automatically set the pointType to UserDefinedCustomGraphicsPointType. This property can also return an empty string in the case where a user defined image point is not being used.

## Syntax

"customGraphicsPointSet_var" is a variable referencing a CustomGraphicsPointSet object.  

```python
# Get the value of the property.
propertyValue = customGraphicsPointSet_var.pointImage

# Set the value of the property.
customGraphicsPointSet_var.pointImage = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2017  

