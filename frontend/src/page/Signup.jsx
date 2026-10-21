import { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

function Signup() {

  const [name,setName] = useState("");
  const [email,setEmail] = useState("");
  const [mobile,setMobile] = useState("");
  const [password,setPassword] = useState("");
  const [confirmPassword,setConfirmPassword] = useState("");

  const handleSignup = async () => {

    if(!name || !email || !mobile || !password || !confirmPassword){
      alert("Please fill all fields");
      return;
    }

    if(password !== confirmPassword){
      alert("Passwords do not match");
      return;
    }

   try {
  const res =  await axios.post("http://127.0.0.1:5000/api/users/signup", {
  name,
  email,
  mobile,
  password,
});


  alert(res.data.message);

}  catch (error) {
  console.log("Full Error:", error);
  console.log("Response:", error.response);
  console.log("Request:", error.request);
  console.log("Message:", error.message);

  alert(error.message);

}

  };


  return (
    <div style={{ maxWidth:"400px", margin:"50px auto", padding:"20px" }}>

      <h1>Create Account</h1>

      <input 
      type="text"
      placeholder="Full Name"
      value={name}
      onChange={(e)=>setName(e.target.value)}
      />
      <br/><br/>


      <input 
      type="email"
      placeholder="Email"
      value={email}
      onChange={(e)=>setEmail(e.target.value)}
      />
      <br/><br/>


      <input 
      type="tel"
      placeholder="Mobile Number"
      value={mobile}
      onChange={(e)=>setMobile(e.target.value)}
      />
      <br/><br/>


      <input 
      type="password"
      placeholder="Password"
      value={password}
      onChange={(e)=>setPassword(e.target.value)}
      />
      <br/><br/>


      <input 
      type="password"
      placeholder="Confirm Password"
      value={confirmPassword}
      onChange={(e)=>setConfirmPassword(e.target.value)}
      />
      <br/><br/>


      <button onClick={handleSignup}>
        Sign Up
      </button>


      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>

    </div>
  );
}

export default Signup;