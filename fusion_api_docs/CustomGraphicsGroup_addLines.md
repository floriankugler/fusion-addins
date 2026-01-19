# CustomGraphicsGroup.addLines Method

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

Adds a new CustomGraphicsLines entity to this group.

## Syntax

"customGraphicsGroup_var" is a variable referencing a [CustomGraphicsGroup](CustomGraphicsGroup.md) object.

```python
# Uses no optional arguments.
returnValue = customGraphicsGroup_var.addLines(coordinates, indexList, isLineStrip)

# Uses optional arguments.
returnValue = customGraphicsGroup_var.addLines(coordinates, indexList, isLineStrip, lineStripLengths)
```

## Return Value

| Type | Description |
|----|----|
| [CustomGraphicsLines](CustomGraphicsLines.md) | Returns the new CustomGraphicsLines object or null in the case of a failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| coordinates | [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md) | The CustomGraphicsCoordinates object that defines the coordinates of the vertices of the lines. A CustomGraphicsCoordinates object can be created using the static create method of the CustomGraphicsCoordinates class. |
| indexList | integer[] | An array of integers that represent indices into the coordinates to define the order the coordinates are used to draw the lines. If an empty array is provided, the coordinates are used in the order they're provided in the provided CustomGraphicsCoordinates object. |
| isLineStrip | boolean | A boolean indicating if a series of individual lines or a connected set of lines (a line strip) is to be drawn. If individual lines are drawn, (this argument is false), each pair of coordinates defines a single line. If a line strip is drawn, (this argument is true), the first pair of coordinates define the first line and the third coordinate defines a line that connects to the second coordinate. The fourth coordinate creates a line connecting to the third coordinate, and so on. |
| lineStripLengths | integer[] | If isLineStrip is true, this argument is used to define the number of coordinates to use in each line strip. It is an array of integers that defines the number of coordinates for each line strip. For example, if the array [4,10] is input, 4 coordinates are connected for the first line strip and 10 are used to create a second line strip. If an empty array is provided, a single line strip is created. If isLineStrip is False, this argument is ignored. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
| --- | --- |
| [Custom Graphics Sample](CustomGraphicsSample_Sample.md) | A sample demonstrating how to create custom graphics entities. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/GraphicsSampleResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version September 2017  

