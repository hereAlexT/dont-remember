data "aws_ecr_authorization_token" "ecr_token" {}

provider "docker" {
  registry_auth {
    address  = data.aws_ecr_authorization_token.ecr_token.proxy_endpoint
    username = data.aws_ecr_authorization_token.ecr_token.user_name
    password = data.aws_ecr_authorization_token.ecr_token.password
  }
}

resource "aws_ecr_repository" "users" {
  name = "users"
}

resource "aws_ecr_repository" "words" {
  name = "words"
}


resource "docker_image" "users" {
  name = "${aws_ecr_repository.users.repository_url}:${var.image_version}"
  build {
    context = "../users"
    platform  = "linux/amd64"
  }
}

resource "docker_image" "words" {
  name = "${aws_ecr_repository.words.repository_url}:${var.image_version}"
  build {
    context = "../words"
    platform  = "linux/amd64"
  }
}

resource "docker_registry_image" "user" {
  name = docker_image.users.name
}
resource "docker_registry_image" "words" {
  name = docker_image.words.name
}
