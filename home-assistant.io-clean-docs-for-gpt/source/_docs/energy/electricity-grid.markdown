---
title: "Integrating your electricity grid"
description: "Learn how to add information about your electricity grid to Home Assistant home energy management."
---

Energy management is all about knowing how much energy you’re consuming, where it’s coming from and where it’s going.

Almost all houses are connected to the electricity grid which provides the energy your home will need. The energy usage is being tracked by your energy meter and is billed to you by your energy provider. Energy prices can differ based on a schedule or change according to market price.



## Tariffs

It has become popular for energy utilities to split the price of energy based on time of the day; this is done in order to incentivise consumers to shift their power needs towards times where the grid has lower loads. These periods of time are commonly referred to as Peak and Off Peak, exactly because they match periods of time where everyone is consuming energy (Peak) and periods of time where the energy is abundant but no one is using it (Off Peak). Therefore Peak energy is more expensive then Off Peak energy.

If you want to split energy usage into multiple tariffs, read this.

## Hardware

Home Assistant will need to know the amount of energy flowing through your meter. This data can be tracked in various ways.

### Connect to your meter

The best way to get this data is directly from your electricity meter that sits between your house and the grid. In certain countries these meters contain standardized ways of reading out the information locally.

#### Connect using a P1 port

The P1 port is a standardized port in the Netherlands, Belgium and Luxembourg. A P1 reader can connect to this port and receive real-time information.

We have worked with creator Marcel Zuidwijk to develop SlimmeLezer+. It's an affordable P1 reader powered by ESPHome that will seamlessly integrate this information in Home Assistant. It is being sold on his website and the firmware is open source on GitHub.



#### Connect via Zigbee Energy Profile

The Zigbee Energy Profile is a wireless energy standard to provide real-time information about electricity usage. This standard is available in some meters in the US, UK and Australia. This is not "normal" Zigbee as implemented by Home Assistant but requires special certified hardware.

We are not currently aware of a device that implements this which supports a local API and is compatible with Home Assistant.

#### Reading the meter via a pulse counter

Many meters, including older ones, have an LED that will flash whenever energy passes through it. For example, each flash is a 1/1000th kWh. By monitoring the time between flashes it’s possible to determine the energy consumption.

We have developed Home Assistant Glow, an open source solution powered by ESPHome's pulse meter sensor. You put it on top of the activity LED of your electricity meter and it will bring your consumption into Home Assistant.



#### Reading the meter via a IEC62056-21

The IEC62056-21 is a common protocol not only for electric meters. It uses an infrared port to read data.
Aquaticus has created an ESPHome component for reading this data. PiggyMeter is a complete project that allows easy installation.


#### Using (Smart Message Language) interface

In countries like Germany, SML (Smart Message Language) is used typically. ESPHome's SML (Smart Message Language) is one way to integrate it. If you prefer to integrate it via MQTT, sml2mqtt is another open source option.

#### Read the meter using an AI-on-the-edge-device

AI-on-the-edge-device is a project running on an ESP32-CAM and can be fully integrated into Home Assistant using the Home Assistant discovery functionality of MQTT. It digitalizes your gas/water/electricity meter display and provides its data in various ways.



### Using a CT clamp sensor

{% include energy/ct_clamp.md %}

### Data provided by your energy provider

Some energy providers will provide you real-time information about your usage and have this data integrated into Home Assistant.

### Manual integration

If you manually integrate your sensors, for example, using the MQTT or Template integrations: Make sure you set and provide the `device_class`, `state_class`, and `unit_of_measurement` for those sensors.

### Troubleshooting

If you are unable to select your energy sensor in the grid consumption drop-down, make sure that its value is being recorded in the Recorder settings.

Energy integrations

_Disclaimer: Some links on this page are affiliate links helping support the Home Assistant project._
