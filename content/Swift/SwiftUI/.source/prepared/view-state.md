# State modifiers

Access storage and provide child views with configuration data.

## Overview {#Overview}

SwiftUI provides tools for managing data in your app. For example, you can store values and objects in an environment that’s shared among the views in a view hierarchy. Any view that shares the environment — typically all the descendant views of the view that stores the item — can then access the stored item.

For more information about the types that SwiftUI provides to help manage data in your app, see [Model data](../../../datastorage/1-ModelData/).

## Identity {#Identity}

- [tag(_:includeOptional:)](https://developer.apple.com/documentation/swiftui/view/tag(_:includeoptional:)) — Sets the unique tag value of this view.
- [id(_:)](https://developer.apple.com/documentation/swiftui/view/id(_:)) — Binds a view’s identity to the given proxy value.
- [equatable()](https://developer.apple.com/documentation/swiftui/view/equatable()) — Prevents the view from updating its child view when its new value is the same as its old value.

## Environment values {#Environment-values}

- [environment(_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:)) — Places an observable object in the view’s environment.
- [environment(_:_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:_:)) — Sets the environment value of the specified key path to the given value.
- [environmentObject(_:)](https://developer.apple.com/documentation/swiftui/view/environmentobject(_:)) — Supplies an observable object to a view’s hierarchy.
- [transformEnvironment(_:transform:)](https://developer.apple.com/documentation/swiftui/view/transformenvironment(_:transform:)) — Transforms the environment value of the specified key path with the given function.

## Preferences {#Preferences}

- [preference(key:value:)](https://developer.apple.com/documentation/swiftui/view/preference(key:value:)) — Sets a value for the given preference.
- [transformPreference(_:_:)](https://developer.apple.com/documentation/swiftui/view/transformpreference(_:_:)) — Applies a transformation to a preference value.
- [anchorPreference(key:value:transform:)](https://developer.apple.com/documentation/swiftui/view/anchorpreference(key:value:transform:)) — Sets a value for the specified preference key, the value is a function of a geometry value tied to the current coordinate space, allowing readers of the value to convert the geometry to their local coordinates.
- [transformAnchorPreference(key:value:transform:)](https://developer.apple.com/documentation/swiftui/view/transformanchorpreference(key:value:transform:)) — Sets a value for the specified preference key, the value is a function of the key’s current value and a geometry value tied to the current coordinate space, allowing readers of the value to convert the geometry to their local coordinates.
- [onPreferenceChange(_:perform:)](https://developer.apple.com/documentation/swiftui/view/onpreferencechange(_:perform:)) — Adds an action to perform when the specified preference key’s value changes.
- [backgroundPreferenceValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/backgroundpreferencevalue(_:_:)) — Reads the specified preference value from the view, using it to produce a second view that is applied as the background of the original view.
- [backgroundPreferenceValue(_:alignment:_:)](https://developer.apple.com/documentation/swiftui/view/backgroundpreferencevalue(_:alignment:_:)) — Reads the specified preference value from the view, using it to produce a second view that is applied as the background of the original view.
- [overlayPreferenceValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/overlaypreferencevalue(_:_:)) — Reads the specified preference value from the view, using it to produce a second view that is applied as an overlay to the original view.
- [overlayPreferenceValue(_:alignment:_:)](https://developer.apple.com/documentation/swiftui/view/overlaypreferencevalue(_:alignment:_:)) — Reads the specified preference value from the view, using it to produce a second view that is applied as an overlay to the original view.

## Default storage {#Default-storage}

- [defaultAppStorage(_:)](https://developer.apple.com/documentation/swiftui/view/defaultappstorage(_:)) — The default store used by `AppStorage` contained within the view.

## Configuring a model {#Configuring-a-model}

- [modelContext(_:)](https://developer.apple.com/documentation/swiftui/view/modelcontext(_:)) — Sets the model context in this view’s environment.
- [modelContainer(_:)](https://developer.apple.com/documentation/swiftui/view/modelcontainer(_:)) — Sets the model container and associated model context in this view’s environment.
- [modelContainer(for:inMemory:isAutosaveEnabled:isUndoEnabled:onSetup:)](https://developer.apple.com/documentation/swiftui/view/modelcontainer(for:inmemory:isautosaveenabled:isundoenabled:onsetup:)) — Sets the model container in this view for storing the provided model type, creating a new container if necessary, and also sets a model context for that container in this view’s environment.
