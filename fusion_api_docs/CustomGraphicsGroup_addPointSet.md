# CustomGraphicsGroup.addPointSet Method

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Adds a new CustomGraphicsPointSet entity to this group. This will be displayed as one or more points where all of the points will display using the same image.

## Syntax

"customGraphicsGroup_var" is a variable referencing a [CustomGraphicsGroup](CustomGraphicsGroup.md) object.

```python
returnValue = customGraphicsGroup_var.addPointSet(coordinates, indexList, pointType, pointImage)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsPointSet](CustomGraphicsPointSet.md) | Returns the newly created CustomGraphicsPointSet object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| coordinates | [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md) | The CustomGraphicsCoordinates object that defines the coordinates where the points will be displayed. A CustomGraphicsCoordinates object can be created using the static create method of the CustomGraphicsCoordinates class. |
| indexList | integer\[\] | An array of integers that represent indices into the coordinates to define which coordinates to use when drawing points. If an empty array is provided, a point is drawn for every coordinate. |
| pointType | [CustomGraphicsPointTypes](CustomGraphicsPointTypes.md) | Specifies the type of point to display. Currently there are two choices; UserDefinedCustomGraphicsPointType and PointCloudCustomGraphicsPointType. When set to PointCloudCustomGraphicsPointType, each point displays as a single pixel and is the most efficient point display type for displaying sets that contain very large quantities of points. When set to UserDefinedCustomGraphicsPointType, you specify the image to display as the point. This can be any PNG image and is centered on the point. |
| pointImage | string | If the pointType is PointCloudCustomGraphicsPointType this argument is ignored and can be an empty string. This argument must be specified if the pointType is UserDefinedCustomGraphicsPointType. This is the path to the PNG image file that will be displayed as the point. It can be either a full path to the file or a relative path that is respect to the .py, dll, or dylib file being run. There is no restriction on the size of the image, but generally very small images would be used for points. |

## Samples

| Name | Description |
| --- | --- |
| [Custom Graphics Sample](CustomGraphicsSample_Sample.md) | A sample demonstrating how to create custom graphics entities. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/GraphicsSampleResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2017  

