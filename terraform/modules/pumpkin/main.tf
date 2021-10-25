terraform {
  required_providers {
    restapi = {
      source = "fmontezuma/restapi"
      version = "1.14.1"
    }
  }
}

provider "restapi" {
  uri                  = "http://127.0.0.1:5000"
  debug                = true
  write_returns_object = true
}

resource "restapi_object" "pumpkin_id" {
  path = "/pumpkins"
  data = "{ \"id\": ${var.pumpkin_id}, \"removePumpkin\": false, \"type\": \"${var.pumpkin_type}\" }"
  debug = true
}

#data "restapi_object" "test" {
#  path="/pumpkins"
#  search_key = "id"
#  search_value = "4433"
#  debug=true
#}
