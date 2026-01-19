# EmbossFeatures.createInput Method

Parent Object: [EmbossFeatures](EmbossFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates an EmbossFeatureInput object. Use properties and methods on this object to define the emboss feature you want to create and then use the Add method, passing in the EmbossFeatureInput object to create the feature.

## Syntax

"embossFeatures_var" is a variable referencing an [EmbossFeatures](EmbossFeatures.md) object.

```python
returnValue = embossFeatures_var.createInput(profiles, faces, depth)
```

## Return Value

| Type | Description |
|----|----|
| [EmbossFeatureInput](EmbossFeatureInput.md) | Returns the newly created EmbossFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| profiles | Base\[\] | An array of Profile objects that define the shape of the emboss. The profile argument can be Profile and SketchText objects. When multiple objects are used, all profiles and sketch texts must be co-planar. |
| faces | BRepFace\[\] | An array of BRepFace objects that define the faces the emboss will be performed on. By default, faces that are tangent to any of the input faces are also used. Use the isTangentChain property on the input object to disable the use of tangent faces. |
| depth | [ValueInput](ValueInput.md) | A ValueInput object that defines the depth of the emboss. A positive value results in the emboss protruding out of the body and a negative value results in the emboss going into the body. |

## Version

Introduced in version September 2025  

