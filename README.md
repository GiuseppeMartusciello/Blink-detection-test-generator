# Automated Test Generation for Blink Detection in Simulated Driving (Unreal Engine)

This repository implements the tool described in the thesis “Automated Test Generation for Blink Detection Algorithms in Simulated Environments”. It automatically produces video test cases for blink-detection algorithms in a driving-like scene, minimizing manual work through two Editor Utility Widgets and Python scripting integrated in Unreal Engine.

## Context and motivation
Public datasets for blink detection often lack duration, variability, and controllable conditions. A simulated pipeline in Unreal Engine overcomes these limits by generating repeatable, scalable test cases with systematic variations.

## Objective
Generate customized video sequences for validating blink detection, varying scene parameters and the blink timings, and automating configuration and rendering to obtain coherent, reproducible datasets with low operator effort.

## Main components (located under Content/Widget)
1) Configuration and rendering widget  
   Lets you set scene options (glasses on/off, street lights on/off, IR camera on/off, time-of-day), choose the active MetaHuman from a dropdown, enter blink timings, and start rendering for the selected MetaHuman or for all MetaHumans. 

2) Automatic combinations widget  
   You provide only the blink timings; the widget iterates all MetaHumans and generates the full set of variants by toggling glasses, lights, IR camera, and day/night automatically.

## Naming
Outputs are saved under Saved/MovieRenders and named with a parameter-encoded convention such as:  
`1,MetaHuman=BP_Glenda,Glasses=false,Lights=false,IrCamera=false,TimeOfTheDay=12.0`  
Videos are produced in .mp4 with uniform settings across variants. 

## Getting started
1. Open the Unreal project.  
2. Go to Content/Widget and launch the configuration widget. Set time-of-day, lights, glasses, IR camera, select a MetaHuman, enter blink timings, then press Synchronize.  
3. Choose Render Selected (single MetaHuman) or Render All (iterate over all).  
4. Alternatively, use the automatic combinations widget: provide only blink timings and start the full batch.

## Requirements
Software
- Windows 10/11  
- Unreal Engine 5.x (tested with UE5; Sequencer and Movie Render Queue are used)  
- Unreal Python scripting enabled (Edit → Plugins → enable Python)  
- Editor Utility Widgets enabled (Edit → Plugins → Editor Scripting Utilities / Editor Utility Widgets)  

Hardware
- Dedicated GPU with sufficient VRAM for 1080p/1440p rendering  
- Adequate CPU cores and RAM for Movie Render Queue batches

Project assets
- MetaHumans are not included in this repository to keep it lightweight and due to licensing constraints. The folder Content/MetaHumans is present but empty in version control; download the required MetaHumans via https://drive.google.com/drive/folders/1m0-CrSsiCE_mmlQJdEvPxP8JhnDnB0i9?usp=drive_link and place them under Content/MetaHumans before rendering.

## Rendering notes
Use Movie Render Queue for consistent results. Outputs are written to Saved/MovieRenders and automatically renamed based on the active configuration. Typical 30 seconds single-video render time during validation was roughly 1 minute 40 seconds, depending strongly on hardware. 

## Dataset and rendered results on Zenodo
Rendered videos and metadata are archived on Zenodo.  
Title: Simulated Driving Environment Video Dataset for Blink Detection  
DOI: https://doi.org/10.5281/zenodo.17045195
If you use the dataset, please cite the Zenodo DOI.

## Repository layout (indicative)
[repo root]  
├─ Config  
├─ Content  
│  ├─ MetaHumans        (present, contents must be restored locally)  
│  ├─ Sequences  
│  └─ Widget            (Editor Utility Widgets)  
├─ Python             (Python automation)  

## License and copyright
Repository code and project configuration: All rights reserved.
Rendered dataset on Zenodo: Creative Commons Attribution 4.0 International (CC BY 4.0)  
Copyright © 2025 Giuseppe Martusciello

## Citation
Giuseppe Martusciello. 2025. Simulated Driving Environment Video Dataset for Blink Detection. Zenodo. https://doi.org/10.5281/zenodo.17045195
