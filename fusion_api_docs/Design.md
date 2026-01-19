# Design Object

Derived from: [Product](Product.md) Object  

## Description

Object that represents an open Fusion design. This derives from the Product base class and adds the Fusion functionality specific to a Design.

## Methods

| Name | Description |
| --- | --- |
| [activateRootComponent](Design_activateRootComponent.md) | Makes the root component the active component in the user interface. This is the same as enabling the radio button next to the root component in the browser. |
| [analyzeInterference](Design_analyzeInterference.md) | Calculates the interference between the input bodies and/or occurrences. |
| [areaProperties](Design_areaProperties.md) | Returns the AreaProperties object that has properties for getting the area, perimeter, centroid, etc for a collection of 2D sketch profiles and/or planar surfaces that all lie on the same plane. |
| [classType](Design_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [computeAll](Design_computeAll.md) | Forces a recompute of the entire design. This is the equivalent of the "Compute All" command. |
| [createConfiguredDesign](Design_createConfiguredDesign.md) | Converts this design into a configured design. The returned ConfigurationTable has a single row and no columns. You can use it to add columns and rows to define the configuration. |
| [createInterferenceInput](Design_createInterferenceInput.md) | Creates an InterferenceInput object. This object collects the entities and options that are used when calculating interference. To analyze interference you first create an InterferenceInput supplying the entities and set any other settings and then provide this object as input to the analyzeInterference method. |
| [deleteEntities](Design_deleteEntities.md) | Deletes the specified set of entities that are associated with this product. |
| [findAttributes](Design_findAttributes.md) | Find attributes attached to objects in this product that match the group and or attribute name. This does not find attributes attached directly to the Product or Document objects but finds the attributes attached to entities within the product. The search string for both the groupName and attributeName arguments can be either an absolute name value, or a regular expression. With an absolute name, the search string must match the entire groupName or attributeName, including case. An empty string will match everything. For example if you have an attribute group named "MyStuff" that contains the attribute "Length1", using the search string "MyStuff" as the group name and "Length1" as the attribute name will find the attributes with those names. Searching for "MyStuff" as the group name and "" as the attribute name will find all attributes that have "MyStuff" as the group name. Regular expressions provide a more flexible way of searching. To use a regular expression, prefix the input string for the groupName or attributeName arguments with "re:". The regular expression much match the entire group or attribute name. For example if you have a group that contains attributes named "Length1", "Length2", "Width1", and "Width2" and want to find any of the length attributes you can use a regular expression using the string "re:Length.*". For more information on attributes see the Attributes topic in the user manual. |
| [findEntityByToken](Design_findEntityByToken.md) | Returns the entities associated with the provided token. The return is an array of entities. In most cases an array containing a single entity will be returned but there are cases where more than one entity can be returned. An example of this is where a token is obtained from a face and subsequent modeling operations cause the face to be split into two or more pieces. All of the faces that represent the original face will be returned with the first face being the most logical match to the original face. |
| [modifyParameters](Design_modifyParameters.md) | Modifies the values of many parameters all at once. Changing them all at once is more efficient than modifying them one at a time. |
| [physicalProperties](Design_physicalProperties.md) | Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc for a collection of 3D solid objects. |
| [setGroundPlaneOffset](Design_setGroundPlaneOffset.md) | Sets the offset of the ground plane. If the isAdpativeGroundPlane property is true, setting the offset will change isAdaptiveGroundPlane to false. The offset value is an offset relative to the current position of the ground plane. One example of how this method can be used is to set the isAdaptiveGroundPlane property to true, which will position the ground plane at the bottom of the part. By doing this, you know the current position of the ground plane. Then calling this method with a value of -2.0 will reposition the ground plane 2 cm below the part. If you called this method again with a value of -1.0 the ground plane will be moved an additional 1 cm away from the geometry, since this is defining an offset relative to the current position. |

## Properties

| Name | Description |
| --- | --- |
| [activeComponent](Design_activeComponent.md) | Returns the component that is current being edited. This can return the root component or another component within the design. |
| [activeEditObject](Design_activeEditObject.md) | Returns the current edit target as seen in the user interface. This edit target is defined as the container object that will be added to if something is created. For example, a component can be an edit target so that when new bodies are created they are added to that component. A sketch can also be an edit target. |
| [activeOccurrence](Design_activeOccurrence.md) | Returns the occurrence that is currently activated, if any. This can return null in the case where no occurrence is activated and the root component is active. |
| [allComponents](Design_allComponents.md) | Returns the Components collection that provides access to existing components in a design. |
| [allParameters](Design_allParameters.md) | Returns a read only list of all parameters in the design. This includes the user parameters and model parameters from all components in this design. The parameters from Externally Referenced components are NOT included because they are in actuality, separate designs. |
| [analyses](Design_analyses.md) | Gets the collection of design analyses associated with this design. |
| [appearances](Design_appearances.md) | Returns the appearances contained in this document. |
| [attributes](Design_attributes.md) | Returns the collection of attributes associated with this product. |
| [configurationRowId](Design_configurationRowId.md) | Returns the ID of the row that defines this configuration. Use the isConfiguration property to determine if this Design is a configuration or not. If this is not a configuration, this property returns an empty string. |
| [configurationTopTable](Design_configurationTopTable.md) | If this design is a configured design or a configuration, this property returns the associated ConfigurationTopTable object. If this is not a configured design or configuration, this property returns null. |
| [contactSets](Design_contactSets.md) | Returns the contact sets associated with this design. |
| [derivedParameters](Design_derivedParameters.md) | Returns a read only list of all parameters that are derived into the design. This includes the user parameters and model parameters from all derives in this design. |
| [designIntent](Design_designIntent.md) | Gets and sets the use intent of this design. Changing the design intent from one type to another is not supported in all cases. For example, if an assembly contains any external or internal components it cannot be converted to a part. |
| [designPlasticRules](Design_designPlasticRules.md) | Gets the collection of plastic rules in the design. |
| [designSheetMetalRules](Design_designSheetMetalRules.md) | Gets the collection of sheet metal rules in the design. |
| [designType](Design_designType.md) | Gets and sets the current design type (DirectDesignType or ParametricDesignType) Changing an existing design from ParametricDesignType to DirectDesignType will result in the timeline and all design history being removed and further operations will not be captured in the timeline. |
| [exportManager](Design_exportManager.md) | Returns the ExportManager for this design. You use the ExportManager to export the current design in various formats. |
| [fusionUnitsManager](Design_fusionUnitsManager.md) | Returns a specialized UnitsManager that can set the default length units and work with parameters. |
| [isAdaptiveGroundPlane](Design_isAdaptiveGroundPlane.md) | Gets and sets if the position of the ground plane for this design is adaptive. If true, the ground plane will automatically move to be just below the model. The orientation of the ground plane is always normal to the "up" direction as defined by the view cube. |
| [isConfiguration](Design_isConfiguration.md) | Gets if this design is a configuration. If this returns true, the configurationRowId can be used to get the row used to define this configuration. Also, when this is true, the design is essentially read-only and edits are either blocked from taking place or cannot be saved. |
| [isConfiguredDesign](Design_isConfiguredDesign.md) | Gets if this design is a configured design. A configured design contains a configuration table. Use the configurationTable property to get the associated table. |
| [isContactAnalysisEnabled](Design_isContactAnalysisEnabled.md) | Gets and sets whether contact analysis is enabled for all components. This is the equivalent of the "Disable Contact / Enable Contact" command. If this if True then any contact analysis defined (either all or contact sets) is enabled. if False, then no contact analysis is performed. |
| [isContactSetAnalysis](Design_isContactSetAnalysis.md) | Gets and sets whether contact analysis is done using contact sets or between all bodies, independent of any contact sets. If True and the isContactAnalysisEnabled property is True then contact analysis is performed using contact sets. If False and isContactAnalysisEnabled is True, then contact analysis is performed between all bodies. If isContactAnalysisEnabled is False then no contact analysis is performed. |
| [isModelingInAssemblyEnabled](Design_isModelingInAssemblyEnabled.md) | If this design is an assembly, this property gets and sets if the modeling functionality is enabled. If this design is a part or hybrid design, the value of this property should be ignored. |
| [isRootComponentActive](Design_isRootComponentActive.md) | Gets whether the root component is the active edit target in the user interface. This is the same as checking the state of the radio button next to the root component in the browser. To activate the root component use the ActivateRootComponent method. |
| [isValid](Design_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [libraryPlasticRules](Design_libraryPlasticRules.md) | Gets the collection of plastic rules in the plastic rule library. |
| [librarySheetMetalRules](Design_librarySheetMetalRules.md) | Gets the collection of sheet metal rules in the sheet metal rule library. |
| [materials](Design_materials.md) | Returns the materials contained in this document. |
| [namedViews](Design_namedViews.md) | Returns the NamedViews object associated with this product. The NamedViews collection provides access to the named views defined in this product and supports the creation of new named views. |
| [objectType](Design_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [objectVisibility](Design_objectVisibility.md) | Returns the ObjectVisibility object associated with this design which controls which objects are displayed in the graphics window. This is the equivalent of the "Object Visibility" settings in the Display Settings drop-down in the navigation toolbar at the bottom of the Fusion graphics window. |
| [parentDocument](Design_parentDocument.md) | Returns the parent Document object. |
| [productType](Design_productType.md) | Returns the product type name of this product. A list of all of the possible product types can be obtained by using the Application.supportedProductTypes property. |
| [renderManager](Design_renderManager.md) | Returns the RenderManager object associated with this design. Using the RenderManager you can access the same functionality that is available in the Render workspace. |
| [rootComponent](Design_rootComponent.md) | Returns the root Component. |
| [rootDataComponent](Design_rootDataComponent.md) | Get the root DataComponent in this design. This is only available for top level designs. |
| [selectionSets](Design_selectionSets.md) | Returns the SelectionSets object associated with this product. If the product does not support selection sets, null is returned. The SelectionSets object is used to create and access existing selection sets. |
| [snapshots](Design_snapshots.md) | Returns the Snapshots object associated with this design which provides access to the existing snapshots and the creation of new snapshots. |
| [timeline](Design_timeline.md) | Returns the timeline associated with this design. |
| [unitsManager](Design_unitsManager.md) | Returns the UnitsManager object associated with this product. |
| [userParameters](Design_userParameters.md) | Returns the collection of User Parameters in a design |
| [workspaces](Design_workspaces.md) | Returns the workspaces associated with this product. |

## Accessed From

[BaseComponent.parentDesign](BaseComponent_parentDesign.md), [Component.parentDesign](Component_parentDesign.md), [DeriveFeature.sourceDesign](DeriveFeature_sourceDesign.md), [DeriveFeatureInput.sourceDesign](DeriveFeatureInput_sourceDesign.md), [FlatPatternComponent.parentDesign](FlatPatternComponent_parentDesign.md), [FusionDocument.design](FusionDocument_design.md), [FusionUnitsManager.design](FusionUnitsManager_design.md), [PlasticRule.parentDesign](PlasticRule_parentDesign.md), [SheetMetalRule.parentDesign](SheetMetalRule_parentDesign.md), [UserParameter.design](UserParameter_design.md), [UserParameters.design](UserParameters_design.md)

## Derived Classes

[FlatPatternProduct](FlatPatternProduct.md), [WorkingModel](WorkingModel.md)

## Samples

| Name | Description |
|----|----|
| [Analyze Interference API Sample](AnalyzeInterferenceSample_Sample.md) | Demonstrates analyzing the interference between components. This uses a direct modeling design because the ability to create bodies that represent the interference volume is only supported in a direct modeling design. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |
| [Simple Extrusion Sample](SimpleExtrusionSample_Sample.md) | Creates a new extrusion feature, resulting in a new component. |

## Version

Introduced in version August 2014  

