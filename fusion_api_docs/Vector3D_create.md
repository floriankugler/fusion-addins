# Vector3D.create Method

Parent Object: [Vector3D](Vector3D.md)  

## Description

Creates a 3D vector object. This object is created statically using the Vector3D.create method.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.core.Vector3D.create()

# Uses optional arguments.
returnValue = adsk.core.Vector3D.create(x, y, z)
```

## Return Value

| Type                     | Description             |
|--------------------------|-------------------------|
| [Vector3D](Vector3D.md) | Returns the new vector. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| x | double | The optional x value. This is an optional argument whose default value is 0.0. |
| y | double | The optional y value. This is an optional argument whose default value is 0.0. |
| z | double | The optional z value. This is an optional argument whose default value is 0.0. |

## Samples

| Name | Description |
|----|----|
| [moveFeatures.add](moveFeatures_add_Sample.md) | Demonstrates the moveFeatures.add method. |

## Version

Introduced in version August 2014  

