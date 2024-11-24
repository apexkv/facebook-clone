# **Facebook-Clone Project**

## **Overview**

This project is a feature-rich, scalable social media platform inspired by Facebook, designed to showcase advanced skills in **microservices architecture**, **machine learning-powered recommendations**, and **high-performance backend engineering**. Built with a modern tech stack, it demonstrates strategic and technical expertise in designing and implementing **scalable, maintainable, and production-ready systems**.

---

## **Features**

### **1. Core Social Media Functionalities**

-   **Post Management**:
    -   Users can create posts with rich content support.
    -   Features for liking posts and adding comments, fostering user interaction.
-   **Comment Management**:
    -   Nested commenting system with the ability to like individual comments.
-   **Friendship Management**:
    -   Friend requests and friend acceptance/rejection workflows.
    -   Relationship graph using **Neo4j** for efficient querying of friendships and mutual connections.

### **2. AI-Powered Post Recommendation System**

-   **Machine Learning Integration**:
    -   Implemented a recommendation system that suggests posts to users based on their interaction history and preferences.
    -   The model leverages **post likes, comments, and user activity** to provide personalized recommendations.
-   **Scheduled Training**:
    -   Used **Celery** for periodic retraining of the recommendation model with fresh interaction data.
    -   Ensures recommendations adapt dynamically to changing user behavior.

### **3. High-Performance System Design**

-   **Microservices Architecture**:
    -   Built multiple independent microservices, each handling a specific domain:
        -   **User Microservice**: Handles user authentication and profile management.
        -   **Post Microservice**: Manages posts, comments, and interactions.
        -   **Friendship Microservice**: Manages friend requests, connections, and graph-based queries.
-   **Caching for Scalability**:
    -   Implemented **Redis caching** in each microservice to minimize database load and reduce latency for frequently accessed data.
-   **API Gateway**:
    -   Designed an **NGINX-based API Gateway** for centralized routing and load balancing across microservices.

### **4. Frontend**

-   Built a responsive and intuitive frontend using **Next.js**, delivering a seamless user experience across devices.

---

## **Tech Stack**

### **Backend**

-   **Django**: Backend framework for all microservices, leveraging its modularity and rapid development capabilities.
-   **PostgreSQL**: Primary database for structured data storage in User and Post microservices.
-   **Neo4j**: Graph database used in the Friendship microservice to efficiently manage and query complex relationships.

### **Frontend**

-   **Next.js**: React-based framework for building a fast, server-side rendered user interface.

### **Caching & Queueing**

-   **Redis**: Caching layer for improving response times and reducing database load.
-   **Celery**: Task queue for managing asynchronous tasks like periodic model training.

### **API Gateway**

-   **NGINX**: Reverse proxy for managing API requests, ensuring secure and efficient communication between microservices.

### **Machine Learning**

-   **Scikit-learn**: For training and deploying the recommendation model.
-   **TF-IDF Vectorization**: Used for transforming post content into numerical features.
<!--
--- -->

## **System Architecture**

<!-- ![System Architecture Diagram](https://via.placeholder.com/800x400?text=Architecture+Diagram) -->

1. **User Microservice**:

    - Handles user registration, login, and profile management.
    - Provides JWT-based authentication for secure inter-service communication.

2. **Post Microservice**:

    - Manages posts, comments, and likes.
    - Implements a machine learning pipeline for post recommendations.

3. **Friendship Microservice**:

    - Manages friend requests and user connections.
    - Uses **Neo4j** to handle relationship graphs efficiently.

4. **API Gateway**:
    - NGINX routes requests to the appropriate microservice.
    - Ensures scalability and isolates backend services from direct client access.

---

## **Key Highlights**

### **Scalability and Performance**

-   Designed with a **microservices-first approach**, ensuring modularity and ease of scaling.
-   Leveraged **Redis caching** and **NGINX load balancing** to handle high traffic with low latency.

### **Machine Learning Innovation**

-   Developed a robust recommendation system that periodically retrains itself using **user interaction data**.
-   Combined content-based filtering with collaborative filtering techniques to enhance recommendation quality.

### **Graph-Powered Relationships**

-   Used **Neo4j** to model friendships and connections, enabling fast and complex queries for features like mutual friends and friend suggestions.

### **DevOps and Deployment**

-   Containerized all microservices using **Docker**, ensuring seamless development and deployment workflows.
-   Configured **Celery** workers to handle background tasks and scheduled jobs, ensuring system stability.

---

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/apexkv/facebook-clone.git
cd facebook-clone
```

### **2. Set Up Environment Variables**

-   Configure `.env` files for each microservice with the necessary database and service credentials.

### **3. Start Services**

-   **Start Docker containers** for all services:
    ```bash
    docker-compose up --build
    ```
-   This will automatically run all the features of the system.

---

## **Future Enhancements**

-   **Expand Recommendation System**:
    -   Incorporate more advanced models like Transformers for post content understanding.
    -   Introduce real-time recommendation updates.
-   **Analytics Dashboard**:
    -   Provide insights into user behavior and engagement metrics.
-   **Notification Microservice**:
    -   Implement a dedicated service for handling user notifications.

---

## **Contributions**

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss your ideas.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README showcases your **technical skills** and ability to design and implement a complex, scalable, and intelligent system. It also reflects your ability to use advanced technologies effectively, setting you apart from typical 2nd-year software engineering students.
