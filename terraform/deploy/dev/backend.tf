terraform {
  backend "s3" {
    bucket  = "your-bucket-for-terraform-backend"
    key     = "your-key-for-terraform-backend/dev/terraform.tfstate"
    region  = "us-east-1"
    encrypt = "true"
  }
}
