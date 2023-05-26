# Don't Remember
[Original Proposal](https://csse6400.github.io/project-proposal-2023/s4786694/proposal.html)
## Abstract

## Proposal Clarification
[ ] Study plan in proposal and here

## Changes
The project proposal implied that the functionality should be displayed through web or mobile application. As a proper UI is not needed to meet the evaluation criterias, it was decided that the functionality would be implemented through APIs. The functionality was decided to be demonstrated with a CLI application.
[ ] Change of the level of English Study
[ ] Choose the vocabulary book
[ ] Dynamatically change the study plan

## Architecture
The architecure is a Service-based Architecture



## Trade-Offs

## Critique

## Evaluation
### Security Tests
To address security concerns, we have implemented access control for user data. To use the functionality users must generate a token with the /login endpoint of the users API. We have created a suite of automated tests to test if the tokens can provide all information of a user, and if user's data is protected by the token.

### Functionality Tests
A suite of automated tests check if the implemented function provide the correct input.

### Availability Tests
The following tests aim to determine the longevity of the service. Due to time limitation, we test whether our application can run for a full day.

### Maintainability Tests
To support the future of our application, we try to test if our architecture can hold up for future test cases. One case is database migrations, where we have implemented functionality for this, incase we want to configure out databases in the future. 


### Scalability Tests
We test how our architecture handles high loads.

## Reflections