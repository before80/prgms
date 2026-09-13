# Migrating from the Observable Object protocol to the Observable macro

Update your existing app to leverage the benefits of Observation in Swift.

## Overview {#Overview}

Starting with iOS 17, iPadOS 17, macOS 14, tvOS 17, and watchOS 10, SwiftUI provides support for [Observation](https://developer.apple.com/documentation/observation), a Swift-specific implementation of the observer design pattern. Adopting Observation provides your app with the following benefits:

- Tracking optionals and collections of objects, which isn’t possible when using [ObservableObject](https://developer.apple.com/documentation/combine/observableobject).
- Using existing data flow primitives like [State()](https://developer.apple.com/documentation/swiftui/state()) and [Environment](https://developer.apple.com/documentation/swiftui/environment) instead of object-based equivalents such as [StateObject](https://developer.apple.com/documentation/swiftui/stateobject) and [EnvironmentObject](https://developer.apple.com/documentation/swiftui/environmentobject).
- Updating views based on changes to the observable properties that a view’s [body](https://developer.apple.com/documentation/swiftui/view/body-8kl5o) reads instead of any property changes that occur to an observable object, which can help improve your app’s performance.

To take advantage of these benefits in your app, you’ll discover how to replace existing source code that relies on [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) with code that leverages the [Observable()](https://developer.apple.com/documentation/observation/observable()) macro.

> Note: Download this sample to see the migrated version of the sample app. To see the premigrated version, download the sample available in [Monitoring data changes in your app](../1.5-MonitoringModelDataChangesInYourApp/). You can also use the premigrated version to code along with this article.

### Use the Observable macro {#Use-the-Observable-macro}

To adopt [Observation](https://developer.apple.com/documentation/observation) in an existing app, begin by replacing [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) in your data model type with the [Observable()](https://developer.apple.com/documentation/observation/observable()) macro. The [Observable()](https://developer.apple.com/documentation/observation/observable()) macro generates source code at compile time that adds observation support to the type.

```swift
// BEFORE
import SwiftUI

class Library: ObservableObject {
    // ...
}
```

```swift
// AFTER
import SwiftUI

@Observable class Library {
    // ...
}
```

Then remove the [Published](https://developer.apple.com/documentation/combine/published) property wrapper from observable properties. Observation doesn’t require a property wrapper to make a property observable. Instead, the accessibility of the property in relationship to an observer, such as a view, determines whether a property is observable.

```swift
// BEFORE
class Library {
    @Published var books: [Book] = [Book(), Book(), Book()]
}
```

```swift
// AFTER
@Observable class Library {
    var books: [Book] = [Book(), Book(), Book()]
}
```

If you have properties that are accessible to an observer that you don’t want to track, apply the [ObservationIgnored()](https://developer.apple.com/documentation/observation/observationignored()) macro to the property.

### Migrate incrementally {#Migrate-incrementally}

You don’t need to make a wholesale replacement of the [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) protocol throughout your app. Instead, you can make changes incrementally. Start by changing one data model type to use the [Observable()](https://developer.apple.com/documentation/observation/observable()) macro. Your app can mix data model types that use different observation systems. However, SwiftUI tracks changes differently based on the observation system that a data model type uses, `Observable` versus `ObservableObject`.

You may notice slight behavioral differences in your app based on the tracking method. For instance, when tracking as [Observable()](https://developer.apple.com/documentation/observation/observable()), SwiftUI updates a view only when an observable property changes and the view’s [body](https://developer.apple.com/documentation/swiftui/view/body-8kl5o) reads the property directly. The view doesn’t update when observable properties not read by `body` changes. In contrast, a view updates when any published property of an [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) instance changes, even if the view doesn’t read the property that changes, when tracking as `ObservableObject`.

> Note: To learn more about when SwiftUI updates views when observable properties change, see [Managing model data in your app](../1.3-ManagingModelDataInYourApp/).

### Migrate other source code {#Migrate-other-source-code}

The only change made to the sample app so far is to apply the [Observable()](https://developer.apple.com/documentation/observation/observable()) macro to `Library` and remove support for the [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) protocol. The app still uses the [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) data flow primitive like [StateObject](https://developer.apple.com/documentation/swiftui/stateobject) to manage an instance of `Library`. If you were to build and run the app, SwiftUI still updates the views as expected. That’s because data flow property wrappers such as [StateObject](https://developer.apple.com/documentation/swiftui/stateobject) and [EnvironmentObject](https://developer.apple.com/documentation/swiftui/environmentobject) support types that use the [Observable()](https://developer.apple.com/documentation/observation/observable()) macro. SwiftUI provides this support so apps can make source code changes incrementally.

However, to fully adopt [Observation](https://developer.apple.com/documentation/observation), replace the use of [StateObject](https://developer.apple.com/documentation/swiftui/stateobject) with [State()](https://developer.apple.com/documentation/swiftui/state()) after updating your data model type. For example, in the following code the main app structure creates an instance of `Library` and stores it as a `StateObject`. It also adds the `Library` instance to the environment using the [environmentObject(_:)](https://developer.apple.com/documentation/swiftui/view/environmentobject(_:)) modifier.

```swift
// BEFORE
@main
struct BookReaderApp: App {
    @StateObject private var library = Library()

    var body: some Scene {
        WindowGroup {
            LibraryView()
                .environmentObject(library)
        }
    }
}
```

Now that `Library` no longer conforms to [ObservableObject](https://developer.apple.com/documentation/combine/observableobject), the code can change to use [State()](https://developer.apple.com/documentation/swiftui/state()) instead of [StateObject](https://developer.apple.com/documentation/swiftui/stateobject) and to add `library` to the environment using the [environment(_:)](https://developer.apple.com/documentation/swiftui/view/environment(_:)) modifier.

```swift
// AFTER
@main
struct BookReaderApp: App {
    @State private var library = Library()

    var body: some Scene {
        WindowGroup {
            LibraryView()
                .environment(library)
        }
    }
}
```

One more change must happen before `Library` fully adopts [Observation](https://developer.apple.com/documentation/observation). Previously the view `LibraryView` retrieved a `Library` instance from the environment using the [EnvironmentObject](https://developer.apple.com/documentation/swiftui/environmentobject) property wrapper. The new code, however, uses the [Environment](https://developer.apple.com/documentation/swiftui/environment) property wrapper instead.

```swift
// BEFORE
struct LibraryView: View {
    @EnvironmentObject var library: Library

    var body: some View {
        List(library.books) { book in
            BookView(book: book)
        }
    }
}
```

```swift
// AFTER
struct LibraryView: View {
    @Environment(Library.self) private var library
    
    var body: some View {
        List(library.books) { book in
            BookView(book: book)
        }
    }
}
```

### Remove the ObservedObject property wrapper {#Remove-the-ObservedObject-property-wrapper}

To wrap up the migration of the sample app, change the data model type `Book` to support [Observation](https://developer.apple.com/documentation/observation) by removing [ObservableObject](https://developer.apple.com/documentation/combine/observableobject) from the type declaration and apply the [Observable()](https://developer.apple.com/documentation/observation/observable()) macro. Then remove the [Published](https://developer.apple.com/documentation/combine/published) property wrapper from observable properties.

```swift
// BEFORE
class Book: ObservableObject, Identifiable {
    @Published var title = "Sample Book Title"
    
    let id = UUID() // A unique identifier that never changes.
}
```

```swift
// AFTER
@Observable class Book: Identifiable {
    var title = "Sample Book Title"
    
    let id = UUID() // A unique identifier that never changes.
}
```

Next, remove the [ObservedObject](https://developer.apple.com/documentation/swiftui/observedobject) property wrapper from the `book` variable in the `BookView`. This property wrapper isn’t needed when adopting [Observation](https://developer.apple.com/documentation/observation). That’s because SwiftUI automatically tracks any observable properties that a view’s [body](https://developer.apple.com/documentation/swiftui/view/body-8kl5o) reads directly. For example, SwiftUI updates `BookView` when `book.title` changes.

```swift
// BEFORE
struct BookView: View {
    @ObservedObject var book: Book
    @State private var isEditorPresented = false
    
    var body: some View {
        HStack {
            Text(book.title)
            Spacer()
            Button("Edit") {
                isEditorPresented = true
            }
        }
        .sheet(isPresented: $isEditorPresented) {
            BookEditView(book: book)
        }
    }
}
```

```swift
// AFTER
struct BookView: View {
    var book: Book
    @State private var isEditorPresented = false
    
    var body: some View {
        HStack {
            Text(book.title)
            Spacer()
            Button("Edit") {
                isEditorPresented = true
            }
        }
        .sheet(isPresented: $isEditorPresented) {
            BookEditView(book: book)
        }
    }
}
```

However, if a view needs a binding to an observable type, replace [ObservedObject](https://developer.apple.com/documentation/swiftui/observedobject) with the [Bindable](https://developer.apple.com/documentation/swiftui/bindable) property wrapper. This property wrapper provides binding support to an observable type so that views that expect a binding can change an observable property. For instance, in the following code [TextField](https://developer.apple.com/documentation/swiftui/textfield) receives a binding to `book.title`:

```swift
// BEFORE
struct BookEditView: View {
    @ObservedObject var book: Book
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        VStack() {
            TextField("Title", text: $book.title)
                .textFieldStyle(.roundedBorder)
                .onSubmit {
                    dismiss()
                }
                
            Button("Close") {
                dismiss()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

```swift
// AFTER
struct BookEditView: View {
    @Bindable var book: Book
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        VStack() {
            TextField("Title", text: $book.title)
                .textFieldStyle(.roundedBorder)
                .onSubmit {
                    dismiss()
                }
                
            Button("Close") {
                dismiss()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```
