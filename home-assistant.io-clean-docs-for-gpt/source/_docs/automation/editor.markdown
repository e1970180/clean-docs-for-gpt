---
title: "Automation editor"
description: "Instructions on how to use the automation editor."
related:
  - docs: /getting-started/automation/
    title: Automating Home Assistant
---

The automation editor is an easy way of creating and editing automations from the UI.

This tutorial uses the Random sensor because it generates data (by default, values between 0 and 20). This enables us to walk through the example, even if you do not have any actual sensors connected yet. You could use any other sensor that outputs a numeric value.

1. Go to {% my automations title="**Settings** > **Automations & scenes**" %} and in the lower right corner, select the **Create Automation** button.
2. Select **Create new automation**.

    

3. Select **Add Trigger**, and in the **Search trigger** field, type "num".
   - Select **Numeric state**.

    

4. Enter the trigger conditions:
   - Define the sensor: Under **Entity**, enter "sensor.random_sensor".
   - If the sensor value is above 10, we want the automation to trigger.
     - In the **Above** field, enter "10".

    

5. Define the action that should happen:
   - In the **Then do** section, select **Add Action**.

     

6. We want to create a persistent notification.
   - Enter "No" and select **Notifications: send a persistent notification**.

    

7. As the message, we want a simple text that is shown as part of the notification.

    ```yaml
    message: Sensor value greater than 10
    ```

8. Select **Save**, give your automation a meaningful name, and **Save** again.

    

    - **Result**: Automations created or edited via the user interface are activated immediately after saving the automation.
    - To learn more about automations, read the documentation for Automating Home Assistant.

## Troubleshooting missing automations

When you're creating automations using the GUI and they don't appear in the UI, make sure that you add back `automation: !include automations.yaml` from the default configuration to your {% term "`configuration.yaml`" %}.
