import { authRequest } from './auth.js'

const ping = () => {
  const extraParameters = {params: {"id": "PONG" }}
  return authRequest.get('/api/ping/',extraParameters)
    .then(response=>{
      return Promise.resolve(response.data)
    }).catch((error)=> {
      return Promise.reject(error)
    });
}


const GetProfileData = () => {
  const extraParameters = {params: {"id": "PONG" }}
  return authRequest.get('/api/myaccount')
    .then(response=>{
      return Promise.resolve(response.data)
    }).catch((error)=> {
      return Promise.reject(error)
    });
}



export { ping,GetProfileData }
