# SetupInput.fixtures Property

Parent Object: [SetupInput](SetupInput.md)  

## Description

An array of models that represent fixtures, where a model can be an Occurrence, BRepBody, or MeshBody.  

The returned array is connected to the SetupInput and can be added to directly without needing to create a new array, populate it, and assign using this property, although, that is supported too.

## Syntax

"setupInput_var" is a variable referencing a SetupInput object.  

```python
# Get the value of the property.
propertyValue = setupInput_var.fixtures

# Set the value of the property.
setupInput_var.fixtures = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Samples

| Name | Description |
| --- | --- |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version April 2023  

