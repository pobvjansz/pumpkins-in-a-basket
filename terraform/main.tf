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

resource "restapi_object" "test_4433" {
  path = "/pumpkins"
  data = "{ \"id\": 4433, \"removePumpkin\": false, \"type\": \"JAPANESE\" }"
  debug = true
}

#data "restapi_object" "test" {
#  path="/pumpkins"
#  search_key = "id"
#  search_value = "4433"
#  debug=true
#}
