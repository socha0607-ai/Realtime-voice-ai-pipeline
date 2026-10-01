```markdown
# Live USB Setup & Terminal Commands Guide

This file contains all exact terminal commands needed to set up, build, test, and push this repository inside an Ubuntu Live environment.

---

## 1. System Setup (Ubuntu Live Session)

Run these commands first inside your Ubuntu terminal:

```bash
# Update package manager
sudo apt update

# Install Git, Python, Pip, and Curl
sudo apt install -y git python3-pip python3-venv curl docker.io

# Start and enable Docker service
sudo systemctl start docker
sudo usermod -aG docker $USER
