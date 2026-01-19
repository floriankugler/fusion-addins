# FilletEdgeSets Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing fillet edge sets associated with a fillet feature.

## Methods

| Name | Description |
| --- | --- |
| [addAsymmetricRadiusEdgeSet](FilletEdgeSets_addAsymmetricRadiusEdgeSet.md) | Adds an asymmetric fillet edge set to the fillet feature. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [addChordLengthEdgeSet](FilletEdgeSets_addChordLengthEdgeSet.md) | Adds a set of edges with a chord length to this fillet feature. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [addConstantRadiusEdgeSet](FilletEdgeSets_addConstantRadiusEdgeSet.md) | Adds a set of edges with a constant radius to this fillet feature. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [addVariableRadiusEdgeSet](FilletEdgeSets_addVariableRadiusEdgeSet.md) | Adds a single edge or set of tangent edges along with variable radius information to this fillet feature. To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [classType](FilletEdgeSets_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](FilletEdgeSets_item.md) | Function that returns the specified fillet edge set using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](FilletEdgeSets_count.md) | The number of fillet edge sets in the collection. |
| [isValid](FilletEdgeSets_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FilletEdgeSets_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[FilletFeature.edgeSets](FilletFeature_edgeSets.md)

## Samples

| Name | Description |  |
| --- | --- | --- |
| [Fillet Feature Edit API Sample](FilletFeatureEditSample_Sample.md) | Demonstrates editing a fillet feature. To successfully run this sample you can use this [Version Introduced in version November 2014](../ExtraFiles/APISampleFilletEdgeSetData.f3d%3E%20file%3C/a%3E%20or%20create%20a%20new%20model%20with%20the%20described%20fillet%20feature.%3C/p%3E%0A%20%20%20%20%3Cp%3E%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20new%20model%20and%20add%20a%20block%20feature.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20single%20fillet%20feature%20that%20defines%20three%20different%20fillets.%20The%20fillets%20need%20to%20be%20created%20in%20a%20way%20where%20they%20don't%20interact%20with%20one%20another.%20The%20easiest%20way%20is%20to%20create%20the%20fillets%20only%20on%20the%20vertical%20edges%20of%20the%20box.%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20constant%20radius%20fillet%20with%20a%20radius%20that%20is%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20chord%20length%20fillet%20whose%20radius%20is%20also%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20variable%20radius%20fillet%20with%20one%20intermediate%20radius%20and%20the%20radii%20are%20about%201/4%20the%20size%20of%20the%20box%20and%20less.%3C/li%3E%0A%20%20%20%20%3C/ol%3E%0A%3C/ol%3E%0ARunning%20the%20sample%20script%20will%20modify%20various%20settings%20of%20each%20fillet%20and%20change%20the%20edge%20each%20fillet%20is%20applied%20to.%0A%20%20%20%20%3C/p%3E%3C/td%3E%0A%20%20%20%20%20%20%3C/tr%3E%0A%20%20%20%20%3C/Table%3E%0A%20%20%20%20%3Ch2%20class=) © Copyright 2026 Autodesk, Inc. | Comment on this page.) |

