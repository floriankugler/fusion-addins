# FilletFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing fillet features in a component and supports the ability to create new fillet features.

## Methods

| Name | Description |
|----|----|
| [add](FilletFeatures_add.md) | Creates a new fillet feature. |
| [addFullRoundFillet](FilletFeatures_addFullRoundFillet.md) | Creates a new full round fillet feature. |
| [addRuleFillet](FilletFeatures_addRuleFillet.md) | Creates a new rule fillet feature. |
| [classType](FilletFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFullRoundFilletInput](FilletFeatures_createFullRoundFilletInput.md) | Creates a FullRoundFilletFeatureInput object. Use properties and methods on this object to define the fillet you want to create and then use the addFullRoundFillet method, passing in the FullRoundFilletFeatureInput object. |
| [createInput](FilletFeatures_createInput.md) | Creates a FilletFeatureInput object. Use properties and methods on this object to define the fillet you want to create and then use the Add method, passing in the FilletFeatureInput object. |
| [createRuleFilletInput](FilletFeatures_createRuleFilletInput.md) | Creates a RuleFilletFeatureInput object. Use properties and methods on this object to define the fillet you want to create and then use the addRuleFillet method, passing in the RuleFilletFeatureInput object. |
| [item](FilletFeatures_item.md) | Function that returns the specified fillet feature using an index into the collection. |
| [itemByName](FilletFeatures_itemByName.md) | Function that returns the specified fillet feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](FilletFeatures_count.md) | The number of fillet features in the collection. |
| [isValid](FilletFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FilletFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.filletFeatures](Features_filletFeatures.md)

## Samples

| Name | Description |  |
| --- | --- | --- |
| [Constant Radius Fillet API Sample](ConstantRadiusFillet_Sample.md) | Creates a constant radius fillet on the selected edge. If there are tangent contiguous edges that will also be included in the fillet. |  |
| [Fillet Feature Edit API Sample](FilletFeatureEditSample_Sample.md) | Demonstrates editing a fillet feature. To successfully run this sample you can use this ../ExtraFiles/APISampleFilletEdgeSetData.f3d%3E%20file%3C/a%3E%20or%20create%20a%20new%20model%20with%20the%20described%20fillet%20feature.%3C/p%3E%0A%20%20%20%20%3Cp%3E%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20new%20model%20and%20add%20a%20block%20feature.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20single%20fillet%20feature%20that%20defines%20three%20different%20fillets.%20The%20fillets%20need%20to%20be%20created%20in%20a%20way%20where%20they%20don't%20interact%20with%20one%20another.%20The%20easiest%20way%20is%20to%20create%20the%20fillets%20only%20on%20the%20vertical%20edges%20of%20the%20box.%0A%20%20%20%20%3Col%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20constant%20radius%20fillet%20with%20a%20radius%20that%20is%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20chord%20length%20fillet%20whose%20radius%20is%20also%20about%201/4%20the%20size%20of%20the%20box.%3C/li%3E%0A%20%20%20%20%3Cli%3ECreate%20a%20variable%20radius%20fillet%20with%20one%20intermediate%20radius%20and%20the%20radii%20are%20about%201/4%20the%20size%20of%20the%20box%20and%20less.%3C/li%3E%0A%20%20%20%20%3C/ol%3E%0A%3C/ol%3E%0ARunning%20the%20sample%20script%20will%20modify%20various%20settings%20of%20each%20fillet%20and%20change%20the%20edge%20each%20fillet%20is%20applied%20to.%0A%20%20%20%20%3C/p%3E%3C/td%3E%0A%20%20%20%20%20%20%3C/tr%3E%0A%20%20%20%20%20%20%3Ctr%3E%0A%20%20%20%20%20%20%20%20%3Ctd%20class=[Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2014  

