# SilhouetteSelection.silhouetteTolerance Property

Parent Object: [SilhouetteSelection](SilhouetteSelection.md)  

## Description

The distance the silhouette can differ from the model. This helps in creating a silhouette in situations where one cannot be created because of open contours.Generally, the tolerance value you use should be smaller than or equal to the machining tolerance.

## Syntax

"silhouetteSelection_var" is a variable referencing a SilhouetteSelection object.  

```python
# Get the value of the property.
propertyValue = silhouetteSelection_var.silhouetteTolerance

# Set the value of the property.
silhouetteSelection_var.silhouetteTolerance = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version July 2024  

