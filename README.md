# Description of our plan

## List of the team members

| Name           | GitHub account                  |
|:---------------|:--------------------------------|
| Luc Brun       | https://github.com/Luckyluuuc   |
| Manon Tregon   | https://github.com/Zimanon      |
| Cécile Luc     | https://github.com/cecilelc20   |
| Alexis Mourier | https://github.com/AlexisMourier|


## Starting Point

These two2 papers serve as the foundation of our project and significantly inspire our approach:
- **Paper 1** [Fuzzy Logic-Based Model That Incorporates Personality Traits for Heterogeneous Pedestrians] (https://www.mdpi.com/2073-8994/9/10/239)
- **Paper 2** [Emotion Contagion Model for Dynamical Crowd Path Planning] (https://www.sciltp.com/journals/ijndi/2024/3/521/320) - 

## Rough Sketch

We intend to use **Paper 1** to implement a pedestrian-walking model based on personality (using the famous OCEAN model) incorporating **fuzzy logic** to nuance subjects' personnalities. This approach is more realistic to the one presented in **Paper 2** where the OCEAN model is also taken into account but subjects belong to one of 5 well-separated categories. We'll also preview a way of solving a panic situation with this model. This should be done for the 1st deadline.

Later, we intend to implement **Paper 2**'s **emotion contagion model** in an attempt to be even more realistic and study the impact of other subjects' emotions as well as exterior factors on a given subject in a crowd. **Paper 1** appears limited in its implementation as it has only been tested on "normal" no-panic scenarios, and is not ideal for testing panic-scenarios. However, implementing panic-scenarios seems crucial to test safety infrastructures and limit life loss in certain scenarios. In case of a fire spreading in a closed room, for instance, this complex model incorporating subjects' personnalities and emotion contagion (spread of panic) could determine the optimal number of exit doors or exit routes. This will enable us to improve and complete our model; and we'll also take the opportunity to step back and check our methodology before the 2nd deadline.

As said before, we finally intend to **pick a panic scenario to test our model** at different stages and determine the optimal safety measures and infrastructures. Modeling crowds in concert halls or stadiums could be an interesting application of pedestrian-walking and crowd simulation. It could enable us to test our model at different stages and has a real importance as death caused by panick crowd movement are common and not isolated incidents at festivals or huge concerts. This is the last stage, where we'll actually experiment with our model and draw up a conclusion for the final deadline.




