# ObjectCollection.createWithArray Method

Parent Object: [ObjectCollection](ObjectCollection.md)  

## Description

Creates a new ObjectCollection that is initialized with the content of the provided array.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.ObjectCollection.createWithArray(array)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns the newly created ObjectCollection or null in the case of failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| array | Base[] | An array of Fusion objects that are used to populate the ObjectCollection. For this method to succeed, getting the input type correct is critical. The term "array" is used generically in the API documentation and describes different things depending on the language being used. When using C++, std::vector is used to input and output a list of items.However, this particular method requires that the content of the vector be of type core.base. If you have a vector of other types, you need to convert it to core.base. The sample below illustrates converting a vector of Occurrence objects into a vector of core.Base objects. std::vector> occArray = rootComp->occurrences()->asArray(); std::vector> occs{ occArray.begin(), occArray.end() }; Ptr objColl = ObjectCollection::createWithArray(occs); When using Python, a Python List or Tuple is used as input. Something not obvious is that when an array is returned from a method or property it's not returned as a standard Python List but is a special API-specific class called "vector". Typically, you don't notice this isn't a List because it supports Python iteration like a List does. Because the createWithArray method requires a standard Python list as input, you need to convert it to a standard list before using it in the createWithArray method. For example, the Occurrences.asArray method returns an "array" of the occurrences, which really returns a vector object of the occurrences. The code below converts the vector into a standard list so it can be used to create an ObjectCollection. occList = list(root.Occurrences.asArray()) objColl = adsk.core.ObjectCollection.craeteWithArray(occList) |

## Samples

| Name | Description |
| --- | --- |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version May 2023  

