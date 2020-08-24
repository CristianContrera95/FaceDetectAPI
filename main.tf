terraform {
  required_providers {
    docker = {
      source = "terraform-providers/docker"
    }
  }
}

provider "docker" {}

resource "docker_image" "face_recognition_api" {
  name         = "face_recognition_api:v1"
  keep_locally = true
}

resource "docker_container" "face_recognition_api" {
  image = docker_image.face_recognition_api.latest
  name  = "face_recognition_api"
  rm    = true
  env   = ["ENVIRONMENT=dev"]
  ports {
    internal = 5000
    external = 5000
  }

}