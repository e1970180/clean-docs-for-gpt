---
title: "Icons"
description: "Material Design Icons in the Home Assistant frontend"
related:
  - docs: /docs/frontend/
    title: Frontend
  - docs: /dashboards/cards/
    title: Dashboard cards
  - docs: /docs/configuration/customizing-devices/
    title: Customizing entities
  - docs: https://pictogrammers.com/library/mdi/
    title: Material Design Icons
---


  


Home Assistant utilizes the community-driven Material Design Icons (MDI) project for icons in the frontend. The icon library is a superset of the base icon library provided by Google and contains thousands of community-made icons for very specific applications, industries, and use-cases.

## Default icons

Every entity in Home Assistant has a default icon assigned to it. There are way too many to list out here, but you'll see them in your dashboard. You can customize any of your entities to change the icons displayed to you.

## Finding icons

### Icon picker

The most common way you can find icons is by using the icon picker built right into Home Assistant. Select the **Icon** field when customizing an entity and start typing. The list will filter to icons that match your search criteria. You can also scroll through all available icons when the field is empty.


  


{% tip %}
The icon picker will filter by icon name and by aliases applied to the icon by the MDI project. For example, typing "user" will show you most "account"-named icons.
{% endtip %}

For more detailed steps on customizing entities, including their icon, refer to customizing entities.

### Material design icons picker browser extension

The easiest way to browse and find icons outside of Home Assistant is with the official Material Design Icons Picker browser extension. The extension is available for Chrome, Firefox, and Edge and is maintained by the MDI team.


  


{% note %}
Not all icons that appear in the MDI Picker Browser Extension may be available in Home Assistant (yet!). While the browser extension is updated as MDI releases new packages, Home Assistant may lag behind until its next release.
{% endnote %}

### Material design icons on the Pictogrammers website

The last way to browse through available icons is by viewing the library on the Pictogrammers website, https://pictogrammers.com/library/mdi/. Select an icon you'd like to use, then click "Home Assistant" to see an example of its usage.

{% note %}
The Pictogrammers website will always show the latest release of the material design icons library. However, you may find icons that may not yet be available in Home Assistant (yet!). Watch the Home Assistant release notes for announcements on upgrades of the Material Design Icons library.
{% endnote %}

## Suggesting or contributing new icons

Being open-source like Home Assistant, the material design icons library is always accepting suggestions and contributions to expand the library.

{% note %}
Before suggesting or creating a new icon, it is very important that you search the current library and search all issues, open and closed, on their GitHub. Try searching with different terms that might mean the same thing. (e.g. "user", "person", "account")
{% endnote %}

### Suggesting a new icon

If you have an idea for an icon that isn't currently in the library, but are not interested in creating it yourself, open a new icon suggestion.

### Contributing a New Icon

If you want to contribute a new icon to the library, familiarize yourself with the System icons guidelines in the Material Design system. Then create your icon and submit it to the Pictogrammers team for review.

#### Tips for creating new icons

- Really pay attention to Material Design guidelines.
- Keep in mind that icons are meant to be contextual, not literal.
- When it comes to little details, less is more.
- If you're unsure, open an issue on their GitHub. They're more than happy to help you!
- Not all icons make it into the library and that is okay!

### Suggesting an icon alias

Sometimes an icon exists, but you aren't able to find it with the terms you were searching for. If this has ever happened to you, please open an issue with the Pictogrammers team to suggest new aliases that can be added to existing icons.
