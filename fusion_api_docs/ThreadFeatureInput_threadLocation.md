# ThreadFeatureInput.threadLocation Property

Parent Object: [ThreadFeatureInput](ThreadFeatureInput.md)  

## Description

Gets and sets which end of the cylinder the thread is measured from when it's not full length. The thread position and length can be measured from either the "low" or "high" end. You can determine the low and high end by using the Cylinder associated with the cylindrical BRepFace the thread is being added to. The BRepFace.geometry which will return a Cylinder object. The axis property of the Cylinder is a vector and the high end of the cylinder is at the far end of the cylinder with respect to the axis vector.  

This property is only used in the case where the isFullLength property is false and is otherwise ignored. It defaults to creating a thread at the high end.

## Syntax

"threadFeatureInput_var" is a variable referencing a ThreadFeatureInput object.  

```python
# Get the value of the property.
propertyValue = threadFeatureInput_var.threadLocation

# Set the value of the property.
threadFeatureInput_var.threadLocation = propertyValue
```

## Property Value

This is a read/write property whose value is a [ThreadLocations](ThreadLocations.md).

## Version

Introduced in version January 2015  

