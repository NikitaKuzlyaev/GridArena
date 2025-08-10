![Image](https://github.com/NikitaKuzlyaev/quiz/blob/master/git-staff/pick4.png?raw=true)

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-0ba37f?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-e535ab?logo=python&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-4B8BBE?logo=python)
![Redis](https://img.shields.io/badge/Redis-Cache%20%2F%20PubSub-dc382d?logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Messaging-ff6600?logo=rabbitmq&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)
![pip](https://img.shields.io/badge/pip-Dependencies-blue?logo=python&logoColor=white)

## GridArena – platform for hosting intellectual competitions

A lightweight and fast online platform for hosting intellectual competitions in a unique format. Fully supports real-time gameplay.

> ⚠️ Currently, only the Russian interface 🇷🇺 is supported.


## 🚀 Features

### 🎮 General Mechanics

- The game board consists of **cards**, each linked to a task.  
- Participants can **purchase cards** to unlock tasks.  
- For **correct solutions**, players earn points:  
  - Faster and fewer attempts yield more points.  
  - Scoring rules are customizable per competition.  
  - Players usually hold multiple tasks simultaneously.  
- Play can be team-based (several people on one computer) or individual.

### 👤 Roles

#### Competition Managers
- Create and manage competitions.  
- Configure board, cards, and tasks.  
- Define scoring rules.  
- Add and manage participants.

#### Participants
- Join competitions with manager-provided credentials.  
- Buy cards, solve tasks, earn points.  
- Compete in real time.  
- Track progress via an **interactive scoreboard**.

### 📊 Scoreboard

- Displays current scores of participants and/or teams.  
- Updates in **real time**.  
- Visualizes competition progress and rivalry.  


### Preview (participant’s view of the competition page)
![Image](https://github.com/NikitaKuzlyaev/quiz/blob/master/git-staff/pick2.jpg?raw=true)

## 🧑‍🏫 Who Is It For?

Designed for **schools, universities, teachers, and competition organizers**, but adaptable for clubs, hackathons, and other events.  
Use it to host themed competitions, gamified lessons, exams, or tournaments on any topic — from physics to programming.

---

## ✅ Current Status

Core functionality is ready and usable:

- **Role-based access**:
  - Admins: manage competitions, participants, scoring rules, and statistics.
  - Participants: compete in assigned events without self-registration.
- **JWT authentication** with token blacklisting.  
- **Flexible permissions** at API and service levels.  
- **Smart exception handling** with developer/user-friendly messages.  
- **Caching** for key data to reduce DB load.  
- **Markdown support** for tasks.  
- **UI themes**, including a playful pink variant.

---

## 🛠️ Roadmap

- **Architecture & Code**: refactoring, config separation, DB optimization, unified permission checks, async solution checking.  
- **Integrations**: monitoring (Grafana, Prometheus, Elasticsearch), advanced queues (Dramatiq/Celery), nginx and security hardening.  
- **Features**: more admin APIs, action logs for participants, detailed game history.  
- **Docs & Deployment**: proper README and deployment plan.  


## 🧰 Technology Stack

| Category              | Technologies                                     |
|-----------------------|--------------------------------------------------|
| Programming Language  | Python 🐍                                        |
| Backend Framework     | FastAPI 🚀                                       |
| Database              | PostgreSQL 🐘                                    |
| ORM & Migrations      | SQLAlchemy 2.0, Alembic                          |
| Message Queue         | RabbitMQ 🐇                                      |
| Cache / PubSub        | Redis ⚡                                         |
| Containerization      | Docker 🐳                                        |
| Frontend              | React ⚛️, Vite ⚡                                 |
| Dependencies (Python) | pip + requirements.txt                           |

Planned:
- Dramatiq / Celery;
- Grafana, Prometheus, Elasticsearch (for monitoring and logging).

---
