# VariableRadiusFilletEdgeSet Object

Derived from: [FilletEdgeSet](FilletEdgeSet.md) Object  

## Description

Provides access to the edges and the parameters associated with a variable radius fillet.

## Methods

| Name | Description |
| --- | --- |
| [addMidPosition](VariableRadiusFilletEdgeSet_addMidPosition.md) | Creates a new mid position radius on the variable radius edge set. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [classType](VariableRadiusFilletEdgeSet_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](VariableRadiusFilletEdgeSet_deleteMe.md) | Deletes the fillet edge set from the fillet. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [deleteMidPosition](VariableRadiusFilletEdgeSet_deleteMidPosition.md) | Deletes the specified mid position from the variable radius fillet. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [continuity](VariableRadiusFilletEdgeSet_continuity.md) | Gets and sets the continuity of the fillet edge set. Valid values are TangentSurfaceContinuityType and CurvatureSurfaceContinuityType. |
| [edges](VariableRadiusFilletEdgeSet_edges.md) | Gets and sets an ObjectCollection containing the edges that are filleted. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [endRadius](VariableRadiusFilletEdgeSet_endRadius.md) | Returns the model parameter that controls the end radius of the fillet. You can edit the end radius by using the properties on the returned ModelParameter object. |
| [isTangentChain](VariableRadiusFilletEdgeSet_isTangentChain.md) | Gets and sets the Tangent chain for fillet. This enables tangent chain option for fillet. |
| [isValid](VariableRadiusFilletEdgeSet_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [midPositions](VariableRadiusFilletEdgeSet_midPositions.md) | Returns a list of model parameters that control the location of each mid point radius. These positions are defined from 0 to 1 where 0 is at the start of the edge and 1 is at the end. You can edit any of these positions by using the properties on its returned ModelParameter object. |
| [midRadii](VariableRadiusFilletEdgeSet_midRadii.md) | Returns a list of model parameters that control radius of the fillet at each position defined along the edge set. You can edit any of these radii by using the properties on its returned ModelParameter object. This list does not include the parameters for the start and end radii. Use the startRadius and endRadius properties to get those. |
| [objectType](VariableRadiusFilletEdgeSet_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [startRadius](VariableRadiusFilletEdgeSet_startRadius.md) | Returns the model parameter that controls the start radius of the fillet. You can edit the start radius by using the properties on the returned ModelParameter object. |
| [tangencyWeight](VariableRadiusFilletEdgeSet_tangencyWeight.md) | Returns the model parameter that controls the G1 or G2 tangency weight of the fillet. It must be a real value between 0.1 and 2.0 inclusive. You can edit the tangency weight by using the properties on the returned ModelParameter object. |

## Accessed From

[FilletEdgeSets.addVariableRadiusEdgeSet](FilletEdgeSets_addVariableRadiusEdgeSet.md)

## Samples

| Name | Description |  |
| --- | --- | --- |
| [Fillet Feature Edit API Sample](FilletFeatureEditSample_Sample.md) | Demonstrates editing a fillet feature. To successfully run this sample you can use this [Version Introduced in version November 2014](../ExtraFiles/APISampleFilletEdgeSetData.f3d%3E%20file%3C/a%3E%20or%20create%20a%20new%20model%20with%20the%20described%20fillet%20feature.%3C/p%3E%0A%20%20%20%20%3Cp%3E%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20new%20model%20and%20add%20a%20block%20feature.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20single%20fillet%20feature%20that%20defines%20three%20different%20fillets.%20The%20fillets%20need%20to%20be%20created%20in%20a%20way%20where%20they%20don't%20interact%20with%20one%20another.%20The%20easiest%20way%20is%20to%20create%20the%20fillets%20only%20on%20the%20vertical%20edges%20of%20the%20box.%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20constant%20radius%20fillet%20with%20a%20radius%20that%20is%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20chord%20length%20fillet%20whose%20radius%20is%20also%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20variable%20radius%20fillet%20with%20one%20intermediate%20radius%20and%20the%20radii%20are%20about%201/4%20the%20size%20of%20the%20box%20and%20less.%3C/li%3E%0A%20%20%20%20%3C/ol%3E%0A%3C/ol%3E%0ARunning%20the%20sample%20script%20will%20modify%20various%20settings%20of%20each%20fillet%20and%20change%20the%20edge%20each%20fillet%20is%20applied%20to.%0A%20%20%20%20%3C/p%3E%3C/td%3E%0A%20%20%20%20%20%20%3C/tr%3E%0A%20%20%20%20%3C/Table%3E%0A%20%20%20%20%3Ch2%20class=) © Copyright 2026 Autodesk, Inc. | Comment on this page.) |

