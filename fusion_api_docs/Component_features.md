# Component.features Property

Parent Object: [Component](Component.md)  

## Description

Returns the collection that provides access to all of the features associated with this component.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.features
```

## Property Value

This is a read only property whose value is a [Features](Features.md).

## Samples

| Name | Description |
|----|----|
| [baseFeatures.add](baseFeatures_add_Sample.md) | Demonstrates the baseFeature.add method. |
| [extrudeFeatures.add using setSymmetricExtent](extrudeFeaturesSymmetricExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setSymmetricExtent method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the extrusion. |
| [extrudeFeatures.add using ThroughAllExtent](extrudeFeaturesThroughAllExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the ThroughAllExtent method. |
| [formFeatures.add](formFeatures_add_Sample.md) | Demonstrates the formFeatures.add method. This creates a new empty form (T-Spline) feature, which you'll see in the timeline. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [moveFeatures.add](moveFeatures_add_Sample.md) | Demonstrates the moveFeatures.add method. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

