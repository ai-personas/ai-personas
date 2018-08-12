# AI Personas

AI Personas is the architecture and framework for AI design. This structure allows to design AI personas with various network structures, environments and inter persona communication. Human persona behaviours defined by the DNA and environments, so AI personas modeled based on this concept.

The AI persona structure follows as:
## DNA
  The persona DNA defined here. DNAs definitions are specific to how the neural structure and processing implemented.With respect to deep learning it will be set of inputs, layers, outputs and its connections. The DNA wil be used in persona design and could be reused in any persona design.
  
## Environment
  The environment is where AI persona to grow up. It contains informations (like text, images, audio, video etc.) and load, extract, transformation scheme to consume these data. Also, environment has society which is individual persona, group of personas, communities, teams etc., The newly created persona can be included in any group, community, team and in this way, that persona behaviour will be enhanced and modulated. The persona could join the team as well to accomplish coordinated work and learn the multitude. 
  
  The persona character defined in two ways. One by DNA and other by what kind of environment it exposed.

  * [Informations](https://github.com/ai-personas/ai-personas/tree/master/Environment/Informations)  
  * [Society](https://github.com/ai-personas/ai-personas/tree/master/Environment/Society)
  
## Personas
  The personas defined here. The persona structure follows by its category and name and each persona has definition which includes multiple age defintion files. At age 0, the DNA and basic parameters will be defined and then subsequent age definitions will include more enviroment details, learning parameters etc., but DNA cannot be altered. 
  
## Physical
  The physical is responsible to create actual persona using persona definition file. The soft implementations could be based on the existing frameworks such as theano, tensorflow, caffe, keras etc.,
  
## Power
The power is responsible to fuel Physical. For soft physical, it would be set of servers/clouds APIs to execute physical for given persona and generate outputs.
