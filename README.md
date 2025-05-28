# Magazine Articles Management

## Project Overview

This project manages information about **Authors**, **Magazines**, and **Articles**. It uses a SQLite database to persist data with three main tables:

- **authors**: Stores author details (id, name).
- **magazines**: Stores magazine details (id, name, category).
- **articles**: Stores articles with title, author reference, and magazine reference.

The relationships are:
- Each article is written by an author (`author_id` references `authors.id`).
- Each article belongs to a magazine (`magazine_id` references `magazines.id`).

The project includes Python classes for each entity (`Author`, `Magazine`, `Article`) that provide methods to create, update, delete, and query the database.

---

## Installation

Follow these steps to set up the project on your local machine:

### Prerequisites

- Python 3.8+ installed
- `sqlite3` installed (comes with Python by default)
- `pytest` for running tests

### Steps

1. **Clone the repository** (or download the project files):

   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>
