# 1. Independent Business Logic

Date: 2023-04-26

## Status

superseded

## Summary

In the context of delivering an application with multiple frontends such as a web app and mobile app to support
different software systems, we decided to relocate the business logic from the frontend to the backend. Consequently, we
transitioned the frontend microkernel architecture to a microservice architecture and utilized RESTful API for
communication between the frontend and backend. The frontend was chosen to be implemented using React because it can
support multiple platforms with minor modifications, thereby decreasing development costs.

## Context

- The system should support both mobile and web application frontends.
- The user experience should be consistent across platforms.
- The development team has experience and is willing to specialize in the backend field.

## Decision

- The system should be implemented using a microservice architecture.
- The microservice is divided into two services, 'words' which is responsible for word-related operations, and 'users'
  which handles user-related operations.
    - The partition is determined based on both technical and domain considerations.
- The frontend should be implemented using React.
- The backend should be implemented with the Python library, Flask.
- Deployment should be done using Docker on AWS with Terraform for autoscaling.
- The database should be implemented with PostgreSQL.

## Consequences

Advantages:

- Business logics are relocated to the backend, making them usable across different frontends.
- Lighter load on the frontend.
- The backend can be scaled independently.
- Using React for the frontend can decrease deployment costs.

## Disadvantages

- The development team has limited experience with frontend frameworks, particularly React.
- The development costs are higher than those for a monolithic architecture.
- Clients can be used only when internet is connected.