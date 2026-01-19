# UserParameters Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the User Parameters within a design and provides methods to create new user parameters.

## Methods

| Name | Description |
| --- | --- |
| [add](UserParameters_add.md) | Adds a new user parameter to the collection. |
| [asArray](UserParameters_asArray.md) | Returns the user parameters in the design as an array. |
| [classType](UserParameters_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [exportUserParameters](UserParameters_exportUserParameters.md) | Function that exports a list of user parameters to a csv file. |
| [importUserParameters](UserParameters_importUserParameters.md) | Function that imports a list of user parameters from a csv file. The format of the csv file is as follows: It must have at least two rows - Header followed by a row of parameter. It must be encoded in UTF8 format. It must contain at least six columns - name, unit, expression, value, comment, and favorite where favorite is either true or false. The columns must only have a comma delimiter. Any locale will work but no thousands. expression column support double quotes. comment can either be single line or multi line. If multi line, it must be in double quotes. Here is an example of a csv file with two rows Name,Unit,Expression,Value,Comments,Favorite p1,mm,32 mm,32,the first parameter,FALSE The function exportUserParameters could be used to see what a csv file looks like. |
| [item](UserParameters_item.md) | Function that returns the specified User Parameter using an index into the collection. |
| [itemByName](UserParameters_itemByName.md) | Function that returns the specified User Parameter using the name of the parameter as it is displayed in the parameters dialog. |

## Properties

| Name | Description |
| --- | --- |
| [count](UserParameters_count.md) | Returns the number of parameters in the collection. |
| [design](UserParameters_design.md) | Returns the design that owns the user parameters collection. |
| [isValid](UserParameters_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](UserParameters_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.userParameters](Design_userParameters.md), [FlatPatternProduct.userParameters](FlatPatternProduct_userParameters.md), [UserParameter.userParameters](UserParameter_userParameters.md), [WorkingModel.userParameters](WorkingModel_userParameters.md)

## Samples

| Name | Description |
|----|----|
| [Set parameters from a csv file and export to STEP](SetParametersFromACsvFileAndExportToSTEP_Sample.md) | Reads data from a .csv file and sets user parameters in the model and then exports the model to STEP. When setting parameters be aware that this sample is setting user parameters. It's also possible to set model parameters but that's not demonstrated here. Also when accessing parameters, it is case sensitive so the names you use in your program much exactly match the names in the model. |

## Version

Introduced in version August 2014  

