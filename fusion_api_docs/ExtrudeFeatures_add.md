# ExtrudeFeatures.add Method

Parent Object: [ExtrudeFeatures](ExtrudeFeatures.md)  

## Description

Creates a new extrude feature based on the information defined by the provided ExtrudeFeatureInput object. To create a new extrusion use the createInput function to create a new input object and use the methods and properties on that object to define the required input for an extrusion. Once the information is defined on the input object you can pass it to the Add method to create the extrusion.

## Syntax

"extrudeFeatures_var" is a variable referencing an [ExtrudeFeatures](ExtrudeFeatures.md) object.

```python
returnValue = extrudeFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ExtrudeFeature](ExtrudeFeature.md) | Returns the newly created ExtrudeFeature or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ExtrudeFeatureInput](ExtrudeFeatureInput.md) | The ExtrudeFeatureInput object that specifies the input needed to create a new extrude feature. |

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |
| [extrudeFeatures.add using setOneSideExtent](extrudeFeaturesOneSideExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setOneSideExtent method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the extrusion. |
| [extrudeFeatures.add using setSymmetricExtent](extrudeFeaturesSymmetricExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setSymmetricExtent method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the extrusion. |
| [extrudeFeatures.add using thin extrude](extrudeFeaturesThin_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setThinExtrude method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the thin extrusion. |
| [extrudeFeatures.add using ThroughAllExtent](extrudeFeaturesThroughAllExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the ThroughAllExtent method. |
| [extrudeFeatures.add using setTwoSidesExtent](extrudeFeaturesTwoSidesExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setTwoSidesExtent method. To use this sample have a design open that contains a profile and a body that is positioned away from the profile but is a size where when the profile is extruded it will intersect the body. When you run the script you will be prompted to select the profile that will be used to create the extrusion and the body to extrude to. The extrusion will be created up to the body with an offset and will also be offset from the sketch plane. |
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |

## Version

Introduced in version August 2014  

