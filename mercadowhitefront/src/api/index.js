import axios from "axios";

const ENDPOINT_PATH = "https://api.escuelajs.co/api/v1/";


    /// SESSION ///

    //Login
export function login(email, password) {
  const user = { email, password };
  return axios.post(ENDPOINT_PATH + "regiser", user);
}

    //Register
export function register(email, password) {
  const user = { email, password };
  return axios.post(ENDPOINT_PATH + "regiser", user);
}

    /// PRODUCTS ///

export function getAllCategories(){
  return axios.get(ENDPOINT_PATH + "categories");
}
