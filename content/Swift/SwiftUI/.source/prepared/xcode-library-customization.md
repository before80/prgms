# Xcode library customization

Expose custom views and modifiers in the Xcode library.

## Overview {#Overview}

You can add your custom SwiftUI views and view modifiers to Xcode’s library. This allows anyone developing your app or adopting your framework to access them by clicking the Library button (+) in Xcode’s toolbar. You can select and drag the custom library items into code, just like you would for system-provided items.

![](./images/xcode-library-customization-hero@2x.png)

To add items to the library, create a structure that conforms to the [LibraryContentProvider](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider) protocol and encapsulate any items you want to add as [LibraryItem](https://developer.apple.com/documentation/developertoolssupport/libraryitem) instances. Implement the [views](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider/views) computed property to add library items containing views. Implement the [modifiers(base:)](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider/modifiers(base:)) method to add items containing view modifiers. Xcode harvests items from all of the library content providers in your project as you work, and makes them available to you in its library.

## Creating library items {#Creating-library-items}

- [LibraryContentProvider](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider) — A source of Xcode library and code completion content.
- [LibraryItem](https://developer.apple.com/documentation/developertoolssupport/libraryitem) — A single item to add to the Xcode library.
