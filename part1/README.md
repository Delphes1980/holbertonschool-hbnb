# HBnB Evolution : Technical Documentation
This repository contains the comprehensive technical documentation for the initial phase of the HBnB Evolution application, a simplified AirBnB-like platform.
This documentation serves as the foundational design blueprint for subsequent development phases, focusing on understanding the overall architecture, detailed business logic, and system interactions.

# 🛠️ Project Overview
HBnB Evolution is an application designed to facilitate user management, property listings, and review functionalities. This initial phase focuses on defining the architectural and design aspects to ensure a solid and well-understood foundation for development.

# ✏️ Core Functionalities
The application supports the following primary operations:

- User Management: Registering users, updating profiles, and differentiating between regular users and administrators.
- Place Management: Listing user-owned properties with details (name, description, price, location) and associated amenities.
- Review Management: Users leaving reviews (rating, comment) for visited places.
- Amenity Management: Managing available amenities that can be linked to places.

# ⚙️ Key Business Rules & Entities
All entities are uniquely identified by an ID and track creation/update timestamps for audit purposes.

- User: first_name, last_name, email, password, is_admin (boolean). Users can be registered, updated, and deleted.
- Place: title, description, price, latitude, longitude. Associated with an owner (User) and can have a list of amenities. Can be created, updated, deleted, and listed.
- Review: rating, comment. Associated with a specific place and user. Can be created, updated, deleted, and listed by place.
- Amenity: name, description. Can be created, updated, deleted, and listed.

# 📂 Architecture
The application adheres to a three-layered architecture to ensure modularity, maintainability, and scalability:

- Presentation Layer: Handles user interaction, API endpoints, input validation, and data serialization/deserialization.
- Business Logic Layer (BLL): Contains the core application logic, models, complex operations orchestration, and ensures data consistency.
- Persistence Layer: Responsible for all data storage and retrieval operations with the database.

# 📖 Documentation Deliverables
This phase delivers the following UML diagrams and accompanying explanatory notes:

- High-Level Package Diagram: Illustrating the three-layer architecture and inter-layer communication via the facade pattern.
- Detailed Class Diagram (Business Logic Layer): Focusing on User, Place, Review, and Amenity entities, including attributes, methods, and relationships.
- Sequence Diagrams (for API Calls):
	- User Registration
	- Place Creation
	- Review Submission
	- Fetching a List of Places
	- User Loggin

## 🧑‍💻 Authors
- [Delphine Coutouly-Laborda](https://github.com/Delphes1980)
- [Xavier Laforgue](https://github.com/XavierLaforgue)