# SplitFaceFeatures.createInput Method

Parent Object: [SplitFaceFeatures](SplitFaceFeatures.md)  

## Description

Creates a SplitFaceFeatureInput object. Use properties and methods on this object to define the split face you want to create and then use the Add method, passing in the SplitFaceFeatureInput object.  

A newly created SplitFaceFeatureInput object defaults to creating a split face feature using the "Split with Surface" option. You can use functions on the SplitFaceFeatureInput object to define a different type of split type.

## Syntax

"splitFaceFeatures_var" is a variable referencing a [SplitFaceFeatures](SplitFaceFeatures.md) object.

```python
returnValue = splitFaceFeatures_var.createInput(facesToSplit, splittingTool, isSplittingToolExtended)
```

## Return Value

| Type | Description |
|----|----|
| [SplitFaceFeatureInput](SplitFaceFeatureInput.md) | Returns the newly created SplitFaceFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| facesToSplit | [ObjectCollection](ObjectCollection.md) | Input the faces to be split. The collection can contain one or more faces from solid and/or open bodies. |
| splittingTool | [Base](Base.md) | Input entity(s) that defines the splitting tool. The splitting tool can be a single entity or an ObjectCollection containing solid and/or open bodies, construction planes, faces, or sketch curves that partially or fully intersect the faces that are being split. |
| isSplittingToolExtended | boolean | A boolean value for setting whether or not the splittingTool is to be automatically extended (if possible) so as to completely intersect the faces that are to be split. This is only used when the split type is "split with surface" which is the default type when a new createInput is created. Use functions on the returned SplitFaceFeatureInput to define a different type of split type. |

## Samples

| Name | Description |
|----|----|
| [splitFaceFeatures.add](splitFaceFeatures_add_Sample.md) | Demonstrates the splitFaceFeatures.add method by spliting a face with another intersecting face. |
| [Split Face Feature API Sample](SplitFaceFeatureSample_Sample.md) | Demonstrates creating a new split face feature. |

## Version

Introduced in version June 2015  

