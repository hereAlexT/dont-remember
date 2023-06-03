# Don't Remember

[Original Proposal](https://csse6400.github.io/project-proposal-2023/s4786694/proposal.html)

## Abstract

This document presents the design, implementation, and evaluation of "Don't Remember," an English vocabulary learning
application. The project aims to provide users with a personalized and efficient learning experience, allowing them to
track their progress, set personal goals, and collaborate with teams. To achieve this, we have employed a microservices
architecture, utilizing AWS ECS, Amazon Elastic Load Balancers, and a PostgreSQL database. The system landscape includes
users, other tools, and the Don't Remember software system, which interact through dedicated APIs.

Throughout the development process, we have focused on ensuring security, reliability, availability, maintainability,
scalability, and extensibility. We have adopted JSON Web Tokens (JWT) for secure token generation and verification, and
implemented auto-scaling policies to maintain system availability and scalability. The use of Terraform for
infrastructure management has improved maintainability, while the microservices architecture has enhanced extensibility.

The document also discusses trade-offs, critiques, and reflections on the project, highlighting the lessons learned and
potential improvements for future projects. The evaluation section covers various tests conducted to assess the system's
functionality, security, availability, maintainability, and scalability. Overall, the "Don't Remember" application
demonstrates the effectiveness of a well-designed architecture and the importance of considering quality attributes in
software development.

## Proposal Clarification

- This section is used to explain some of the unclear content described in the proposal.
- In the [proposal scope](https://csse6400.github.io/project-proposal-2023/s4786694/proposal.html#scope), it says
  _User preference, including change the level of English study._ In here, The _change the level of English study_ means
  two functions: 1. Users should know the study progress of each day. 2. The system should automatically choose the word
  that user need to learn each day.
- In the [proposal scope](https://csse6400.github.io/project-proposal-2023/s4786694/proposal.html#scope), it says
  _dynamically change the studying plan_. It means the same as the _change the level of English study_ in the proposal.
  which is that the system should automatically choose the word that user need to learn each day.
- In the following sections, we will use _study plan_ or _plan_ to indicate the number of words a user set to learn each
  day.

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

### System Landscape

<img src="../model/dont-remember-system-landscape-architecture.png" width="600" alt="System Landscape">
In the diagram above, we observe two distinct software systems and one role represented within the system landscape of Don't
Remember, which also includes users, other tools, and Don't Remember. As Don't Remember is a business-to-business (ToB)
project, the _user_ role primarily symbolizes staff members.

The _Other Tools_ software system embodies a suite of compliant and personalized software integrated within the
company's server infrastructure. Staff can utilize these tools to interact with the Don't Remember software system.
Alternatively, they can also use a built-in Command Line Interface (CLI) within Don't Remember to communicate with the
system. However, it's worth noting that this CLI is primarily intended for demo purposes; therefore, we generally advise
against its regular use.

Lastly, the _Other Tools_ system interfaces with the Don't Remember system through a set of dedicated APIs. As such, a
streamlined interaction is established, further facilitating user engagement.

### Don't Remember Software System

<img src="../model/dont-remember-software-system-architecture.png" width="400" alt="Software System Architecture"><br>
Our software system provides a CLI tool for demonstration purposes. User requests can originate from this CLI tool or
other tools. Initially, these requests reach the Amazon Elastic Load Balancers. Subsequently, these requests are
redirected to the auto-scaling group that hosts two microservices: the Users Microservice and the Words Microservice.
Both services can directly communicate with the database.

#### Load Balancers

The load balancers use two rules to manage traffic:

- Requests directed to `/api/v1/users/*` or `/api/v1/users` are forwarded to the Words Microservice.
- Requests directed to `/api/v1/words/*` or `/api/v1/words` are forwarded to the Users Microservice.

#### Services

The Users Microservice and Words Microservice are hosted on AWS ECS, with auto-scaling policies in place. Each Service
is using Flask as the web framework, gunicorn as the WSGI server. And each service is stateless, all the stateful data
is
stored in the database.

The Users Microservice handles user and team-related requests, specifically:

- Add/Delete word they want to learn
- Update word status (choose "remember" or "forget" a word)
- Show personal progress
- Set personal plan
- Show word learning history

On the other hand, the Words Microservice handles word-related tasks:

- signup/login/logout
- Build new team/Add me to a team/leave a team
- Set team plan
- Check team information (including team members, team progress, team plan).

#### Database

We use a Postgres database to store all the data. This includes user information, user's learning
word records, learning history, team information, and team members and so on.

#### CLI tool

A Python-based CLI tool is available for demonstration purposes. It encompasses all the functionalities mentioned within
the scope.

### How does it achieve Quality Attributes?

#### Security

In the "Don't Remember" project, we enhance security through the use of Tokens and JWT. Tokens serve as proof of
identity and authorization; users carry them in their subsequent requests, and our servers validate these Tokens to
confirm identities. Furthermore, JWT, with its self-contained nature, contains all necessary information, reducing the
need for constant database queries. This design enables secure and efficient identity verification, authorization, and
cross-domain authentication, all while significantly bolstering the system's security.

#### Reliability

Our architectural design is fault-tolerant, for the reason that firstly, we use AWS ECS to host our services, which
provides auto-scaling policies, when requests increases, the ECS will scale up to make sure the system caused no time
out fault. Secondly, there is a health endpoint in each service, the load balancer will check the health of each
service,
if one service is down, the load balancer will redirect or start a new service.

#### Availability

- An auto-scaling policies are in place to ensure the availability of the system. When the number of requests increases,
  the ECS will scale out to make sure the system is always available.
- Similar to Reliability, there is a health endpoint in each service, the load balancer will check the health of each
  one, if fails, new service will be started.

#### Maintainability

Terraform is used to manage the infrastructure, which makes it easy to maintain and update. ECS is used, when update, we
only need to update the docker image, and the ECS will automatically update the service.

#### Scalability

- AWS ECS is used with auto-scaling policies.
- Microservices architecture is used, when requests to one microservice are increased, it can be scaled easily.

#### Extensibility

In the "Don't Remember" project, scalability is predominantly showcased through our use of a microservices architecture.
Leveraging the inherent decoupling characteristics of this architecture, we can add new functionalities by simply
creating a new microservice. Additionally, we provide well-defined and decoupled endpoints, making it convenient for
future developers to build new features based on this foundation. Moreover, the employment of JWT alleviates server
load, freeing up more resources for potential service expansion.

## Trade-Offs

### Three Token Verification Strategies: Redis, PostgreSQL, and JWT

Initially, we introduced tokens for security purposes. Each user is assigned a token with a set expiration time upon
login. Below, we outline three different strategies for token verification:

The first strategy involves storing tokens in Redis. This approach is advantageous due to its speed and the benefit of
having a separate service, simplifying maintenance. However, for a minimum viable product (MVP), this strategy is likely
too costly in terms of development.

Consequently, the second strategy is to store tokens in a PostgreSQL database. Compared to Redis, this is a more
cost-effective solution, and its speed suffices for the MVP. Nonetheless, it does present a potential security risk in
the event of a database leak.

The final strategy utilizes JSON Web Tokens (JWT) to automatically generate tokens. These tokens don't require storage
and are encapsulated in the HTTP request headers. This approach is not only more secure but also less
development-intensive than the previous two methods. However, it comes with a functional drawback: it does not support
server-side logout.

In consideration of speed, development cost, security, and functionality, we have ultimately decided to use JSON Web
Tokens (JWT) for token generation and verification, despite its inability to support server-side logout.

### Choosing the Optimal Database Strategy for MVP Development

In terms of database design, we considered two different strategies.

The first strategy involved using a hybrid approach: storing the user table in PostgreSQL, and the wordslist and
Dictionary tables in Amazon DocumentDB. Owing to its NoSQL nature, Amazon DocumentDB provides stable, low-latency read
and write performance, which is superior compared to relational databases like PostgreSQL. However, this approach poses
significant challenges for our MVP development: the cost of utilizing Amazon DocumentDB is high, and the execution of
joint queries with User data stored in PostgreSQL can be complicated.

The alternative strategy was to store all tables in PostgreSQL. This option offers a more cost-effective solution that
aligns well with the budget constraints of our MVP development. Given these considerations, we've decided to adopt this
second strategy, consolidating all our tables within a single PostgreSQL database.

### Deciding Between Separate or Combined Microservices for Team and User Functions

Should Team and User function be seperated into two microservices?

- Separate Team and User as Two Microservices
    - Pros:
        - Easy to development, each microservice only need to handle one type of request.
    - Cons:
        - Developing two microservices will increase development costs.
        - Our current database has a capacity of 300 connections; separating them will establish more connections when
          scaling out, necessitating a database upgrade.
        - Need a method a figure how to communicate between Team and User, because they are highly related.
- Put Team and User in the Same Microservices
    - Pros:
        - Lower development and deployment cost.
        - Easier communication between Team and User.
        - The current database capacity of 300 connections is sufficient.
    - Cons:
        - Potential deployment waste, since requests to users are more frequent than requests to teams.
          Considered this is a MVP, we decided to put Team and User in the same microservice.

## Critique

### Security

JWT is able to secure the data of the users in the API. All tests currently pass for security, the api is able to
retrieve user information with a token. Without a token no information can be retrieved, as the token is also used to
identify the user making the request. Additionally there is an expiration time on the token, and it is confirmed by the
tests that the user can not use an expired token to retreive information. There are some long term concerns with this
API's JWT implementation. If a account if comprimised in the future, there is no current method to revoke access to any
tokens created by the account. So a malicious user can still retrieve data with a stolen token until it expires. This
will be be balance of the expiration time of the token. It must be set to a time where it will not inconvenience the
user, but also protect them if their account is comprimised.

### Functionality

Well designed and comprehensive unit tests are passed as well as manual tests by CLI tool which shows that the app is
running as expected.

### Scalability and Availability

Our architecture can scale up well with ECS and load balancing. The conclusion of tests show that our we can handle high
loads as long as there is enough time to warm up and and we are able to spawn enough instances. At max loads, the user
API has to spawn mutliple instances, and our tests were limited by the number of instances we could spawn. However, the
word API did not need as many resources. So, as long as users are able to login and signup, they are able to study their
words without issues. The only times our product would suffer outages or slow speeds, is if there is a sharp spike in
users signing up, and after few it would normal as more instances are spawned, and we can go past the 22 maximum limit.
Due to this, it would be abnormal for our product to be down, and our architecure can scale up well.

For the availability, our scalability tests prove that it can handle a steady ammount of users at once. And as further
evidence we show that our availability test is able to run uninterupted for a whole day. This test was done while
testing was still happening, so it was able to do it with some activity. The only thing we are not sure of is how a
steady number of concurrent users over a much longer period of time effects our services.

### Extensibility

Microservices and well-designed decoupled API endpoints make the software extensible. Microservices make the system easy
to extend new functions without the impact of previous services. Decoupled API endpoints make the client can customize
the
workflow. Besides, an endpoint `/word_history` endpoint, provide detailed records of the learning, the clients could
utilize
it to do stuff such as draw a user's forget curve.

### Maintainability

While microservices architecture offers advantages such as modularity, independent deployment, and technology diversity,
it also introduces complexities of distributed systems, increased communication overhead, distributed transaction
management, and operational challenges. These factors should be carefully considered and evaluated based on specific
needs and team capabilities when adopting microservices. In our deployment structure, we have utilized AWS combined with
Terraform, which provides ease of maintenance. Additionally, the user and word services are decoupled, ensuring that
maintenance activities do not impact each other. Furthermore, our current system lacks the capability to perform
database schema updates workflow, which may potentially affect maintainability.

## Evaluation

### CLI Tool Test

#### Test Plan

The purpose of this test is to recreate user scenarios. This test includes all functions of Don’t Remember, simulations
have been conducted for every possible usage scenario of the user, and every step of the user's operation has been
simulated in the results.

#### Test Link

- [CLI Tool Test](cli_tool_test_logs.md)

#### Results

All commands return normal results. Functions in the demonstration are all runned normally. The actual test results
match the expected results.

### Security Tests

All tests are made using the pytest library, and can be run with the command "pytest [filename]"

#### Test Plan

To address security concerns, we have implemented access control for user data. To use the functionality users must
generate a token with the /login endpoint of the users API. We have created a suite of automated tests to test if the
tokens can provide all information of a user, and if user's data is protected by the token.

First the suite tests whether the token is able to be used to use the functionality of the words API. Then it tests
whether the word API can be used without a token, passing if it doesn't leak any information. Then the final test waits
for the token to expire and then tests if every endpoint is able to be accessed with an expired token.

#### Test Link

- [Security Tests](../tests/test_security.py)

#### Results

<br>
<img src="./images/test_security.png" width="400" alt="Test Result of Security Tests">

### Functionality Tests

#### Test Plan

Test every functionality of the system, which includes all the functionalities mentioned in the scope. We think up every
possible use case and write tests to cover them. The tests are first conducted in our local development environment, and
then they are tested after being deployed on AWS.

#### Test Link

- [Users Test](../tests/test_func_user.py)
- [Words Test](../tests/test_func_word.py)

#### How to Run the Code

1. Change the URl of endpoints in base.py
2. Use command `pytest`

#### Test Results

<img src="./images/test_func_user.png" width="400" alt="Test Result of test_func_user">
<img src="./images/test_func_word.png" width="400" alt="Test Result of test_fuc_word"> <br>

### CLI Tool Evaluation

### Test Plan

We tested the CLI tool manually, as it we want to test the user experience and
the functionality of the CLI tool. We designed 15 usage cases, and test them one by one. The detailed test
cases are in [Test Cases](./cli_tool_test_logs.md).

### Test Record

- [Test Record](./cli_tool_test_logs.md)

#### Test Results

All cases passed.

### Availability Tests

#### Test Plan

The following tests aim to determine the longevity of the service. Due to time limitation, we test whether our
application can run for a full day, checking if the health endpoints of each API hourly.

#### Test Link

- [Availability Test](../tests/test_availability.py)

#### Test Result

Our services were able to run uninterupted for a full 24 hours, with some testing activity occuring during that
time.<br>
<img src="./images/test_func_word.png" width="400" alt="Test Result of test_fuc_word"> <br>

### Maintainability Tests

#### Test Plan

We make some changed in both users and words services and update the container version, they used `terraform apply` to
deploy latest update.

#### Test Workflow & Result

Before maintenance, we record the current revision, in this case, revision = 3.<br>
<img src="./images/maintain_1.png" width="600" alt="Before Maintenance"><br>
Then, we update codes and use Terraform to update.<br>
<img src="./images/maintain_2.png" width="600" alt="Update Requests"><br>
During maintenance, a new task (revision = 4) is initialized.<br>
<img src="./images/maintain_3.png" width="600" alt="While Maintenance"><br>
After maintenance, only one instance with revision = 4 exists.<br>
<img src="./images/maintain_4.png" width="600" alt="After Maintenance"><br>

As shown above, tests passed.

### Scalability Tests

#### Test Plan

We test how our architecture handles high loads. Using K6, we created one virtual user (VU) who signs in, logins, adds a
new word, gets the word and studies it. At first, we tried to push the APIs to the limit, we ran the test for a total of
12 minutes with a ramping scale up with the follow values:

- 4 minutes, target 1000
- 4 minutes, target 2500
- 4 minutes, target 0

This test was able to manage very high loads, but we hit maximum instances of 22 total. After this we created a more
suitable test which ran for a total of 28 minutes which had a maximum of 667 virtual users. It had a ramping scale with
the following values:

- 4 minutes, targe 200
- 6 minutes, target 400
- 6 minutes, target 667
- 6 minutes, target 400
- 4 minutes, target 200
- 2 minutes, target 50

#### Test Link

- [Scalability Test](../tests/test_scalability.js)

#### Test Results

For the first scenario of 2500 VUs max:<br>
<img src="./images/test_scalability_2.png" width="600" alt="Scenario 1 of scalability tests"><br>

For the second scenario:<br>
<img src="./images/test_scalability.png" width="600" alt="Scenario 2 of scalability tests"><br>
At the max VUs the performance and instances of the services are shown here.<br>
<img src="./images/user_service.png" width="600" alt="Scenario 2 user service "><br>
<img src="./images/word_service.png" width="600" alt="Scenario 2 of word service"><br>

## Reflections

During the process of designing and implementing the project proposal for the "Don't Remember" application, We have
learned several valuable lessons that would influence our approach in future projects. The biggest learning experience
was the process of designing the architecture and how to test it. When given the project proposal, the presense of
quality attributes greatly helped deliver a quality product. Without it, we would have struggled to find the best
solution to deliver the functionality. We were able to make important changes to the implementation and architecture by
considering how we would be able to deliver and test the quality attributes. This allowed us to design for the future.
Additionally, designing an architecture first proved to make development substantially easier and also made it easier to
split tasks between team members. For future projects, we will be using quality attributes and designing architecture to
achieve the best implementation, as this project proves how beneficial it can be.

In the architecture design aspect, previously we only studied others' mature architectures from a case-study perspective.
Through this project, we found that we would encounter many problems in the software architecture design and development
process. For example, when implementing the functions, we found that many details were not considered in the
architecture design. In addition to the software architecture design, we also revised the product architecture during
the implementation process. Because software implementation is not only based on the software architecture but also on
real user scenarios, the design of the whole product is also very important. In the product architecture design, we
sorted out our main functions, user scenarios, user processes, and the feedback corresponding to each user action when
interacting with the software. These designs were very useful in the software implementation and the subsequent testing
sessions. If we have the opportunity to do a similar project next time, we believe we will do a good job of product
design at the beginning, which will make the subsequent development and testing more efficient.

In our API design, although we initially decided to introduce tokens to ensure security, our lack of understanding
regarding tokens led to frequent changes in our strategy, resulting in a significant waste of time. Moreover, the lack
of a test-driven approach throughout the entire project meant that we discovered numerous issues during testing,
necessitating revisiting the codebase for modifications. This led to an escalation in development costs.

Another important learning experience was setting up test suites. At the start, we only implemented these as a requirement
to demonstrate our evaluations. It was assumed that it was going to be another functionality we had to deliver. However,
once we implemented this, we noticed how much time it saved us in the long run. By writing the tests, we were able to
debug early. And by ensuring the functionality worked after every change, it freed other developers working on different
aspects of the project from having to debug their code and the code of others. This was apparent during the development
of the CLI tool, where we had already created the API functionality and its test suites. We only had to debug the CLI
tool, as we knew that the functionality can already deliver everything in the tests.

For what we could do differently, first, we should have focused more on the overall product design at the beginning,
which would have made development and testing more efficient later on. Secondly, I think there is one thing we could
have done better. It is that we didn't estimate the user volume at the beginning. Although we passed the load test
perfectly in the end, it was probably just luck. Next time, we should consider the user volume in advance and use it as
an assumption in designing the architecture to avoid wasting development and deployment costs. Apart from that, we would
start testing much earlier. Preferably during the development of the functionality. As when we wrote the tests after
finishing writing the functionality, there were a lot of errors. And some developers were writing other pieces of the
functionality, that depended on other functionality, and became stuck. Another way to improve in the future is to use GitHub
actions to automate tests on the repository. Running the tests was expected of the developers, but not enforced. And to
ensure that nothing slipped through the cracks, automated tests on our repository after every push could help us catch
errors early.

Finally, thank you to the professor and tutors for guiding this project, and thank you to the team members for their
contributions.