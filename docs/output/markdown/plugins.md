---
title: Plugins
layout: default
nav_order: 7
---

<!--

DO NOT EDIT
-----------
This file is auto-generated.
To update it, consult instructions:
https://github.com/acceleratedscience/open-ad-toolkit/tree/main/docs

-->

# OpenAD Plugins

Plugins are how molecular tools and AI models are made available to the OpenAD client. They provide drastically simplified access to a series of advanced tools, and they make it easy for your own Python applications to interface with OpenAD.

Creating your own plugins is easy if you have a basic understanding of Python.

<br>

### Creating Your Own Plugin
You can create your first plugin in just minutes. This creates the ability for your own projects (or your favorite tools) to access OpenAD's powerful visualisation capabilities and more.

We will be publishing a detailed tutorial soon on this page.

<br><br>

## Available Plugins

Currently there are two publicly available plugins available.

1. **Deep Search**<br>
    Find molecules by similarity or substructure, scan patents for molecules and vice versa and search across available Deep Search collections.<br>
    More information about this plugin can be found in the [openad-plugin-ds](https://github.com/acceleratedscience/openad-plugin-ds) repo.

        pip install git+https://github.com/acceleratedscience/openad-plugin-ds

   <br><br>
1. **RXN**<br>
    RXN helps you predict chemical reactions, retrosynthesis pathways and experimental procedures.<br>
    More information about this plugin can be found in the [openad-plugin-rxn](https://github.com/acceleratedscience/openad-plugin-rxn) repo.

        pip install git+https://github.com/acceleratedscience/openad-plugin-rxn
