# 1. Microkernel architecture

Date: 2023-4-19

## Status

Accepted

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
    - Product recommendations based on both a customer's history and on purchasing behaviour of similar customers.
    - Recording all customer interactions in the application.
- Sales department wants customers to be able to change between using mobile and web applications without interrupting their sales experience.
- Development team has experience using Java.

## Decision

All business logic will be implemented in its own tier of the software architecture.
Web and mobile applications will implement the interaction tier.
They will communicate with the backend to perform all logic processing.
This provides clear separation of concerns and ensures consistency of business logic across frontend applications.
It means the business logic only needs to be implemented once.
This follows good design practices and common user interface design patterns.

The business logic will be implemented in Java.
This suits the current development team's experience and is a common environment.
Java has good performance characteristices.
Java has good support for interacting with databases, to deliver the data storage and transaction processing requirements.

## Consequences

Advantages
- After the user caches the dictionary, it can be used locally without networking
- Reduced the servers load
- If the users hardware is good, 
Neutral
- Multiple interfaces are required for different frontend applications.
  These can be delivered through different Java libraries.

Disadvantages
- Additional complexity for the overall architecture of the system.
