import axios from "axios";
import { userStore } from "@/store/user";
import router from "@/router";


async function loginRequest(loginData) {
  const user = userStore();
  const authApi = "http://192.168.131.2:5000";
  return axios
    .post(`${authApi}/login`, loginData)
    .then((resp) => {
      const u = resp.data
      user.userId = u.userId;
      user.username = u.username;
      user.first_name = u.first_name;
      user.last_name = u.last_name;
      user.email = u.email;
      user.connections = u.connections;
      sessionStorage.setItem("city_park_token", u.token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${u.token}`;
    })
}

async function tokenCheck(token) {
  const user = userStore();
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  const authApi = "http://192.168.131.2:5000";
  return axios
    .get(`${authApi}/user`)
    .then((resp) => {
      const u = resp.data
      user.userId = u.userId;
      user.username = u.username;
      user.first_name = u.first_name;
      user.last_name = u.last_name;
      user.connections = u.connections;
      user.email = u.email;
      user.loggedIn = true;
      router.push("/")
      return resp;
    })
    .catch((err) => {
      // TODO: notify user, back to login screen.
      axios.defaults.headers.common['Authorization'] = ``;
      router.push("/login")
      return err;
    })
  // TODO: if token is valid set the axios interceptor
  // axios interceptor
}

// async function loadUserData(token) {
//   console.log("User Data Request");
//   const user = userStore();
//   // axios request to backend to get the user data with the token
//   user.username = "Rinz";
//   user.firstName = "Jacob";
//   user.lastName = "Edmonson";
//   user.email = "Sample Email";
// }

export { loginRequest, tokenCheck };
