# Persistent storage

Store data for use across sessions of your app.

## Overview {#Overview}

The operating system provides ways to store data when your app closes, so that when people open your app again later, they can continue working without interruption. The mechanism that you use depends on factors like what and how much you need to store, whether you need serialized or random access to the data, and so on.

![](./images/persistent-storage-hero@2x.png)

You use the same kinds of storage in a SwiftUI app that you use in any other app. For example, you can access files on disk using the [FileManager](https://developer.apple.com/documentation/foundation/filemanager) interface. However, SwiftUI also provides conveniences that make it easier to use certain kinds of persistent storage in a declarative environment. For example, you can use [FetchRequest](https://developer.apple.com/documentation/swiftui/fetchrequest) and [FetchedResults](https://developer.apple.com/documentation/swiftui/fetchedresults) to interact with a Core Data model.

## Saving state across app launches {#Saving-state-across-app-launches}

- [Restoring your app’s state with SwiftUI](4.1-RestoringYourAppSStateWithSwiftui/) — Provide app continuity for users by preserving their current activities.
- [defaultAppStorage(_:)](https://developer.apple.com/documentation/swiftui/view/defaultappstorage(_:)) — The default store used by `AppStorage` contained within the view.
- [AppStorage](https://developer.apple.com/documentation/swiftui/appstorage) — A property wrapper type that reflects a value from `UserDefaults` and invalidates a view on a change in value in that user default.
- [SceneStorage](https://developer.apple.com/documentation/swiftui/scenestorage) — A property wrapper type that reads and writes to persisted, per-scene storage.

## Accessing Core Data {#Accessing-Core-Data}

- [Loading and displaying a large data feed](4.2-LoadingAndDisplayingALargeDataFeed/) — Consume data in the background, and lower memory use by batching imports and preventing duplicate records.
- [managedObjectContext](https://developer.apple.com/documentation/swiftui/environmentvalues/managedobjectcontext)
- [FetchRequest](https://developer.apple.com/documentation/swiftui/fetchrequest) — A property wrapper type that retrieves entities from a Core Data persistent store.
- [FetchedResults](https://developer.apple.com/documentation/swiftui/fetchedresults) — A collection of results retrieved from a Core Data store.
- [SectionedFetchRequest](https://developer.apple.com/documentation/swiftui/sectionedfetchrequest) — A property wrapper type that retrieves entities, grouped into sections, from a Core Data persistent store.
- [SectionedFetchResults](https://developer.apple.com/documentation/swiftui/sectionedfetchresults) — A collection of results retrieved from a Core Data persistent store, grouped into sections.
