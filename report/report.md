# Don't Remember

[Original Proposal](https://csse6400.github.io/project-proposal-2023/s4786694/proposal.html)

## Abstract

## Proposal Clarification

- This section is used to explain some of the unclear content described in the proposal.
- In the [proposal scope](https://csse6400.github.io/project-proposal-2023/s4786694/proposal.html#scope), it says
  _User preference, including change the level of English study._ In here, The _change the level of English study_ means
  two functions: 1. Users should know the study progress of each day. 2. The system should automatically choose the word
  that user need to learn each day.
- In the [proposal scope](https://csse6400.github.io/project-proposal-2023/s4786694/proposal.html#scope), it says
  _dynamically change the studying plan_. It means the same as the _change the level of English study_ in the proposal.       which is that the system should automatically choose the word that user need to learn each day.
- In the following sections, we will use _study plan_ or _plan_ to indicate the number of words a user set to learn each       day.

## Changes

- In the proposal, it says _choose the vocabulary book(example: IELTS,Oxford)_. For the copyright constraint, we
  selected
  an opensource dictionary [WordSet](https://github.com/wordset/wordset-dictionary) as our dictionary.
- In the proposal, it says:

> when user have a period of time without using this software to study, it will decrease the new daily words and show
> more learned words to review. And if user learn new words quickly in recent days, it will increase the difficulty and
> show more new words in the future study.

There is no scientific way found to determine the difficulty of a word, we decided to allow users to add their own word,
they can also delete word if they want.

## Scope
The MVP should be able to:
- Basic Functionality
  - Signup/Login/Logout
- Word Learning
  - Add/Delete word they want to learn/
  - Update word status (choose "remember" or "forget" a word)
  - Show personal progress
  - Set personal plan
  - Show word learning history
- Team Learning
  - Build new team/Add me to a team/leave a team
  - Set team plan
  - Check team information (including team members, team progress, team plan).


## Architecture

The architecure is a Service-based Architecture

## Trade-Offs

## Critique

## Evaluation

### Security Tests

To address security concerns, we have implemented access control for user data. To use the functionality users must
generate a token with the /login endpoint of the users API. We have created a suite of automated tests to test if the
tokens can provide all information of a user, and if user's data is protected by the token.

### Functionality Tests

A suite of automated tests check if the implemented function provide the correct input.

### Availability Tests

The following tests aim to determine the longevity of the service. Due to time limitation, we test whether our
application can run for a full day.

### Maintainability Tests

To support the future of our application, we try to test if our architecture can hold up for future test cases. One case
is database migrations, where we have implemented functionality for this, incase we want to configure out databases in
the future.

### Scalability Tests

We test how our architecture handles high loads.

## Reflections
