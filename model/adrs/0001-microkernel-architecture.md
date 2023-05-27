# 1. Microkernel architecture

Date: 2023-4-19

## Status

~~Accepted~~ --> Invalid

## Summary  

*In the context of* delivering an word memorize software,  
*facing* the proposal proposed by the project proposal, a third party can expand the functions according to our architecture,  
*we decided* to to use microkernel architecture to improve extensibility,  
*to achieve* consistent logical behaviour across platforms,  
*accepting* potential complexity of interfaces to different platforms.

## Context

- The system will have a front-end and a back-end.
    - The front-end can complete complex logical behaviors according to the user's behavior, generate an instruction and send it to the back-end to query the dictionary
    - The back-end only needs to be responsible for executing the instructions transmitted by the front-end and connecting to the database, and then sending back data such as dictionary definitions
- Delivering functional requirements requires complex processing and database transactions.
    - Progress based on both a user's history and behaviour.
    - Recording all users' word history.
    - Team fuction.
    - In order to ensure security, an expirable token should be generated when the user logs in and then stored in redis
- Development team has experience using Python.

## Decision

All logic will be implemented in front-end of the software architecture.
Web and mobile applications will implement the interaction tier.
Front-end communicate with the back-end to access database.
This provides clear separation of concerns and ensures consistency of logic across front-end and back-end.

The front-end logic will be implemented in React.
The back-end logic will be imeplemented in Python.
The project will be deployed on AWS。
The data would store in PostgreSQL on AWS.
This suits the current development team's experience and is a common environment.

## Consequences

Advantages
- After the user caches the dictionary, it can be used locally without networking
- Reduced the servers load
- If the users hardware is good, the responsiveness would increaseconsumes more memory on the user's system

Disadvantages
- The development team lacks front-end development experience.
- The front-end load was increased
- Would consumes more memory on the user's system
