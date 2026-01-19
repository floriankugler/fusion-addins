# UnitsManager Object

Derived from: [Base](Base.md) Object  

## Description

Utility class used to work with Values and control default units. Internal values are held in SI units (e.g. seconds, radians, kg for time, angle, mass) with the exception that all lengths are in cm rather than meter and this affects derived units (e.g. velocity is cm/s, volume is cm^3). Units are specified flexibility via strings (e.g. "cm", "in", "inch", "cm^3", "cm\*cm\*cm", "mph", "mps" "m/s"). Units like length can be defaulted based on the design settings if the user does not explicitly specify units - so "3" can be 3 inches, mm or cm depending on what the design settings are.

## Methods

| Name | Description |
| --- | --- |
| [classType](UnitsManager_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [convert](UnitsManager_convert.md) | Converts a value from one unit to another. The input and output unit specifiers must be compatible. For example, "in" (inches) and "cm" (centimeters) will work because they both define length. So Convert(1.5, "in", "ft") -> 0.125 Convert(1.5, unitsManager.defaultLengthUnits, "cm") -> depends on the current default distance units, with "mm" it gives 0.15 So Convert(1.5, "in", "kg") -> -1 and GetLastError returns ExpressionError (to denote error) So Convert(1, "in", "internalUnits") -> 2.54 So Convert(1, "internalUnits", "in") -> 0.3937... |
| [evaluateExpression](UnitsManager_evaluateExpression.md) | Gets the value (in internal units) of the expression. |
| [formatInternalValue](UnitsManager_formatInternalValue.md) | **RETIRED** Formats the internal value as a string. The output string is formatted using the current unit settings in preferences. The preferences control the number of decimal places, whether units are abbreviated and several other things. FormatInternalValue(1.5, "in") -> "0.591 in" FormatInternalValue(1.5, "in", false) -> "0.591" FormatInternalValue(1.5, "mm", true) -> "15.00 mm" FormatInternalValue(1.5) -> depends on DistanceUnits, might be "15.0 mm" |
| [formatUnits](UnitsManager_formatUnits.md) | Formats the unit according to the user preferences "centimeter" -> "cm" "inch" -> "in" "cm* cm *cm / s" -> , "cm^3 / s" |
| [formatValue](UnitsManager_formatValue.md) | Given a floating point number this method evaluates it as a value of a specific unit type and returns an appropriate string. By default, the current unit settings defined in the user preferences is used, but you can set the method arguments to override the defaults to specify the formatting you want. The input value always uses internal units, which are centimeters for length, radians for angles, and mass is in kilograms. This method is useful whenever you have a value you've gotten from Fusion or computed on your own and need to display it to the user as a string. This method does the conversion and also takes into account the units and the formatting the user has specified in their preferences. Below are some examples of various formatting where the user preferences for general precision is four decimal places, and the angular precision is one decimal place. Also, trailing zeros are set to be hidden and the minimum precision is two decimal places when trailing zeros are turned off. The design units are specified to be "inch". Here, only the value is supplied and the default is to assume the units are the current design length unit and use the preference settings to format it so there are four decimal places shown and the unit name is included. formatValue(1.5) -> "0.5906 in" In this example, an angle is specified by using "deg" as the unit, and the result showing one decimal place, which is what's defined in the user preference, and it shows the unit name. formatValue(0.7853981633974483096, "deg") -> "45.0 deg" This example converts the input value of 1.5 cm to mm where eight decimal places are shown, trailing zeros are shown, and the unit name is shown. The fourth argument of minimum precision is ignored, since it is only used when showTrailing zeros is False. formatValue(1.5, "mm", 8, BooleanOptions.TrueBooleanOption, 0, True) - > "15.00000000 mm" |
| [isValidExpression](UnitsManager_isValidExpression.md) | Checks to see if the given expression is valid. |
| [standardizeExpression](UnitsManager_standardizeExpression.md) | Standardizes the expression in terms of spacing and user preferences. StandardizeExpression("1.5") -> depends on distance units, but with might be "1.5 mm" StandardizeExpression("1.5", "in") -> "1.5 in" StandardizeExpression("1.5 cm + 1.50001 centimeter") -> "1.5 cm + 1.50001 cm" StandardizeExpression("1.5", "m * m * m / s") -> "1.5 m^3 /s" |

## Properties

| Name | Description |
| --- | --- |
| [defaultLengthUnits](UnitsManager_defaultLengthUnits.md) | Returns the unit strings for the current default length unit as specified in preferences. - e.g. "cm" or "in" This is the string that is being used by Fusion to represent the current length unit and is affected by the preference settings that let the user choose whether abbreviations and symbols can be used. This means that inch length units can be returned as inch, in, or ". If you need a consistent way of determining the current length unit, the distanceDisplayUnits of the FusionUnitsManager object returns an enum value. |
| [internalUnits](UnitsManager_internalUnits.md) | Returns a string that represents internal units - i.e. "internalUnits". This can be used when performing conversions via Convert. |
| [isValid](UnitsManager_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](UnitsManager_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [product](UnitsManager_product.md) | Returns the parent Product. |

## Accessed From

[CAM.unitsManager](CAM_unitsManager.md), [Design.unitsManager](Design_unitsManager.md), [Drawing.unitsManager](Drawing_unitsManager.md), [FlatPatternProduct.unitsManager](FlatPatternProduct_unitsManager.md), [Product.unitsManager](Product_unitsManager.md), [WorkingModel.unitsManager](WorkingModel_unitsManager.md)

## Derived Classes

[FusionUnitsManager](FusionUnitsManager.md)

## Samples

| Name | Description |
|----|----|
| [Get Volume of Active Design API Sample](GetsVolumeOfActiveDesign_Sample.md) | Traverses through the active design and totals the volume of every body within the design. |
| [Use inputBox to get value and evaluateExpression to validate it](InputBox_Sample.md) | Uses the UserInterface.inputBox function to get a string from the user and then validates that the strinng entered is a valid expression by using the UnitsManager.evaluateExpression function. |

## Version

Introduced in version August 2014  

