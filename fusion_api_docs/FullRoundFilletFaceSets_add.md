# FullRoundFilletFaceSets.add Method

Parent Object: [FullRoundFilletFaceSets](FullRoundFilletFaceSets.md)  

## Description

Adds a set of faces to be filleted to the full round fillet feature.  

When this face set is associated with an existing fillet feature, to use this method you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"fullRoundFilletFaceSets_var" is a variable referencing a [FullRoundFilletFaceSets](FullRoundFilletFaceSets.md) object.

```python
# Uses no optional arguments.
returnValue = fullRoundFilletFaceSets_var.add(centerFace, sideOneFaces, sideTwoFaces)

# Uses optional arguments.
returnValue = fullRoundFilletFaceSets_var.add(centerFace, sideOneFaces, sideTwoFaces, areAutomaticSideFaces)
```

## Return Value

| Type | Description |
|----|----|
| [FullRoundFilletFaceSet](FullRoundFilletFaceSet.md) | Returns the newly created FullRoundFilletFaceSet or null in the case of failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| centerFace | [BRepFace](BRepFace.md) | Input a BRepFace object that specifies the center face to be filleted. When specifying a center face which has tangentially connected faces then all the tangentially connected faces will be filleted automatically. |
| sideOneFaces | BRepFace[] | Input array of BRepFace objects to specify the side one faces. Only one BRepFace object which is adjacent to the center face can be provided if you set areAutomaticSideFaces to true. |
| sideTwoFaces | BRepFace[] | Input array of BRepFace objects to specify the side two faces. Only one BRepFace object which is adjacent to the center face can be provided if you set areAutomaticSideFaces to true. |
| areAutomaticSideFaces | boolean | Optional input boolean that specifies whether the input side faces are used as automatically inferred side faces. It defaults to true, which results in the side faces not being shown in the dialog when the user edits the feature. The same as when the user infers the side faces from the center face selection. When this is set to false, the side faces will be shown in the dialog as if the user had used the side face selection inputs when creating the feature. For the default to apply the input must meet the requirements that one side one face and one side two face is input and those faces are connected to the center face. This is an optional argument whose default value is True. |

## Version

Introduced in version September 2025  

