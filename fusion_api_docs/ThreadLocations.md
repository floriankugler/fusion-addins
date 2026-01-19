# ThreadLocations Enumerator

## Description

List of the positions of a thread feature when it is not full length.  

## Methods

| Name | Value | Description |
|----|----|----|
| HighEndThreadLocation | 0 | Position thread at the high end of the cylinder. You can determine the high end in the model by using the geometry property of the cylindrical BRepFace object, which will return a Cylinder object. The axis property of the Cylinder is a vector and the high end of the cylinder is at the far end of the cylinder with respect to the axis vector. |
| LowEndThreadLocation | 1 | Position thread at the low end of the cylinder. You can determine the low end in the model by using the geometry property of the cylindrical BRepFace object, which will return a Cylinder object. The axis property of the Cylinder is a vector and the low end of the cylinder is at the near end of the cylinder with respect to the axis vector. |

## Version

Introduced in version January 2015  

