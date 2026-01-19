# BRepBodies.add Method

Parent Object: [BRepBodies](BRepBodies.md)  

## Description

Creates a new BRepBody object. The input can be a persisted or transient BRepBody and the result is a persisted BRepBody. In a direct modeling design, the BRepBody is created within the component the BRepBodies collection was obtained from. In a parametric modeling design, the new BRepBody is created within the specified Base Feature.  

Because of a current limitation, if you want to create a BRepBody in a parametric model, you must first call the edit method of the base feature, then use the add method to create the body, and finally call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it.

## Syntax

"bRepBodies_var" is a variable referencing a [BRepBodies](BRepBodies.md) object.

```python
# Uses no optional arguments.
returnValue = bRepBodies_var.add(body)

# Uses optional arguments.
returnValue = bRepBodies_var.add(body, targetBaseFeature)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the newly created BRepBody or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| body | [BRepBody](BRepBody.md) | The input BRepBody. Typically this is a transient BRepBody but that's not a requirement. In any case, there is not any association back to the original BRepBody. |
| targetBaseFeature | [BaseFeature](BaseFeature.md) | The BaseFeature object that this BRep body will be associated with. This is an optional requirement. It is required in a parametric modeling design but is ignored in a direct modeling design. This is an optional argument whose default value is null. |

## Version

Introduced in version May 2016  

