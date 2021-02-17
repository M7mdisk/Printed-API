import React, { useState, useEffect, useContext } from 'react';
import { GetProfileData } from '../api/rest.js'
import { UserContext } from '../contexts/userContext.js'

function FilledProfileData() {
    // eslint-disable-next-line no-unused-vars
    const {user, setUser, isUserLoggedIn} = useContext(UserContext)
    const [Profileinfo, setProfileInfo] = useState();
    const [isFetching, setIsFetching] = useState(true);
    // const testPing = () => {
    //     GetProfileData()
    //   .then((data)=>{
    //     setPingResult(data.id)
    //   }).catch((error)=> {
    //     setUser(null);
    //   });
    // }

    useEffect(() => {
        setIsFetching(true);
        GetProfileData()
      .then((data)=>{
        console.log(data)

        setProfileInfo(data)
        console.log(Profileinfo)
        setIsFetching(false);
      }).catch((error)=> {
        setUser(null);
      });      },[]);
      console.log(Profileinfo)
      return (
        <div className="flex flex-col items-center mt-6 -mx-2">
            {isFetching ? <><p>loading</p></>:<>
        <img className="object-cover w-24 h-24 mx-2 rounded-full" src={Profileinfo.photo_url} alt="avatar"/>
        <h4 className="mx-2 mt-2 font-medium text-gray-800 dark:text-gray-200 hover:underline">{Profileinfo["first_name"] +" "+Profileinfo["last_name"]  }</h4>
        <p className="mx-2 mt-1 text-sm font-medium text-gray-600 dark:text-gray-400 hover:underline">{Profileinfo["email"]}</p> </>
            }
        </div>
    )
  }
  
  export default FilledProfileData;
  