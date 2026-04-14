# Ticketing System

##  Project Overview
This project is a web-based Ticketing System designed to simulate a real-world IT support/helpdesk workflow. It allows users to create, manage, and track support tickets, while administrators handle issue resolution and system oversight.

The system demonstrates full-stack development concepts, role-based access control, cloud deployment, and automated deployment workflows.

---

##  Key Features
- User authentication and role-based access control (User / Admin)
- Ticket creation, updating, and deletion
- Ticket status tracking (e.g., Open, In Progress, Resolved)
- Priority assignment for tickets
- Admin dashboard for managing all tickets
- Structured workflow for issue resolution

---

##  Cloud Deployment (AWS EC2)
The application was deployed on an **Amazon Web Services (AWS) EC2 instance**, providing a cloud-based environment for hosting the backend system.

The EC2 instance served as the runtime environment for:
- The Flask backend application
- The application database (or database-connected services)
- Webhook-based deployment automation

---

##  Webhook-Based Auto Deployment

This project includes a webhook-based automation script that enables lightweight continuous deployment.

A Flask-based webhook service listens for POST requests on a dedicated endpoint (`/update`). When triggered, it automatically:

- Pulls the latest code from the Git repository on the EC2 instance
- Stops the currently running application process
- Restarts the application with the updated codebase

This simulates a basic CI/CD pipeline by automating deployment steps without manual server intervention.

---

##  Technologies Used
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Database: (MySQL / SQLite – hosted or connected via EC2 environment)
- Cloud: Amazon AWS EC2
- Version Control: Git / GitHub
- Deployment: Linux (Ubuntu on EC2)

---

##  My Contributions
This project was completed in a group. My specific contributions include:

- Developed core ticket management functionality (create, update, and track tickets)
- Implemented ticket status workflow and priority handling
- Configured and deployed the application on AWS EC2
- Built webhook-based automation for deployment updates
- Assisted with backend debugging and system integration
- Contributed to testing and validation of application features

---

##  Key Learnings
- Cloud deployment using AWS EC2
- Full-stack application architecture
- Role-based access control systems
- Webhook-based automation and deployment workflows
- Linux server management and process handling
- Collaborative development using Git and GitHub

---

##  Future Improvements
- Use Docker or systemd for safer deployment management
- Move to managed AWS services (RDS for database, Elastic Beanstalk for deployment)
- Add email/notification system for ticket updates
- Improve UI/UX design for dashboard interface
- Add logging and monitoring for webhook events
