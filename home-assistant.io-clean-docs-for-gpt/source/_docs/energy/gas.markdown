---
title: "Integrating your gas usage"
description: "Learn how to add information about your gas usage to Home Assistant home energy management."
---

Some homes are connected to gas. Gas is being used to heat water, cook and heat up the home.

Home Assistant allows you to track your gas usage and easily compare it against your energy usage for the same period of time.

## Hardware

Home Assistant will need to know the amount of gas that is being consumed.

### Connect to your meter

The best way to get this data is directly from your gas meter that sits between your house and the grid. In certain countries these meters contain standardized ways of reading out the information locally or provide this information via the electricity meter.

#### Connect using a P1 port

The P1 port is a standardized port on electricity meters in the Netherlands, Belgium and Luxembourg which also provides gas consumption information. A P1 reader can connect to this port and receive real-time information.

We have worked with creator Marcel Zuidwijk to develop SlimmeLezer+. It's an affordable P1 reader powered by ESPHome that will seamlessly integrate this information in Home Assistant. It is being sold on his website and the firmware is open source on GitHub.



#### Read the Gas Meter using an AI-on-the-edge-device

AI-on-the-edge-device is a project running on an ESP32-CAM and can be fully integrated into Home Assistant using the Home Assistant Discovery Functionality of MQTT. It digitalizes your gas/water/electricity meter display and provides its data in various ways. 



#### Read the Gas Meter using a magnetometer

Diaphragm/bellows gas meters are the most common type of gas meter, seen in almost all residential installations, and their movement can frequently be observed with a magnetometer. The QMC5883L and HMC5883L are common and inexpensive options that ESPHome supports. A project that makes it easy to use these magnetometers and calibrate them is this water-gas-meter project on GitHub.
