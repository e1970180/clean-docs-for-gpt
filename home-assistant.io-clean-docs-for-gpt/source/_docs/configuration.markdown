---
title: "Configuration.yaml"
description: "Configuring Home Assistant via text files."
related:
  - docs: /docs/configuration/yaml/
    title: YAML syntax
  - docs: /docs/configuration/secrets
    title: Storing credentials in `secrets.yaml` file
  - docs: /common-tasks/general/#backups
    title: Creating and restoring backups
  - docs: /integrations/backup/docs/tools/dev-tools/#reloading-the-yaml-configuration
    title: Creating backups for Home Assistant Container and Core
  - docs: /docs/tools/dev-tools/#reloading-the-yaml-configuration
    title: Reloading the YAML configuration from developer tools
  - docs: /common-tasks/os/#configuring-access-to-files
    title: Configuring file access on the Operating System
  - docs: /common-tasks/supervised/#configuring-access-to-files
    title: Configuring file access on Supervised
  - docs: docs/configuration/troubleshooting/
    title: Troubleshooting the configuration
---

While you can configure most of Home Assistant from the user interface, for some integrations, you need to edit the `configuration.yaml` file.

This file contains {% term integrations %} to be loaded along with their configurations. Throughout the documentation, you will find snippets that you can add to your configuration file to enable specific functionality.



Example of a configuration.yaml file, accessed using the File editor add-on on a Home Assistant Operating System installation.


## Editing `configuration.yaml`

How you edit your `configuration.yaml` file depends on your editor preferences and the installation method you used to set up Home Assistant. Follow these steps:

1. Set up file access.
2. Locate the config directory.
3. Edit your `configuration.yaml` file.
4. Save your changes and reload the configuration to apply the changes.

### To set up access to the files and prepare an editor

Before you can edit a file, you need to know how to access files in Home Assistant and setup an editor.
File access depends on your installation method. If you use {% term "Home Assistant Operating System" %} or {% term "Home Assistant Supervised" %}, you can use editor add-ons, for example, but not if you use {% term "Home Assistant Core" %} or {% term "Home Assistant Container" %}.

To set up file access, follow the steps for your installation method:

- Configure file access on the Operating System:
  - If you are unsure which option to choose, install the file editor add-on.
  - Alternatively, use the Studio Code Server add-on. This editor offers live syntax checking and auto-fill of various Home Assistant entities. But it looks more complex than the file editor.
  - If you prefer to use a file editor on your computer, use the Samba add-on.
- Configure file access on Supervised:
  - Using the File editor add-on.
  - Using the Studio Code Server add-on.
  - Using the Samba add-on.

### To find the configuration directory

1. To look up the path to your configuration directory, go to {% my system_health title="**Settings** > **System** > **Repairs**" %}.
   - Select the three dots menu and select **System information**.

    

2. Find out the location of the **Configuration directory**.

    
   - Unless you changed the file structure, the default is as follows:     - 
     - {% term "Home Assistant Operating System" %}: the `configuration.yaml` is in the `/config` folder of the installation.
     - {% term "Home Assistant Container" %}: the `configuration.yaml` is in the config folder that you mounted in your container.
     - {% term "Home Assistant Core" %}: the `configuration.yaml` is in the config folder passed to the `hass` command (default is `~/.homeassistant`).
3. Once you located the config folder, you can edit your `configuration.yaml` file.

{% note %}

If you have watched any videos about setting up Home Assistant using `configuration.yaml` (particularly ones that are old), you might notice your default configuration file is much smaller than what the videos show. Don't be concerned, you haven't done anything wrong. Many items in the default configuration files shown in those old videos are now included in the `default_config:` line that you see in your configuration file. Refer to the default config integration for more information on what's included in that line.

{% endnote %}

## Validating the configuration

After changing configuration or automation files, you can check if the configuration is valid. A configuration check is also applied automatically when you reload the configuration or when you restart Home Assistant.

The method for running a configuration check depends on your installation type. Check the common tasks for your installation type:

- Configuration check on Operating System
- Configuration check on Supervised
- Configuration check on Container
- Configuration check on Core

## Reloading the configuration to apply changes

For configuration changes to become effective, the configuration must be reloaded. Most integrations in Home Assistant (that do not interact with {% term devices %} or {% term services %}) can reload changes made to their configuration in `configuration.yaml` without needing to restart Home Assistant.

1. Under **Settings**, select the three dots menu (top right) {% icon "mdi:dots-vertical" %}, select **Restart Home Assistant** > **Quick reload**.

   

2. If you find that your changes were not applied, you need to restart.
   - Select **Restart Home Assistant**.
   - Note: This interrupts automations and scripts.

   

## Troubleshooting the configuration

If you run into trouble while configuring Home Assistant, refer to the configuration troubleshooting page.
