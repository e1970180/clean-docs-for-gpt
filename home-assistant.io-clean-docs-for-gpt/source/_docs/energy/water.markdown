---
title: "Integrating your water usage"
description: "Learn how to add information about your water usage to Home Assistant home energy management."
---

Home Assistant allows you to track your water usage in the home energy management too.

Although water usage is not strictly "energy", it is still a valuable resource to track and monitor as it is often tightly coupled with energy usage (like gas). Additionally, it can help you reduce your ecological footprint by using less water.

### Home water meters

There are several ways to measure water usage in your home. Multiple methods exist for reading your water usage. Older water meters typically feature a common arrow or only display total consumption. For these meters, you may require an AI-on-the-edge-device with an ESP32 camera. While effective, this solution can be tedious to set up as it leans towards a DIY approach.

Newer water meters are equipped with a rotary disk that can be read using two methods. The first method utilizes light sensors, while the second method employs proximity sensors. The proximity sensor detects changes in the magnetic field, with each rotation of the disk representing one liter of water used. Meanwhile, the light sensor method operates on an autocorrelation technique, providing accuracy down to 100 milliliters instead of the traditional one-liter step.

For most water meters, the rotary encoder disk suffices the light sensor version. However, some older or specialized meters may necessitate the use of a proximity meter instead.

Home Assistant also has integrations build into the platform that connect with existing products

## Home Assistant integrations

Home Assistant will need to know the amount of water that is being consumed to be able to track usage. Several water metering (fluid flow rate sensor device) hardware options are available to do this. Depending on your setup, the required hardware is provided by your public water utility company, or you may need to buy your own. 

Some hardware with water meters may also provide additional practical functions or sensors, such as valve, for example, for controlling water shutoff, or temperature and pressure (to enable freeze alarms).

We have the following integrations available for existing products that can provide information about water usage:

- Flo
- Flume
- HomeWizard Energy
- StreamLabs
- Suez Water

There are also products for water usage monitoring that are based on existing common IoT protocol standards:

- Z-Wave
- Zigbee
- Matter


## Community-made sensors

If your water meter lacks a rotary disk, magnetic disk, or coil. There are alternative solutions available to seamlessly integrate water monitoring into your smart home setup:

- AI-on-the-edge-device is a project running on an ESP32-CAM and can be fully integrated into Home Assistant using the Home Assistant Discovery Functionality of MQTT. It digitalizes your gas/water/electricity meter display and provides its data in various ways.!Photo of the AI-on-the-edge-device Workflow, `Gallons Per Minute` (gal/min), and `Gallons to Recharge` (gal):

- cullAssistant (ESPHome)

Alternatively, the following shops sell ESPHome-based devices that use a 3-phase light sensor to detect a rotating disk in your water meter and convert this to the amount of water used in milliliters (ml):
- Muino water meter reader (ESPHome)

Alternatively, the following shops sell ESPHome-based devices, that use a proximity sensor to detect a rotating magnet in your water meter and use that pulse to count each liter of water used:
- S0tool ("Made for ESPHome" approved)
- Waterlezer dongle (Dutch)
- Slimme Watermeter Gateway (Dutch)
- watermeterkit.nl (Dutch)

## DIY

Maybe you like to build one yourself?
- Pieter Brinkman has quite a nice blog article on how to create your own water sensor using ESPHome, or build a water meter that works with the P1 Monitor integration.
- AI-on-the-edge-device is a project running on an ESP32-CAM and can be fully integrated into Home Assistant using the Home Assistant Discovery Functionality of MQTT. It digitalizes your gas/water/electricity meter display and provides its data in various ways.
- watermeter running classic OCR and statistical pattern recognition on any system supporting Docker
- Muino water meter reader 3-phase Using the 3-phase sensor technique, a battery-powered version can be possible with this sensor.
- Read water meter with magnetometer using QMC5883L or HMC5883L, common and inexpensive magnetometers. This should be compatible with all the water meters the Flume water sensor is compatible with, which is compatible with about 95% of water meters in the United States.
- Some watermeters use Wireless M-Bus for remote metering. wmbusmeters project can automatically capture, decode, decrypt and convert M-Bus packets to MQTT. It supports several M-Bus receivers, including RTL-SDR using rtl-wmbus library. You can also build a WMBus ESPHome-based receiver. An add-on for Home Assistant exists for easy installation and configuration. See the community page for more.
- Read water (or gas) usage data from the Itron EverBlu Cyble Enhanced RF meters using the RADIAN protocol over 433 MHz everblu-meters-esp8266/esp32, via an ESP32/ESP8266 and a CC1101 transceiver. Used across the UK and Europe. Fully integrates with Home Assistant using MQTT AutoDiscovery. According to available documentation, this method may also work with AnyQuest Cyble Enhanced, EverBlu Cyble, and AnyQuest Cyble Basic, but these remain untested.

If you manually integrate your sensors, for example, using the MQTT or RESTful integrations: Make sure you set and provide the `device_class`, `state_class`, and `unit_of_measurement` for those sensors.

For any of the above-listed options, make sure it actually works with the type of water meter you have before getting one.
