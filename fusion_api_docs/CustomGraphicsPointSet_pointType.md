# CustomGraphicsPointSet.pointType Property

Parent Object: [CustomGraphicsPointSet](CustomGraphicsPointSet.md)  

## Description

Specifies which of the predefined point images to use. Attempting to set this property to UserDefinedCustomGraphicsPointType will fail. To change to a user defined point type you must set use the pointImage property to specify the image to use and this will have the side-effect of changing the value of this property to UserDefinedCustomGraphicsPointType.

## Syntax

"customGraphicsPointSet_var" is a variable referencing a CustomGraphicsPointSet object.  

```python
# Get the value of the property.
propertyValue = customGraphicsPointSet_var.pointType

# Set the value of the property.
customGraphicsPointSet_var.pointType = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsPointTypes](CustomGraphicsPointTypes.md).

## Version

Introduced in version September 2017  

