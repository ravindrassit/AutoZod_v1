import os
import sys
import subprocess

def deploy(port):
    if port == 9000:
        print("Deploying Development Environment...")
        compose_file = "docker-compose.dev.yml"
    elif port == 9001:
        print("Deploying Staging Environment...")
        compose_file = "docker-compose.staging.yml"
    elif port == 9002:
        print("Deploying Production Environment...")
        compose_file = "docker-compose.prod.yml"
    else:
        print("Invalid port. Please use 9000 for development, 9001 for staging, or 9002 for production.")
        sys.exit(1)

    # Run the Docker Compose command
    subprocess.run(["docker-compose", "-f", compose_file, "up", "-d"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        deploy(port)
    except ValueError:
        print("Please enter a valid port number.")
        sys.exit(1)
