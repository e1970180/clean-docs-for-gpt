---
title: "Templating"
description: "Instructions on how to use the templating feature of Home Assistant."
---

This is an advanced feature of Home Assistant. You'll need a basic understanding of:

- Home Assistant architecture, especially states.
- The State object.

Templating is a powerful feature that allows you to control information going into and out of the system. It is used for:

- Formatting outgoing messages in, for example, the notify platforms and Alexa integration.
- Process incoming data from sources that provide raw data, like MQTT, `rest` sensor or the `command_line` sensor.
- Automation Templating.

## Building templates

Templating in Home Assistant is powered by the Jinja2 templating engine. This means that we are using their syntax and make some custom Home Assistant variables available to templates during rendering. Jinja2 supports a wide variety of operations:

- Mathematical operation
- Comparisons
- Logic

We will not go over the basics of the syntax, as Jinja2 does a great job of this in their templates documentation.

The frontend has a {% my developer_template title="template editor tool" %} to help develop and debug templates. Navigate to {% my developer_template title="Developer Tools > Template" %}, create your template in the _Template editor_ and check the results on the right.

Templates can get big pretty fast. To keep a clear overview, consider using YAML multiline strings to define your templates:

{% raw %}

```yaml
script:
  msg_who_is_home:
    sequence:
      - action: notify.notify
        data:
          message: >
            {% if is_state('device_tracker.paulus', 'home') %}
              Ha, Paulus is home!
            {% else %}
              Paulus is at {{ states('device_tracker.paulus') }}.
            {% endif %}
```

{% endraw %}

### Important template rules

There are a few very important rules to remember when adding templates to YAML:

1. You **must** surround single-line templates with double quotes (`"`) or single quotes (`'`).
2. It is advised that you prepare for undefined variables by using `if ... is not none` or the `default` filter, or both.
3. It is advised that when comparing numbers, you convert the number(s) to a `float` or an `int` by using the respective filter.
4. While the `float` and `int` filters do allow a default fallback value if the conversion is unsuccessful, they do not provide the ability to catch undefined variables.

Remembering these simple rules will help save you from many headaches and endless hours of frustration when using automation templates.

### Enabled Jinja extensions

Jinja supports a set of language extensions that add new functionality to the language.
To improve the experience of writing Jinja templates, we have enabled the following
extensions:

- Loop Controls (`break` and `continue`)

### Reusing templates

You can write reusable Jinja templates by adding them to a `custom_templates` folder under your
configuration directory. All template files must have the `.jinja` extension and be less than 5MiB.
Templates in this folder will be loaded at startup. To reload the templates without
restarting Home Assistant, invoke the {% my developer_call_service service="homeassistant.reload_custom_templates" %} action.

Once the templates are loaded, Jinja includes and imports will work
using `config/custom_templates` as the base directory.

For example, you might define a macro in a template in `config/custom_templates/formatter.jinja`:

{% raw %}

```text
{% macro format_entity(entity_id) %}
{{ state_attr(entity_id, 'friendly_name') }} - {{ states(entity_id) }}
{% endmacro %}
```

{% endraw %}

In your automations, you could then reuse this macro by importing it:

{% raw %}

```text
{% from 'formatter.jinja' import format_entity %}
{{ format_entity('sensor.temperature') }}
```

{% endraw %}

## Home Assistant template extensions

Extensions allow templates to access all of the Home Assistant specific states and adds other convenience functions and filters.

### Limited templates

Templates for some triggers as well as `trigger_variables` only support a subset of the Home Assistant template extensions. This subset is referred to as "Limited Templates".

### This

State-based and trigger-based template entities have the special template variable `this` available in their templates and actions. See more details and examples in the Template integration documentation.

### States

Not supported in limited templates.

- Iterating `states` will yield each state object.
- Iterating `states.domain` will yield each state object of that domain.
- `states.sensor.temperature` returns the state object for `sensor.temperature` (avoid when possible, see note below).
- `states` can also be used as a function, `states(entity_id, rounded=False, with_unit=False)`, which returns the state string (not the state object) of the given entity, `unknown` if it doesn't exist, and `unavailable` if the object exists but is not available.
  - The optional arguments `rounded` and `with_unit` control the formatting of sensor state strings, please see the examples below.
- `states.sensor.temperature.state_with_unit` formats the state string in the same way as if calling `states('sensor.temperature', rounded=True, with_unit=True)`.
- `is_state` compares an entity's state with a specified state or list of states and returns `True` or `False`. `is_state('device_tracker.paulus', 'home')` will test if the given entity is the specified state. `is_state('device_tracker.paulus', ['home', 'work'])` will test if the given entity is any of the states in the list.
- `state_attr('device_tracker.paulus', 'battery')` will return the value of the attribute or None if it doesn't exist.
- `is_state_attr('device_tracker.paulus', 'battery', 40)` will test if the given entity attribute is the specified state (in this case, a numeric value). Note that the attribute can be `None` and you want to check if it is `None`, you need to use `state_attr('sensor.my_sensor', 'attr') is none` or `state_attr('sensor.my_sensor', 'attr') == None` (note the difference in the capitalization of none in both versions).
- `has_value('sensor.my_sensor')` will test if the given entity is not unknown or unavailable. Can be used as a filter or a test.

{% warning %}
Avoid using `states.sensor.temperature.state`, instead use `states('sensor.temperature')`. It is strongly advised to use the `states()`, `is_state()`, `state_attr()` and `is_state_attr()` as much as possible, to avoid errors and error message when the entity isn't ready yet (e.g., during Home Assistant startup).
{% endwarning %}

#### States examples

The next two statements result in the same value if the state exists. The second one will result in an error if the state does not exist.

{% raw %}

```text
{{ states('device_tracker.paulus') }}
{{ states.device_tracker.paulus.state }}
```

{% endraw %}

Print out a list of all the sensor states:

{% raw %}

```text
{% for state in states.sensor %}
  {{ state.entity_id }}={{ state.state }},
{% endfor %}
```

{% endraw %}

Print out a list of all the sensor states sorted by `entity_id`:

{% raw %}

```text
{% for state in states.sensor | sort(attribute='entity_id') %}
  {{ state.entity_id }}={{ state.state }},
{% endfor %}
```

{% endraw %}

Entities that are on:

{% raw %}

```text
{{ ['light.kitchen', 'light.dining_room'] | select('is_state', 'on') | list }}
```

{% endraw %}

Other state examples:
{% raw %}

```text
{% if is_state('device_tracker.paulus', 'home') %}
  Ha, Paulus is home!
{% else %}
  Paulus is at {{ states('device_tracker.paulus') }}.
{% endif %}

#check sensor.train_departure_time state
{% if states('sensor.train_departure_time') in ("unavailable", "unknown") %}
  {{ ... }}

{% if has_value('sensor.train_departure_time') %}
  {{ ... }}


{% set state = states('sensor.temperature') %}{{ state | float + 1 if is_number(state) else "invalid temperature" }}

{% set state = states('sensor.temperature') %}{{ (state | float * 10) | round(2) if is_number(state)}}

{% set state = states('sensor.temperature') %}
{% if is_number(state) and state | float > 20 %}
  It is warm!
{% endif %}

{{ as_timestamp(states.binary_sensor.garage_door.last_changed) }}

{{ as_local(states.binary_sensor.garage_door.last_changed) }}

{{ as_timestamp(now()) - as_timestamp(states.binary_sensor.garage_door.last_changed) }}

{{ as_local(states.sensor.time.last_changed) }}

{{ states('sensor.expires') | as_datetime }}

# Make a list of states
{{ ['light.kitchen', 'light.dining_room'] | map('states') | list }}
```

{% endraw %}

#### Formatting sensor states

The examples below show the output of a temperature sensor with state `20.001`, unit `°C` and user configured presentation rounding set to 1 decimal.

The following example results in the number `20.001`:

{% raw %}
```text
{{ states('sensor.temperature') }}
```
{% endraw %}

The following example results in the string `"20.0 °C"`:

{% raw %}
```text
{{ states('sensor.temperature', with_unit=True) }}
```
{% endraw %}

The following example result in the string `"20.001 °C"`:

{% raw %}
```text
{{ states('sensor.temperature', with_unit=True, rounded=False) }}
```
{% endraw %}

The following example results in the number `20.0`:

{% raw %}
```text
{{ states('sensor.temperature', rounded=True) }}
```
{% endraw %}

The following example results in the number `20.001`:

{% raw %}
```text
{{ states.sensor.temperature.state }}
```
{% endraw %}

The following example results in the string `"20.0 °C"`:

{% raw %}
```text
{{ states.sensor.temperature.state_with_unit }}
```
{% endraw %}

### Attributes

Not supported in limited templates.

You can print an attribute with `state_attr` if state is defined.

#### Attributes examples

{% raw %}

```text
{% if states.device_tracker.paulus %}
  {{ state_attr('device_tracker.paulus', 'battery') }}
{% else %}
  ??
{% endif %}
```

{% endraw %}

With strings:

{% raw %}

```text
{% set tracker_name = "paulus"%}

{% if states("device_tracker." + tracker_name) != "unknown" %}
  {{ state_attr("device_tracker." + tracker_name, "battery")}}
{% else %}
  ??
{% endif %}
```

{% endraw %}

List of friendly names:

{% raw %}

```text
{{ ['binary_sensor.garage_door', 'binary_sensor.front_door'] | map('state_attr', 'friendly_name') | list }}
```

{% endraw %}

List of lights that are on with a brightness of 255:

{% raw %}

```text
{{ ['light.kitchen', 'light.dining_room'] | select('is_state', 'on') | select('is_state_attr', 'brightness', 255) | list }}
```

{% endraw %}


### State translated

Not supported in limited templates.

The `state_translated` function returns a translated state of an entity using a language that is currently configured in the general settings.

#### State translated examples

{% raw %}

```text
{{ states("sun.sun") }}             # below_horizon
{{ state_translated("sun.sun") }}   # Below horizon
{{ "sun.sun" | state_translated }}  # Below horizon
```

```text
{{ states("binary_sensor.movement_backyard") }}             # on
{{ state_translated("binary_sensor.movement_backyard") }}   # Detected
{{ "binary_sensor.movement_backyard" | state_translated }}  # Detected
```

{% endraw %}


### Working with groups

Not supported in limited templates.

The `expand` function and filter can be used to sort entities and expand groups. It outputs a sorted array of entities with no duplicates.

#### Expand examples

{% raw %}

```text
{% for tracker in expand('device_tracker.paulus', 'group.child_trackers') %}
  {{ state_attr(tracker.entity_id, 'battery') }}
  {%- if not loop.last %}, {% endif -%}
{% endfor %}
```

{% endraw %}

The same thing can also be expressed as a filter:

{% raw %}

```text
{{ expand(['device_tracker.paulus', 'group.child_trackers'])
  | selectattr("attributes.battery", 'defined')
  | join(', ', attribute="attributes.battery") }}
```

{% endraw %}

{% raw %}

```text
{% for energy in expand('group.energy_sensors') if is_number(energy.state) %}
  {{ energy.state }}
  {%- if not loop.last %}, {% endif -%}
{% endfor %}
```

{% endraw %}

The same thing can also be expressed as a test:

{% raw %}

```text
{{ expand('group.energy_sensors')
  | selectattr("state", 'is_number') | join(', ') }}
```

{% endraw %}


### Entities

- `is_hidden_entity(entity_id)` returns whether an entity has been hidden. Can also be used as a test.

### Entities examples

{% raw %}

```text
{{ area_entities('kitchen') | reject('is_hidden_entity') }} # Gets a list of visible entities in the kitchen area
```

{% endraw %}

### Devices

- `device_entities(device_id)` returns a list of entities that are associated with a given device ID. Can also be used as a filter.
- `device_attr(device_or_entity_id, attr_name)` returns the value of `attr_name` for the given device or entity ID. Can also be used as a filter. Not supported in limited templates.
- `is_device_attr(device_or_entity_id, attr_name, attr_value)` returns whether the value of `attr_name` for the given device or entity ID matches `attr_value`. Can also be used as a test. Not supported in limited templates.
- `device_id(entity_id)` returns the device ID for a given entity ID or device name. Can also be used as a filter.

#### Devices examples

{% raw %}

```text
{{ device_attr('deadbeefdeadbeefdeadbeefdeadbeef', 'manufacturer') }}  # Sony
```

```text
{{ is_device_attr('deadbeefdeadbeefdeadbeefdeadbeef', 'manufacturer', 'Sony') }}  # true
```

```text
{{ device_id('sensor.sony') }}  # deadbeefdeadbeefdeadbeefdeadbeef
```

{% endraw %}

### Config entries

- `config_entry_id(entity_id)` returns the config entry ID for a given entity ID. Can also be used as a filter.
- `config_entry_attr(config_entry_id, attr)` returns the value of `attr` for the config entry of the given entity ID. Can also be used as a filter. The following attributes are allowed: `domain`, `title`, `state`, `source`, `disabled_by`. Not supported in limited templates.

#### Config entries examples

{% raw %}

```text
{{ config_entry_id('sensor.sony') }}  # deadbeefdeadbeefdeadbeefdeadbeef
```

```text
{{ config_entry_attr(config_entry_id('sensor.sony'), 'title') }}  # Sony Bravia TV
```



{% endraw %}

### Floors

- `floors()` returns the full list of floor IDs.
- `floor_id(lookup_value)` returns the floor ID for a given device ID, entity ID, area ID, or area name. Can also be used as a filter.
- `floor_name(lookup_value)` returns the floor name for a given device ID, entity ID, area ID, or floor ID. Can also be used as a filter.
- `floor_areas(floor_name_or_id)` returns the list of area IDs tied to a given floor ID or name. Can also be used as a filter.
- `floor_entities(floor_name_or_id)` returns the list of entity IDs tied to a given floor ID or name. Can also be used as a filter.

#### Floors examples

{% raw %}

```text
{{ floors() }}  # ['floor_id']
```

```text
{{ floor_id('First floor') }}  # 'first_floor'
```

```text
{{ floor_id('my_device_id') }}  # 'second_floor'
```

```text
{{ floor_id('sensor.sony') }}  # 'first_floor'
```

```text
{{ floor_name('first_floor') }}  # 'First floor'
```

```text
{{ floor_name('my_device_id') }}  # 'Second floor'
```

```text
{{ floor_name('sensor.sony') }}  # 'First floor'
```

```text
{{ floor_areas('first_floor') }}  # ['living_room', 'kitchen']
```

{% endraw %}

### Areas

- `areas()` returns the full list of area IDs
- `area_id(lookup_value)` returns the area ID for a given device ID, entity ID, or area name. Can also be used as a filter.
- `area_name(lookup_value)` returns the area name for a given device ID, entity ID, or area ID. Can also be used as a filter.
- `area_entities(area_name_or_id)` returns the list of entity IDs tied to a given area ID or name. Can also be used as a filter.
- `area_devices(area_name_or_id)` returns the list of device IDs tied to a given area ID or name. Can also be used as a filter.

#### Areas examples

{% raw %}

```text
{{ areas() }}  # ['area_id']
```

```text
{{ area_id('Living Room') }}  # 'deadbeefdeadbeefdeadbeefdeadbeef'
```

```text
{{ area_id('my_device_id') }}  # 'deadbeefdeadbeefdeadbeefdeadbeef'
```

```text
{{ area_id('sensor.sony') }}  # 'deadbeefdeadbeefdeadbeefdeadbeef'
```

```text
{{ area_name('deadbeefdeadbeefdeadbeefdeadbeef') }}  # 'Living Room'
```

```text
{{ area_name('my_device_id') }}  # 'Living Room'
```

```text
{{ area_name('sensor.sony') }}  # 'Living Room'
```

```text
{{ area_entities('deadbeefdeadbeefdeadbeefdeadbeef') }}  # ['sensor.sony']
```

```text
{{ area_devices('Living Room') }}  # ['my_device_id']
```

{% endraw %}

### Entities for an integration

- `integration_entities(integration)` returns a list of entities that are associated with a given integration, such as `hue` or `zwave_js`.
- `integration_entities(config_entry_title)` if you have multiple entries set-up for an integration, you can also use the title you've set for the integration in case you only want to target a specific entry.

If there is more than one entry with the same title, the entities for all the matching entries will be returned, even if the entries are for different integrations. It's not possible to search for entities of an untitled integration.

#### Integrations examples

{% raw %}

```text
{{ integration_entities('hue') }}  # ['light.hue_light_upstairs', 'light.hue_light_downstairs']
```

```text
{{ integration_entities('Hue bridge downstairs') }}  # ['light.hue_light_downstairs']
```

{% endraw %}

### Labels

- `labels()` returns the full list of label IDs, or those for a given area ID, device ID, or entity ID.
- `label_id(lookup_value)` returns the label ID for a given label name.
- `label_name(lookup_value)` returns the label name for a given label ID.
- `label_areas(label_name_or_id)` returns the list of area IDs tied to a given label ID or name.
- `label_devices(label_name_or_id)` returns the list of device IDs tied to a given label ID or name.
- `label_entities(label_name_or_id)` returns the list of entity IDs tied to a given label ID or name.

Each of the label template functions can also be used as a filter.

#### Labels examples

{% raw %}

```text
{{ labels() }}  # ['christmas_decorations', 'energy_saver', 'security']
```

```text
{{ labels("living_room") }}  # ['christmas_decorations', 'energy_saver']
```

```text
{{ labels("my_device_id") }}  # ['security']
```

```text
{{ labels("light.christmas_tree") }}  # ['christmas_decorations']
```

```text
{{ label_id('Energy saver') }}  # 'energy_saver'
```

```text
{{ label_name('energy_saver') }}  # 'Energy saver'
```

```text
{{ label_areas('security') }}  # ['driveway', 'garden', 'porch']
```

```text
{{ label_devices('energy_saver') }}  # ['deadbeefdeadbeefdeadbeefdeadbeef']
```

```text
{{ label_entities('security') }}  # ['camera.driveway', 'binary_sensor.motion_garden', 'camera.porch']
```

{% endraw %}

### Issues

- `issues()` returns all open issues as a mapping of (domain, issue_id) tuples to the issue object.
- `issue(domain, issue_id)` returns a specific issue for the provided domain and issue_id.

#### Issues examples

{% raw %}

```text
{{ issues() }}  # { ("homeassistant", "deprecated_yaml_ping"): {...}, ("cloud", "legacy_subscription"): {...} }
```

```text
{{ issue('homeassistant', 'python_version') }}  # {"breaks_in_ha_version": "2024.4", "domain": "homeassistant", "issue_id": "python_version", "is_persistent": False, ...}
```

{% endraw %}

### Immediate if (iif)

A common case is to conditionally return a value based on another value.
For example, return a "Yes" or "No" when the light is on or off.

This can be written as:

{% raw %}

```text
{% if is_state('light.kitchen', 'on') %}
  Yes
{% else %}
  No
{% endif %}
```

{% endraw %}

Or using a shorter syntax:

{% raw %}

```text
{{ 'Yes' if is_state('light.kitchen', 'on') else 'No' }}
```

{% endraw %}

Additionally, to the above, you can use the `iif` function/filter, which is
an immediate if.

Syntax: `iif(condition, if_true, if_false, if_none)`

`iif` returns the value of `if_true` if the condition is truthy, the value of `if_false` if it's `falsy` and the value of `if_none` if it's `None`.
An empty string, an empty mapping or an an empty list, are all falsy, refer to the Python documentation for an in depth explanation.

`if_true` is optional, if it's omitted `True` is returned if the condition is truthy.
`if_false` is optional, if it's omitted `False` is returned if the condition is falsy.
`if_none` is optional, if it's omitted the value of `if_false` is returned if the condition is `None`.

Examples using `iif`:

{% raw %}

```text
{{ iif(is_state('light.kitchen', 'on'), 'Yes', 'No') }}

{{ is_state('light.kitchen', 'on') | iif('Yes', 'No') }}

{{ (states('light.kitchen') == 'on') | iif('Yes', 'No') }}
```

{% endraw %}

{% warning %}
The immediate if filter does not short-circuit like you might expect with a typical conditional statement. The `if_true`, `if_false` and `if_none` expressions will all be evaluated and the filter will simply return one of the resulting values. This means you cannot use this filter to prevent executing an expression which would result in an error.

For example, if you wanted to select a field from `trigger` in an automation based on the platform you might go to make this template: `trigger.platform == 'event' | iif(trigger.event.data.message, trigger.to_state.state)`. This won't work because both expressions will be evaluated and one will fail since the field doesn't exist. Instead you have to do this `trigger.event.data.message if trigger.platform == 'event' else trigger.to_state.state`. This form of the expression short-circuits so if the platform is `event` the expression `trigger.to_state.state` will never be evaluated and won't cause an error.
{% endwarning%}

### Time

`now()`, `time_since()`, `time_until()`, `today_at()`, and `utcnow()` are not supported in limited templates.

- `now()` returns a datetime object that represents the current time in your time zone.
  - You can also use: `now().second`, `now().minute`, `now().hour`, `now().day`, `now().month`, `now().year`, `now().weekday()` and `now().isoweekday()` and other `datetime` attributes and functions.
  - Using `now()` will cause templates to be refreshed at the start of every new minute.
- `utcnow()` returns a datetime object of the current time in the UTC timezone.
  - For specific values: `utcnow().second`, `utcnow().minute`, `utcnow().hour`, `utcnow().day`, `utcnow().month`, `utcnow().year`, `utcnow().weekday()` and `utcnow().isoweekday()`.
  - Using `utcnow()` will cause templates to be refreshed at the start of every new minute.
- `today_at(value)` converts a string containing a military time format to a datetime object with today's date in your time zone. Defaults to midnight (`00:00`).

  - Using `today_at()` will cause templates to be refreshed at the start of every new minute.

  {% raw %}

  ```text
  # Is the current time past 10:15?
  {{ now() > today_at("10:15") }}
  ```

  {% endraw %}

- `as_datetime(value, default)` converts a string containing a timestamp, or valid UNIX timestamp, to a datetime object. If that fails, it returns the `default` value or, if omitted, raises an error. When the input is already a datetime object it will be returned as is. in case the input is a datetime.date object, midnight will be added as time. This function can also be used as a filter.
- `as_timestamp(value, default)` converts a datetime object or string to UNIX timestamp. If that fails, returns the `default` value, or if omitted raises an error. This function can also be used as a filter.
- `as_local()` converts a datetime object to local time. This function can also be used as a filter.
- `strptime(string, format, default)` parses a string based on a format and returns a datetime object. If that fails, it returns the `default` value or, if omitted, raises an error.
- `relative_time` converts a datetime object to its human-friendly "age" string. The age can be in seconds, minutes, hours, days, months, or years (but only the biggest unit is considered. For example, if it's 2 days and 3 hours, "2 days" will be returned). Note that it only works for dates _in the past_.
  - Using `relative_time()` will cause templates to be refreshed at the start of every new minute.
- `time_since(datetime, precision)` converts a datetime object into its human-readable time string. The time string can be in seconds, minutes, hours, days, months, and years. `precision` takes an integer (full number) and indicates the number of units returned.  The last unit is rounded. For example: `precision = 1` could return "2 years" while `precision = 2` could return "1 year 11 months". This function can also be used as a filter.
If the datetime is in the future, returns 0 seconds.
A precision of 0 returns all available units, default is 1.
- `time_until(datetime, precision)` converts a datetime object into a human-readable time string. The time string can be in seconds, minutes, hours, days, months, and years. `precision` takes an integer (full number) and indicates the number of units returned.  The last unit is rounded. For example: `precision = 1` could return "2 years" while `precision = 2` could return "1 year 11 months". This function can also be used as a filter.
If the datetime is in the past, returns 0 seconds.
A precision of 0 returns all available units, default is 1.
- `timedelta` returns a timedelta object, which represents a duration (an amount of time between two datetimes). It accepts the same arguments as the Python `datetime.timedelta` function -- days, seconds, microseconds, milliseconds, minutes, hours, weeks.

  {% raw %}

  ```text
  # 77 minutes before current time.
  {{ now() - timedelta( hours = 1, minutes = 17 ) }}
  ```

  {% endraw %}

- `as_timedelta(string)` converts a string to a timedelta object, which represents a duration (an amount of time between two datetimes). Expects data in the format `DD HH:MM:SS.uuuuuu`, `DD HH:MM:SS,uuuuuu`, or as specified by ISO 8601 (e.g. `P4DT1H15M20S` which is equivalent to `4 1:15:20`) or PostgreSQL’s day-time interval format (e.g. `3 days 04:05:06`). This function can also be used as a filter.

  {% raw %}

  ```text
  # Renders to "00:10:00"
  {{ as_timedelta("PT10M") }}
  ```

  {% endraw %}

- Filter `timestamp_local(default)` converts a UNIX timestamp to the ISO format string representation as date/time in your local timezone. If that fails, returns the `default` value, or if omitted raises an error. If a custom string format is needed in the string, use `timestamp_custom` instead.
- Filter `timestamp_utc(default)` converts a UNIX timestamp to the ISO format string representation representation as date/time in UTC timezone. If that fails, returns the `default` value, or if omitted raises an error. If a custom string format is needed in the string, use `timestamp_custom` instead.
- Filter `timestamp_custom(format_string, local=True, default)` converts an UNIX timestamp to its string representation based on a custom format, the use of a local timezone is the default. If that fails, returns the `default` value, or if omitted raises an error. Supports the standard Python time formatting options.

{% tip %}
UNIX timestamp is the number of seconds that have elapsed since 00:00:00 UTC on 1 January 1970. Therefore, if used as a function's argument, it can be substituted with a numeric value (`int` or `float`).
{% endtip %}

{% important %}
If your template is returning a timestamp that should be displayed in the frontend (e.g., as a sensor entity with `device_class: timestamp`), you have to ensure that it is the ISO 8601 format (meaning it has the "T" separator between the date and time portion). Otherwise, frontend rendering on macOS and iOS devices will show an error. The following value template would result in such an error:

{% raw %}

`{{ states.sun.sun.last_changed }}` => `2023-07-30 20:03:49.253717+00:00` (missing "T" separator)

{% endraw %}

To fix it, enforce the ISO conversion via `isoformat()`:

{% raw %}

`{{ states.sun.sun.last_changed.isoformat() }}` => `2023-07-30T20:03:49.253717+00:00` (contains "T" separator)

{% endraw %}

{% endimportant %}

{% raw %}

```text
{{ 120 | timestamp_local }}
```

{% endraw %}

### To/From JSON

The `to_json` filter serializes an object to a JSON string. In some cases, it may be necessary to format a JSON string for use with a webhook, as a parameter for command-line utilities or any number of other applications. This can be complicated in a template, especially when dealing with escaping special characters. Using the `to_json` filter, this is handled automatically.

`to_json` also accepts boolean arguments for `pretty_print`, which will pretty print the JSON with a 2-space indent to make it more human-readable, and `sort_keys`, which will sort the keys of the JSON object, ensuring that the resulting string is consistent for the same input.

If you need to generate JSON that will be used by a parser that lacks support for Unicode characters, you can add  `ensure_ascii=True` to have `to_json` generate Unicode escape sequences in strings.

The `from_json` filter operates similarly, but in the other direction, de-serializing a JSON string back into an object.


### To/From JSON examples

#### Template

{% raw %}

```text
{% set temp = {'temperature': 25, 'unit': '°C'} %}
stringified object: {{ temp }}
object|to_json: {{ temp|to_json(sort_keys=True) }}
```

{% endraw %}

#### Output

{% raw %}

```text
stringified object: {'temperature': 25, 'unit': '°C'}
object|to_json: {"temperature": 25, "unit": "°C"}
```

{% endraw %}

Conversely, `from_json` can be used to de-serialize a JSON string back into an object to make it possible to easily extract usable data.

#### Template

{% raw %}

```text
{% set temp = '{"temperature": 25, "unit": "°C"}'|from_json %}
The temperature is {{ temp.temperature }}{{ temp.unit }}
```

{% endraw %}

#### Output

{% raw %}

```text
The temperature is 25°C
```

{% endraw %}

### Is defined

Sometimes a template should only return if a value or object is defined, if not, the supplied default value should be returned. This can be useful to validate a JSON payload.
The `is_defined` filter allows to throw an error if a value or object is not defined.

Example using `is_defined` to parse a JSON payload:

{% raw %}

```text
{{ value_json.val | is_defined }}
```

{% endraw %}

This will throw an error `UndefinedError: 'value_json' is undefined` if the JSON payload has no `val` attribute.

### Version

- `version()` Returns a AwesomeVersion object for the value given inside the brackets.
  - This is also available as a filter (`| version`).

Examples:

{% raw %}

- `{{ version("2099.9.9") > "2000.0.0" }}` Will return `True`
- `{{ version("2099.9.9") hh"`.
- Function `unpack(value, format_string, offset=0)` will try to convert a `bytes` object into a native Python object. The `offset` parameter defines the offset position in bytes from the start of the input `bytes` based buffer. This will call function `struct.unpack_from(format_string, value, offset=offset)`. Returns `None` if an error occurs or when `format_string` is invalid. Note that the function `unpack` will only return the first `bytes` object, despite the function `struct.unpack_from` supporting to return multiple objects (e.g. with `format_string` being `">hh"`.

{% note %}

Some examples:
{% raw %}

- `{{ 0xDEADBEEF | pack(">I") }}` - renders as `b"\xde\xad\xbe\xef"`
- `{{ pack(0xDEADBEEF, ">I") }}` - renders as `b"\xde\xad\xbe\xef"`
- `{{ "0x%X" % 0xDEADBEEF | pack(">I") | unpack(">I") }}` - renders as `0xDEADBEEF`
- `{{ "0x%X" % 0xDEADBEEF | pack(">I") | unpack(">H", offset=2) }}` - renders as `0xBEEF`

{% endraw %}

{% endnote %}

### String filters

- Filter `urlencode` will convert an object to a percent-encoded ASCII text string (e.g., for HTTP requests using `application/x-www-form-urlencoded`).
- Filter `slugify(separator="_")` will convert a given string into a "slug".
- Filter `ordinal` will convert an integer into a number defining a position in a series (e.g., `1st`, `2nd`, `3rd`, `4th`, etc).
- Filter `value | base64_decode` Decodes a base 64 string to a string, by default utf-8 encoding is used.
- Filter `value | base64_decode("ascii")` Decodes a base 64 string to a string, using ascii encoding.
- Filter `value | base64_decode(None)` Decodes a base 64 string to raw bytes.



Some examples:
{% raw %}

- `{{ "aG9tZWFzc2lzdGFudA==" | base64_decode }}` - renders as `homeassistant`
- `{{ "aG9tZWFzc2lzdGFudA==" | base64_decode(None) }}` - renders as `b'homeassistant'`

{% endraw %}



### Hashing

The template engine contains a few filters and functions to hash a string of
data. A few very common hashing algorithms are supported: `md5`, `sha1`,
`sha256`, and `sha512`.

Some examples:

{% raw %}

- `{{ md5("Home Assistant") }}` - renders as `f3f2b8b3b40084aa87e92b7ffb02ed13885fea2d07`
- `{{ "Home Assistant" | md5 }}` - renders as `f3f2b8b3b40084aa87e92b7ffb02ed13885fea2d07`

- `{{ sha1("Home Assistant") }}` - renders as `14bffd017c73917bfda2372aaf287570597b8e82`
- `{{ "Home Assistant" | sha1 }}` - renders as `14bffd017c73917bfda2372aaf287570597b8e82`

- `{{ sha256("Home Assistant") }}` - renders as `a18f473c9d3ed968a598f996dcf0b9de84de4ee04c950d041b61297a25bcea49`
- `{{ "Home Assistant" | sha256 }}` - renders as `a18f473c9d3ed968a598f996dcf0b9de84de4ee04c950d041b61297a25bcea49`

- `{{ sha512("Home Assistant") }}` - renders as `f251e06eb7d3439e1a86d6497d6a4531c3e8c809f538be62f89babf147d7d63aca4e77ae475b94c654fd38d8f543f778ce80007d6afef379d8a0e5d3ddf7349d`
- `{{ "Home Assistant" | sha512 }}` - renders as `f251e06eb7d3439e1a86d6497d6a4531c3e8c809f538be62f89babf147d7d63aca4e77ae475b94c654fd38d8f543f778ce80007d6afef379d8a0e5d3ddf7349d`

{% endraw %}


### Regular expressions

For more information on regular expressions
See: Python regular expression operations

- Test `string is match(find, ignorecase=False)` will match the find expression at the beginning of the string using regex.
- Test `string is search(find, ignorecase=False)` will match the find expression anywhere in the string using regex.
- Filter `string|regex_replace(find='', replace='', ignorecase=False)` will replace the find expression with the replace string using regex. Access to the matched groups in `replace` is possible with `'\\1'`, `'\\2'`, etc.
- Filter `value | regex_findall(find='', ignorecase=False)` will find all regex matches of the find expression in `value` and return the array of matches.
- Filter `value | regex_findall_index(find='', index=0, ignorecase=False)` will do the same as `regex_findall` and return the match at index.

### Shuffling

The template engine contains a filter and function to shuffle a list.

Shuffling can happen randomly or reproducibly using a seed. When using a seed
it will always return the same shuffled list for the same seed.

Some examples:

{% raw %}

- `{{ [1, 2, 3] | shuffle }}` - renders as `[3, 1, 2]` (_random_)
- `{{ shuffle([1, 2, 3]) }}` - renders as `[3, 1, 2]` (_random_)
- `{{ shuffle(1, 2, 3) }}` - renders as `[3, 1, 2]` (_random_)

- `{{ [1, 2, 3] | shuffle("random seed") }}` - renders as `[2, 3, 1] (_reproducible_)
- `{{ shuffle([1, 2, 3], seed="random seed") }}` - renders as `[2, 3, 1] (_reproducible_)
- `{{ shuffle([1, 2, 3], "random seed") }}`- renders as `[2, 3, 1] (_reproducible_)
- `{{ shuffle(1, 2, 3, seed="random seed") }}` - renders as `[2, 3, 1] (_reproducible_)

{% endraw %}

### Flatten a list of lists

The template engine provides a filter to flatten a list of lists: `flatten`.

It will take a list of lists and return a single list with all the elements.
The depth of the flattening can be controlled using the `levels` parameter.
The flattening process is recursive, so it will flatten all nested lists, until
the number of levels (if specified) is reached.

Some examples:

{% raw %}

- `{{ flatten([1, [2, [3]], 4, [5 , 6]]) }}` - renders as `[1, 2, 3, 4, 5, 6]`
- `{{ [1, [2, [3]], 4, [5 , 6]] | flatten }}` - renders as `[1, 2, 3, 4, 5, 6]`

- `{{ flatten([1, [2, [3]]], levels=1) }}` - renders as `[1, 2, [3]]`
- `{{ [1, [2, [3]]], flatten(levels=1) }}` - renders as `[1, 2, [3]]`

- `{{ flatten([1, [2, [3]]], 1) }}` - renders as `[1, 2, [3]]`
- `{{ [1, [2, [3]]], flatten(1) }}` - renders as `[1, 2, [3]]`

{% endraw %}

### Find common elements between lists

The template engine provides a filter to find common elements between two lists: `intersect`.

This function returns a list containing all elements that are present in both input lists.

Some examples:

{% raw %}

- `{{ intersect([1, 2, 5, 3, 4, 10], [1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[1, 2, 3, 4, 5]`
- `{{ [1, 2, 5, 3, 4, 10] | intersect([1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[1, 2, 3, 4, 5]`
- `{{ intersect(['a', 'b', 'c'], ['b', 'c', 'd']) }}` - renders as `['b', 'c']`
- `{{ ['a', 'b', 'c'] | intersect(['b', 'c', 'd']) }}` - renders as `['b', 'c']`

{% endraw %}

### Find elements in first list not in second list

The template engine provides a filter to find elements that are in the first list but not in the second list: `difference`.
This function returns a list containing all elements that are present in the first list but absent from the second list.

Some examples:

{% raw %}

- `{{ difference([1, 2, 5, 3, 4, 10], [1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[10]`
- `{{ [1, 2, 5, 3, 4, 10] | difference([1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[10]`
- `{{ difference(['a', 'b', 'c'], ['b', 'c', 'd']) }}` - renders as `['a']`
- `{{ ['a', 'b', 'c'] | difference(['b', 'c', 'd']) }}` - renders as `['a']`

{% endraw %}

### Find elements that are in either list but not in both

The template engine provides a filter to find elements that are in either of the input lists but not in both: `symmetric_difference`.
This function returns a list containing all elements that are present in either the first list or the second list, but not in both.

Some examples:

{% raw %}

- `{{ symmetric_difference([1, 2, 5, 3, 4, 10], [1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[10, 11, 99]`
- `{{ [1, 2, 5, 3, 4, 10] | symmetric_difference([1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[10, 11, 99]`
- `{{ symmetric_difference(['a', 'b', 'c'], ['b', 'c', 'd']) }}` - renders as `['a', 'd']`
- `{{ ['a', 'b', 'c'] | symmetric_difference(['b', 'c', 'd']) }}` - renders as `['a', 'd']`

{% endraw %}

### Combine all unique elements from two lists

The template engine provides a filter to combine all unique elements from two lists: `union`.
This function returns a list containing all unique elements that are present in either the first list or the second list.

Some examples:

{% raw %}

- `{{ union([1, 2, 5, 3, 4, 10], [1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[1, 2, 3, 4, 5, 10, 11, 99]`
- `{{ [1, 2, 5, 3, 4, 10] | union([1, 2, 3, 4, 5, 11, 99]) }}` - renders as `[1, 2, 3, 4, 5, 10, 11, 99]`
- `{{ union(['a', 'b', 'c'], ['b', 'c', 'd']) }}` - renders as `['a', 'b', 'c', 'd']`
- `{{ ['a', 'b', 'c'] | union(['b', 'c', 'd']) }}` - renders as `['a', 'b', 'c', 'd']`

{% endraw %}

### Combining dictionaries

The template engine provides a function and filter to merge multiple dictionaries: `combine`.

It will take multiple dictionaries and merge them into a single dictionary. When used as a filter,
the filter value is used as the first dictionary. The optional `recursive` parameter determines
whether nested dictionaries should be merged (defaults to `False`).

Some examples:

{% raw %}

- `{{ {'a': 1, 'b': 2} | combine({'b': 3, 'c': 4}) }}` - renders as `{'a': 1, 'b': 3, 'c': 4}`
- `{{ combine({'a': 1, 'b': 2}, {'b': 3, 'c': 4}) }}` - renders as `{'a': 1, 'b': 3, 'c': 4}`

- `{{ combine({'a': 1, 'b': {'x': 1}}, {'b': {'y': 2}, 'c': 4}, recursive=True) }}` - renders as `{'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 4}`
- `{{ combine({'a': 1, 'b': {'x': 1}}, {'b': {'y': 2}, 'c': 4}) }}` - renders as `{'a': 1, 'b': {'y': 2}, 'c': 4}`

{% endraw %}

## Merge action responses

Using action responses we can collect information from various entities at the same time.
Using the `merge_response` template we can merge several responses into one list.

| Variable       | Description                                     |
| -------------- | ----------------------------------              |
| `value`        | The incoming value (must be an action response). |

The `entity_id` key is appended to each dictionary within the template output list as a reference of origin. If the input dictionary already contains an `entity_id` key, the template will fail.

The `value_key` key is appended to each dictionary within the template output list as a reference of origin if the original service call was providing a list of dictionaries, for example, `calendar.get_events` or `weather.get_forecasts`.

Examples of these two keys can be seen in example merge calendar action response template output.


### Example

```yaml
{% raw %}

{% set combined_forecast = merge_response(response) %}
{{ combined_forecast[0].precipitation | float(0) | round(1) }}

{% endraw %}
```

### Example how to sort

Sorting the dictionaries within the list based on a specific key can be done directly by using Jinja's `sort` filter.

```yaml
{% raw %}

{{ merge_response(calendar_response) | sort(attribute='start') | ... }}

{% endraw %}
```

### Example merge calendar action response

```json
{
  "calendar.sports": {
    "events": [
      {
        "start": "2024-02-27T17:00:00-06:00",
        "end": "2024-02-27T18:00:00-06:00",
        "summary": "Basketball vs. Rockets",
        "description": "",
      }
    ]
  },
  "calendar.local_furry_events": {"events": []},
  "calendar.yap_house_schedules": {
    "events": [
      {
        "start": "2024-02-26T08:00:00-06:00",
        "end": "2024-02-26T09:00:00-06:00",
        "summary": "Dr. Appt",
        "description": "",
      },
      {
        "start": "2024-02-28T20:00:00-06:00",
        "end": "2024-02-28T21:00:00-06:00",
        "summary": "Bake a cake",
        "description": "something good",
      }
    ]
  },
}
```

```yaml
{% raw %}
{{ merge_response(response_variable) }}
{% endraw %}
```

```json
[
  {
    "description": "",
    "end": "2024-02-27T18:00:00-06:00",
    "entity_id": "calendar.sports",
    "start": "2024-02-27T17:00:00-06:00",
    "summary": "Basketball vs. Rockets",
    "value_key": "events"
  },
  {
    "description": "",
    "end": "2024-02-26T09:00:00-06:00",
    "entity_id": "calendar.yap_house_schedules",
    "start": "2024-02-26T08:00:00-06:00",
    "summary": "Dr. Appt",
    "value_key": "events"
  },
  {
    "description": "something good",
    "end": "2024-02-28T21:00:00-06:00",
    "entity_id": "calendar.yap_house_schedules",
    "start": "2024-02-28T20:00:00-06:00",
    "summary": "Bake a cake",
    "value_key": "events"
  }
]
```

### Example non-list action responses

```json
{
  "vacuum.deebot_n8_plus_1": {
    "header": {
      "ver": "0.0.1",
    },
    "payloadType": "j",
    "resp": {
      "body": {
        "msg": "ok",
      },
    },
  },
  "vacuum.deebot_n8_plus_2": {
    "header": {
      "ver": "0.0.1",
    },
    "payloadType": "j",
    "resp": {
      "body": {
        "msg": "ok",
      },
    },
  },
}
```

```yaml
{% raw %}
{{ merge_response(response_variable) }}
{% endraw %}
```

```json
[
  {
    "entity_id": "vacuum.deebot_n8_plus_1",
    "header": {
      "ver": "0.0.1",
    },
    "payloadType": "j",
    "resp": {
      "body": {
        "msg": "ok",
      },
    },
  },
  {
    "entity_id": "vacuum.deebot_n8_plus_2",
    "header": {
      "ver": "0.0.1",
    },
    "payloadType": "j",
    "resp": {
      "body": {
        "msg": "ok",
      },
    },
  },
]
```

## Processing incoming data

The other part of templating is processing incoming data. It allows you to modify incoming data and extract only the data you care about. This will only work for platforms and integrations that mention support for this in their documentation.

It depends per integration or platform, but it is common to be able to define a template using the `value_template` configuration key. When a new value arrives, your template will be rendered while having access to the following values on top of the usual Home Assistant extensions:

| Variable     | Description                        |
| ------------ | ---------------------------------- |
| `value`      | The incoming value.                |
| `value_json` | The incoming value parsed as JSON. |

This means that if the incoming values looks like the sample below:

```json
{
  "on": "true",
  "temp": 21
}
```

The template for `on` would be:

{% raw %}

```yaml
"{{value_json.on}}"
```

{% endraw %}

Nested JSON in a response is supported as well:

```json
{
  "sensor": {
    "type": "air",
    "id": "12345"
  },
  "values": {
    "temp": 26.09,
    "hum": 56.73
  }
}
```

Just use the "Square bracket notation" to get the value.

{% raw %}

```yaml
"{{ value_json['values']['temp'] }}"
```

{% endraw %}

The following overview contains a couple of options to get the needed values:

{% raw %}

```text
# Incoming value:
{"primes": [2, 3, 5, 7, 11, 13]}

# Extract first prime number
{{ value_json.primes[0] }}

# Format output
{{ "%+.1f" | value_json }}

# Math
{{ value_json | float * 1024 if is_number(value_json) }}
{{ float(value_json) * (2**10) if is_number(value_json) }}
{{ value_json | log if is_number(value_json) }}
{{ log(1000, 10) }}
{{ sin(pi / 2) }}
{{ cos(tau) }}
{{ tan(pi) }}
{{ sqrt(e) }}

# Timestamps
{{ value_json.tst | timestamp_local }}
{{ value_json.tst | timestamp_utc }}
{{ value_json.tst | timestamp_custom('%Y', True) }}
```

{% endraw %}

To evaluate a response, go to **{% my developer_template title="Developer Tools > Template" %}**, create your output in "Template editor", and check the result.

{% raw %}

```yaml
{% set value_json=
    {"name":"Outside",
     "device":"weather-ha",
     "data":
        {"temp":"24C",
         "hum":"35%"
         } }%}

{{value_json.data.hum[:-1]}}
```

{% endraw %}

### Using templates with the MQTT integration

The MQTT integration relies heavily on templates. Templates are used to transform incoming payloads (value templates) to state updates or incoming actions (command templates) to payloads that configure the MQTT device.

#### Using value templates with MQTT

Value templates translate received MQTT payload to a valid state or attribute.
The received MQTT is available in the `value` template variable, and in the `value_json` template variable if the received MQTT payload is valid JSON.

In addition, the template variables `entity_id`, `name` and `this` are available for MQTT entity value templates. The `this` attribute refers to the entity state of the MQTT item.

{% note %}

Example value template:

With given payload:

```json
{ "state": "ON", "temperature": 21.902, "humidity": null }
```

Template {% raw %}`{{ value_json.temperature | round(1) }}`{% endraw %} renders to `21.9`.

Template {% raw %}`{{ value_json.humidity }}`{% endraw %} renders to `None`.

{% endnote %}

#### Using command templates with MQTT

For actions, command templates are defined to format the outgoing MQTT payload to a format supported by the remote device. When an action is executed, the template variable `value` has the action data in most cases unless otherwise specified in the documentation.

In addition, the template variables `entity_id`, `name` and `this` are available for MQTT entity command templates. The `this` attribute refers to the entity state of the MQTT item.

{% note %}

**Example command template with JSON data:**

With given value `21.9` template {% raw %}`{"temperature": {{ value }} }`{% endraw %} renders to:

```json
{
  "temperature": 21.9
}
```

{% endnote %}

**Example command template with raw data:**

When a command template renders to a valid `bytes` literal, then MQTT will publish this data as raw data. In other cases, a string representation will be published. So:

- Template {% raw %}`{{ "16" }}`{% endraw %} renders to payload encoded string `"16"`.
- Template {% raw %}`{{ 16 }}`{% endraw %} renders to payload encoded string `"16"`.
- Template {% raw %}`{{ pack(0x10, ">B") }}`{% endraw %} renders to a raw 1 byte payload `0x10`.

### Determining types

When working with templates, it can be useful to determine the type of
the returned value from a method or the type of a variable at times.

For this, Home Assistant provides the `typeof()` template function and filter,
which is inspired by the JavaScript
`typeof` operator. It reveals the type of the given value.

This is mostly useful when you are debugging or playing with templates in
the developer tools of Home Assistant. However, it might be useful in some
other cases as well.

Some examples:

{% raw %}

- `{{ typeof(42) }}` - renders as `int`
- `{{ typeof(42.0) }}` - renders as `float`
- `{{ typeof("42") }}` - renders as `str`
- `{{ typeof([1, 2, 3]) }}` - renders as `list`
- `{{ typeof({"key": "value"}) }}` - renders as `dict`
- `{{ typeof(True) }}` - renders as `bool`
- `{{ typeof(None) }}` - renders as `NoneType`

- `{{ 42 | typeof }}` - renders as `int`
- `{{ 42.0 | typeof }}` - renders as `float`
- `{{ "42" | typeof }}` - renders as `str`
- `{{ [1, 2, 3] | typeof }}` - renders as `list`
- `{{ {"key": "value"} | typeof }}` - renders as `dict`
- `{{ True | typeof }}` - renders as `bool`
- `{{ None | typeof }}` - renders as `NoneType`

- `{{ some_variable | typeof }}` - renders the type of `some_variable`
- `{{ states("sensor.living_room") | typeof }}` - renders the type of the result of `states()` function

{% endraw %}

## Some more things to keep in mind

### `entity_id` that begins with a number

If your template uses an `entity_id` that begins with a number (example: `states.device_tracker.2008_gmc`) you must use a bracket syntax to avoid errors caused by rendering the `entity_id` improperly. In the example given, the correct syntax for the device tracker would be: `states.device_tracker['2008_gmc']`

### Priority of operators

The default priority of operators is that the filter (`|`) has priority over everything except brackets. This means that:

{% raw %}

```text
{{ states('sensor.temperature') | float / 10 | round(2) }}
```

{% endraw %}

Would round `10` to 2 decimal places, then divide `states('sensor.temperature')` by `10` (rounded to 2 decimal places so 10.00). This behavior is maybe not the one expected, but priority rules imply that.
