import axios from "axios";
import { userStore } from "@/store/user";
import router from "@/router";

const AUTH_SERVICE = import.meta.env.VITE_AUTH_SERVICE;

/**
 * Login request method which posts to a predefined endpoint.
 * @memberof store.user
 * @param {Object} loginData
 * @param {String} loginData.user_name User's username
 * @param {String} loginData.password User's password
 * @returns {Promise}
 */
async function loginRequest(loginData) {
  const user = userStore();
  return axios.post(`${AUTH_SERVICE}/login`, loginData).then((resp) => {
    const u = resp.data;
    user.user_id = u.user_id;
    user.user_name = u.user_name;
    user.first_name = u.first_name;
    user.last_name = u.last_name;
    user.email = u.email;
    user.connections = u.connections;
    sessionStorage.setItem("city_park_token", u.token);
    axios.defaults.headers.common["Authorization"] = `Bearer ${u.token}`;
  });
}

/**
 * Sets axios authorization header and hits the backend to check and see
 * if the token is valid.
 * @memberof store.user
 * @param {String} Token Token String
 * @returns {Promise} JSON response
 */
async function tokenCheck(token) {
  console.log("Conducting Token Check");
  const user = userStore();
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  return axios
    .get(`${AUTH_SERVICE}/user`)
    .then((resp) => {
      const u = resp.data;
      user.user_id = u.user_id;
      user.user_name = u.user_name;
      user.first_name = u.first_name;
      user.last_name = u.last_name;
      user.connections = u.connections;
      user.email = u.email;
      user.loggedIn = true;
      router.push("/");
      return resp;
    })
    .catch((err) => {
      // TODO: notify user, back to login screen.
      axios.defaults.headers.common["Authorization"] = ``;
      router.push("/login");
      return err;
    });
  // TODO: if token is valid set the axios interceptor
  // axios interceptor
}
export { loginRequest, tokenCheck };
