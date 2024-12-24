[
  {
    "name": "shitts-app",
    "image": "${docker_image_url_django}",
    "essential": true,
    "cpu": 10,
    "memory": 512,
    "portMappings": [
      {
        "containerPort": 8000,
        "protocol": "tcp"
      }
    ],
    "command": ["gunicorn", "-w", "3", "-b", ":8000", "shitts-app.wsgi:application"],
    "environment": [],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/shitts-app",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "shitts-app-log-stream"
      }
    }
  }
]
