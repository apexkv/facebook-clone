# Facebook Clone

The **Facebook Clone System** is a highly scalable, distributed, and microservices-based architecture designed to mimic the core features of a social networking platform. The architecture is divided into several microservices, each responsible for specific functionalities like user management, posts, friendships, chat, comments, likes, notifications, and search. The system leverages modern technologies and best practices to ensure high performance, scalability, and maintainability.

### Microservices and Components

-   #### Next.js Frontend:

    -   The frontend of the application is built with Next.js, providing a responsive and dynamic user interface. It interacts with the backend through the Nginx API Gateway.

-   #### Nginx API Gateway:
    -   Acts as the central entry point for all client requests, routing them to the appropriate microservices. It handles cross-cutting concerns like authentication, rate limiting, and load balancing.
-   #### User Microservice:

    -   **Database:** MySQL
    -   **Description:** Manages user authentication, profile management, and stores user-related data such as user ID, name, and profile picture URL.
    -   **Caching:** Redis is used to cache frequently accessed user data to enhance performance.
    -   **Communication:** Integrates with RabbitMQ for asynchronous messaging and interacts with other microservices as needed.

-   #### Post Microservice:

    -   **Database:** MySQL
    -   **Description:** Handles the creation, retrieval, and storage of posts, including shared posts. It also references user data.
    -   **Caching:** Redis is used to optimize feed delivery and reduce database load.
    -   **Communication:** Uses RabbitMQ for messaging and depends on the Friendship and User microservices for data synchronization.

-   #### Friendship Microservice:

    -   **Database:** Neo4j
    -   **Description:** Manages user friendships, enabling complex queries such as mutual friends and friend connections.
    -   **Caching:** Redis is used to improve performance by caching friendship data.
    -   **Communication:** Relies on RabbitMQ for messaging and interacts with the Post microservice.

-   #### Chat Microservice:

    -   **Database:** MongoDB
    -   **Description:** Provides real-time messaging functionality between users. It stores chat data and utilizes Socket.io for real-time communication.
    -   **Caching:** Redis is used to manage session data.
    -   **Communication:** Connects to the User microservice and uses RabbitMQ for messaging.

-   #### Comments Microservice:

    -   **Database:** Neo4j
    -   **Description:** Handles comments on posts, including replies, and links them to the relevant user and post data.
    -   **Caching:** Redis is used to improve the retrieval speed of comments.
    -   **Communication:** Relies on RabbitMQ and interacts with the User and Post microservices.

-   #### Likes Microservice:

    -   **Database:** Neo4j
    -   **Description:** Manages likes on posts and comments, linking them to users, posts, and comments.
    -   **Caching:** Redis is used to cache like data, enhancing performance.
    -   **Communication:** Uses RabbitMQ and connects with the User, Post, and Comments microservices.

-   #### Notifications Microservice:

    -   **Database:** MongoDB
    -   **Description:** Manages user notifications, such as friend activity and post interactions.
    -   **Caching:** Redis is used to cache notifications for quick retrieval.
    -   **Communication:** Uses RabbitMQ and interacts with the User microservice.

-   #### Search Microservice:
    -   **Database:** Elasticsearch
    -   **Description:** Implements search functionality, allowing users to search for friends and posts. Elasticsearch is used for its powerful full-text search capabilities.
    -   **Caching:** Redis is used to cache search results, reducing the load on Elasticsearch.
    -   **Communication:** Utilizes RabbitMQ for messaging and connects with the User and Post microservices.

### Shared Services

-   #### RabbitMQ:

    -   Acts as the messaging backbone of the system, facilitating asynchronous communication between microservices, ensuring loose coupling, and enabling event-driven architecture.

-   #### Redis:
    -   Employed across multiple microservices as a caching layer to optimize performance and reduce database load.

### Architecture Diagram

![Facebook Clone Architecture](./Facebook%20Clone%20System%20Architecture.png)
