terraform {

  cloud {

    organization = "freyestoledo-org"

    workspaces {

      name = "week12-mc-project"

    }

  }



  required_providers {

    aws = {

      source = "hashicorp/aws"

      version = "~> 5.0"

    }

  }



  required_version = ">= 0.14.9"

}



provider "aws" {

  region = "us-east-1"

}


data "aws_iam_role" "lab_role" {

  name = "LabRole"

}


resource "aws_lambda_function" "start_lambda" {

  filename = "startEC2.zip"

  function_name = "startEC2_Fabian"

  role = data.aws_iam_role.lab_role.arn

  runtime = "python3.9"

  handler = "startEC2.lambda_handler"

}
