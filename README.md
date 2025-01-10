# Description of our plan

## List of the team members

| Name           | GitHub account                  |
|:---------------|:--------------------------------|
| Luc Brun       | https://github.com/Luckyluuuc   |
| Manon Tregon   | https://github.com/Zimanon      |
| Cécile Luc     | https://github.com/cecilelc20   |
| Alexis Mourier | https://github.com/AlexisMourier|


## Starting Point

These two papers serve as the foundation of our project and significantly inspire our approach:
- **Paper 1** [Emotion Contagion Model for Dynamical Crowd Path Planning] (https://www.sciltp.com/journals/ijndi/2024/3/521/320) - 
- **Paper 2** [Fuzzy Logic-Based Model That Incorporates Personality Traits for Heterogeneous Pedestrians] (https://www.mdpi.com/2073-8994/9/10/239)


## Project Description

The primary objective of this project was to develop a more realistic crowd behavior model, building upon insights from two prior research studies.

To achieve this, we divided the project into three main phases:

1. **Baseline Model Development**: We started by designing a basic crowd-behavior model that allowed agents to exit a room using a scoring system to evaluate each accessible position in the environment. Additionally, agents accounted for local density to avoid being overwhelmed by the surrounding crowd.

2. **Incorporating Emotion Contagion**:
Next, we enhanced the model by introducing emotion contagion, aiming to simulate the emotional exchanges that naturally occur within dense crowds. This step required the development of a personality system to define distinct behavior types among agents.

3. **Incorporating Fuzzy Logic**:
Finally, we made the model even more realistic by replacing rigid if-then-else rules with fuzzy logic rules. These flexible rules are particularly well-suited for abstract concepts like emotions and personalities, enabling a more nuanced representation of human behavior.

## Goals and Achievements

All the features outlined above were successfully implemented.

Our goal was to create a crowd-behavior model that surpasses the realism of the two existing models that inspired our work. By "more realistic," we sought to better approximate real-world dynamics—an inherently challenging objective to quantify.

To evaluate our progress, we generated graphs based on various metrics (e.g., maximum crowd density, average exit speed for agents with specific personality traits, etc.). While some metrics produced intriguing results, the observed behaviors of the crowd often remained quite similar, regardless of the implemented improvements.


## How to run the simulation ?

### Step 1: Install the Environment  

Before running any program, make sure to install the environment associated with the project. Use the following command:  


`conda env create -f env.yml`


First and formost you should install the environment associated with the project before running any program : 

`conda env create -f env.yml`

Running the simulation is simple. Follow these steps:

### Step 2: Run the Simulation
Execute the visualisation.py script:

`python visualisation.py`

As the script runs, you'll see several prompts in your terminal. These questions allow you to customize the simulation environment. Filling them out is optional—you can skip them if you prefer.

After completing the prompts, a browser window will open automatically.

Click "Start," and enjoy watching the simulation in action!